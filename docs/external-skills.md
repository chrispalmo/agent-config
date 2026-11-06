# Skills owned by another repository

An external skill stays in its owning Git repository. Agent-config can distribute a reviewed snapshot from a local checkout without adding its source to this repository's skill catalog. This is an explicit, host-local operation: default installs, `--all`, catalog pruning, cloud bootstrap and ordinary uninstall do not discover, refresh or remove external skills.

The existing installer supplies target locations; a small standard-library Python helper handles source identity, packaging and ownership. Python 3.9+ and Git are required. No fetching, authentication setup, repository update, service enrollment or publication is performed. Installing a skill does not authorize the actions described by it.

## Select and install

Review the owning repository, the skill and its supporting resources. Use the owning project's validation before distributing it. Generate a candidate configuration:

```bash
python3 scripts/external-skills.py pin \
  --checkout /absolute/path/to/owning-repository \
  --path skills/example
```

Save the reviewed JSON outside this repository, for example at `~/.config/agent-config/external-skills/example.json`:

```json
{
  "version": 1,
  "name": "example",
  "repository": "git@github.com:organization/owning-repository.git",
  "checkout": "/absolute/path/to/owning-repository",
  "path": "skills/example",
  "sha256": "<64-character hash printed by pin>"
}
```

The config preserves the chosen checkout path, which may be an alias for the Git root. Every install resolves it and verifies that its `origin` exactly matches `repository`. The skill directory and frontmatter name must agree. Packaging includes `SKILL.md` and files beneath `agents/`, `references/`, `assets/` and `scripts/`. The hash covers relative paths, file contents and executable status; unrelated repository files are excluded. Symlinks within the skill and non-regular source files are rejected. The name check is an identity check, not full skill validation.

Install only on authorized machines and choose targets explicitly:

```bash
./scripts/install.sh --external-skill ~/.config/agent-config/external-skills/example.json \
  --cursor --claude --agents
```

Codex and Cursor normally share `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Existing destination overrides apply, and repeated shared destinations are installed once. External operations reject default target selection and `--all`; they cannot combine with rules, packages or catalog skills. No repository-level registration or installer linkage is needed for a standing rule to mention the skill or its service-discovery configuration.

Each installed folder has a distinct `.agent-config-external.json` receipt recording the owning repository/path, snapshot hash, file inventory, checkout path, Git HEAD and whether the skill has working-tree changes. An explicitly reviewed, hash-pinned working tree may be installed before its source is committed. HEAD alone is not claimed as the installed version. The receipt contains no credentials; keep credentials out of repository URLs and source resources.

## Update and remove

Update or recover the checkout through its owning project, review the new skill contents, run `pin` again, and replace the local config only with the intended source and hash. Repeat the explicit installation command. A missing checkout, wrong origin or hash mismatch aborts; the installer never fetches or chooses another source. Unrelated changes to the owning repository do not force a skill update. Moving the checkout is supported by changing `checkout` while preserving repository/path identity and the intended hash.

Updates remove retired files from the old receipt and preserve unrelated files and folders. All targets are checked before writes. A name already in the internal catalog, foreign destination, changed source identity, local edits to owned files, overlapping roots, or a duplicate in the selected harness's former native skill directory causes an error. Inspect and resolve the conflict explicitly; there is no force option. Changing the owning repository or skill path requires removal under the original config before installation under a new one.

Remove with the same local config and explicit targets:

```bash
./scripts/uninstall.sh --external-skill ~/.config/agent-config/external-skills/example.json \
  --cursor --claude --agents
```

Removal uses the installed ownership receipt and works when the checkout is unavailable. It deletes only unchanged owned files, the receipt, and resulting empty owned directories, preserving unrelated content. Already absent installations are harmless. Keep the config until all intended destinations have been removed, then delete it if no longer needed. If an owned installed file is missing or changed, preserve/recover that work and reconcile it with the receipt before retrying; removal does not discard local edits.

## Limits and verification

Content pinning detects a changed snapshot; it does not authenticate a repository owner or make skill instructions safe to execute. Local configs and receipts are trusted ownership records, not a security boundary against processes that can edit them. Explicit refresh adds a review step and means installed skills do not automatically receive owner updates. Review that trade-off if native cross-repository distribution becomes available or manual updates prove burdensome.

Destinations are staged before replacement and ordinary failures attempt rollback, retaining the backup path if recovery fails. This is not a crash-safe transaction across harnesses. Serialize installs/removals and avoid editing destinations during them. The isolated tests cover file distribution, failures, preservation and lifecycle behavior; they do not prove native discovery, activation, or skill effectiveness in each harness. Runtime builtin-skill inventories are not expanded by this feature; avoid choosing names used by native tools.

Run `python3 scripts/test-external-skills.py` for the focused suite and `./scripts/test-install.sh` for catalog/rule regressions. The source and maintained service documentation remain authoritative; installed copies are distribution artifacts.
