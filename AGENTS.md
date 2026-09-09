# Agent guide — agent-config

Central repository of Agent Skills and Agent Rules for Cursor, Claude Code, and OpenAI Codex.

## Startup checklist

1. Read `README.md` for layout and install behavior.
2. Read this file for operating procedures.
3. Skills live in `skills/<name>/SKILL.md` or `skills/<package>/<name>/SKILL.md`.
4. Rules live in `rules/<name>/RULE.md`.
5. Shared scripts live directly under `scripts/`; do not add `scripts/skills/` or `scripts/rules/` directories.

## Documentation authority

| Question | Source of truth |
| --- | --- |
| What skills exist? | `skills/skills.manifest` |
| What skills form a package? | `skills/packages.manifest` |
| What rules exist? | `rules/rules.manifest` |
| Local install | `scripts/install.sh` |
| Cloud VM install | `scripts/cloud/bootstrap.sh` |
| Cloud dashboard paste | `scripts/cloud/README.md` |

## Adding or removing a skill

1. Create or remove the skill directory under `skills/`.
2. Add or remove its path in `skills/skills.manifest`.
3. If it belongs to a cross-linked group, keep `skills/packages.manifest` in sync.
4. Run `./scripts/test-install.sh`.

## Adding or removing a rule

1. Create or remove `rules/<name>/RULE.md`.
2. Add or remove its path in `rules/rules.manifest`.
3. Set `alwaysApply: true` or `globs` in frontmatter.
4. Run `./scripts/test-install.sh`.

## Cross-agent compatibility

Keep shared instructions vendor-neutral. If an agent requires different output, implement that in `scripts/install.sh` rather than duplicating source content.

When setting up project agent guidance in any repository, put shared guidance in `AGENTS.md` and create `CLAUDE.md` containing only `@AGENTS.md`.

## Safety

- No client secrets, private nicknames, or non-publishable material in skills or rules.
- Do not update git config.
- Do not push or archive repositories unless the user explicitly asks.
- Installer must abort on foreign clashes; never overwrite unmanaged destinations.
