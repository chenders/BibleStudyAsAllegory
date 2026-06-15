#!/usr/bin/env python3
"""
validate_entry.py - check a Bible-companion entry against the project template.

Usage:
    python3 scripts/validate_entry.py entries/gen-22-binding-of-isaac.md
    python3 scripts/validate_entry.py entries/      # all .md in a dir
    python3 scripts/validate_entry.py               # defaults to entries/

Exit code 0 if every checked entry passes; 1 if any entry has missing
required elements. Sections legitimately marked "n/a" count as present.
"""
import re
import sys
from pathlib import Path

HEADER_FIELDS = ["Reference", "ID / slug", "Genre / form", "Score (R0)", "Keywords"]

READING_LAYERS = [
    "Faithful translation",
    "King James",
    "Plain-English retelling",
    "What it means",
    "Why this matters",
]

BEHIND_SECTIONS = [
    "Setting & Context",
    "Text & Composition",
    "Is it historical?",
    "Interpretation across traditions",
    "Literal or figurative?",
    "Parallel Accounts",
    "Older sources & cross-tradition parallels",
    "Schisms",
    "Connections",
    "Cultural Afterlife",
    "Apparatus",
]

SCORE_5 = re.compile(r"I[0-5].{0,4}C[0-5].{0,4}P[0-5].{0,4}H[0-5].{0,4}A[0-5]")
SCORE_4 = re.compile(r"I[0-5].{0,4}C[0-5].{0,4}P[0-5].{0,4}H[0-5]")
STATUS = re.compile(r"status\b[^\n]{0,80}\b(draft|reviewed|locked)\b", re.I)
VERSION = re.compile(r"v\d+(\.\d+)?\b|\d{4}-\d{2}-\d{2}")


def has(text_lower, needle):
    return needle.lower() in text_lower


def check_entry(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    errors, warnings = [], []

    if not re.search(r"^#\s+\S", text, re.M):
        errors.append("missing H1 title line (# Title - subtitle)")

    for f in HEADER_FIELDS:
        if not has(low, f):
            errors.append('missing header field: "%s"' % f)

    for layer in READING_LAYERS:
        if not has(low, layer):
            errors.append('missing reading layer: "%s"' % layer)

    for sec in BEHIND_SECTIONS:
        if not has(low, sec):
            errors.append('missing section: "%s"' % sec)

    if SCORE_5.search(text):
        pass
    elif SCORE_4.search(text):
        warnings.append("score line has four axes - add the fifth (A = Attestation)")
    else:
        errors.append("no well-formed score line I# . C# . P# . H# . A# found")

    if not STATUS.search(text):
        errors.append("Apparatus missing a Status line (draft | reviewed | locked)")
    if not VERSION.search(text):
        warnings.append("Apparatus missing a version or date (e.g. v0.1 - YYYY-MM-DD)")

    return errors, warnings


def gather(arg):
    p = Path(arg)
    if p.is_dir():
        return sorted(p.glob("*.md"))
    if p.is_file():
        return [p]
    return []


def main():
    args = sys.argv[1:] or ["entries"]
    files = []
    for a in args:
        files.extend(gather(a))
    files = [f for f in files if f.name.lower() != "readme.md"]

    if not files:
        print("validate_entry: no entry files found.")
        return 0

    any_fail = False
    for f in files:
        errors, warnings = check_entry(f)
        if errors:
            any_fail = True
            print("FAIL  %s" % f)
            for e in errors:
                print("        x %s" % e)
            for w in warnings:
                print("        ~ %s" % w)
        else:
            print("PASS  %s" % f)
            for w in warnings:
                print("        ~ %s" % w)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
