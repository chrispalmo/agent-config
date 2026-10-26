---
name: browser-session
description: Register agent-created browser tabs and clean up temporary browser work
alwaysApply: true
---

# Browser Sessions

Before opening browser tabs, load the `browser-session` skill. Group agent-created tabs under `bot/<task>` and register them in the shared local browser-session registry. Close temporary tabs when their purpose ends; retain tabs needed for human action with a reason and expiry. Use `browser-cleanup` for manual or scheduled cleanup. Follow harness browser policies and native lifecycle controls; never infer ownership of existing tabs or bypass unavailable browser controls.
