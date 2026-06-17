# Project File Map

What each file is and where it belongs. **CORE** = upload as a project file.
**INSTRUCTIONS FIELD** = paste into the project's Instructions box, not as a file.
**OPTIONAL** = useful reference/worked example; add if you want it.

## The two layers

The project runs on two interlocking layers:

- **The entry layer** (`01`–`12` + the personas + `render-entry.py`) — produces the
  deep, per-pericope **entries** and renders each to its standard reading page: the
  template, style, methodology, worked example, the 18-agent review panel, and the
  rendering spec + renderer that give every story the same look and behaviour.
- **The reference / index layer** (`R0`–`R6` + the architecture doc) — catalogues
  and **scores** the whole field across six parallel corpora. Built as the
  companion to the entry layer (it defers to the Operation Guide and Registry).
  Each deep entry carries the same **`I·C·P·H·A` score line and taxonomy tags** as its
  `R1` stub, so the two layers stay linked.

## Entry layer

| File | What it is | Where it goes |
|---|---|---|
| `00-README-file-map.md` | This map | OPTIONAL |
| `01-project-instructions.md` | The operating brief — a teaching tool for a curious newcomer (cultural literacy, comparative understanding, honest historicity) | **INSTRUCTIONS FIELD** (paste contents) |
| `02-operation-guide.md` | Methodology: who this is for, the two layers, unit-splitting, R0-based prioritization, calibrate-then-scale, copyright/neutrality | **CORE** |
| `03-story-entry-template.md` | The per-entry schema — 5 reading layers (incl. *Why this matters*) + Behind-the-Text fields (incl. *Is it historical?*, *Older sources & cross-tradition parallels*, the optional *Psychoanalytic reading* and *Allegorical reading*) + the `R0` score line and taxonomy tags | **CORE** |
| `04-style-guide.md` | Voice/tense/length rules; newcomer audience | **CORE** |
| `05-example-cain-and-abel.md` | The worked example / quality bar — **v1.2** (now carries its `I5·C4·P5·H2·A0` score) | **CORE** |
| `06-story-index.md` | The **production plan** — calibration set, draft order, status (defers the canonical catalogue to `R1`) | **CORE** |
| `07-expert-panel-and-review.md` | The **18-agent** roster + the review/convergence workflow | **CORE** |
| `10-recurring-elements-registry.md` | Source of truth for canonical names/places/motifs + conventions (divine-name, Islamic naming, taxonomy link, collision watchlist) | **CORE** *(living; Managing Editor maintains)* |
| `12-rendering-spec.md` | The **rendering standard** — the fixed look, behaviour, accessibility floor, and authoring contract for every entry's reading page; owned by #15 | **CORE** |
| `render-entry.py` | The **canonical renderer** — turns any entry `.md` into the standard self-contained dark HTML reading page (run `python render-entry.py ENTRY.md`); the single code path so all stories render identically | **CORE** (tool) |
| `persona-01 … persona-18` | The **18** agent personas — #1–#13 the maker/reviewer panel (several owning an `R0` axis), plus **#14 Indexer / Librarian** (catalogue integrity), **#15 Visual & Front-End Design Reviewer** (the rendered-companion / artifact layer), **#16 Psychoanalytic & Depth-Psychology Critic** (the psychoanalytic-reading section), **#17 Allegorical & Figural Reader** (the allegorical-reading section), and **#18 Explanatory Graphics & Motion Designer** (builds the explanatory charts, diagrams, maps, and animations for the artifact layer) | **CORE** |
| `05a-…-v0.2.md` · `08-…-review-log.md` · `09-…-12agent-rerun….md` | Raw draft + review-loop records (historical) | OPTIONAL |

## Reference / index layer

