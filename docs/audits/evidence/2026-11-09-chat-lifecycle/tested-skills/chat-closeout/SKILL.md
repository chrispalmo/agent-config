---
name: chat-closeout
description: Prepare a chat to be left on read, reused, archived, or deleted by completing authorized work or establishing verified continuation elsewhere. Use when the user requests chat cleanup or closeout, including a selected project or global scope; readiness questions alone belong to chat-state.
---

# Chat Closeout

Remove the need to return to the conversation to recover unfinished business. Complete the requested work or establish a reliable continuation; a summary alone does not close an obligation. Use the criteria and reporting contract in [chat-state](../chat-state/SKILL.md), which is the single authority for readiness verdicts.

## Resolve the requested outcome

Assessment is included. Read chat-state and inspect the relevant history, records, and dependencies; the user need not run both skills. Reuse a sufficient recent assessment, checking for changes before acting.

Default a bare closeout request to preparing the current chat to be left on read or reused. If the user names archiving or deletion, prepare to that standard. If the request includes performing the archive/delete action, distinguish preparation from the action and honor applicable host controls. Preparing for an action does not itself request that action. Standing conversations can reach the same readiness standard while remaining open indefinitely.

Determine scope from the user's request. Global scope changes the set of chats, not the authority to act in their projects. Do not replace an explicit read-only review with execution.

## Resolve obligations within authority

Carry existing authorization, acceptance conditions, and holds forward. A closeout request authorizes appropriate preservation and routine reconciliation within scope; it does not approve an unselected proposal, cancel a commitment, waive a review gate, or grant unrelated spending, publication, deletion, or messaging authority. Explain any concrete missing decision, finish independent authorized work, and keep the affected verdict open. Do not ask again for authority already supplied.

Choose the useful disposition for each obligation rather than forcing every item through a fixed sequence:

- **Finish:** complete and verify authorized work that belongs here, including required documentation, checks, integration, commits, merges, installation, synchronization, or deployment when within scope and authority. Do not turn cleanup into new features or whole-repository housekeeping. Attribute changed files and preserve unrelated work; clean Git status is not a universal completion condition.
- **Transfer:** when delegation is authorized, use the available delegate skill or supported equivalent. Carry the substantive task, actual authority and source, artifacts, next action, blockers, human gates, and responsibility for supervision, integration, and acceptance. Verify delivery and effective ownership. Preserve active work and avoid duplicate owners. A failed or merely proposed handoff leaves the obligation here.
- **Externalize a decision or deferred item:** update the existing authoritative tracker or continuity record, using status-ledger when available. Preserve what is needed from the human, whether it is required or optional, consequences, source, deadline or review trigger, and how it will surface. Do not create a reminder or contact a person without authority. Deferred work remains deferred; do not quietly defer active work to obtain a green verdict.
- **Preserve necessary material:** save decisions, useful agreed findings, validation, authorization evidence, and deliverables in their appropriate durable homes. Retain provenance and uncertainty; copy only relevant material into an appropriate audience/access scope. Check saved contents and discoverability. Reuse adequate stores; if none exists, create the smallest useful continuity record in an authorized location. Do not create a competing ledger or assume a temporary directory, chat attachment, uncommitted file, or transcript capture is a durable backup.
- **Retire owned resources:** reconcile relevant jobs, schedules, browser sessions, worktrees, temporary servers, and attachments within authority, using their existing ownership/lifecycle mechanisms. Keep resources needed for ongoing work and transfer their maintenance. Never delete or stop resources merely because they appear in the conversation.

The source chat's responsibilities are discharged only when its work is verified complete or every remaining obligation has an effective continuation independent of returning here. An active worker whose result must still be collected here has not been transferred. A time-sensitive human action needs a suitable discovery/follow-up path; a buried note is insufficient.

## Verify the requested readiness

Re-read changed records and inspect the actual results. Confirm no consequential item from the assessed scope disappeared, became falsely complete, lost its owner, or acquired invented approval. Verify required Git or external operations against the intended revisions/destinations, not just a worker's claim.

For archive/delete preparation, inspect the relevant host behavior and resource dependencies. For deletion, verify necessary records and artifacts can be recovered without this conversation and without its dependent attachments or storage. If those effects cannot be established, report UNVERIFIED instead of promising deletion safety. Do not destroy the evidence while trying to establish readiness.

When archive/delete execution is also requested, perform it only after readiness is established and through supported controls. Preserve the closeout result outside the target chat if that action would otherwise remove the user's only completion record. If an action fails, report actual state and remaining work rather than treating preparation as execution.

For a project or global closeout, deduplicate shared obligations, reconcile ownership before concurrent mutations, and finish independent authorized items while blocked ones remain explicit. Disclose inaccessible chats. Prefer existing destinations; do not build a new global task system or spawn a chat for every loose end.

Finish with chat-state's visible action verdicts, the distinction between all work finished and work continuing elsewhere, verified destinations, human/agent obligations, and any remaining blockers. A new topic can invalidate this snapshot. Do not append optional new work as though it were required to close out.
