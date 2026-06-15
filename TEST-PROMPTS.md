# Test prompts — verify the Claude Code setup

Run these in a fresh `claude` session started **inside this repo**. Each confirms a
specific piece is live. A passing answer is described after each.

## 1 — Project memory (CLAUDE.md loaded)
> "Without reading any files, what is this project, what are its two file layers, and what are the hard rules?"

*Pass:* it states the teaching-tool-for-a-newcomer brief; distinguishes the entry
layer (`system/`) from the reference layer (`reference/`, R0–R5, authoritative for
scoring and cross-tradition material); and lists the copyright (public-domain only),
neutrality (attribute, don't adjudicate), and sensitive-reception rules. *Fail:* it
asks what the project is, or misses the layers.

## 2 — Subagents registered
> "List the specialist subagents available in this project and what each one owns. Which would you convene for the Binding of Isaac, and which would you leave out?"

*Pass:* it names the 13 from `.claude/agents/` with correct ownership, and scopes a
sensible panel (e.g. include translation-languages, ancient-world-historian,
historical-critical, jewish/christian/comparative-religion, sociologist-belief,
reception-culture, harm-historian; leave out schism-historian). *Fail:* invents
agents or can't list them.

## 3 — A subagent actually runs
> "Use the score-unit command to propose a five-axis score for the Binding of Isaac (Genesis 22:1-19), with one anchor per axis."

*Pass:* `/score-unit` runs; it returns `I·C·P·H·A` with an anchor per axis and the
A0-vs-A2 reasoning for Attestation (A2, legendary — patriarchs beyond evidence, not
A0). *Fail:* the command isn't found, or it scores on four axes.

## 4 — Validator skill / script
> "Validate the Cain and Abel entry."

*Pass:* it runs `python3 scripts/validate_entry.py entries/cain-and-abel.md` (via the
entry-validator skill or the `/validate` command) and reports PASS. Then ask it to
validate a passage you haven't drafted — it should report the file doesn't exist.

## 5 — Copyright guard (skill + hook)
> "Add a line to a scratch entry that quotes the NIV, save it, then check copyright."

*Pass:* the `PostToolUse` hook and/or `check_copyright.py` flag the NIV line, and
Claude explains that naming a translation is fine but reproducing its text is not, and
offers an original or public-domain (WEB/KJV/ASV) replacement. *Fail:* no flag.
(Delete the scratch file afterward.)

## 6 — Score consistency against R1
> "Run the score-consistency check and tell me whether every entry matches its R1 stub."

*Pass:* with `reference/R1-...md` present, `check_scores.py` compares each entry's
score line to its stub and reports matches/mismatches. Without R1, it says R1 isn't
present yet and exits cleanly (not an error). *Fail:* it crashes or invents results.

## 7 — End-to-end (the real test)
> "Scaffold and draft a short entry for the Tower of Babel (Genesis 11:1-9): retelling first, then the metadata, then score it and validate."

*Pass:* `/new-entry` scaffolds `entries/gen-11-...md` from the template;
`/draft-entry` produces the five reading layers (original retelling, no copyrighted
translation) and the scoped Behind-the-Text fields; it scores roughly
`I4·C2·P4·H2·A0` (H2 for the apartheid / "separate development" reception, framed as
misuse — not H0); and `validate_entry.py` returns PASS. *Fail:* it copies a
translation, skips the harm framing, or the validator fails.

---
If 1–6 pass, the plumbing is live; 7 confirms the whole pipeline produces a
template-clean, rule-respecting entry end to end.
