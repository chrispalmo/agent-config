---
name: plaintext
description: Produce one copyable plain-text payload when the user invokes plaintext or directly asks for text to paste without rich formatting. Use for prompts, messages, emails, and other requested copy-paste output.
disable-model-invocation: true
---

# Plaintext

A direct request for copyable plain-text output is an invocation of this workflow. Produce the requested payload in one fenced block with no language tag. Keep contextual notes outside the block when they help.

Preserve the text and intentional spacing the recipient will paste. Avoid Markdown styling inside the payload unless the user requests Markdown. Literal code fences that belong to a requested prompt or Markdown payload may appear inside it: use an outer fence longer than the longest same-character fence in the payload so the whole result remains copyable. Do not split a single deliverable across several blocks.

Apply conversation conventions to surrounding chat; the payload follows the requested recipient's format. Copyable output does not authorize sending or publishing it.
