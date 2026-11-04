---
name: github-init
description: Initializes the current project as a Git repository, creates a GitHub repository, and pushes the initial branch with upstream tracking. Defaults to a private repository in snowflake1xyz with Snowflake1 guidance connected; explicit text may override owner or visibility. Use only when the human explicitly invokes github-init.
disable-model-invocation: true
---

# GitHub Init

Initialize the current project as a remote-synced GitHub repository.

## Invocation

Start only when the human explicitly requests this skill by name; a general repository setup request does not activate it.

Interpret text following the skill invocation as natural-language overrides, not as a rigid argument syntax.

- `/github-init` → private repository owned by `snowflake1xyz`
- `/github-init public` → public repository owned by `snowflake1xyz`
- `/github-init name=my-project` → private repository named `my-project`
- `/github-init in the acme organization` → private repository owned by `acme`
- `/github-init public owner=acme` → public repository owned by `acme`
- `/github-init in my personal account` → personal repository, exempt from automatic Snowflake1 connection
- `/github-init internal in acme` → internal repository owned by `acme`, if its GitHub Enterprise plan supports internal repositories

Ownership on GitHub is limited to a personal user account or an organization. For an organization owner, verify repository-creation privileges; for an explicitly requested personal owner, verify the authenticated account can create there. If trailing text is ambiguous, ask one focused question.

## Defaults and overrides

1. Verify `git` and `gh` are available and `gh auth status` succeeds. Stop and report a definitive authentication or authorization failure.
2. Resolve the authenticated user with `gh api user --jq .login`.
3. Default `owner` to `snowflake1xyz` (SF1) and `visibility` to `private`, regardless of the authenticated user. Never fall back to a personal namespace if organization access fails.
4. Override `owner` only when the user explicitly requests another organization or a personal account. Resolve “my personal account” to the verified authenticated user.
5. Override `visibility` only when the trailing text explicitly requests `public`, `private`, or `internal`. Treat `internal` as organization-only and verify GitHub accepts it.
6. Use the basename of the current working directory as the repository name unless trailing text explicitly supplies another name.
7. Check whether `<owner>/<repository-name>` already exists. If the default name is unavailable, use the first available numeric suffix (`name-2`, `name-3`, and so on). Never silently alter an explicit name; ask whether to use the existing repository or choose another name.

## Workflow

1. Resolve the intended project directory from the active workspace and invocation; ask only when it is ambiguous.
2. Inspect the project for likely secrets, credentials, environment files, generated files, and dependency directories. Add appropriate ignore rules before staging, and never commit likely secrets.
3. If the directory is not a Git repository, run `git init`.
4. For a new organization-owned repository, follow the canonical [Snowflake1 connection procedure](https://github.com/snowflake1xyz/snowflake1/blob/main/PROJECT_SETUP.md#installation) using its current approved `main` revision and existing authenticated access. Complete its required reading and verification, preserving project instructions. Repositories explicitly created under a personal account are exempt; an explicit connection request or opt-out takes precedence. Disclose blocked connection rather than claiming full setup. Then, if there is no commit, stage the safe project files and create an initial commit. Follow repository commit-message conventions when present; otherwise use `Initial commit`.
5. If `origin` already exists, verify that it points to the intended GitHub repository. Do not replace or push to a mismatched remote without user approval.
6. If no GitHub remote exists, create `<owner>/<repository-name>` from the current directory with `gh repo create`, passing exactly one of `--private`, `--public`, or `--internal`, plus `--source=. --remote=origin`.
7. Push the current branch with upstream tracking using `git push -u origin HEAD`.
8. Verify the actual owner and visibility with `gh repo view`, verify the local branch tracks the remote branch, and account for any remaining working-tree changes rather than discarding them to force a clean tree.

Ask only when an override is ambiguous, an organization rejects repository creation, an existing remote conflicts, likely secrets require a user decision, or an operation would overwrite or expose existing work.

## Completion

Report the GitHub repository URL, owner, visibility, current branch, upstream branch, Snowflake1 connection status (verified, exempt, or blocked), and any files intentionally left uncommitted.
