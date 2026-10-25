# agent-config

Central repository of Agent Skills and Agent Rules for Cursor, Claude Code, and OpenAI Codex.

This repo replaces the old standalone `chrispalmo/skills` repo as the source of truth. Skills and rules stay separate as artifacts, while install/uninstall/test scripts are shared.

## Layout

```text
agent-config/
├── scripts/
│   ├── common.sh
│   ├── install.sh
│   ├── uninstall.sh
│   ├── test-install.sh
│   └── cloud/
├── skills/
│   ├── skills.manifest
│   ├── packages.manifest
│   └── <skill>/SKILL.md
└── rules/
    ├── rules.manifest
    └── <rule>/RULE.md
```

## Install

```bash
./scripts/install.sh
```

Default install writes skills for Claude Code and Codex/Cursor, and rules for Claude Code and Codex. Cursor-native roots are opt-in. Skills include their supporting resources; full installs remove retired skills owned by this repository, while package installs preserve skills outside the package.

| Option | Effect |
| --- | --- |
| `--cursor` | Install Cursor-native skills and rules |
| `--claude` | Install Claude Code skills and rules |
| `--agents` / `--codex` | Install Codex skills and Codex rules |
| `--skills` | Install only skills |
| `--rules` | Install only rules |
| `--package <name>` | Install one complete skills package |

Common full install:

```bash
./scripts/install.sh --cursor --claude --agents
```

If you already installed the old `~/dev/skills` repo, run its uninstall script first so old skill symlinks do not block this installer:

```bash
~/dev/skills/scripts/uninstall.sh --all
~/dev/skills/scripts/uninstall.sh --cursor
./scripts/install.sh --cursor --claude --agents
```

## Cloud agents

Cloud agents do not see this machine. Follow the human setup guide in [scripts/cloud/README.md](scripts/cloud/README.md) (Cursor, Claude Code, and Codex, step by step).


## Coordinate work

The [coordination package](skills/coordination/README.md) groups triage, propose-tasks, delegate, and harness. They organize supplied ideas, propose next work, assign existing tasks, and optionally operate an explicitly chosen external native worker. Install together with `./scripts/install.sh --skills --package coordination --cursor --claude --agents`; the shared message and greeting rules use the separate normal rule installation flow.

## Search past chats

The [search-agent-chats skill](skills/search-agent-chats/SKILL.md) is installed across Cursor, Claude Code, and Codex. It provides read-only searches against the private archive when the archive's search script is available in its maintained checkout. Archive capture and search-index refresh remain separate: Cursor hooks capture locally, while Claude Code and Codex transcript capture and cloud/remote archive synchronization are not provided by this skill.


## Adding skills and rules

- Add skills under `skills/<name>/SKILL.md` and register them in `skills/skills.manifest`.
- Add cross-linked skill packages to `skills/packages.manifest`.
- Add rules under `rules/<name>/RULE.md` and register them in `rules/rules.manifest`.
- Keep shared project guidance in `AGENTS.md` and `CLAUDE.md` as a one-line `@AGENTS.md` shim.

## Maintenance

Follow the [maintenance guide](docs/maintenance.md) when changing guidance. Run `python3 scripts/check-content.py`, `./scripts/test-install.sh`, and `git diff --check` after source changes.

The [instruction and workflow audit](docs/audits/2026-10-07-instruction-and-workflow-audit.md) records the implemented simplifications, proofread retirement, optional Beads support, and closeout. Project continuity defaults to minimal guidance and can reuse a compact Markdown record or adopted Beads tracker. Harness compatibility and the broad installer audit remain deferred until the next harness switch; behavioral evaluations are also deferred.

## Safety

- No secrets or non-publishable preferences in skills or rules.
- Installers abort rather than overwrite unmanaged destinations.
- Generated rule files contain `<!-- managed-by: chrispalmo/agent-config -->`.
