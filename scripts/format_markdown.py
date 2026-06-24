#!/usr/bin/env python3
"""PostToolUse hook: conservatively tidy a Markdown file after Claude writes it.

Wired to Write|Edit. Reads the hook payload from stdin and, if the edited file is
Markdown, applies only NON-DESTRUCTIVE tidying:
  - strip trailing whitespace from every line
  - normalize line endings to LF
  - guarantee exactly one trailing newline

It deliberately does NOT run a full reformatter (mdformat / prettier). Both were
tested against the entries and rewrite emphasis markers (`*x*` -> `_x_`), thematic
breaks (`---` -> `____`), and blank-line spacing — producing 25-100+ line diffs and,
in mdformat's case, corrupting authored emphasis. A literary entry is hand-tuned
prose, not source code, so we tidy whitespace and leave the content exactly as written.

Always exits 0 (non-blocking) and only rewrites the file when something actually changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # no/garbled payload — nothing to do
    path = (payload.get("tool_input") or {}).get("file_path")
    if not path or not path.endswith(".md"):
        return
    p = Path(path)
    if not p.is_file():
        return
    try:
        original = p.read_text(encoding="utf-8")
    except Exception:
        return
    body = "\n".join(line.rstrip() for line in original.splitlines())
    tidied = body.rstrip("\n") + "\n" if body.strip() else ""
    if tidied != original:
        p.write_text(tidied, encoding="utf-8")


if __name__ == "__main__":
    main()
