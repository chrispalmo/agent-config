# agent-config

Central repository of Agent Skills and Agent Rules for Cursor, Claude Code, and OpenAI Codex.

This repo replaces the old standalone `chrispalmo/skills` repo as the source of truth. Skills and rules stay separate as artifacts, while install/uninstall/test scripts are shared.

## Layout

```text
agent-config/
├── scripts/
│   ├── common.sh
│   ├── install.sh
│   ├── uninstall.sh
│   ├── test-install.sh
│   └── cloud/
├── skills/
│   ├── skills.manifest
│   ├── packages.manifest
│   ├── _collections/
│   │   └── <collection>/<skill>/SKILL.md
│   └── <skill>/SKILL.md
└── rules/
    ├── rules.manifest
    └── <rule>/RULE.md
```

All skill collections live under [skills/_collections](skills/_collections/README.md); independent skills live directly under `skills/`. Collection overviews identify their member skills. Installed command names stay the same.

## Install

```bash
./scripts/install.sh
```

Default install and `--all` write skills and rules for Cursor, Claude Code, and Codex. Explicit agent flags restrict installation to the selected targets. Skills include their supporting resources; full installs remove retired skills owned by this repository, while package and single-skill installs preserve skills outside the selection.

| Option | Effect |
| --- | --- |
| `--cursor` | Install Shared-root skills and Cursor-native rules |
| `--claude` | Install Claude Code skills and rules |
| `--agents` / `--codex` | Install Shared-root skills and Codex rules |
| `--skills` | Install only skills |
| `--rules` | Install only rules |
| `--package <name>` | Install one complete skills package |
| `--skill <path>` | Install one independent catalog skill; preserve other installed skills |

Common full install:

```bash
./scripts/install.sh --cursor --claude --agents
```

If you already installed the old `~/dev/skills` repo, run its uninstall script first so old skill symlinks do not block this installer:

```bash
~/dev/skills/scripts/uninstall.sh --all
~/dev/skills/scripts/uninstall.sh --cursor
./scripts/install.sh --cursor --claude --agents
```

Skills for Codex and Cursor share `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Full installs refresh supporting resources and remove only repository-owned duplicates from the former native roots. Explicit destination overrides remain supported. Pending-review skills live in `drafts/` and are never installed.

## Cloud agents

Cloud agents do not see this machine. Follow the human setup guide in [scripts/cloud/README.md](scripts/cloud/README.md) (Cursor, Claude Code, and Codex, step by step).

## Browser tabs

The always-on [browser-session rule](rules/browser-session/RULE.md) routes browser work to [browser-session](skills/_collections/browser/browser-session/SKILL.md). Agent-created tabs use `bot/<task>` groups and a shared local registry under `/tmp/agent-browser-<uid>/sessions/` (`/private/tmp/…` on macOS). This private per-user location works within normal workspace permissions without changing global settings. It is independent of each harness's working directory and temporary-directory environment. Session/tab activity has a two-hour grace period; tabs awaiting human action have a 48-hour hold unless the human requests indefinite retention. Temporary tabs should close when their purpose ends.

Invoke `$browser-cleanup` or request browser cleanup to use [browser-cleanup](skills/_collections/browser/browser-cleanup/SKILL.md) manually. Scheduled cleanup uses that same skill and policy; installing this repository does not create a schedule. Ungrouped, unregistered, ambiguous, recently used, active, pinned, and audible tabs are spared. The registry is local to a machine; cloud agents cannot use it without access to the same state and browser. Source and installer checks do not prove that every harness invokes these skills or follows the rule.

The two skills form the `browser` package. Their helper has no browser access and only manages registry records and eligibility plans. Run `python3 scripts/test-browser-sessions.py` for isolated lifecycle checks.

The operating system may clear temporary storage. If that happens, ownership records are lost and cleanup safely leaves unregistered tabs open. Do not infer ownership from group names or recreate old records. `AGENT_BROWSER_STATE_DIR` is an explicit isolated-test override, not a per-harness configuration setting.

When upgrading from the former persistent location, install the browser package and run the helper's `migrate --from ~/.local/state/agent-browser/sessions` command once. It moves existing records under locks without changing deadlines or other session fields. Ordinary commands fail if legacy records remain, so an interrupted migration can be retried before new registrations. Update existing cleanup/review schedules to use the helper's default store. Reversing the storage change also requires an explicit locked migration and updating every caller together; never run two ownership stores or change the global permission default as part of a storage change.

## Coordinate work

The [coordination package](skills/_collections/coordination/README.md) groups triage, propose-tasks, delegate, harness, and pause-for-review. They organize supplied ideas, propose next work, assign existing tasks, and optionally operate an explicitly chosen external native worker. Install together with `./scripts/install.sh --skills --package coordination --cursor --claude --agents`; the shared message and greeting rules use the separate normal rule installation flow.

The [design collection](skills/_collections/design/README.md) groups the design comparison tool and the neon neo-brutalist minimal style.

## Search past chats

The [search-agent-chats skill](skills/search-agent-chats/SKILL.md) is installed across Cursor, Claude Code, and Codex. It searches retained conversations from all three harnesses through the maintained archive's search script, with word/optional meaning search and exact event citations. Results expose scope, the last capture observation, word-index freshness, and meaning coverage separately. Agents choose among the tools actually available; no native/archive routing order is prescribed. Capture, model setup, and cloud/remote synchronization are not installed by this skill.


## Adding skills and rules

- Add independent skills under `skills/<name>/SKILL.md` or grouped skills under `skills/_collections/<collection>/<name>/SKILL.md`, and register them in `skills/skills.manifest`.
- Add cross-linked skill packages to `skills/packages.manifest`.
- Add rules under `rules/<name>/RULE.md` and register them in `rules/rules.manifest`.
- Keep shared project guidance in `AGENTS.md` and `CLAUDE.md` as a one-line `@AGENTS.md` shim.

## Maintenance

Follow the [maintenance guide](docs/maintenance.md) when changing guidance. Use a Python virtual environment and install `requirements-dev.txt` for validation. Run `python3 scripts/check-content.py`, `./scripts/test-install.sh`, and `git diff --check` after source changes.

The [instruction and workflow audit](docs/audits/2026-10-07-instruction-and-workflow-audit.md) records the implemented simplifications, retired skills and closeout. Project continuity defaults to minimal guidance and can reuse a compact Markdown record or an existing tracker. Harness compatibility and the broad installer audit remain deferred until the next harness switch. An [initial bounded behavioral pilot](docs/audits/evidence/2026-10-23-skill-pilot/README.md) is complete; broader longitudinal evaluation remains deferred.

## Safety

- No secrets or non-publishable preferences in skills or rules.
- Installers abort rather than overwrite unmanaged destinations.
- Generated rule files contain `<!-- managed-by: chrispalmo/agent-config -->`.
