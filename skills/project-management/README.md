# Project management skills

Four complementary Agent Skills for AI-assisted solo development.

## Skills

| Skill                                           | Purpose                                    | When                         |
| ----------------------------------------------- | ------------------------------------------ | ---------------------------- |
| [project-bootstrap](project-bootstrap/SKILL.md) | Scaffold VISION/PLAN/STATUS/AGENTS         | New project or retrofit      |
| [status-ledger](status-ledger/SKILL.md)         | Maintain IMPLEMENTATION_STATUS.md          | Every work session           |
| [project-audit](project-audit/SKILL.md)         | Score repo maturity, list gaps             | Before bootstrap or retrofit |
| [ingest](ingest/SKILL.md)                       | Reconcile dumps into durable project state | New information or documents |

## Workflow

```text
project-audit  →  project-bootstrap
   assess            scaffold
                         ↓
                ingest ↔ status-ledger
                reconcile    maintain
```

## References

| File                                          | Used by           |
| --------------------------------------------- | ----------------- |
| [templates/](references/templates/)           | project-bootstrap |
| [audit-rubric.md](references/audit-rubric.md) | project-audit     |
| [variants.md](references/variants.md)         | project-bootstrap |

## Core pattern

| File                       | Role                                            |
| -------------------------- | ----------------------------------------------- |
| `VISION.md`                | Scope filter, non-goals                         |
| `IMPLEMENTATION_PLAN.md`   | Phased roadmap                                  |
| `IMPLEMENTATION_STATUS.md` | **Living ledger** — status, evidence, decisions |
| `AGENTS.md`                | Canonical agent onboarding and session handoff  |
| `CLAUDE.md`                | One-line Claude Code import of `AGENTS.md`      |

`IMPLEMENTATION_STATUS.md` is mandatory. Everything else is project-type
dependent. Keep shared guidance in `AGENTS.md`; use the `CLAUDE.md` import shim
because Claude Code does not load `AGENTS.md` natively. Do not duplicate shared
instructions in vendor rule trees. `EXPLORATION_BACKLOG.md` is not bootstrapped;
`status-ledger` creates and wires it into an existing project only when asked to
park the first item.
