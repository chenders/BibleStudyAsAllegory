---
description: Run the expert-panel review loop on a drafted entry until it converges
argument-hint: [entries/<slug>.md]
allowed-tools: Read, Edit, Grep, Glob, Task, Bash(python3:*)
model: opus
---
Run the review loop on: **$ARGUMENTS**

1. Read the entry. Use the **managing-editor** subagent to pick the review panel the entry needs.
2. Dispatch each relevant specialist subagent as a reviewer of its owned field, plus **standards-integrity** every round (copyright, even-handedness, accuracy, level, completeness). Each returns severity-tagged findings (S1 Critical / S2 Major = blocking; S3–S5 = suggested) and a round verdict.
3. Integrate fixes into the entry. Record what changed and why.
4. Repeat. **Convergence:** stop when a full round returns no BLOCKING and no new SUGGESTED items. Cap ~4 rounds; the managing-editor adjudicates any standoff and records dissent in the Apparatus.
5. Re-run `python3 scripts/validate_entry.py $ARGUMENTS` and `python3 scripts/check_copyright.py $ARGUMENTS`. When clean and converged, set `Status: reviewed` (the managing-editor makes the lock call separately).
6. Confirm the entry's score line and tags still match its `reference/R1` stub; flag any drift.
