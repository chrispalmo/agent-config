# Native activation evidence and subscription preference

Historical report of the 23 October check. On 24 October the human requested deleting the subscription-order rule; it has been removed from source and all three harnesses. The skill-review investigation is closed with notes retained. See [the current closeout](CLOSEOUT.md). The receipts and patch below preserve the earlier installation as historical evidence, not current setup or authority to reinstall it.

## Result

The maintained archive preserves useful native tool payloads but does not implement a dedicated skill-activation counter or receive the documented activation telemetry. No payload loss was found in the bounded adapter checks, so no archive parser change was made. The earlier four native compatibility requests were reused; this pass made **zero new Claude/Cursor inference requests** and configured no telemetry destination.

The human's then-requested Claude-first, Cursor-on-quota preference was added to the shared rules, as preserved in [the historical source patch](owned-source.patch). Its installation and preservation are recorded in [the historical installation receipt](installation.json); the rule was subsequently deleted as noted above. Pending skill-source changes remain uninstalled.

## Authority and scope

The human approved items 5.1–5.4 in [the source chat](codex://threads/01a1626c-ec38-7921-bde3-679edf63fa17), turn `01a1698f-6765-7672-a900-c2ca23c52c49`, explicitly requesting that Claude be tried first and Cursor finish after an actual Claude usage limit, with the preference retained for future chats. This existing owner completed only 5.4 and that preference. The source coordinator owns aggregate reporting, account usage and other project work.

Inspection was restricted to maintained code/docs, selected local configuration metadata, owned synthetic records and [the four existing native receipts](../2026-10-23-native-compatibility/README.md). Private archive conversations were not searched or exported. Codex activation completeness, cloud surfaces and account entitlements were not evaluated. No new chats, subagents, capture hooks, backend, automation, paid-provider requests, plan changes, staging, commits or pushes were introduced.

## Signal comparison

| Signal | What the evidence establishes | Limit for counting usage |
| --- | --- | --- |
| Claude `Skill` tool call and launch result | The retained resource request invokes `browser-session` this way. | Both earlier explicit invocations used resource Reads without a Skill call. Tool-call-only totals undercount those observed cases; invocation does not prove the instructions were followed. |
| Native explicit request plus unpredictable asset token | The earlier owned Claude and Cursor fixtures loaded their selected instruction and relative asset. | These controlled witnesses establish those invocations only. Arbitrary asset Reads in real work can serve inspection or reuse and are not a general activation detector. |
| Read of an installed skill body | Cursor's earlier resource request reads the owned body. The archive adapters preserve the content and path in synthetic transcript-shaped records. | A file can be read to inspect or edit a skill. Repeated reads are not necessarily separate activations; frontend injection can produce no body Read. |
| Startup skills/commands inventory | Claude's earlier initialization lists available skills, including uninvoked ones. | Availability cannot be counted as activation. |
| Skill names or slash strings in user prose | The adapters preserve an owned quoted non-invocation fixture. | A mention expresses content or intent, not confirmed activation. |
| Dedicated native activation event | Vendor documentation describes purpose-built events; details below. | Actual export, per-skill identity, completeness, deduplication and local receipt coverage remain unverified. No event was collected in this pass. |

[Receipt identities and extracted tool evidence](prior-receipt-comparison.json) retain the comparison without rerunning native requests. Cursor start/completion rows are grouped by call ID; the extracted tool list uses completion rows only. No cross-surface deduplication or general usage total is claimed.

## Maintained capture and adapter checks

The inspected archive checkout is `/Users/cp/dev/agent-chats`. Its native capture normalizer retains the native row and normalized message content. Claude assistant messages containing `tool_use` blocks receive top-level `event_kind=message`; this is not payload loss. A hypothetical consumer filtering only `event_kind=tool_call` would miss that retained content. Cursor's retained-transcript adapter recognizes `tool_use` blocks as `tool_call` and preserves their inputs. CLI stream JSON and retained transcript JSON are distinct formats; the synthetic checks do not establish that one can be passed directly to the other's adapter.

[Thirteen offline cases](parser-preservation.json) cover Skill/Read payloads, ordinary file inspection, quoted mentions, tool results and inventory. [Inputs](synthetic-inputs.json) are owned synthetic data, not captured private chats. [The bounded checker](check_signals.py) imports pure normalization functions without discovery, reconciliation or writes to the archive. It can be rerun with `python3 docs/audits/evidence/2026-10-23-batch5-activation/check_signals.py` from the repository root when the maintained checkout is available; source hashes identify the inspected versions.

[Code/doc keyword inspection](counter-source-search.json) found no activation-specific counter or OTLP handler in the inspected maintained scripts/docs. The lifecycle hook reads a transcript path and triggers bounded capture; it is not an activation telemetry receiver. [Configuration metadata](configuration-metadata.json) confirms that selected Claude/Cursor lifecycle bindings reference the maintained checkout and that no telemetry environment key names were present in the inspected Claude user settings or this process. This does not audit managed settings, other processes, remote services or vendor-internal telemetry. No endpoint, authentication header, raw hook command or credential value is retained here.

## Documented export paths, checked 23 October 2026

[Claude's monitoring reference](https://code.claude.com/docs/en/monitoring-usage#skill-activated-event) describes `claude_code.skill_activated` for Skill-tool and slash invocations. It carries trigger, source and event sequence. User/plugin names are replaced by `custom_skill` unless `OTEL_LOG_TOOL_DETAILS=1`. Therefore an anonymous activation total and an identifiable per-skill total are different capabilities. Enabling tool details would change exported metadata and was not done here. These are documentation claims, not a successful local export test.

[Cursor's wire reference](https://cursor.com/docs/enterprise/opentelemetry-export/wire#cursorskillactivated) describes `cursor.skill.activated`, with name, trigger and source, plus surface/version metadata. Logs require deduplication by `cursor.event.id`; export has no backfill before activation. The documented slash/attachment omission concerns Grok Bot specifically and should not be generalized to every surface. Runtime coverage for the installed personal CLI remains unverified.

[Cursor's setup reference](https://cursor.com/docs/enterprise/opentelemetry-export) places that server-side destination on the Enterprise plan with team-admin configuration. Availability to the current personal subscription was not established. No upgrade or enterprise export is part of this work.

## Preference and maintenance decision

The rule applies when assigning work across existing Claude/Cursor subscriptions. It preserves useful completed work and an exact public quota/reset receipt before continuing with Cursor. Ordinary work in another harness does not require delegation. Existing authorization, privacy, holds, spending and expiry boundaries still govern continuation. Its installation does not prove future behavioral compliance or exercise an actual quota transition.

Applying the earlier Bitter Lesson checkpoint favors reusing retained evidence and generic capture over a new classifier, mandatory review service or standing evaluation programme. The rule records a deliberate human preference rather than claiming one model is universally better. Added ongoing machinery and provider inference cost for this pass are zero; ordinary Codex execution still consumes its normal allowance. Reconsider the implementation after repeated routing friction, subscription changes or contradictory native evidence, while preserving the human's preference unless they change it.

Longitudinal monitoring remains deferred. If resumed, first validate native activation receipts and identity/privacy settings with owned fixtures before reporting complete usage counts. Existing archive Reads can support explicitly incomplete load evidence. Outcome evidence—correctness, completion time and human intervention—must accompany maintenance decisions; invocation frequency alone cannot justify keeping or retiring a skill. A relevant model/harness upgrade or observed mismatch should trigger renewed checks. No monthly review, automatic retirement or continuous collector was scheduled.

## Validation and preservation

[Baseline](baseline.json), [existing-rule comparison](baseline-rule-comparison.json) and [isolated generated delta](generated-rule-delta.json) establish that only the new preference changes generated content. [Validation](validation.json) records source/catalog checks, all 12 content fixtures, installer regressions, offline adapter checks, local links and whitespace checks. [The scoped source patch](owned-source.patch) isolates this pass from the pre-existing dirty tree. [The installation receipt](installation.json) and [cleanup receipt](cleanup.json) record exact changed destinations, preserved skill/source hashes and removal of task-only temporary files. One watched Cursor CLI configuration hash changed while the task was open; attribution is unestablished, and this pass did not edit or restore it. The receipt records this observation without claiming every settings hash matched.

This completes the bounded signal comparison and preference installation. Reliable end-to-end activation counting, helper execution in restricted modes, the prior reporting overclaim and the longer model-upgrade study remain separate unresolved work.
