# ADR-013 — Isolated public-safe synthetic behavioral research

Date: 2026-10-13. Status: IMPLEMENTED offline research; EXPERIMENTAL evaluation.

## Context

The A–C .NET runner evaluates authorization decisions with simulated static context.
It has no independently labeled behavioral events. Model D behavioral research needs
reproducible anomaly and benign hard-negative observations while existing disclosure
constraints prohibit exposing confidential mechanisms and real data.

## Decision

Add `research/acbsd` as a standalone Python research package. Reuse existing
`research/` JSON/JSONL artifact conventions, explicit synthetic provenance,
refusal to overwrite results, ignored `local-*` runs, source hashes and versioned
specification. Do not reinterpret A–C DENY outcomes as attack labels or force the
C# authorization-observation contract onto behavioral windows. The existing planned
C# analysis interfaces remain untouched; no production project depends on Python.

Generate versioned observation windows, store labels/scenarios separately and use
an explicit inference allowlist. Group related rows before randomized splitting;
reserve one family entirely. Fit transformations on training only and choose
thresholds on validation only. Use standard-library generation and pinned
scikit-learn research baselines; no infrastructure, ingestion or Kubernetes client.

Provide a separate stateless evidence/asset recommendation reference. Its outputs
are review suggestions and carry no execution authority. Keep detector metrics,
recommendation correctness and authorization correctness distinct. Preserve all
existing secret/disclosure gates and require owner authorization for publication.

## Consequences

The framework can validate synthetic behavioral evaluation software and illustrate
failure modes, without claiming real effectiveness or implementing Model D.
Idealized features and overlapping temporal/entity distributions limit external
validity. Research results require their actual environment and source snapshot;
large local datasets remain ignored. No history or legacy changes are required.
See [SPEC-019](../specs/SPEC-019-SYNTHETIC-BEHAVIORAL-DATASET.md) and
[methodology](../../../research/acbsd/METHODOLOGY.md).

## DATA-002 extension — 2026-10-13

Provide an optional chronological split with 60-second boundary gaps, keeping the
existing random default. Related bursts remain grouped; entity-disjoint claims are
not supported. Allow repeated feature values at different timestamps and report
them separately from duplicate identifiers. Export verified partition artifacts
without fitting. Evaluate recommendations against an explicit synthetic policy
after inference; keep those expectations out of model inputs.

The [actual 50k report](../../../research/acbsd/DATA002_REPORT.md) records tests,
checksums and unfavorable model results. Raw Kubernetes/session generation and
real-world effectiveness remain missing/unverified; historical security gates fail.
