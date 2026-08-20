---
name: github-init
description: Initializes the current project as a Git repository, creates a GitHub repository, and pushes the initial branch with upstream tracking. Defaults to a private repository owned by the authenticated GitHub user; trailing invocation text may request public or internal visibility or an organization owner. Use when the user invokes github-init.
disable-model-invocation: true
---

# GitHub Init

Initialize the current project as a remote-synced GitHub repository.

## Invocation

Interpret text following the skill invocation as natural-language overrides, not as a rigid argument syntax.

- `/github-init` → private repository owned by the authenticated GitHub user
- `/github-init public` → public repository owned by the authenticated GitHub user
- `/github-init name=my-project` → private repository named `my-project`
- `/github-init in the acme organization` → private repository owned by `acme`
- `/github-init public owner=acme` → public repository owned by `acme`
- `/github-init internal in acme` → internal repository owned by `acme`, if its GitHub Enterprise plan supports internal repositories

Ownership on GitHub is limited to a personal user account or an organization. An authenticated user cannot create a repository in another personal user's namespace; for a non-default owner, require an organization where the authenticated user has repository-creation privileges. If trailing text is ambiguous, ask one focused question.

## Defaults and overrides

1. Verify `git` and `gh` are available and `gh auth status` succeeds. Stop and report a definitive authentication or authorization failure.
2. Resolve the authenticated user with `gh api user --jq .login`.
3. Default `owner` to that authenticated user and `visibility` to `private`.
4. Override `owner` only when the trailing text names an organization or owner namespace.
5. Override `visibility` only when the trailing text explicitly requests `public`, `private`, or `internal`. Treat `internal` as organization-only and verify GitHub accepts it.
6. Use the basename of the current working directory as the repository name unless trailing text explicitly supplies another name.
7. Check whether `<owner>/<repository-name>` already exists. If the default name is unavailable, use the first available numeric suffix (`name-2`, `name-3`, and so on). Never silently alter an explicit name; ask whether to use the existing repository or choose another name.

## Workflow

1. Confirm the intended project directory.
2. Inspect the project for likely secrets, credentials, environment files, generated files, and dependency directories. Add appropriate ignore rules before staging, and never commit likely secrets.
3. If the directory is not a Git repository, run `git init`.
4. If there is no commit, stage the safe project files and create an initial commit. Follow repository commit-message conventions when present; otherwise use `Initial commit`.
5. If `origin` already exists, verify that it points to the intended GitHub repository. Do not replace or push to a mismatched remote without user approval.
6. If no GitHub remote exists, create `<owner>/<repository-name>` from the current directory with `gh repo create`, passing exactly one of `--private`, `--public`, or `--internal`, plus `--source=. --remote=origin`.
7. Push the current branch with upstream tracking using `git push -u origin HEAD`.
8. Verify the actual owner and visibility with `gh repo view`, verify the local branch tracks the remote branch, and verify the working tree is clean.

Ask only when an override is ambiguous, an organization rejects repository creation, an existing remote conflicts, likely secrets require a user decision, or an operation would overwrite or expose existing work.

## Completion

Report the GitHub repository URL, owner, visibility, current branch, upstream branch, and any files intentionally left uncommitted.
