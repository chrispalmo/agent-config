---
name: status-ledger
description: Maintain the project's authoritative work state, completion evidence, decisions, and handoff after durable changes. Use the existing tracker, compact Markdown record, or adopted Beads backend without creating competing task stores.
---

# Status Ledger

Read the repository's authority guidance before choosing a store. Use its existing tracker or current-state note; IMPLEMENTATION_STATUS.md is an optional Markdown convention. If Beads is authoritative, read [Beads guidance](references/beads.md). Do not silently substitute another backend when the chosen store is unavailable.

## Start and update

Read current work, next action, blockers, and relevant decisions. The latest user instruction governs selection; an old next-item entry or a ready-work query does not authorize unrelated work. Do not repeat completed work unless new evidence or the request warrants it.

Update affected records when authorized work changes execution state, evidence, consequential decisions, scope, risks, or the next action. Independent items may advance together when authorized; ledger conventions do not require serial execution or grant delegation permission. Mark work complete only with relevant evidence and distinguish done, deferred, cancelled, and blocked outcomes.

Keep decisions with their reasons and sources in the named decision authority. Store validation beside the affected work, and link specifications or evidence rather than copying them into multiple records. Record only measured metrics. Do not refresh timestamps or tables for read-only exchanges without a durable change.

## Handoff

When work remains, leave a concrete next step, unresolved blockers, and enough file, command, or tracker references to resume. Carry existing user authorization and constraints forward; ask only for a missing consequential decision. Do not add a ledger solely to record a routine completion.

If no store exists and the work needs continuity, add the smallest current-state note to existing documentation or use the compact template supplied by project-bootstrap when that package is available. Do not automatically create a full project-management stack.

## Parked ideas

Only when the user asks to park a speculative item, reuse the tracker's deferred/ideas mechanism or create an ideas note from [the optional template](references/EXPLORATION_BACKLOG.md). Mark the idea uncommitted and preserve its source. Wire a short guidance pointer if future sessions need it; check the note and pointer independently and avoid duplicates.

Parked ideas do not change committed scope. Surface them during an explicit status review or project closeout, or when the user asks about them. Do not use them as the next work item without authorization.
