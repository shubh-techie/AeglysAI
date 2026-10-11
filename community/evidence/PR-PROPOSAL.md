# COM-001: evidence contract

## Result

Governance, security boundaries, templates; Taxonomy, metric sources/periods/deduplication/verification; Strict schema and synthetic fixtures; Privacy, bounded fail-closed and redacted validation; Community index and COM-001 through COM-008 roadmap; Atomic byte-pinned snapshot integrity.

This change supplies repository documentation and offline validation, not a live
service or proof of real community outcomes. Fixtures are explicitly synthetic.

## Scope

See STATUS.md, the task specification and requirement-to-test traceability.
Dependencies: none. Review and merge prerequisites first. Shared governance
helpers belong to COM-001 and are not duplicated in this package.

## Validation

Task acceptance tests: 24 passed in the combined recovery environment;
the same suite passed in the isolated worktree. Scoped staged security/disclosure
scanning passed. Documentation was checked in the combined dependency snapshot. No hosted CI success
is claimed. Full tracked/history scans retain known publication blockers.

## Safety and publication

No secret scanner rule/history exclusion changed. No source or Portal application
behavior is modified. Human consent/provenance/publication approval remains required.
No commit, push or PR has been created.

Proposed commit: `feat(community): COM-001 establish governance and evidence standards`.


## Final review and participation amendment

Proposed PR title: COM-001: Establish community governance and evidence standards.

Clarifies individual versus team/project stage counts and privacy/publication boundaries. All existing schemas stay at 1.0.0. Event-stage reporting needs a separately versioned extension before Portal consumption. Task tests pass locally; full repository publication gates remain blocked. No PR, commit or push is authorized by this review.
