---
description: Scaffold a new entry file from the template, with the header pre-filled
argument-hint: [Book chapter:verses] (e.g. Genesis 22:1-19)
allowed-tools: Read, Write, Bash(mkdir:*)
---
Create a new entry file for the passage: **$ARGUMENTS**

1. Confirm the unit: state the exact reference (book, chapter, verses) and its boundaries. If the passage was named loosely, say which reference you're using and why.
2. Copy the structure of `system/03-story-entry-template.md` into a new file at `entries/<slug>.md`, where `<slug>` follows the pattern in the template (e.g. `gen-22-binding-of-isaac`).
3. Pre-fill only what is certain from the reference itself: the title, reference, ID/slug, timeline position, canon(s), and genre/form. Leave the rest as the template's italic guidance for now.
4. Do not draft prose yet — this command only scaffolds. Tell me the file is ready and suggest running `/draft-entry`.
