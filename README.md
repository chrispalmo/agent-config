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
    └── <rule>/
        ├── RULE.md
        └── references/          # optional
```

All skill collections live under [skills/_collections](skills/_collections/README.md); independent skills live directly under `skills/`. Collection overviews identify their member skills. Installed command names stay the same.

## Install

```bash
./scripts/install.sh
```

Default install and `--all` write skills and rules for Cursor, Claude Code, and Codex. Explicit agent flags restrict installation to the selected targets. Skills include their supporting resources; full installs remove retired skills owned by this repository, while package and single-skill installs preserve skills outside the selection.

Rule installation and removal require Python 3.9+ (standard library only). Rules may keep supporting files under `rules/<name>/references/` and link to them with ordinary inline Markdown links such as `[example](references/example.svg)`. Use an angle-bracket destination for filenames containing spaces or parentheses. The installer checks these links and rewrites them to absolute installed paths, preserving optional fragments and quoted titles. Reference-style Markdown definitions and paths outside `references/` are not rewritten.

Rule references are installed outside native rule-discovery directories: beside the Cursor/Claude rules directory in `<rules-directory>.resources/<name>/references/`, and beside Codex's generated instruction file in `<AGENTS-file>.resources/<name>/references/`. These locations follow destination overrides. Codex receives references only for its always-on rules. Reinstallation refreshes owned reference directories and removes retired ones; uninstall removes owned references while preserving unrelated files. Foreign destination clashes abort before installation writes, and source reference trees must contain regular files/directories rather than symlinks. Pending-review drafts are excluded.

Cursor rule installation also adds a managed global [`sessionStart` hook](https://cursor.com/docs/hooks#sessionstart). When the workspace is outside the installed rules' ancestor tree, it supplies always-on rule bodies before work starts and links scoped rules for the agent to read when their patterns apply. Workspaces already covered by native ancestor discovery receive no duplicate context. The hook reads the installed `.mdc` files and their resolved reference links; canonical guidance stays in `rules/`.

Existing Cursor hooks are preserved. `CURSOR_HOOKS` overrides the hook configuration path, which defaults to `hooks.json` beside the rules directory. The managed helper lives in `<rules-directory>.resources/.agent-config-context/` and uses Python 3.9+ at session start. Uninstall removes only its own hook and helper. Cursor's account-level User Rules remain separately configurable in its UI; cloud bootstrap retains its existing root-level ancestor link because cloud agents do not run user session-start hooks.

| Option | Effect |
| --- | --- |
| `--cursor` | Install Shared-root skills and Cursor-native rules |
| `--claude` | Install Claude Code skills and rules |
| `--agents` / `--codex` | Install Shared-root skills and Codex rules |
| `--skills` | Install only skills |
| `--rules` | Install only rules |
| `--package <name>` | Install one complete skills package |
| `--skill <path>` | Install one independent catalog skill; preserve other installed skills |
| `--external-skill <config.json>` | Install a pinned skill from another local repository; explicit agent targets required |

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

For skills owned/versioned in another repository, use the explicit [external-source installation flow](docs/external-skills.md). Its local configuration pins the repository, skill path and packaged contents; the owning source stays outside agent-config. Default installs, pruning and uninstall preserve external installations. This mode requires Python 3.9+ and does not fetch sources or roll them out to other machines.

## SF1 artifact delivery

The always-on [SF1 artifact delivery rule](rules/sf1-artifacts/RULE.md) discovers `artifact-box` through `~/.config/snowflake1/artifact-box.json` on enrolled hosts. The host configuration points to the service usage guide. The project-owned `artifact-box` skill installs separately through the [external-source flow](docs/external-skills.md). Installing the rule does not enroll a machine, connect repositories to SF1, or authorize publication.

## Cloud agents

Cloud agents do not see this machine. Follow the human setup guide in [scripts/cloud/README.md](scripts/cloud/README.md) (Cursor, Claude Code, and Codex, step by step).

## Browser tabs

The always-on [browser-session rule](rules/browser-session/RULE.md) routes browser work to [browser-session](skills/_collections/browser/browser-session/SKILL.md). Agent-created tabs use `bot/<task>` groups and a shared local registry under `/tmp/agent-browser-<uid>/sessions/` (`/private/tmp/…` on macOS). This private per-user location works within normal workspace permissions without changing global settings. It is independent of each harness's working directory and temporary-directory environment. Session/tab activity has a two-hour grace period; tabs awaiting human action have a 48-hour hold unless the human requests indefinite retention. Temporary tabs should close when their purpose ends.

Invoke `$browser-cleanup` or request browser cleanup to use [browser-cleanup](skills/_collections/browser/browser-cleanup/SKILL.md) manually. Scheduled cleanup uses that same skill and policy; installing this repository does not create a schedule. Ungrouped, unregistered, ambiguous, recently used, active, pinned, and audible tabs are spared. The registry is local to a machine; cloud agents cannot use it without access to the same state and browser. Source and installer checks do not prove that every harness invokes these skills or follows the rule.

The two skills form the `browser` package. Their helper has no browser access and only manages registry records and eligibility plans. Run `python3 scripts/test-browser-sessions.py` for isolated lifecycle checks.

The operating system may clear temporary storage. If that happens, ownership records are lost and cleanup safely leaves unregistered tabs open. Do not infer ownership from group names or recreate old records. `AGENT_BROWSER_STATE_DIR` is an explicit isolated-test override, not a per-harness configuration setting.

When upgrading from the former persistent location, install the browser package and run the helper's `migrate --from ~/.local/state/agent-browser/sessions` command once. It moves existing records under locks without changing deadlines or other session fields. Ordinary commands fail if legacy records remain, so an interrupted migration can be retried before new registrations. Update existing cleanup/review schedules to use the helper's default store. Reversing the storage change also requires an explicit locked migration and updating every caller together; never run two ownership stores or change the global permission default as part of a storage change.

## Coordinate work

The [coordination package](skills/_collections/coordination/README.md) groups triage, propose-tasks, delegate, harness, pause-for-review, and chat-closeout. They organize supplied ideas, propose next work, assign existing tasks, optionally operate an explicitly chosen external native worker, and assess or resolve a chat's unfinished obligations. Chat-closeout handles read-only readiness questions and requested execution in one skill; it reports leave/start-new-topic and archive readiness against the actual completion boundary. Install with `./scripts/install.sh --skills --package coordination --cursor --claude --agents`; the shared message and greeting rules use the separate normal rule installation flow.

The [design collection](skills/_collections/design/README.md) groups the design comparison tool and the neon neo-brutalist minimal style.

The collection's [device-frames skill](skills/_collections/design/device-frames/SKILL.md) sources and checks phone/tablet housings for interactive previews, screenshots, and videos. Its source guide covers official Apple artwork, Android tools, and community libraries, with exact-model checks and explicit approximation limits. It does not bundle a device catalog or update existing artifacts.

## Assess decisions and AI methods

The always-on [Decision Criteria rule](rules/decision-criteria/RULE.md) defines how recommendations state their objectives, criteria, evidence, and trade-offs. The separate [Decision Criteria skill](skills/decision-criteria/SKILL.md) provides an explicit assessment or reassessment action without duplicating the full standing rule. Invoke it as `$decision-criteria` in Codex or `/decision-criteria` in Claude Code and Cursor; a plain-language mention is not a portable substitute for native invocation of this explicit-only skill.

The [Bitter Lesson skill](skills/bitter-lesson/SKILL.md) supports automatic selection for consequential AI-method choices and explicit assessment or reassessment through `$bitter-lesson` in Codex or `/bitter-lesson` in Claude Code and Cursor. It keeps its essay on demand and has no companion rule. An explicit request to reassess takes precedence over reusing an earlier checkpoint.

Both skills install independently through the existing single-skill options. They have no package or installation dependency on each other or on a rule. Installation checks verify generated artifacts; they do not establish native discovery or behavioral reliability.

## Search past chats

The [search-agent-chats skill](skills/search-agent-chats/SKILL.md) is installed across Cursor, Claude Code, and Codex. It searches retained conversations from all three harnesses through the maintained archive's search script, with word/optional meaning search and exact event citations. Results expose scope, the last capture observation, word-index freshness, and meaning coverage separately. Agents choose among the tools actually available; no native/archive routing order is prescribed. Capture, model setup, and cloud/remote synchronization are not installed by this skill.


## Adding skills and rules

The automatically discoverable [github-repo-defaults skill](skills/github-repo-defaults/SKILL.md) defaults new GitHub repositories to `snowflake1xyz` unless the user explicitly requests another owner. New organization-owned repositories follow the canonical [Snowflake1 connection procedure](https://github.com/snowflake1xyz/snowflake1/blob/main/PROJECT_SETUP.md#installation); personal repositories are exempt. The explicit-only [github-init skill](skills/github-init/SKILL.md) uses the same defaults while retaining its private visibility default and initial-push workflow.

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
