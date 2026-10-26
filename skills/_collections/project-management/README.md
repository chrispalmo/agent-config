# Project continuity skills

Use the smallest structure that lets authorized work resume with clear scope, evidence, and one work-state authority. Existing documents and trackers are valid equivalents; no filename, multi-file stack, or task backend is mandatory.

| Skill | Purpose | When useful |
| --- | --- | --- |
| [project-audit](project-audit/SKILL.md) | Inspect continuity using concrete evidence | A requested project review or demonstrated confusion |
| [project-bootstrap](project-bootstrap/SKILL.md) | Fill missing guidance or durable-state structure | A requested new-project setup or retrofit |
| [status-ledger](status-ledger/SKILL.md) | Update the chosen work authority and handoff | Authorized work changes durable project state |

Audit and bootstrap are optional workflows. Normal maintenance does not require the human to invoke a skill every session.

## Resources and modes

[Assessment criteria](project-audit/references/audit-rubric.md) define the continuity review. [The mode guide](project-bootstrap/references/variants.md) covers minimal guidance and compact Markdown continuity. [Bootstrap templates](project-bootstrap/references/templates/README.md) are starting points; include only relevant sections.

Resources live with their owning skills and are copied into each installed skill. Shared project instructions belong in AGENTS.md, with CLAUDE.md containing only @AGENTS.md. Name the authority for scope, tasks, decisions, and evidence; a single artifact may serve several roles. Any summaries of task state should derive from that authority rather than competing with it.

For substantial new Markdown project records, prefer `docs/` scoped to the area they govern, while keeping agent entry points at the relevant directory root. The [location guidance](project-bootstrap/references/variants.md#documentation-location) covers project-wide and area-local placement; preserve adequate existing arrangements and external trackers.
