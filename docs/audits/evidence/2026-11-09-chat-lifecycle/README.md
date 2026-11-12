# Chat lifecycle trial and installation

9–10 November 2026, Asia/Bangkok. The human chose to try the two-skill system after discussing a single-entry alternative, then requested installation followed by chat-state, chat-closeout, and another chat-state. The skills are canonical members of the coordination package and installed for Codex, Cursor, and Claude Code. The [initial installation receipt](installation.json) records the 9 November sources; the [continuity refresh receipt](continuity-refresh.json) records current hashes and the two approved additions installed on 10 November. Source changes remain local and uncommitted; no publication was requested.

The two-skill interface below was superseded by the [13 November consolidation](../2026-11-13-chat-closeout/README.md). Current [Chat Closeout](../../../../skills/_collections/coordination/chat-closeout/SKILL.md) handles both assessment and execution. The [last Chat State source](../2026-11-13-chat-closeout/before/chat-state/SKILL.md) and [last two-skill Chat Closeout source](../2026-11-13-chat-closeout/before/chat-closeout/SKILL.md) are retained for history; they include the 10 November additions. The original three-status trial sources under `tested-skills/` and their hashes in [verification.json](verification.json) are unchanged. Subsequent source revisions do not imply that the historical behavioral trial was rerun.

