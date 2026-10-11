# AEGLYSAI-COM-RECOVERY-001 — Research community handover

Date: 2026-10-11. Repository: shubh-techie/AeglysAI.

All five requested local implementations and acceptance suites are **IMPLEMENTED /
TESTED / READY_FOR_REVIEW**. Public release is **BLOCKED**, not complete: full tracked
and reachable-history gates still fail. No commits, PRs, pushes or merges were made.
No Model D, production account, live enforcement or Portal application work occurred.

## Preservation and separation

Verified the original 35-file dirty working tree at 6f24cd6 on the existing COM-008A
branch before editing. Preserved exact original bytes, SHA-256 manifest, status, diff,
refs and full base-commit metadata in owner-only durable local storage outside the
public repository. The private location is provided to the owner separately.
Original evidence schema 1.0.0, evidence tests and positive fixture remain byte-identical.
The earlier partial-sprint log is retained unchanged in the recovery tree as chronology.

Fetched verified remote main f2928136. Its committed tree equals the original local
base; no current source changes were lost. Kept the combined recovery snapshot on
recovery/AEGLYSAI-COM-RECOVERY-001. Four new task branches start at f2928136; the
existing COM-008A branch remains at 6f24cd6 with the identical baseline tree. All
have zero unique unrelated commits relative to main. No existing branch was rebased,
reset, force-moved, merged or cleaned. Local task review worktrees are external.

The package file lists below match actual worktree changes. Each has only its own
new files and append-only task log. COM-001 owns root navigation, generic CI tests,
governance index and roadmap. Other tasks own their own README/status/roadmap and
PR draft; they do not duplicate governance helpers. The two recovery reports are
recovery-only material and are not part of the five proposed task commits.

Dependencies are not secretly staged or committed: separate dependent worktree tests
use AEGLYSAI_COMMUNITY_ROOT pointing at the COM-001 worktree. A combined snapshot
validates all documentation links. After approved dependency merges, ordinary
repository-root defaults suffice. Do not publish a dependent PR before COM-001
is available on its approved base. Shared development-log appends may require a
normal merge conflict resolution later; preserve every entry and do not rebase.

## Task delivery matrix

| Task | Repository | Implementation | ADR/SPEC | Tests | Branch | PR | Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COM-001 | shubh-techie/AeglysAI | IMPLEMENTED / TESTED / READY_FOR_REVIEW locally | ADR-008 / SPEC-014 | 24 passed; staged gate passed | `docs/AEGLYSAI-COM-001-community-governance` | Not created; scoped draft provided | Full security gate, publication and required privacy approvals |
| COM-003A | shubh-techie/AeglysAI | IMPLEMENTED / TESTED / READY_FOR_REVIEW locally | ADR-009 / SPEC-015 | 4 passed; staged gate passed | `feat/AEGLYSAI-COM-003A-submission-templates` | Not created; scoped draft provided | Full security gate, publication and required privacy approvals |
| COM-005 | shubh-techie/AeglysAI | IMPLEMENTED / TESTED / READY_FOR_REVIEW locally | ADR-010 / SPEC-016 | 12 passed; staged gate passed | `feat/AEGLYSAI-COM-005-contributor-onboarding` | Not created; scoped draft provided | Full security gate, publication and required privacy approvals |
| COM-007A | shubh-techie/AeglysAI | IMPLEMENTED / TESTED / READY_FOR_REVIEW locally | ADR-011 / SPEC-017 | 13 passed; staged gate passed | `docs/AEGLYSAI-COM-007A-adoption-evidence` | Not created; scoped draft provided | Full security gate, publication and required privacy approvals |
| COM-008A | shubh-techie/AeglysAI | IMPLEMENTED / TESTED / READY_FOR_REVIEW locally | ADR-012 / SPEC-018 | 27 passed; staged gate passed | `docs/AEGLYSAI-COM-008A-reporting-contract` | Not created; scoped draft provided | Full security gate, publication and required privacy approvals |

## Executed validation

- .NET restore and Release build passed, zero warnings/errors.
- 168 .NET tests passed, zero failed/skipped: Domain 14, Application 53,
  integration/security 93, architecture 4, experiments 4.
- 80 community tests passed together; all five acceptance suites also passed in
  their isolated task worktrees with explicit COM-001 dependencies.
- Four schemas passed Draft 2020-12 meta-validation. Positive fixtures accepted;
  negative fixtures rejected. Pending reports reject publication mode; approved
  SYNTHETIC fixtures remain synthetic, not observed approvals or impact.
- 16 security tests and five Compose compatibility tests passed; Compose config,
  workflow YAML, Markdown local targets/fences and whitespace checks passed.
- Original evidence contract/test/fixture hashes unchanged. All intended source
  snapshots are eligible for Git inclusion; no ignore rules or exclusions changed.
