#!/usr/bin/env python3
"""
check_scores.py - check each entry's five-axis score line against its R1 stub.

Usage:
    python3 scripts/check_scores.py

Compares the `Score (R0)` line of every entries/*.md against the `Score:` line
of its matching stub in reference/R1-bible-canon-reference.md. If R1 is not
present yet, it says so and exits cleanly.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
REF = ROOT / "reference"

SCORE = re.compile(r"I[0-5]\D{0,4}C[0-5]\D{0,4}P[0-5]\D{0,4}H[0-5](?:\D{0,4}A[0-5])?")
# A Bible reference like "Gen 22:1-19", "Genesis 22:1", "1 Sam 17:1-58".
REFPAT = re.compile(r"\b([1-3]?\s?[A-Z][a-z]+)\.?\s+(\d+):(\d+)(?:[\u2013\u2014-](\d+))?")


def norm_score(s):
    m = SCORE.search(s)
    if not m:
        return None
    return re.sub(r"[^A-Z0-9]", "", m.group(0).upper())


def norm_ref(book, chap, v1, v2):
    b = re.sub(r"\s", "", book).lower()[:4]
    tail = "%s:%s" % (chap, v1)
    if v2:
        tail += "-" + v2
    return b + tail


def find_ref(text):
    m = REFPAT.search(text)
    if not m:
        return None
    return norm_ref(m.group(1), m.group(2), m.group(3), m.group(4))


def load_entries():
    out = []
    if not ENTRIES.is_dir():
        return out
    for f in sorted(ENTRIES.glob("*.md")):
        if f.name.lower() == "readme.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        ref = score = None
        for line in text.splitlines():
            if ref is None and "**Reference:**" in line:
                ref = find_ref(line)
            if score is None and "Score" in line and SCORE.search(line):
                score = norm_score(line)
        out.append((f.name, ref, score))
    return out


def load_r1():
    """Return {normalized_ref: (score, rawline)} from the R1 catalogue."""
    cat = {}
    if not REF.is_dir():
        return None
    r1files = list(REF.glob("R1*.md"))
    if not r1files:
        return None
    lines = r1files[0].read_text(encoding="utf-8", errors="replace").splitlines()
    last_ref = None
    for line in lines:
        # A reference wrapped in backticks marks the start of a stub.
        for m in re.finditer(r"`([^`]+)`", line):
            r = find_ref(m.group(1))
            if r:
                last_ref = r
                break
        if "Score" in line:
            sc = norm_score(line)
            if sc and last_ref and last_ref not in cat:
                cat[last_ref] = (sc, line.strip())
    return cat


def main():
    entries = load_entries()
    if not entries:
        print("check_scores: no entries found in entries/.")
        return 0

    cat = load_r1()
    if cat is None:
        print("check_scores: reference/R1-bible-canon-reference.md not found - "
              "add it to cross-check entry scores against the catalogue. Entry scores read:")
        for name, ref, score in entries:
            print("    %-34s ref=%s score=%s" % (name, ref, score))
        return 0

    problems = 0
    for name, ref, score in entries:
        if not score:
            print("~ %s: no score line found in entry" % name)
            problems += 1
            continue
        if not ref:
            print("~ %s: could not parse a Reference to match against R1" % name)
            problems += 1
            continue
        if ref not in cat:
            print("~ %s (%s): no matching R1 stub - add one to the catalogue" % (name, ref))
            problems += 1
            continue
        r1score, raw = cat[ref]
        if score != r1score:
            problems += 1
            print("MISMATCH %s (%s):" % (name, ref))
            print("    entry: %s" % score)
            print("    R1   : %s   [%s]" % (r1score, raw[:80]))
        else:
            print("ok  %-34s %s == R1" % (name, score))

    print("\ncheck_scores: %d issue(s)." % problems if problems else
          "\ncheck_scores: all entry scores match their R1 stubs.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
