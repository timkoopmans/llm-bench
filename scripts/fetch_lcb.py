#!/usr/bin/env python3
"""Fetch LiveCodeBench and emit one unittest spec file per LeetCode problem.

- Downloads test6.jsonl (latest LCB release) on first run.
- Filters to LeetCode-style problems with `class Solution` starter code
  and at least one public test case.
- Optional date filter (--after YYYY-MM-DD) — pick problems released after
  a model's training cutoff for contamination-free benchmarking.
- Writes specs to bench/scripts/specs/lcb/p<id>_<slug>.py.

Usage:
  fetch_lcb.py                       # default: after 2026-01-01, limit 50
  fetch_lcb.py --after 2025-06-01    # custom cutoff
  fetch_lcb.py --limit 200           # more problems
  fetch_lcb.py --force-download      # re-download even if cached
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

LCB_URL = (
    "https://huggingface.co/datasets/livecodebench/code_generation_lite"
    "/resolve/main/test6.jsonl"
)

HERE = Path(__file__).resolve().parent
CACHE_DIR = HERE / "specs" / "lcb" / "_cache"
SPEC_DIR = HERE / "specs" / "lcb"
CACHE_FILE = CACHE_DIR / "test6.jsonl"

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s: str) -> str:
    return SLUG_RE.sub("_", s.lower()).strip("_")[:60]


def download(force: bool = False) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CACHE_FILE.exists() and not force:
        print(f"using cached {CACHE_FILE} ({CACHE_FILE.stat().st_size / 1e6:.1f} MB)")
        return
    print(f"downloading {LCB_URL} → {CACHE_FILE}")
    with urllib.request.urlopen(LCB_URL) as r, CACHE_FILE.open("wb") as out:
        total = int(r.headers.get("Content-Length", 0))
        got = 0
        chunk = 1 << 20
        while True:
            buf = r.read(chunk)
            if not buf:
                break
            out.write(buf)
            got += len(buf)
            if total:
                print(
                    f"  {got/1e6:.1f}/{total/1e6:.1f} MB ({100*got/total:.1f}%)",
                    end="\r",
                )
    print(f"\ndone: {CACHE_FILE.stat().st_size / 1e6:.1f} MB")


def _make_test(i: int, inp: str, out: str, func: str) -> str:
    return (
        f"    def test_public_{i}(self):\n"
        f"        args = [json.loads(line) for line in {inp!r}.strip().split('\\n') if line.strip()]\n"
        f"        expected = json.loads({out!r})\n"
        f"        result = Solution().{func}(*args)\n"
        f"        self.assertEqual(result, expected)\n"
    )


def emit_spec(row: dict) -> Path | None:
    starter = row.get("starter_code") or ""
    if "class Solution" not in starter:
        return None
    meta = json.loads(row.get("metadata") or "{}")
    func = meta.get("func_name")
    if not func:
        return None
    pubs_raw = row.get("public_test_cases") or "[]"
    try:
        pubs = json.loads(pubs_raw)
    except json.JSONDecodeError:
        return None
    if not pubs:
        return None

    tests = "".join(
        _make_test(i + 1, tc.get("input", ""), tc.get("output", ""), func)
        for i, tc in enumerate(pubs)
    )

    qid = str(row.get("question_id", "x"))
    title = row.get("question_title", "untitled")
    slug = slugify(title)
    platform = row.get("platform", "?")
    date = (row.get("contest_date") or "?")[:10]
    difficulty = row.get("difficulty", "?")
    question = (row.get("question_content", "") or "").strip()
    starter_clean = starter.strip()
    tname = slug or f"p{qid}"

    body = (
        f'"""LiveCodeBench {qid} — {title} ({platform}, {date}, {difficulty})\n\n'
        f"Source: https://leetcode.com/problems/{slug}/\n\n"
        f"QUESTION:\n{question}\n\n"
        f"NOTE FOR THE MODEL:\n"
        f"Implement class `Solution` with method `{func}` exactly matching\n"
        f"the signature in the starter code below. Do NOT include any tests,\n"
        f"doctests, or `if __name__` block. Your code will be concatenated\n"
        f"above the spec which runs your Solution against canonical tests.\n\n"
        f"STARTER CODE:\n{starter_clean}\n"
        f'"""\n'
        f"import json\n"
        f"import unittest\n\n\n"
        f"class Test_{tname}(unittest.TestCase):\n"
        f"{tests}\n\n"
        f'if __name__ == "__main__":\n'
        f"    unittest.main(exit=False, verbosity=2)\n"
    )
    SPEC_DIR.mkdir(parents=True, exist_ok=True)
    out = SPEC_DIR / f"p{qid}_{slug}.py"
    out.write_text(body)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--after", default="2026-01-01", help="contest_date > this")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--force-download", action="store_true")
    ap.add_argument(
        "--difficulty",
        default="all",
        help="comma-separated: easy,medium,hard,all (default: all)",
    )
    args = ap.parse_args()
    diffs = {d.strip().lower() for d in args.difficulty.split(",")}
    diff_all = "all" in diffs

    download(force=args.force_download)

    written = 0
    skipped = 0
    with CACHE_FILE.open() as fh:
        for line in fh:
            if written >= args.limit:
                break
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("platform") != "leetcode":
                skipped += 1
                continue
            date = (row.get("contest_date") or "")[:10]
            if date <= args.after:
                skipped += 1
                continue
            if not diff_all and (row.get("difficulty") or "").lower() not in diffs:
                skipped += 1
                continue
            path = emit_spec(row)
            if path:
                written += 1
            else:
                skipped += 1

    print(f"wrote {written} specs to {SPEC_DIR} (skipped {skipped})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