- Every scoped proposed staged scan passed using a temporary alternate index.
  Every full proposed tracked scan returned exit 1 on known baseline findings.
  Full reachable-history scanning returned exit 1. Passing staged scans do not
  clear history, revoke credentials or establish legal disclosure approval.

Validation initially exposed a filename pattern rejecting JSON artifacts and the
existing artifacts/ ignore rule excluding intended monthly fixtures. Both were
corrected: validate safe JSON filenames and keep public synthetic snapshots under
fixtures/snapshots, with regression coverage. No broad ignore exception or forced
addition was used. These failures are fixed, not marked as passing earlier. A final integrity review
also removed a hash-then-reopen race: snapshot hashing and JSON parsing now use
the same bounded bytes, with concurrent-replacement regression coverage.

NOT VERIFIED: hosted CI, Portal end-to-end interoperability, live consent/withdrawal
operations, external source authenticity, real independence/adoption, dependency
vulnerability clearance, event results, website deployment or legal/security clearance.

## Validation commands

```sh
dotnet restore AeglysAI.sln
dotnet build AeglysAI.sln -c Release --no-restore
dotnet test AeglysAI.sln -c Release --no-build --no-restore
python3 -m venv /tmp/aeglysai-community-env
/tmp/aeglysai-community-env/bin/python -m pip install -r scripts/community/requirements.txt
/tmp/aeglysai-community-env/bin/python -m unittest discover -s scripts/community/tests -v
/tmp/aeglysai-community-env/bin/python scripts/community/validate_evidence.py community/evidence/fixtures/valid/synthetic-all-levels.json
/tmp/aeglysai-community-env/bin/python scripts/community/validate_recognition.py community/contributors/fixtures/valid/synthetic-recognition.json
/tmp/aeglysai-community-env/bin/python scripts/community/validate_adoption.py community/adoption/fixtures/valid/synthetic-integration.json
/tmp/aeglysai-community-env/bin/python scripts/community/validate_monthly.py community/reporting/fixtures/valid/synthetic-monthly.json --artifact-root community/reporting/fixtures/snapshots
python3 scripts/community/check_docs.py
python3 -m unittest discover -s scripts/security/tests -v
python3 -m unittest discover -s scripts/tests -v
docker compose -f deployment/docker/compose.yaml config --quiet
python3 scripts/security/scan.py tracked
python3 scripts/security/scan.py history
```

Install the existing checksum-verified scanner and put it on PATH as documented
in scripts/security/README.md. Full gate commands currently return 1, intentionally.
For isolated worktrees only, set AEGLYSAI_COMMUNITY_ROOT to the operator-controlled
COM-001 checkout; do not expose that path choice as Portal request input. Run each
worktree's test files listed in its task status. Reviewed proposed-tree scans used
alternate indexes; no real working-tree staging is performed by this handover.

## Security findings by category — redacted

- Current reserved disclosure filename: docs/aegisai/research/INVENTION_CANDIDATES.md;
  contents are the generic placeholder, but the path rule still fails.
- Current metadata credential candidates: research/results/aegisai009-smoke/environment.json
  and research/results/aegisai010-local-smoke/environment.json. No new exemptions
  or verified scanner-policy remediation is claimed.
- Preserved historical invention/artifact exposure: earlier candidate document and
  five research/results/local-validation files at bcd4f475; placeholder snapshot
  also reported at f2928136. These locations are not asserted first-public dates.
- Historical credential/signing-material candidates at b9518fa5: identity tempkey.jwk,
  client Startup.cs, gateway TokenExchangeDelegatingHandler.cs, messaging
  AzServiceBusMessageBus.cs, order appsettings.json and basket TokenExchangeService.cs.
- Historical environment candidates at ecb96495, 415efe65 and 98572c06.

No values, unpublished mechanisms or attorney communications are reproduced.
Credential revocation, signing-key retirement, historical exposure assessment and
counsel's disclosure determination remain UNCONFIRMED. Removing current files or
accepting a PR does not establish those decisions or restore historical novelty.

## Approval decisions needed

1. Review and approve the five local scopes/drafts before any commit, push or PR.
2. Resolve historical credential/signing retirement and legal disclosure decisions;
   separately authorize any justified narrow scanner-policy remediation.
3. Establish real consent/withdrawal reporting channels, retention policy, responsible
   reviewers and source/privacy/publication approvals before real evidence is collected.
4. Review licensing/provenance and real independent sources before making public claims.
5. Authorize normal prerequisite integration and shared-log conflict resolution when
   committing the prepared branches; no force push, rebase or history rewrite.

## Exact proposed commit and PR order