| File | What it is | Where it goes |
|---|---|---|
| `A_Scholarly_Bible_Companion-_Reference_Architecture….md` | The meta-spec for the five-corpora reference system | **CORE** (reference) |
| `R0-scoring-rubric.md` | The shared **5-axis rubric** (I·C·P·H·A) + controlled **keyword taxonomy**; the axis-ownership map | **CORE** (reference) |
| `R1-bible-canon-reference.md` | The **master catalogue**: Protestant 66, unit by unit, with descriptions, links, keywords, and scores | **CORE** (reference) |
| `R2-torah-reference.md` | The Torah in **Jewish framing** (parashot, Tanakh, rabbinic anchors) — persona #5's shelf | **CORE** (reference) |
| `R3-quran-reference.md` | The **Quran** (114 suras + shared-prophet divergences) — persona #13's shelf | **CORE** (reference) |
| `R4-hadith-reference.md` | The **Hadith** (grading, collections, parallels) — persona #13's shelf | **CORE** (reference) |
| `R5-ancient-near-eastern-reference.md` | **ANE & related sources** with relationship grades — persona #4's shelf | **CORE** (reference) |
| `R6-book-of-mormon-reference.md` | The **Book of Mormon** in its own (Latter Day Saint) framing — 15 internal books, unit by unit, with heavy `→R1` cross-links and the origin/historicity debate in three attributed voices — persona #13's shelf, with #12 on the Restorationist-movement and intra-movement (LDS / Community of Christ) dimension | **CORE** (reference) |

## Action list for syncing the project (panel now #1–#18)
This pass adds the Explanatory Graphics & Motion Designer (#18) — a maker for the
artifact layer who decides where a passage wants a diagram, chart, map, genealogy,
timeline, or animation and builds it, alongside the Design Reviewer (#15) who reviews
the look. #18 owns no entry-schema field; it works at the rendered-artifact layer.

1. **Add:** `persona-18-graphics-motion.md`.
2. **Re-upload** the updated docs: `07-expert-panel-and-review.md` (adds the #18 card;
   18-agent roster), this `00-README`, `persona-01` (panel now #1–#18), and
   `11-project-test-prompts.md` (panel-size count).
3. **Also this pass — rendering standard:** the Cain & Abel reading page's look and
   behaviour are now codified so every future story matches it. **Add**
   `12-rendering-spec.md` and `render-entry.py`; **re-upload** `02-operation-guide.md`
   (new standing decision 3.7 + checklist item), `03-story-entry-template.md` (The
   Reading is now *1 · The text* + *2 · How the translations differ*, replacing the
   Faithful-translation + KJV layers), `persona-15` and `persona-18` (point to the
   spec).
4. Everything else is unchanged this pass.
## Latest pass — add the Book of Mormon (`R6`)
Adds a sixth corpus to the reference layer: the Book of Mormon, framed in its own
right (Latter Day Saint reception), unit by unit, with heavy back-links to `R1` and the
origin/historicity question handled in three attributed voices (faith claim / academic
consensus / apologetics). Scored on the full five-axis `I·C·P·H·A` rubric; the
Attestation (A) axis is applied per the note at the top of `R6` (datable ancient-event
units → A1 under the mainstream consensus; doctrine/sermon/vision/quotation → A0).

1. **Add:** `R6-book-of-mormon-reference.md`.
2. **Re-upload** `R0-scoring-rubric.md` (adds `R6` to the corpus list and the `→bom`
   cross-corpus tag in Facet E), `R1-bible-canon-reference.md` (adds `→bom` back-links
   at the entries the Book of Mormon quotes/reworks — the Isaiah blocks, the Sermon on
   the Mount, Romans/olive tree, Malachi, Babel — plus `R6` in its companion line), and
   this `00-README`.
3. **Owner:** `R6` sits on persona **#13**'s (Comparative Religion) shelf, with **#12**
   (Schism & Sectarian-Formation) on the Restorationist-movement and intra-movement
   (LDS / Community of Christ) dimension. No new persona is required; if the panel later
   wants a dedicated Latter Day Saint specialist, that would be a future addition.
4. Everything else is unchanged this pass.
   **Personas — none split; all 18 are individual files** (`persona-01`–`persona-18`).
   #14 (Indexer / Librarian) owns catalogue integrity, #15 (Visual & Front-End Design
   Reviewer) owns the rendered-companion / artifact layer, #16 (Psychoanalytic &
   Depth-Psychology Critic) owns the psychoanalytic-reading section, and #17 (Allegorical
   & Figural Reader) owns the allegorical-reading section, and #18 (Explanatory Graphics & Motion Designer) owns the explanatory-visual layer of rendered artifacts — all active members.
