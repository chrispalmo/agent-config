# Usage, limits, and recovery

Use this reference when a real resource boundary affects authorized work or the user requests a resource report. Preserve the user's chosen subscriptions, order of preference, spending caps, cancellation instructions, and approval holds. Verify relevant current receipts without exposing credentials. Do not hardcode a vendor, plan, date, or temporary product hold into the reusable workflow.

## A real limit and a permitted fallback

Treat an actual quota/limit error as evidence for cutover. A percentage, slow response, or account-wide allowance estimate alone does not establish failure or justify abandoning an active run. Diagnose other failures on their actual evidence. Capture the exact error, account/route and model or pool if named, observed time, exact reset receipt and timezone if supplied, current process state, and preserved session/artifact identity. Unknown reset time or continued eligibility stays unknown. A pool may be shared or overlapping rather than additive.

Preserve useful output before changing routes. Continue with an already permitted, actually supported fallback from the saved checkpoint, keeping the same acceptance and holds. Do not interrupt useful active work merely because another route appears available. If a route or cost boundary materially changes, obtain the missing authority for that part while continuing independent authorized work.

Never renew, buy credits, enable overages, change billing, bypass an approval, or use an unapproved paid route to continue. A prior reset time does not prove post-cancellation access. Expiry, cancellation, and separate promotional credit can have different eligibility conditions; verify them before relying on them, or keep the step blocked. Do not infer an available credit balance from an older receipt.

## Delayed resumption

Use a supported scheduling tool only for genuinely blocked, already authorized steps after considering the permitted fallback. Inspect existing schedules to avoid duplicates. Save the precise remaining action, checkpoint, allowed route, reset evidence and timezone, cancellation/spend boundary, relevant holds, and stop condition. When supported, constrain retries so an expired or cancelled route is not attempted outside its authority. A required human choice is not resolved by waiting for quota.

Keep the monitor quiet while the state is unchanged or non-actionable; notify on meaningful change, completion, failure, or required human action. Recheck eligibility and authorization when it wakes. Stop/remove a now-unneeded retry through the native lifecycle tool. Do not schedule a new inference run when the authorized work has already finished. If scheduling is unavailable or unauthorized, leave the saved checkpoint and exact blocker; do not invent a reminder receipt or claim automatic continuation.

## Resource and effort reporting

Use the human's stated resource objective. Useful output from expiring included capacity can justify supervision in the main harness. Judge that choice by accepted output, quality, delivery time, human attention, cleanup, and the user's preferences. Financial comparisons, savings estimates, and counterfactual pricing are outside this workflow. Explicit spending permissions still constrain execution; they are not a ranking formula.

Report native usage or allowance data only when relevant and already available, with route, scope, window, units, and known gaps. Account-wide changes cannot be wholly attributed to this task when other work ran concurrently. Keep overlapping or incompatible resource pools separate.

For token records, establish whether each record is a per-response increment or a cumulative session snapshot. Deduplicate response/session identities. Sum disjoint increments, or derive valid deltas within one continuous cumulative counter; never sum cumulative snapshots. Treat resets and missing windows explicitly. Cached input may be a subset of input and reasoning may be a subset of output: follow the native schema and do not add subsets twice. Keep incompatible units and overlapping pools separate. Do not expose private reasoning to build a usage report.

When reporting effort, include coordinator supervision, delegated work, failed candidates, retries, verification, and parent corrections. Coordinator token share alone does not establish effectiveness: models, cache accounting, output quality, and owner use of the main harness can differ. Define whether time means elapsed delivery time, human attention, or total model/process effort; concurrent durations are not automatically additive elapsed time. More messages, workers, or tokens alone do not establish a better result.

Use trustworthy existing measurements when available; label missing data and estimates. Do not start new model runs, broad telemetry collection, or a measurement platform merely to complete a reporting field.
