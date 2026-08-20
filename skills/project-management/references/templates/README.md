# Project management templates

Scaffolding templates for `project-bootstrap`. Copy to new project roots.

## Standard stack (greenfield solo + agents)

```
project/
├── README.md
├── VISION.md
├── IMPLEMENTATION_PLAN.md
├── IMPLEMENTATION_STATUS.md    ← MANDATORY
├── AGENTS.md                   ← canonical startup + session handoff
└── CLAUDE.md                   ← imports AGENTS.md for Claude Code
```

Templates in this directory:

- `VISION.md`
- `IMPLEMENTATION_PLAN.md`
- `IMPLEMENTATION_STATUS.md`
- `AGENTS.md`
- `CLAUDE.md`

Do **not** scaffold vendor-specific rule directories (for example `.cursor/rules/`)
by default. Put always-on guidance in `AGENTS.md` so Cursor, Claude Code, and
Codex share one source of truth. Claude Code does not load `AGENTS.md`
natively, so its checked-in `CLAUDE.md` shim contains only `@AGENTS.md`.

`EXPLORATION_BACKLOG.md` is an on-demand template, not part of the standard
stack. `status-ledger` copies it into an existing project and wires the handoff
guidance only when asked to park the first item.

## Variants

See `../variants.md` for consulting, container, meta, minimal, and tool variants.

## Mandatory artifact: IMPLEMENTATION_STATUS.md

Minimum sections:

1. Header (last reviewed, phase, focus, next item, fresh-agent one-liner)
2. Status vocabulary
3. Phase gates table
4. Phase checklist with evidence column
5. Decision log
6. Deviations from plan
7. Agent handoff checklist

Optional: metrics snapshot, verification log, open risks, repo state table.

## Conformance scoring

Use `../audit-rubric.md` to score projects:

- **Full** ≥85% — agent-ready
- **Partial** 60–84% — retrofit recommended
- **Minimal** <60% — agent will struggle

## What NOT to include by default

- Vendor-only agent rule trees (`.cursor/rules/`, etc.) as required artifacts
- Formal ADR directories
- Memory Bank 6-file structure
- docflow CONVENTIONS + audit CI
- Separate ROADMAP.md (merge into PLAN)
