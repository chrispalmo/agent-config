# Project type variants

Used by `project-bootstrap` to pick the right scaffolding set.

## Detection signals

| Signals                                 | Variant               |
| --------------------------------------- | --------------------- |
| Empty repo or idea only                 | greenfield            |
| `backlog/`, `audit-`, client contracts  | consulting            |
| Multiple git subrepos, workspace README | container             |
| `PLAN.md`, content pipeline, scoring    | meta                  |
| README says frozen/minimal              | minimal — README only |

---

## Greenfield product (default)

Full stack:

```
project/
├── README.md
├── VISION.md
├── IMPLEMENTATION_PLAN.md
├── IMPLEMENTATION_STATUS.md    ← MANDATORY
├── AGENTS.md                   ← canonical startup + session handoff
└── CLAUDE.md                   ← imports AGENTS.md for Claude Code
```

Add as needed: `docs/`, `TESTING_STRATEGY.md`, domain specs.

Do not bootstrap `EXPLORATION_BACKLOG.md`. If asked to park a speculative item,
`status-ledger` creates it in the existing project and wires its conditional
handoff guidance into `AGENTS.md`.

---

## Consulting / engagement

```
engagement/
├── README.md
├── AGENTS.md
├── audit-charter.md          # replaces VISION
├── audit-status.md           # replaces IMPLEMENTATION_STATUS
├── backlog/items.jsonl       # machine-readable work queue
├── evidence/                 # dated snapshots
└── CLAUDE.md                 # imports AGENTS.md for Claude Code
```

---

## Workspace container (multi-repo)

```
container/
├── README.md                 # layout, nested-git rules
├── AGENTS.md                 # startup checklist, cross-repo sync
├── CLAUDE.md                 # imports AGENTS.md for Claude Code
└── .vscode/settings.json     # git.autoRepositoryDetection: subFolders
```

Child repos get their own PM stack. Container does NOT track child code.

---

## Real-world deadline workflow

Add to greenfield stack:

```
state/handoff.md              # session handoff
log/session-log.md            # append-only session log
```

---

## Meta / content pipeline

```
meta-project/
├── README.md
├── PLAN.md                   # can serve PLAN + partial STATUS
├── FRAMEWORK-LOG.md          # process iteration log
├── AGENTS.md                 # startup + documentation authority
└── CLAUDE.md                 # imports AGENTS.md for Claude Code
```

Optional: project-local Agent Skills under a vendor skill directory if the team
uses them (not required for the PM stack).

---

## Minimal / frozen

```
project/
└── README.md                 # explicit "frozen" or "minimal" note
```

---

## Completed tool / utility

If the tool is complete and has no ongoing work, classify it **Skip** in
`project-audit`:

```
tool/
├── README.md                 # usage + phase completion table
└── docs/IMPLEMENTATION-PLAN.md
```

If ongoing maintenance is expected, add lightweight
`IMPLEMENTATION_STATUS.md`, `AGENTS.md`, and the `CLAUDE.md` import shim, then
apply the standard rubric.

---

## What NOT to include by default

- Vendor-only rule trees as required artifacts
- Formal ADR directories
- Memory Bank 6-file structure
- docflow CONVENTIONS + audit CI
- Separate ROADMAP.md (merge into PLAN)

Optional ADRs only when: regulated compliance, multi-agent team, or decisions need formal acceptance criteria.
