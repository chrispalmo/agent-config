---
name: proofread
description: Reviews prose in a worktree through a mechanical proofreading pass and an optional substance pass. Use when the user asks to proofread articles, documentation, pages, copy, or other prose; check spelling, grammar, style, outdated claims, broken links, or technical accuracy.
---

# Proofread

Review prose in a temporary worktree without silently broadening editorial
changes. Use two distinct passes so mechanical corrections do not get confused
with factual, historical, or opinionated changes.

## 1. Establish scope

1. Read the repository instructions and identify the authoritative source files,
   preview/build commands, and publishing boundary.
2. Confirm the content set, locale/style guide, and whether drafts are included.
   Preserve established regional spelling unless the project says otherwise.
3. Create a dedicated worktree when the review touches multiple files or the
   source branch must remain clean.
4. Do not publish, merge, remove the worktree, or delete the branch unless the
   user asks.

Use a temporary Markdown ledger. Do not create a JSONL tracker unless it
materially helps the task; for ordinary prose review, it adds noise rather than
decision value.

## 2. Mechanical pass

Read every in-scope document before proposing a complete ledger. Record spelling,
grammar, punctuation, typography, consistency, heading structure, and clearly
broken code examples separately from factual or opinionated concerns.

Create `PROOFREAD.md` in the project work area:

```markdown
| ID | File | Type | Status | Excerpt / issue | Suggestion |
| -- | ---- | ---- | ------ | --------------- | ---------- |
| API-001 | `content/post/api.md` | grammar | obvious | ... | ... |
| API-002 | `content/post/api.md` | style | unclear | ... | ... |
```

- Use stable `<FILE_PREFIX>-<NNN>` IDs so the user can select fixes in batches.
- Mark only unambiguous corrections as `obvious`; apply these without waiting.
- Mark choices about voice, regional language, brand casing, wording, or
  meaning as `unclear`; pause and ask for IDs or instructions.
- Never rewrite prose for taste alone.
- Commit the ledger only if the project workflow benefits from a durable review
  checkpoint. Otherwise keep it uncommitted for immediate review.

After applying approved fixes, verify the relevant build, tests, links, or local
preview. Delete `PROOFREAD.md` once the pass is accepted unless the user asks to
retain it.

## 3. Optional substance pass

Run this only when requested, or when the user asks about outdated, incorrect,
or disagreeable material. Do not mix its findings with the mechanical ledger.

Create `SUBSTANCE.md`:

```markdown
| ID | File | Kind | Status | Decision | Issue | Suggested direction |
| -- | ---- | ---- | ------ | -------- | ----- | ------------------- |
| SUB-001 | `content/post/deploy.md` | outdated | open |  | Describes a retired workflow as current. | Add dated context. |
```

Possible kinds: `outdated`, `incorrect`, `broken link`, `technical bug`,
`disagree`, `process`, or another precise label.

- Leave `Decision` empty for the user.
- Link file paths when the format supports it.
- Verify external claims and links before labeling them broken or outdated.
- Do not implement substance findings until the user supplies decisions.
- Interpret `fix`, `delete`, `ignore`, and `ok` literally; ask when a decision
  is ambiguous.

When material was true in its original context but is no longer current, prefer
preserving it with a concise dated note such as `> **Note (2026):** ...` rather
than rewriting history.

## 4. Close out safely

1. Show the exact files changed and the checks run.
2. Keep mechanical and substance diffs distinguishable until the user accepts
   both.
3. Remove temporary ledgers only after their decisions are applied or explicitly
   abandoned.
4. Clean the worktree down to accepted source changes before any merge.
5. Do not publish or deploy without explicit instruction.

## Handoff format

```text
Scope: <files reviewed and exclusions>
Mechanical: <obvious fixes applied; unclear IDs awaiting decision>
Substance: <not requested | ledger path and decision status>
Verified: <commands or preview URL>
Temporary artifacts: <ledgers retained or removed>
```
