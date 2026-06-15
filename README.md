# Bible Companion — Claude Code companion project

A file-system-native workspace for producing the Bible-companion entries in Claude
Code, alongside (and reusing) your Claude.ai project. Claude Code adds what a chat
project can't: a real directory of entries, the 13 personas as **subagents**, the
production steps as **slash commands**, and **deterministic checkers** (structure,
copyright, score-consistency) wired into **skills** and a **hook** so quality gates
run automatically instead of from memory.

It's most useful once you're past calibration and producing many entries: batch
drafting, whole-corpus validation, and keeping ~1,000 score lines in sync with the
`R1` catalogue are exactly the jobs a chat window is bad at and a repo is good at.

## 1. Install Claude Code

The native installer is the current recommended path (npm is deprecated):

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash
# or Homebrew on macOS:
brew install --cask claude-code
```

Then authenticate: `claude` (it walks you through login on first run). Docs:
https://docs.claude.com/en/docs/claude-code/overview

## 2. Set up the repo

```bash
unzip bible-companion-cc.zip
cd bible-companion-cc
git init && git add -A && git commit -m "scaffold"   # optional but recommended
claude                                                # start Claude Code here
```

Then **add your corpus files** (copies from the Claude.ai project):

- Put `R0`–`R5` into `reference/` (see `reference/README.md` for exact names).
- Put any remaining entry-layer files (story index, expert-panel doc, registry)
  into `system/`. The template, style guide, operation guide, and the Cain-and-Abel
  worked example are already seeded.

Nothing else is required — the scaffold runs as-is. Verify with:

```bash
python3 scripts/validate_entry.py entries/cain-and-abel.md   # -> PASS
python3 scripts/check_copyright.py entries/                  # -> no markers
python3 scripts/check_scores.py                              # reads scores; needs R1 to cross-check
```

## 3. What's in the box

| Piece | Location | What it does |
|---|---|---|
| Project memory | `CLAUDE.md` | Auto-loaded orientation: the teaching-tool brief, the two layers, the five-axis score, the hard rules. The Claude Code analogue of your Instructions field. |
| Subagents (the panel) | `.claude/agents/*.md` | The 13 specialists — managing-editor, narrative-writer, translation-languages, historical-critical, ancient-world-historian, jewish/christian/comparative-religion, sociologist-belief, reception-culture, harm-historian, schism-historian, standards-integrity. Each has its own system prompt, tools, and model, and runs in its own context. |
| Commands (the workflow) | `.claude/commands/*.md` | `/new-entry`, `/draft-entry`, `/review-entry`, `/score-unit`, `/validate`, `/sync-check`. |
| Skills (auto-checks) | `.claude/skills/*/SKILL.md` | entry-validator, copyright-guard, score-consistency — wrap the scripts and auto-trigger by description. |
| Hook | `.claude/settings.json` | A non-blocking `PostToolUse` copyright scan whenever an entry is written/edited. |
| Scripts | `scripts/*.py` | The deterministic checkers (no LLM needed): `validate_entry.py`, `check_copyright.py`, `check_scores.py`. |

## 4. The workflow

```text
/new-entry "Genesis 22:1-19"     scaffold the file from the template
/draft-entry entries/gen-22-...  retelling first (narrative-writer), then the
                                 scoped specialists fill Behind-the-Text
/score-unit  entries/gen-22-...  assign I·C·P·H·A, one anchor per axis
/review-entry entries/gen-22-... panel review loop to convergence
/validate                        structure + copyright + R1 score sync
```

The managing-editor subagent scopes the panel at the start and makes the lock call
at the end. You stay in the loop — approve the plan, the score, and the lock.

A note on subagents: they're loaded at session start, so if you edit a file in
`.claude/agents/` mid-session, restart `claude` (or use `/agents`) to pick it up.

## 5. Verify the setup

Run the prompts in `TEST-PROMPTS.md` in a fresh Claude Code session — they confirm
the memory, subagents, commands, skills, hook, and scripts are all live.

## 6. Tooling recommendations

See `RECOMMENDATIONS.md` for which built-in/official/community Claude Code skills,
agents, plugins, and MCP servers are worth adding for this project — and how to
repackage this repo's custom skills/agents/commands as an installable plugin.

---
*Built to pair with the Claude.ai "Understanding the Bible" project. Same brief,
same rubric, same hard rules — different surface.*
