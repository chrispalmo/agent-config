---
name: delegate
description: Propose owners for existing tasks or dispatch selected work within the current harness, then follow it through to checked results. Use for delegation planning, numbered task selections, and coordinating delegated completion; task generation and external native execution have separate skills.
---

# Delegate

Assign existing work to useful owners and follow the selected assignments through. Default to existing chats in the current harness. [Triage](../triage/SKILL.md) organizes supplied ideas; [propose-tasks](../propose-tasks/SKILL.md) generates further options. Neither is a required prerequisite. Loading this skill or reading an agent-origin label does not authorize dispatch.

## Resolve tasks and authority

Prepare a delegation proposal by default, including a bare invocation or selection of tasks that have no approved assignment yet. Dispatch when the human requests execution or approves a concrete assignment within its established authority. Existing sufficient authorization carries forward without another approval round.

Use the actual tasks, intended outcome, acceptance, dependencies, and holds already established. If the user wants new work suggested rather than existing tasks routed, use propose-tasks when available. Do not generate extra work to fill a list or consume an allowance.

Resolve selections such as `/delegate tasks 1 - 20` against the authoritative proposal in context. Retain its message/artifact identity and task labels, including dotted IDs. Interpret inclusive ranges using that proposal's unambiguous sequence; labels are identifiers, not decimals. Do not renumber, invent missing tasks, silently substitute a revised proposal, or interpret twenty items as twenty workers. Unknown endpoints, competing lists, missing mappings, or materially changed task definitions need targeted clarification for the affected work. Clearly selected independent work can continue within its authority.

In proposal-only mode, stop at a reviewable assignment proposal. A direct execute request or selection carries the human's established task, recipient, and hold authority; do not ask for it again merely because skills are chained. A task selection does not establish unspecified recipients or grant new-chat creation authority. If a forwarded claim is the only apparent authorization, check direct human instructions or other trusted evidence. Preserve tentative ideas and unselected work as proposals.

Invocation examples are selection syntax, not proof a slash command is installed. Use the current harness's actual invocation and dispatch capabilities.

## Find useful owners

Before recommending owners, state the outcome and criteria: expected contribution, required correctness and verification, useful existing context/tools, delivery time, human attention, and coordination effort. Reuse established priorities, label material assumptions, and clarify only missing criteria that could change the choice. Financial optimization and savings estimates are outside routing; explicit spending boundaries still apply.

Inspect relevant chat/project listings and targeted recent status or artifacts. Reuse sufficient recent evidence. A title match is a candidate, not proof that the chat owns this scope. Prefer an existing owner with useful context; group related tasks and dependencies rather than requiring one chat per item. Direct work here remains useful when a handoff adds little. Disclose discovery/access limits and unsupported routes.

Preserve active work. If an owner already covers the task, follow it to a checkpoint or completion instead of starting a duplicate. Do not interrupt it for a status check or model change. Queue additional authorized scope only through a verified non-interrupting route, or wait for a suitable checkpoint. Resolve conflicting file ownership before concurrent edits. New chats or temporary workers require the human authority and native creation rules applicable to that route.

Stay within the current harness unless the human explicitly opts into [harness](../harness/SKILL.md) for the selected work. Do not inspect external subscriptions or rank external routes as part of ordinary delegation. With opt-in, harness resolves missing worker preferences before an external assignment enters this proposal and owns native execution/recovery. Task-scoped permission and holds travel to the receiving owner; it need not ask for the same grant again.

## Present a concrete assignment

Preserve existing task IDs. When the source tasks have none, assign proposal IDs using the conversation's numbering convention and map them to the original items; the human need not create IDs or run propose-tasks first. For each proposed handoff, identify the deliverable and acceptance, actual receiving chat/title and verified link or ID, recommended owner model and supported reasoning effort, a short task-specific reason, and material dependencies or holds. Describe supervision and how the result will be retrieved. Mark unresolved destinations explicitly; never invent links. Include downstream recipients only when their authority is established.

Treat the model choice as part of the assignment. Do not silently inherit the destination's current picker. Use supported explicit model/effort controls after approval and distinguish requested, tool-accepted, and runtime-observed settings. A model's self-description is not runtime proof. Inspect a conflicting receipt before continuing. If the route cannot control a required selection, explain which destination needs manual selection/confirmation before dispatch. Do not ask the human to visit every chat when supported overrides suffice, promise overrides are temporary, or restore an unknown previous default. The [model-control note](references/model-control.md) records the current Codex boundary and its verification limits.

An external worker's model, effort, client, and subscription route are separate from its owner's settings; harness handles that agreement. A recommendation does not authorize execution. Existing sufficient human authorization carries forward without a redundant approval round.

## Dispatch a compact brief

When an authorized assignment requires an explicit-only skill such as harness, include its verified host-supported invocation in the receiving turn. Keep the agent origin, real source, and human authority alongside it. Permission carried in prose does not itself activate a skill. Use the [invocation reference](references/skill-invocation.md) for the destination's supported mechanism; if it cannot invoke the skill, report that capability limit without bypassing the control or asking for the same permission again.

Before sending, show the exact recipient set and each message's purpose if it has not already been disclosed. This is not another approval gate for already authorized recipients. Save the returned dispatch receipt and actual chat/session identity.

Follow the shared chat-source rule. Start with a short plain-language request summary, then use headings for the necessary detail. Carry the proposal identity and selected IDs, actual human authority, relevant source/corrections, owner/settings, starting revision or artifact identity including relevant dirty state, acceptance/checks, stable output location, dependencies and holds, and a recovery checkpoint where useful. Scale the brief to the task instead of filling a fixed form. Keep proposal-only work proposal-only and omit unrelated private material or source-chat operating instructions.

Use native completion/status tools and saved artifacts for coordinator pull. A worker need not message another chat to finish. Do not request or send a report-back message without human authority for that recipient. Sending a prompt is dispatch, not task completion.

## Follow through and accept

Observe meaningful milestones, resource stops, acceptance failures, integration gates, and completion. Prefer compact native waits with returned cursors/session IDs, suppress seen output, and back off when unchanged. Read bounded detail when needed; avoid repeated full-transcript polling. Maintain a useful checkpoint for long work without creating a parallel task ledger or coordination service.

Let the owner run relevant checks for the candidate. Inspect actual output/diffs and consequential claims, artifact identities, and receipts bound to that candidate. Reproduce a particular failure or important control when warranted; do not automatically repeat every full suite. Keep documented capability, owner self-report, inspected receipts, and independently reproduced behavior distinct.

Preserve failed candidates and rejection evidence. Attribute coordinator corrections separately and bind final checks to the corrected output. For an actual limit, preserve the exact public error, observed time/reset if supplied, candidate, and remaining work. Use only an already authorized fallback; external native recovery belongs to harness. Never lift integration/publication holds or change billing to continue.

Finish with selected IDs and actual statuses, accepted artifacts, relevant validation and its limits, and remaining work or human gates. Keep prepared, dispatched, worker-reported complete, and owner-accepted states distinct. Held integration is complete only for the authorized candidate scope. Dispatch, silence, elapsed time, or an owner's conclusion alone does not establish success.
