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

    # Wide table: one row per task, columns per backend.
    # Pick the most recent row that has a non-null total per (task,label);
    # fall back to most recent row overall if none have data.
    by_task = defaultdict(dict)  # task -> label -> chosen row
    by_task_all = defaultdict(lambda: defaultdict(list))
    for r in rows:
        t = r.get("task")
        l = r.get("label")
        if not t or not l:
            continue
        by_task_all[t][l].append(r)
    for t, by_label in by_task_all.items():
        for l, rs in by_label.items():
            rs.sort(key=lambda r: r.get("ts", ""))
            chosen = None
            for r in reversed(rs):
                if r.get("total") is not None:
                    chosen = r
                    break
            by_task[t][l] = chosen or rs[-1]

    labels_order = ["claude", "blackwell", "3090s"]
    seen_labels = set()
    for v in by_task.values():
        seen_labels.update(v.keys())
    labels_order = [l for l in labels_order if l in seen_labels] + [
        l for l in sorted(seen_labels) if l not in labels_order
    ]

    print(f"## Per-task (latest run per backend)\n")
    header = "| task |" + "".join(f" {l} |" for l in labels_order)
    sep = "|------|" + "".join("--------|" for _ in labels_order)
    print(header)
    print(sep)

    def cell(r):
        if r is None:
            return "—"
        p = r.get("passed")
        t_ = r.get("total")
        tps = r.get("tok_s")
        wall = r.get("wall")
        if not t_:
            # No spec data (timeout, no code extracted, pytest collected 0).
            bits = ["⏱"]
            if wall:
                bits.append(f"{wall:.0f}s")
            return " ".join(bits)
        spec = f"{p}/{t_}"
        if p != t_:
            spec = f"❌ {spec}"
        bits = [spec]
        if tps:
            bits.append(f"{tps:.0f}t/s")
        if wall:
            bits.append(f"{wall:.1f}s")
        return " · ".join(bits)

    import re
    REPO_URL = "https://github.com/timkoopmans/llm-bench/blob/main"
    LCB_RE = re.compile(r"^p\d+_")
    def task_link(t):
        if LCB_RE.match(t or ""):
            return f"[{t[:50]}]({REPO_URL}/scripts/specs/lcb/{t}.py)"
        return f"[{t[:50]}]({REPO_URL}/scripts/specs/{t}.py)"

    totals = {l: [0, 0] for l in labels_order}  # passed, total
    for t in sorted(by_task.keys()):
        row = by_task[t]
        line = f"| {task_link(t)} |"
        for l in labels_order:
            r = row.get(l)
            line += f" {cell(r)} |"
            if r and r.get("total"):
                totals[l][0] += r["passed"] or 0
                totals[l][1] += r["total"]
        print(line)

    # Footer totals row
    total_line = "| **TOTAL passed** |"
    for l in labels_order:
        p, t_ = totals[l]
        total_line += f" **{p}/{t_}** |" if t_ else " — |"
    print(total_line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
