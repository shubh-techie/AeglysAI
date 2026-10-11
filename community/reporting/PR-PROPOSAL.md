# COM-008A: reporting contract

## Result

Reuse evidence 1.0.0 unchanged; separate monthly schema; Calendar periods, pinned snapshots, definitions/units/references; Aggregation, deduplication and coverage; Verification, quality and publication approval; Immutable revisions and historical reproducibility; Portal handover independent of frontend; privacy/bounded files.

This change supplies repository documentation and offline validation, not a live
service or proof of real community outcomes. Fixtures are explicitly synthetic.

## Scope

See STATUS.md, the task specification and requirement-to-test traceability.
Dependencies: COM-001. Review and merge prerequisites first. Shared governance
helpers belong to COM-001 and are not duplicated in this package.

## Validation

Task acceptance tests: 27 passed in the combined recovery environment;
the same suite passed in the isolated worktree. Scoped staged security/disclosure
scanning passed. Documentation was checked in the combined dependency snapshot. No hosted CI success
is claimed. Full tracked/history scans retain known publication blockers.

## Safety and publication

No secret scanner rule/history exclusion changed. No source or Portal application
behavior is modified. Human consent/provenance/publication approval remains required.
No commit, push or PR has been created.

Proposed commit: `feat(reporting): COM-008A add versioned monthly impact contract`.


## Final review and participation amendment

Proposed PR title: COM-008A: Add versioned monthly impact reporting contract.

Clarifies individual versus team/project stage counts and privacy/publication boundaries. All existing schemas stay at 1.0.0. Event-stage reporting needs a separately versioned extension before Portal consumption. Task tests pass locally; full repository publication gates remain blocked. No PR, commit or push is authorized by this review.
