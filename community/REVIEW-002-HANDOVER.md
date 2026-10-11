# AEGLYSAI-COM-REVIEW-002 final handover

Local contract/documentation review, not a deployed event or Portal release. No commits, pushes, merges or PRs were created. Existing recovery backups remain intact.

## Mandatory participation contract

REGISTER → FORK AEGLYSAI → CLONE & RUN BASELINE → UNDERSTAND & DOCUMENT → SUBMIT SANITIZED QUALIFICATION EVIDENCE → ORGANIZER REVIEW → SELECTION → BUILD & COMPETE.

Every participant, including the lead, completes individual qualification; another member's evidence cannot substitute. Official registration Form, personal fork/branch URLs, architecture/setup understanding, observation, improvement and sanitized actual baseline build/run/test results are required. A/B/C understanding suffices; Model D is not required. Qualification never guarantees selection.

Teams have 1–4 individually qualified and selected members and exactly one lead. Private administration assigns unique team IDs, matches approved registration IDs and prevents duplicate active membership. An organizer publishes a dated, timezone-aware change deadline and reviews each change, including any exceptional late request. These are procedural requirements, not implemented database enforcement.

Each team chooses exactly one of five approved tracks. Any language/framework and standalone MVP/proof of concept/prototype are permitted after qualification. Require meaningful executable intelligent behavior and minimum acceptance criteria; no enterprise deployment or proprietary cloud requirement.

Final submission: private team ID and challenge, public source repository/commit, reproducible README, actual working demonstration, accessible video-file URL of at most 120 seconds, intelligent-method explanation, tests, licenses/attribution and limitations. App demo URL is optional; webcam footage and evidence uploads are not mandatory. Judging consent does not authorize publication.

Round 1 code/video shortlisting weights: 30/25/20/15/10. Round 2 Google Meet demo/Q&A ranking weights: 35/25/20/15/5. Each totals 100; rounds are not combined. Proposed finalists: 5–10 teams subject to capacity. Published tie-breaks, recusal, originality, disclosed AI assistance, licensed libraries and equivalent clarification procedures apply. Scores, private comments and participant mappings stay private.

## Validation and security

Community suite: 87 tests passed, including 11 COM-003A tests. Local Markdown targets/fences pass; remote URLs, anchors and live Forms are NOT VERIFIED. Four Draft 2020-12 schemas remain byte-for-byte unchanged at 1.0.0. .NET source/configuration is unchanged; .NET checks were not rerun in this documentation amendment.

Security tests: 16 passed. Scoped and combined staged scans pass. Full tracked/history scans fail with exit 1 on pre-existing findings; no bypass or suppression was introduced. Final scan receipts and exact scoped patches are stored privately outside Git.

Tracked findings: docs/aegisai/research/INVENTION_CANDIDATES.md (reserved path); research/results/aegisai009-smoke/environment.json and research/results/aegisai010-local-smoke/environment.json (credential candidates, not reclassified here).

Historical findings: invention/research evidence at bcd4f475; legacy signing-key and credential candidates at b9518fa5; environment artifacts at ecb96495, 415efe65 and 98572c06; current placeholder also encountered at f2928136. Counsel disclosure assessment, credential revocation and signing-key retirement remain UNCONFIRMED. Historical exposure has not been eliminated. No sensitive content is reproduced here.

## Task readiness and proposed PR order

| Task | Tests | ADR/SPEC | Branch | Proposed PR title | Status |
| --- | ---: | --- | --- | --- | --- |
| COM-001 | 24 | ADR-008 / SPEC-014 | docs/AEGLYSAI-COM-001-community-governance | COM-001: Establish community governance and evidence standards | READY_FOR_REVIEW locally; publication BLOCKED |
| COM-003A | 11 | ADR-009 / SPEC-015 | feat/AEGLYSAI-COM-003A-submission-templates | COM-003A: Define mandatory qualification and five-track hackathon contracts | READY_FOR_REVIEW locally; publication BLOCKED |
| COM-005 | 12 | ADR-010 / SPEC-016 | feat/AEGLYSAI-COM-005-contributor-onboarding | COM-005: Add contributor onboarding and consent-aware recognition | READY_FOR_REVIEW locally; publication BLOCKED |
| COM-007A | 13 | ADR-011 / SPEC-017 | docs/AEGLYSAI-COM-007A-adoption-evidence | COM-007A: Define independent adoption verification | READY_FOR_REVIEW locally; publication BLOCKED |
| COM-008A | 27 | ADR-012 / SPEC-018 | docs/AEGLYSAI-COM-008A-reporting-contract | COM-008A: Add versioned monthly impact reporting contract | READY_FOR_REVIEW locally; publication BLOCKED |

All five branches have scoped uncommitted changes and dependencies; no task PR links or implementation commits exist. COM-001 provides common helpers; merge/review dependencies first. Structured event-stage reporting is PLANNED, not completed.

