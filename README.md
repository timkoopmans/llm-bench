# llm-bench

Three-way coding-task benchmark in iTerm2: a hosted frontier model vs two
self-hosted open-weight models on the same canonical specs. Same prompt,
side-by-side streams, real `tokens/sec`, deterministic pass/fail.

| Pane        | Endpoint                     | Hardware                              | Model                                      |
|-------------|------------------------------|---------------------------------------|--------------------------------------------|
| `claude`    | Anthropic Messages API       | hosted, multi-tenant                   | `claude-sonnet-4-6` (default)              |
| `blackwell` | vast.ai vLLM, port 8000      | 1× **RTX PRO 6000 Blackwell SE** 96 GB | `openai/gpt-oss-120b` (MXFP4 native)       |
| `3090s`     | `idc-1` llama.cpp, port 8001 | 2× **RTX 3090** 48 GB total            | `Qwen3-Coder-30B-A3B-Instruct-GGUF` Q5_K_M |

Headroom on Blackwell (96 GB) lets us run a 120B reasoning model native
MXFP4, while the 3090 pair runs a 30B coder at Q5_K_M. Lets us see a
true frontier-vs-mid-tier comparison on identical-class hardware
budgets, plus the hosted-frontier baseline.

## Layout

```
scripts/
  llm-compare              # 3-pane spec runner (iTerm2 split, AppleScript)
  llm_stream.py            # streamer: OpenAI + Anthropic, real tok/s, spec runner
  vast-vllm                # vast.ai instance lifecycle (create/refresh-ports/fix/status/...)
  fetch_lcb.py             # LiveCodeBench fetcher → spec files
  refactor-compare         # multi-file refactor benchmark across git worktrees
  refactor_apply.py        # split model dump into worktree files + pytest
  expand_prompt.py         # Sonnet-distilled implementation guide cache
  specs/                   # canonical unittest specs (model implements, spec scores)
    lrucache.py
    lfucache.py
    black_scholes.py       # + Greeks + IV solver
    hrp.py                 # Lopez de Prado Hierarchical Risk Parity
    american_binomial.py   # CRR American option
    lcb/                   # LiveCodeBench problems (cached, dated-filtered)
specs/<base>.expanded.md   # Sonnet-distilled implementation guide (cached)
```

## Usage

```sh
# one-time
cp .env.example .env        # fill HF_TOKEN, ANTHROPIC_API_KEY, VAST_*, LLM_*
uv venv && uv sync

# 3-pane spec compare (cache-busted, with countdown, with pass/total)
scripts/llm-compare start                                       # spawn panes
scripts/llm-compare go                                          # rerun in cached panes
SPEC_FILE=scripts/specs/hrp.py scripts/llm-compare go           # any spec
EXPAND=1 SPEC_FILE=scripts/specs/hrp.py scripts/llm-compare go  # +frontier-distilled guide
scripts/llm-compare lcb                                         # random LiveCodeBench problem
scripts/llm-compare reset                                       # forget cached pane IDs

# Multi-file refactor across worktrees
scripts/refactor-compare start                                  # 5 target primitives, 148 tests
scripts/refactor-compare go

# vast.ai management
scripts/vast-vllm status     # endpoint probe + supervisor + GPU + weights size
scripts/vast-vllm fix        # disable AUTO_PARALLEL, push HF_TOKEN, restart
scripts/vast-vllm stop       # keep weights cached on disk, stop GPU billing
```

## Streamer output

Each pane shows:
1. Prompt preview + 5-second countdown (so screen-recording stays in sync)
2. Live token stream — thinking blocks dim, content normal
3. Footer with authoritative token counts from the server's `usage` field
4. Auto-run of extracted code against canonical spec
5. Boxed summary: `model | hw | tok/s | TTFT | wall | out tok | specs N/M PASS|FAIL`

Tokens/sec comes from the server's `usage.completion_tokens` (OpenAI
`stream_options.include_usage=true`) or `message_delta.usage.output_tokens`
(Anthropic) — not from chunk count, which over-counts on multi-token chunks
(Anthropic batches ~30+ tokens per SSE event) and under-counts on
short outputs.

## How specs work

Each `specs/*.py` is a self-contained `unittest.TestCase` referencing a
class or function the model must implement. The streamer:

1. Sends prompt = spec source + "implement what makes these tests pass"
2. Extracts python fenced blocks from the stream
3. Writes them above the spec into a temp file
4. Runs the temp file with `.venv/bin/python3`
5. Parses `Ran N tests` + `FAILED (failures=X, errors=Y)` → `N_passed/N_total`

