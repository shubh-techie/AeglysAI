# SPEC-018 — COM-008A reporting contract

Date: 2026-10-11. Status: IMPLEMENTED locally; approval/publication pending.

## Scope

Implement public-safe documentation, schema 1.0.0, synthetic fixtures and offline
semantic validation. Read [contract documentation](../../../community/reporting/README.md).
The workflow is a contract/procedure, not a production service. No real participants,
independent adoptions, approvals or research metrics are claimed.

## Architecture and limits

See [architecture decision](../adr/ADR-012-MONTHLY-REPORTING.md). Domain/application .NET dependencies
are unchanged. Full-history findings remain publication blockers. Operator-owned
paths and human review cannot be supplied by an untrusted client. Source truth,
consent, independence and legal clearance are not established by JSON validation.

## Requirement-to-implementation traceability

| Acceptance requirement | Implementation | Automated verification |
| --- | --- | --- |
| Reuse evidence 1.0.0 unchanged; separate monthly schema | schemas/monthly-impact-1.0.0.schema.json; validate_monthly.py | `MonthlyTests.test_positive_fixtures_and_revision; test_unknown_status_and_version_rejected` |
| Calendar periods, pinned snapshots, definitions/units/references | monthly schema; validator | `MonthlyTests.test_calendar_month_and_december_boundary; test_definition_or_unit_change_rejected; test_embedded_record_cannot_diverge` |
| Aggregation, deduplication and coverage | monthly validator | `MonthlyTests.test_exclusions_and_count_arithmetic; test_duplicate_reference_does_not_double_count; test_full_coverage_claim_requires_source_coverage` |
| Verification, quality and publication approval | monthly validator | `MonthlyTests.test_draft_sources_cannot_be_promoted; test_incomplete_quality_blocks_approval; test_pending_rejected_for_publication` |
| Immutable revisions and historical reproducibility | revision history and byte-pinned artifacts | `MonthlyTests.test_revision_id_and_digest_are_verified; test_invalid_archived_aggregation_rejected_even_with_matching_hash` |
| Portal handover independent of frontend; privacy/bounded files | PORTAL-INTEGRATION.md; contract_tools.py | `MonthlyTests.test_traversal_and_symlink_escape_rejected; test_missing_snapshot_and_bad_hash_fail_closed; test_cli_redacts_failure_and_missing_dependency` |

Run the task suite under `scripts/community/tests/` with the pinned environment.
Actual results and limits are recorded in `community/reporting/STATUS.md`.


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
