---
description: Draft and render a Bible-companion entry for a given passage
argument-hint: [book chapter:verse-verse]
---
Create a full project entry for: $ARGUMENTS

Follow the project's own rules end to end, using the project files as the authority:

1. Confirm the unit. Identify the exact passage (book, chapter, verses) and its
   boundaries. If "$ARGUMENTS" is loose — e.g. a chapter where the famous story is
   only part of it — state the precise reference you're using and why before drafting.
2. Draft the retelling first (Narrative Writer, #9), then fill the metadata —
   following `03-story-entry-template.md` exactly, in the voice of `04-style-guide.md`,
   with the methods in `02-operation-guide.md`, matched to the quality bar in
   `05-example-cain-and-abel.md`. Mark genuinely-irrelevant fields n/a; don't pad.
3. Answer the three teaching questions where the passage allows: Why this matters;
   Is it historical? (graded well-attested / contested / rejected); and Older sources
   & cross-tradition parallels (relationship graded: direct borrowing / shared
   tradition / independent parallel / coincidence), drawing comparative material from
   `R1`–`R5`.
4. Score and tag against `R0-scoring-rubric.md` (`I·C·P·H·A`, each 0–5, with one
   `;`-separated rationale clause per axis in that order) and keep the line in sync
   with the `R1` stub.
5. Stay even-handed: distinguish what the text says, traditional readings, scholarship,
   and later reception. Quote only public-domain translations (WEB / KJV / ASV),
   briefly; the retelling is always original prose. Frame any harmful reception clearly
   as misuse, never endorsed, never with how-to detail.
6. Route the prose through #9, the final checks through Standards & Integrity (#10),
   and the rendered page through the Design Reviewer (#15); add explanatory graphics
   via #18 only where they earn their place.
7. Save the entry as `<slug>.md` (slug like `rev-06-four-horsemen`), then render it to
   the standard reading page with `python render-entry.py <slug>.md`, per
   `12-rendering-spec.md`. Report the score line and the output filename when done.
