---
name: project-bootstrap
description: >-
  Scaffolds the agent continuity stack (VISION, IMPLEMENTATION_PLAN,
  IMPLEMENTATION_STATUS, AGENTS.md, and a Claude Code compatibility shim) on
  new or under-documented repos. Detects project type (greenfield, consulting,
  container, meta, minimal). Use when starting a new project, retrofitting PM
  docs, or when the user asks to bootstrap or scaffold project management files.
---

# Project Bootstrap

Scaffold the agent continuity stack from
`skills/project-management/references/templates/` in this skills repository
(resolve via the real path of this skill's `SKILL.md`).

Keep shared guidance in `AGENTS.md`. Cursor, Codex, and other compatible agents
load it directly. Claude Code does not, so create a one-line `CLAUDE.md` import
shim rather than duplicating instructions. Do not create vendor rule trees (for
example `.cursor/rules/`) unless the user explicitly asks.

## Quick start

1. Run `project-audit` first (or inline detect)
2. Pick variant: greenfield (default) | consulting | container | meta | minimal
3. Copy templates; customize placeholders
4. Backfill STATUS from existing docs
5. Set fresh-agent one-liner

## Project type detection

See `skills/project-management/references/variants.md` for the full variant guide.

| Signals                                 | Variant               |
| --------------------------------------- | --------------------- |
| Empty repo or idea only                 | greenfield            |
| `backlog/`, `audit-`, client contracts  | consulting            |
| Multiple git subrepos, workspace README | container             |
| `PLAN.md`, content pipeline, scoring    | meta                  |
| README says frozen/minimal              | minimal — README only |

## Files to create (greenfield)

```
VISION.md
IMPLEMENTATION_PLAN.md
IMPLEMENTATION_STATUS.md    # ALWAYS — mandatory
AGENTS.md                   # canonical startup + session handoff
CLAUDE.md                   # contains only: @AGENTS.md
```

Do **not** create or reference `EXPLORATION_BACKLOG.md` during bootstrap. The `status-ledger` skill adds and wires it into an existing project only when asked to park the first speculative item.

Templates: `skills/project-management/references/templates/`

## Backfill rules

- Existing README → extract into VISION problem/goal
- Existing PLAN → migrate to IMPLEMENTATION_PLAN.md
- Chat context → seed STATUS checklist + decision log
- Existing vendor rules (`.cursor/rules/`, etc.) → fold shared substance into
  `AGENTS.md`; identify obsolete duplicates, but remove them only with explicit
  user approval
- Existing `CLAUDE.md` → preserve Claude-specific instructions and add
  `@AGENTS.md` if it is not already imported
- Never delete existing docs without approval

## STATUS mandatory sections

1. Header (date, phase, focus, next item, fresh-agent one-liner)
2. Status vocabulary
3. Phase gates
4. Phase checklist with evidence column
5. Decision log
6. Deviations
7. Handoff checklist

## Variants

**Consulting:** `audit-charter.md`, `audit-status.md`, `backlog/items.jsonl`  
**Container:** README + AGENTS.md + `.vscode/settings.json` nested git  
**Minimal:** README with explicit scope note only

## After bootstrap

Tell user to invoke `status-ledger` skill every session.

## Reference

- Templates: `skills/project-management/references/templates/README.md`
- Variants: `skills/project-management/references/variants.md`
