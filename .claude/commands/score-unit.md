---
description: Assign or check the five-axis R0 score for a unit, axis by axis with anchors
argument-hint: [entries/<slug>.md or Book chapter:verses]
allowed-tools: Read, Grep, Glob, Task
---
Score the unit: **$ARGUMENTS** on the five independent R0 axes. Read `reference/R0-scoring-rubric.md` first if present.

Score each axis on its own evidence (don't let a high Influence inflate Popularity, or a high Harm darken Influence), and name at least one concrete anchor per non-zero axis:

- **I — Influence** (reception-culture): named works, settings, films, idioms, uses in law/politics. 0 none → 5 foundational.
- **C — Contestedness** (historical-critical, + schism-historian on battleground texts): the specific crux, named schools, the split. 0 settled → 5 the text is itself a battleground.
- **P — Popularity** (sociologist-belief): survey anchor (with source + year) or idiom penetration. 0 obscure → 5 universal.
- **H — Harm** (harm-historian): documented misuse on the Text→Reception→Consequence→Counter-tradition→Status skeleton. 0 none → 5 catastrophic.
- **A — Attestation** (ancient-world-historian + historical-critical): well-attested / contested / rejected. A0 no testable claim · A1 rejected · A2 legendary · A3 contested · A4 substantially attested · A5 corroborated. Mind the A0-vs-A2 line.

Output the compact line `I# · C# · P# · H# · A#` with a one-line rationale per axis. If the entry exists, compare to its current score line and to its `reference/R1` stub; report any mismatch. Add `(low confidence)` where a score rests on thin evidence. No composite by default.
