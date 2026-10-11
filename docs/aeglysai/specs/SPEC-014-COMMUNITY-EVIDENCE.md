# SPEC-014 — COM-001 community governance and evidence

Date: 2026-10-11. Status: IMPLEMENTED locally; validation in community sprint status.

## Contract and acceptance

Provide CONTRIBUTING, conduct policy, existing disclosure guidance, issue/PR
templates, community index and roadmap. Define Reach, Interest, Participation,
Contribution and Independent technical impact as separate levels. Every metric
requires definition, source, period, deduplication and verification method.

Evidence schema version 1.0.0 forbids undeclared fields and negative/noninteger
counts. Offline semantics reject duplicate metric IDs, invalid/non-aware or reversed
periods, inconsistent counts, source-kind mismatches and public dummy provenance.
Missing tooling/schema/input fails nonzero; diagnostics never print field values.
Synthetic fixtures do not demonstrate real community impact. Human review of source
bytes/digests, independence and public approval remains required.

## Verification

Tests cover all five levels, malformed fixtures, extra personal-data fields,
invalid periods, replayed IDs, deduplication arithmetic, private/credential URL
forms, missing tooling/schema, oversized input and redacted error handling.
A CI community test job validates these contracts without weakening the separate
security gate. See [evidence standard](../../../community/evidence/README.md),
[ADR-008](../adr/ADR-008-COMMUNITY-EVIDENCE.md) and
[task status](../../../community/evidence/STATUS.md).

## Limits

No participant database, telemetry collection or live analytics integration.
No claimed real source verification, moderation staffing, public release or impact.
Future schema changes must preserve original version semantics.

## Requirement-to-implementation traceability

| Acceptance requirement | Implementation | Automated verification |
| --- | --- | --- |
| Governance, security boundaries, templates | CONTRIBUTING.md; CODE_OF_CONDUCT.md; .github templates | `GovernanceTests.test_governance_evidence_and_templates_exist` |
| Taxonomy, metric sources/periods/deduplication/verification | community/evidence/README.md; evidence-1.0.0.schema.json | `EvidenceTests.test_all_five_levels_valid` |
| Strict schema and synthetic fixtures | community/evidence/fixtures; validate_evidence.py | `EvidenceTests.test_invalid_fixtures_rejected` |
| Privacy, bounded fail-closed and redacted validation | validate_evidence.py | `EvidenceTests.test_unknown_fields_rejected_at_every_boundary; test_cli_redacts_values_and_fails_closed` |
| Community index and COM-001 through COM-008 roadmap | community/README.md; community/ROADMAP.md | `GovernanceTests.test_roadmap_covers_all_eight_packages` |

Run the task suite under `scripts/community/tests/` with the pinned environment.
Actual results and limits are recorded in `community/evidence/STATUS.md`.

## Snapshot integrity acceptance

Shared snapshot helpers hash and parse one bounded byte buffer, preventing a
file change between hashing and parsing from altering the validated input.
SnapshotIntegrityTests covers concurrent replacement, duplicate keys and oversized
artifacts. The evidence schema and existing evidence tests remain unchanged.


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Event stages are explicitly distinct; competition success never establishes independent adoption. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

Reporting distinguishes individual qualification from team/project outcomes, keeps roster mappings private and separates publication consent from judging consent. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.
