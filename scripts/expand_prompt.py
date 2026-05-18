#!/usr/bin/env python3
"""Ask Claude Sonnet to expand a canonical pytest spec into an implementation
guide a junior coder could follow. Cached next to spec as <stem>.expanded.md.

Usage:
  expand_prompt.py <spec.py>            # cached; reuse if exists
  expand_prompt.py <spec.py> --force    # regen
  expand_prompt.py <spec.py> --model claude-sonnet-4-6
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def expand(spec_path: Path, model: str) -> str:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    spec_src = spec_path.read_text()
    user_msg = (
        "You are a senior engineer writing an implementation guide for a junior "
        "coder who must implement the algorithm tested by the following pytest "
        "spec. They will see only your guide and the spec; they cannot ask "
        "questions. Produce a numbered, structured guide with these sections:\n"
        "1. Required function signatures, copied verbatim from the spec.\n"
        "2. Algorithm steps in plain English / pseudocode (the math, the order "
        "of operations).\n"
        "3. Required imports (only stdlib + numpy/pandas/scipy as needed).\n"
        "4. Key edge cases the tests exercise, with one-line strategy each.\n"
        "5. Common pitfalls — be specific and concrete. Include sign / scale "
        "/ convention traps, AND library-strictness gotchas (e.g. scipy's "
        "squareform rejects non-zero diagonals from float noise — either "
        "np.fill_diagonal(d, 0) first or pass checks=False; scipy.optimize "
        "fminbound requires bracket; np.linalg.cholesky needs PSD-not-PD; "
        "etc.). If the algorithm uses scipy or numpy in a way that has a "
        "well-known footgun, call it out explicitly.\n"
        "6. Suggested private helper functions and what each does.\n"
        "Do NOT write the final implementation code. Do NOT redefine the tests. "
        "Keep it under 500 words.\n\n"
        "SPEC:\n```python\n" + spec_src + "\n```"
    )
    body = json.dumps(
        {
            "model": model,
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": user_msg}],
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec_file")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    spec = Path(args.spec_file).resolve()
    if not spec.is_file():
        print(f"spec not found: {spec}", file=sys.stderr)
        return 2
    cache = spec.with_suffix(".expanded.md")
    if cache.exists() and not args.force:
        print(cache)
        return 0
    text = expand(spec, args.model)
    cache.write_text(text)
    print(cache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
