# Maintaining agent guidance

Keep useful instructions small, internally consistent, and tied to observed needs. Change canonical source guidance first; generated installations are separate artifacts. Personal preferences remain deliberate choices rather than targets for automatic simplification.

The user requested an instruction, workflow, and maintenance audit. Harness compatibility and installer integrity are deferred until the next harness switch. An [initial bounded seven-skill behavioral pilot](audits/evidence/2026-10-23-skill-pilot/README.md) is complete; broader longitudinal behavioral evaluation remains deferred. Findings and the action queue live in the [audit report](audits/2026-10-07-instruction-and-workflow-audit.md). The accepted instruction and workflow redesign is implemented; the report records its evidence and closeout.

A later [selected native Claude/Cursor compatibility check](audits/evidence/2026-10-23-native-compatibility/README.md) covers explicit invocation, resource reads, two owned precedence cases and isolated install/uninstall preservation. Helper execution in the tested read-only modes, complete counter coverage and the broader compatibility/installer audits remain unverified by that pass.

The [bounded activation-signal comparison](audits/evidence/2026-10-23-batch5-activation/README.md) reuses those receipts and checks retained payloads against maintained archive adapters. It found no dedicated activation counter or payload-loss defect requiring repair. Documented native telemetry exports remain unvalidated locally; file reads and startup inventory do not establish complete usage counts. No continuous collector or longitudinal programme was started.

## Authority

| Subject | Canonical source |
| --- | --- |
| Available skills and rules | [Skill catalog](../skills/skills.manifest), [rule catalog](../rules/rules.manifest) |
| Package membership | [Package catalog](../skills/packages.manifest) |
| Shared operating guidance | [Repository agent guide](../AGENTS.md) |
| Instruction and workflow findings | [Audit report](audits/2026-10-07-instruction-and-workflow-audit.md) |
| Installation behavior | [Installer](../scripts/install.sh) |
| Cloud setup | [Cloud guide](../scripts/cloud/README.md) |

Do not add a second task ledger for the audit. Update the report's action queue when implementation or deferred work changes. A future project-management backend decision may replace that queue; migrate it once rather than maintaining both.

## Checks for source changes

Use a Python virtual environment for validation dependencies: `python3 -m venv .venv`, activate it with `. .venv/bin/activate`, then run `python3 -m pip install -r requirements-dev.txt`. Run these checks after changing a skill, rule, catalog, or package:

```bash
python3 scripts/check-content.py
python3 scripts/test-content.py
./scripts/test-install.sh
git diff --check
```

The [content check](../scripts/check-content.py) validates registered and unregistered source artifacts, duplicate paths and basenames, YAML syntax and duplicate keys, metadata identity and boolean types, paired cross-harness invocation controls, draft separation, scoped-rule metadata, package membership, and canonical compatibility shims. It checks that explicit-only descriptions state activation, but cannot establish full prose semantics, every prose link, external facts, harness discovery, or agent behavior. Installed resource copies and managed retirement are covered by the installer tests. The existing installer tests remain a regression baseline; running them does not complete the deferred installer audit.

Read the affected skill together with its related rules and templates. Check that descriptions and body triggers agree, existing authorization carries forward, explicit user intent wins, and concrete completion conditions are stated. Ask whether each added step prevents an observed failure or merely prescribes ceremony. Keep uncertainty and proposed decisions visible; do not claim behavioral gains from a static review.

When changing a workflow repeated in templates or reference documents, update every applicable copy in the same change. Prefer one procedural authority with small pointers elsewhere. Preserve established user preferences unless the user asks to change them.

## Review triggers

| Trigger | Work to perform |
| --- | --- |
| A recurring unnecessary stop, missed instruction, duplicated document, or false completion | Capture the prompt context, conflicting instruction, and consequence; make the smallest justified correction. |
| Skill or rule change | Run source checks and review affected rules, reference documents, and templates together. |
| Workflow or backend change | Choose one authority for tasks, handoff, decisions, and evidence; document migration and reversal before adoption. |
| Next harness switch | Resume the deferred compatibility and installer audits, including resource resolution, metadata semantics, built-in collisions, scoped rules, cloud setup, and install/uninstall lifecycle. |
| Behavioral evaluation explicitly resumed | Compare representative tasks with existing, minimal, and revised guidance; use repetitions for ambiguous differences. |

For continued maintenance, review instruction usefulness after roughly three months of active use or sooner when repeated friction appears. This is a suggested review cadence, not a scheduled automation or a requirement to interrupt unrelated work.

## External assumptions

Record evidence at the time it is checked. A supported claim needs a source, version or environment, verification method, and review trigger. Documentation supports documented behavior; runtime checks support observed behavior. Neither proves effectiveness by itself.

| Assumption | Evidence status | Next review |
| --- | --- | --- |
| Cross-harness discovery paths, precedence, and metadata semantics | Selected native Claude/Cursor invocation/resource cases checked; full counter coverage, Codex/cloud and broader precedence remain unverified | Observed mismatch, relevant harness change or next harness switch |
| Broad local/cloud installation and upgrade integrity | Selected isolated lifecycle/resource/foreign-preservation cases checked; broader local/cloud integrity remains deferred | Next harness switch |
| Instruction revisions improve agent outcomes | Hypotheses from static inspection | When behavioral evaluations resume |

Keep this small table until a compatibility review warrants a detailed support matrix. Do not turn dates into unconditional instructions to research or edit files before unrelated work. The existing bundled-name inventory and cloud guidance will be refreshed with the deferred harness review.

## Completion of a maintenance change

Record the concrete problem, changed instruction, checks run, and remaining limitations in the existing authoritative record. Show the source diff. Installing globally, adopting a new backend, or publishing changes is a separate action whose authorization comes from the user's request and the applicable repository rules.
