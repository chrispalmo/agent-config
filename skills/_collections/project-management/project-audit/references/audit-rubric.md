# Continuity assessment criteria

Assess whether another agent can act correctly using the available evidence. These criteria are the procedural authority for project-audit; they do not predict performance or require particular filenames.

| Capability | Evidence to inspect | Consequence of a gap |
| --- | --- | --- |
| Scope and success | Goals, non-goals, current user instruction, and acceptance conditions | Work may solve the wrong problem or broaden scope. |
| Work authority | One named task/status store with useful current items | Agents may duplicate work or maintain competing backlogs. |
| Blockers and dependencies | Unresolved decisions, prerequisites, and a concrete next action | An agent may start work that cannot finish. |
| Completion and verification | Relevant commands or checks and evidence on completed work | Recorded completion may lack support. |
| Decisions and provenance | Reasons for consequential choices and links to their sources | Assumptions may become facts or settled decisions may be reopened. |
| Resumption and guidance | Build/test entry points, repository constraints, changed-state handoff | The next session may repeat work or miss important constraints. |

Use supported, partial, missing, or not applicable. Explain why a capability does not apply. Distinguish a missing store from a stale or contradictory one. Accept adequate equivalents without partial-credit penalties: a tracker, README section, project note, database-backed work queue, or specification can satisfy the need.

A missing `docs/` directory or records in another adequate location are not continuity gaps. Assess whether canonical records are discoverable and scoped appropriately rather than enforcing a preferred folder layout.

Sample completed and open work against actual artifacts where available. Static review supports conclusions about the inspected guidance; agent-outcome claims require separate behavioral evidence. Frozen projects and completed tools can need only usage and scope information. Do not invent planned work to fill the table.

## Report shape

State the project's purpose and whether its current work can be resumed. Then use a table with Capability, Assessment, Evidence, and Gap or consequence. Finish with prioritized corrections and unresolved choices. Follow active conversation formatting and link conventions.

For a requested retrofit, reuse the project's existing authority and close the demonstrated gaps. Invoke project-bootstrap only when guidance or continuity structure actually needs creating; do not prescribe it merely because optional documents are absent.
