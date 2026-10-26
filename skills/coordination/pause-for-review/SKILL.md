---
name: pause-for-review
description: Stop staged work at explicit review checkpoints and resume according to the user's review instructions. Use when the user explicitly invokes pause-for-review.
disable-model-invocation: true
---

# Pause for Review

Start only when the human explicitly requests this workflow by name.

Apply hard gates only to the user's requested stages. Resolve checkpoint placement from the request and context; ask before dependent work if it remains unclear. Complete the next checkpoint's artifacts before requesting review. Do not draft or precompute the following stage while its gate is pending.

Link the concrete artifacts that later work relies on, verify their locations, state any blocking decision and the next stage, and invite feedback or a continuation instruction. Use the active conversation's numbering and link conventions, including absolute local links when required. Keep the checkpoint summary brief.

Record the open checkpoint in an existing status or review store if one exists. Do not create a new ledger solely for an approval record.

| Reply | Meaning |
| --- | --- |
| feedback | Revise the listed artifacts and present that checkpoint again. |
| continue | Proceed to the next checkpoint; the current artifacts remain unapproved and must be shown there. |
| approve | Record approval of the listed artifacts, then stop unless the user also authorizes continuation. |
| approve and continue | Record approval and proceed to the next checkpoint. |

Equivalent natural-language instructions have the same effect. Carry existing authorization forward rather than asking for it again. Approval applies only to the artifacts actually reviewed; silence or unrelated praise is not approval. Record the approved artifacts and next stage in the existing authority or conversation.

If later work changes an approved premise, reopen only the affected checkpoint. Surface decisions that block the next stage; do not manufacture planning artifacts or review gates outside the requested workflow.
