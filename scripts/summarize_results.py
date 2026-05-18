#!/usr/bin/env python3
"""Print a markdown leaderboard from results.jsonl.

Usage:
  summarize_results.py [results.jsonl]   # default: ../results.jsonl
  summarize_results.py --task hrp        # filter to one task
  summarize_results.py --label claude    # filter to one backend
  summarize_results.py --last 9          # only the last N runs
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean


def fmt_specs(p, t):
    if not t:
        return "-"
    return f"{p}/{t}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log_file", nargs="?", default=None)
    ap.add_argument("--task")
    ap.add_argument("--label")
    ap.add_argument("--last", type=int, default=0)
    args = ap.parse_args()

    path = Path(args.log_file or Path(__file__).resolve().parent.parent / "results.jsonl")
    if not path.is_file():
        print(f"no log file at {path}", file=sys.stderr)
        return 2

    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if args.task:
        rows = [r for r in rows if r.get("task") == args.task]
    if args.label:
        rows = [r for r in rows if r.get("label") == args.label]
    if args.last:
        rows = rows[-args.last:]

    if not rows:
        print("no matching rows", file=sys.stderr)
        return 1

    print(f"## Runs ({len(rows)})\n")
    print("| ts            | task                 | label     | model               | tok/s | TTFT | wall  | out  | specs |")
    print("|---------------|----------------------|-----------|---------------------|------:|-----:|------:|-----:|------:|")
    for r in rows:
        print(
            f"| {r.get('ts','')[5:16]} "
            f"| {(r.get('task','') or '')[:20]:<20} "
            f"| {(r.get('label','') or '')[:9]:<9} "
            f"| {(r.get('model','') or '')[:19]:<19} "
            f"| {r.get('tok_s','-')!s:>5} "
            f"| {r.get('ttft','-')!s:>4} "
            f"| {r.get('wall','-')!s:>5} "
            f"| {r.get('out_tok','-')!s:>4} "
            f"| {fmt_specs(r.get('passed'), r.get('total')):>5} |"
        )

    agg = defaultdict(list)
    for r in rows:
        agg[(r.get("task"), r.get("label"))].append(r)

    print(f"\n## Aggregate ({len(agg)} task/backend combos)\n")
    print("| task                 | label     | runs | mean tok/s | mean TTFT | mean wall | full-pass |")
    print("|----------------------|-----------|-----:|-----------:|----------:|----------:|----------:|")
    for (task, label), rs in sorted(agg.items()):
        tps = [r["tok_s"] for r in rs if r.get("tok_s") is not None]
        tts = [r["ttft"] for r in rs if r.get("ttft") is not None]
        wls = [r["wall"] for r in rs if r.get("wall") is not None]
        full = sum(
            1 for r in rs
            if r.get("passed") is not None and r.get("total") and r["passed"] == r["total"]
        )
        n = len(rs)
        m_tps = f"{mean(tps):.1f}" if tps else "-"
        m_ttft = f"{mean(tts):.2f}" if tts else "-"
        m_wall = f"{mean(wls):.2f}" if wls else "-"
        print(
            f"| {(task or '')[:20]:<20} "
            f"| {(label or '')[:9]:<9} "
            f"| {n:>4} "
            f"| {m_tps:>10} "
            f"| {m_ttft:>9} "
            f"| {m_wall:>9} "
            f"| {full}/{n:<3} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
