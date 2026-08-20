---
name: plaintext
description: >-
  Replies with the requested output as a single copyable plaintext codeblock.
  Use when the user wants a prompt, email, message, or other text to paste into
  another agent or app without markdown formatting issues; or when they invoke
  plaintext.
disable-model-invocation: true
---

# Plaintext

Produce the requested text so it can be copied and pasted elsewhere without
formatting artifacts.

## Output rules

1. Put the entire deliverable in **one** fenced codeblock with no language tag:
   ```
   ...
   ```
2. Never nest fences inside the deliverable fence.
3. Inside the fence: plain text only. Do not use markdown (bold, lists-as-markdown,
   headings, links, etc.) unless the user explicitly asks for markdown.
4. Text outside the fence is fine when useful (context, a clarifying question,
   a short note). Do not avoid it or force it — follow what the response needs.
5. Preserve intentional line breaks and spacing the user will paste as-is.

## Typical uses

- Agent prompts to paste into another chat
- Emails, Slack/Teams messages, or commit-message bodies
- Any copy-paste payload where rich formatting would break
