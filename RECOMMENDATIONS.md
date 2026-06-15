# Claude Code tooling recommendations for this project

What's worth adding, grouped by type. The custom subagents, skills, and commands in
this repo are already the core of it; this is what complements them.

## Custom — already in this repo (the "ones I made for you")

These ship in the scaffold; no install step, they load when you run `claude` here.

- **13 subagents** (`.claude/agents/`) — your expert panel as real subagents, each
  with its own context, tools, and model. Drafters (narrative-writer, comparative-
  religion, harm-historian) run on Opus; reviewers/researchers on Sonnet; the
  read-only auditor (standards-integrity) stays tool-restricted.
- **6 commands** (`.claude/commands/`) — `/new-entry`, `/draft-entry`,
  `/review-entry`, `/score-unit`, `/validate`, `/sync-check`.
- **3 skills** (`.claude/skills/`) — entry-validator, copyright-guard,
  score-consistency, each wrapping a deterministic script and auto-triggering by
  description.
- **1 hook** (`.claude/settings.json`) — a non-blocking copyright scan on entry writes.

Tweak any of them by editing the Markdown/JSON; restart `claude` to reload subagents.

## Built-in Claude Code features to lean on

- **Agent Skills.** Beyond the three custom ones, Claude Code's document skills are
  useful at export time — e.g. turning a locked entry into a Word doc or PDF for a
  reader edition. Ask Claude Code to "export this entry as a PDF" and it will reach
  for the right skill.
- **Built-in subagents.** Claude Code ships general agents (exploration, docs lookup)
  that are always available; your custom panel sits alongside them. Run `/agents` to
  see the full library and manage them.
- **Plan mode & checkpoints.** Use plan mode for a multi-entry batch, and the rewind
  (Esc-Esc) to undo a bad drafting pass without losing the rest.
- **`/context`** to watch token budget when you dispatch several subagents at once
  (up to ~10 can run in parallel).

## MCP servers worth connecting

Add with `claude mcp add ...`. Pick by need:

- **Scripture text (public-domain).** The single highest-value add. You need WEB/KJV/
  ASV text on tap without pasting copyrighted translations. A scripture-lookup MCP, or
  simply Claude Code's built-in **WebFetch** pointed at a public-domain API such as
  `bible-api.com` (serves the World English Bible and KJV), gives the translation-
  languages subagent clean source text. Keep the in-copyright rule in mind: fetch only
  WEB/KJV/ASV.
- **GitHub** (`@modelcontextprotocol/server-github`) — version the corpus, open issues
  per book, track entry status in PRs. Natural fit for ~1,000 growing files.
- **Google Drive** — if your Claude.ai project keeps source PDFs/notes in Drive,
  the Drive MCP lets Claude Code read them directly.
- **A reference manager (Zotero or similar)** — if you want "Sources & further reading"
  to pull from a managed bibliography rather than free text.

Don't bother with the dev-centric MCP/plugins (database, CI, secrets scanners) — this
isn't a code project.

## Plugins

Most marketplace plugins target software teams, so few apply directly. Two moves that do:

1. **Browse the official marketplace** with `/plugin` (catalog:
   `anthropics/claude-plugins-official`). A zero-config **markdown formatter** hook is
   the one general-purpose pick worth having — it keeps entries tidy on save.
2. **Package *this* repo's suite as a plugin** so you can reuse it across machines or
   share it. Plugins bundle commands + agents + skills + hooks behind one install. The
   structure differs slightly from a project (dirs sit at the plugin root, not under
   `.claude/`, and only `plugin.json` goes in `.claude-plugin/`):

```text
bible-companion-plugin/
├── .claude-plugin/
│   └── plugin.json          # manifest ONLY
├── agents/                  # copy from .claude/agents/
├── commands/                # copy from .claude/commands/
├── skills/                  # copy from .claude/skills/
├── hooks/
│   └── hooks.json           # the "hooks" object from .claude/settings.json
└── scripts/                 # the checkers
```

`plugin.json`:

```json
{
  "name": "bible-companion",
  "description": "Drafting, scoring, review, and validation tools for the Bible-companion project: a 13-persona panel, entry workflows, and structure/copyright/score checks.",
  "version": "0.1.0",
  "author": { "name": "Your Name" },
  "license": "MIT"
}
```

Then add it to a marketplace (a Git repo with `.claude-plugin/marketplace.json`) and
install with `/plugin install bible-companion@your-marketplace`, or load a local dir
directly. Official guide: https://code.claude.com/docs/en/plugins

## Quick reference — docs

- Subagents: https://code.claude.com/docs/en/sub-agents
- Slash commands & skills: https://docs.claude.com/en/docs/claude-code/overview
- Hooks: search "Claude Code hooks" in the docs map
- Plugins: https://code.claude.com/docs/en/plugins
