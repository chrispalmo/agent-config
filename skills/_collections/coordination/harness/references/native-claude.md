# Native Claude route

Read after a Claude native route and its settings are proposed or selected. Verify current local help/version and the actual account route; previous execution does not establish current eligibility.

## Launch and persistence

The [official CLI reference](https://code.claude.com/docs/en/cli-reference), checked 25 October 2026, documents print mode, explicit model/effort selection, structured output, auth status, and session resume. Effort support depends on the model. Choose persistence intentionally: `--no-session-persistence` prevents later conversation resume, even when initialization returns a session ID. Such a run recovers through its saved artifacts and remaining-work brief.

An illustrative one-shot argument pattern is:

```text
claude --print --model <approved-model> --effort <supported-approved-effort>
       --output-format json --no-session-persistence <bounded-task-brief>
```

This is an argument pattern, not a shell command to paste. Resolve the installed binary, use safely quoted values or an argument array, set the authorized working directory, and preserve its approval/tool settings. Do not add permission-bypass flags or automatic model fallback to make headless execution complete. Retain a tool refusal and the affected work when a required action is denied.

## Authentication and entitlement

Inspect public authentication metadata without retaining credentials or unrelated account information. A logged-in or cached subscription label is not proof of current included entitlement. If it conflicts with fresher account/plan evidence, resolve the discrepancy before inference. A browser check is conditional on that uncertainty, not required for every run.

For subscription-only work, check current provider/auth routing and remove conflicting child-only environment overrides without changing global credentials or logging their values. Removing environment keys alone does not establish the selected account or allowance. Do not probe uncertain access with inference or silently switch to credits.

## Results and recovery

Retain requested settings and any native-reported model/provider separately, the public terminal/error state, session identity, workspace, candidate identities, relevant checks, and pending work. For streaming output, retain sanitized initialization/result/error evidence rather than private thinking or complete tool transcripts.

An actual limit can leave useful edits and passing checks despite a failed process. Inspect the files and receipts before writing the recovery summary; stale progress text must not override them. Another harness receives that checkpoint, not a claim to have resumed the original native conversation. A returned candidate retains its integration/release holds until owner acceptance.

Recheck this adapter when CLI, authentication, output, or persistence controls change. Documentation and prior observations establish these mechanics; no general performance improvement is claimed.
