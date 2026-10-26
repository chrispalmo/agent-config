# Continuity modes

Choose structure by the work and existing project practice. Adequate existing stores take precedence over these examples; filenames are suggestions.

| Mode | When useful | Structure |
| --- | --- | --- |
| Minimal | Small tools, maintenance, short tasks, frozen projects | Reuse usage/scope documentation and shared agent guidance. Add a short next-action note only when work must resume; use the existing tracker or note for work state. |
| Markdown | Sustained work with modest dependencies | One compact work record for current work, blockers, evidence, decisions, and next action. Split scope or design into a separate document only when it improves review. |

## Adaptation

A consulting engagement can keep its existing charter, evidence index, question board, and work queue. A workspace container needs layout and cross-repository guidance; child repositories keep their own authorities. A content pipeline can use its existing editorial plan. A deadline project may need a short handoff, but not a second independent status ledger. A completed tool needs no invented backlog.

## Documentation location

Prefer `docs/` for substantial new Markdown project records, scoped to the area they govern. Root `docs/` holds project-wide direction, architecture, operating guidance, and overall work state when Markdown is the chosen store. Substantial areas may keep local `docs/` beside their source for records specific to that area. Create these folders only when useful records need them.

Give each document one canonical home. Root or local indexes link to that home rather than duplicating its contents. Keep shared AGENTS.md at the relevant directory root and its one-line CLAUDE.md import beside it; link to canonical records using their actual paths or URLs.

This is a placement preference, not a prerequisite for continuity. Preserve adequate existing arrangements, including root-level notes and external trackers, and follow explicit user direction. Do not migrate records solely to conform, seed empty folders, require a multi-file management stack, or create a competing task store.

## Canonical roles

Name where scope, executable work, decisions, and evidence live in AGENTS.md. One artifact may serve several roles. Plans can explain phases or architecture while task state lives elsewhere; derived summaries should link to their source and must not become another manually maintained queue.

Do not add a roadmap, research folder, formal decision directory, or exploration backlog solely to satisfy a template. Keep vendor-specific shared guidance in AGENTS.md and the Claude compatibility file as an import.
