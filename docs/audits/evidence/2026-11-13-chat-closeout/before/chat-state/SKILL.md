---
name: chat-state
description: Assess a chat's unfinished work, human and agent obligations, and readiness to leave on read, start a new topic, or archive. Use for conversation-state or readiness questions, including a requested project or global review. Read-only; preparation belongs to chat-closeout.
---

# Chat State

Tell the user what they can do with the conversation without abandoning work or losing necessary material. Distinguish all agreed work being finished from unfinished work having a reliable continuation elsewhere. This skill owns the readiness criteria shared with [chat-closeout](../chat-closeout/SKILL.md).

Assess without changing files, tasks, chats, read states, schedules, or running work. A question such as “can I archive this?” requests an assessment. If the user also requests preparation, use chat-closeout within that authority; they need not invoke an assessment first. A read receipt, silence, inactivity, or a finished model turn establishes neither approval nor completion.

## Establish scope and evidence

Default to this conversation. For a project, selected set, or global review, enumerate the accessible chats in that scope using supported tools and pagination. State hosts/sources, selection, omissions, and inspection time; do not describe the accessible subset as all chats. Include archived chats only when requested or needed to verify a relevant dependency. Do not create a global task store or inspect unrelated material.

Read original messages and later corrections back to the beginning or a verified clearance checkpoint, carrying forward the obligations and external references at that checkpoint. A title, listing summary, or prior “done” statement is a discovery aid, not a clearance checkpoint by itself. State missing/truncated history and whether it prevents a verdict. Reuse adequate recent evidence instead of repeating a full audit.

Reconcile the conversation with the relevant current work records, artifacts, execution results, and receiving owners. Inspect only dependencies that affect the verdict. Preserve source identity and distinguish direct human requests from quotations, agent promises, automated submissions, proposals, and inferred intent.

For repository work, the repository's designated records own continuity; standing chats are replaceable coordination entry points. Check that necessary decisions, work state, evidence, and next actions are recoverable from those records by a replacement chat or another harness. The transcript may supplement those records but must not be required to resume the work.

## Account for unfinished business

Find unanswered substantive requests, incomplete deliverables, verification and integration, held publication, promised follow-up, required human decisions/actions, delegated work and its supervision, and relevant running jobs, schedules, temporary resources, worktrees, or attachments. These are prompts for judgment, not mandatory checks of every subsystem.

For each consequential open item, establish the actual owner, status, next action or trigger, authority/holds, and a source or durable destination. Expose missing ownership or follow-up rather than inventing it. Use the existing project records; distinguish work owned here from work already owned elsewhere.

Keep proposed, authorized, in progress, blocked, deferred, cancelled/superseded, transferred, and verified complete distinct where they affect a decision. An agent promise without authority is an unresolved promise, not permission to execute. A question addressed to the user is not automatically a human commitment. Identify required input separately from optional suggestions. Do not promote unselected ideas into a backlog or make their rejection a condition of closure.

Check the requested completion boundary: saved, tested, committed, merged, installed, pushed, and deployed are different outcomes. Require the ones the task actually needs; unrelated dirty files or optional publication do not block clearance. A dispatched message proves delivery at most, not acceptance, completion, or transfer of supervision.

An item has a reliable continuation when the durable record is accessible and discoverable from the destination's normal workflow, preserves enough context and evidence to resume, and identifies who takes the next action and how it will surface. For active delegation, verify the receiving owner's acceptance or an established assignment mechanism that makes ownership effective. Include responsibility for follow-up, integration, and acceptance. A scratch note, unnamed future reader, or promised report back only to this chat does not meet this standard. Do not invent a reminder or schedule: a recorded review trigger and an actual monitor are different things.

## Judge each action independently

Use **YES**, **NO**, or **UNVERIFIED**. A known unmet condition means NO; missing consequential evidence means UNVERIFIED. Explain each non-YES verdict and the smallest action or evidence needed to change it. Limit certainty to the inspected scope.

| Action | Conditions for YES |
| --- | --- |
| Leave on read / start a new topic | No unfinished obligation depends on the user remembering to return to this exchange. Agreed work is finished or has a reliable continuation elsewhere. Required human input is discoverable at that destination with its consequence and appropriate next trigger. |
| Archive | The leave condition holds, and no running work, follow-up, or resource depends on this chat remaining active or visible. Necessary historical references remain retrievable under the host's established archive behavior. |

Routine assessment and reporting cover only these two actions. Do not investigate or report deletion readiness unless the user specifically asks about deletion. For that explicit request, separately verify that necessary work, decisions, authorization evidence, and artifacts survive independently and establish the host's relevant deletion effects; archive readiness alone does not establish deletion readiness.

Standing versus task conversation determines whether the user intends to retain it, not whether its work is finished. Readiness does not require retaining every casual suggestion or word of the transcript. Preserve material needed for ongoing or accepted work, including useful agreed conclusions. A copied authority summary must preserve its actual source and scope; it cannot create permission.

Readiness is a snapshot. New work, changed artifacts, or failed follow-up can invalidate it. Reuse does not erase prior context or guarantee unrelated topics cannot influence one another. A fresh conversation is available when context separation matters.

## Report for action

Lead with two compact, clearly visible statuses: **ready to leave on read/start a new topic** and **ready to archive**, using text verdicts with optional symbols. Separately state whether **all agreed work is finished** or **work continues elsewhere**. Do not hide unfinished work behind a green readiness marker.

Follow with outstanding human and agent actions, their owners and direct destination/evidence links, any remaining dependency on this chat, and what would remove it. Say whether actual archiving occurred; assessment alone does not archive. Include scope, inspection time, and material coverage limits without a repetitive form for trivial cases. Follow the user's numbering and link conventions.

When a substantive proposal needs the human's disposition to resolve an existing loose end, ask a concrete decision question, such as “Do you want me to hand these off now?” Distinguish this from optional ideas, which need no response, and completed work, which needs no acknowledgment. Silence does not authorize the proposed work.

For global reviews, give one row per assessed chat and links to shared obligations rather than counting them repeatedly. Preserve different verdicts and access limits per chat. Do not mark chats read or archive them to make the report look clear.
