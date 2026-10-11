# AEGLYSAI-013B — Project naming and domain migration

Date: 2026-10-11

Official project name: **AeglysAI — Adaptive Intelligence for Secure Distributed Systems**.
Website: [aeglysai.com](https://aeglysai.com).
Repository: [shubh-techie/AeglysAI](https://github.com/shubh-techie/AeglysAI).

Status: naming migration **IMPLEMENTED / TESTED** in the working tree, pending review.
Validation results are recorded below. Model D remains **PLANNED**. Existing
security/disclosure findings remain unresolved; this migration does not clear them.

## Audit before editing

Started from clean `security/AEGISAI-013-patent-safe-repository-hardening` at
`0256125`, following the approved current-tree cleanup. The remote already points
to AeglysAI. Created local `refactor/AEGLYSAI-013B-project-rename` from that commit;
no remote rename, commit, push or PR creation is part of this task.

The pre-edit textual inventory found old-name references in 118 tracked text
files: 2 top-level branding files (35 matches), 63 application/project files
(168), 14 tooling/build files (68), 37 documentation/research files (204), and
2 frozen environment files (161). This aggregate is an inventory, not a disclosure
assessment. ZIP artifacts were excluded from textual counting and preserved.
There were 11 projects, 14 namespace groups and 22 ignored bin/obj directories.

| Required category | Before | Treatment and current state |
| --- | --- | --- |
| Public branding | AegisAI README/agent guidance and project descriptions | AeglysAI branding and official supplied links in current guidance |
| Source/namespaces | AegisAI namespace root; AddAegisAuthentication extension | AeglysAI namespace root; AddAeglysAuthentication; type names otherwise preserved |
| Solution/project filenames | AegisAI.sln and 11 AegisAI project folders/files | AeglysAI.sln and 11 AeglysAI project folders/files |
| Build/deployment/workflows | Old project/DLL paths, tool temp names and AEGISAI_PORT | New paths/temp names; AEGLYSAI_PORT with legacy fallback; CI display rebranded |
| Documentation/research identifiers | Historical AEGISAI-001–013, SPEC/ADR references and docs/aegisai paths | Original IDs/paths retained; current summaries rebranded; migration guide under docs/aeglysai |
| Generated files | Ignored old bin/obj outputs | Removed only known ignored old outputs; build generates new assembly names |
| Historical/legal/disclosure material | Frozen results, historical snapshots, canonical research wording, private evidence and Git history | Preserved; canonical source-link targets now reference immutable pre-migration code |

No old public website domain was found in reviewed repository text. The old
synthetic issuer is under `.example.invalid` and is deliberately retained as a
trust identifier. The supplied website URL is a public link, not a JWT authority,
API audience, deployed endpoint or verified DNS/hosting migration.

## Compatibility assessment and transition

The repository contains no published-package configuration or known external
consumer declarations. Absence here does not prove no external users exist.
Namespaces, default assembly/package identities and build paths change: external
consumers must rebuild and update references. No binary compatibility shim or
type-forwarding assembly is supplied. Open `AeglysAI.sln` in the IDE after migration.
The renamed authentication extension requires updating callers during that rebuild.

Use the current solution and runner:

```sh
dotnet restore AeglysAI.sln
dotnet build AeglysAI.sln --configuration Release --no-restore
dotnet test AeglysAI.sln --configuration Release --no-build --no-restore
dotnet run --project benchmarks/AeglysAI.Experiments -c Release --no-build -- \
  --manifest research/experiments/smoke-v1.json \
  --output research/results/local-my-reproduction
```

The output must be a new directory. Local runs remain ignored and require review
before publication. This example is a reproduction instruction, not an executed
new research experiment. Existing source.zip files contain their original names:
extract them separately and use their included AegisAI.sln to reproduce those
historical snapshots. Do not edit archives or hashes to make them look renamed.

| External identifier | Compatibility treatment |
| --- | --- |
| API routes, HTTP/JSON contracts, configuration sections | Preserved, including Authentication, LocalDevelopment and authorization sections |
| Local JWT issuer/audience | Preserve `https://aegisai-local.example.invalid` and `aegisai-local-development`; do not widen token acceptance |
| Model/policy versions and synthetic run IDs | Preserved; no data/schema reinterpretation |
| ActivitySource/Meter name and telemetry keys | Preserve `AegisAI.Authorization` and `aegisai.*`; existing exporter/dashboard bindings continue |
| Port environment variable | `AEGLYSAI_PORT` takes precedence; unset/empty falls back to `AEGISAI_PORT`, then 5080 |
| Compose identity/derived local image tags | Preserve default `aegisai-local`; use AEGLYSAI_COMPOSE_PROJECT only for an explicit new-resource migration |
| Official dotnet image tags/framework | Preserve .NET 8 images, target framework and dependency versions |
| Git remote, branches, tags and historical commits | Unchanged except creation of the requested local work branch |
| GitHub checks | Build and test job label and security gate label remain stable; CI workflow display is AeglysAI CI |

No deployed resource was renamed or started/stopped. For an owner-approved local
resource transition, first stop the old project using its old name, then select
the new name for subsequent commands. Keep that selection consistent for up/down,
health, demo and experiments. Do not remove persistent volumes as part of branding.
An illustrative transition, **not executed by this task**, is:

```sh
AEGLYSAI_COMPOSE_PROJECT=aegisai-local ./dev down
export AEGLYSAI_COMPOSE_PROJECT=aeglysai-local
./dev up
```

## Preserved old-name references

- Historical AEGISAI task IDs, ADR/SPEC filenames, dates and original log entries.
- `docs/aegisai/`: stable historically referenced paths, including migration/history
  snapshots. Historical code links in the claims register/model definitions point
  to `0256125` rather than nonexistent old source paths in the current tree.
- Canonical research wording; no invention mechanism or claim was rebranded or
  expanded. The generic invention placeholder remains unchanged.
- `research/results/aegisai009-smoke` and `aegisai010-local-smoke`, their complete
  bytes, manifests, hashes, environment metadata and archived source names.
- Local trust strings, telemetry identifiers, legacy port alias and default Compose
  identity above. These are compatibility exceptions, not inconsistent branding.
- Original confidential evidence stays outside this repository. No private evidence
  is copied into migration documents or source files.

## Validation and open findings

Executed locally on macOS arm64 with .NET SDK 8.0.204 and Gitleaks 8.30.1:

| Check | Actual result |
| --- | --- |
| Restore AeglysAI.sln | Passed; all 11 projects restored |
| Release build, no restore | Passed; zero warnings/errors |
| Release tests, no build/restore | 168 passed: Domain 14, Application 53, integration/security 93, architecture 4, experiments 4; zero failed/skipped |
| Existing Python security suite | 16 passed; scanner failures remain fail-closed |
| New Compose compatibility tests | Five passed: default identity/port, legacy port, new-port precedence, empty-value fallback, explicit project-name opt-in |
| Docker Compose config | Passed; no deployed resource changes |
| References and documentation | All 11 project references, 14 namespace groups, local Markdown links/fences, shell syntax and Git whitespace checks passed |
| Proposed staged-change scan | Passed using the isolated index; no new blocked findings |
| Proposed tracked-content scan | Exit 1; existing reserved filename plus the two existing environment-metadata candidates |
| Reachable-history scan | Exit 1; preserved disclosure, local artifacts, credential/signing-material and metadata findings |

Naming tests can be repeated with `python3 -m unittest discover -s scripts/tests -v`;
they require the Docker Compose CLI and change no resources. The security suite
remains `python3 -m unittest discover -s scripts/security/tests -v` with the pinned
scanner on PATH.

The tracked scan used an isolated temporary index representing all proposed
renames, additions and deletions. The real index is untouched: a direct tracked
scan against unstaged old paths would report missing files. Stage the reviewed
rename before the final ordinary staged/tracked checks. The original solution CRLF is preserved; whitespace validation recognizes CR
line endings with a command-local `core.whitespace` option. No Git configuration
is changed. No scanner logic is
altered to overlook missing files. The history scan still covers all locally
reachable references; no Git history is rewritten by an alternate index.

No newly introduced unresolved validation failure was observed. Hosted CI, Docker
image rebuild/startup, external package consumers, exporter deployments and website
hosting/DNS are **NOT VERIFIED** by these local checks. No passing security
clearance is claimed.
All scanner configuration/rules and full reachable-history scanning remain active;
only scanner temporary-directory branding and public fixture naming changed.
No findings are allowlisted, baselined or suppressed.

The reserved invention filename still triggers the tracked confidentiality check,
even though its current contents are generic. Existing environment source-digest
false positives and preserved historical disclosure/credential findings remain.
Credential revocation, signing-key retirement, first public availability and
counsel's disclosure determination are **UNCONFIRMED / NOT VERIFIED**.

Exact retained finding paths, without values or invention detail:

- `docs/aegisai/research/INVENTION_CANDIDATES.md` (current reserved-name rule and
  historical snapshots including `02561254` and `bcd4f475`).
- The five historical `research/results/local-validation/` files at `bcd4f475`:
  environment.json, manifest.json, observations.jsonl, source.zip and summary.json.
- `GloboTicket.Services.Identity/tempkey.jwk` at `b9518fa5`.
- `GloboTicket.Client/Startup.cs` at `b9518fa5`.
- `GloboTicket.Gateway/DelegatingHandlers/TokenExchangeDelegatingHandler.cs` at `b9518fa5`.
- `GloboTicket.Integration.MessagingBus/AzServiceBusMessageBus.cs` at `b9518fa5`.
- `GloboTicket.Services.Order/appsettings.json` at `b9518fa5`.
- `GloboTicket.Services.ShoppingBasket/Helpers/TokenExchangeService.cs` at `b9518fa5`.
- `research/results/aegisai009-smoke/environment.json` at `ecb96495`.
- `research/results/aegisai010-local-smoke/environment.json` at `415efe65`.
- `research/results/local-validation/environment.json` at `98572c06`.

Abbreviated commits above identify scanner locations, not necessarily first
publication or introduction. Full private evidence remains external. Owner
credential retirement confirmation, counsel review and separately authorized
handling of verified metadata false positives/reserved-name policy remain open.

## Review and Git proposal

See the [exact change inventory](AEGLYSAI-013B-FILE-CHANGES.md).

Suggested commit: `refactor(branding): AEGLYSAI-013B standardize project naming and domain`.
Suggested PR title: `AEGLYSAI-013B: Migrate AegisAI branding to AeglysAI`.

The local branch includes the security-cleanup parent. If PR #12 remains unmerged,
review this as a stacked change against the security branch, or wait for that
branch's normal merge before choosing main as the PR base. No automatic history
rewrite/rebase, PR creation or publication is authorized.
