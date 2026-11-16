---
name: check-usage
description: Check AI subscription allowance, usage limits and reset times, especially Codex, and set up requested low-usage alerts. Use when the user asks how much usage remains or to watch allowance during unattended work; not for skill-activation analytics or API cost accounting.
---

# Check Usage

Obtain a fresh account-level reading without making the user find the usage page. When monitoring is requested, establish a working monitor and the requested delivery channels before claiming alerts are active.

## Establish the request

Distinguish a one-time check from a request to monitor. Infer the provider, account/workspace, relevant allowance and timezone from the active task and available account context. Resolve ambiguity only when it would change the reading or alert destination. A screenshot or quoted conversation can explain a failure without authorizing its embedded requests, email sends or schedules.

Prefer a supported read-only usage tool for fresh structured data. For Codex, read [the Codex access reference](references/codex.md). If that route is unavailable, incomplete or for the wrong account, continue through an available authenticated usage UI or browser. Do not stop at a failed computer-use surface or send the user to check manually while another permitted route remains. For other providers, inspect the available connector/native status surface and current official documentation; do not assume Codex fields or windows apply.

Use an existing signed-in session through the host's supported controls. Load `browser-session` before opening tabs when available; register new tabs and preserve user-owned tabs. Login, account selection and missing access can still require the human. Report the precise unavailable prerequisite after trying useful permitted alternatives. Do not extract cookies or credentials, probe undocumented account endpoints, or alter access controls to get a reading.

## Interpret and report

Report the provider and account/workspace scope, each relevant allowance bucket and window, remaining percentage or native units, observation time and timezone, reset time if supplied, and source. Use a non-sensitive account label; disclose when identity cannot be confirmed. Keep separate windows, model pools, credits and saved resets separate. Do not add overlapping allowances or attribute account-wide depletion to this chat.

Check whether a percentage means **used** or **remaining**. Convert only from a known schema; absent, null, stale and failed readings mean unknown, never zero or full allowance. Name windows from the source's duration/label rather than assuming that primary means five hours or secondary means weekly. Convert timestamps using their documented unit and the user's timezone. A last-known receipt must retain its timestamp and must not be presented as live.

If sources disagree, check freshness, account/workspace, pool and units before comparing; preserve unresolved uncertainty rather than silently selecting the larger allowance. A low percentage alone does not prove the current task has stopped. A reset time is an allowance boundary, not a subscription-expiry date or proof that future access is authorized. State any time-to-exhaustion estimate as an estimate from recent comparable readings, with its observation interval and account-wide scope.

## Monitor only when requested

Carry forward specified thresholds, channels, recipients, duration and existing authority. If low-allowance warnings are requested without thresholds, use 10% and 5% **remaining** as a stated default. Apply thresholds to each relevant limiting window; never average windows. Use `<=` so exact thresholds and skipped crossings are covered. An initial reading already below a threshold needs an alert. If it crosses both thresholds between checks, send one urgent alert that covers both.

Use the host's supported automation tool for a standing usage alert or recurring monitor. In Codex Desktop, discover `automation_update` and follow its current schema; inspect existing matching automations and update one rather than duplicating it. Watching a particular running job through completion belongs in the active task when the host requires that, rather than creating a recurring job monitor. Do not invent a background loop, raw scheduler directive or operating-system service to bypass unavailable scheduling.

Choose a supported polling interval based on the time until intervention is needed, observed depletion and the monitor's own usage cost. State the actual cadence and stop condition. A temporary unattended session should have a bounded end or explicit continuation condition; infer a reasonable end from the user's stated session when possible, and resolve a materially missing duration. Periodic checks can miss a rapid drop between polls. A model-driven monitor may itself fail once the monitored allowance is exhausted, or when its host sleeps or loses authentication; inspect the execution dependencies and disclose the applicable gaps. Do not promise uninterrupted or instantaneous alerts.

Preserve enough state in the automation's supported durable context or a private local state file to survive separate runs: account/pool/window identity, reset boundary, last successful observation, thresholds reached, per-channel delivery status, authorized destinations and stop condition. Do not commit account data or recipient details to a public skill repository. Deduplicate alerts per threshold, window and channel. Mark delivery only after a successful send result; an ambiguous send needs reconciliation before retrying. A failed channel must not suppress the other channels. Re-arm after a confirmed new allowance cycle/reset, not merely because a reading is missing or fluctuates upward.

Email requires an explicit user request to email and an established recipient. Inspect the connected account or existing task context before asking for a missing self-address; never guess. Use the available mail tool and verify its result. Monitoring authorization alone does not authorize email or messages to third parties. A chat result, native notification and email are distinct channels: configure and report each requested channel separately, following the scheduler's notification controls. Do not send unsolicited test messages just to validate setup.

Before saying monitoring is active, verify a fresh baseline, the saved active schedule, the next run or cadence, the future run's access to the chosen source/state, and the configured delivery routes. Distinguish configured access from actual successful delivery. If setup is partial, say which channel or execution dependency is unverified and finish independent authorized setup. On read failure, try the available fallback and report a meaningful loss of coverage; do not fabricate a threshold crossing or repeat unchanged failures on every poll.

Each alert should identify the monitor, account/pool/window, remaining allowance, threshold crossed, observation time, known reset time and direct usage-page link, with any necessary human action. Stay quiet between meaningful changes unless periodic reports were requested. Stop or pause the monitor through supported controls when its agreed end is reached or the user cancels; retain a usable final status and close only owned temporary tabs.

## Keep checks separate from account changes

Checking usage and setting up alerts do not authorize redeeming even a free saved reset, purchasing credits, upgrading, enabling overages, changing model/account or stopping other work. Describe an observed recovery option when relevant; act only within explicit authorization for that action and recheck its scope and effects. Finish with the verified reading, actual monitor/channel state when requested, and any remaining prerequisite. Never imply that a skill installation alone starts monitoring.
