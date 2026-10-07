# Skills

Canonical Agent Skills for Cursor, Claude Code, and OpenAI Codex. [The catalog](skills.manifest) defines installed skills and [the package catalog](packages.manifest) defines cross-linked groups.

Skills live directly under skills/ or in a package directory. Supporting references, assets, scripts, and agent metadata live inside the owning skill and are installed with it. Shared repository scripts remain under scripts/ at the repository root.

## Install

From the repository root:

```bash
./scripts/install.sh
./scripts/install.sh --cursor --claude --agents
./scripts/install.sh --skills --package project-management
```

The default writes to the Claude and Codex skill roots. Select --cursor for the Cursor-native root. A full reinstall removes retired skills only when their ownership identifies this repository; unrelated skills are preserved. Package installs preserve managed skills outside the selected package.

See [project continuity](project-management/README.md) and [interview workflows](interview/README.md). Proofread has been retired and is no longer in the catalog.
