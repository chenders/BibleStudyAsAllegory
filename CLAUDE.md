# Bible Companion — Claude Code project memory

A modern, accessible companion to the Bible, written as a **teaching tool for a
curious newcomer** — a reader who is not religious, has never read the Bible, and
wants to understand it the way you'd understand any foundational text of the
surrounding culture. Each unit (one coherent passage = one entry) is retold in
vivid present-day English and surrounded by structured metadata.

Three priorities drive every entry: **cultural literacy** (why this matters — where
it surfaces in language, law, politics, art), **comparative understanding** (how
Jewish, Christian, and Islamic traditions and the older Near Eastern sources relate,
contrast, and borrow — graded, not asserted), and **honest historicity** (what
history and archaeology actually say — graded plainly, neither credulous nor
debunking). Assume no prior knowledge; explain every name, custom, and reference.

## Repository layout

- `system/` — the **entry layer** you write *with*: the template
  (`03-story-entry-template.md`), the style guide (`04`), the operation guide (`02`).
  Drop your other entry-layer files here. `entries/cain-and-abel.md` is the worked
  example and the quality bar.
- `reference/` — the **reference layer** you write *from* (authoritative for scoring,
  cataloguing, and cross-tradition material). Add your `R0`–`R5` files here:
  `R0` scoring rubric, `R1` Bible canon catalogue, `R2` Torah, `R3` Qur'an,
  `R4` Hadith, `R5` Ancient Near Eastern sources.
- `entries/` — the finished entries (one Markdown file per unit).
- `.claude/agents/` — the 13 specialist **subagents** (the expert panel).
- `.claude/commands/` — the **workflows**: `/new-entry`, `/draft-entry`,
  `/review-entry`, `/score-unit`, `/validate`, `/sync-check`.
- `.claude/skills/` — validation skills: entry-validator, copyright-guard,
  score-consistency.
- `scripts/` — the deterministic checkers the skills/commands/hook call.

## How an entry is built

1. `/new-entry "Genesis 22:1-19"` — confirm the unit and scaffold the file from the template.
2. `/draft-entry` — **retelling first, then metadata.** The narrative-writer drafts
   reading layers 3–5; translation-languages does layer 1 and verifies the KJV
   (layer 2); the scoped specialists fill Behind-the-Text. Mark irrelevant fields **n/a**.
3. `/score-unit` — assign the five-axis score `I·C·P·H·A` (see below), one anchor per axis.
4. `/review-entry` — run the panel review loop to convergence; standards-integrity every round.
5. `/validate` and `/sync-check` — structure, copyright, and R1 score consistency.
6. The managing-editor integrates and makes the lock call; set `Status: locked`.

## The five-axis score (R0) — read each independently, 0–5

`I·C·P·H·A` = **Influence · Contestedness · Popularity · Harm · Attestation.**
Never collapse into one number. Anchor each non-zero axis to concrete evidence.
Owners: I→reception-culture, C→historical-critical (+schism-historian on battleground
texts), P→sociologist-belief, H→harm-historian, A→ancient-world-historian (+historical-
critical). The managing-editor integrates and keeps each entry's line matching its `R1` stub.
Attestation note: A0 = no testable claim (primeval/symbolic); A2 = legendary/unverifiable
(named figures beyond evidence). Mind that line.

## Hard rules (always)

- **Copyright.** Retellings are always original prose. Quote scripture only from
  public-domain translations (World English Bible, KJV, ASV), kept short. Never
  reproduce NIV, ESV, NLT, NASB, NRSV, CSB, or The Message — naming one in a note is
  fine, pasting its text is not. Never reproduce song lyrics or poems.
- **Neutrality.** Report interpretations across traditions, attributed ("In Catholic
  tradition…", "Source critics argue…"); never rule on whose theology is correct.
  Keep separate: what the text says · faith interpretations · scholarship · reception.
  Avoid supersessionism (don't present the Christian reading as the true/fulfilled meaning).
- **Sensitive reception.** Where a passage has been used to cause harm (slavery,
  antisemitism, conquest), record it as documented misuse on the Text → Reception →
  Consequence → Counter-tradition → Status skeleton, framed and rejected — never how-to,
  never endorsed. Lead with the textual correction.
- **Grade relationships.** For older sources and cross-tradition parallels, use graded
  language — direct borrowing · shared common tradition · independent parallel ·
  coincidence — never asserting dependence where scholars debate it.

## Calibration mindset

Starting small and iterating; the template, length, and tone will change as we refine
on familiar stories. Treat early entries as drafts. If the schema doesn't fit a passage,
say so and propose a fix rather than forcing it.
