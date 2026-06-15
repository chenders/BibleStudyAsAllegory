---
description: Check that every entry's score line and tags match its R1 catalogue stub
allowed-tools: Bash(python3:*), Read, Grep
---
Verify catalogue consistency between the drafted entries and the master catalogue.

1. Run `python3 scripts/check_scores.py` to compare each `entries/*.md` score line against its stub in `reference/R1-bible-canon-reference.md`.
2. For any mismatch, show the entry's line and the R1 stub's line side by side, and say which is likely correct (the entry, if it has been reviewed more recently; otherwise flag for the managing-editor).
3. List any entry with no matching R1 stub (needs a stub added) and any R1 stub whose unit has been drafted but whose score predates the entry (needs the stub refreshed).
Report only; propose fixes but don't apply them unless I ask.
