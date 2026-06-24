#!/usr/bin/env python3
"""build_index.py — build the publishable site: an index page over all entries,
each entry rendered to its standard HTML reading page, plus a JSON manifest.

For every `entries/*.md` that is a real entry (has a `**Score (R0):**` line), this:
  1. renders it to `<slug>.html` with the canonical renderer (scripts/render-entry.py),
  2. extracts its metadata (title, reference, score, status) for the index, and
  3. writes `index.html` (dark, matching the entry pages) and `manifest.json`.

Usage:
    python scripts/build_index.py [--entries entries] [--out _site]
                                   [--renderer scripts/render-entry.py]

The output directory is what gets uploaded to GitHub Pages.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AXES = ["I", "C", "P", "H", "A"]
AXIS_NAMES = {"I": "Influence", "C": "Contestedness", "P": "Popularity",
              "H": "Harm", "A": "Attestation"}


def field(md: str, name: str) -> str | None:
    """Value of a `**Name:** value` metadata line (the colon is inside the bold)."""
    m = re.search(r"^\*\*" + re.escape(name) + r":\*\*\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else None


def first_backtick(s: str | None) -> str | None:
    if not s:
        return None
    m = re.search(r"`([^`]+)`", s)
    return m.group(1).strip() if m else s.strip()


def strip_md(s: str) -> str:
    return re.sub(r"[*_`]", "", s).strip()


def parse_entry(path: Path) -> dict | None:
    md = path.read_text(encoding="utf-8")
    score_raw = first_backtick(field(md, "Score (R0)"))
    if not score_raw:
        return None  # not an entry (e.g. README.md)

    title = md.splitlines()[0].lstrip("#").strip()
    slug = first_backtick(field(md, "ID / slug")) or path.stem
    axes = {a: int(n) for a, n in re.findall(r"([ICPHA])\s*(\d)", score_raw)}

    status = ""
    m = re.search(r"^\*\*Status:\*\*\s*(.+)$", md, re.M)
    if m:
        bold = re.search(r"\*\*(.+?)\*\*", m.group(1))
        status = strip_md(bold.group(1) if bold else m.group(1))[:80]

    return {
        "slug": slug,
        "file": path.name,
        "html": f"{slug}.html",
        "title": title,
        "reference": strip_md(field(md, "Reference") or "") or None,
        "canon": strip_md(field(md, "Canon(s)") or "") or None,
        "score": score_raw,
        "axes": axes,
        "status": status,
    }


def render_entry(renderer: Path, src: Path, dest: Path) -> bool:
    r = subprocess.run([sys.executable, str(renderer), str(src), str(dest)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not dest.exists():
        print(f"  ! render failed for {src.name}:\n{r.stderr[-400:]}", file=sys.stderr)
        return False
    return True


def score_html(e: dict) -> str:
    spans = []
    for a in AXES:
        n = e["axes"].get(a)
        if n is None:
            continue
        spans.append(f'<span class="ax" title="{AXIS_NAMES[a]}: {n}/5">{a}{n}</span>')
    return '<span class="score">' + "".join(spans) + "</span>" if spans else ""


def esc(s: str | None) -> str:
    if not s:
        return ""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def index_html(entries: list[dict]) -> str:
    rows = []
    for e in entries:
        status = f'<span class="status">{esc(e["status"])}</span>' if e["status"] else ""
        ref = f'<span class="ref">{esc(e["reference"])}</span>' if e["reference"] else ""
        rows.append(
            f'<li><a class="entry" href="{esc(e["html"])}">'
            f'<span class="title">{esc(e["title"])}</span>{ref}</a>'
            f'<span class="meta">{score_html(e)}{status}</span></li>'
        )
    n = len(entries)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bible Companion — Index of entries</title>
<style>
:root{{--ground:#0f1117;--panel:#161a22;--ink:#e7e9ef;--bright:#f5f6fa;--soft:#bfc6d3;
--muted:#979ead;--rule:#242935;--rubric:#c25a4d;}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--ground);color:var(--ink);
font-family:'Source Sans 3',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
line-height:1.5;-webkit-font-smoothing:antialiased;}}
.wrap{{max-width:760px;margin:0 auto;padding:3rem 1.25rem 5rem;}}
h1{{color:var(--bright);font-size:1.9rem;margin:0 0 .25rem;letter-spacing:-.01em;}}
.sub{{color:var(--muted);margin:0 0 2rem;}}
ul{{list-style:none;margin:0;padding:0;}}
li{{padding:1rem 0;border-top:1px solid var(--rule);
display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;justify-content:space-between;}}
a.entry{{text-decoration:none;color:inherit;flex:1 1 22rem;}}
.title{{color:var(--bright);font-weight:600;}}
a.entry:hover .title{{color:var(--rubric);}}
.ref{{display:block;color:var(--muted);font-size:.9rem;margin-top:.15rem;}}
.meta{{display:flex;gap:.6rem;align-items:center;}}
.score{{font-variant-numeric:tabular-nums;font-size:.8rem;color:var(--soft);
letter-spacing:.02em;white-space:nowrap;}}
.score .ax{{padding:.05em .3em;border:1px solid var(--rule);border-radius:4px;margin-left:.15em;}}
.status{{font-size:.72rem;color:var(--muted);text-transform:lowercase;}}
footer{{margin-top:3rem;color:var(--muted);font-size:.8rem;border-top:1px solid var(--rule);padding-top:1rem;}}
footer a{{color:var(--soft);}}
</style></head>
<body><main class="wrap">
<h1>Bible Companion</h1>
<p class="sub">An index of {n} {"entry" if n == 1 else "entries"}. Each is a passage retold in
present-day English with structured metadata and a five-axis score (I·C·P·H·A).</p>
<ul>
{chr(10).join(rows)}
</ul>
<footer>Generated by <code>scripts/build_index.py</code>. Source:
<a href="https://github.com/chenders/BibleStudyAsAllegory">chenders/BibleStudyAsAllegory</a>.</footer>
</main></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entries", default="entries")
    ap.add_argument("--out", default="_site")
    ap.add_argument("--renderer", default="scripts/render-entry.py")
    args = ap.parse_args()

    entries_dir, out_dir, renderer = Path(args.entries), Path(args.out), Path(args.renderer)
    out_dir.mkdir(parents=True, exist_ok=True)

    entries = []
    for md in sorted(entries_dir.glob("*.md")):
        e = parse_entry(md)
        if e is None:
            continue
        if render_entry(renderer, md, out_dir / e["html"]):
            entries.append(e)

    if not entries:
        sys.exit("error: no entries found to index.")

    entries.sort(key=lambda e: e["slug"])
    (out_dir / "index.html").write_text(index_html(entries), encoding="utf-8")
    (out_dir / "manifest.json").write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: {len(entries)} entries -> {out_dir}/ (index.html, manifest.json, "
          f"{len(entries)} entry pages)")


if __name__ == "__main__":
    main()
