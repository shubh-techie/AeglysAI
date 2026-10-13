# ADR-009 — Language-neutral synthetic hackathon contracts

Date: 2026-10-11. Original decision checkpoint: IMPLEMENTED locally; pending
review/publication at that checkpoint. See the reconciliation amendment below
for current published implementation and pending security-clearance status.

## Decision

One offering contains five beginner-friendly technical tracks. Any language and
optional AeglysAI integration keep the entry barrier low. Each track specifies
synthetic input, minimum criteria, suggested negative/edge tests and safety limits.
Participants choose their own method and thresholds; no complete solutions are
provided. Require offline reproduction and distinguish recommendation from actual
mock enforcement. Tests validate supplied inputs, documentation links and contract
coverage; they do not claim participant solution correctness.

## Consequences

These templates do not announce event dates, prizes or independent results.
Synthetic examples are not benchmarks of accuracy or effectiveness. Event operations
and the missing sprint packages require additional owner-supplied scope.
See [SPEC-015](../specs/SPEC-015-HACKATHON-SUBMISSIONS.md).


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Mandatory qualification, selected-competitor submission, two-round judging and private Workspace administration are documented. Official Form URLs and event eligibility/capacity decisions remain organizer prerequisites. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

COM-003A now requires individual prequalification for every member, teams of 1–4 with one lead, private roster approval and cutoff configuration, executable prototypes, accessible demo-video links, independent judging and separately handled publication consent. See QUALIFICATION.md, TEAMS.md, SUBMISSION.md and JUDGING.md in community/hackathon. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.


## 2026-10-11 — AEGLYSAI-COM-RECONCILE-002 amendment

The original five-track decision above remains historical. That implementation is
published on main `711c1556`; security clearance remains unresolved. The current
offering adds Challenge 06: AI for Everyday Life, an accessible synthetic everyday
task with an executable, explained intelligent prototype. This broadens topic
choice without changing individual qualification, teams of 1–4, the two-minute
video, judging or private Google Workspace administration. Any language/framework
and optional integration remain supported. All four evidence contracts stay 1.0.0;
no event-stage schema extension or Portal implementation is introduced.
