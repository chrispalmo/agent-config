# Allocating exploration across question layers

## Executive summary

Use a rough effort allowance across all layers, with different numbers of follow-ups for different questions. Begin with enough breadth to identify meaningful alternatives and decisive assumptions, then spend further investigation on branches most likely to improve the result, avert consequential rework, or answer useful objections. Close resolved branches and reuse shared evidence. Depth alone does not describe the amount or quality of preparation. The allowance is a planning judgment, not a spending controller; no numerical question counter or live billing monitoring is required.

Research on rational metareasoning, language-model search, adaptive inference, and source-grounded question asking provides useful mechanisms for allocation and stopping. It does not establish an optimal number of anticipated user questions for Concierge. The policy below is an adaptation to test through actual use, not a measured efficiency improvement. Return to the [Concierge workflow](../SKILL.md#activation-and-depth) for activation, authorization, and depth settings.

## What does the multiplication count?

For a fully expanded tree with branching factors `n1`, `n2`, and `n3`, the final layer has `n1 * n2 * n3` questions. Total questions across all three layers are:

```text
N = n1 + n1*n2 + n1*n2*n3
```

More generally, `N = sum over layers k of (product of n1 through nk)`. These formulas exclude the original request. They assume every parent at a given layer has the same number of children, without pruning or shared answers.

| Questions per parent at successive layers | Final layer | Total across layers |
| --- | ---: | ---: |
| 10, 10, 10 | 1,000 | 1,110 |
| 3, 3, 3 | 27 | 39 |
| 8, 3, 1 | 24 | 56 |

Real work need not form a complete tree. A question can be closed without children, several answers can share one investigation, and an unexpected finding can open a new branch. Use this arithmetic to notice an excessive branching plan; do not maintain a count of every imagined question. If a numerical comparison is useful or requested, distinguish distinct substantive questions from repeated links to shared answers, and include attempted investigations.

Question count is only a planning proxy. One question might require a short explanation; another could require a prototype or difficult experiment. Candidate evaluation, source reading, tool calls, verification, revisions, shared research, and writing explanations all consume effort beyond the nominal question count. Use trustworthy usage data already supplied by the execution system when relevant; describe estimates and unavailable measurements honestly. Do not equate a question, document, tool call, and model call, or invent token or monetary accounting from question counts.

## How should the agent choose an internal allowance?

Before substantial exploration, identify the important questions and roughly assess the work implied by the requested depth. Use the task characteristics below to judge whether a small investigation or sustained exploration is warranted. Keep this as an ordinary planning judgment; no numerical allowance, configuration interview, separate ledger, or extra budgeting process is needed.

| Task characteristic | Allocation implication |
| --- | --- |
| Narrow explanation with stable evidence | Few distinct questions; close the branch once the answer and relevant caveat are supported. |
| Comparison or design choice | Broader first layer covering materially different alternatives and the user's criteria; investigate disputed tradeoffs more deeply. |
| Build or reproduction | Include feasibility, the working flow, verification, and likely feedback; favor experiments that resolve several questions together. |
| Consequential or hard-to-reverse decision | Protect investigation of decisive assumptions, failure conditions, and disconfirming evidence before peripheral refinements. |
| Expensive or unavailable evidence | Use a bounded pilot or available fallback, and preserve the unresolved question with its consequence. More generated questions cannot replace access. |

Layer allocations can differ, but so can siblings within a layer. Do not require every layer to narrow: a finding may justify widening one branch. Reassess at meaningful findings or completed deliverables, rather than after every action. Ask whether the next investigation would improve the result, resolve a consequential uncertainty, or prepare a useful alternative. Group related questions into one investigation wherever practical.

Explicit user limits remain constraints. Exact token or monetary enforcement belongs in an execution system that supports it; the skill must not promise a hard ceiling from prompting alone. Use existing supported controls when available and authorized, and disclose unsupported guarantees. Do not scrape billing pages, repeatedly poll usage, or build monitoring infrastructure solely for this workflow.

## Which question deserves the next investigation?

Use expected contribution relative to marginal cost. The following criteria support a qualitative judgment; invented probabilities, utility scores, or a weighted total would imply calibration that is not available.

| Criterion | Observable basis and reason for using it |
| --- | --- |
| Decision sensitivity | Could a plausible answer change the chosen approach, acceptable scope, or recommendation? This prioritizes questions that affect action. |
| Consequence | What failure, delay, or rework could the answer prevent? This preserves consequential issues that may be unlikely to be asked aloud. |
| Likely user need | Does the request or earlier feedback make the question relevant? This favors prepared answers the user can actually use. |
| Remaining uncertainty | Is evidence missing, conflicting, stale, or untested? This directs work toward a resolvable gap rather than repeated explanation. |
| Distinct coverage | Does this add an independent alternative or challenge, or repeat known evidence? This limits confirmation bias and redundant breadth. |
| Marginal cost and reuse | What new research, execution, writing, and refresh effort is needed? Can one investigation answer several questions? This accounts for actual preparation cost. |

Start with a brief coverage scan before favoring the most promising branch. Preserve at least a relevant disconfirming perspective where a consequential recommendation could otherwise become one-sided. Generate later questions from the answers and evidence obtained, instead of inventing an entire recursive tree before researching. Some uncertainties need a sequence of checks: assess the bounded sequence as well as its first step, so that a short-term stopping rule does not discard valuable deeper work.

## What would an uneven allocation look like?

For an arithmetic illustration at depth three, investigate six first-layer questions. Expand four of them into three follow-ups each, adding twelve second-layer questions. Expand three consequential second-layer questions into two follow-ups each, adding six third-layer questions. That is twenty-four questions across unevenly expanded branches.

The numbers illustrate branching, not a required plan, counter, or recommended default. A meaningful result could require fewer questions or justify more investigation. One difficult experiment could cost more effort than all these questions answered from existing evidence. Depth three does not require every question to have grandchildren.

## How can the agent tell whether it is too shallow or too broad?

Preparation is too shallow when a decision-changing assumption, plausible alternative, consequential failure condition, or likely objection remains unsupported despite an affordable useful check. Add depth to an unresolved causal or implementation issue; add breadth when the alternatives or framing are incomplete. A confident-looking answer and a large question count do not establish sufficient coverage.

Preparation is becoming unproductive when branches repeat the same evidence, depend on premises already rejected, cannot affect the result or likely follow-up, or cost more to prepare and maintain than they plausibly save. Close or combine those branches. Low novelty alone is not a reason to skip an independent verification of a consequential claim.

Stop when the result is usable, important questions have adequate support or explicit limitations, and no available further investigation has a credible material benefit relative to its cost. Also stop at explicit review gates and known limits. If the effort allowance or an explicit limit is reached first, return the usable result and name the important unanswered question, its consequence, and the smallest useful next check. Stopping does not establish completeness. Explain names, sources, attempts, omissions, and reasons to the user; provide counts only when they help answer a question about allocation or cost.

## What research supports these choices?

**Rational metareasoning — choosing computation by decision value.** Hay, Russell, Tolpin, and Shimony's *Selecting Computations: Theory and Applications* (2012) formulates choosing further computation as a decision problem, balancing expected improvement in the final choice against computation cost. Sections 1–3 also show why a one-step policy can stop too early when useful evidence takes multiple computations. This is a theoretical foundation and includes experiments in selection problems and Go; it is not an evaluation of anticipating human follow-ups. [Paper](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf), [publication record](https://proceedings.mlr.press/r10/hay12a.html).

**STORM — asking better follow-ups at the same question count.** Shao and colleagues' *Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models* (2024) uses diverse perspectives and iterative, source-grounded question asking. Sections 3.1–3.2 describe the process; section 4.4 uses five additional perspectives plus a basic-facts perspective, with at most five rounds per conversation: up to thirty questions. This is a study setting, not an optimal allowance. Section 5.2 holds total questions equal across ablations; generating questions together without iterative conversation gives poorer outline coverage. The task is Wikipedia-like article preparation, not executive decision support. The paper also reports source-bias transfer and unsupported connections in generated writing. [Published paper](https://aclanthology.org/2024.naacl-long.347.pdf).

**Tree of Thoughts — generate candidates without fully expanding each one.** Yao and colleagues (2023) separate candidate generation, evaluation, retained breadth, and search depth. Their breadth-first method keeps a bounded set of promising states; their depth-first method prunes and backtracks. Sections 3–4 also show that imperfect pruning can discard a successful path. The paper studies Game of 24, creative writing, and mini crosswords with 2023 models; its settings are not validated question quotas for general research or current agents. [Methods and experiments](https://arxiv.org/html/2305.10601v2#S3).

**Adaptive test-time compute — allocation depends on the question.** Snell, Lee, Xu, and Kumar (2024) find that the useful balance between search and sequential revision varies with model-relative question difficulty and compute budget on MATH. Sections 3.2 and 8, and Appendix C, identify a significant caveat: estimating difficulty itself costs computation, which their allocation analysis does not fully account for. This supports task-dependent allocation as a design hypothesis, not a cheap or universally optimal difficulty classifier for Concierge. [Paper](https://arxiv.org/html/2408.03314v1).

**Graph of Thoughts — combine shared work.** Besta and colleagues model generated information as a graph, including aggregation of multiple paths and refinement, rather than requiring independent tree branches. Section 3 explains these transformations. Reusing one source investigation or explanation across several anticipated questions is an adaptation of that idea; the paper does not measure the savings for this workflow. [Graph model and transformations](https://arxiv.org/html/2308.09687v4#S3).

This is a focused review of allocation mechanisms, not a systematic literature review or a claim that no related research exists. The relevant introductions, methods, examples, and limitations above were inspected. No experiment comparing Concierge budgets, user-time savings, missed objections, or token usage has been run. Calibrating numeric allowances or claiming improvement would require representative use, measured cost including allocation overhead, and feedback on which prepared answers actually helped. Behavioral evaluation remains separate from drafting this guidance.
