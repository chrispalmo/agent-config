# Pinned template releases

Use the [template helper](../scripts/template.py) when creating a review from the reusable controls or explicitly updating an existing review. It uses Python 3.9+ on macOS/Linux, needs no dependencies or network, and discovers the local release catalog beside the installed skill. The current local release is [0.1.1](../assets/template-releases/0.1.1.json); [0.1.0](../assets/template-releases/0.1.0.json) remains available. Refreshing the installed skill makes additional releases available; it does not update existing reviews.

## Create or adopt a consumer

Run commands with the helper's actual installed or source path. For example, from this skill's directory:

```sh
python3 scripts/template.py list
python3 scripts/template.py init --dest /absolute/review/vendor/design-review --to 0.1.1
python3 scripts/template.py init --dest /absolute/review/vendor/design-review --to 0.1.1 --apply
```

`init` previews the files; `--apply` installs the exact release. Supply `--example` on both invocations to seed a complete fictional review in that directory. Otherwise supply your own renderer, content and layout using the [mount contract](footer.md). Keep the controls' relative imports together. The example's HTML, renderer and page CSS become app-owned files: the updater never owns or refreshes them.

For an existing exact copy, `adopt --dest DIR --to VERSION` checks every shared file against that release. Add `--apply` to record ownership without changing those files. Mismatching or missing files block adoption; resolve them in the owning source or initialize a separate resource directory and integrate it explicitly. Never infer a release from a filename, Git HEAD or approximate visual match.

## Check and update

```sh
python3 scripts/template.py check --dest /absolute/review/vendor/design-review
python3 scripts/template.py update --dest /absolute/review/vendor/design-review --to 0.1.1
python3 scripts/template.py update --dest /absolute/review/vendor/design-review --to 0.1.1 --apply
```

Only versions returned by `list` are available. `--releases /absolute/local/releases` selects another reviewed local catalog. `check` defaults to the newest locally available release, including retained releases; it makes no claim about upstream availability. `--to VERSION` chooses an exact target. All plans include release notes, compatibility, changed files, conflicts and a unified diff. `--json` provides structured output. Exit status 0 means a valid plan or successful operation, 2 means conflicts/incompatibility, and 1 means invalid input or an execution failure. Inspect `applied`/`wouldChange` to distinguish a dry run or no-op from an update.

Release **0.1.1** repairs standalone layout ownership: shared CSS supplies the grid, viewport height, preview scrolling and drawer box sizing. A docked drawer uses its wrapper's available height. Existing consumers with the documented three direct children can update the shared files without copying example styles. A surrounding navigation shell must allocate the remaining height as described in the [standalone layout contract](footer.md#standalone-layout); existing app height overrides are preserved. Live apps without the wrapper keep their layout. Mount API 1, saved state 3, export 4 and all review semantics are unchanged. The starter no longer duplicates the shared layout; existing starter/renderer files remain app-owned and are not rewritten by updates.

`check` and operations without `--apply` are read-only. Applying an update requires the task's authority to edit that consumer. Existing authorization carries forward; the helper adds no conversational approval gate. It rechecks the recorded shared-file hashes before writing, rejects changed/missing owned files and unowned filename clashes, applies the shared resource set together, and verifies written bytes before finishing. There is no force option or automatic merge. App-specific files, review IDs/versions, comments, approval snapshots, parameters and external service state are outside its write set. Run relevant browser and state checks in the owning app after applying and before publishing; the helper validates files/contracts, not arbitrary app behavior.

Mount/data contract changes or a major-version change stop the updater. Prepare those migrations in a separate source copy, preserve a real feedback export, and validate compatibility before switching the app. Layout changes may require a visible app-side integration even when shared code is compatible. For example, mobile header scrolling needs the standalone wrapper described in the mount contract.

## Receipts and recovery

Each consumer has `.design-review-template.json`, identifying the release, contract and shared-file hashes. `.design-review-template/` retains immutable release payloads, an ownership marker and an updater lock. Preserve both with the owning source. These are authoring metadata; the app need not load them or show version controls in its header.

```sh
python3 scripts/template.py rollback --dest /absolute/review/vendor/design-review --to 0.1.0
python3 scripts/template.py rollback --dest /absolute/review/vendor/design-review --to 0.1.0 --apply
python3 scripts/template.py recover --dest /absolute/review/vendor/design-review
```

Rollback uses retained bytes even when the original catalog is unavailable. It obeys the same local-edit and compatibility checks. It changes code only; it cannot reverse an incompatible shared-state migration. A failed ordinary write attempts to restore the preceding files/receipt. An interrupted write leaves a journal and blocks later updates until `recover` restores the preceding state. Recovery refuses to overwrite edits made after the interruption. Do not edit the same shared files while an update runs. The lock coordinates this helper's processes, not arbitrary editors, and the multi-file operation is not an atomic filesystem snapshot.

Hashes detect accidental corruption and changed content; they do not authenticate a publisher. Use a known source catalog. Symlinks and paths outside the flat shared-resource directory are rejected. The updater never fetches, runs package code, changes saved review data, installs global skills or publishes an artifact.

## Release policy

The initial local trial release is **0.1.0**. A template release covers the six shared runtime assets, their hashes, starter snapshots, notes and compatibility declarations. It does not version skill prose or the authoring helper itself. Shared controls have one version; avoid mixing individual files from different releases.

Patch releases repair behavior within the existing mount/data contract; minor releases add compatible features. Breaking contracts require a major release or an explicitly documented incompatible trial minor. Incompatibility must appear in the contract fields, not just the version label. Labels describe intent; app checks establish compatibility.

The template version is distinct from the review's `reviewVersion`, option source revisions, saved-state/export schemas, and Artifact Box code/state revisions. Header-only fixes do not invalidate a design approval. Changed designs still receive the appropriate review revision. Current contracts are mount API 1, saved state 3 and export 4. Pinned template files do not freeze the host's renderer/bridge runtime.

After reviewing and checking canonical assets, the maintainer creates a new immutable local release:

```sh
python3 scripts/template.py release --version 0.1.2 --note 'Describe behavior, compatibility and integration steps.'
python3 scripts/template.py release --version 0.1.2 --note 'Describe behavior, compatibility and integration steps.' --apply
python3 scripts/template.py verify --assets assets
```

The helper refuses an existing or older version. Preserve earlier releases; never rewrite their payloads. `verify` validates every catalog release and, with `--assets`, requires the newest one to match current runtime and starter sources. Update the compatibility constants when their contracts change. Repository checks include the focused lifecycle suite at `scripts/test-design-review-template.py`; the installer tests also exercise the distributed helper/catalog.

For layout changes, also run the repository's `node scripts/test-design-review-layout.cjs` with an available Playwright installation and Chrome. `PLAYWRIGHT_MODULE` may point to that installation and `PLAYWRIGHT_CHANNEL` selects an installed browser channel. Optional arguments select the runtime assets directory and an evidence directory. The fixture exercises standalone and nested layouts without fictional example CSS, existing height overrides, live-app flow, header scrolling, themes, text enlargement, resizing and the starter. It uses temporary browser contexts and closes the browser and loopback server when finished; it does not prove physical-phone or on-screen-keyboard behavior.

By default, checks run when requested. A future explicitly requested automation may call `check` or prepare a diff, but this workflow creates no schedules or update subscriptions. New reviews can select the newest installed release; existing ones remain pinned. Updating source, refreshing the installed skill and publishing a new Artifact Box bundle remain separate actions. Keep update notices in authoring tooling or catalog metadata.
