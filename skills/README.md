# skills

Agent Skills (`SKILL.md`) for Cursor, Claude Code, and OpenAI Codex.

This directory is the skills half of `chrispalmo/agent-config`. The root `scripts/install.sh` installs these skills and the sibling `rules/` by default.

## Layout

```text
skills/
├── skills.manifest
├── packages.manifest
├── bundled-skills.manifest
├── project-management/
├── interview/
├── design-tool/
├── github-init/
├── pause-for-review/
├── plaintext/
└── proofread/
```

Independent skills live directly under `skills/`. Folders that group multiple skills are packages, not categories.

## Install

From the repository root:

```bash
./scripts/install.sh
./scripts/install.sh --cursor --claude --agents
./scripts/install.sh --skills --package project-management
```

Default install writes skills to `~/.codex/skills` and `~/.claude/skills`. Use `--cursor` when Cursor's native `~/.cursor/skills` root is required, including Cursor cloud VMs.
