---
name: score-consistency
description: Check that each drafted entry's five-axis score line matches its stub in the R1 master catalogue. Use after scoring or editing an entry, before lock, or when asked whether the catalogue and entries are in sync. Surfaces score drift between entries/ and reference/R1.
---
# Score consistency

Compares the `Score (R0)` line on each `entries/*.md` against the `Score:` line of its stub in `reference/R1-bible-canon-reference.md`, so the entry and the master catalogue never disagree.

## Run it
```
python3 scripts/check_scores.py
```

## What it reports
- **Mismatches** — an entry whose `I·C·P·H·A` line differs from its R1 stub (shows both).
- **Missing stub** — a drafted entry with no matching R1 entry (a stub should be added).
- **Unmatched** — entries whose reference couldn't be located in R1.

If `reference/R1-bible-canon-reference.md` isn't present yet, the check explains that and exits cleanly.

## How to resolve
The reviewed entry is usually authoritative; update the R1 stub to match it (and note the change). If the entry is the one that drifted, fix the entry. The managing-editor owns the final call and keeps R1 consistent.
