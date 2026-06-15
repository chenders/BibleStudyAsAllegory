#!/usr/bin/env python3
"""
check_copyright.py - scan text for in-copyright Bible translation markers.

Usage:
    python3 scripts/check_copyright.py entries/
    python3 scripts/check_copyright.py entries/gen-22-binding-of-isaac.md

Supports the project hard rule: quote scripture only from public-domain
translations (World English Bible, KJV, ASV); the retelling is always original.

This is a heuristic. NAMING a translation in a note is allowed; PASTING its
text is not. Each flag is a prompt to check, not a verdict. Exits 0 (advisory)
so it is safe to run from a non-blocking hook.
"""
import re
import sys
from pathlib import Path

# (label, regex). Word boundaries on abbreviations to limit false hits.
PATTERNS = [
    ("NIV", re.compile(r"\bNIV\b")),
    ("New International Version", re.compile(r"New International Version", re.I)),
    ("ESV", re.compile(r"\bESV\b")),
    ("English Standard Version", re.compile(r"English Standard Version", re.I)),
    ("NLT", re.compile(r"\bNLT\b")),
    ("New Living Translation", re.compile(r"New Living Translation", re.I)),
    ("NASB", re.compile(r"\bNASB\b")),
    ("New American Standard", re.compile(r"New American Standard", re.I)),
    ("NRSV", re.compile(r"\bN?RSV\b")),
    ("CSB", re.compile(r"\bCSB\b")),
    ("Christian Standard Bible", re.compile(r"Christian Standard Bible", re.I)),
    ("The Message", re.compile(r"\bThe Message\b")),
    ("MSG", re.compile(r"\bMSG\b")),
]


def scan(path):
    hits = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:
        return hits
    for n, line in enumerate(lines, 1):
        for label, rx in PATTERNS:
            if rx.search(line):
                hits.append((n, label, line.strip()[:100]))
    return hits


def gather(arg):
    p = Path(arg)
    if p.is_dir():
        return sorted(p.glob("**/*.md"))
    if p.is_file():
        return [p]
    return []


def main():
    args = sys.argv[1:] or ["entries"]
    files = []
    for a in args:
        files.extend(gather(a))
    files = [f for f in files if f.name.lower() != "readme.md"]

    total = 0
    for f in files:
        hits = scan(f)
        if hits:
            print("~ %s" % f)
            for n, label, snippet in hits:
                total += 1
                print("    line %d: %s  |  %s" % (n, label, snippet))

    if total:
        print("\ncopyright-guard: %d potential flag(s). Naming a translation is fine; "
              "reproducing its text is not - check each." % total)
    else:
        print("copyright-guard: no in-copyright translation markers found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
