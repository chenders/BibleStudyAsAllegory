---
name: entry-validator
description: Validate a Bible-companion entry against the project template. Use whenever an entry file in entries/ has been created or edited, or when asked to check that an entry is complete, well-formed, or ready for review/lock. Checks the five reading layers, all Behind-the-Text sections, the I·C·P·H·A score line, and the Status/version line.
---
# Entry validator

Checks an entry against `system/03-story-entry-template.md` and reports what's missing.

## Run it
```
python3 "${CLAUDE_SKILL_DIR}/../../../scripts/validate_entry.py" <entry.md | entries/>
```
Or, from the project root, simply: `python3 scripts/validate_entry.py entries/<slug>.md` (pass a directory to check all).

## What it verifies
- The H1 title and the header fields (Reference, ID/slug, Genre/form, Score, Keywords).
- **THE READING** — all five layers present: Faithful translation, King James Version, Plain-English retelling, What it means, Why this matters.
- **BEHIND THE TEXT** — Setting & Context, Text & Composition, Is it historical?, Interpretation across traditions, Literal or figurative?, Parallel Accounts, Older sources & cross-tradition parallels, Schisms, Connections, Cultural Afterlife, Apparatus.
- A well-formed five-axis score line `I# · C# · P# · H# · A#` (a four-axis line is flagged as needing the A migration).
- An Apparatus with `Status:` (draft/reviewed/locked) and a version/date.

## How to use the result
Report PASS/FAIL and the exact missing items. A section legitimately marked **n/a** counts as present. Fix gaps before review; never mark a section done that isn't filled or honestly n/a.