Cache busting: a UUID nonce is appended to every prompt as a `# nonce:`
comment, so vLLM's prefix cache and Anthropic's ephemeral cache never
hit on rerun. Temperature stays at 0 — comparisons stay deterministic
across reruns of the same backend, while cross-backend differences are
real (model + engine + hardware).

## Frontier-distilled prompts

`EXPAND=1` triggers `expand_prompt.py`: Claude Sonnet generates a
500-word implementation guide (signatures, pseudocode steps, required
imports, edge cases, library footguns) and it's appended to the prompt
shown to every pane. Caches as `specs/<stem>.expanded.md`.

This mirrors the production agent pattern: **frontier model plans,
cheap local model executes.**

## Specs implemented

| Spec                    | Tests | What it measures                                |
|-------------------------|-------|-------------------------------------------------|
| `lrucache.py`           | 10    | Sanity check — most models pass cold            |
| `lfucache.py`           | 15    | O(1) LFU with LRU tie-break — bookkeeping trap  |
| `black_scholes.py`      | 17    | Price + Greeks + IV solver — Greek-sign trap    |
| `hrp.py`                | 12    | Hierarchical Risk Parity — scipy footguns       |
| `american_binomial.py`  | 12    | CRR backward induction — early-exercise         |
| `lcb/p*.py`             | varies| LiveCodeBench post-cutoff (anti-contamination)  |

## Findings (this session)

### Throughput

On a typical 1k–3k token reasoning-coding output:

| Backend                        | Model                          | tok/s | TTFT   |
|--------------------------------|--------------------------------|-------|--------|
| Blackwell vLLM MXFP4 + cudagraph | **gpt-oss-120b**             | ~170  | ~0.1 s |
| Blackwell vLLM FP8             | Qwen3-Coder-30B-FP8            | ~170  | ~0.1 s |
| 3090s llama.cpp Q5_K_M         | Qwen3-Coder-30B-Q5_K_M         | ~115–130 | ~0.3 s |
| Claude Sonnet 4.6 (AU→US)      | claude-sonnet-4-6              | ~70–90 | ~1–4 s |

