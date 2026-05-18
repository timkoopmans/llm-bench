#!/usr/bin/env python3
"""Stream OpenAI- or Anthropic-style chat and print TTFT + tokens/s footer.

Usage:
  llm_stream.py --label vast --url http://host:port/v1 --model qwen-coder \
                --prompt-file /tmp/p.txt [--api-key EMPTY] [--backend openai|anthropic]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request


def build_request(args, prompt):
    if args.backend == "anthropic":
        anth_body = {
            "model": args.model,
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
            "stream": True,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                }
            ],
        }
        if args.top_p is not None:
            anth_body["top_p"] = args.top_p
        body = json.dumps(anth_body).encode()
        return urllib.request.Request(
            f"{args.url}/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": args.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
    oai_body = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if args.top_p is not None:
        oai_body["top_p"] = args.top_p
    if args.frequency_penalty is not None:
        oai_body["frequency_penalty"] = args.frequency_penalty
    if args.presence_penalty is not None:
        oai_body["presence_penalty"] = args.presence_penalty
    body = json.dumps(oai_body).encode()
    return urllib.request.Request(
        f"{args.url}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {args.api_key}",
        },
        method="POST",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--url", required=True, help="base url ending in /v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--api-key", default="EMPTY")
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--backend", choices=["openai", "anthropic"], default="openai")
    ap.add_argument("--countdown", type=int, default=0, help="seconds to display prompt before firing")
    ap.add_argument("--run", action="store_true", help="extract python code blocks and run them after stream")
    ap.add_argument("--spec", default="", help="hardware spec line shown in summary")
    ap.add_argument("--spec-file", default="", help="canonical test spec file appended to model code before running")
    ap.add_argument("--write-file", default="", help="write extracted code to this path (for sandbox refactor mode)")
    ap.add_argument("--write-raw", action="store_true", help="write entire raw stream content to --write-file (skip fenced-block extraction; for multi-file refactor)")
    ap.add_argument("--test-cmd", default="", help="shell command to run after --write-file; parses pytest output for pass/total")
    ap.add_argument("--runner", default="python3", help="python interpreter used for --run spec execution")
    ap.add_argument("--log-file", default="", help="append one JSON line per run to this file")
    ap.add_argument("--task-name", default="", help="label for the task in the log line (defaults to spec-file basename)")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--top-p", type=float, default=None, help="OpenAI only")
    ap.add_argument("--frequency-penalty", type=float, default=None, help="OpenAI only; helps break repetition loops")
    ap.add_argument("--presence-penalty", type=float, default=None, help="OpenAI only")
    ap.add_argument("--idle-timeout", type=float, default=60.0, help="seconds to wait for next byte before aborting a hung stream")
    ap.add_argument("--wall-timeout", type=float, default=0.0, help="hard cap on total request seconds (0 = no cap). Aborts mid-stream and proceeds to footer with what we have.")
    args = ap.parse_args()

    with open(args.prompt_file) as fh:
        prompt = fh.read()

    req = build_request(args, prompt)

    print(f"\033[1;36m=== {args.label} | {args.model} ===\033[0m", flush=True)
    print(f"\033[2m{args.url}\033[0m", flush=True)
    print(f"\033[1;35m--- prompt ---\033[0m", flush=True)
    print(f"\033[35m{prompt}\033[0m", flush=True)
    print(f"\033[1;35m--------------\033[0m\n", flush=True)

    if args.countdown > 0:
        for i in range(args.countdown, 0, -1):
            sys.stdout.write(f"\r\033[1;33mstarting in {i}...\033[0m  ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r\033[1;32mGO!                \033[0m\n\n")
        sys.stdout.flush()

    DIM = "\033[2m"
    RESET = "\033[0m"

    t0 = time.perf_counter()
    ttft = None
    in_reasoning = False
    output_tokens = 0  # authoritative from server when available
    input_tokens = 0
    collected_content = []  # buffer for --run

    deadline = (t0 + args.wall_timeout) if args.wall_timeout > 0 else None
    try:
        with urllib.request.urlopen(req, timeout=args.idle_timeout) as resp:
            for raw in resp:
                if deadline is not None and time.perf_counter() > deadline:
                    print(f"\n\033[1;31m[wall-timeout {args.wall_timeout}s — aborting]\033[0m", flush=True)
                    break
                line = raw.decode("utf-8", errors="replace").rstrip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue

                reasoning = ""
                content = ""

                if args.backend == "anthropic":
                    t = obj.get("type", "")
                    if t == "message_start":
                        u = obj.get("message", {}).get("usage", {}) or {}
                        input_tokens = u.get("input_tokens", 0) or input_tokens
                        output_tokens = u.get("output_tokens", 0) or output_tokens
                    elif t == "content_block_delta":
                        d = obj.get("delta", {})
                        dt = d.get("type", "")
                        if dt == "thinking_delta":
                            reasoning = d.get("thinking", "")
                        elif dt == "text_delta":
                            content = d.get("text", "")
                    elif t == "message_delta":
                        u = obj.get("usage", {}) or {}
                        if "output_tokens" in u:
                            output_tokens = u["output_tokens"]
                else:
                    choices = obj.get("choices") or []
                    if choices:
                        delta = choices[0].get("delta", {}) or {}
                        # `reasoning_content` (DeepSeek-R1 distills) or `reasoning` (vLLM gpt-oss parser)
                        reasoning = (
                            delta.get("reasoning_content")
                            or delta.get("reasoning")
                            or ""
                        )
                        content = delta.get("content") or ""
                    u = obj.get("usage")
                    if isinstance(u, dict):
                        input_tokens = u.get("prompt_tokens", input_tokens) or input_tokens
                        output_tokens = u.get("completion_tokens", output_tokens) or output_tokens

                if reasoning:
                    if not in_reasoning:
                        sys.stdout.write(DIM + "[think] ")
                        in_reasoning = True
                    if ttft is None:
                        ttft = time.perf_counter() - t0
                    sys.stdout.write(reasoning)
                    sys.stdout.flush()
                if content:
                    if in_reasoning:
                        sys.stdout.write(RESET + "\n\n")
                        in_reasoning = False
                    if ttft is None:
                        ttft = time.perf_counter() - t0
                    sys.stdout.write(content)
                    sys.stdout.flush()
                    collected_content.append(content)
            if in_reasoning:
                sys.stdout.write(RESET)
    except Exception as e:
        print(f"\n\033[1;31mERROR: {e}\033[0m", flush=True)
        # fall through so we still log a row with whatever we have
        if args.log_file:
            wall = time.perf_counter() - t0
            tps = (output_tokens / wall) if (wall > 0 and output_tokens) else 0.0
            log_run(
                args.log_file, args.label, args.model, args.spec, args.spec_file,
                args.task_name, tps, ttft, wall, input_tokens, output_tokens,
                {"exit": -3, "passed": 0, "total": 0},
            )
        return 1

    wall = time.perf_counter() - t0
    gen = wall - (ttft or 0)
    tps = (output_tokens / gen) if (gen > 0 and output_tokens) else 0.0
    tpot_ms = (gen * 1000.0 / output_tokens) if output_tokens else 0.0
    ttft_s = f"{ttft:.2f}s" if ttft else "n/a"
    print(
        f"\n\n\033[1;33m── {args.label} ──  "
        f"TTFT {ttft_s} | in {input_tokens} tok | out {output_tokens} tok @ "
        f"{tps:.1f} tok/s ({tpot_ms:.1f} ms/tok) | gen {gen:.2f}s wall {wall:.2f}s\033[0m",
        flush=True,
    )

    result = None  # dict with exit/passed/total or None
    if args.write_file and args.test_cmd:
        result = run_sandbox(
            "".join(collected_content), args.label, args.write_file, args.test_cmd,
            raw=args.write_raw,
        )
    elif args.run:
        result = run_extracted(
            "".join(collected_content), args.label, spec_file=args.spec_file,
            runner=args.runner,
        )
    print_summary(args.label, args.model, args.spec, result, tps, ttft, output_tokens, wall)
    if args.log_file:
        log_run(
            args.log_file, args.label, args.model, args.spec, args.spec_file,
            args.task_name, tps, ttft, wall, input_tokens, output_tokens, result,
        )
    return 0


def log_run(path, label, model, hw, spec_file, task_name, tps, ttft, wall, in_tok, out_tok, result):
    import datetime
    import os
    task = task_name
    if not task:
        if spec_file:
            task = os.path.basename(spec_file).rsplit(".", 1)[0]
        else:
            task = "unknown"
    row = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "task": task,
        "label": label,
        "model": model,
        "hw": hw,
        "ttft": round(ttft, 3) if ttft else None,
        "wall": round(wall, 3),
        "tok_s": round(tps, 1),
        "in_tok": int(in_tok or 0),
        "out_tok": int(out_tok or 0),
        "passed": (result or {}).get("passed"),
        "total": (result or {}).get("total"),
        "exit": (result or {}).get("exit"),
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a") as fh:
        fh.write(json.dumps(row) + "\n")


def run_sandbox(content: str, label: str, write_file: str, test_cmd: str, raw: bool = False):
    """Write extracted (or raw) code to write_file, then run test_cmd. Parse summary."""
    import re
    import subprocess
    code = content if raw else extract_python_blocks(content)
    print(f"\n\033[1;34m── {label} refactor run ──\033[0m", flush=True)
    if not code.strip():
        print("\033[1;31mno code extracted\033[0m", flush=True)
        return {"exit": 1, "passed": 0, "total": 0}
    import os
    os.makedirs(os.path.dirname(write_file) or ".", exist_ok=True)
    with open(write_file, "w") as fh:
        fh.write(code)
    print(f"\033[2mwrote\033[0m {write_file}  ({len(code)} bytes)", flush=True)
    try:
        proc = subprocess.run(
            test_cmd, shell=True, capture_output=True, text=True, timeout=180
        )
    except subprocess.TimeoutExpired:
        print(f"\033[1;31mTIMEOUT after 180s\033[0m", flush=True)
        return {"exit": 124, "passed": 0, "total": 0}
    out = (proc.stdout or "") + (proc.stderr or "")
    tail = "\n".join(out.strip().splitlines()[-12:])
    color = "\033[1;32m" if proc.returncode == 0 else "\033[1;31m"
    print(f"{color}exit {proc.returncode}\033[0m", flush=True)
    if tail:
        print(tail, flush=True)
    # Parse pytest summary lines: "N passed", "N failed", "N error(s)"
    passed = 0
    failed = 0
    errors = 0
    for m in re.finditer(r"(\d+) (passed|failed|errors?)", out):
        n = int(m.group(1))
        kind = m.group(2)
        if kind == "passed":
            passed = max(passed, n)
        elif kind == "failed":
            failed = max(failed, n)
        elif kind.startswith("error"):
            errors = max(errors, n)
    total = passed + failed + errors
    return {"exit": proc.returncode, "passed": passed, "total": total}


def print_summary(label, model, spec, result, tps, ttft, out_toks, wall):
    sep = "\033[1m" + "═" * 60 + "\033[0m"
    print(f"\n{sep}", flush=True)
    print(f"\033[1m  {label.upper()}\033[0m", flush=True)
    print(f"  \033[36mmodel\033[0m  {model}", flush=True)
    if spec:
        print(f"  \033[36mhw\033[0m     {spec}", flush=True)
    ttft_s = f"{ttft:.2f}s" if ttft else "n/a"
    print(
        f"  \033[36mperf\033[0m   {tps:.1f} tok/s  |  TTFT {ttft_s}  |  wall {wall:.2f}s  |  {out_toks} out tok",
        flush=True,
    )
    if result is not None:
        p, t, x = result["passed"], result["total"], result["exit"]
        score_str = f"{p}/{t} specs passed" if t else f"exit {x} (no specs inferred)"
        if x == 0 and t > 0 and p == t:
            badge = "\033[1;42;30m  PASS  \033[0m"
        else:
            badge = "\033[1;41;37m  FAIL  \033[0m"
        print(f"  \033[36mspecs\033[0m  {badge}  {score_str}", flush=True)
    print(sep, flush=True)


def extract_python_blocks(text: str) -> str:
    """Concatenate all ```python (or ```) fenced code blocks in text."""
    import re
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.DOTALL)
    if not blocks:
        return text  # fallback: try raw
    return "\n\n".join(b.rstrip() for b in blocks)


def run_extracted(content: str, label: str, spec_file: str = "", runner: str = "python3"):
    """Run extracted code (+ optional canonical spec appended). Returns dict."""
    import re
    import subprocess
    import tempfile
    code = extract_python_blocks(content)
    print(f"\n\033[1;34m── {label} test run ──\033[0m", flush=True)
    if not code.strip():
        print("\033[1;31mno code extracted\033[0m", flush=True)
        return {"exit": 1, "passed": 0, "total": 0}
    full = code
    if spec_file:
        try:
            with open(spec_file) as fh:
                spec_src = fh.read()
            full = code + "\n\n# === canonical spec ===\n" + spec_src
        except OSError as e:
            print(f"\033[1;31mspec-file unreadable: {e}\033[0m", flush=True)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", delete=False, prefix=f"llm_{label}_"
    ) as fh:
        fh.write(full)
        path = fh.name
    try:
        proc = subprocess.run(
            [runner, path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        exit_code = proc.returncode
        out = (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired as e:
        print(f"\033[1;31mTIMEOUT after 30s\033[0m  ({path})", flush=True)
        return {"exit": 124, "passed": 0, "total": 0}
    tail = "\n".join(out.strip().splitlines()[-15:])
    color = "\033[1;32m" if exit_code == 0 else "\033[1;31m"
    print(f"{color}exit {exit_code}\033[0m  ({path})", flush=True)
    if tail:
        print(tail, flush=True)

    # Parse unittest output: "Ran N test(s) in T s" then "OK" or "FAILED (failures=F, errors=E)"
    total = 0
    failed = 0
    m = re.search(r"^Ran (\d+) tests? in ", out, re.MULTILINE)
    if m:
        total = int(m.group(1))
    mf = re.search(r"FAILED \(([^)]+)\)", out)
    if mf:
        for part in mf.group(1).split(","):
            kv = part.strip().split("=")
            if len(kv) == 2 and kv[0] in ("failures", "errors"):
                try:
                    failed += int(kv[1])
                except ValueError:
                    pass
    elif total and re.search(r"^OK\b", out, re.MULTILINE):
        failed = 0
    elif not total and exit_code != 0:
        failed = 1  # crash before any test ran → count as one fail
    passed = max(0, total - failed)
    return {"exit": exit_code, "passed": passed, "total": total}


if __name__ == "__main__":
    raise SystemExit(main())
