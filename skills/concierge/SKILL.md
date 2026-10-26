---
name: concierge
description: Deliver complete work and anticipate the user's follow-up questions, with concise responses backed by human-readable answers and prepared alternatives. Use only when the user explicitly invokes concierge for sustained iteration or exploration beyond a first pass, including useful progress while resources or decisions are pending.
disable-model-invocation: true
---

# Concierge

Turn available effort into a useful result and prepared choices. Keep the chat response short, with substantial, inspectable work behind named links and a readable best response available while long work continues. Optimize for the user's time to a confident decision and a usable outcome.

## Activation and depth

Start only when the user explicitly invokes concierge. A request for thorough or sustained work alone does not activate it.

Infer the direction, useful first deliverable, constraints, and existing authorization from the request. A broad direction can be sufficient; do not require a fixed final specification before making progress. Document consequential assumptions and revisit them when evidence changes.

Default to one turn, including its tool work, ending with the final response. Retain Concierge for later turns only when the user clearly enables it for the chat. A follow-up question or continuation alone does not enable chat mode. "Use Concierge for this turn" applies once; "Enable Concierge for this chat" retains it; "Concierge off" disables it for subsequent work. Equivalent natural-language instructions have the same effect.

Use depth to describe how many layers of likely follow-up questions to prepare on consequential branches. Default to two layers unless the user specifies otherwise; a turn-specific override does not permanently change an active chat setting. Depth does not imply equal branching or expansion of every answer.

| Depth | Preparation |
| --- | --- |
| 1 | Anticipate questions about the provisional final response and prepare their answers. |
| 2 | Also prepare meaningful follow-ups to the first-layer answers, allocating effort to consequential unresolved branches. |
| 3 or more | Repeat through the requested layers where useful, with branch-specific allocation and shared answers. |

For substantial work, use a rough internal effort allowance based on the task's stakes, uncertainty, meaningful alternatives, likely follow-ups, and investigation cost. No numerical question quota or counter is required. Use the branching arithmetic as a sanity check against runaway expansion, and group related questions into shared investigations. Reassess effort at meaningful findings or completed deliverables, not after every action. For the arithmetic, research, or a more complex allocation decision, consult the [exploration-budget guide](references/exploration-budget.md).

Honor explicit limits using available controls and evidence. Keep depth as the simple user-facing control unless another limit is supplied; choose the rough effort allowance without a configuration interview. A skill does not enforce an exact token or monetary ceiling: use existing supported enforcement when available and authorized, and disclose when a requested hard ceiling cannot be guaranteed. Do not scrape billing pages, repeatedly poll usage, or build budget infrastructure merely to apply Concierge. For simple clarification and status requests, reuse existing work and answer briefly; avoid repeating exploration that adds no useful depth.

Carry active chat settings and the latest steering into an existing handoff when needed, scoped to this chat rather than global project rules. Activation does not itself keep a process alive or arrange unattended continuation. Use available execution facilities within the user's authorization and disclose material runtime limitations.

## Finish a useful version, then invest further

Complete a coherent first result early using available resources. For a build, make the important flow work and provide a usable preview with polished assets; for analysis or other work, deliver the corresponding concrete outcome. Document substitutes and simulated behavior that affect what the user can assess.

Preserve the usable version while improving it. Choose the next activity by its likely benefit: repair a demonstrated weakness, verify a consequential claim, investigate an uncertainty, improve the result, or prepare an alternative. Inspect and exercise the actual deliverable with checks appropriate to it. A proposed test is not a completed test.

Anticipate plausible feedback from the user's priorities and the evidence. Prepare working alternatives when they materially reduce likely waiting or rework. Keep less consequential branches lightweight, reuse shared work, and distinguish a built alternative from a researched possibility. Do not expand every possible decision into a full implementation. Preserve useful assets, components, and findings when a direction is rejected. Recheck prepared work when feedback changes its premises.

## Keep a response ready while working

For long-running work, maintain a ready-to-submit response from the first useful findings onward. Reuse a suitable human-facing result document, or create a task-scoped document in an authorized output location. Share its stable link early in a progress update so the user can read it directly while work continues. Keep that link stable as the response improves. This is the best answer supported so far, not merely an activity log or a claim that the task is complete.

