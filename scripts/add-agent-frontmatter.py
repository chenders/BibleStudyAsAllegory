#!/usr/bin/env python3
"""Add or repair Claude Code subagent YAML frontmatter on agent markdown files.

Claude Code loads subagents from `.claude/agents/*.md` and requires YAML
frontmatter with at least `name` and `description` (docs:
https://code.claude.com/docs/en/sub-agents). The markdown body below the
frontmatter becomes the agent's system prompt.

This script adds that frontmatter idempotently:
  - `name`         <- the file's stem (already kebab-case for persona-NN-* files)
  - `description`  <- derived from the file's own H1 title + first italic tagline
  - the existing markdown is preserved verbatim as the body.

It is safe to re-run: files that already carry valid `name` + `description`
frontmatter are left untouched; files with malformed/partial frontmatter are
rebuilt cleanly (the body is never duplicated).

Usage:
    python add-agent-frontmatter.py [DIR] [--apply]

DIR defaults to `.claude/agents`. Without --apply it performs a dry run and
prints what it would change. With --apply it writes the files in place.

IMPORTANT: after applying, RESTART your Claude Code session — subagents are
loaded at session start, so on-disk edits are not picked up until you restart.
"""
import sys, re, pathlib

args = [a for a in sys.argv[1:]]
APPLY = "--apply" in args
pos = [a for a in args if not a.startswith("-")]
DIR = pathlib.Path(pos[0]) if pos else pathlib.Path(".claude/agents")


def derive_description(body: str) -> str:
    """Build a description from the file's first H1 and first italic tagline."""
    title = ""
    start = 0
    m = re.search(r"^#\s+(.+)$", body, re.M)
    if m:
        title = re.sub(r"^Persona\s*[—\-:]\s*", "", m.group(1).strip()).strip()
        start = m.end()

    # first *italic* span after the H1 (may span multiple lines; skips **bold**)
    tagline = ""
    m2 = re.search(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", body[start:], re.S)
    if m2:
        tagline = m2.group(1).strip()

    desc = ". ".join(part for part in (title, tagline) if part) or "Project review agent."
    desc = re.sub(r"[*_`]", "", desc)            # strip leftover markdown emphasis
    desc = re.sub(r"\s+", " ", desc).strip()     # collapse whitespace/newlines

    if len(desc) > 300:                          # truncate politely at a sentence end
        cut = desc[:300]
        desc = (cut[: cut.rfind(". ") + 1] if ". " in cut else cut.rstrip() + "…").strip()

    return desc.replace("\\", "\\\\").replace('"', '\\"')   # YAML double-quote escaping


def strip_frontmatter(text: str):
    """Return (body, had_frontmatter). Removes a leading --- ... --- block if present."""
    if text.startswith("---\n") or text.startswith("---\r\n"):
        m = re.search(r"^---\s*$", text[3:], re.M)
        if m:
            return text[3 + m.end():].lstrip("\n"), True
    return text, False


def main():
    if not DIR.is_dir():
        sys.exit(f"directory not found: {DIR}\n(point me at your agents dir, e.g. .claude/agents)")

    changed = 0
    files = sorted(DIR.glob("*.md"))
    if not files:
        sys.exit(f"no .md files in {DIR}")

    for p in files:
        text = p.read_text(encoding="utf-8")
        body, had_fm = strip_frontmatter(text)
        name = p.stem
        desc = derive_description(body)
        new = f'---\nname: {name}\ndescription: "{desc}"\n---\n\n' + body.lstrip("\n")

        if new == text:
            print(f"  ok        {p.name}  (already valid)")
            continue

        print(f"  {'repair' if had_fm else 'add':<9} {p.name}")
        print(f"            name: {name}")
        print(f'            description: "{desc[:88]}{"…" if len(desc) > 88 else ""}"')
        if APPLY:
            p.write_text(new, encoding="utf-8")
        changed += 1

    print()
    if APPLY:
        print(f"Applied to {changed} file(s). Now RESTART your Claude Code session to load them.")
    else:
        print(f"Would change {changed} file(s). Re-run with --apply to write the files.")


if __name__ == "__main__":
    main()
