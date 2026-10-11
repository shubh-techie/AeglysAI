# ADR-008 — Public-safe community evidence contracts

Date: 2026-10-11. Status: IMPLEMENTED locally; pending review/publication.

## Context

Community activity is not interchangeable with independently verified technical
impact. Public evidence must be reproducible without collecting identities or
exposing restricted research. Existing history findings prohibit publication.

## Decision

Use five distinct levels with explicit units, definitions, periods, provenance,
deduplication and verification. Version a strict JSON Schema plus an offline Python
semantic validator. Reject unknown fields, duplicate IDs, bad periods, inconsistent
counts and draft records when verified evidence is required. Print only error
categories. Pin validator dependencies in a separate community requirements file.
Use synthetic fixtures exclusively for automated checks. Keep private evidence
outside Git and require human approval for real source and disclosure verification.

## Consequences

Schema conformance does not prove authenticity, independence or research impact.
Verified fields are review assertions, not cryptographic attestation. JSON fields
cannot establish reviewer truth; publication requires human source checks.
This is repository tooling and adds no domain/application dependencies to .NET.
See [SPEC-014](../specs/SPEC-014-COMMUNITY-EVIDENCE.md).


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