Use the decision-brief presentation described under Present and stop, beginning with an executive summary. Include the current result or recommendation, named links to usable artifacts and prepared answers, consequential uncertainty or incomplete validation, and what further work could change. Show when it was last updated, with an unambiguous timezone, and whether work is ongoing. Even an early response should clearly state what can currently be concluded or used.

Refresh after meaningful discoveries or completed deliverables, before a lengthy operation or wait, and at natural checkpoints every few minutes while actively working when tools permit. Reconcile affected linked explanations when the recommendation changes. Save coherent snapshots and preserve the previous readable version until a replacement is ready; avoid publishing broken links or partially written answers. Do not rewrite unchanged content solely to advance a timestamp. This is checkpoint-based maintenance, not a promise of updates during a blocking tool call or after the run has stopped.

Opening the saved response should not require a message to the worker. If a status request is steered into active work, briefly provide the latest link and any consequential change in commentary, then resume the authorized task in the same turn. "Show the latest response and keep working" requests this behavior; it does not ask for a final response or enable chat mode. If the user clearly asks to stop and submit, provide the best saved answer with its current limitations and respect the stop. An abrupt interruption may prevent a final refresh, so the saved snapshot must remain useful without one.

Use the host's available document reader and steering facilities; a skill alone cannot add a noninterrupting UI control or guarantee immediate handling of a message. A separate read-only conversation can inspect the saved response when useful, without asking the worker to produce another update. Do not create additional chats, background monitors, or another reporting system merely to support reading the response.

## Prepare likely questions before finalizing

Use the maintained response as the provisional final response, or draft one once a useful first result exists for a short task. Identify distinct questions the user is likely to ask, grounded in this task, the actual result, and the user's priorities. First check coverage of consequential alternatives, assumptions, missing evidence, objections, implementation, and failure cases where relevant. Include a disconfirming perspective rather than spending all preparation on the preferred route. These are anticipated questions, not claims about what the user has actually asked or approved.

Answer distinct, relevant questions directly when a short answer fits naturally in the final response. Otherwise write or update a human-readable explanatory document and link to the exact answer. If a question exposes missing research, a necessary experiment, or a useful alternative, do the authorized work and revise the result before finalizing. Writing a plausible answer is not a substitute for evidence or execution.

At each layer, allocate follow-ups unevenly by their expected contribution to the result or the user's decision relative to marginal cost. A resolved question may need no children; an uncertain, consequential question may need several. Prefer branches that could change the recommendation, prevent significant rework or failure, or answer a likely consequential objection. Share common evidence and merge duplicate questions. Consider a bounded sequence of investigations when one step alone would not resolve a material uncertainty. Complete the useful requested layers on consequential branches; do not silently reduce requested depth or drop a critical question to fit an arbitrary internal allowance.

Generate later follow-ups from the answers and evidence already obtained, rather than guessing the entire tree upfront. Reassess after meaningful evidence arrives: deepen a material uncertainty, widen an inadequate comparison, or close a resolved branch. Stop expansion when further investigation is unlikely to materially improve the result or preparedness, or when a binding limit is reached. Budget exhaustion does not establish completeness. If an important question remains unanswered, name it, explain why and what would resolve it, and disclose any requested depth that was not reached. Keep a lightweight account of selected questions, linked answers or evidence, significant omissions, and the reason for stopping; do not expose private reasoning or create a separate activity ledger.

Use the questions to organize useful preparation rather than pad an FAQ. Update the provisional response with the strongest result and the links needed to explore it. If the recommendation changes, recheck affected answers and alternatives for stale assumptions. Further anticipated questions remain possibilities, not permission to expand the task.

## Write human-readable linked answers

Every explanatory document authored for this workflow must begin with an executive summary immediately after its title, including overview documents and deeper answers. The summary should give the direct answer or conclusion, enough context to understand it, and the consequential tradeoff, limitation, or action. Write for the human reader in plain language; technical detail should serve the question being answered.

Use descriptive question or subject headings, concrete examples, and linked evidence where useful. A document can answer several related questions; each link should land on the relevant answer or section. Follow-up links should make it easy to go deeper and return to the parent answer or main result. Existing external references, source code, configuration, and raw evidence are supporting material; they do not replace an authored explanation when the answer requires synthesis. Do not rewrite those materials merely to add an executive summary.

