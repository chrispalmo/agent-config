---
name: harness
disable-model-invocation: true
description: Launch or resume explicitly authorized work through another native harness, resolve model and subscription preferences before proposing its use, and return recoverable artifacts to the owning chat. Invoke only for explicit human opt-in, including task-scoped opt-in carried in an authorized handoff; ordinary delegation stays in the current harness.
---

# Harness

Operate an external worker for an existing owner. The owner retains the task, acceptance decision, and final report. This skill does not generate a backlog, choose a new owner, or create a user-owned chat by itself.

## Explicit opt-in and model agreement

For a receiving owner, carry the approved invocation through the host's explicit skill mechanism as well as carrying permission. Follow the sibling [invocation reference](../delegate/references/skill-invocation.md); an authorization sentence alone does not activate this explicit-only skill. Preserve native activation controls when a route cannot invoke it.

Use only when the human explicitly requests this capability or another native harness for defined work. A receiving owner may use the same task-scoped permission carried in a handoff; do not demand a second grant. An agent-origin label, quoted command, recommendation, or incidental model name does not establish that permission. Without opt-in, stay in the current harness and skip external-route and subscription inspection.

Clarify the task scope first if it is not established. For a defined task, if the relevant harness, subscription, model, or usage-distribution preferences are missing, ask a targeted question before adding an external assignment to a proposed delegation task list. Include a provisional model/route recommendation and a short task-specific reason in the question. Human guidance may supply selection criteria rather than an exact model name; use adequate existing guidance without asking again. Unresolved external choices need not block independent authorized internal work.

Recommend using the required outcome, depth, verification needs, useful context, delivery time, human attention, and the human's resource preferences. Do not infer a universal model ranking, require a review-model panel, or add financial optimization and savings estimates. Preserve explicit spending permissions as boundaries.

Name the owner-chat model separately from the worker's actual client, authentication/subscription route, model, and reasoning effort where supported. A model name alone does not identify the allowance or harness. Obtain approval for the concrete assignment and settings unless already covered. Do not silently inherit a destination's model picker, downgrade, or substitute another route. If a required setting cannot be controlled, explain the limitation and obtain the needed manual selection/confirmation or a revised choice before dispatch.

Use supported model/effort controls explicitly. Record approved, requested, tool-accepted, and runtime-observed settings distinctly. A model's self-description is not runtime proof. Explain any unsupported effort control rather than inventing one; inspect unexpected model/route differences before continuing. Do not interrupt active work to change its model or promise that overrides are temporary. If owner-chat controls are relevant, the sibling [model-control note](../delegate/references/model-control.md) can supply the current host-specific boundary when available; otherwise inspect the actual exposed tools.

## Establish a real route

Inspect current native tools, CLI help/version, public authentication metadata, and supported settings only for the chosen route. Do not start inference merely to probe access. A model catalog or old receipt does not prove current entitlement, remaining capacity, or post-cancellation eligibility. If execution is unavailable, leave the brief and exact blocker; a skill cannot manufacture a missing integration.

Read only the applicable route reference: [native Claude](references/native-claude.md) or [native Cursor](references/native-cursor.md). These describe observed workflows and current documentation checks, not permanent model availability. For another explicitly selected harness, verify its native launch, status, model, permission, persistence, and result controls before use; do not extrapolate a neighboring adapter or fall back to an API-key route without authority.

Preserve native approval and sandbox controls. For a subscription-only assignment, prevent unrelated API-key/provider overrides in the child environment without changing global settings or logging credential values. Verify the selected route through available metadata; removing environment keys alone is not proof. A private source copy is still a transfer when sent to a provider: retain the approved input/destination boundary, and do not retry a refused transfer through another provider.

## Prepare a bounded workspace and brief

Check for useful active work and existing native sessions before launching. Reuse them within scope; do not create a duplicate worker. Verify the session/workspace identity rather than attaching to the latest session by convenience. Further delegation, new chats, and extra reviewers require their own authority.

