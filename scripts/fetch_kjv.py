#!/usr/bin/env python3
"""Download the King James Version (Project Gutenberg eBook #10) and split it
into one greppable plain-text file per book under reference/kjv/.

The source is the standard 66-book Protestant KJV — no Apocrypha (that is simply
what eBook #10 contains). KJV is public domain, so the full text may live in the
repo's reference layer; we keep it gitignored and regenerate it with this script.

Each output line is `Book C:V\ttext`, e.g.

    John 3:16\tFor God so loved the world, ...

so `grep "John 3:16" reference/kjv/` returns a citable line directly, and a
recursive grep across the directory finds any phrase in the canon.

Usage:
    python3 scripts/fetch_kjv.py                 # download and build
    python3 scripts/fetch_kjv.py --source FILE   # use a local pg10.txt
    python3 scripts/fetch_kjv.py --out DIR        # write somewhere else
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

SOURCE_URL = "https://www.gutenberg.org/cache/epub/10/pg10.txt"

# The two section dividers in the body (and in the table of contents). They are
# not books and must be skipped. Note the wording differs between the two.
OT_DIVIDER = "The Old Testament of the King James Version of the Bible"
NT_DIVIDER = "The New Testament of the King James Bible"
END_MARKER = "*** END OF THE PROJECT GUTENBERG"

# A verse marker, matched anywhere in joined text. The lookbehind keeps us from
# matching the tail of a longer number; KJV prose has no other `\d+:\d+` patterns.
VERSE_RE = re.compile(r"(?<!\d)(\d+):(\d+)\s+")
BOOK_START_RE = re.compile(r"^1:1\s")  # a book's first verse is always at line start

# Canonical Protestant order. The Gutenberg headings are verbose ("The First
# Book of Moses: Called Genesis"); we zip them positionally with these display
# names, which also drive the zero-padded filenames. If the source ever drifts
# from this 66-book order the verse/heading asserts below will catch it.
BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]
EXPECTED_BOOKS = 66
EXPECTED_VERSES = 31102  # well-known KJV total; a complete-parse sanity gate


def slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def fetch_source(source: str | None) -> str:
    if source:
        return Path(source).read_text(encoding="utf-8")
    print(f"Downloading {SOURCE_URL} ...", file=sys.stderr)
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as resp:
        return resp.read().decode("utf-8")


def extract_body(text: str) -> str:
    """Return the scripture body: from the 2nd OT-divider line (the first is the
    table of contents) up to the Gutenberg end marker."""
    lines = text.splitlines()
    ot_positions = [i for i, ln in enumerate(lines) if ln.strip() == OT_DIVIDER]
    if len(ot_positions) < 2:
        sys.exit(f"error: expected >=2 '{OT_DIVIDER}' lines (TOC + body), "
                 f"found {len(ot_positions)} — source format may have changed.")
    start = ot_positions[1]
    end = next((i for i, ln in enumerate(lines) if END_MARKER in ln), len(lines))
    return "\n".join(lines[start:end])


def _heading_above(lines: list[str], start: int) -> tuple[str, int]:
    """The book title is the nearest non-blank, non-divider line above a book's
    1:1 marker (the lines between are: blank, title, blank, testament divider)."""
    j = start - 1
    while j >= 0:
        s = lines[j].strip()
        if s and s not in (OT_DIVIDER, NT_DIVIDER):
            return s, j
        j -= 1
    return "(unknown)", start


def _parse_verses(seg: list[str]) -> list[tuple[int, int, str]]:
    """Verses in one book segment. Markers (`C:V`) can appear anywhere, not just
    at line start, because Gutenberg wraps text and a new verse may begin partway
    through a physical line. So we join the segment and split on every marker."""
    text = " ".join(s for s in (ln.strip() for ln in seg)
                    if s and s not in (OT_DIVIDER, NT_DIVIDER))
    text = re.sub(r"\s+", " ", text).strip()
    markers = list(VERSE_RE.finditer(text))
    verses = []
    for i, m in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        verses.append((int(m.group(1)), int(m.group(2)),
                       text[m.end():end].strip()))
    return verses


def parse_books(body: str) -> list[tuple[str, list[tuple[int, int, str]]]]:
    """Split the body into (heading, verses) per book, in source order.

    Books are delimited by their `1:1` marker — chapter 1, verse 1 occurs exactly
    once per book and nowhere else, which is far more reliable than blank lines
    (some verses, e.g. Genesis 31:48, contain a paragraph break)."""
    lines = body.splitlines()
    starts = [i for i, ln in enumerate(lines) if BOOK_START_RE.match(ln)]
    heads = [_heading_above(lines, st) for st in starts]

    books: list[tuple[str, list[tuple[int, int, str]]]] = []
    for k, st in enumerate(starts):
        # End the segment at the *next* book's title so its preamble doesn't
        # bleed in as a continuation of this book's last verse.
        seg_end = heads[k + 1][1] if k + 1 < len(starts) else len(lines)
        verses = _parse_verses(lines[st:seg_end])
        books.append((heads[k][0], verses))
    return books


def write_books(books, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    index_rows = []
    for i, ((heading, verses), name) in enumerate(zip(books, BOOKS), start=1):
        fname = f"{i:02d}-{slug(name)}.txt"
        lines = [f"# {name} — KJV (Project Gutenberg eBook #10)"]
        for chap, verse, txt in verses:
            lines.append(f"{name} {chap}:{verse}\t{txt}")
        (out_dir / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")
        total += len(verses)
        index_rows.append((fname, name, len(verses), heading))
    write_index(out_dir, index_rows, total)
    return total


def write_index(out_dir: Path, rows, total: int) -> None:
    lines = [
        "# KJV — local reference text",
        "",
        "Source: Project Gutenberg eBook #10 (public domain). Regenerate with "
        "`python3 scripts/fetch_kjv.py`. This directory is gitignored.",
        "",
        "Line format: `Book C:V<TAB>text`. Search with e.g. "
        "`grep \"John 3:16\" reference/kjv/` or `grep -rn \"<phrase>\" reference/kjv/`.",
        "",
        f"{len(rows)} books, {total} verses.",
        "",
        "| File | Book | Verses | Gutenberg heading |",
        "| --- | --- | --- | --- |",
    ]
    for fname, name, n, heading in rows:
        lines.append(f"| `{fname}` | {name} | {n} | {heading} |")
    (out_dir / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", help="local pg10.txt instead of downloading")
    ap.add_argument("--out", default="reference/kjv", help="output directory")
    args = ap.parse_args()

    body = extract_body(fetch_source(args.source))
    books = parse_books(body)

    if len(books) != EXPECTED_BOOKS:
        sys.exit(f"error: parsed {len(books)} books, expected {EXPECTED_BOOKS}. "
                 f"First headings: {[h for h, _ in books[:3]]}")

    out_dir = Path(args.out)
    total = write_books(books, out_dir)

    if total != EXPECTED_VERSES:
        sys.exit(f"error: parsed {total} verses, expected {EXPECTED_VERSES} — "
                 f"the parse is incomplete; files were written but are suspect.")

    print(f"OK: {len(books)} books, {total} verses -> {out_dir}/")


if __name__ == "__main__":
    main()
