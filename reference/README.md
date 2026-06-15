# reference/ — the reference layer (write *from*)

Drop your authoritative corpus files here. The tooling and subagents look for them
by these names (a leading `R#` is all the scripts need):

- `R0-scoring-rubric.md` — the five-axis rubric + controlled taxonomy
- `R1-bible-canon-reference.md` — the master catalogue (entry stubs + scores)
- `R2-torah-reference.md` — Jewish framing
- `R3-quran-reference.md` — Qur'an
- `R4-hadith-reference.md` — Hadith
- `R5-ancient-near-eastern-reference.md` — older Near Eastern sources

`check_scores.py` cross-checks each entry's score line against its `R1` stub; if
`R1` isn't here yet, it says so and exits cleanly. These files are the authority on
scoring, cataloguing, and cross-tradition parallels — defer to them.