1. COM-001: `feat(community): COM-001 establish governance and evidence standards`. PR title: `COM-001: evidence contract`. Body: [scoped draft](evidence/PR-PROPOSAL.md).
2. COM-003A: `feat(hackathon): COM-003A define five-track submission contracts`. PR title: `COM-003A: hackathon contract`. Body: [scoped draft](hackathon/PR-PROPOSAL.md).
3. COM-005: `feat(community): COM-005 add contributor onboarding and consent contracts`. PR title: `COM-005: contributors contract`. Body: [scoped draft](contributors/PR-PROPOSAL.md).
4. COM-007A: `feat(research): COM-007A define independent adoption verification`. PR title: `COM-007A: adoption contract`. Body: [scoped draft](adoption/PR-PROPOSAL.md).
5. COM-008A: `feat(reporting): COM-008A add versioned monthly impact contract`. PR title: `COM-008A: reporting contract`. Body: [scoped draft](reporting/PR-PROPOSAL.md).

Review/merge COM-001 first, COM-003A next, then COM-005, COM-007A and COM-008A.
Prerequisite updates must be ordinary owner-authorized merges or new clean branches
at the approved base, never automatic history rewriting. The actual task branches
already exist locally; their scoped working changes are uncommitted. PR links and
merge dates do not exist for these proposed tasks and are not invented.

## Full file inventory by task

### COM-001 — 28 scoped paths

- `.github/ISSUE_TEMPLATE/community-task.md`
- `.github/pull_request_template.md`
- `.github/workflows/ci.yml`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `README.md`
- `community/README.md`
- `community/ROADMAP.md`
- `community/evidence/PR-PROPOSAL.md`
- `community/evidence/README.md`
- `community/evidence/ROADMAP.md`
- `community/evidence/STATUS.md`
- `community/evidence/fixtures/invalid/inconsistent-count.json`
- `community/evidence/fixtures/invalid/missing-definition.json`
- `community/evidence/fixtures/invalid/personal-data-field.json`
- `community/evidence/fixtures/invalid/reversed-period.json`
- `community/evidence/fixtures/valid/synthetic-all-levels.json`
- `community/evidence/schemas/evidence-1.0.0.schema.json`
- `docs/aeglysai/adr/ADR-008-COMMUNITY-EVIDENCE.md`
- `docs/aeglysai/specs/SPEC-014-COMMUNITY-EVIDENCE.md`
- `scripts/community/check_docs.py`
- `scripts/community/contract_tools.py`
- `scripts/community/requirements.txt`
- `scripts/community/tests/test_contract_tools.py`
- `scripts/community/tests/test_evidence.py`
- `scripts/community/tests/test_governance.py`
- `scripts/community/validate_evidence.py`
- `docs/aegisai/DEVELOPMENT_LOG.md`
### COM-003A — 17 scoped paths

- `community/hackathon/PR-PROPOSAL.md`
- `community/hackathon/README.md`
- `community/hackathon/REPRODUCIBILITY.md`
- `community/hackathon/ROADMAP.md`
- `community/hackathon/SAFETY.md`
- `community/hackathon/STATUS.md`
- `community/hackathon/templates/PROJECT-README.md`
- `community/hackathon/templates/SUBMISSION.md`
- `community/hackathon/tracks/api-traffic-watch.md`
- `community/hackathon/tracks/explain-security-alert.md`
- `community/hackathon/tracks/find-the-anomaly.md`
- `community/hackathon/tracks/predict-the-outage.md`
- `community/hackathon/tracks/smart-login-guardian.md`
- `docs/aeglysai/adr/ADR-009-HACKATHON-CONTRACTS.md`
- `docs/aeglysai/specs/SPEC-015-HACKATHON-SUBMISSIONS.md`
- `scripts/community/tests/test_hackathon.py`
- `docs/aegisai/DEVELOPMENT_LOG.md`
### COM-005 — 19 scoped paths

- `community/contributors/GOOD-FIRST-ISSUES.md`
- `community/contributors/HACKATHON-TRANSITION.md`
- `community/contributors/LIFECYCLE.md`
- `community/contributors/PR-PROPOSAL.md`
- `community/contributors/QUICKSTART.md`
- `community/contributors/README.md`
- `community/contributors/RECOGNITION.md`
- `community/contributors/ROADMAP.md`
- `community/contributors/STATUS.md`
- `community/contributors/fixtures/invalid/no-consent.json`
- `community/contributors/fixtures/invalid/withdrawn-credit-retained.json`
- `community/contributors/fixtures/valid/synthetic-recognition.json`
- `community/contributors/fixtures/valid/synthetic-withdrawal.json`
- `community/contributors/schemas/recognition-1.0.0.schema.json`
- `docs/aeglysai/adr/ADR-010-CONTRIBUTOR-ONBOARDING.md`
- `docs/aeglysai/specs/SPEC-016-CONTRIBUTOR-ONBOARDING.md`
- `scripts/community/tests/test_recognition.py`
- `scripts/community/validate_recognition.py`
- `docs/aegisai/DEVELOPMENT_LOG.md`
### COM-007A — 17 scoped paths