The later [repository continuity clarification](#repository-continuity-and-handoff-clarification---2026-11-09) is accepted and recorded below. The human approved both wording additions and installation on 10 November; the [adoption and refresh](#adoption-and-refresh---2026-11-10) is complete. No integration decision remains open in this lifecycle scope.

## Installation and live closeout

Promoted the accepted sources into the coordination collection, registered both skills and their package membership, updated active documentation and package tests, and removed the obsolete draft locations and overview. The existing package installer is the narrowest supported selection: its five previous members already matched both installed roots. Installation added 16 files for the two new skills; all 1,272 pre-existing installed files/links in the checked roots remained unchanged. Entrypoints, UI metadata, and ownership receipts match canonical source in both roots. No standing rules changed.

Both skill validators, content validation (23 skills, one unrelated draft, 12 rules), all 55 repository tests, and the isolated installer suite passed after integration. These checks establish source/package/install consistency. A refreshed native picker session was not tested, and this does not establish cross-harness behavioral reliability.

The first requested state check reported leave/reuse and archive NO while the requested closeout remained unfinished; no human input was needed. Closeout preserves installation evidence here and in the existing [project audit record](../../2026-10-07-instruction-and-workflow-audit.md#chat-lifecycle-installation-and-closeout---2026-11-09), reconciles historical draft links, and retires the owned temporary trial and install snapshots after preserving their useful evidence. The three trial agents are complete; no attachments or local automation references to this source chat were found. Native Codex tools support listing and restoring archived chats. No actual archive, read-state change, delegation, schedule, commit, or push is part of this closeout.

The original trial's limits below remain evidence limits, not newly assigned work. Source and validation records are discoverable from the coordination overview and the project's existing audit workflow. Their presence on disk does not establish an independent backup. Publication remains optional and unrequested; unrelated title, security-review, and design-draft changes remain outside this work.

## Repository continuity and handoff clarification - 2026-11-09

The human corrected the claim that a standing chat owns continuity: **the repository owns continuity**. Standing chats are replaceable entry points for coordination. Necessary responsibility/work state must support resumption from repository records in a replacement chat or another harness; a transcript is not the authoritative continuity store. The human also wants a concrete question when substantive proposed work needs disposition to resolve a real loose end. That does not require acknowledgment of completed work or a decision on every optional idea, and silence grants no authority.

Authority was checked against original messages in [agent-config - maintain](codex://threads/01a17760-afea-7330-bf7f-5419e2a007ae), including the approval to hand off this clarification and the explicit instruction to leave the radar deferred. The [lifecycle work owner](codex://threads/01a1b6f1-813b-7480-a518-5834ba591d45) accepted assessment, preservation, and any integration proposal. The initial handoff held source adoption and reinstallation pending a decision. The human's direct approval on 10 November authorized both additions and refreshing installed skills. No new standing rule, publication, chat creation, or external model run was requested.

The assessment prioritizes resumption without the original chat/harness, clear decisions on consequential loose ends, and minimal added process. At the 9 November assessment, canonical entrypoints matched the installed Codex/Cursor and Claude Code copies and the initial installation hashes. Static inspection found:

| Requirement | Existing guidance | Remaining gap |
| --- | --- | --- |
| Repository owns continuity | Chat State requires discoverable durable records; Chat Closeout preserves necessary state in existing authoritative project records. | Repository authority and recovery by a replacement chat or another harness are implicit. Archive readiness can otherwise be read as relying on retrievable chat history. |
| Concrete question for a real pending disposition | Both distinguish required input from optional suggestions; closeout explains missing decisions and preserves holds. | The report can list a human action without asking the concrete decision question the human requested. |
| No invented commitment or approval | Chat State rejects silence as approval and forbids making rejection of unselected ideas a closure condition. | Already explicit; preserve it. |

### Approved source wording

Added this paragraph verbatim to Chat State's **Establish scope and evidence** section after reconciliation with project records on 10 November:

> For repository work, the repository's designated records own continuity; standing chats are replaceable coordination entry points. Check that necessary decisions, work state, evidence, and next actions are recoverable from those records by a replacement chat or another harness. The transcript may supplement those records but must not be required to resume the work.

Added this paragraph verbatim to Chat State's **Report for action** section:

> When a substantive proposal needs the human's disposition to resolve an existing loose end, ask a concrete decision question, such as “Do you want me to hand these off now?” Distinguish this from optional ideas, which need no response, and completed work, which needs no acknowledgment. Silence does not authorize the proposed work.

Both additions are in the existing shared criteria; Chat Closeout already incorporates that authority and its body is unchanged. No second implementation, standing rule, automatic footer, timer, or new task store was added. The first paragraph is an assessment requirement, preserving Chat State's read-only boundary. This wording comparison is not a behavioral test or proof of improved reliability.

### Continuation and holds

**The integration decision is resolved and the authorized work is complete.** The human explicitly approved both additions and installation; this was not inferred from silence. No required human or agent action remains assigned to the lifecycle clarification. This record is discoverable through the coordination overview and existing project audit links; a replacement agent can recover the decision, implemented wording, installation evidence, and limits here without requiring the source maintain chat to remain visible.

The lifecycle work maintainer completed the source update, affected checks, and narrow supported refresh described below. Commit and push remain unrequested. The central audit was left to the coordinator during the initial follow-up; its lifecycle assignment now points to this verified completion. No reply back to the source chat is required.

The separate [Model selection and review pilot](codex://threads/01a1c125-bd33-7b50-86a9-71fd3629e7fc) owns model identity/control, dated recommendations, and the model-adoption review proposal. It is not supervised by this clarification. The radar remains explicitly deferred: no schedule, monitor, or rollout. The initial 9 November follow-up changed only this evidence record; the approved 10 November changes are recorded next.

### Adoption and refresh - 2026-11-10

The human requested both additions, refreshing the installed skills, the exact changes, and another chat-state assessment. The [exact source diff](continuity-additions.patch) contains only the two approved paragraphs. Descriptions, UI metadata, catalog membership, and Chat Closeout's body remain unchanged; it reads Chat State's shared criteria. Reviewed the added recovery requirement alongside the read-only boundary and the existing distinctions between required human input, optional ideas, authorization, and completion.

The skill validator, content validation (23 skills, one unrelated draft, 12 rules), all 55 repository tests, and the isolated installer suite passed. Refreshed the coordination package for Codex, Cursor, and Claude Code using the supported package installer. The [refresh receipt](continuity-refresh.json) verifies matching entrypoints, UI metadata, and ownership receipts in both installed roots. Of 1,294 pre-existing installed files/links checked, only the two installed Chat State entrypoints changed; the other 1,292 were unchanged and no files were added. No rules were refreshed.

Source changes and this record remain local and uncommitted. The original synthetic trial and initial installation hashes remain historical evidence; no new independent behavioral trial or native picker discovery test was performed. The requested final chat-state assessment follows installation and record verification. No actual archive, read-state change, new handoff, scheduled follow-up, commit, or push is part of this work.

## Candidate and scope

The tested [Chat State](tested-skills/chat-state/SKILL.md) assessed human and agent obligations and gives separate verdicts for leaving/reusing, archiving, and deleting. The tested [Chat Closeout](tested-skills/chat-closeout/SKILL.md) included that assessment and completes or externalizes authorized work. Chat State owns the shared readiness criteria. Both preserve the distinction between all agreed work being complete and remaining work having effective continuation elsewhere.

At the original trial, the skills were uninstalled drafts, outside both catalogs. Their descriptions permit ordinary discovery after a future installation; no explicit-only policy was introduced. Natural-language readiness questions remain read-only, and a preparation request does not authorize actual archiving/deletion. Closeout carries existing authority without expanding it. Both can address a requested project/global scope, but coverage is limited to accessible chats and relevant dependencies.

Criteria were no lost commitments, supported action verdicts, effective ownership and discovery after transfer, independent preservation before deletion, and low attention/maintenance cost. The shared state is ordinary project records; no registry, telemetry, timer, backend, or automatic status footer was added. Reuse does not erase model context.

## Method and observations

Three fresh subagents received the draft entrypoints and synthetic raw fixtures, without the parent conversation, expected answers, or grading criteria. One performed read-only assessment; two performed closeout in isolated temporary projects. The latter could update project records and preserve artifacts but could not operate real chats, repositories, services, or external messaging. Each fixture supplied a fictional host contract: project storage survives deletion, while chat history and session attachments do not. This establishes nothing about real host deletion behavior.

| Case | Observed result | Parent review |
| --- | --- | --- |
| Standing responsibility with an accepted release owner, human pricing gate, and chat-only approved artifact | [Leave/reuse YES, archive YES, delete NO](cases/standing/output/result.md). Remaining work stays visible; optional loyalty idea and unrelated dirty file were not made blockers. | Correct distinction between readiness and completion. Approval artifact and deployment hold must survive independently before deletion. |
| Task with tests reported passing, incomplete integration, unapproved preview, failed push and failed handoff | [All three readiness verdicts NO](cases/integration/output/result.md). Corrected [the task record](cases/integration/project/tasks.md), preserved the human hold and source-chat ownership, and did not retry external actions. | Correctly rejected the assistant's false completion statement and exposed inadequate preview evidence. A record alone did not become an accepted transfer. |
| Selected design whose comparison, decision and SVG existed only in chat | [All three verdicts YES after preservation](cases/preservation/output/result.md). Wrote [the decision](cases/preservation/project/design-decision.md), copied the SVG, and linked them from the normal project entry point. | Verified byte-equal SVG, valid XML, source/authority distinctions, and independent discovery. Comparison claims remain qualitative rather than invented measurements. |
| Older research with unavailable prior history and missing resource/attachment inventory | [All three verdicts UNVERIFIED](cases/preservation/output/result.md). The known assistant “safe to delete” claim was insufficient; the evidence gap was recorded outside chat. | Correctly avoided turning missing coverage into clearance or inventing follow-up. |

The parent read the actual results and changed records and independently checked the saved asset, relative links, selected unchanged files, and corrected task status. [Verification data](verification.json) records these checks and the tested skill hashes. The retained cases contain synthetic inputs and resulting project files. [The two changed initial records](before/) preserve their pre-closeout contents. Outputs were normalized only for human names and machine-specific paths so evidence links work after moving out of temporary storage.

### Procedural deviation

The integration evaluator self-reported briefly creating a hash-baseline file outside its permitted `project/` and `output/` subfolders, then removing it. It remained within the isolated test area, and no such file remains. The lasting mutations were the permitted task record and result. This is a test-boundary compliance failure despite correct readiness decisions; the trial must not be described as an unqualified pass. No production action or real conversation mutation occurred.

## Validation and limits

Both skill-creator validators passed. Repository content validation accepted 21 active skills, three drafts including one unrelated existing draft, and 12 rules. The 18 content, 12 rule-reference, six Cursor-context, and 19 external-skill tests passed (55 total), as did the isolated installer suite and whitespace checks. These checks cover packaging and existing regressions; they do not validate conversational judgment. Installation into temporary test roots is not global installation.

This is one run of four synthetic cases with no baseline, repetition, or cross-harness comparison. The two-chat preservation case exercises a selected-set workflow, not an exhaustive live global sweep. No real dispatch, merge, push, deployment, archive, or deletion was tested. The reports expose the requested verdicts prominently, but reading time and brevity were not measured. Actual host resource/deletion behavior, native skill discovery, and reliability on long live histories remain untested.

At the original trial's closeout, source was local and uncommitted, nothing was globally installed or published, and integration, installation, and live closeout were unselected follow-on proposals. The later installation and live-closeout scope is recorded above. Revisit the design after a missed commitment, false readiness verdict, ineffective handoff, or repeated report noise; no scheduled evaluation was created.
