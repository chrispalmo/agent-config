# Execution and independence record

The human approved the four frozen prompts on 28 October 2026. The lead review is a fifth report, explicitly informed by earlier conversation context. No reviewer received the existing project-management package, proposed replacement, preferred name, seed bibliography, previous reviewer answer or conversation history.

## Isolation

Each reviewer ran as a new native CLI session in a different temporary workspace. Cursor used ask mode, sandbox enabled and separate supported configuration/data directories. Codex used read-only sandboxing, disabled memory use/generation, ignored user configuration, disabled apps/plugins/multi-agent features, disabled project-document injection and used separate SQLite state directories. Public web search was enabled only for literature assignments.

An outer macOS sandbox denied reading the repository tree, retained chat stores, unrelated personal skills and the other reviewer directories. Preflight probes demonstrated that the repository README was inaccessible while the assigned prompt was readable. The profiles are preserved alongside the workspace map. These controls protect separation from the discussion and peer findings; they are not proof that every unrelated file on the machine is unreadable, nor that provider/system instructions or training data are unbiased.

The prior-knowledge prompts explicitly invoked the frozen Bitter Lesson skill. This is a shared intervention, so those reports are **prior knowledge plus the requested skill**, not unprompted model beliefs. The literature prompts did not supply that skill or the hypothesis that simplification should win.

## Operational deviations

An initial process startup attempt failed before inference because its stderr descriptor pointed into the denied repository. Redirecting stderr to the isolated workspace resolved this; failed startup receipts are retained.

Astra's first prior-knowledge turn could not open the skill because macOS refused nested sandbox application. It produced no assessment. A new native session received the exact frozen skill and bundled essay inline; the delivered prompt is saved here. This preserved the sandbox and avoided substituting remembered skill content. Fable read the skill file but did not retrieve the optional essay, whereas Astra's inline attachment included both. This input difference limits strict comparability and is not concealed.

Codex reported that it could not read global AGENTS guidance, consistent with the intended block. It also reported native transcript persistence failures under the outer isolation. The orchestrator retained public streamed events, final responses and receipts outside the worker's readable scope. Native session IDs therefore identify executions; they are not promises of resumable sidebar chats. A hook timeout warning appeared, but no hook-supplied factual context is visible in the recorded stream.

## Model identity and billing

Fable's literature session reached Cursor's usage limit after collecting sources but before producing a report. The human then explicitly instructed Opus 5.5 to pick up where Fable stopped and stated that another $5 had been added for this continuation. The same isolated native research session was resumed with `claude-opus-5-5-xhigh`. This is an authorized model replacement, not an automatic fallback. Preserve the incomplete Fable attempt separately; the resulting literature report must be attributed to Opus using Fable's collected research, not presented as a completed independent Fable report.

The Opus continuation initialized as **Claude Opus 5.5 300K Extra High**, then returned an Opus usage-limit error without assistant text or a final report. No further inference retry was made. A read-only native account check confirmed the expected account. The error alone does not establish whether the extra allowance was consumed, unavailable to this route, or limited separately for Opus. The human subsequently declined further allowance and asked to close with the available results. The continuation is closed incomplete; the empty report is not counted as completion.

Cursor was explicitly invoked with `claude-fable-5-1-thinking-xhigh`; its runtime initialization identifies **Claude Fable 5.1 300K Extra High**. The catalog's larger advertised context label differs from the runtime label; the short prompts did not approach either limit. Codex was explicitly invoked with `gpt-6-astra` and `model_reasoning_effort="xhigh"`, with no fallback. Its public event stream does not independently attest the served model or effort; report these as the requested native configuration rather than a server-side attestation.

Native account authentication was used. The agent changed no billing settings, credit limits or subscriptions. No API-key route to a model provider or automatic model fallback was used. After the quota failure, inference resumed only following the human's explicit replacement instruction and added allowance. Receipts contain provider token accounting where supplied, not an invoice or an independently verified dollar charge. Do not equate cached/input/output fields across providers without checking their definitions.

## Preservation and interpretation

Public event streams exclude reasoning/thinking blocks. Initial substantive answers are preserved before synthesis, with hashes in the freeze manifest. Cursor emits both assistant text and a terminal result containing that text; the readable canonical report uses that terminal result once. The original combined capture is retained as an execution artifact, not counted as two responses.

The lead's initial review was frozen before it read peer answers. Agreement between the two prior-knowledge reports is model judgment conditioned on a shared prompt/skill. Agreement among literature reports may arise from overlapping studies. Neither constitutes new experimental replication. Source verification and corrections belong in the synthesis/verification record, not silent edits to initial reviewer answers.

## Icebox and cleanup closeout — 28 October 2026

The human iceboxed investigation and simplification until 2027, or earlier when both a significant new wave of frontier models arrives and access to the current frontier level of intelligence becomes substantially cheaper. The former reminder was deleted, with no replacement schedule or monitor. Task-owned temporary workspaces were removed after preserving the evidence in this packet; workspace paths in historical receipts describe where execution occurred and are no longer resumable locations. Native session IDs remain provenance only.

Raw event streams, stderr and the duplicated combined capture are retained locally and excluded from Git. The synchronized evidence includes original reports, frozen hashes, receipts, exact prompts, isolation profiles and public tool-action metadata. This avoids republishing fetched third-party page bodies and repetitive harness logs. The execution manifest identifies local-only artifacts separately.
