---
name: github-repo-defaults
description: Apply GitHub ownership and Snowflake1 connection defaults when creating a new repository or publishing a local project to a new GitHub repository. Use for repository creation requests, including project setup that creates a repo.
---

# GitHub Repository Defaults

Create new GitHub repositories under `snowflake1xyz` (SF1) unless the user explicitly requests another owner. Use the fully qualified `snowflake1xyz/<repo>` when creating the remote; the authenticated account is not the default owner. Use a personal account only when explicitly requested. If organization access fails, report the blocker instead of falling back to a personal namespace.

For each new organization-owned repository, follow the canonical [Snowflake1 connection procedure](https://github.com/snowflake1xyz/snowflake1/blob/main/PROJECT_SETUP.md#installation). This is the existing connection guide, not a separately installed skill. Retrieve the current approved `main` revision through existing authenticated access and follow its Installation section, including the required policy reading and verification. Keep the connection procedure there rather than copying its template into this skill.

Connection means installing the canonical pointer in the project's root `AGENTS.md`, preserving project instructions, and keeping `CLAUDE.md` as the `@AGENTS.md` shim. A Git remote alone does not establish this connection. Repositories explicitly created under a personal account are exempt from automatic SF1 connection; an explicit user request to connect or opt out takes precedence.

Apply these defaults within the authorized creation task. Do not transfer existing repositories or change their ownership merely because they differ from the default. Report the resulting repository URL and owner, plus whether connection was verified, exempt, or blocked. If the connection source is unavailable, disclose the incomplete connection instead of claiming the new repository is fully set up.
