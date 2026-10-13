# Challenge 06: AI for Everyday Life

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Build a helpful intelligent tool for an ordinary daily task, such as prioritizing
fictional chores, sorting synthetic shopping items or explaining a fictional study
schedule. Any language; AeglysAI integration is optional. Any framework and a
standalone local working prototype, MVP or proof of concept are acceptable.
Meaningful intelligent functionality may use explainable rules, optimization or ML;
a static page or hard-coded output alone is insufficient.

## Input contract and synthetic example

This example defines a small fictional task-planning input. `tasks` is a nonempty
array with unique, nonblank `id` values, nonblank `description` values, positive
integer `duration_minutes` and integer `priority` from 1 (low) to 5 (high).
`available_minutes` is a nonnegative integer. Reject invalid values and duplicate
IDs. Additional synthetic domains are welcome if their input/output contracts and
acceptance tests are documented. No real participant or household data is required.

```json
{
  "tasks": [
    {"id": "fictional-task-1", "description": "Review a synthetic study note", "duration_minutes": 15, "priority": 4},
    {"id": "fictional-task-2", "description": "Sort fictional shopping items", "duration_minutes": 10, "priority": 2}
  ],
  "available_minutes": 20
}
```

## Minimum acceptance criteria

Demonstrate actual executable behavior: read documented synthetic inputs and output
JSON recommendations linked to input IDs with a human-readable explanation of the
intelligent method. For this planning example, selected durations must not exceed
the available budget; report an empty recommendation when nothing fits. Explain
tradeoffs and limitations rather than claiming the example proves effectiveness.
Include an offline entrypoint, dependencies, installation/run instructions,
automated tests and deterministic reproduction instructions (fixed seed where
randomness is used). A different everyday-life domain must demonstrate equivalent
input validation, a measurable objective and explained outputs. Use separate
training/evaluation data if learning is involved; do not use evaluation labels as input.

## Suggested tests

Include normal, zero-budget, no-fitting-task and invalid-input cases. Test duplicate
IDs, missing fields, negative durations and out-of-range priorities. Check budget
constraints and reproducibility; compare against a declared simple baseline where
appropriate. No specific output or threshold is prescribed by the challenge.

## Safety and limitations

Use only synthetic data and follow the [safety guide](../SAFETY.md). Avoid personal
profiles, sensitive health/financial/legal decisions, production accounts or real
world automated actions. This challenge grants no exception to mandatory individual
prequalification and selection for every member, teams of 1–4, a maximum two-minute
video, or two-round judging. See [qualification](../QUALIFICATION.md),
[teams](../TEAMS.md), [submission](../templates/SUBMISSION.md) and
[judging](../JUDGING.md). No complete reference solution is supplied.
