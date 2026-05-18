# llm-bench

Side-by-side coding benchmark in iTerm2. Hosted Claude vs two self-hosted boxes, same prompt, same canonical specs.

| Pane        | Endpoint                     | Hardware                              | Model                                      |
|-------------|------------------------------|---------------------------------------|--------------------------------------------|
| `claude`    | Anthropic Messages API       | hosted                                | `claude-sonnet-4-6`                        |
| `blackwell` | vast.ai vLLM                 | 1x RTX PRO 6000 Blackwell SE 96 GB    | `openai/gpt-oss-120b` (MXFP4)              |
| `3090s`     | `idc-1` llama.cpp            | 2x RTX 3090 (48 GB total)             | `Qwen3-Coder-30B-A3B-Instruct-GGUF` Q5_K_M |

Three terminal columns, live streams, per-pane footer with tokens/sec, TTFT, wall time and pass/fail.

## Layout

```
scripts/
  llm-compare              3-pane spec runner (iTerm2 split, AppleScript)
  llm_stream.py            streamer for OpenAI + Anthropic
  vast-vllm                vast.ai instance lifecycle
  fetch_lcb.py             LiveCodeBench fetcher
  refactor-compare         multi-file refactor across git worktrees
  refactor_apply.py        split model dump, drop files in worktree, run pytest
  expand_prompt.py         get Sonnet to write a guide, cache it
  specs/
    lrucache.py            sanity
    lfucache.py
    black_scholes.py       price, Greeks, IV solve
    hrp.py                 Hierarchical Risk Parity
    american_binomial.py   CRR binomial tree
    lcb/                   LiveCodeBench problems (date-filtered)
```

## Usage

```sh
cp .env.example .env
uv venv && uv sync

scripts/llm-compare start                                       # spawn panes, fire
scripts/llm-compare go                                          # rerun in same panes
SPEC_FILE=scripts/specs/hrp.py scripts/llm-compare go           # pick a spec
EXPAND=1 SPEC_FILE=scripts/specs/hrp.py scripts/llm-compare go  # with Sonnet-distilled guide
scripts/llm-compare lcb                                         # random LiveCodeBench problem

scripts/refactor-compare start                                  # 5 primitives, 148 pytest tests
scripts/vast-vllm status                                        # GPU, weights, endpoint
```

Each pane prints prompt, counts down 5 seconds, streams, then runs the extracted code against the spec. Tokens/sec comes from the server's `usage` field, not chunk count, so Anthropic's chunk batching doesn't blow up the number.

The prompt has a UUID nonce appended so vLLM's prefix cache and Anthropic's ephemeral cache never hit on rerun.

## How specs work

A spec is a self-contained `unittest.TestCase`. Model implements what makes the tests pass. Streamer extracts python from the stream, prepends it to the spec, runs the file, parses `Ran N tests` and `FAILED (failures=X)` into `passed/total`.

For multi-file refactors, the model emits `# === FILE: <path> ===` markers, the splitter drops each file into a per-backend git worktree, then pytest runs against the worktree using the project's own venv.

## Frontier-distilled prompts

`EXPAND=1` runs Sonnet first to produce a 500-word implementation guide (signatures, pseudocode, imports, edge cases, library traps). That guide gets appended to the prompt every pane sees. The point is the agent pattern where frontier plans and a cheaper local executes.

## Specs in here

| Spec                    | Tests | Notes                                      |
|-------------------------|-------|--------------------------------------------|
| `lrucache.py`           | 10    | warm-up                                    |
| `lfucache.py`           | 15    | O(1) LFU with LRU tie-break                |
| `black_scholes.py`      | 17    | price + Greeks + IV solver                 |
| `hrp.py`                | 12    | Lopez de Prado HRP                         |
| `american_binomial.py`  | 12    | CRR backward induction                     |
| `lcb/p*.py`             | varies| LiveCodeBench (anti-contamination by date) |

## What I found

Throughput on a typical 1k to 3k token output:

