---
description: Run all structural, copyright, and score-consistency checks on entries
argument-hint: [entries/<slug>.md or blank for all]
allowed-tools: Bash(python3:*), Read
---
Validate **$ARGUMENTS** (or all entries if no argument).

Run, in order, and report results plainly:
1. `python3 scripts/validate_entry.py $ARGUMENTS` — template structure: all required sections, the five reading layers, a well-formed `I·C·P·H·A` score line, and a Status + version/date.
2. `python3 scripts/check_copyright.py $ARGUMENTS` — scan for in-copyright translation markers (NIV/ESV/NLT/NASB/NRSV/CSB/The Message). Naming a translation is fine; pasting its text is not — judge each flag.
3. `python3 scripts/check_scores.py` — each entry's score line vs. its `reference/R1` stub.

Summarize pass/fail per check and list concrete fixes for anything that failed. Do not edit files unless I ask.
