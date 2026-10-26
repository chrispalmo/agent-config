# Coordination package closeout — 26 October 2026

The reviewed [coordination package](../../skills/_collections/coordination/README.md) is promoted and installed for Codex, Cursor, and Claude Code. After the initial scoped publication, the human requested the same physical package structure as project-management, reinstallation across all harnesses, and synchronization of every pending repository change. The five coordination skill sources now live under `skills/_collections/coordination/`; all collections share the `skills/_collections/` parent, and installed names and invocation behavior remain unchanged. This closeout supersedes the initial scoped-sync status.

## Adopted behavior

| Component | Responsibility |
| --- | --- |
| [triage](../../skills/_collections/coordination/triage/SKILL.md) | Organize supplied material and discuss possible continuations; no automatic handoffs. |
| [propose-tasks](../../skills/_collections/coordination/propose-tasks/SKILL.md) | Check existing commitments, distinguish completion from optional development, and present numbered tasks with reasons. |
| [delegate](../../skills/_collections/coordination/delegate/SKILL.md) | Prepare assignments by default, preserve sufficient human authorization, select explicit owner models, and dispatch when authorized. |
| [harness](../../skills/_collections/coordination/harness/SKILL.md) | Operate an explicitly chosen external native worker; clarify missing route/model preferences before proposing external assignments. |
| [pause-for-review](../../skills/_collections/coordination/pause-for-review/SKILL.md) | Hold explicitly requested review checkpoints and resume according to the human’s instructions. |
| [chat-source](../../rules/chat-source/RULE.md) | Identify agent requests, use readable briefs, and make replies understandable on their own. |
| [address-the-user](../../rules/address-the-user/RULE.md) | Keep the human's name preference in the general rule and address the agent as “boss” when directly replying to an agent-originated message. |

## Review disposition

The Astra review's first three recommendations were approved and implemented: include the receiving host's actual explicit skill invocation in authorized handoffs, make delegate proposal-first and give unnumbered tasks IDs, and keep project-specific history out of installed runtime resources. The human replaced the fourth recommendation with the general addressing-rule rename, then specified the agent greeting. The cancelled Claude review is not pending.

The [native-run evidence](evidence/coordination-native-runs/README.md) retains historical observations separately from installed guidance. Full superseded draft/review materials were preserved locally at `~/.local/state/agent-config/reviews/2026-10-26-coordination/` before retiring the promoted draft directories. They are historical records, not active instructions.

## Validation, installation, and cleanup

The full checkout passed the content checker (19 skills, zero drafts, 11 rules), all 14 content regression tests, all 16 browser-registry tests, the isolated installer suite, local Markdown reference checks, and whitespace checks. All previously pending source, documentation, and historical evaluation evidence is included in this full repository sync. The newer metadata checks and invocation-policy files are now published together, resolving the earlier difference between local and committed validation.

The installer accepts a source relocation only when the existing managed marker identifies a retired path within this repository with the same skill name. New fixtures verify successful relocation across all three targets and refusal of a foreign source before partial changes. Existing resource-ownership checks remain in force.

A full installation used:

```bash
./scripts/install.sh --cursor --claude --agents
```

All 38 installed skill copies (19 in the shared Codex/Cursor root and 19 in Claude Code) match canonical sources, resources, and ownership paths. All generated rules match isolated rendering. No repository-owned duplicates remain in the former native skill roots. Proofread and Ingest are absent from canonical catalogs and installations; remaining mentions in reports and retirement fixtures are historical evidence.

Generated Python caches are excluded from Git. Historical patch artifacts retain their exact unified-diff whitespace; a scoped Git attribute excludes those evidence patches from prose/source whitespace checks. Promoted drafts remain archived outside installer inputs. The four old top-level coordination skill folders are gone, and current catalogs, package documentation, links, and tests use the nested layout. The final remote commit and clean working-tree verification are recorded in the chat and local completion receipt.

No package implementation or review work remains. The chat is ready to archive after the full commit is verified on the remote and the working tree is clean. Broader behavioral evaluations, native activation coverage, and desktop model-override verification remain optional future work; source and installation checks do not establish those outcomes.

## Collection layout decision and final closeout

The human chose a single `skills/_collections/` directory for every collection and approved the component sheet for installation and sync. [The collection index](../../skills/_collections/README.md) lists browser, coordination, design, interview, and project-management. Every member has its own skill folder; Interview's entrypoint is now inside its `interview/` member folder beside reverse-brief. Independent skills remain directly under `skills/`.

Catalogs, active links, source-layout guidance, and test/helper paths were updated together. Historical evidence snapshots retain their dated paths. The approved component SVG was preserved byte-for-byte through relocation and is included in the source commit and installed resources.

The final checkout passed the content checker, 14 content regressions, 16 browser-registry regressions, isolated installer tests, active local-link checks, and whitespace checks. Full reinstallation across Cursor, Claude Code, and Codex produced 38 verified skill copies and exact rendered rules, with all ownership markers pointing at current sources. No owned legacy duplicates or retired skill folders remain.

The layout decision, implementation, installation, and cleanup are complete. Final publication identity and working-tree verification are retained in the chat and local completion receipt. No review or implementation is held for this package.

## Final naming and visual-default instructions

The human then requested `_collections` so the parent sorts ahead of ordinary skill folders. The source layout is `skills/_collections/<collection>/<skill>/`; only that namespace component accepts an underscore, while skill names remain unchanged. Catalog validation and managed relocation checks support the chosen parent, and two regression cases keep ordinary skill names and misplaced namespace components restricted.

The human also replaced the former visual default with neon neo-brutalist minimal while retaining purposeful delight. The shared visual rule and style-skill discovery text agree on that default, with explicit user direction and established brands taking precedence. The approved component sheet is included. The entire empty `drafts/` tree, including its empty subdirectory, was inspected and removed; `private-repo` remains absent.

The final required checks passed: 19 skills, zero drafts, 11 rules, 14 content regressions, 16 browser-registry regressions, the isolated installer suite, active local links, and whitespace. Full reinstallation and exact source/resource/ownership/rule comparisons passed across Cursor, Claude Code, and Codex. No collection, style, installation, or cleanup decision remains open. The chat can close after source publication is confirmed by the final remote and clean-tree check.
