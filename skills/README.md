# Skills

Canonical Agent Skills for Cursor, Claude Code, and OpenAI Codex. [The catalog](skills.manifest) defines installed skills and [the package catalog](packages.manifest) defines cross-linked groups.

Skills live directly under skills/ or in a package directory. Supporting references, assets, scripts, and agent metadata live inside the owning skill and are installed with it. Shared repository scripts remain under scripts/ at the repository root.

## Install

From the repository root:

```bash
./scripts/install.sh
./scripts/install.sh --cursor --claude --agents
./scripts/install.sh --skills --package project-management
```

The default installs skills for all three harnesses. Codex and Cursor share `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Native rules retain their separate harness roots. Explicit `CODEX_SKILLS`, `CURSOR_SKILLS`, and `CLAUDE_SKILLS` overrides are supported. A full reinstall removes retired skills only when their ownership identifies this repository; unrelated skills are preserved. Package installs preserve managed skills outside the selected package.

See [design workflows](design/README.md), [coordination workflows](coordination/README.md), [project continuity](project-management/README.md) and [interview workflows](interview/README.md).

Pending-review skills live under `drafts/`, outside the install catalog. Reviewed skills must be promoted into the catalog before installation.
