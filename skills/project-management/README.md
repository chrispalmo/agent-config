# Project continuity skills

Use the smallest structure that lets authorized work resume with clear scope, evidence, and one work-state authority. Existing documents and trackers are valid equivalents; no filename, multi-file stack, or task backend is mandatory.

| Skill | Purpose | When useful |
| --- | --- | --- |
| [project-audit](project-audit/SKILL.md) | Inspect continuity using concrete evidence | A requested project review or demonstrated confusion |
| [project-bootstrap](project-bootstrap/SKILL.md) | Fill missing guidance or durable-state structure | A requested new-project setup or retrofit |
| [status-ledger](status-ledger/SKILL.md) | Update the chosen work authority and handoff | Authorized work changes durable project state |
| [ingest](ingest/SKILL.md) | Reconcile inputs with existing project knowledge | The user supplies new information to incorporate |

Audit and bootstrap are optional workflows. Normal maintenance does not require the human to invoke a skill every session. Ingest works with an existing project store without requiring the rest of this suite.

## Resources and modes

[Assessment criteria](project-audit/references/audit-rubric.md) define the continuity review. [The mode guide](project-bootstrap/references/variants.md) covers minimal guidance, compact Markdown continuity, and optional Beads task tracking. [Bootstrap templates](project-bootstrap/references/templates/README.md) are starting points; include only relevant sections. [Beads guidance](status-ledger/references/beads.md) applies to existing Beads projects and requested adoption, not automatic backend selection.

Resources live with their owning skills and are copied into each installed skill. Shared project instructions belong in AGENTS.md, with CLAUDE.md containing only @AGENTS.md. Name the authority for scope, tasks, decisions, and evidence; a single artifact may serve several roles. Any summaries of task state should derive from that authority rather than competing with it.
