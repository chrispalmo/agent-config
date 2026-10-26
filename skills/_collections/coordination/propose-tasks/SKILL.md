---
name: propose-tasks
description: Propose useful tasks or next steps for the current project or discussion, checking existing plans first and presenting justified proposals in a numbered table. Use when the user asks what to do next, requests further development ideas, or wants project task suggestions; do not turn an ordinary execution request into a planning exercise.
---

# Propose Tasks

Give the user a grounded account of what remains and useful options for further development. Proposing work does not authorize execution, delegation, new chats, or changes to the project's plan.

## Establish scope and current state

Use the user's explicit scope first. In a new chat belonging to a project, use that project's goals, guidance, and current state. Include adjacent work only when its connection to the project's outcome is concrete; explain that connection. In an established chat, stay with its purpose and the work already being developed unless the user requests a broader project review.

Inspect the existing authoritative plan, ledger, tracker, or current-state note when available, together with enough relevant evidence to understand the next action, completed work, blockers, and decisions. Reuse recent inspection where sufficient. Do not create a competing ledger or silently substitute another store. A request for next steps does not require a full audit, another test suite, subscription checks, or broad chat searches.

Distinguish remaining agreed work from new proposals. Prefer the existing next action when it still fits the user's goal; do not replace an unfinished plan with speculative features. Respect later corrections and holds. If a clear action is already authorized and the user requests execution, proceed within that authority rather than introducing a new proposal or approval gate.

When the current scope is complete and the relevant evidence supports it, say so directly before suggesting anything else: the agreed work is complete and no open items were found within the inspected scope. Label additional ideas as optional further development. Known blockers, unanswered required decisions, and held integration are still open items. If the state is unavailable or uncertain, say what is unknown rather than claiming all loose ends are tied off across the entire project.

## Generate useful proposals

Before recommending or ordering tasks, state the intended outcome and relevant criteria, such as contribution to the project or thread goal, evidence of an unresolved problem, correctness, recovery, learning value, dependencies, human attention, and implementation effort. Reuse established criteria and label material assumptions. Do not introduce monetary estimates or claimed savings as an agent-workflow ranking criterion.

Suggest work because it has a concrete benefit, not because an allowance is available or a list needs filling. Each proposed task should be bounded enough to understand and select. State what would change or what question would be resolved. Its justification should connect that result to the user's goal, cite relevant evidence where available, and distinguish a demonstrated gap from an exploratory idea. Avoid invented precision, duplicate tasks, and unrelated improvements.

## Present a numbered table

Use this format for task proposals, including responses to ordinary next-step questions:

| ID | Proposed task | Justification |
| --- | --- | --- |
| <next conversation task ID> | <short description of the action or investigation and its intended result> | <why it is useful now, with evidence or an explicit assumption where material> |

Follow the conversation's existing numbering convention and sequence. Where no convention exists, use dotted IDs with one group per new proposal table. Do not restart the sequence on each invocation. Preserve existing task IDs when referring to a prior proposal or authoritative tracker; distinguish tracker IDs from new conversation proposal IDs rather than silently renumbering the tracker. Retain the proposal's message or artifact identity so a later selection can resolve the exact version.

Keep descriptions short and justifications specific. Link the relevant plan item, artifact, or evidence directly when mentioning it. Add a status/basis column or clearly labeled separate tables only when needed to distinguish existing commitments, blocked work, and optional further development. Do not imply that table order is a priority ranking without explaining its basis. Do not force a fixed number of tasks or invent proposals when none is worth recommending.

## Keep proposal, organization, and execution distinct

This skill generates useful options from the current state. Triage organizes and addresses a supplied stream; it is not a mandatory prerequisite. Delegation assigns selected work to owners and follows it through. A user can use these capabilities independently or explicitly chain them within an established scope.

When the user also requests a delegation proposal, carry the exact task IDs, outcome, justification, known acceptance, and authorization boundary into the available delegation workflow. Do not invoke an unavailable skill or claim a draft command is installed. A proposal alone does not send messages, create chats, authorize another harness, or promote tentative ideas into requested implementation. Preserve any existing direct authorization rather than asking for it again solely because a workflow is chained.
