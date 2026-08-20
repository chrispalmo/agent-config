# Audit rubric

Scoring standard for `project-audit`. Used to rate any repo's agent-continuity maturity.

## Checklist (weighted)

Weights are slices of a **100-point** total (not per-item grades).

| # | Artifact | Weight | Required? |
|---|----------|--------|-------------|
| A1 | README | 5 | Yes |
| A2 | VISION.md (or equivalent goals doc) | 10 | Recommended |
| A3 | IMPLEMENTATION_PLAN.md | 10 | Recommended |
| A4 | **IMPLEMENTATION_STATUS.md** | **25** | **Mandatory** |
| A5 | AGENTS.md (startup + doc authority) | 15 | Recommended |
| A6 | AGENTS.md session handoff / STATUS update protocol | 15 | Recommended |
| A7 | Decision log (in STATUS or separate) | 10 | Mandatory (embedded OK) |
| A8 | Research/docs directory | 5 | Optional |
| A9 | Workflow skill (optional, any agent) | 5 | Optional |
| | **Total** | **100** | |

`AGENTS.md` is the canonical shared surface for Cursor, Claude Code, Codex, and
similar tools. Cursor and Codex load it natively; Claude Code requires a
`CLAUDE.md` file that imports it with `@AGENTS.md`. Vendor-only rule files (for
example `.cursor/rules/*.mdc`) may count as **partial** credit toward A5/A6 if
they duplicate the same guidance, but full credit requires the shared substance
to live in `AGENTS.md`.

Compatibility is reported separately from the 100-point maturity score:

- **Shared guide:** `AGENTS.md` present
- **Claude Code bridge:** `CLAUDE.md` imports `@AGENTS.md`
- **Duplicate guidance:** absent (vendor files contain only vendor-specific rules)

## Conformance tiers

- **Full** (≥85): Greenfield production-ready for agents
- **Partial** (60–84): Usable but gaps cause agent confusion
- **Minimal** (<60): Fresh agents will struggle
- **Skip**: Intentional minimal (frozen, infra, fork, document delivery)

Tier gates override the numeric score:

- Missing or inadequate `IMPLEMENTATION_STATUS.md` or decision log: cap at
  **Partial**, because both are mandatory.
- Intentional frozen/minimal repositories and completed tools with no ongoing
  work: classify **Skip** rather than forcing the full rubric.

## Scoring model

| Symbol | Meaning | Points earned |
|--------|---------|---------------|
| ✓ / 🟢 | present and adequate | **full** weight |
| ~ / 🟡 | partial / acceptable equivalent | **~half** weight (round to nearest integer) |
| — / 🔴 | missing | **0** |

Always show both points and percent of total in Earned, e.g. `🟢 10 (10%)`, `🟡 15 (15%)`, `🔴 0 (0%)`.

## Acceptable equivalents

| Standard | Acceptable equivalent |
|----------|----------------------|
| VISION | `docs/vision.md`, `audit-charter.md` |
| STATUS | `state/STATUS.md`, `audit-status.md`, living plan current state |
| PLAN | `PLAN.md`, `docs/implementation-plan.md` |
| AGENTS handoff | Clear session-end STATUS protocol in `AGENTS.md` |

## Output format

```markdown
# Audit: <project>
**Tier:** <Full|Partial|Minimal|Skip> (<earned> / 100)
**Variant:** <greenfield|consulting|container|meta|minimal|tool>
**Compatibility:** AGENTS.md <present|missing>; Claude bridge <present|missing|not targeted>

Scoring: each row’s **Weight** is its share of 100. **Earned** counts toward the total (🟢 ✓ = full, 🟡 ~ ≈ half, 🔴 — = 0).

| # | Artifact | Weight | Found | Earned |
|---|----------|--------|-------|--------|
| A1 | README | 5 | ✓|~|— <short note> | 🟢|🟡|🔴 <points> (<points>%) |
| A2 | VISION | 10 | ... | ... |
| A3 | IMPLEMENTATION_PLAN | 10 | ... | ... |
| A4 | IMPLEMENTATION_STATUS | 25 | ... | ... |
| A5 | AGENTS.md startup + authority | 15 | ... | ... |
| A6 | AGENTS.md handoff | 15 | ... | ... |
| A7 | Decision log | 10 | ... | ... |
| A8 | Research/docs | 5 | ... | ... |
| A9 | Workflow skill | 5 | ... | ... |
| | **Total** | **100** | | **🟢|🟡|🔴 <earned> (<earned>%)** |

## Gaps (priority)
1. ...
2. ...

## Next
Invoke `project-bootstrap` to close gaps (omit if Skip / already Full).
```

## Retrofit playbook

For each project scoring <85:

1. **Assess tier** — minimal / partial / skip?
2. **Pick variant** — greenfield / consulting / container / meta / tool (see `variants.md`)
3. **Create STATUS first** (mandatory artifact)
4. **Backfill VISION + PLAN** from existing docs or chat history
5. **Add or expand AGENTS.md** with startup checklist and session handoff
6. **Add `CLAUDE.md` bridge** containing `@AGENTS.md` when Claude Code is in scope
7. **Migrate decisions** from chat/plan into STATUS decision log
8. **Set fresh-agent one-liner** in STATUS header
9. Remove obsolete vendor-only rule trees once `AGENTS.md` covers them

## Implementation order

```
1. project-audit     → assess repo
2. project-bootstrap → scaffold gaps found
3. status-ledger     → maintain every session
```
