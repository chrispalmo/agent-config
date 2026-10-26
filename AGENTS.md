# Agent guide — agent-config

Central repository of Agent Skills and Agent Rules for Cursor, Claude Code, and OpenAI Codex.

## Startup checklist

1. Read `README.md` for layout and install behavior.
2. Read this file for operating procedures.
3. Pending-review drafts live under `drafts/` and are excluded from installation. Skills live in `skills/<name>/SKILL.md` or `skills/_collections/<collection>/<name>/SKILL.md`.
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
| Guidance maintenance | `docs/maintenance.md` |
| Instruction and workflow audit findings | `docs/audits/2026-10-07-instruction-and-workflow-audit.md` |

## Complete maintenance changes

Own the consequences of the requested change. Finish when the affected source, catalogs, package layout, active references, tests, and authorized installed copies agree. Infer routine consistency repairs from the request; the user should not need to enumerate follow-on cleanup. Follow `docs/maintenance.md` for the maintenance procedure and verification commands.

Follow the existing layout when adding or moving artifacts. Collections group at least two related skills under `skills/_collections/<collection>/<skill>/`, with matching package membership. When only one remains, move it to `skills/<name>/` and remove the obsolete package, overview, and empty directories. Inspect the filesystem as well as Git: empty directories are not tracked. Preserve intentional fixtures and unrelated content.

Resolve the current authoritative source and accepted decisions before copying or revising guidance or assets. Inspect existing changes before editing, and re-read shared records before updating them so concurrent work is preserved. Historical reports describe their dated state; they do not override current sources or grant new authority.

Carry forward installation and publication authorization within the current task. Scope writes to the authorized work. Completion reports must distinguish source changes, installation, validation, and publication, and name relevant remaining changes or blockers. Passing tests or syncing one commit does not establish that the whole repository is clean or synced.

## Cross-agent compatibility

Keep shared instructions vendor-neutral. If an agent requires different output, implement that in `scripts/install.sh` rather than duplicating source content.

When setting up project agent guidance in any repository, put shared guidance in `AGENTS.md` and create `CLAUDE.md` containing only `@AGENTS.md`.

## Guidance maintenance

When changing guidance, preserve the user's established preferences and correct demonstrated gaps with the smallest useful change. Keep procedures in `docs/maintenance.md` rather than duplicating them here. Static checks do not establish behavioral improvements.

Audit findings and proposals are evidence, not standalone instructions. Adopted changes live in the canonical skills and rules; the audit report holds their evidence and closeout. Harness compatibility and the broad installer audit remain deferred until the next harness switch; behavioral evaluations remain deferred until requested. The current audit work store remains the report.

## Safety

- No client secrets, private nicknames, or non-publishable material in skills or rules.
- Do not update git config.
- Do not push or archive repositories unless the user explicitly asks.
- Installer must abort on foreign clashes; never overwrite unmanaged destinations.