| Backend                              | tok/s   | TTFT   |
|--------------------------------------|---------|--------|
| Blackwell vLLM (gpt-oss-120b MXFP4)  | ~170    | ~0.1s  |
| Blackwell vLLM (Qwen3-Coder-30B FP8) | ~170    | ~0.1s  |
| 3090s llama.cpp (Qwen3-Coder Q5_K_M) | 115-130 | ~0.3s  |
| Claude Sonnet 4.6 (AU to US)         | 70-90   | 1-4s   |

Same throughput from 30B FP8 and 120B MXFP4 on Blackwell is the giveaway: the card is memory-bandwidth limited and MXFP4 halves the bytes per token, so 4x the params costs roughly the same.

On HRP without the frontier guide:

| Backend                | Specs        | Wall   | tok/s |
|------------------------|--------------|--------|-------|
| Claude Sonnet 4.6      | 12/12 PASS   | 14.4s  | 86    |
| Blackwell gpt-oss-120b | 12/12 PASS   | 17.3s  | 170   |
| 3090s Qwen3-Coder-30B  | 2/12 FAIL    | 5.0s   | 132   |

gpt-oss-120b on a single 96 GB Blackwell SE matches Sonnet on the quant specs in this repo, at twice the throughput. The 30B coder needs the `EXPAND=1` guide to dodge the scipy `squareform` zero-diagonal trap.

On the multi-file refactor (5 primitives, 148 pytest tests), all three backends produced refactors that pass 148/148. Once the task is well-scoped, model size matters less than people think.

LiveCodeBench post-Jan-2025 hard problems are still above the 30B coder's ceiling. Sonnet passes them. gpt-oss-120b hasn't been measured here yet but should close the gap.

## Cost

Rough numbers, single-user batch=1:

| Backend                                  | $/MTok out      |
|------------------------------------------|-----------------|
| Claude Sonnet 4.6                        | ~$15            |
| vast.ai $1.07/hr saturated at 170 tok/s  | ~$1.78          |
| Owned 3090s (electricity only)           | ~$0.10          |

Local pays back if you keep it busy. Idle vast hours bill anyway.

## Pitfalls I hit

- vLLM on Blackwell SM_12.0 + MXFP4 hung silently for over an hour the first time when I had `--enforce-eager` set. Restarting without that flag and letting cudagraph compile worked fine. MXFP4 paths on the newest arch aren't fully exercised yet in vLLM 0.20.1.
- gpt-oss reasoning fields. vLLM's `openai_gptoss` parser puts thinking on `delta.reasoning`, not `delta.reasoning_content` (DeepSeek-R1 style). Wrong field name shows up as a fake 20s TTFT pause. Streamer reads both now.
- 120 GB vast disk fills fast. Qwen3-Coder-30B (30 GB) plus gpt-oss-120b (63 GB) plus overhead is over the line. Delete the old model from `/workspace/models` before swapping `VLLM_MODEL`.
- vast's single-GPU image with `AUTO_PARALLEL=true` injects an empty `--tensor-parallel-size` and crashes vLLM. `vast-vllm fix` disables it.

## Notes on the panes

iTerm2 split is driven via osascript. Pane IDs cached in `/tmp/llm-compare-panes` so `go` reuses the same panes for repeat runs. `reset` forgets them.

The Anthropic side uses prompt caching (ephemeral). Cache TTL is 5 minutes, so it only matters if you rerun the same prompt inside that window. The nonce defeats it anyway.

Temperature stays at 0 across all panes. That keeps reruns of the same backend deterministic, so any difference you see is real across backend, not sampling noise.

## Roadmap

- Self-repair loop (feed failure back, retry N rounds)
- Sampling diversity flags (temperature, frequency_penalty)
- LiveCodeBench `--difficulty hard` + multi-shot
- BigCodeBench and DS-1000 adapters
- Cost-per-passed-test ledger
- Aider polyglot edit benchmark
- Speculative decoding draft + verifier on Blackwell
