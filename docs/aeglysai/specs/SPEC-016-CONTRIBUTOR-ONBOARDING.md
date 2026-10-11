# SPEC-016 — COM-005 contributors contract

Date: 2026-10-11. Status: IMPLEMENTED locally; approval/publication pending.

## Scope

Implement public-safe documentation, schema 1.0.0, synthetic fixtures and offline
semantic validation. Read [contract documentation](../../../community/contributors/README.md).
The workflow is a contract/procedure, not a production service. No real participants,
independent adoptions, approvals or research metrics are claimed.

## Architecture and limits

See [architecture decision](../adr/ADR-010-CONTRIBUTOR-ONBOARDING.md). Domain/application .NET dependencies
are unchanged. Full-history findings remain publication blockers. Operator-owned
paths and human review cannot be supplied by an untrusted client. Source truth,
consent, independence and legal clearance are not established by JSON validation.

## Requirement-to-implementation traceability

| Acceptance requirement | Implementation | Automated verification |
| --- | --- | --- |
| Quick start, good first issues, lifecycle, hackathon transition | community/contributors/*.md | `RecognitionTests.test_onboarding_documents_complete` |
| Consent, artifact-only attribution and withdrawal | RECOGNITION.md; validate_recognition.py | `RecognitionTests.test_publication_requires_explicit_consent; test_withdrawal_requires_tombstone` |
| Versioned public-safe recognition contract | schemas/recognition-1.0.0.schema.json; fixtures | `RecognitionTests.test_positive_and_withdrawal_fixtures; test_negative_fixtures` |
| No invented awards, people or endorsements; no person fields | recognition schema | `RecognitionTests.test_no_person_fields; test_anonymous_still_requires_consent` |

Run the task suite under `scripts/community/tests/` with the pinned environment.
Actual results and limits are recorded in `community/contributors/STATUS.md`.


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
