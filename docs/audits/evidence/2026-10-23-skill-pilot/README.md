# Skill behavior pilot — 2026-10-23

## Executive summary

Completed the bounded seven-skill comparison using native Claude Pro / Opus 5.5 and Cursor / Gemini 4 Argon. There are **28 primary decision artifacts across 14 enabled/baseline pairs**, plus **seven completed follow-up sessions** for capture recovery and candidate checks. One earlier Cursor launch stopped before inference at workspace trust. No provider API SDK, new credits, overage authorization, paid evaluation service, global installation, or product change was used. No quota/reset block was observed; remaining account percentages were not queried by this stream.

Guidance improved two tested behaviors: Triage answered the speculative tracker question instead of merely recapping it, and Browser Sessions supplied a usable native fallback when shared registration was unavailable. Several simpler baselines already satisfied the tested contracts. The archive cases exposed unsupported conclusions from a metadata-only title; a narrow candidate avoided that inference on both routes. A Triage prepared-brief permission ambiguity deserves clarification, but its exact failure did not fully repeat. Three candidate patches were prepared at this pilot's close. No skill retirement is justified by this small sample.

Updated: **2026-10-23 02:10 +07**. Native inference and artifact review are complete. The existing audit report remains the authoritative work/decision record.

**Later source integration:** The [2026-10-23 follow-up](../2026-10-23-skill-integration/README.md) integrated the archive and Triage clarifications into canonical source, with actual fixture archive queries and six native forward checks. Global installations remain unchanged; the Bitter Lesson wording candidate remains unapplied. The observations and frozen inputs below describe the original pilot.

## Authorization and frozen scope

Direct human approval was verified in source chat `01a1626c-ec38-7921-bde3-679edf63fa17`, turn `01a164e4-5130-7043-91ef-64ae7b5f6fcc`: tasks 2.1–2.4, existing subscriptions only, coordination through existing chats, all holds preserved, clean reviewable work. No new chats, extra agents, recurring monitors, global installation, release work, protected device/database operation, or unrelated archive/browser record was part of this pilot.

The current catalog has 16 skills. The selected seven canonical sources remained equal to their frozen snapshots, and source bodies are present in both installed roots; see [source reconciliation](source-reconciliation.json). This is not an audit of every supporting resource or discovery path.

## What was actually compared

Each skill has a supplied synthetic task with consequential scenarios, a matched baseline prompt and a prompt injecting its frozen source guidance. [Cases and the separately retained rubric](cases.json), [manifest and source hashes](manifest.json), [output index](outputs.md), [independent assessment](assessment.json), and [native receipts/usage](run-summary.json) are retained. The evaluated harnesses were not asked to score themselves. Exact ledger targets and cleanup closure decisions were checked structurally; the remaining findings come from independent reading of the public artifacts against the rubric.

Claude pairs use the same Opus 5.5 high-effort route, safe mode, no tools, read-only permission mode and MCP exclusion. Managed policy remains in force. The injected workflow text is the treatment; this does not test native skill selection.

Cursor pairs use the same Gemini 4 Argon route, ask mode, enabled sandbox, Auto-review, scoped native trust and owned synthetic workspace. Baselines omit inline injection; global discovery may still expose skill metadata or guidance. No full-absence claim is made. Receipts show **zero tool calls** for the completed Cursor runs. Full opaque provider/system context is not exposed and is not claimed identical beyond the controlled inputs and native settings.

All cases prohibit tools and use supplied material. Final JSON decisions are observable artifacts, **not proof that proposed file edits, browser closure, dispatch, archive search, or integration steps were executed**. The archive source fixture is retained at [canonical synthetic events](fixtures/archive/A.jsonl). No live archive coverage was inspected.

## Findings and dispositions

