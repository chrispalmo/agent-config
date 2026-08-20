---
name: interview
description: >-
  Runs a structured, multi-turn interview to gather missing context for a
  decision or another skill's workflow. Use when the user directly invokes the
  interview skill and wants adaptive questioning before work continues.
disable-model-invocation: true
---

# Interview

This is a user-invoked workflow. Do not start it from ambient context, even when
an agent ignores the `disable-model-invocation` metadata extension.

Gather context efficiently across N rounds. Do not run `reverse-brief` unless
the user invokes it.

## Start

1. Parse optional arguments from the invocation, independent of agent syntax.
   Defaults: **2 rounds**, **10 questions per round**. Examples of argument
   text: `10 questions 2 rounds`, `15 questions`, `3 rounds`.
2. Infer the subject, pending decisions, and originating skill from the conversation.
3. Reuse facts already provided; do not ask the user to repeat them.
4. State the interview subject, planned rounds, and questions-per-round in one short line, then begin Round 1 immediately.
5. If no subject can be inferred, make the first round establish it. Do not spend a turn asking one setup question.
6. Tell the user they may say `DONE` or `STOP` to end, or optionally invoke
   `reverse-brief` to end and inspect the handoff.

## Interview protocol

- Run at most the configured number of rounds unless the user requests more.
- Ask the configured number of questions in every round you run.
- Put all questions for a round in one message.
- Number questions `<round>.<question>`: for round _r_ with _q_ questions,
  use `r.1`–`r.q`. Start each round at `.1`; do not reuse numbers.
- Keep each question focused. Combine tightly related subparts only when they
  can be answered together.
- Tell the user they may answer briefly, answer by number, or skip any question.
- Never chase every unanswered question. Treat omission as "no answer
  provided," not agreement, rejection, or permission.
- Offer concrete options, examples, or a recommended default when they reduce
  effort, while allowing free-form answers.
- Do not use a sequence of single-question turns.

## Round design (N rounds)

Treat rounds as a continuum from breadth → depth → convergence. Scale the
emphasis to the configured _N_:

| Phase of N           | Emphasis                                                                       |
| -------------------- | ------------------------------------------------------------------------------ |
| Early (near round 1) | Map the decision space; cover relevant areas only                              |
| Middle               | Probe consequential details, tensions, and high-impact gaps from prior answers |
| Late (near round N)  | Resolve decision-critical ambiguity; confirm priorities, defaults, next action |

Areas to draw from when relevant:

- desired outcome and success criteria
- users, stakeholders, and decision owner
- current state and motivation
- scope and non-goals
- constraints, dependencies, and fixed commitments
- alternatives already considered
- preferences and tradeoffs
- risks, reversibility, and failure tolerance
- timeline, budget, and available effort
- evidence, unknowns, and assumptions
- required deliverable and approval process

For N = 1, combine breadth and convergence in that single round. For N = 2, round 1 is mostly breadth; round 2 is mostly depth and convergence. For larger N, spread the continuum evenly; do not open broad new topics in late rounds unless prior answers reveal a material omission, or a previous answer reveals new information that warrants additional probing.

Do not repeat skipped questions unless the missing answer blocks the decision; if it does, reframe the question and explain briefly why it matters.

## Stop conditions

Stop before the final round when enough context exists to proceed confidently or the user asks to stop.

End the interview when the user says `DONE` (or equivalent) **or** invokes `reverse-brief`. Otherwise, after the final configured round, stop asking and remind them they may say `DONE` or invoke `reverse-brief`.

- On `DONE`: stop. Do **not** invoke `reverse-brief`. Resume the originating skill or task with what was gathered, or ask what they want next if standalone.
- On `reverse-brief`: stop and run the bundled `reverse-brief` sub-skill.
- Do not auto-invoke `reverse-brief` at any point.

Do not begin implementation during the interview unless the user explicitly asks to stop interviewing and proceed.
