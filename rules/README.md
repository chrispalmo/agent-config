# rules

Personal Agent Rules for Cursor, Claude Code, and OpenAI Codex.

Canonical files are vendor-neutral `RULE.md` files. The root installer generates per-agent views:

| Agent | Generated path |
| --- | --- |
| Cursor | `~/.cursor/rules/<name>.mdc` |
| Claude Code | `~/.claude/rules/<name>.md` and `~/.claude/CLAUDE.md` |
| OpenAI Codex | `~/.codex/AGENTS.md` |

Add each rule directory to `rules.manifest`. Every `RULE.md` must set `alwaysApply: true` or `globs` in frontmatter.