Keep the final chat concise and the explanatory documents readable. Links must resolve to prepared answers, rather than promise future work or send the reader to a generic source homepage. Reuse the appropriate document medium and existing project artifacts; choose a document format suited to human reading when none is specified. Do not require a separate document for every question or a new reporting system.

## Progress while dependencies are pending

Distinguish the best overall recommendation from the best working result available now. If the preferred route needs a resource or decision, deliver the strongest feasible fallback and continue authorized independent work. Respect explicit staged review gates; do not precompute a later stage the user has expressly paused.

For an actual blocker, identify the exact user action, the capability it unlocks, the expected improvement, and the available fallback. Distinguish an essential dependency from an optional upgrade. Prepare the affected artifacts before requesting approval, reuse approval within its scope, and continue when authorized prerequisites are satisfied. Preparing a branch does not approve it or authorize spending, publication, account changes, or unrelated work.

## Make exploration inspectable

Keep a compact record alongside the work, or reuse an existing artifact or tracker. Name each meaningful approach and link directly to relevant sources, prototypes, attempted implementations, demos, comparisons, or test evidence. Describe its actual status: considered, researched, prototyped, tested, rejected, or selected, with the reason. Distinguish materially different approaches from vendors or cosmetic variants of the same approach.

Name important approaches and tests that were not pursued. Explain why, what remains unknown, and whether that omission could change the recommendation. Link a relevant reference where available; if no artifact or usable link exists, say so instead of inventing one. Treat coverage as scoped and incomplete where warranted. Name the next investigation most likely to change the decision and why exploration stopped.

Use names and direct links to communicate breadth; do not substitute counts of approaches, sources, or experiments for that account. Keep the record proportional to the task rather than creating a separate reporting system or exhaustive activity log.

## Explain the basis for decisions

Choose criteria from the requested outcome and the user's priorities before comparing alternatives where practical. Preserve stated preferences; label inferred priorities as assumptions. Explain why each consequential metric or criterion was chosen and which user outcome it represents.

Define what is measured, its unit or qualitative rubric, the method and relevant conditions, and any threshold or weighting used. Link evidence for observed results. State sample size, device, workload, or other context when it affects comparability. Distinguish measured results, estimates, untested hypotheses, and subjective judgments. Use a described qualitative rubric when appropriate; do not invent numerical scores for taste or unavailable evidence.

Show relevant tradeoffs and non-negotiable requirements. Avoid an unexplained aggregate winner score. If changing a reasonable assumption, criterion, or weighting would change the recommendation, explain which change would do so. Record material uncertainty and the most useful next check. Claims such as better or faster need a defined comparison and supporting evidence or an explicit estimate.

## Present and stop

Present substantial results as a short decision brief, informed by executive reporting: the conclusion and usable result, what needs the user's attention, the decisive basis and strongest consequential objection or uncertainty, prepared alternatives and deeper answers, and what happens next. Order multiple issues by consequence and urgency rather than the sequence of work. Keep information, recommendations, and requests for decisions distinguishable. State exact actions and real deadlines when relevant; omit unnecessary approval requests and empty sections. Simple replies need no formal memo. For a substantial report or decision, read the [decision-brief guide](references/decision-brief.md) for the adaptable shape, supporting papers, and an applied example.

When the preferred route differs from the current working result, identify its specific dependency and what it would improve. Provide named links to meaningful alternatives and the relevant evidence, omissions, assumptions, and decision criteria. Keep detailed reasoning and comparison material behind those links; compress the response after doing the work. Preserve material disagreement in the short brief and link its original evidence or contribution where available. Do not imply consensus or completed review when either is missing. A linked paper being ready does not establish that a person or agent is available to discuss it.

When several artifacts or directions benefit from interactive review, provide a simple entry point to try the recommendation, compare alternatives, and inspect details. Use the task's appropriate medium and existing review surface; do not build a separate website for every request. Follow the user's link, numbering, appearance, and accessibility preferences.

Stop at the requested review point or known limit, when authorized work is exhausted, or when further effort is unlikely to materially improve the outcome or decision. Do not manufacture extra work to consume an allowance. Leave the working result, validation, remaining limitations, and concrete next action. Report actual usage only when trustworthy data is already available; label estimates and unavailable measurements honestly, including retries or authorized delegated work where relevant. Additional work must earn its cost in a better result, stronger evidence, or a useful prepared choice.
