---
name: browser-session
description: Register and manage agent-created browser tabs using bot/ task groups and a shared local session registry. Use before opening browser tabs and when resuming or finishing browser work.
---

# Browser Sessions

Use `bot/<task>` groups, for example `bot/store-setup`, for tabs created during the task. Use a short task slug; keep harness identity in the registry. This skill records local browser work, not general task activity.

## Register and renew

The helper is [scripts/registry.py](scripts/registry.py), relative to this skill. Run it with Python 3; it does not control the browser. It stores one JSON file per session under `/tmp/agent-browser-<uid>/sessions/` (`/private/tmp/…` on macOS), using the current user's numeric UID, private directories, and locked, atomic writes. Every harness uses this same path regardless of its working directory, `TMPDIR`, or `XDG_STATE_HOME`. `status` reports the resolved registry path. No service or background heartbeat is required. Do not store URLs, page contents, credentials, or sensitive task descriptions in records.

Temporary storage can be cleared by the operating system. Missing records never establish ownership: leave those tabs alone. Do not reconstruct ownership from a `bot/` group name. `AGENT_BROWSER_STATE_DIR` selects a separate store for isolated tests only; do not set it during normal browser work or cleanup.

1. Read the current harness's browser documentation. Reuse its automatic tab cleanup and handoff/deliverable controls. Obtain an exact browser/profile identity (prefer the extension instance ID) and supported group/tab IDs. Browser indexes alone are not stable identities. Use a browser-incarnation ID too if the tool provides one.
2. Run `python3 <helper> start --task store-setup --browser <browser-profile-identity> --owner <harness-and-task-id>`. Keep the returned session ID in the task context. Reuse that session on resume; create separate groups for different sessions, even when their titles match. Never adopt an existing group solely because its name matches.
3. Open tabs through the permitted browser tool and group them in their current window under the returned `group_title`. Create a separate group for each window as needed. Register each new tab: `python3 <helper> tab --session <session-id> --tab <tab-id> --group <group-id>`. Register only tabs this session created, including confirmed child tabs. Never move existing human/unknown tabs into a bot group.
4. Renew before using a registered tab: `python3 <helper> touch --session <session-id> --tab <tab-id>`. This protects the session for two hours and the used tab for two hours. Registration also protects newly opened tabs for two hours. Renew at browser activity boundaries rather than after every click. Before known long unattended work, use `touch --session <id> --hours <duration>` to cover that work; renew when it resumes. If it stops unexpectedly, protection eventually expires.

If grouping, a stable browser identity, filesystem access, or registration is unavailable, use native ephemeral tab controls and close temporary tabs yourself. Explain that shared cleanup cannot cover those tabs. Do not fabricate registration, silently substitute another registry, or weaken browser restrictions to make it work. A local registry does not coordinate remote machines without access to that same browser and state directory.

Keep the harness's normal sandbox and approval settings. Do not change global permission settings, select a custom permission profile, or add write grants to enable this registry. If access is denied, follow the native ephemeral-tab fallback above.

The helper reports any records remaining in the former `~/.local/state/agent-browser/sessions/` store instead of silently splitting ownership between stores. Deployment maintenance can move them once with `migrate --from <old-sessions-directory>`. Migration locks both stores and preserves IDs, activity times, holds, and keeps; it never renews sessions. Ordinary browser work should report that migration is needed rather than create another store.

## Finish or hand off

Close intermediate, duplicate, research, and completed workflow tabs when no longer needed. Verify closure through a fresh tab listing. Do not close a live result requested by the human. A saved result link is often enough when the live tab has no special purpose.

For a tab needed for human review, login, a click, or continuation, apply the harness's native retention mark and run `python3 <helper> handoff --session <id> --tab <id> --reason 'Human review required'`. This sets a 48-hour review deadline. Tell the human why it remains open and when it becomes eligible for cleanup. A deadline is not evidence that the human acted. The cleanup job may close it at the first scheduled run after expiry; it need not close exactly at expiry.

Use `handoff ... --keep` only when the human explicitly requests indefinite retention; this cancels automatic expiry for that tab. Resume browser work with `touch`, which clears a finite handoff on that tab but preserves an explicit indefinite keep. Do not renew finished sessions merely because a cleanup job is inspecting them.

After closing tabs, use the full fresh snapshot format in [browser-cleanup](../browser-cleanup/SKILL.md) and run `reconcile --snapshot <file>` to remove absent/moved tabs from the registry. No open tabs means the record can be removed. Keep the session ID and any needed continuation information in the owning chat; never commit the runtime registry.

## Cleanup

Load [browser-cleanup](../browser-cleanup/SKILL.md) for requested manual or scheduled cleanup. Unregistered tabs and older ungrouped tabs are excluded. Only adopt legacy tabs with explicit human identification and authorization.
