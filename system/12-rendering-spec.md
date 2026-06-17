# Rendering & Build Spec

*The standard for turning a finished entry into its reading page, so every story
looks and behaves identically. Owned and maintained by the Visual & Front-End Design
Reviewer (#15); the explanatory graphics inside a page are built by the Explanatory
Graphics & Motion Designer (#18). The canonical reference render is
`cain-and-abel.html`, produced from `05-example-cain-and-abel.md`.*

Every entry ships as **one self-contained, dark, screen-native HTML page** —
continuous scroll, no pagination, no external requests at view time. You do not
hand-build it. You run the renderer:

```
python render-entry.py ENTRY.md [OUTPUT.html]
```

`render-entry.py` is the single code path for all entries; output defaults to
`<slug>.html` (slug from the entry's **ID / slug** field). Requires `markdown`,
`fonttools`, `brotli` (`pip install --break-system-packages markdown fonttools
brotli`); the three fonts are used from `./fonts` if present, else downloaded once
from Google Fonts. If the look needs to change, change the renderer (and this spec) —
never one page by hand, or the stories drift apart.
 
---

## 1 · Page anatomy (fixed order)

1. **Eyebrow** — the scripture reference, set as a small caps kicker (from
   **Reference**).
2. **Title** — `# Traditional Title — Descriptive subtitle` as the `<h1>`.
3. **Data strip** — Genre · Setting · Canon · Parallels · ID, compacted (each value
   trimmed at its first `(` or ` — `).
4. **Score bar** — the five axes `Influence · Contested · Popularity · Harm ·
   Attestation`. Each axis is hover-/tap-revealable and carries a popup with: the
   axis name and value, **its definition (drawn from `R0`)**, the 0→5 scale, and
   *this entry's* one-clause rationale (parsed from the `*(…)*` note on the Score
   line, mapped to the axes in `I·C·P·H·A` order). Harm's value is shown in the
   rubric accent when non-zero. There is **no always-on score note** — the rationale
   lives only in the tooltips.
5. **Table of contents** — see §4.
6. **THE READING** — the five reading layers (§3).
7. **BEHIND THE TEXT** — the reference fields, in template order.
8. **Apparatus** — sources, confidence, status, version/date.
## 2 · Design tokens (do not improvise per story)

- **Theme:** dark. Ground `#0f1117`, panels `#161a22`, rules `#242935`. Ink
  `#e7e9ef`; brighter `#f5f6fa`; soft/muted/faint greys step down from there.
- **Accent (rubric):** `#c25a4d` — used only for the field-marker ticks (the `<h3>`
  left border), the non-zero Harm value, active-section markers, and focus rings.
  **Orange / terracotta is never the main colour.**
- **Type:** EB Garamond (serif) for all reading — body and every heading; Source Sans
  3 (sans) for apparatus / chrome only (eyebrow, data strip, score, TOC, code,
  ed-notes). Body 13pt, line-height ~1.62, measure capped at `56rem`. Italics are
  reserved for titles and transliterated terms, not for emphasis runs.
- **Fonts are embedded, subset to the glyphs the page uses, and WOFF2-compressed** —
  a full page is ~150–165 KB, self-contained and offline-capable. Never link out to
  a web font or ship full TTFs.
## 3 · The Reading — five layers

The renderer expects these `### ` headings, in order, inside `## THE READING`:

1. **`1 · The text`** — one clear translation made directly from the original
   language, kept close to the wording. An opening italic one-liner becomes the lead
   note. (Editorial translation; never paste an in-copyright version.)
2. **`2 · How the translations differ — and what's at stake`** — the cruxes: where
   the famous wordings part company and why it matters (KJV / ASV / WEB and the
   ancient witnesses). This replaces a second parallel translation. Coordinate with
   *Text & Composition* so the two don't duplicate.
3. **`3 · … retelling`** — the plain-English retelling. Italic runs inside this layer
   render as the muted "divine-voice" treatment.
4. **`4 · What it means`** — the accessible interpretation.
5. **`5 · Why this matters`** — the newcomer's payoff.
## 4 · Navigation & interaction

- **Wide screens (≥1220px):** a fixed left-gutter section nav with scroll-spy (the
  current section is marked with the rubric tick), filling space that would otherwise
  be empty margin.
- **Narrower screens (<1220px):** the gutter nav is hidden and a collapsible
  disclosure labelled **"Click here to see the table of contents"** appears below the
  header — styled as an obvious button, collapsed by default, grouped into THE READING
  and BEHIND THE TEXT, auto-closing after a jump.
- **Score tooltips:** hover on desktop, tap on mobile (tap-away dismisses); the popup
  is anchored below the score bar and width-capped so it never overflows a phone.
- Smooth in-page scrolling; section anchors have scroll-margin so headings aren't
  hidden under the top edge.
## 5 · Accessibility & performance floor (every page, non-negotiable)

- No horizontal overflow from 320px up; `text-size-adjust` pinned so iOS can't inflate
  the layout; `overflow-wrap` so long tokens can't force a scroll.
- Pinch-zoom left enabled; visible keyboard focus (`:focus-visible`); `prefers-
  reduced-motion` respected (transitions and smooth-scroll disabled).
- Semantic `<main><article>`; meaning never carried by colour alone.
- Any explanatory graphic added by #18 carries a text alternative (and, for charts, a
  readable data fallback); motion never hides information a still can't recover.
- Self-contained: no network at view time; target ~150–165 KB per page.
## 6 · Authoring contract (what the entry markdown must provide)

The renderer is structure-driven, so an entry only renders correctly if it follows
`03-story-entry-template.md`:

- First line `# Title — subtitle`; metadata as `**Key:** value` lines; then `---`;
  then the body.
- **Score line:** `**Score (R0):** \`I# · C# · P# · H# · A#\` *(clause; clause;
  clause; clause; clause.)*` — exactly five `;`-separated clauses, in `I·C·P·H·A`
  order, each becoming one axis's "This entry" rationale.
- The reading-layer and Behind-the-Text headings spelled as in the template (the
  renderer keys the divine-voice treatment off a `### …retelling` heading and builds
  the score tooltips off the axis letters).
- Markdown conventions the renderer styles: a whole-italic `*(parenthetical)*`
  paragraph → ed-note; a whole-italic `*lead*` paragraph → aside/lead note; inline
  `*(gloss)*` → muted gloss; `**bold**` → bright. Keep these in mind when writing.
  If a new entry needs a structural change (a new field, a different layer), change the
  template **and** the renderer together, re-render the worked example to confirm it
  still matches, and note it here — so the whole corpus moves as one.

**Status:** locked · **Version / date:** v1.0 — 2026-06-17
