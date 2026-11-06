# Qualification evidence: chalasanisreenivasulu2-glitch

## Environment

- OS: Microsoft Windows 11 Pro, version 10.0.26200
- Shell: Git Bash (MINGW64), bash 5.2.37; PowerShell as fallback
- Docker Desktop: Client 29.3.1, Server 29.3.1
- .NET SDK: 9.0.201 [C:\Program Files\dotnet\sdk]
- Git: 2.49.0.windows.1

## Build and test results

- `./dev up`: build succeeded, API started, `/health` returned `{"status":"healthy"}`.
- `./dev demo`: three model decisions returned with Correlation IDs; one DENY
  returned without one. See `qualification-logs/03-demo-attempt4.log`.
  - Model A, reports/read: ALLOW (`PermissionGranted`), correlation
    `897265a62cbd49679c1e78e0f8e00620`.
  - Model B, reports/read: ALLOW (RBAC and ABAC conditions satisfied),
    correlation `7556685cb4f441cd977de7cd86810c65`.
  - Model C, reports/read: STEP_UP (`AdditionalAssuranceRequired`), risk score
    0.300 (Medium), correlation `f2b03a0411d644a5a8d8791cf676fc44`. STEP_UP is
    returned as a decision with an obligation
    (`VerifyStrongerAuthenticationAndReevaluate`); the demo does not show
    enforcement of that obligation at the API boundary.
  - Model A, reports/write: DENY (`NoMatchingPermission`). No `Correlation`
    line precedes this decision in the log - the demo emits correlation IDs
    for ALLOW and STEP_UP outcomes but not for DENY. See line 11 of
    `qualification-logs/03-demo-attempt4.log`.
- `./dev test`: 168 passed, 0 failed across five assemblies
  (Architecture 4, Domain 14, Application 53, Experiments 4, Integration 93).
- `./dev experiment my-smoke`: 2400 attempts per model, 0 errors. Benchmark
  output saved to `qualification-logs/05-experiment.log`.

## Failed attempts and workarounds (Windows)

1. CRLF line endings broke `tools-entrypoint.sh` (`set: Illegal option -`).
   Worked around locally with `core.autocrlf input` and an LF conversion; not
   committed.
2. Git Bash rewrote `/local/token` into a Windows-style path. Worked around
   with `MSYS_NO_PATHCONV=1` and `MSYS2_ARG_CONV_EXCL="*"`.
3. A failed bind mount left a directory where a file was expected
   (`deployment/docker/.local/appsettings.Development.json`). Removed it and
   restarted.
4. `./dev demo` failed with `api:8080: Name or service not known` when the API
   container was down. Reordered to run `./dev up` first.
5. Secondary observation: the DENY decision on `reports/write` does not carry
   a `Correlation` field in the log, while ALLOW and STEP_UP decisions do.
   The DENY response itself is well-formed; this is a logging gap in
   `./dev demo`, not a decision-path issue.

## Architecture

From the build and demo output, the baseline is a .NET 8 three-model
authorization pipeline wrapped in Docker and driven by a `dev` script.

Layers (from the build output):

- `AeglysAI.Domain` - core entities.
- `AeglysAI.Application` - use cases.
- `AeglysAI.Infrastructure` - implementations.
- `AeglysAI.Api` - HTTP entrypoint on `:8080`.
- `AeglysAI.DevTools` - CLI used by `./dev` (`init`, `demo`, `test`, `experiment`).
- `benchmarks/AeglysAI.Experiments` - microbenchmark harness.

Request/decision flow (from the successful `./dev demo` output):

1. `./dev up` builds `aegisai-local-api` and `aegisai-local-tools`, creates the
   network `aegisai-local_default`, generates a synthetic one-hour credential
   at `/local/token`, and starts the API container on
   `127.0.0.1:5080->8080`.
2. `./dev health` returns `{"status":"healthy"}`.
3. `./dev demo` posts to `http://api:8080` with `/local/token` and returns
   three model outputs. Model A is RBAC only and permits `reports/read` with
   `PermissionGranted`; `reports/write` is denied with `NoMatchingPermission`.
   Model B adds an ABAC evaluation, returning an `abac` block with
   `ConditionsSatisfied`. Model C adds contextual risk, returning `STEP_UP`
   with `risk.score` 0.300, `level` Medium, `algorithmVersion`
   `contextual-weighted-v1`, five weighted signals
   (`AuthenticationWeakness` 0.25, `ResourceSensitivity` 0.25,
   `OperationSensitivity` 0.20, `NetworkExposure` 0.15, `DeviceExposure` 0.15),
   and obligation `VerifyStrongerAuthenticationAndReevaluate`.
4. Every ALLOW and STEP_UP decision carries a Correlation ID, which acts as
   the audit boundary. The DENY decision does not; noted above.
5. `./dev test` runs five test assemblies with 168 passing tests.
6. `./dev experiment my-smoke` emits a JSON benchmark: A 492k decisions/s,
   B 109k, C 67k, with a `Limitations` field explicitly disclaiming production
   claims.

The key architectural property: Model C separates deterministic policy
(RBAC to ABAC, ALLOW/DENY) from probabilistic risk (weighted score to
STEP_UP). The final outcome is policy-bounded - risk can only escalate to
STEP_UP and cannot override a DENY. This is the "AI advises, policy decides"
pattern.

## Technical observation

