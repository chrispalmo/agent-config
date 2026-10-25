# Native Cursor route

Read after a Cursor native route and its settings are proposed or selected. Verify the actual client/account route as well as the model. Previous sessions, paths, and allowance windows are not reusable defaults.

## Launch and resume

The [official parameters](https://cursor.com/docs/cli/reference/parameters), checked 25 October 2026, expose model selection, model listing, session resume, output format, workspace, and sandbox options. Locate the installed binary rather than assuming whether it is named `agent` or `cursor-agent`, and inspect current help/version.

An illustrative argument pattern is:

```text
<verified-native-binary> --print --model <approved-model>
  --output-format <json-or-stream-json> --workspace <authorized-workspace>
  --sandbox enabled [--resume <verified-existing-session-id>] <remaining-work-brief>
```

Use safely quoted values or an argument array. Resume only a verified matching session/workspace; omit the resume argument for an authorized new native session. Native execution does not implicitly authorize a new user-owned chat, cloud session, or worktree.

Keep workspace trust within the approved location. The documented `--trust` and `--force` flags suppress prompts or broaden command permission; they are not neutral boilerplate. Preserve approval and sandbox controls. They limit unintended commands/access but may block legitimate tests, which should be reported as blocked rather than treated as product failures. A workspace path or trust setting does not establish source-transfer consent.

A separate reasoning-effort flag was not established by the checked parameter documentation. Report that control as unverified unless the current client exposes it. Do not invent a flag or treat a model-name suffix as proof of effort.

## Authentication and public results

The [authentication documentation](https://cursor.com/docs/cli/reference/authentication) describes native login and API-key routes. Inspect relevant public status and child-environment routing. For subscription-only work, account for `CURSOR_API_KEY` and other applicable provider overrides without exposing their values; an old launcher's removal list does not prove the current route.

The [output documentation](https://cursor.com/docs/cli/reference/output-format) distinguishes final JSON from stream events. When initialization metadata is needed, retain sanitized model, session, working-directory, and permission/auth-source fields. Final JSON alone may lack those fields and must not be called runtime-model verification. Preserve exit status and public error output when failure produces no final JSON. Select the output format explicitly.

## Acceptance and cleanup

A completed process and selected passing checks still require owner acceptance of the actual candidate. Preserve a rejected candidate and its evidence, and identify any owner correction separately.

Verify exported artifacts before cleaning task-owned scratch. Preserve borrowed dependencies and other owners' work. Inspect current native controls for residual trust/session state and report unsupported cleanup; do not edit global stores to simulate revocation. Recheck this adapter after a relevant client, authentication, or output change.