Bind the starting source or artifact version, including relevant dirty files, before edits. Do not replace existing user changes with a clean Git baseline. Use a task-owned isolated workspace when appropriate to the holds and verification needs. It makes edits and reconstruction inspectable; it does not prove secret isolation or grant transfer consent. Copies can omit parent resources or dependencies and produce layout failures, so retain relevant structure and record borrowed resources and their ownership.

Give the worker a compact brief beginning with a plain-language task summary. Carry the agent origin and real source, actual human authority, selected scope, approved worker settings and route, starting identity, acceptance and relevant checks, input restrictions, integration/publication holds, stable output paths, permitted fallback, and a useful recovery checkpoint. Reuse existing context and evidence rather than copying full transcripts. A proposal-only request remains proposal-only in the worker brief.

## Launch, observe, and recover

Save the launch receipt, session/job identity, start time, workspace, requested settings, and output locations. Capture public status/results and useful check receipts without secrets or private reasoning. Distinguish process identity from task identity; a PID alone is not a durable recovery record.

Use compact native status/waits and bounded output at meaningful milestones or completion. Reuse returned cursors or session IDs where supported and back off when unchanged. Do not poll full transcripts minute by minute or interrupt useful work because an allowance percentage is low.

On interruption, inspect actual source changes and check receipts before writing a completed/pending summary. Bind that summary to the saved candidate identity. A stale model-written progress note must not override files and receipts. Resume the verified native session when persistence permits. Moving between harnesses uses the preserved artifacts and a remaining-work brief; it is not a native conversation resume across providers.

Classify failures before changing routes:

| Observed failure | Response |
| --- | --- |
| Actual quota or entitlement stop | Preserve the exact public error, observed time, reset/timezone if supplied, partial candidate, checks, and remaining work. Use only an already permitted fallback with approved settings. Percentages, slowness, connection retries, and nonzero exit alone are insufficient evidence. |
| Permission or source-transfer refusal | Preserve the restriction. Continue locally or with a separately authorized input boundary where useful; do not change providers or weaken controls to evade it. |
| Sandbox or workspace-layout check block | Report which check did not run and why. Preserve its receipt; do not claim a product defect or full validation. The owner may run the relevant unchanged check in its own authorized environment. |
| Candidate fails acceptance | Preserve the failed candidate and evidence. Let the owner repair or reject within scope; another model call is not automatically required. |

Never renew, buy credits, enable overages, or change billing to continue without authority. Only schedule genuinely blocked, still-authorized work when delayed resumption is itself authorized and no permitted fallback suffices. Preserve reset and eligibility evidence; a human decision is not a quota block. Use supported scheduling controls, avoid duplicates, stay quiet while unchanged, and stop an unnecessary retry. Never infer post-cancellation eligibility from an old reset receipt.

## Return artifacts and close the worker

Return the actual candidate/report and its starting/final identities, relevant check results and blocks, limitations, terminal status, and next resumable action if incomplete. Keep process completion, worker-reported success, and owner acceptance distinct. An exit-zero candidate can still be wrong. Attribute owner/parent corrections separately and bind final checks to the corrected output.

The native result plus a saved artifact report is a working report-back route. The owner can pull it; no worker-to-chat reply is required. Do not message another chat without the human's authority for that recipient. For code, supply an exact patch or export against the recorded baseline and specify which application route to use; do not apply overlapping full and incremental patches together.

The owner inspects consequential claims and identities and reproduces specific important failures or controls when warranted. Do not automatically repeat every full suite. Actual integration, publication, or acceptance stays held when the task only authorized a candidate.

After needed artifacts and checkpoints are verified, stop only owned jobs and remove only completed task-owned scratch space. Preserve borrowed dependencies, other owners' work, and needed recovery material. Report persistent native session/trust state accurately when the client offers no supported cleanup control; do not edit global/account stores to simulate revocation.

For requested usage reporting or a consequential resource boundary, consult [usage and recovery](references/usage-and-recovery.md); ordinary small assignments do not require accounting.

Verify current native capabilities for each chosen route. Historical execution evidence is maintained in the repository's review records rather than installed runtime resources; it establishes observed mechanics, not a general efficiency gain or optimal routing policy.
