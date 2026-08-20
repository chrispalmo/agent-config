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

Default install writes skills for Claude Code and Codex/Cursor, and rules for Claude Code and Codex. Cursor-native roots are opt-in.

| Option | Effect |
| --- | --- |
| `--cursor` | Install Cursor-native skills and rules |
| `--claude` | Install Claude Code skills and rules |
| `--agents` / `--codex` | Install Codex/Cursor shared skills and Codex rules |
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

Cloud agents do not see this machine. Paste this stub once into each vendor environment setup field after the public GitHub repo exists:

```bash
git clone --depth 1 https://github.com/chrispalmo/agent-config.git ~/.agent-config
exec ~/.agent-config/scripts/cloud/bootstrap.sh
```

## Adding skills and rules

- Add skills under `skills/<name>/SKILL.md` and register them in `skills/skills.manifest`.
- Add cross-linked skill packages to `skills/packages.manifest`.
- Add rules under `rules/<name>/RULE.md` and register them in `rules/rules.manifest`.
- Keep shared project guidance in `AGENTS.md` and `CLAUDE.md` as a one-line `@AGENTS.md` shim.

## Safety

- No secrets or non-publishable preferences in skills or rules.
- Installers abort rather than overwrite unmanaged destinations.
- Generated rule files contain `<!-- managed-by: chrispalmo/agent-config -->`.
