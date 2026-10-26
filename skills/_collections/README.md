# Skill collections

Collections group two or more related skills for human browsing and package installation. Every collection has an overview and member skill folders matching its package membership. A sole remaining skill returns to `skills/<name>/`, and the obsolete collection overview, package, and empty directories are removed. Installed skill names and invocation policies do not change with source organization.

| Collection | Purpose | Members |
| --- | --- | --- |
| [browser](browser/README.md) | Manage agent-created browser tabs and their cleanup. | browser-session, browser-cleanup |
| [coordination](coordination/README.md) | Organize ideas, propose and assign work, operate opted-in workers, and hold requested reviews. | triage, propose-tasks, delegate, harness, pause-for-review |
| [design](design/README.md) | Compare interface proposals and apply a selected visual style. | design-tool, neon-neo-brutalist-minimal |
| [project-management](project-management/README.md) | Audit, establish, and maintain project continuity. | project-audit, project-bootstrap, status-ledger |

Install a complete collection from the repository root:

```bash
./scripts/install.sh --skills --package coordination --cursor --claude --agents
```

The [skill catalog](../skills.manifest) and [package catalog](../packages.manifest) remain authoritative for availability and membership. Collection membership does not automatically activate a skill or grant authority to act.
