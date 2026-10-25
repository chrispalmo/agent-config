# Explicit skill invocation in a handoff

Use when an authorized assignment needs an explicit-only skill in its receiving chat. The sender carries both the human's task-scoped authority and the destination host's actual invocation. A marker requests activation; it does not authenticate the sender or grant authority. Keep ordinary internal assignments free of external-harness invocation.

Resolve the installed skill identity and the receiving host/interface before composing the message. Keep proposal-only work proposal-only, and use the original human authorization to establish the allowed task and route. If the host cannot activate the skill through that interface, explain the capability limit and the supported manual step. Do not bypass a blocked invocation by reproducing the skill through another tool.

## Codex

The [skill policy documentation](https://learn.chatgpt.com/docs/build-skills#optional-metadata) retains explicit invocation when implicit invocation is disabled. The [app-server skill protocol](https://learn.chatgpt.com/docs/app-server#skills) uses a `$<skill-name>` marker in text; a structured skill input can additionally inject the installed content when the interface supports it.

For a text-only dispatch interface, include the verified marker in the actual receiving prompt. For example, an authorized harness assignment can begin:

```text
$harness Carry out the approved native-worker assignment below.
Agent-originated
Source: <real source chat/location and link or ID>
Human authority: <actual request/selection and its scope>
```

Continue with the compact task, approved settings, output, and holds. Do not invent a structured-input argument on a wrapper that only accepts a prompt string. Current Codex app chat messaging supports text prompts and model/effort overrides; the underlying protocol documents marker resolution, but that wrapper's activation behavior has not been exercised here.

## Claude Code

[Claude Code documents](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) direct invocation by putting the command at the start of the message. Resolve the actual installed command name, including any namespace. For an interface that accepts native skill commands, the equivalent authorized prompt can begin:

```text
/harness Carry out the approved native-worker assignment below.
Agent-originated
Source: <real source chat/location and link or ID>
Human authority: <actual request/selection and its scope>
```

This placement lets the native command come first while keeping the provenance label near the top. A command after plain text permits invocation under the documented rules but does not directly start it; use the direct form when the assignment depends on loading the skill. Verify support in the selected UI or CLI rather than assuming every transport handles commands identically.

## Activation evidence

The documentation above was checked on 26 October 2026. A returned dispatch receipt proves delivery, not that skill content loaded. Inspect a native activation/content receipt when the host exposes one; otherwise distinguish the requested invocation from unverified activation. Do not launch a dummy task to obtain a receipt. A real authorized assignment can supply that evidence. Recheck this note when host invocation controls or dispatch interfaces change.
