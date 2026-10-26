---
name: plaintext
description: Produce one copyable plain-text payload only when the human explicitly invokes plaintext. Use for prompts, messages, emails, and other requested copy-paste output.
disable-model-invocation: true
---

# Plaintext

Start only when the human explicitly selects the skill or directs an invocation of plaintext by name. A general request for plain text or copyable output does not activate this workflow. Produce the requested payload in one fenced block with no language tag. Keep contextual notes outside the block when they help.

Preserve the text and intentional spacing the recipient will paste. Avoid Markdown styling inside the payload unless the user requests Markdown. Literal code fences that belong to a requested prompt or Markdown payload may appear inside it: use an outer fence longer than the longest same-character fence in the payload so the whole result remains copyable. Do not split a single deliverable across several blocks.

Apply conversation conventions to surrounding chat; the payload follows the requested recipient's format. Copyable output does not authorize sending or publishing it.
