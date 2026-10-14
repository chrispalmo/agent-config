---
name: delegated-session-access
description: Give delegated agent sessions the repositories their instructions require
alwaysApply: true
---

# Delegated Session Access

When you start another agent session or task for a repository, check that repository's agent instructions for other repositories they require at startup, such as a linked company policy repo. Give the new session access to those repositories when you start it. If you can only attach one, tell it in the task prompt which others to attach before starting work.

If a repository your instructions require is unreachable, use whatever means your environment provides to obtain or attach access before reporting it unavailable.
