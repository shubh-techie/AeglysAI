# SPEC-015 — COM-003A technical submission contracts

Date: 2026-10-11. Status: original five-track implementation published on main `711c1556`; sixth-track amendment implemented locally, security clearance pending.

## Acceptance

Provide Smart Login Guardian, Find the Anomaly, API Traffic Watch, Explain My
Security Alert, Predict the Outage and Challenge 06: AI for Everyday Life under one offering. All support any language
and standalone local programs. Every track includes valid synthetic input, goal,
minimum criteria, suggested tests and safe boundaries. Provide README/submission
forms, reproduction checklist and code/dependency safety guidance.

Minimum participant outputs are documented JSON decisions/flags/warnings/explanations
associated with input IDs or array indices. No fixed model, thresholds, final outputs
or complete reference implementation is supplied. Train/test separation and no
future-label leakage are required where applicable. No production accounts, logs,
network enforcement or confidential submissions are permitted.

## Verification and limits

Automated checks cover six distinct tracks, valid JSON examples, input contract
keys, required sections, templates and local links. Participant implementations,
event operations, submissions, judging and actual impact are NOT VERIFIED.
See [track index](../../../community/hackathon/README.md),
[ADR-009](../adr/ADR-009-HACKATHON-CONTRACTS.md) and
[task status](../../../community/hackathon/STATUS.md).

## Requirement-to-implementation traceability

| Acceptance requirement | Implementation | Automated verification |
| --- | --- | --- |
| Six language-neutral beginner tracks; integration optional | community/hackathon/tracks | `HackathonContractTests.test_exactly_six_distinct_tracks_and_runnable_json_inputs` |
| Synthetic inputs and acceptance/negative tests | community/hackathon/tracks | `HackathonContractTests.test_examples_have_expected_minimum_contracts` |
| README/submission/reproduction/safety templates | community/hackathon/templates; REPRODUCIBILITY.md; SAFETY.md | `HackathonContractTests.test_templates_checklists_and_safety_are_present` |
| Usable links, no complete solution | community/hackathon/README.md | `HackathonContractTests.test_all_local_community_markdown_links_resolve` |

Run the task suite under `scripts/community/tests/` with the pinned environment.
Actual results and limits are recorded in `community/hackathon/STATUS.md`.


## 2026-10-11 — AEGLYSAI-COM-REVIEW-002 addendum

Mandatory qualification, selected-competitor submission, two-round judging and private Workspace administration are documented. Official Form URLs and event eligibility/capacity decisions remain organizer prerequisites. Existing version 1.0.0 schemas are preserved. Structured event-stage reporting requires a separately versioned extension and migration review; it is not implemented here. Publication remains blocked by unresolved tracked/history security findings.


## 2026-10-11 — Final participation amendment

COM-003A now requires individual prequalification for every member, teams of 1–4 with one lead, private roster approval and cutoff configuration, executable prototypes, accessible demo-video links, independent judging and separately handled publication consent. See QUALIFICATION.md, TEAMS.md, SUBMISSION.md and JUDGING.md in community/hackathon. Existing 1.0.0 schemas are unchanged; structured event-stage reporting remains a planned versioned extension. Official Forms and deadlines are pending organizer configuration.


## AEGLYSAI-COM-RECONCILE-002 traceability

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Everyday-life intelligent working prototype and public-safe synthetic input | community/hackathon/tracks/ai-for-everyday-life.md | `HackathonContractTests.test_everyday_life_example_and_shared_submission_rules` |
| Sixth challenge selectable from current participant materials | README.md, QUALIFICATION.md, templates/PROJECT-README.md, templates/SUBMISSION.md in community/hackathon | `HackathonContractTests.test_sixth_challenge_is_listed_in_participant_contracts` |
| Existing individual qualification, roster, short video and two-round scoring preserved | QUALIFICATION.md, TEAMS.md, templates/SUBMISSION.md, JUDGING.md | QualificationComplianceTests and ParticipationAmendmentTests |

The sixth challenge is a local amendment, not yet published. The prior five-track
implementation is already public; existing security/disclosure failures remain
unresolved. Event Forms, deadlines and participant outcomes are not verified.
