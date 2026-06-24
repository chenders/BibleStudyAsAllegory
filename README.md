# Bible Companion

A plain-English companion to the Bible for people who want to understand it as a foundational text of the surrounding culture, not as a believer or a critic.

## Contents

- [What this is](#what-this-is)
- [Project status](#project-status)
- [Repository layout](#repository-layout)
- [The reference shelf](#the-reference-shelf)
- [The five-axis score](#the-five-axis-score)
- [The expert panel](#the-expert-panel)
- [How an entry is built](#how-an-entry-is-built)
- [Getting started](#getting-started)
- [Editorial principles](#editorial-principles)
- [License](#license)

## What this is

Bible Companion is a teaching tool for a curious newcomer: someone who is not religious, has never read the Bible, and wants to understand it the way they would understand any work that shaped the language, law, and art around them. It assumes no prior knowledge and explains every name, custom, and reference as it comes up.

The Bible is broken into units. A unit is one coherent passage, and each unit becomes one entry. The entry retells the passage in vivid present-day English, then surrounds that retelling with structured metadata: the original-language notes, a public-domain scripture quotation, what the passage means, why it matters, and how different traditions and scholars read it.

Three priorities shape every entry:

- **Cultural literacy.** Why the passage matters today, and where it surfaces in everyday language, law, politics, and art.
- **Comparative understanding.** How Jewish, Christian, and Islamic traditions, along with older Near Eastern sources, relate to the text and to each other. Relationships are graded by the strength of the evidence, never asserted.
- **Honest historicity.** What history and archaeology actually say about the passage, stated plainly: neither taking the text at its word nor setting out to debunk it.

The goal is understanding, not persuasion. The project does not argue that the text is true or false, and it does not tell you what to believe.

## Project status

This is early-stage and still in calibration. There are currently **two finished entries** (`cain-and-abel` and `php-04-i-can-do-all-things`), so treat the published work as a small sample rather than a corpus. The system, the reference shelf, and the 19-agent review panel are built out ahead of the entries, so that adding new entries is mostly a matter of running the pipeline.

## Repository layout

```
BibleUnderstanding/
├── entries/          One Markdown file per finished unit (a coherent passage = one entry).
├── reference/        The reference shelf you write *from* — R0 rubric, R1–R6 corpora, and a local KJV.
├── system/           The entry layer you write *with* — template, style guide, op guide.
├── scripts/          Deterministic Python checkers (validation, scoring, copyright, render, KJV fetch).
└── .claude/
    ├── agents/        The 19 specialist subagents (the expert panel).
    ├── commands/      The authoring workflows (/new-entry, /draft-entry, /review-entry, …).
    └── skills/        Validation skills (entry-validator, copyright-guard, score-consistency).
```

| Directory | What lives there |
|---|---|
| `entries/` | The finished entries, one Markdown file per unit. Some entries also ship a rendered `.html` companion. |
| `reference/` | The reference shelf you write *from* — authoritative for scoring, cataloguing, and cross-tradition material. Holds the R0 rubric, the R1–R6 corpora, and the local KJV (gitignored — built on demand, not stored in the repo). |
| `system/` | The entry layer you write *with* — the entry template, the style guide, and the operation guide. |
| `scripts/` | The deterministic checkers (no model needed): validation, score-consistency, copyright, render, and the KJV fetcher. |
| `.claude/agents/` | The 19 specialist subagents that make up the expert panel. |
| `.claude/commands/` | The authoring workflows, exposed as slash commands. |
| `.claude/skills/` | Validation skills that wrap the scripts and trigger automatically. |

## The reference shelf

The reference layer is the material every entry is written *from*. It is **R0 (the scoring rubric) plus six parallel corpora, R1–R6**, alongside a local copy of the King James Version for quotation and text-searching (grep).

| Shelf | File | What it is |
|---|---|---|
| R0 | `reference/R0-scoring-rubric.md` | The five-axis scoring rubric plus the controlled keyword taxonomy. |
| R1 | `reference/R1-bible-canon-reference.md` | Master catalogue of the Protestant 66-book canon. Authoritative for score consistency. |
| R2 | `reference/R2-torah-reference.md` | The Torah in Jewish framing (54 parashot). |
| R3 | `reference/R3-quran-reference.md` | The 114 suras of the Qur'an. |
| R4 | `reference/R4-hadith-reference.md` | Hadith and the major collections. |
| R5 | `reference/05-ancient-near-eastern-reference.md` | Ancient Near Eastern source texts. The file is named `05-…`, but its H1 and shelf label are R5. |
| R6 | `reference/R6-book-of-mormon-reference.md` | Book-by-book Book of Mormon reference. |

A local KJV lives in `reference/kjv/`. It is **gitignored** and built on demand by `scripts/fetch_kjv.py` from the public-domain Project Gutenberg KJV. It produces one greppable file per book, with lines in the form `Book C:V<TAB>text`.

## The five-axis score

Every unit is scored on five independent axes, written as `I·C·P·H·A`:

| Axis | Name | Reads |
|---|---|---|
| I | Influence | How much the passage has shaped culture, language, law, and art. |
| C | Contestedness | How much traditions and scholars disagree over it. |
| P | Popularity | How widely it is known and circulated today. |
| H | Harm | The weight of its documented harmful reception. |
| A | Attestation | How well the underlying events or figures are evidenced. |

Each axis runs **0–5, is read independently, and is anchored to concrete evidence**. The axes are never collapsed into a single number. On attestation, mind the low end: **A0 = no testable claim** (primeval or symbolic material), while **A2 = legendary or unverifiable** (named figures beyond the reach of evidence).

## The expert panel

Drafting and review run through **19 specialist subagents** in `.claude/agents/`. Each has its own system prompt, tools, and model, and runs in its own context. The managing editor scopes the panel for a given passage rather than convening all nineteen every time.

| Group | Agents |
|---|---|
| Tradition scholars | `jewish-tradition`, `christian-tradition`, `comparative-religion` |
| Historical & critical | `historical-critical`, `ancient-world-historian`, `translation-languages`, `schism-historian` |
| Reception, harm & belief | `reception-culture`, `reception-harm-historian`, `sociologist-belief` |
| Interpretive lenses | `allegorical-reader`, `psychoanalytic-critic` |
| Prose & narrative | `narrative-writer` |
| Artifact, design & accessibility | `visual-design-reviewer`, `graphics-motion`, `accessibility-standards` |
| Integrity & catalogue | `standards-integrity`, `indexer-librarian` |
| Orchestration | `managing-editor` |

## How an entry is built

Each entry moves through a fixed pipeline. The steps map to slash commands so the process is repeatable.

1. **Scaffold** (`/new-entry`). Confirm the passage and create the entry file from the shared template.
2. **Draft** (`/draft-entry`). Write the retelling first, then the metadata. The plain-English layers come first; original-language notes, the scripture quotation, and the behind-the-text sections follow.
3. **Score** (`/score-unit`). Rate the passage on the five independent axes (Influence, Contestedness, Popularity, Harm, Attestation), with a concrete anchor for each.
4. **Review** (`/review-entry`). Run the panel of specialist reviewers and revise until their feedback converges.
5. **Validate** (`/validate` and `/sync-check`). Check structure, copyright, and that the score matches the master catalogue.
6. **Lock.** An editor integrates the final result and marks the entry locked.

The full slash-command set is `/new-entry`, `/draft-entry`, `/review-entry`, `/score-unit`, `/validate`, `/sync-check`, and `/entry` (which drafts and renders an entry end to end).

## Getting started

This repository is a [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) workspace. Open it by running `claude` in the repository root; the project memory, subagents, commands, and skills load automatically. Entries are authored through the slash commands described above rather than by hand.

One tooling note that matters: run Python scripts through `uv`. (A `PostToolUse` hook also runs the copyright checker automatically whenever an entry is written or edited.) Run any checker as:

```bash
uv run python3 scripts/<name>.py
```

Before quoting or grepping scripture, build the local KJV (it is gitignored and not checked in):

```bash
uv run python3 scripts/fetch_kjv.py
```

## Editorial principles

These rules are not style preferences. They define what the project will and will not do, and they hold for every entry.

- **Copyright.** Every retelling is original writing. Scripture is quoted only from public-domain translations (the World English Bible, the King James Version, or the American Standard Version), and quotations are kept short. Modern copyrighted translations are never reproduced; naming one is fine, pasting its text is not.
- **Neutrality.** Interpretations from different traditions are reported and attributed ("In Catholic tradition...", "Source critics argue..."), and the project never rules on whose theology is correct. This neutrality covers *theological truth-claims* only. It does not soften empirical or historical findings, which are reported on the evidence.
- **No self-censorship.** Any claim that is fair, relevant, and well-sourced belongs in the entry, even if a tradition or group finds it offensive. Offence is never a reason to omit, soften, or hedge. This cuts every direction: critical scholarship on any tradition's founding texts (authorship, dating, revision, historicity, harmful reception) is stated as plainly as the evidence warrants.
- **No generated image of Muhammad.** The project never produces a visual depiction of the Prophet Muhammad, and applies the same restraint to any image with a documented record of provoking lethal reprisal. The reason is **safety, not deference to offence**: such images have repeatedly gotten the people who made or published them, and bystanders, killed (the *Charlie Hebdo* massacre of 2015 and the murder of the schoolteacher Samuel Paty in 2020 are among the documented cases). This restraint applies to *generated images only*. The *text* still treats Muhammad, Islamic aniconism, and the killings themselves as fully and frankly as any other subject. Where a depiction would otherwise appear, the project uses the conventions of Islamic art (a veil, a flame, calligraphy, or absence) and says so.
- **Sensitive reception.** Where a passage has been used to justify harm (slavery, antisemitism, conquest), that history is recorded as documented misuse and clearly rejected, leading with the textual correction. It is never presented as a how-to and never endorsed.
- **Graded relationships.** Connections to older sources and parallels across traditions are described with calibrated language (direct borrowing, shared common tradition, independent parallel, coincidence) and never claim dependence where scholars genuinely disagree.

## License

No license has been chosen yet. **This is a TODO:** there is no `LICENSE` file in the repository, and nothing here should be assumed to be openly licensed until one is added.

Two distinct categories of content will need to be addressed when a license is set:

- **Original prose.** The retellings, metadata, and reference notes are original work authored for this project, and their license is to be determined.
- **Quoted scripture.** Scripture quotations are drawn only from public-domain translations (WEB, KJV, ASV), which carry no copyright restriction in their own right.
