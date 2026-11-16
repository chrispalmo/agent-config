# Codex usage access

Use this reference for Codex account allowance. The provider-specific details below were checked on 16 November 2026 against the Codex Desktop host tool schema and a successful read. Rediscover the current tool/schema if fields or behavior differ; tool availability depends on the calling host.

## Direct host tool

Discover the tool named `get_usage_limits` in the Codex app tools (currently `mcp__codex_app__get_usage_limits`) and call it with `{}`. It reads the ChatGPT account signed in on the task's host. It is account-wide, not a per-chat token budget, and does not consume a reset or purchase credits.

| Field | Meaning and handling |
| --- | --- |
| `rateLimitsByLimitId` | Prefer this map when populated; keep distinct limit IDs/pools separate. |
| `rateLimits` | Legacy single-bucket view; use when the map is unavailable, without counting both views. |
| `primary`, `secondary` | Optional windows within a bucket. Either can be absent. |
| `usedPercent` | Percentage consumed. Remaining = `max(0, min(100, 100 - usedPercent))` for a valid numeric value. Null/missing is unknown. |
| `windowDurationMins` | Window length in minutes. For example, 10,080 minutes is seven days; the field position does not identify the window. |
| `resetsAt` | Unix timestamp in **seconds**; convert to the user's timezone. Missing means unknown. |
| `credits`, reset-credit information | Separate account options, when supplied; neither is a percentage of included allowance. Availability is not authority to spend or redeem. |

The tool may expose account identifiers and additional eligibility/control fields. Retain only what the task needs, and follow current field documentation rather than guessing their meaning. Do not publish the raw response in repository evidence. A valid bucket does not establish coverage of every product or model allowance; report the scope actually returned.

## Authenticated fallback

Use the account's visible Settings → Usage or Usage & billing page. A known entry point is [ChatGPT usage overview](https://chatgpt.com/settings/usage?tab=overview). Prefer a user-supplied or already-open authenticated tab through the host's browser controls, and verify the displayed account/workspace and allowance labels. If the route redirects or changes, navigate from the signed-in app's settings. A public web search cannot read the user's private allowance.

If direct app computer use cannot expose the meter, try the authenticated browser before asking the user to retrieve it. Conversely, a browser login block need not prevent a direct host-tool read. For an already-accessible interactive Codex CLI session, `/status` is another documented route; it is a slash command inside Codex, not a shell executable. Do not start model work merely to generate usage telemetry.

Official supporting references: [Codex with a ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) documents the dashboard and CLI status route; [reviewing Work and Codex usage](https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop) describes settings and workspace-dependent displays. These establish access routes, not the current user's plan, window lengths or balance. Use current tool/UI evidence for those values.
