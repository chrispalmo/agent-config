---
name: reverse-brief
description: Present the confirmed facts, interpretations, unresolved choices, and actionable handoff for a decision or task when the user explicitly invokes reverse-brief. Do not run automatically at the end of an interview.
disable-model-invocation: true
---

# Reverse Brief

Start only when the human explicitly requests this workflow by name.

Stop any active interview and infer the subject and originating task from the full relevant conversation. If there is no active interview, brief the current decision or task. Do not ask another interview round.

Separate stated facts and preferences from derived insights. Give the basis for material interpretations and qualify uncertainty when it affects a decision. Preserve consequential wording, skipped answers, contradictions, and unresolved choices; proposed defaults are not confirmed decisions.

Present a compact confirmed understanding, useful conclusions, unresolved issues, proposed defaults, and concrete handoff as applicable. Omit empty fields. Use the active conversation's link, numbering, and output conventions rather than forcing a new list sequence or fixed template.

Show the brief before dependent work uses it. Respect a requested review checkpoint. If the user already asked for continuation, show the brief and resume the authorized task in the same turn; do not ask again. Otherwise leave it available for review. Corrections take precedence over prior interpretations. A standalone brief needs no invented next task or extra confirmation question.