- `community/adoption/PR-PROPOSAL.md`
- `community/adoption/PROVENANCE.md`
- `community/adoption/README.md`
- `community/adoption/ROADMAP.md`
- `community/adoption/STATUS.md`
- `community/adoption/VERIFICATION.md`
- `community/adoption/fixtures/invalid/maintainer-not-independent.json`
- `community/adoption/fixtures/invalid/no-execution.json`
- `community/adoption/fixtures/invalid/unknown-relationship.json`
- `community/adoption/fixtures/valid/synthetic-integration.json`
- `community/adoption/fixtures/valid/synthetic-reproduction.json`
- `community/adoption/schemas/adoption-1.0.0.schema.json`
- `docs/aeglysai/adr/ADR-011-ADOPTION-VERIFICATION.md`
- `docs/aeglysai/specs/SPEC-017-ADOPTION-VERIFICATION.md`
- `scripts/community/tests/test_adoption.py`
- `scripts/community/validate_adoption.py`
- `docs/aegisai/DEVELOPMENT_LOG.md`
### COM-008A — 21 scoped paths

- `community/reporting/PORTAL-INTEGRATION.md`
- `community/reporting/PR-PROPOSAL.md`
- `community/reporting/README.md`
- `community/reporting/ROADMAP.md`
- `community/reporting/STATUS.md`
- `community/reporting/fixtures/invalid/incorrect-period.json`
- `community/reporting/fixtures/invalid/unapproved-publication.json`
- `community/reporting/fixtures/invalid/unknown-evidence.json`
- `community/reporting/fixtures/invalid/wrong-total.json`
- `community/reporting/fixtures/snapshots/monthly-revision-1.json`
- `community/reporting/fixtures/snapshots/source-evidence.json`
- `community/reporting/fixtures/snapshots/verified-synthetic-evidence.json`
- `community/reporting/fixtures/valid/synthetic-approved-monthly.json`
- `community/reporting/fixtures/valid/synthetic-monthly.json`
- `community/reporting/fixtures/valid/synthetic-revised-monthly.json`
- `community/reporting/schemas/monthly-impact-1.0.0.schema.json`
- `docs/aeglysai/adr/ADR-012-MONTHLY-REPORTING.md`
- `docs/aeglysai/specs/SPEC-018-MONTHLY-REPORTING.md`
- `scripts/community/tests/test_monthly.py`
- `scripts/community/validate_monthly.py`
- `docs/aegisai/DEVELOPMENT_LOG.md`

Recovery-only files: community/SPRINT-STATUS.md and community/RECOVERY-HANDOVER.md.
The shared development log appears in each task inventory with a different append;
these are not five copies of another task's change.

## PORTAL INTEGRATION CONTRACT

| Contract | Exact path | Version |
| --- | --- | --- |
| Base evidence | community/evidence/schemas/evidence-1.0.0.schema.json | 1.0.0, unchanged |
| Recognition | community/contributors/schemas/recognition-1.0.0.schema.json | 1.0.0 |
| Independent adoption | community/adoption/schemas/adoption-1.0.0.schema.json | 1.0.0 |
| Monthly reporting | community/reporting/schemas/monthly-impact-1.0.0.schema.json | 1.0.0 |

Authoritative envelope documentation: [Portal handover](reporting/PORTAL-INTEGRATION.md).
Register the base evidence schema under its versioned ID locally; resolve no remote
schema URLs. Consume version 1.0.0 with the matching semantic validator and pinned
approved source commit, snapshots and full revision history. Read exact raw bytes,
recompute SHA-256 and reject malformed/missing/escaping artifacts and unsupported
versions. Keep draft/verified evidence separate from pending/approved/withdrawn
report publication. Use server-owned reviewer authorization and human evidence checks;
a client-supplied approval flag is not authority.

Fixture paths: community/reporting/fixtures/valid/synthetic-monthly.json,
synthetic-approved-monthly.json and synthetic-revised-monthly.json. Their source
and prior-release bytes are under community/reporting/fixtures/snapshots. The
pending fixture MUST fail publication mode; all examples remain visibly SYNTHETIC.
No real approval, consent, independent adopter or metric improvement is asserted.

The Portal must distinguish source coverage/quality, preserve exact integers, exclude
withdrawn/draft material from verified public impact, retain immutable revisions,
and implement approved privacy/retention workflows separately. No Astro, Portal
application or deployed-resource dependency is introduced by these contracts.
