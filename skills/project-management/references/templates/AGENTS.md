# Agent guide — [project name]

Canonical shared instructions for coding agents. Cursor, Codex, and other
AGENTS.md-compatible tools load this file directly; Claude Code loads it through
the `CLAUDE.md` import shim.

## Startup checklist

1. Read `IMPLEMENTATION_STATUS.md` first — **Current focus**, **Next work item**, blockers
2. Skim `VISION.md` if scope is unclear
3. Use `IMPLEMENTATION_PLAN.md` for phase deliverables
4. [Project-specific: read domain docs, run tests, etc.]

## Documentation authority

| Question | Source of truth |
|----------|-----------------|
| What are we building? | `VISION.md` |
| What's the roadmap? | `IMPLEMENTATION_PLAN.md` |
| What's done/blocked/next? | `IMPLEMENTATION_STATUS.md` |
| Why was X decided? | `IMPLEMENTATION_STATUS.md` decision log |

## Session workflow

### At session start

1. Read `IMPLEMENTATION_STATUS.md` — **Current focus**, **Next work item**, blockers, deviations
2. Skim `VISION.md` if scope unclear
3. Do not redo `done` items unless evidence is invalid

### Before ending session

After authorized work changes execution state, evidence, decisions, risks, or
the next action, update `IMPLEMENTATION_STATUS.md`:

| Section | Action |
| ------- | ------ |
| Header | Refresh **Last reviewed**, **Current focus**, **Next work item** |
| Phase checklist | Set status + **Evidence** (paths, commands, commit SHAs) |
| Phase gates | Update when kill-criterion evidence exists |
| Decision log | Add dated decisions with docs touched |
| Deviations | Record plan changes |
| Metrics snapshot | Fill after measured runs |
| Open risks | Add new blockers |

If blocked without code changes, set row to `blocked` with named **Blocker / next action**.

Do not edit STATUS after read-only questions, reviews, or audits that discover
no durable project change.

Prefer the **status-ledger** skill for ledger maintenance when available.

## Build / test commands

```bash
# [Add project-specific commands]
```

## Safety

- [Project-specific constraints: no prod deploys, no secrets in commits, etc.]
