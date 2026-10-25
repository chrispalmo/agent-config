# Model selection and control

The human approves a concrete model recommendation with the assignment. An owner chat and an external worker can use different models and subscription routes; name them separately. Use current task requirements and established usage preferences rather than a universal model ranking or financial optimization.

Ordinary internal delegation presents its exact recommended owner model and effort with the assignment. For explicitly requested external execution, the sibling harness skill owns preference clarification and worker controls. Existing adequate task-scoped authorization carries forward.

## Current Codex app capability

Checked 25 October 2026 against the live app-tool definitions and a fresh chat-list response. This was a read-only capability inspection; no handoff was sent and no model setting was changed to test the override.

| Surface | Exposed capability and limit |
| --- | --- |
| `send_message_to_thread` | Accepts optional `model` and `thinking` arguments for Codex-backed chats. Omitting them preserves current settings. Supply approved values explicitly for a model-controlled handoff. The destination host validates available model/effort combinations. |
| `create_thread` | Accepts model and effort for Codex chats, subject to its explicit human request and creation rules. Do not infer new-chat authority from model approval. These overrides do not apply to ChatGPT-backed cloud chats. |
| `list_threads` | The inspected response has identities, titles, project/status metadata, and summaries, but no selected-model or reasoning-effort fields. It is not a current model-picker inspection API. |
| `read_thread` | Exposes status and history. An earlier run receipt can establish what was used for that run, but does not establish the chat's current selected model. |

The [official app-server documentation](https://learn.chatgpt.com/docs/app-server#start-a-turn) describes model/effort overrides on `turn/start`. It also states that per-turn configuration overrides become defaults for later turns, and that steering an active turn does not accept model overrides. This documents the underlying protocol; the exact persistence and runtime receipt behavior of the desktop handoff wrapper has not been independently tested here. Do not present an override as necessarily temporary.

## Dispatch evidence and fallback

Show the owner chat, approved model and effort, brief reason, and control method in the proposed handoff. Include a worker route/model separately only when external work has been authorized and its preferences resolved.

Use supported override fields when available. Retain the request and returned acceptance receipt, then inspect actual runtime identity if a trustworthy receipt exposes it. Distinguish requested, accepted, and runtime-observed settings. A model claiming its own identity is not an independent receipt. If returned settings conflict with the approved selection, stop the affected route and resolve the mismatch rather than silently changing models.

When the available interface cannot set the required model, explain exactly which chat requires a manual model/effort selection and confirmation before dispatch. Do not send work under an unknown inherited selection merely to discover what runs. Never test a setting by sending an otherwise unauthorized prompt, starting a new worker, or interrupting active work.

Review this capability note when the app's tools or supported host/model combinations change, or a real handoff reveals different override behavior. The source checks validate packaging and prose structure, not execution-model enforcement.
