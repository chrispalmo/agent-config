---
name: conversation-titles
description: Initialize conversation titles once at creation or at the start of the first assistant turn, using project name — topic where applicable
alwaysApply: true
---

# Conversation Titles

Apply this naming convention exactly once during initial setup: when creating a conversation yourself, or at the start of the first assistant turn in a human-created conversation. For a new conversation that belongs to a named project, use this title format:

`<project> — <short topic>`

Use the project's displayed name and a spaced em dash. The title is a plain, recognizable label for the conversation's subject, not a summary of its contents or progress.

Preserve the exact capitalization of the displayed project name, proper names, brands, acronyms, and code identifiers. Use sentence capitalization for newly generated topic text; do not lowercase the whole title or mechanically convert it to title case. Preserve the capitalization of a full title explicitly supplied by the user.

Use the host's supported creation-time title field or title-setting tool. Updating an automatically generated title at the start of the first assistant turn counts as initialization; a dedicated creation-time title field is not required. If the title already follows the convention or was explicitly chosen by the user, leave it unchanged. For new conversations without a named project, use a concise topic title without a project prefix. If no supported title control is available during initialization, skip it rather than catching up in a later turn.

After initial setup, the initialization naming convention is inactive for that conversation. Do not reapply it in later turns, when the conversation resumes, or when its project, topic, or scope becomes clear or changes. A later user request to rename the conversation is a separate task governed by that request; preserve the capitalization described above, without reactivating the initialization naming convention.