| Skill | Observed result | Proportionate recommendation |
| --- | --- | --- |
| Status Ledger | Both routes, with and without injection, reused the named store, preserved the release hold, recorded only the supplied 84-test evidence, and left status-only exchanges unchanged. | Keep provisionally. This straightforward case establishes no incremental benefit; difficult resumptions remain useful future cases. |
| Concierge | Both conditions chose the existing CSV and stopped without implementation or retained exploration. Cursor enabled output was 2,352 characters versus 837 in baseline, including procedural non-actions. | Preserve proportionate one-turn/stopping behavior. Substantial preparedness value was not tested; avoid adding more reporting ritual on the strength of this case. |
| Triage | Both enabled routes answered the tracker/board question substantively; both baselines largely recapped/deferred it. The original Cursor enabled brief also described diagnostic execution as authorized under a proposal-only request. | Keep substantive coverage. Review the explicit prepared-brief boundary candidate; repeated current output was narrower, so a robust fix is not established. |
| Bitter Lesson | Both conditions rejected unsupported reviewer ceremony, preserved normal permissions, and recognized specialization backed by distinct tools and observed benefit. Enabled outputs repeated unclear shorthand for an unperformed test. | No broader effectiveness claim. Consider the narrow plain-language candidate; do not add a new mandatory checkpoint. |
| Browser Sessions | Both routes protected the human tab. Injection supplied native fallback for unavailable grouping/registry instead of blocking registry-dependent work or inventing a substitute store. Cursor still assumed an unconfirmed native retention control. | Keep the fallback. Test an explicit missing-retention-control case before asserting integration reliability or adding another instruction. |
| Browser Cleanup | All four primary outputs selected initial candidates 101/102 and final closure 101 after changed live state, and avoided lease renewal or preview mutation. | Keep ownership and safety controls. Existing helper tests corroborate local invariants, not real browser UI behavior. |
| Search Agent Chats | Both conditions preserved the human hold, citation and coverage limits. Enabled outputs inferred brainstorm status from a metadata-only title; the repeated Claude control did too. Candidates on both routes left contents/decision status unknown. | Review the narrow metadata limitation candidate. Real capture, retrieval and cloud coverage remain outside this fixture test. |

These are single-task comparisons with a few targeted follow-ups. Response length and elapsed times are observed overhead, not controlled performance estimates or proof of harm. The [output index](outputs.md) shows measurements per primary output; native reported token categories remain separate by harness. List-price estimates in receipts are **not bills**.

## Candidate patches and follow-up evidence

At the original pilot's close, all were isolated proposals under `candidates/`; canonical skills and installed guidance had not been modified. See the later source-integration update above for current status.

| Candidate | Evidence | Status |
| --- | --- | --- |
| [Archive metadata limits](candidates/search-agent-chats-metadata-limits.patch) | Repeated current Claude output and original Cursor output inferred contents from the title; one candidate output per route explicitly left those contents unknown. | Targeted fixture benefit observed; small sample; unapplied. |
| [Triage proposal-only execution boundary](candidates/triage-proposal-only-execution.patch) | Original Cursor boundary overreached; repeat was narrower; candidate expressly denied both dispatch and recipient execution. | Clarity improvement, not a demonstrated robust behavior fix; unapplied. |
| [Bitter Lesson plain test status](candidates/bitter-lesson-plain-test-status.patch) | Both enabled outputs reproduced the wording previously questioned by the human. | Wording-only candidate; no behavioral candidate run; unapplied. |

Each patch passed `git apply --check`. [Assessment details](assessment.json) retain the counterevidence and limits. No permission, approval, hold or verification requirement was removed.

## Validation and recovery

The 28 primary artifacts parse as JSON. Eight exact ledger/cleanup target checks passed. The [validation receipts](validation.json) record content validation for 16 skills/ten rules, all 12 content fixtures, installer regressions, all 16 browser registry tests and whitespace checks. Initial content commands used a Python without validation dependencies and stopped; reruns using the existing repository virtual environment passed without installing packages.

The first Cursor launch stopped at native workspace trust. The successful route used only an owned fixture directory, normal scoped `--trust`, ask mode, enabled sandbox and Auto-review; no force/yolo or blanket MCP approval. Its one matching task trust marker and disposable workspace were removed after verification; [cleanup receipt](cleanup.json) records the exact scope.

Claude's single-result JSON route retained only the continuation tail for one long Triage answer. That receipt and exposed tail are preserved and excluded from the primary comparison. Both Triage conditions were repeated through public-message streaming; private reasoning blocks were omitted. Later native receipts retain public outputs and scalar usage only. This was a capture recovery, not evidence that the model itself produced only the tail.

Claude settings, Cursor hooks and Codex configuration hashes stayed equal to the initial snapshot. Cursor CLI's whole-file state hash changed during native use; the initial per-section snapshot was unavailable, so the pilot does not attribute every state-file change. Per-section before/after hashes for targeted follow-ups show stable non-authentication/non-privacy sections. The runner issued no billing, permission-default or global installation command.

## What remains outside this completed pass

The three-to-six-month observation proposal, passive telemetry collection, major-model-upgrade comparisons, statistical performance conclusions, native activation/discovery reliability, live browser/archive integration and deployed candidate effectiveness were not completed or scheduled here. Required holds and existing user preferences remain authoritative. The next useful work is review of the narrow archive clarification and selected realistic difficult cases, rather than building a larger standing evaluation system from these results.
