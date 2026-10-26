# Native skill compatibility checks — 2026-10-23

## Result and scope

Approved item 4.5 completed a bounded native discovery/resource check and isolated install/uninstall cycle. **Native explicit invocation and relative asset use were observed on both harnesses without skill-body text in the prompts.** Two owned precedence canaries selected the project skill over a legacy Claude command, and the `.agents` copy over the `.cursor` copy in Cursor. These are observations for the tested versions and fixtures, not universal precedence rules.

Browser guidance also loaded through native mechanisms, but **helper execution was not validated**. Claude inspected the helper and declined execution in plan mode; Cursor attempted the owned helper and received a permissions denial. An independent fixture preparation defect is recorded below. No rejected command was rerouted, no permission mode was widened and no actual helper status output is claimed.

All canonical skill bodies and the existing global skill installations remain unchanged. This pass did not repeat the [completed source clarification checks](../2026-10-23-skill-integration/README.md), exercise real browser tabs, or start the longitudinal monitoring programme.

## Authorization and environment

Direct human approval for coordinating items 4.1–4.5 was read in source chat `01a1626c-ec38-7921-bde3-679edf63fa17`, turn `01a1693a-b831-7c92-a3e0-68e1efe083fc`. This existing chat owned only 4.5; product-root reconciliation remained with the coordinator. [The manifest](manifest.json) records scope, initial hashes, versions and constraints.

Four native inference sessions used existing subscription routes: Claude Code 2.1.293 / Opus 5.5 high effort, and Cursor Agent 2026.10.22-27dcf5f / Gemini 4 Argon High. [Authentication checks](auth-precheck.json) confirm first-party Claude subscription auth and availability of the selected Cursor model through its native account route. No direct paid provider API, new credits, overage authorization, global model/billing/plan change, commit, staging or push was used. No quota/reset block occurred.

Claude retained normal subscription authentication and existing permission policy, with session plan mode, prompts denied, six maximum turns, Read/Bash/Skill tools and no MCP servers. The owned project's local setting disabled automatic memory. Installed help says `--bare` requires API authentication and `--safe-mode` disables skills; neither was used. Cursor used ask mode, enabled sandbox, Auto-review, task-scoped trust and the documented `CURSOR_CONFIG_DIR` override. Its disposable configuration retained existing settings/permission controls without copying authentication values into the evidence. Both processes had a 240-second bound; no equivalent native Cursor turn cap is claimed.

## Fixtures and installation lifecycle

[Preparation](prepare.py) used the actual repository installer with explicit owned destination overrides, selecting the browser package and plaintext for Claude and Cursor. Ten copied canonical source/resource files matched their sources. [The fixture manifest](fixture-manifest.json) retains exact installer arguments, unmanaged hashes and canaries; [retained fixtures](fixtures/) show the actual files before native use/uninstallation.

The precedence canaries are disposable aliases of plaintext, not new production skills. Only their `name` changed, and one instruction to read an owned `assets/origin.txt` token was appended. `disable-model-invocation: true` and `allow_implicit_invocation: false` were preserved. A same-named legacy command and a second Cursor skill carried different tokens. Tokens and resource paths were absent from the native requests; [the prompts](prompts/) contain no skill bodies. The uninstrumented plaintext and browser package copies were also installed byte-identically.

[The foreign collision check](foreign-clash.json) aborted with exit 1, preserving the unmanaged plaintext file and leaving the other target uninstalled. [Scoped uninstallation](lifecycle.json) removed managed bodies and resource directories while preserving all four unmanaged files byte-for-byte, including notes beside managed resources. Unmanaged alias canaries remained untouched by the uninstaller. Temporary files were removed only during task closeout.

## Native observations

[Sanitized command/model/exit metadata, actual public tool receipts and outputs](runs/) are retained. Private reasoning was not stored. Native outputs were independently read; self-reported conclusions are distinguished from tool evidence.

| Request | Actual observation | Limit |
| --- | --- | --- |
| Claude explicit plaintext alias | Native `/compat-plain-scope` invocation led directly to a Read of the project skill's relative asset. The output contained its unpredictable token in one four-backtick payload. The legacy command's token was absent. | Tests project skill versus legacy command, not arbitrary personal/project precedence or automatic selection suppression. |
| Cursor explicit plaintext alias | Native slash invocation led directly to the `.agents/skills` alias's asset. Its token appeared in one four-backtick payload; the `.cursor` token was absent. | One observed winner for this CLI/version/fixture; opaque backend context is not fully exposed. |
| Claude browser helper resource | A real native Skill call launched `browser-session`. Actual Bash reads inspected the installed personal helper and the owned fixture path. | The helper itself was not executed. Claude identified that an existing store can create a lock, conflicting with plan mode. Its proposed status JSON was explicitly a guess. |
| Cursor browser helper resource | Actual Read loaded the owned `.agents/skills/browser-session/SKILL.md`, then Shell attempted its relative helper. The receipt returned `Command blocked by permissions configuration`, with `isReadonly: true`. | No helper execution or status output occurred. The final response attributed this to ask mode and quoted a more specific message absent from the receipt; that attribution/quote is not established. |

[The independent assessment](assessment.json) retains these distinctions. Both registry fixture directories stayed empty; no real default registry was queried or mutated.

The preparation script made the harness parent directories 0755 beneath a private 0700 ancestor. The registry helper requires its immediate parent to be private too. [The fixture limitation](registry-fixture-limit.json) records that unmet precondition; it would prevent a runtime-success conclusion even apart from the native mode limits. This was a test-setup defect, not evidence of a broken skill or helper. It was not silently repaired and retried after the denial.

## Implications for usage monitoring

The two tested explicit invocations produced asset Reads without a `Skill` tool call in the retained streams. **A collector counting only that tool call would have missed them.** Conversely, Claude's startup `skills`/`slash_commands` inventory listed skills not necessarily used. Inventory presence is not activation evidence. This is an inference from these actual receipts, not certification of an OpenTelemetry counter or every invocation path.

Before adopting usage counts, verify the native activation signal against explicit frontend invocation, automatic selection and resource reuse. Broader Codex discovery, cloud behavior, same-name global/project combinations, complete activation coverage, browser retention and long-term benefit remain untested here. No new collector, evaluation platform, standing policy or source wording change was added.

## Validation, cleanup and next boundary

[Validation](validation.json) links source-copy equality, explicit-only metadata preservation, native canary evidence, actual helper limitations, unmanaged preservation, global before/after identities and documentation checks. The existing installer regression suite was inspected and its earlier passing results reused; this pass added the actual selected install/uninstall and foreign-clash observations rather than duplicating that suite or claiming a broad installer audit.

[Cleanup](cleanup.json) records task-only trust-marker removal and deletion of the disposable roots, configuration, registries and baseline. No unrelated trust record or installed body was changed. [The existing-file documentation patch](owned-documentation.patch) is scoped against the state at this task's start. The existing [audit report](../../2026-10-07-instruction-and-workflow-audit.md) remains the authoritative record.

The two earlier archive/Triage changes still await global deployment. This pass supports selected native invocation, resource reads and installer preservation; it does not establish helper execution under these read-only modes, correct browser handoff reporting, full compatibility or broad skill effectiveness. Further work should target those specific gaps when they matter, keeping the longer observation programme separate from this completed check.

Documented baselines checked on 23 October: [Claude skills](https://code.claude.com/docs/en/skills), [Cursor skills](https://cursor.com/docs/skills), and [Cursor configuration](https://cursor.com/docs/cli/reference/configuration). Documentation claims were used to choose probes; runtime receipts determine the results above.
