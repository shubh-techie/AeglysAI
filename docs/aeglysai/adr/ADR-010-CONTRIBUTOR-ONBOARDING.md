# ADR-010 — Contributor consent and artifact recognition

Date: 2026-10-11. Status: IMPLEMENTED locally; review and publication pending.

## Decision

Use public-safe versioned offline contracts and explicit human review boundaries.
Recognition identifies artifacts, not people; consent is separate from technical acceptance and withdrawal minimizes public fields.
No production account, external service, private evidence upload or Portal code
is connected. New contracts use schema plus semantic validation and redacted,
fail-closed CLI behavior. These are research repository tools, not .NET domain
services; Clean Architecture dependency boundaries are unchanged.

## Consequences and limits

Passing validation proves contract conformance, not consent, authenticity,
independence or legal/publication clearance. The owner must approve real data,
reviewers, privacy procedures and publication. Historical findings still block Git
publication. See [SPEC-016](../specs/SPEC-016-CONTRIBUTOR-ONBOARDING.md) and
[contract documentation](../../../community/contributors/README.md).


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
