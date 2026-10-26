---
name: interview
description: Run an adaptive context-gathering interview when the user explicitly invokes interview before a decision or task. Reuse known answers and stop when the decision-critical context is sufficient.
disable-model-invocation: true
---

# Interview

Start only when the user requests this workflow, even if a harness ignores invocation metadata. Infer the subject and originating task from the conversation; use the first batch to establish missing scope if necessary.

## Question batches

Honor requested rounds and counts. Otherwise use at most two batches of up to three focused questions each; these are maxima, not quotas. State the subject and planned limit briefly, then ask the first useful batch. Prefer concrete choices with a free-text route when available.

Reuse facts already provided and omit questions whose answers would not change the decision. Group independent questions in one message and follow the active conversation's numbering and formatting conventions. Internal round/question IDs need not become restarted display labels. Let the user answer by label, briefly, or skip.

Move from scope and success toward consequential uncertainties and practical choices. Do not chase every skipped answer or infer consent from omission. Reframe an unanswered question only when it blocks the requested outcome, and explain why it matters.

## Finish and continuation

End when enough context exists, the configured limit is reached, or the user says DONE or STOP. Do not require another DONE after the final useful batch. Summarize any decision-critical uncertainty and resume an already-authorized originating task once the interview ends. STOP ends interviewing; if it also cancels the task, respect that instruction.

While awaiting interview answers, do not begin dependent implementation. Independent work may continue only when the user has authorized it. Do not add a separate confirmation gate unless the user requested one or a consequential choice remains unresolved.
