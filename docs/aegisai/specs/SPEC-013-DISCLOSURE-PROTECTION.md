# SPEC-013 — Repository security and disclosure protection

Date: 2026-10-11 | Task: AEGISAI-013

Status: safeguards **IMPLEMENTED / TESTED** locally, pending review and uncommitted.
Confidentiality audit **NOT CLEARED**. Hosted execution **NOT VERIFIED**.
AEGISAI-014–024 remain **PLANNED**, not started.

## Actual inspection baseline

Inspection began with a clean `main` at `37f37d9`; origin is the HTTPS repository
`https://github.com/shubh-techie/AeglysAI.git`. Existing local/remote-tracking refs
also include a later repository-name change at `64453b4`, outside main. No fetch,
checkout, merge or remote setting change occurred. All 27 locally reachable
commits were included in the history audit; local refs do not prove remote state.
The legacy tag still peels to `b9518fa`. Historical recovery remains unchanged.

AEGISAI-012 research definitions entered in `c8e6112`, merged in `ff37d4b`, and
are preserved by `research-baseline-v0.1`. Completion SPEC-012 and ADR-006 entered
in `8f638bf` and merged in `37f37d9`. All eleven canonical research documents
remain byte-identical to the research tag. Their pending-review wording records
historical task status, not an absence of these later commits.

| Capability | Observed implementation and boundary |
| --- | --- |
| .NET 8 Clean Architecture | Domain, Application, Infrastructure, API; four dependency-direction tests |
| Authentication | Real JWT bearer validation; issuer-qualified identity; server-owned context; local development public-key trust |
| A | Deterministic role grants; authenticated `/authorization/evaluate` |
| B | Mandatory A before equality-based ABAC; authenticated `/authorization/evaluate/model-b` |
| C | Mandatory B before fixed weighted contextual risk; authenticated `/authorization/evaluate/model-c`; missing indicators deny |
| Observation | Correlation identifiers, pseudonymized console audit, tracing/metrics; observer failures are best-effort and do not change A–C decisions |
| Experiments | Existing paired seeded A–C engine-only runner; warmup separated from measured repetitions; JSON/JSONL, environment metadata and source archives |
| D | No behavioral event store, feature pipeline, trained artifact, anomaly detector, behavioral fusion, D endpoint, enforcement or feedback implementation |

STEP_UP and LIMIT in C remain recommendations. There is no protected operation,
challenge verification or enforced rate control. Existing experiments have no
independent attack labels, FPR/FNR implementation or D row. Timing covers engines,
not HTTP, audit durability, enforcement or distributed services. No new experiments
were executed in AEGISAI-013.

The existing suite covers identity forgery, caller attributes/risk rejection,
mandatory policy denial precedence, unknown risk, invalid configuration and
best-effort audit failure, plus architecture and experiment counting. It has no
D telemetry tenancy/replay/freshness, model-load, enforced-control concurrency,
cooldown/hysteresis or D audit fail-safe tests. No line/branch coverage measurement
was executed; passing 168 tests does not establish complete security coverage.

## Artifact classification and audit outcome

Reviewed generic application code, synthetic configuration and baseline test
fixtures are public-development candidates, subject to normal staged review.
Existing invention-oriented research prose is **UNCERTAIN — human disclosure
review required**. Existing environment metadata, raw local observations and
source archives are also **UNCERTAIN**, not automatically approved evidence.
Historical credential candidates are **PROTECTED — human security review required**.
No suspected value is reproduced here; scanners print paths and short commits only.

Notable locations requiring review:

- `docs/aegisai/research/INVENTION_CANDIDATES.md` (introduced at `c8e6112`).
- `research/results/local-validation/` (tracked despite local-results exclusion).
- `research/results/aegisai009-smoke/environment.json` at `ecb96495`.
- `research/results/aegisai010-local-smoke/environment.json` at `415efe65`.
- `research/results/local-validation/environment.json` at `98572c06`.
- `GloboTicket.Client/Startup.cs` at `b9518fa5`.
- `GloboTicket.Gateway/DelegatingHandlers/TokenExchangeDelegatingHandler.cs` at `b9518fa5`.
- `GloboTicket.Integration.MessagingBus/AzServiceBusMessageBus.cs` at `b9518fa5`.
- `GloboTicket.Services.Order/appsettings.json` at `b9518fa5`.
- `GloboTicket.Services.ShoppingBasket/Helpers/TokenExchangeService.cs` at `b9518fa5`.
- `GloboTicket.Services.Identity/tempkey.jwk` at `b9518fa5`.

Path/commit references identify audit locations, not necessarily first introduction.
Scanner candidates may include false positives; validity, live credential use,
revocation and legal disclosure implications are **NOT VERIFIED**. No credential
was tested against external services. Full reports must be reviewed privately.
Related publication is stopped. No findings are hidden by a historical baseline.

## Implemented safeguards

