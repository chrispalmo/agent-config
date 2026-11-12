# Chat closeout consolidation and comparison

13 November 2026, Asia/Bangkok. The user requested investigation of unsupported readiness in [agent-config - Phone frame skill](codex://threads/01a1d0e3-6e7a-7f23-a08e-a779bf9382b2), then approved consolidation, corrected completion criteria, testing, and installation across all local agents in [the source chat](codex://threads/01a1d0f2-92b9-7140-ba78-9ec33ba31610).

## Decision and scope

Use one [Chat Closeout](../../../../skills/_collections/coordination/chat-closeout/SKILL.md) entrypoint for read-only state questions and requested execution. Retain the two visible leave/start-new-topic and archive readiness statuses. Bare invocation resolves authorized work; actual archive execution still requires that action to be requested. Retire Chat State from the active catalog and owned installed copies, with no compatibility wrapper or new standing rule.

The observed failure was declaring installation complete and treating unrequested Git synchronization as unnecessary, then relying on the same completion record and installation hashes to repeat YES. Required outcomes and permission to execute them must be assessed separately. Repository closeout normally covers accepted task commits and intended integration/synchronization, unless a different endpoint was explicitly chosen or continuation effectively transferred. Unrelated dirty files do not block the task. Required work without authority remains open, and evidence must establish the actual outcome claimed.

The Bitter Lesson comparison prioritizes unsupported clearance, unauthorized effects, completed authorized work, human intervention, and useful recovery over elaborate process. The alternative baseline is an agent using ordinary outcome instructions and raw evidence. A single short skill retains user-specific readiness and completion expectations; the earlier two-entry interface has no demonstrated independent-verification benefit. Reconsider the retained detail after this comparison or another false verdict; remove prescriptions that add no observed benefit. This does not start ongoing evaluations or reopen the broader deferred audit.

## Preserved sources and experiment

[Before sources](source-before.json) retain exact hashes of the previous entrypoints and UI metadata under `before/`; [the candidate](candidate/chat-closeout/SKILL.md) records the evaluated consolidated source. The 9 November trial and dated receipts remain historical evidence. The former canonical Chat State link is redirected to the retained source rather than a broken path.

[Acceptance criteria](grading.md) were written before dispatch. Three independent agents receive the same seven isolated cases: minimal outcome instructions, prior two-skill guidance, and the consolidated candidate. Each case supplies original messages, project policy, files, Git repositories with local bare destinations, and a fixture host with controlled sync/archive operations. No production service or real chat is changed. Agents receive no expected answer, suspected defect, source-chat history, or other condition's results. Evaluators may perform authorized fixture commits and local synchronization but cannot change Git configuration or inspect other runs. Raw [cases](fixtures/cases.json), [host adapter](fixtures/host.py), [assignment](fixtures/assignment.txt), and [initial hashes](initial-state.json) preserve the setup.

## Observed results

| Condition | Cases meeting the pre-run criteria | Unsupported clearance | Protected/read-only state and authority checks |
| --- | --- | --- | --- |
| [Minimal instructions](results/baseline/output/summary.md) | 6 of 7 | Installed source committed locally, synchronization declared outside scope, YES/YES. | Passed |
| [Previous two skills](results/existing/output/summary.md) | 6 of 7 | Same unpublished-source failure; the completion record was committed but sync remained dismissed. | Passed |
| [Consolidated skill](results/candidate/output/summary.md) | 7 of 7 | None in these cases; unpublished source remains NO/NO pending a concrete synchronization decision. | Passed |

The [independent parent verification](behavior-verification.json) checks actual file hashes, Git commits and destination references, syntax, unrelated notes, host attempts, and assessment-only state. All conditions completed the explicitly authorized commit/sync/archive case and preserved local-only outcomes, unrelated edits, accepted transfer and the human pricing hold. All recognized the failed sync and missing history. The candidate correctly committed task source and prepared the missing sync decision without inventing permission or dropping the requirement. Exact user-facing outputs and their hashes are retained as strings in each `raw/outputs.json`; readable copies normalize greetings, links, and Markdown line-break syntax only. The destination folders under results retain reference evidence only, not live Git repositories.

This is a bounded observation: one independent agent per condition, seven cases grouped per agent, no repetition, no real remote service or native archive action, and no cross-harness behavioral comparison. Host behavior is stipulated by fixtures. The result supports the explicit completion-boundary correction here; it does not establish universal reliability or prove that one entrypoint alone caused the improvement. Source wording fell from 2,058 to 1,040 whitespace-delimited words. No new reviewer role, compulsory invocation sequence, or recurring evaluator was added.

## Validation and installation

The exact publication tree also passed content validation (22 skills; unrelated pending design/security skills excluded), the same 55 regressions, and the installer suite. New/changed prose links resolve. Task source whitespace checks pass; the retained historical continuity patch intentionally preserves Git context-line spaces.

The skill validator, repository content validation (24 skills, zero drafts, 12 rules), all 55 content/rule-reference/Cursor-context/external-source tests, the isolated installer suite, affected prose links, retained-source hashes, and whitespace checks passed. The installer regression now exercises package preservation followed by ownership-aware retirement, preserving foreign content and unrelated local notes.

The [global installation receipt](installation.json) verifies Cursor/Codex's shared root and Claude Code's root. All 30 package source-file comparisons and 12 ownership records match, with exact installed file sets. Four files changed (the entrypoint and UI metadata in both roots); eight owned Chat State files were removed; 1,299 other preexisting installed files/links were unchanged. The old native Codex/Cursor locations also contain no Chat State entrypoint. Other coordination members already matched source, and no rules were refreshed. Normal automatic selection remains enabled. Fresh-session activation and native behavior in each harness remain untested; the current conversation can retain its startup inventory until refreshed.

## Repository closeout

Implementation, the bounded comparison, source checks, and authorized global installation are complete. The task-scoped source and evidence have been prepared and validated independently of unrelated pending edits. Remote synchronization still requires explicit authorization under the repository rule. That obligation remains here and is not waived by completing installation. No actual archival, new schedule, external messaging, or production service mutation was requested or performed. The source chat owns the final synchronization decision and verification; no continuation is claimed elsewhere.
