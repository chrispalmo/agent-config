# Skills

Canonical Agent Skills for Cursor, Claude Code, and OpenAI Codex. [The catalog](skills.manifest) defines installed skills and [the package catalog](packages.manifest) defines cross-linked groups.

Independent skills live directly under `skills/`. All [collections](_collections/README.md) live under `skills/_collections/<collection>/`, with each member in its own skill folder. Collections are installed using the existing `--package` option. Supporting references, assets, scripts, and agent metadata live inside the owning skill and are installed with it. Shared repository scripts remain under scripts/ at the repository root.

## Install

From the repository root:

```bash
./scripts/install.sh
./scripts/install.sh --cursor --claude --agents
./scripts/install.sh --skills --package project-management
```

The default installs skills for all three harnesses. Codex and Cursor share `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Native rules retain their separate harness roots. Explicit `CODEX_SKILLS`, `CURSOR_SKILLS`, and `CLAUDE_SKILLS` overrides are supported. A full reinstall removes retired skills only when their ownership identifies this repository; unrelated skills are preserved. Package installs preserve managed skills outside the selected package.

See [design workflows](_collections/design/README.md), [coordination workflows](_collections/coordination/README.md), [project continuity](_collections/project-management/README.md), and the standalone [interview skill](interview/SKILL.md).

Pending-review skills live under `drafts/`, outside the install catalog. Reviewed skills must be promoted into the catalog before installation.