Existing Git ignores are preserved. Narrow private directory/filename guards,
local cloud/SSH credential directories, secret report names, strong-name keys and
future local result directories are added. Already tracked files remain tracked;
force-add and unusual filenames still require the staged gate and human review.
Docker excludes those categories and invention-oriented research prose. Docker
ignores do not restrict the existing tools-container repository bind mount or
the source snapshot runner, which recursively includes C# files under source,
test, benchmark and deployment directories. Keep protected files outside the root.

[ADR-007](../adr/ADR-007-DISCLOSURE-GATES.md) records the gate boundary.
[Local instructions](../../../scripts/security/README.md) cover verified scanner
installation, explicit hook activation and staged/tracked/history checks.
The hook is supplied but **not installed**; existing local Git configuration is
unchanged. CI is fail-closed, uses read-only permissions and no artifact uploads.
No branch protection or required-check setting is assumed or changed.

## Executed validation

Environment: macOS arm64, OS 26.6, .NET SDK 8.0.204, Gitleaks 8.30.1,
local Docker server 29.6.2. Scanner archive checksum matched the upstream release.

| Check | Actual result |
| --- | --- |
| `dotnet restore AegisAI.sln` | Passed with permitted tooling access; initial sandboxed attempt stalled and was stopped |
| Release build, `--no-restore` | Passed; zero warnings/errors |
| Release tests, `--no-build --no-restore` | 168 passed: Domain 14, Application 53, integration/security 93, architecture 4, experiments 4; zero failed/skipped |
| Python security gate tests | 16 passed; actual scanner, index semantics, hook invocation, missing/wrong/failing tooling, forced additions, renamed files, deletion, private temp storage, ignore behavior and explicit classification versus generic guidance |
| Actual scratch Docker context test | 19 protected fixtures excluded, three public fixtures retained; synthetic data only, no external base image |
| Tracked gate | Exit 1; existing disclosure/local-evidence paths and environment metadata candidates require review |
| History gate | Exit 1; existing candidates across locally reachable history require review |
| Actual staged gate | Exit 0 on an empty index; does not certify unstaged new work |
| Proposed-change staged gate | Exit 0 with all 15 changed/new files staged in a disposable repository; real index untouched |
| Documentation/workflow checks | Local Markdown links, fences, changed-file whitespace, shell syntax, YAML parsing/structure and `git diff --check` passed |

Existing integration logs include expected rejected-request exceptions and local
Data Protection storage notices. Neither is a failed test or a production storage
guarantee. Scanner report/diagnostic data is suppressed and temporary. Archive
and encoding scanning is bounded; arbitrary prose, encrypted files and historical
binary content still require manual review. No patent-classification completeness
or legal conclusion is claimed.

## Human remediation checklist and continuation gate

1. Keep publication, artifact upload and new invention disclosures on hold.
2. Review candidate paths and history privately; distinguish genuine exposure
   from scanner false positives and synthetic fixtures without copying values
   into public issues or logs.
3. Confirm credential revocation/rotation through the owner; record confirmation
   privately. Do not probe live systems with historical values.
4. Obtain counsel's assessment of existing research disclosures, permitted public
   baseline scope and any required handling of already published material.
5. Preserve evidence and history. Any current-tree removal or narrow reviewed
   scanner exception requires a separate owner-authorized change. No automatic
   deletion, history rewriting, tag movement or remote modification is proposed.
6. Re-run staged, tracked and history gates; arrange owner-managed required checks
   and hook activation. Publication still requires explicit owner authorization.

Next incremental sequence, after Phase 1 clearance: public D contracts/specification;
synthetic telemetry and features; versioned statistical baseline; mandatory-policy
composition; isolated mock controls and feedback; extension of the existing runner;
security/architecture checks and factual research reporting. No private mechanism
is specified by this sequence. Stop any design portion requiring confidential
implementation and document only its approved interface and evidence gap.

## Reviewable change boundaries

Suggested commits, **not executed**:

1. `chore(security): add fail-closed secret and disclosure gates` — ignore files,
   `.gitleaks.toml`, `.githooks/pre-commit`, `.github/workflows/security.yml`,
   installer, scanner, tests and local instructions.
2. `docs(security): record AEGISAI-013 audit and publication hold` — generic policy,
   this specification, ADR-007, README and development-log status.

Exact file-change list (four modified, eleven added):

```text
.dockerignore
.gitignore
README.md
docs/aegisai/DEVELOPMENT_LOG.md
.githooks/pre-commit
.github/workflows/security.yml
.gitleaks.toml
SECURITY_AND_DISCLOSURE_POLICY.md
docs/aegisai/adr/ADR-007-DISCLOSURE-GATES.md
docs/aegisai/specs/SPEC-013-DISCLOSURE-PROTECTION.md
scripts/security/README.md
scripts/security/install-gitleaks.sh
scripts/security/scan.py
scripts/security/tests/check_docker_context.py
scripts/security/tests/test_scan.py
```

Protected local evidence contains only a redacted inventory and gate summaries;
no patent claims, private mechanism document, attorney communication or raw
credential copy was created. Storage is outside the repository with owner-only
permissions and is temporary; durable custody remains an owner-managed step.