Observation: `./dev demo` on Windows under Git Bash fails on every attempt with
a path-translation bug that does not occur on Linux.

Evidence from the failed runs:

- `Could not find a part of the path '/tmp/tmp.XNodYVnN4v/C:/Users/Git/local/token'`
  - the container's `/local/token` was rewritten by MSYS path conversion into
  a Windows-style path embedded inside a Linux temp directory.
- `tools-entrypoint.sh: 2: set: Illegal option -` - the script shipped with
  CRLF line terminators (confirmed with `file`), so `set -eu` was parsed as
  `set -eu\r`.
- `Access to the path '/local/appsettings.Development.json' is denied` after a
  partial run left a stale artifact in `deployment/docker/.local/`.

Only after `export MSYS_NO_PATHCONV=1`, `export MSYS2_ARG_CONV_EXCL="*"`,
deleting the stale `.local/appsettings.Development.json`, and running
`./dev up` first did `./dev demo` succeed.

Why this matters: the baseline's developer entrypoint is not portable to
Windows, which is a meaningful fraction of hackathon participants. The failures
present as application errors rather than environment errors, and reaching a
green run required four workarounds and a manual cleanup step.

## Improvement idea

Scope: make `./dev` Windows-portable without changing any decision logic.

Three small, testable changes:

1. Normalize the entrypoint script in the repository. Add a `.gitattributes`
   rule (`deployment/docker/*.sh text eol=lf`) and a pre-build check in `dev`
   that fails fast with a clear message if any shipped shell script contains
   `\r`. `git config core.autocrlf` was set to `true`, which produced CRLF on
   checkout - an explicit attribute fixes it for every Windows contributor.
2. Set MSYS exclusions inside `dev` itself. At the top of `dev`, when `$OSTYPE`
   matches `msys|cygwin`, export `MSYS_NO_PATHCONV=1` and
   `MSYS2_ARG_CONV_EXCL="*"`. This removes the need for contributors to
   discover the workaround manually.
3. Make `dev demo` self-sufficient. Currently `demo` assumes `up` already ran
   and that `.local/token` exists; if not, it fails with a Docker DNS error
   (`api:8080: Name or service not known`) that hides the real cause. Change
   `demo` to (a) detect the absence of a running `aegisai-local-api-1` and
   invoke `up` first, and (b) `rm -f deployment/docker/.local/appsettings.Development.json`
   before `init` to clear stale artifacts.

Explicitly out of scope: the risk model, weights, policy versions, decision
outcomes, and the DENY correlation logging gap (the latter is noted as a
secondary observation, not part of this improvement).

## Engineering value

- Reproducibility. The qualification instruction is "demonstrate the baseline
  builds/runs." On Windows, that currently requires four undocumented
  workarounds. Fixing this turns a multi-attempt session into a single
  `./dev up && ./dev demo`. For a hackathon whose Round 1 depends on
  reproducible evidence, this is the highest-leverage improvement available.
- Failure clarity. The three distinct failure modes encountered
  (`set: Illegal option`, `C:/Users/Git/local/token`,
  `api:8080 Name or service not known`) all look like application bugs but are
  environmental. Better entrypoint checks convert each into an actionable
  one-line message instead of a stack trace.
- CI parity. The fix makes local Windows runs match the Linux CI path (the repo
  already has `ci/github-actions`). Contributors stop debugging their shell and
  start debugging the code.
- No risk to the security model. Nothing in the improvement touches the
  RBAC/ABAC/risk pipeline or the Correlation audit boundary, so it can be
  merged without re-validating any security claim.

## Validation approach

Three levels, all cheap.

Level 1 - Static (seconds). Add a test in `scripts/tests/` that greps every
`*.sh` under `deployment/` for `\r` and fails if found. Run it on a Windows
checkout with `core.autocrlf=true` - it must fail on the current `main` and
pass on the branch.

Level 2 - End-to-end on Windows (minutes). On a fresh clone, with no manual
exports and no pre-existing `.local` directory:

    git clone https://github.com/chalasanisreenivasulu2-glitch/AeglysAI.git
    cd AeglysAI
    ./dev up
    ./dev health
    ./dev demo
    ./dev test
    ./dev experiment my-smoke
    ./dev down

Success criteria: every command exits 0 with no `MSYS_*` exports and no manual
`rm -rf`. Compare the `./dev demo` output against the reference run in
`qualification-logs/03-demo-attempt4.log`. The three ALLOW/STEP_UP decisions
should match exactly apart from Correlation UUIDs. The DENY decision should
match exactly. If both hold, the improvement is behaviour-preserving.

Level 3 - Regression. Re-run `./dev test`. The baseline is 168 passing tests
across five assemblies (Architecture 4, Domain 14, Application 53,
Experiments 4, Integration 93). Any change in the test count means something
structural moved and must be investigated before the change is merged.

## Evidence

    qualification-logs/
      01-up-4.log                    green build
      02-health.log                  {"status":"healthy"}
      03-demo-attempt4.log           green demo (three models + one DENY)
      04-test.log                    168 passed
      05-experiment.log              microbenchmark JSON
      06-down-4.log
      03-demo-attempt1-api-not-running.log
      03-demo-attempt2.log
      03-demo-attempt3.log

The successful logs document a working build and run. The three
`03-demo-attempt*.log` files preceding attempt 4 document the failed runs
referenced in the Technical observation section.