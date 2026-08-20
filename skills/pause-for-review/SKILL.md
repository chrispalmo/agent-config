---
name: pause-for-review
description: >-
  Stops staged work at explicit review checkpoints, links the artifacts that
  gate later stages, and resumes according to explicit review instructions.
  Use when the user invokes /pause-for-review.
disable-model-invocation: true
---

# Pause for Review

Treat each review checkpoint as a hard gate.

## At a checkpoint

1. Follow the user's stated stages. If checkpoint placement is unclear, ask before starting.
2. Complete work only through the next checkpoint.
3. If a status or review ledger exists, record the open checkpoint, artifact paths, and next stage.
4. Do not begin, draft, or precompute the next stage before the user replies.
5. End with:

```markdown
## Review checkpoint

- Review: [artifact](relative/path)
- Decision needed: [only unresolved decisions, or omit]
- Next stage: [next stage]

Reply with feedback, continue, approve, or approve and continue.
```

Link only artifacts that later work will rely on. Verify each target exists. Prefer workspace-relative Markdown links and keep the summary brief.

## Resume

| Reply                  | Meaning                                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `feedback`             | Revise the listed artifacts and present the same checkpoint again.                                                      |
| `continue`             | Leave the listed artifacts unapproved and work until the next checkpoint. Include all still-unapproved artifacts there. |
| `approve`              | Record approval of the listed artifacts, then stop and await instructions.                                              |
| `approve and continue` | Record approval of the listed artifacts, then work until the next checkpoint.                                           |

Apply approval only to the artifacts listed at the current checkpoint. Record one durable line with the date, approved artifacts, and next stage in an existing status or review ledger. If no project ledger exists, retain the approval in the active conversation context. Do not create files solely to record approval.

## Guardrails

- Never infer approval from silence, praise, or unrelated instructions.
- Never mark an artifact approved before the user approves it.
- Surface only decisions that block the next stage.
- Do not add planning documents merely because they might be useful.
- If a later stage changes an approved premise, stop and reopen the affected checkpoint.
