# Coordination package closeout — 26 October 2026

The reviewed [coordination package](../../skills/coordination/README.md) is promoted and installed for Codex, Cursor, and Claude Code. The human authorized the final greeting change, promotion, installation, and repository sync. No approval or implementation work remains for this package. The chat can be archived once the scoped commit is confirmed on the remote.

## Adopted behavior

| Component | Responsibility |
| --- | --- |
| [triage](../../skills/triage/SKILL.md) | Organize supplied material and discuss possible continuations; no automatic handoffs. |
| [propose-tasks](../../skills/propose-tasks/SKILL.md) | Check existing commitments, distinguish completion from optional development, and present numbered tasks with reasons. |
| [delegate](../../skills/delegate/SKILL.md) | Prepare assignments by default, preserve sufficient human authorization, select explicit owner models, and dispatch when authorized. |
| [harness](../../skills/harness/SKILL.md) | Operate an explicitly chosen external native worker; clarify missing route/model preferences before proposing external assignments. |
| [chat-source](../../rules/chat-source/RULE.md) | Identify agent requests, use readable briefs, and make replies understandable on their own. |
| [address-the-user](../../rules/address-the-user/RULE.md) | Keep the human's name preference in the general rule and address the agent as “boss” when directly replying to an agent-originated message. |

## Review disposition

The Astra review's first three recommendations were approved and implemented: include the receiving host's actual explicit skill invocation in authorized handoffs, make delegate proposal-first and give unnumbered tasks IDs, and keep project-specific history out of installed runtime resources. The human replaced the fourth recommendation with the general addressing-rule rename, then specified the agent greeting. The cancelled Claude review is not pending.

The [native-run evidence](evidence/coordination-native-runs/README.md) retains historical observations separately from installed guidance. Full superseded draft/review materials were preserved locally at `~/.local/state/agent-config/reviews/2026-10-26-coordination/` before retiring the promoted draft directories. They are historical records, not active instructions.

## Validation and installation

The current checkout passed the content checker, all 12 content regression tests, the isolated installer suite, and whitespace checks. The rule migration tests cover both managed old-file retirement and aborting before partial migration on a foreign destination clash.

The exact scoped publication candidate separately passed its committed content checker and full isolated installer suite. The newer, independently modified local checker found no added findings against the committed baseline; its seven pre-existing metadata findings concern other skills and remain outside this package. All four coordination skills pass those newer checks.

Installed package sources and resources were compared with the repository in `~/.agents/skills` (Codex/Cursor) and `~/.claude/skills`. Generated rules matched the isolated preview. The only rule differences were the addressing rename, two managed old-file retirements, chat-source updates, and the combined Codex rule output. Other installed rules were unchanged in content.

Installation used explicit targets:

```bash
./scripts/install.sh --skills --package coordination --cursor --claude --agents
./scripts/install.sh --rules --cursor --claude --agents
```

The sync is scoped to this package, its catalogs/documentation, the two general rules, and relevant installer tests. Unrelated dirty changes remain in the working tree. Explicit target flags keep the installation commands valid with both the committed installer and the independently modified local installer.

These checks establish source consistency, packaging, migration, and installed file identity. Native skill activation, desktop model overrides, and improved agent behavior are not established by these checks. Those limitations are recorded for future real use; no dummy delegation, model run, or further review is pending.
