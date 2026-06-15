---
description: Draft a full entry — retelling first, then metadata via the specialist subagents
argument-hint: [entries/<slug>.md or Book chapter:verses]
allowed-tools: Read, Write, Edit, Grep, Glob, Task
model: opus
---
Draft the entry for: **$ARGUMENTS**

Work in this order (retelling first, then metadata — per the Operation Guide):

1. Read `system/03-story-entry-template.md`, `system/04-style-guide.md`, and the worked example `entries/cain-and-abel.md` (the quality bar) if present.
2. Use the **managing-editor** subagent to scope which specialists this passage actually needs — not every expert every time.
3. **THE READING:** use **narrative-writer** for layers 3 (retelling), 4 (what it means), and 5 (why this matters). Use **translation-languages** for layer 1 (faithful translation) and to verify layer 2 (KJV) is genuine public-domain text.
4. **BEHIND THE TEXT:** dispatch the scoped specialists for their owned fields — ancient-world-historian (Setting & Context; Is it historical?; ANE antecedents), historical-critical (Text & Composition), jewish-tradition / christian-tradition / comparative-religion (Interpretation across traditions; the Qur'an cousins), sociologist-belief (Literal or figurative?), reception-culture (Cultural Afterlife), harm-historian (Harmful afterlife, only if applicable), schism-historian (Schisms, only if applicable).
5. Assemble the drafted sections into `entries/<slug>.md`. Mark genuinely-irrelevant fields **n/a** rather than padding.
6. Run `/score-unit` logic to set the `I·C·P·H·A` line, then add Apparatus (sources, confidence/open questions, `Status: draft`, version + today's date).
7. Validate with `python3 scripts/validate_entry.py entries/<slug>.md` and fix any gaps before handing back.

Hard rules throughout: retelling is original prose; quote scripture only from public-domain translations (WEB/KJV/ASV), short; attribute interpretations across traditions rather than ruling on them; frame any harmful reception as rejected misuse.
