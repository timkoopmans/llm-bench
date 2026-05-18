#!/usr/bin/env python3
"""Split a multi-file refactor dump into individual files in a worktree, then exec pytest.

Usage:
  refactor_apply.py <worktree_root> <dump_file> <pytest_args...>

Dump format (model output): segments delimited by lines matching
  # === FILE: <relative-path> ===
Fenced ```python ... ``` wrappers are stripped if present.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

MARKER_RE = re.compile(r"^\s*#\s*===\s*FILE:\s*(.+?)\s*===\s*$", re.MULTILINE)
FENCE_OPEN_RE = re.compile(r"^\s*```(?:python|py)?\s*$", re.MULTILINE)
FENCE_CLOSE_RE = re.compile(r"^\s*```\s*$", re.MULTILINE)


def strip_fences(text: str) -> str:
    """Remove ```python opening and ``` closing fences (anywhere in the segment)."""
    text = FENCE_OPEN_RE.sub("", text)
    text = FENCE_CLOSE_RE.sub("", text)
    return text.strip("\n") + "\n"


def split_dump(dump: str) -> list[tuple[str, str]]:
    """Return list of (relative_path, content) from a multi-file dump."""
    parts = MARKER_RE.split(dump)
    # parts: [preamble, path1, body1, path2, body2, ...]
    out: list[tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        path = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        out.append((path, strip_fences(body)))
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    wt_root = Path(sys.argv[1]).resolve()
    dump_path = Path(sys.argv[2])
    pytest_args = sys.argv[3:]

    if not wt_root.is_dir():
        print(f"worktree not found: {wt_root}", file=sys.stderr)
        return 2
    if not dump_path.is_file():
        print(f"dump not found: {dump_path}", file=sys.stderr)
        return 2

    dump = dump_path.read_text()
    files = split_dump(dump)
    if not files:
        print("no '# === FILE: ... ===' markers found in dump", file=sys.stderr)
        return 1

    written = 0
    for rel, body in files:
        # Reject absolute paths or paths escaping worktree.
        if rel.startswith("/") or ".." in Path(rel).parts:
            print(f"skip unsafe path: {rel}", file=sys.stderr)
            continue
        target = (wt_root / rel).resolve()
        try:
            target.relative_to(wt_root)
        except ValueError:
            print(f"skip path outside worktree: {rel}", file=sys.stderr)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)
        print(f"  wrote {target.relative_to(wt_root)}  ({len(body)} bytes)")
        written += 1

    if written == 0:
        return 1

    env = os.environ.copy()
    env["PYTHONPATH"] = str(wt_root / "src") + (
        ":" + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    proc = subprocess.run(pytest_args, cwd=wt_root, env=env)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
