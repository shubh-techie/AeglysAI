# AEGLYSAI-DATA-001 review handoff

**IMPLEMENTED** offline synthetic dataset tools and reference recommendation rules.
**EXPERIMENTAL** benchmark results; production Model D remains **PLANNED**.

## Repository and preserved work

Verified origin `https://github.com/shubh-techie/AeglysAI.git`, HEAD
`70dd66c4df3540b0b47d5b229b744131d351b8d0`. Started on
`docs/AEGLYSAI-COM-RECONCILE-002-status-and-challenge` with 18 modified files and
one untracked community challenge. Created the requested branch
`research/AEGLYSAI-DATA-001-synthetic-security-dataset` without a commit.
All prior edits remain; the development log is shared and this task only appends
its dated entry. No Portal, production .NET, legacy tag/history or gate policy changes.

## Deliverables and assessment

- Architecture, full event schema and eight-family catalogue: [SPEC-019](../../docs/aeglysai/specs/SPEC-019-SYNTHETIC-BEHAVIORAL-DATASET.md).
- Isolation and contract decisions: [ADR-013](../../docs/aeglysai/adr/ADR-013-SYNTHETIC-BEHAVIORAL-RESEARCH.md).
- Generator/verification/training/evaluation commands: [README](README.md).
- Example files: [events](examples/smoke-v1/events.jsonl), [ground truth](examples/smoke-v1/ground_truth.jsonl), [manifest](examples/smoke-v1/manifest.json), 200 wholly synthetic windows.
- Actual metrics, versions, uncertainty and source: [result bundle](../results/acbsd-data001-smoke/README.md), [summary](../results/acbsd-data001-smoke/summary.json).
- Actual tests, timings, failed setup attempts and negative observations: [VALIDATION](VALIDATION.md).
- Dataset provenance/use limits: [dataset card](DATASET_CARD.md); protocol, leakage and RQ scope: [methodology](METHODOLOGY.md).
- Next research gaps: [roadmap](ROADMAP.md); requirements-to-tests: [traceability](TRACEABILITY.md).

Known-family test F1 is .9538 deterministic, .9858 Random Forest and .8197 Isolation
Forest. Random Forest holdout recall is 0; Isolation Forest benign-surge FPR is 1.
These failures remain reported. Test scores reflect an idealized, single-seed simulator
with shared entities/temporal ranges, easily interpretable features and 32% anomalies.
No production accuracy, patent novelty, safe containment or complete paper findings
are established. The framework supports exploratory behavioral detection and
recommendation correctness studies, limited parts of existing RQ1/RQ4. Full incident
response, RQ2 policy safety and RQ3 resilience require additional approved protocols.

## Final review checks and disclosure

Final local Markdown targets/fences, Git whitespace, example regeneration and
15 research tests pass. The unchanged gate passes a disposable staged snapshot
of all 43 task files (exit 0, .969526 s); this is a scoped scan, not full clearance.
Existing full tracked/history publication gates
remain FAIL (exit 1) on unresolved findings. New untracked task files were included in that disposable snapshot. No staging, exception or scanner-policy change is used.
Public-safe synthetic input does not establish repository-wide disclosure clearance;
human review of source/results, licensing and existing findings remains required.
No root license is present. Generated observations and predictions stay local except
for the small example and summary/source bundle. No real data or execution clients exist.

## Commit and PR plan — pending explicit owner authorization

1. Review this task's files and the dated development-log hunk only. Preserve the
   unrelated community changes; do not stage the whole dirty working tree or the
   whole shared development-log diff.
2. Resolve applicable existing publication blockers through owner-approved remediation;
   rerun unchanged staged/tracked/history gates. A scoped clean scan is not full clearance.
3. After explicit authorization, stage only the reviewed task scope and commit:
   `feat(research): AEGLYSAI-DATA-001 add synthetic behavioral security benchmark`.
4. Push the requested research branch and create PR only after explicit authorization.
   Title: `AEGLYSAI-DATA-001: Cloud-Native Behavioral Security Dataset`.
   Describe offline synthetic scope, label isolation, grouped holdout, actual results
   and negative observations, tests and unresolved publication limits. Merge/publish
   require separate explicit authorization. No history rewrite or force push.

## Exact task-owned changed-file list

These 43 paths are relative to the repository root. Generated source copies are
intentional reproducibility artifacts; local ignored runs and caches are excluded.
Pre-existing community edits are outside this task list. The development-log file
contains both pre-existing changes and this task's append.

- `.github/workflows/ci.yml`
- `README.md`
- `docs/aegisai/DEVELOPMENT_LOG.md`
- `docs/aegisai/architecture/RESEARCH_ARCHITECTURE.md`
- `docs/aegisai/research/RESEARCH_MODELS.md`
- `docs/aegisai/research/RESEARCH_PROGRAM.md`
- `docs/aegisai/research/RESEARCH_VARIABLES.md`
- `docs/aeglysai/adr/ADR-013-SYNTHETIC-BEHAVIORAL-RESEARCH.md`
- `docs/aeglysai/specs/SPEC-019-SYNTHETIC-BEHAVIORAL-DATASET.md`
- `research/README.md`
- `research/acbsd/DATASET_CARD.md`
- `research/acbsd/HANDOFF.md`
- `research/acbsd/METHODOLOGY.md`
- `research/acbsd/README.md`
- `research/acbsd/ROADMAP.md`
- `research/acbsd/TRACEABILITY.md`
- `research/acbsd/VALIDATION.md`
- `research/acbsd/__init__.py`
- `research/acbsd/benchmark.py`
- `research/acbsd/dataset.py`
- `research/acbsd/examples/smoke-v1/events.jsonl`
- `research/acbsd/examples/smoke-v1/ground_truth.jsonl`
- `research/acbsd/examples/smoke-v1/manifest.json`
- `research/acbsd/requirements.txt`
- `research/acbsd/risk.py`
- `research/acbsd/scenarios/v1.json`
- `research/acbsd/tests/test_benchmark.py`
- `research/acbsd/tests/test_dataset.py`
- `research/acbsd/tests/test_risk.py`
- `research/acbsd/verify.py`
- `research/results/acbsd-data001-smoke/README.md`
- `research/results/acbsd-data001-smoke/dataset-manifest.json`
- `research/results/acbsd-data001-smoke/source/__init__.py`
- `research/results/acbsd-data001-smoke/source/benchmark.py`
- `research/results/acbsd-data001-smoke/source/dataset.py`
- `research/results/acbsd-data001-smoke/source/requirements.txt`
- `research/results/acbsd-data001-smoke/source/risk.py`
- `research/results/acbsd-data001-smoke/source/scenarios/v1.json`
- `research/results/acbsd-data001-smoke/source/tests/test_benchmark.py`
- `research/results/acbsd-data001-smoke/source/tests/test_dataset.py`
- `research/results/acbsd-data001-smoke/source/tests/test_risk.py`
- `research/results/acbsd-data001-smoke/source/verify.py`
- `research/results/acbsd-data001-smoke/summary.json`
