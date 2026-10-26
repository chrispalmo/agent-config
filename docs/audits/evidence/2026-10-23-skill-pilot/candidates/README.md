# Candidate skill clarifications

## Executive summary

Three narrow patches were prepared at the initial pilot's close and passed `git apply --check` then. The later [source-integration follow-up](../../2026-10-23-skill-integration/README.md) applied the archive and Triage candidates to canonical source. Global installations remain unchanged, and the Bitter Lesson wording patch remains unapplied. The behavioral evidence below is from frozen inline guidance, not installed candidate skills.

| Candidate | Rationale | Evidence and limitation |
| --- | --- | --- |
| [Archive metadata limits](search-agent-chats-metadata-limits.patch) | A title or metadata-only hit cannot establish contents or accepted decisions. | Current enabled Claude twice and original Cursor inferred brainstorm status; one candidate output per route left contents unknown. Small synthetic sample only. |
| [Triage proposal-only execution](triage-proposal-only-execution.patch) | A prepared proposal must not grant recipient execution authority. | Original Cursor boundary overreached, but a repeated control was narrower; the candidate explicitly denied dispatch and execution. Clarity proposal rather than proven robust fix. |
| [Plain test status](bitter-lesson-plain-test-status.patch) | Use an explicit statement that a proposed test has not been performed. | Both enabled native outputs repeated shorthand the human had questioned. No behavioral candidate rerun; wording-only proposal. |

See the [independent assessment](../assessment.json), [native output index](../outputs.md), and per-candidate validation receipts. No patch weakens permission, hold, review or verification requirements.