Proposed commits, in table order:

- `feat(community): COM-001 establish governance and evidence standards`
- `feat(hackathon): COM-003A define qualification and team submission contracts`
- `feat(community): COM-005 add contributor onboarding and consent contracts`
- `feat(research): COM-007A define independent adoption verification`
- `feat(reporting): COM-008A add versioned monthly impact contract`

## Exact materially changed file inventory

### COM-001

- community/ROADMAP.md
- community/evidence/PR-PROPOSAL.md
- community/evidence/README.md
- community/evidence/ROADMAP.md
- community/evidence/STATUS.md
- docs/aeglysai/adr/ADR-008-COMMUNITY-EVIDENCE.md
- docs/aeglysai/specs/SPEC-014-COMMUNITY-EVIDENCE.md
- docs/aegisai/DEVELOPMENT_LOG.md (task-specific append)

### COM-003A

- community/hackathon/JUDGING.md
- community/hackathon/PR-PROPOSAL.md
- community/hackathon/QUALIFICATION.md
- community/hackathon/README.md
- community/hackathon/ROADMAP.md
- community/hackathon/STATUS.md
- community/hackathon/TEAMS.md
- community/hackathon/WORKSPACE.md
- community/hackathon/templates/QUALIFICATION.md
- community/hackathon/templates/SUBMISSION.md
- docs/aeglysai/adr/ADR-009-HACKATHON-CONTRACTS.md
- docs/aeglysai/specs/SPEC-015-HACKATHON-SUBMISSIONS.md
- scripts/community/tests/test_hackathon.py
- docs/aegisai/DEVELOPMENT_LOG.md (task-specific append)

### COM-005

- community/contributors/HACKATHON-TRANSITION.md
- community/contributors/PR-PROPOSAL.md
- community/contributors/ROADMAP.md
- community/contributors/STATUS.md
- docs/aeglysai/adr/ADR-010-CONTRIBUTOR-ONBOARDING.md
- docs/aeglysai/specs/SPEC-016-CONTRIBUTOR-ONBOARDING.md
- docs/aegisai/DEVELOPMENT_LOG.md (task-specific append)

### COM-007A

- community/adoption/PR-PROPOSAL.md
- community/adoption/README.md
- community/adoption/ROADMAP.md
- community/adoption/STATUS.md
- docs/aeglysai/adr/ADR-011-ADOPTION-VERIFICATION.md
- docs/aeglysai/specs/SPEC-017-ADOPTION-VERIFICATION.md
- docs/aegisai/DEVELOPMENT_LOG.md (task-specific append)

### COM-008A

- community/reporting/PORTAL-INTEGRATION.md
- community/reporting/PR-PROPOSAL.md
- community/reporting/ROADMAP.md
- community/reporting/STATUS.md
- docs/aeglysai/adr/ADR-012-MONTHLY-REPORTING.md
- docs/aeglysai/specs/SPEC-018-MONTHLY-REPORTING.md
- docs/aegisai/DEVELOPMENT_LOG.md (task-specific append)

## PORTAL INTEGRATION CONTRACT

Qualification: community/hackathon/QUALIFICATION.md and templates/QUALIFICATION.md.
Team eligibility and roster rules: community/hackathon/TEAMS.md.
Competition submission: community/hackathon/templates/SUBMISSION.md.
Scoring, originality and conflicts: community/hackathon/JUDGING.md.
Workspace/privacy boundaries: community/hackathon/WORKSPACE.md.
All are documentation contracts, not a participant API or authentication service.

Google Forms collect registration/submissions; private Sheets manage eligibility, teams/reviews/scores; private Drive holds supporting records; GitHub holds sanitized technical evidence/source; Meet hosts finalist demos; Portal publishes only approved event/results. No custom database or authentication service is required.

Existing schema versions and exact paths:

- community/evidence/schemas/evidence-1.0.0.schema.json — 1.0.0
- community/contributors/schemas/recognition-1.0.0.schema.json — 1.0.0
- community/adoption/schemas/adoption-1.0.0.schema.json — 1.0.0
- community/reporting/schemas/monthly-impact-1.0.0.schema.json — 1.0.0

Use schema AND semantic validation and owner-approved immutable source snapshots; see community/reporting/PORTAL-INTEGRATION.md for commands/fixtures and local reference registration. Never infer adoption from submission, finalists or winners. These schemas do not define dedicated event-stage fields; a separately versioned extension and migration review are required for that dashboard. Existing 1.0.0 contracts are locally reviewable; release and cross-repository integration are BLOCKED/NOT VERIFIED.

Pending organizer decisions: official Form URLs, event dates and team-change cutoff, eligibility/capacity, reviewer access/retention, consent/withdrawal and approved publication. Existing security findings additionally require credential/key and counsel decisions. No owner approval is inferred.
