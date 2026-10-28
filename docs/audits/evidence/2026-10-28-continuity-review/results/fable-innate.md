I'll read the supplied skill first.**Disclosure.** I read the supplied `skills/bitter-lesson/SKILL.md` (the summary was sufficient; I did not open the bundled essay). Other visible injected guidance: the harness's general operating instructions and an Ask-mode reminder restricting me to read-only actions, consistent with this assignment. Nothing else was retrieved.

## Outcome sought

A contributor—human or agent—who has never seen the originating chat can resume the work correctly: what the person wanted and how success is judged, which consequential choices were made and why, what constraints and permissions bind, what is done vs. verified vs. open, and where things live. The cost of producing and maintaining that record should be small relative to the cost of losing it.

## Decision criteria

(Deduction.) How much to preserve should scale with four factors:

1. **Reconstruction gap** — how much the work's native artifacts already encode. Code with tests, commits, and PR descriptions encodes a lot; an exploratory research thread or a console-driven ops change encodes almost nothing.
2. **Stakes and irreversibility** of the decisions involved.
3. **Handoff probability** — likelihood that a fresh session, another harness, or another contributor picks it up.
4. **Who reads it.** If only agents read, judge by recovery success, not legibility rituals; if a human reads, legibility has independent value (the skill's "human-facing board" point).

A practical test for the first factor: "If this chat vanished now, what would a competent newcomer get wrong from the artifacts alone?" That answer is what should be written down, and little else.

## Recommended approach: outcome-stated, method-free, native-medium

Ask agents for a durable record of what native artifacts don't already carry, written where the next worker will naturally look, at consequential moments rather than continuously.

Content (not format):
- **Intent**: objective and success criteria in the person's words, including explicit non-goals.
- **Decisions**: consequential choices with a one-line reason; rejected alternatives only when the choice is non-obvious.
- **Constraints and permissions**: human-stated, visibly separate from agent inferences, never edited by agents without the human.
- **State**: done / verified / unverified / blocked / next step.
- **Pointers**: locations of artifacts, not copies.
- **Hazards learned**: gotchas that cost time.

Triggers: a consequential decision is made, a constraint is learned, before an irreversible action, before stopping. Not per-turn journaling.

Medium: whatever the work already uses—commit messages plus a short doc in a repo; a notes file alongside research outputs; a ticket or runbook for operations. One conventional entry point per unit of work so discovery isn't a problem. Prefer updating over appending so the record stays small and current.

Structure gradient:
- **Low** (reversible, single-session, well-encoded by artifacts): nothing beyond native artifacts.
- **Medium**: a short handoff note at checkpoints.
- **High** (irreversible, multi-contributor, poorly encoded): explicit decision entries, a constraints section, verification state, possibly a human-reviewed summary.

## Bitter Lesson lens

The skill asks whether a prescription compensates for model limitations or encodes a fixed theory of how work proceeds. Recoverable state is neither: it addresses a structural fact—context is not shared across sessions, harnesses, or contributors—that capability growth does not remove. (Prior-knowledge claim: agent sessions do not persist working context by default; harness-specific memory features exist, but their cross-harness portability would need verification.) The skill says to evaluate shared state and recovery on operational benefits, which fits here.

What *does* change with capability is how much must be written. More capable agents reconstruct more from artifacts and compress better, so the record shrinks toward intent, constraints, and the non-obvious "why". That argues for stating the outcome ("a newcomer must be able to resume without the chat") and letting the agent choose form, rather than mandating templates, planning sequences, or a scribe role. A fixed template is a workaround worth imposing only when agents demonstrably fail to judge what matters—and it should carry a removal condition (e.g., a model upgrade followed by a re-test).

## Where this depends on assumed capability

The light version assumes agents can (a) recognize consequential moments, (b) compress faithfully without inventing decisions, (c) read and honor an existing record rather than re-deriving, and (d) maintain rather than only append. Uncertainty: I don't know how reliably current models do (a) and (d); that is the main thing to test. With weaker agents, add explicit triggers ("before ending, update X"), a fixed location, and a short template. With stronger agents, the outcome statement suffices. Work type matters independently of model: ops and multi-contributor work sit high on the gradient regardless.

## Strongest alternative

Do nothing beyond native artifacts and rely on capable reconstruction—the pure general-method baseline. It is cheapest and immune to record rot. It fails on one thing: "why" isn't recoverable from "what". Intent, rejected alternatives, and human-granted permissions are not in the code or the output. (Deduction.)

A second alternative—export full transcripts and let future agents search them—preserves everything but is costly to read, drags harness-specific noise across tools, and buries permissions in chatter. Heavier frameworks (memory systems, structured ledgers, a dedicated scribe agent) I would reject as a default; justify them only on observed recovery failures, not anticipated ones.

## Main failure modes

- **Record rot**: stale notes mislead more than no notes. Mitigate by dating entries, marking provisional items, updating rather than appending, keeping it small.
- **Ceremony creep**: agents write long status documents every turn. Mitigate with consequence-tied triggers, a size budget, periodic pruning.
- **Confabulated history**: a summary records a decision or approval that wasn't made. Mitigate by keeping human-stated constraints in a human-controlled section; records describe, they don't grant authority.
- **Unread records**: the next agent doesn't look. Mitigate with one conventional entry point, referenced in kickoff.
- **Over-trust**: the next agent treats the note as truer than current reality. The note should say what to verify against.
- **Portability**: harness-native memory doesn't travel; plain files in the work's own location do.

## Evidence that would change my view

Proposed test (unrun): on representative tasks across work types, run each with and without a handoff note; have a fresh session or different harness resume; measure resumption correctness, time to productive work, human clarifications needed, and constraint violations, with comparable total resources. If artifacts-only resumption matches note-assisted resumption for a work class, drop the note there. If notes are frequently stale or ignored, fix triggers or location before adding structure. If failures concentrate in one class, add structure only there. Reconsideration triggers: model or harness change, adding contributors, repeated recovery friction, or a case where a note caused harm.

## Name

Keep the ordinary term **"handoff note"** for the artifact (borrowed from shift handoffs in operations and clinical practice—prior knowledge that such practices exist; I'm not claiming a specific protocol transfers) and **"recoverable state"** for the property. "Decision record" already exists for the high end. Avoid coining a framework name; it invites the ceremony the skill warns against.

## Claim types

Prior knowledge: Sutton's argument; existence of decision-record and handoff practices; session context non-persistence; LLM summaries can confabulate. Deductions: why ≠ what; structure scales with stakes × handoff probability × reconstruction gap. Assumptions: agents can write to a persistent location; the person occasionally reviews. Uncertainty: reliability of agents' consequence-judgment and maintenance behavior; portability of harness memory features—both need verification.