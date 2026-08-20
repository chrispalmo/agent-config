---
name: status-ledger
description: >-
  Creates and maintains IMPLEMENTATION_STATUS.md as the durable execution
  ledger — tracking progress, evidence, decisions, scope deviations, metrics,
  and session handoff. Use at session start and end, when updating project
  status, recording decisions, or when the user asks about implementation
  progress or what to work on next.
---

# Status Ledger

`IMPLEMENTATION_STATUS.md` is repo-owned memory. Chat is scratch paper.

## Session start

1. Read STATUS header: **Last reviewed**, **Current phase**, **Current focus**, **Next work item**
2. Read fresh-agent one-liner
3. Check deviations + open blockers
4. Do not redo `done` rows unless evidence invalid

## During work

- Advance one checklist ID at a time (P0-001, P1-003, etc.)
- Set `done` only with evidence: file paths, command output, commit SHA
- Record product/architecture decisions in **Decision log** immediately
- Record plan changes in **Deviations from implementation plan**
- If the user asks to park a speculative idea, follow **First-use activation** below,
  then append it quietly — do not discuss the icebox otherwise

## Exploration backlog (first-use activation)

Do not create or wire `EXPLORATION_BACKLOG.md` during project bootstrap.

Only when the user asks to add or park the first speculative item:

1. Create `EXPLORATION_BACKLOG.md` from
   `skills/project-management/references/templates/EXPLORATION_BACKLOG.md`
   in this skills repository (resolve via the real path of this skill's `SKILL.md`).
2. Wire handoff guidance in `AGENTS.md`: add a short note that the backlog is
   non-canonical and surfaced only on an explicit status review or project
   closeout.
3. Append the requested item.

Check the file and guidance independently:

- If the backlog is missing, create it.
- If the `AGENTS.md` guidance is missing, add it.
- Append the item without duplicating either artifact.

## Exploration backlog (when to surface)

Do **not** mention `EXPLORATION_BACKLOG.md` at session start, during normal implementation, or when planning next work.

Bring it up only when:

1. **Status check** — the user asks for progress/status, or you run an explicit STATUS review
2. **Project closeout** — wrapping the project or a major phase; ask what to do with parked ideas (promote to PLAN,keep, or delete)

## Session end

After authorized work changes execution state, evidence, decisions, risks, or
the next action, update the affected sections:

| Section      | Action                            |
| ------------ | --------------------------------- |
| Header       | Date, focus, next item, one-liner |
| Checklist    | Status + evidence column          |
| Gates        | When kill criteria measured       |
| Decision log | Dated rows with docs updated      |
| Deviations   | If scope diverged from PLAN       |
| Metrics      | If numbers changed                |
| Verification | Commands run                      |
| Risks        | New blockers                      |

Do not edit STATUS after read-only questions, reviews, or audits that discover
no durable project change.

## Status vocabulary

`not_started` | `in_progress` | `blocked` | `done` | `deferred` | `cancelled`

## Decision log format

```markdown
| Date | Decision | Reason | Docs updated |
| 2026-07-09 | Use X over Y | [why] | VISION.md, STATUS |
```

## If STATUS missing

Invoke `project-bootstrap` first, or create from
`skills/project-management/references/templates/IMPLEMENTATION_STATUS.md` in this skills repository.

## Enforced by

The target project's canonical `AGENTS.md` session workflow. Claude Code reaches
the same instructions through the project's `CLAUDE.md` import shim. Use the
**status-ledger** skill for the full procedure.
