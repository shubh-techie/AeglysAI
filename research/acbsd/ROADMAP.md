# ACBSD research roadmap

Date: 2026-10-13.

- **IMPLEMENTED**: version-1 catalogue, reproducible synthetic generation, strict
  validation, instance-grouped partitions, family holdout, separate provenance,
  detector feature allowlist, offline recommendation reference and tests.
- **EXPERIMENTAL**: deterministic/Random Forest/Isolation Forest benchmark with
  validation thresholds, per-family metrics, grouped uncertainty and scoring latency.
  Actual execution is recorded in [VALIDATION](VALIDATION.md) and the
  completed [DATA-002 50k report](DATA002_REPORT.md).
- **PLANNED**: multiple generator/model seeds, prevalence/range/context ablations,
  entity-disjoint splits, scenario mixtures, degraded operations and
  feature extraction from internally consistent synthetic raw event streams.
- **PLANNED**: verified literature review, licensing decision and human disclosure
  clearance before public release; unresolved repository security gates stay blocking.
- **PLANNED**: paper protocol freeze and independent review before confirmatory work.
  Model D authorization integration and confidential mechanisms are outside this task.

- **IMPLEMENTED (DATA-002)**: chronological partitions with window boundary gaps,
  verified physical split exports and feature-repetition diagnostics; 19 tests pass.
- **EXPERIMENTAL (DATA-002)**: one 50k seed, three completed benchmarks and declared
  recommendation-policy alignment. Model D input gaps are documented in the report.
