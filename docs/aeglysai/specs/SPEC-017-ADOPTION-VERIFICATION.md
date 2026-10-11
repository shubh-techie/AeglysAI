# SPEC-017 — COM-007A adoption contract

Date: 2026-10-11. Status: IMPLEMENTED locally; approval/publication pending.

## Scope

Implement public-safe documentation, schema 1.0.0, synthetic fixtures and offline
semantic validation. Read [contract documentation](../../../community/adoption/README.md).
The workflow is a contract/procedure, not a production service. No real participants,
independent adoptions, approvals or research metrics are claimed.

## Architecture and limits

See [architecture decision](../adr/ADR-011-ADOPTION-VERIFICATION.md). Domain/application .NET dependencies
are unchanged. Full-history findings remain publication blockers. Operator-owned
paths and human review cannot be supplied by an untrusted client. Source truth,
consent, independence and legal clearance are not established by JSON validation.

## Requirement-to-implementation traceability

| Acceptance requirement | Implementation | Automated verification |
| --- | --- | --- |
| Usage versus independent adoption/reproduction; classification | README.md; VERIFICATION.md; validate_adoption.py | `AdoptionTests.test_internal_usage_not_independent_adoption; test_affiliated_external_is_not_independent` |
| Source/commit/execution/citation provenance | PROVENANCE.md; adoption schema | `AdoptionTests.test_verified_requires_review; test_invalid_doi_reference` |
| Corrections, withdrawals and privacy-safe examples | fixtures; VERIFICATION.md; validator | `AdoptionTests.test_corrected_record_requires_superseded_prior; test_duplicate_and_cyclic_records_rejected; test_withdrawal_is_not_verified` |
| Engagement is not technical adoption | adoption schema | `AdoptionTests.test_engagement_and_person_fields_rejected; test_real_data_cannot_use_dummy_source` |

Run the task suite under `scripts/community/tests/` with the pinned environment.
Actual results and limits are recorded in `community/adoption/STATUS.md`.


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
