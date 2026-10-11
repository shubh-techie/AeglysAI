# ADR-012 — Immutable monthly impact reporting

Date: 2026-10-11. Status: IMPLEMENTED locally; review and publication pending.

## Decision

Use public-safe versioned offline contracts and explicit human review boundaries.
Keep evidence version 1.0.0 unchanged and wrap it in a separately versioned reporting envelope with byte-pinned snapshots, explicit approval and immutable revision history.
No production account, external service, private evidence upload or Portal code
is connected. New contracts use schema plus semantic validation and redacted,
fail-closed CLI behavior. These are research repository tools, not .NET domain
services; Clean Architecture dependency boundaries are unchanged.

## Consequences and limits

Passing validation proves contract conformance, not consent, authenticity,
independence or legal/publication clearance. The owner must approve real data,
reviewers, privacy procedures and publication. Historical findings still block Git
publication. See [SPEC-018](../specs/SPEC-018-MONTHLY-REPORTING.md) and
[contract documentation](../../../community/reporting/README.md).


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