Blackwell at single-user batch=1 is **~2× Claude on throughput** and
**~10× on TTFT** (network + multi-tenant queue dominate Claude's TTFT).
Same throughput for 30B FP8 and 120B MXFP4 — Blackwell is memory-bandwidth
limited; MXFP4 cuts the per-token byte traffic enough that 4× the params
costs roughly the same per token.

### Quality

- **Real-world multi-file refactor (5 primitives, 148 tests):** all three
  backends produced refactors that pass 148/148. On well-scoped tasks,
  Qwen3-Coder-30B (FP8 and Q5_K_M alike) matches Sonnet.
- **LiveCodeBench post-Jan-2025 hard:** Claude passes; Qwen3-Coder-30B
  hits its capability ceiling regardless of quant. gpt-oss-120b not yet
  measured on this set but expected to close the gap.
- **HRP (Hierarchical Risk Parity) without `EXPAND`:** the scipy
  `squareform` strict-zero-diagonal footgun trips small models. Result
  on bare prompt (no guide):

  | Backend                  | Specs    | Wall   | tok/s |
  |--------------------------|----------|--------|-------|
  | Claude Sonnet 4.6        | **12/12 PASS** | 14.4 s | 86 |
  | Blackwell gpt-oss-120b   | **12/12 PASS** | 17.3 s | 170 |
  | 3090s Qwen3-Coder-30B    | 2/12 FAIL | 5.0 s | 132 |

  gpt-oss-120b matches Sonnet capability AND doubles Sonnet throughput.
  The 30B coder model needs the frontier-distilled `EXPAND=1` guide to
  recover (the guide explicitly flags the squareform footgun).
- **FP8 vs Q5_K_M of the same base model:** essentially equivalent on
  the well-scoped refactor; gap shows up at the edge of capability,
  not in well-understood tasks.

### Pathologies

- **Temperature=0 + greedy can loop on hard problems** — qwen-coder
  occasionally got stuck repeating tokens on HRP. Sampling diversity
  or frequency-penalty would fix it (not yet wired).
- **Anthropic batches chunks aggressively** — Sonnet emits ~30 tokens
  per SSE event; raw "chunks/s" makes it look 50× slower than it is.
  Always use authoritative `usage` counts.
- **Model output format drift** — without strict format instructions,
  small models sometimes wrap classes in `if __name__` blocks or skip
  required functions. The spec runner catches this as "extracted 0
  python blocks" or `NameError`.
- **Reasoning field naming inconsistency** — DeepSeek-R1 distills emit
  `delta.reasoning_content`; vLLM's `openai_gptoss` parser emits
  `delta.reasoning`. The streamer now reads both. If reasoning silently
  buffers and the visible TTFT looks long (e.g. 24 s for gpt-oss-120b),
  check the field name first.
- **vLLM on Blackwell SM_12.0 + MXFP4** — first MARLIN MoE backend
  load hung silently for >60 min when used with `--enforce-eager`.
  Restarting without that flag (letting cudagraph compile) loaded
  fine and stayed fast (~170 tok/s on 120B). MXFP4 kernel paths on
  the newest arch may not be fully exercised in vLLM 0.20.1.
- **Vast disk full on 120 GB instance** — Qwen3-Coder-30B (30 GB) +
  gpt-oss-120b (63 GB) + overhead exceeds the default 120 GB rental.
  Delete the previous model from `/workspace/models` before swapping
  via `VLLM_MODEL`.

### Cost (rough, this session)

| Backend                                   | $/MTok out (effective) |
|-------------------------------------------|-----------------------:|
| Claude Sonnet 4.6                         |                ~$15   |
| Vast.ai @ $1.07/hr, 170 tok/s saturated   |                ~$1.78 |
| Owned 3090s, ignoring CAPEX               |                 ~$0.10 (electricity) |

Blackwell pays back vs Sonnet **only if you keep it saturated**. Idle
hours bill regardless.

### When Blackwell dominates

Cases where the local FP8 box is unambiguously the right pick:

1. **Long-context single-shot:** 131k-token codebase analysis — Blackwell
   ingests + emits in one continuous run, no per-call API overhead. Claude
   has cheaper per-token but worse end-to-end latency at this scale.
2. **High-throughput batch generation:** evaluation pipelines, synthetic
   data generation, log summarisation. vLLM continuous-batching scales to
   dozens of concurrent requests on one card → 10–20× effective tok/s vs
   Claude's per-request rate limits.
3. **Tight agent loops with self-repair:** 5+ iterations per task means
   network latency dominates Claude wall time. Local cuts it to milliseconds.
4. **Constrained / structured decoding:** JSON-mode at scale, regex
   constraints, grammar-guided sampling — vLLM exposes these directly with
   no extra latency; Anthropic's structured-output is more limited.
5. **Speculative decoding pairs:** draft + verifier on one Blackwell can
   push another 1.5–2× tok/s. Not available via hosted API.
6. **Privacy / airgap requirement:** any time the data can't leave a network
   boundary, hosted is off the table.
7. **High-volume well-scoped refactor / migration:** see the target
   primitives test — 148/148 with FP8 30B, at ~10× lower $/Mtok than Claude.

Where Blackwell does NOT win, even saturated:
- Novel reasoning under uncertainty (Sonnet still slightly better priors,
  though gpt-oss-120b closes most of the gap on quant problems)
- Multi-step agent planning over very long horizons
- One-shot critical correctness where retry cost > savings

With gpt-oss-120b on Blackwell, the **capability vs hosted Sonnet is
roughly matched on the quant specs in this repo** (BS, HRP, CRR) and
throughput is **~2× Sonnet**. The frontier-vs-local gap is much smaller
than it was when comparing Sonnet vs a 30B-class coder model.

### When to use what

- Hard, novel, high-stakes correctness → Claude
- High-volume well-scoped (refactor, well-understood algorithm) → local
- Real coding workflow → **frontier plans + local executes** (the `EXPAND=1` mode)

## Roadmap

- [ ] Self-repair loop: feed failure traceback back to model, score after N rounds
- [ ] Sampling-diversity flags (`temperature`, `frequency_penalty`)
- [ ] LiveCodeBench `--difficulty hard` + multi-shot
- [ ] BigCodeBench / DS-1000 adapters
- [ ] Cost-per-passed-test accounting
- [ ] Aider polyglot edit benchmark
- [ ] Persistent leaderboard across runs (JSONL → markdown)
- [ ] Speculative decoding draft+verifier on Blackwell

## Notes

- vast.ai instance setup: see `scripts/vast-vllm` head comment. The
  `AUTO_PARALLEL=true` env on a single-GPU box injects an empty
  `--tensor-parallel-size` flag and crashes vLLM; the `fix`
  subcommand disables it.
- idc-1 llama.cpp serves at `http://idc-1:8001/v1`. Swap the served
  model via the `MODEL_*` vars in the sibling ops repo bootstrap and
  `systemctl restart llama-server`.
- The Anthropic backend uses prompt caching (`cache_control: ephemeral`)
  on the user message — cache TTL 5 min; only matters for repeat
  prompts within that window, which the nonce defeats.
