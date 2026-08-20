---
name: reverse-brief
description: >-
  Ends a context-gathering interview and shows the user the facts, inferred insights, unresolved questions, and exact handoff that will guide the originating workflow. Use when the user invokes reverse-brief directly. Do not run unless invoked.
disable-model-invocation: true
---

# Reverse Brief

Turn the conversation into an inspectable handoff before another skill or task continues.

This is the bundled closing workflow for `interview`, but it may also be invoked directly for the current decision or task.

## Start

1. Stop the active interview. Do not ask another question round.
2. Infer the interview subject and originating skill or task from the conversation.
3. Use all relevant context, including statements made before the interview.
4. If no interview is active, reverse-brief the current decision or task.

## Evidence rules

- Do not invent an answer for anything the user skipped.
- Separate the user's stated facts and preferences from your interpretations.
- For each derived insight, state the evidence or reasoning behind it.
- Label uncertain interpretations with `Confidence: low`, `medium`, or `high`.
- Surface contradictions, tensions, and material unknowns explicitly.
- Distinguish recommended defaults from decisions the user has confirmed.
- Preserve important wording when paraphrasing could change intent.

## Output

Use this structure:

```markdown
# Reverse brief: [subject]

## Confirmed understanding

- Goal:
- Success criteria:
- Scope:
- Non-goals:
- Constraints:
- Preferences:

## Conclusions and insights

1. **[Conclusion]** — [evidence or reasoning]. Confidence: [level].

## Unresolved

- **[Question or tension]** — [why it matters].

## Proposed defaults

- **[Default]** — [why it is reasonable and what would change it].

## Handoff to [originating skill or task]

- [Concrete instruction or context that the workflow should use]
```

Omit empty fields and add subject-specific fields when useful. Keep the handoff
compact enough to act as working context, while retaining decision-critical
details.

## Confirmation and continuation

Show the reverse brief before feeding it to the originating workflow.

- If the user corrects it, revise the brief before continuing.
- If the user says to continue, resume the originating skill or task using the revised brief as authoritative context.
- If the user explicitly requested immediate continuation, show the brief and then resume in the same response.
- If there is no originating workflow, ask what the user wants done with the brief.
