---
name: project-bootstrap
description: Create or retrofit the minimum project guidance and durable state needed for the requested work. Reuse existing documents and trackers; choose minimal or Markdown continuity according to project needs.
---

# Project Bootstrap

Read the repository's current guidance and identify scope, work-state authority, decisions, evidence, and verification commands. Reuse adequate equivalents. An inline continuity check is enough; running a separate audit is optional.

Choose the smallest useful mode from [the variant guide](references/variants.md). Default to minimal guidance for small tools and maintenance. Use a compact Markdown work record when sustained work needs handoff. Do not install or switch a backend just because bootstrap was requested.

Create only demonstrated missing pieces, using relevant [templates](references/templates/README.md) as starting points. Omit unused sections and replace placeholders with project facts. A separate vision or roadmap is useful only when scope or dependencies need more room; no multi-file stack is mandatory. Avoid duplicating executable work across a plan and a tracker.

For substantial new Markdown records, prefer `docs/` scoped to the area they govern, following the [location guidance](references/variants.md#documentation-location). Preserve adequate existing placement; do not migrate records just to match this preference or create empty documentation folders.

Put shared instructions in AGENTS.md at the relevant directory root, with CLAUDE.md beside it containing only @AGENTS.md. Link to canonical records rather than duplicating them. When existing vendor guidance has useful substance, reconcile it into the shared guide before replacing the shim; preserve intent and do not discard unresolved conflicting instructions. Explicit user requests for another arrangement take precedence. Existing authorization covers the requested retrofit; ask only when a consequential conflict is still undecided.

Record current work and consequential decisions with their evidence in the chosen authority. Add a narrow instruction to update that store when authorized work changes durable state, and leave an actionable next step when work remains. The human should not need to invoke a maintenance skill every session.

Do not bootstrap an exploration backlog. If the user later parks an idea, status-ledger can add it to the existing tracker or create a small ideas note on demand. Finish with created or updated artifacts, the authority chosen, validation, and any remaining gaps.
