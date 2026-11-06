# Qualification review: chalasanisreenivasulu2-glitch

## Problem and resulting behavior

**Problem.** The AeglysAI baseline ships a developer entrypoint (`./dev`) that
does not run cleanly on Windows under Git Bash. Four independent failures
occur before a green run is reached, and each presents as an application error
rather than an environment error.

**Resulting behavior.**

- `./dev demo` fails with
  `Could not find a part of the path '/tmp/tmp.<id>/C:/Users/Git/local/token'`
  â€” MSYS path conversion rewrites the container path `/local/token` into a
  Windows-style path embedded inside a Linux temp directory.
- `tools-entrypoint.sh` exits with `set: Illegal option -` â€” the shipped
  script uses CRLF line terminators, so `set -eu` is parsed as `set -eu\r`.
- After a partial run, `./dev demo` fails with
  `Access to the path '/local/appsettings.Development.json' is denied` â€”
  a stale artifact remains in `deployment/docker/.local/`.
- When the API container is down, `./dev demo` fails with
  `api:8080: Name or service not known` â€” a DNS error that hides the real
  cause (API not running).

**Secondary behavior observed.** The `Correlation` field is emitted for
ALLOW and STEP_UP decisions but not for the DENY decision on
`reports/write`. Line 11 of `qualification-logs/03-demo-attempt4.log`
contains the DENY response with no preceding `Correlation:` line.

## Task and scope

**Task.** Make `./dev` portable on Windows without changing any authorization
logic, and without changing the audit-boundary behavior of the risk pipeline.

**In scope.**

- Entrypoint script line-ending normalization in the repository.
- MSYS path handling inside `dev` for Windows shells.
- Self-sufficiency of `dev demo` when `dev up` has not run.

**Explicitly out of scope.**

- The RBAC / ABAC / risk pipeline.
- Policy versions, weights, decision outcomes.
- The DENY correlation logging gap â€” retained as a secondary observation,
  not addressed by this task.

**Non-goals.** Not a security review. Not a production hardening task. Not a
change to any published contract.

## Implementation and tests

| Change | Status | Evidence |
|---|---|---|
| Document the four Windows failure modes in the qualification record | IMPLEMENTED | `community/qualification/chalasanisreenivasulu2-glitch.md`, section "Failed attempts and workarounds" |
| Capture green build + demo + test logs | IMPLEMENTED | `qualification-logs/01-up-4.log`, `03-demo-attempt4.log`, `04-test.log` |
| Add `.gitattributes` rule (`deployment/docker/*.sh text eol=lf`) | PLANNED | Not yet committed â€” described in the Improvement idea section |
| Add pre-build CRLF check in `dev` | PLANNED | Not yet committed |
| Set `MSYS_NO_PATHCONV=1` and `MSYS2_ARG_CONV_EXCL="*"` inside `dev` | PLANNED | Not yet committed |
| `dev demo` self-sufficiency (auto-`up`, stale artifact cleanup) | PLANNED | Not yet committed |
| Three-level validation plan (static + end-to-end + regression) | PLANNED | Described in the Validation approach section |
| Baseline build (`./dev up`) | TESTED | `01-up-4.log`, 5439 bytes, ends with API started |
| Baseline demo (`./dev demo`) | TESTED | `03-demo-attempt4.log`, 1988 bytes, contains 3 ALLOW/STEP_UP Correlation lines and 1 DENY line |
| Baseline test suite (`./dev test`) | TESTED | `04-test.log`, 6792 bytes, 168 tests across 5 assemblies, 0 failures |
| Baseline benchmark (`./dev experiment my-smoke`) | TESTED | `05-experiment.log`, 3962 bytes, 2400 attempts per model, 0 errors |
| Windows workaround sequence (four items above, applied manually) | TESTED | Reproduced across `03-demo-attempt1` through `03-demo-attempt4` logs |

**Commands actually executed (with the Windows workarounds applied manually).**

    export MSYS_NO_PATHCONV=1
    export MSYS2_ARG_CONV_EXCL="*"
    rm -f deployment/docker/.local/appsettings.Development.json
    ./dev up
    ./dev health
    ./dev demo
    ./dev test
    ./dev experiment my-smoke
    ./dev down

**Known limitations.**

- The four Windows workarounds were applied manually in the shell; they are
  not yet codified in `dev`. This is why the `.gitattributes` rule, the CRLF
  check, the MSYS exports, and the `demo` self-sufficiency changes are
  PLANNED, not IMPLEMENTED.
- The DENY correlation logging gap is documented but not fixed. It is out of
  scope for this task.
- The green demo run (`03-demo-attempt4.log`) was produced after the
  workarounds were applied, not from a fresh clone. A fresh-clone run is
  planned as Level 2 validation but was not performed in this submission.

**Public-safe reproduction instructions.**

    git clone https://github.com/chalasanisreenivasulu2-glitch/AeglysAI.git
    cd AeglysAI
    git checkout qualification/chalasanisreenivasulu2-glitch
    export MSYS_NO_PATHCONV=1
    export MSYS2_ARG_CONV_EXCL="*"
    rm -f deployment/docker/.local/appsettings.Development.json
    ./dev up && ./dev health && ./dev demo && ./dev test
    ./dev down

Expected output for `./dev demo` matches
`qualification-logs/03-demo-attempt4.log` apart from Correlation UUIDs.

## Evidence

**Metric definitions.**

- "168 tests" is the sum of `Passed!` counts across five assemblies:
  Architecture (4), Domain (14), Application (53), Experiments (4),
  Integration (93). Source: `04-test.log`. Deduplication: the test runner
  reports each assembly once; no assembly is run twice.
- "0 failures" is the reported `Failed: 0` in each `Passed!` line.
- "2400 attempts per model, 0 errors" is the raw count in
  `05-experiment.log` under `Attempts` and `Errors` per model. This is a
  microbenchmark; the log's own `Limitations` field disclaims production
  performance claims.
- The `Correlation` IDs in `03-demo-attempt4.log` are per-request values
  emitted by the API. They are verification artifacts, not metrics.

**Verification method.**

- Logs were captured with `./dev ... 2>&1 | tee qualification-logs/NN-name.log`
  at the time of the run. No log has been edited after capture.
- Usernames were replaced with `USER` in the log files before commit. No
  other content was modified.
- The demo output was checked for the presence of three ALLOW/STEP_UP
  Correlation lines and one DENY line. The absence of a Correlation line
  preceding the DENY is a documented finding, not an artefact of the capture.

**What the evidence does not establish.**

- No community impact claim. The 2400-attempt benchmark is a microbenchmark
  and does not measure real-world authorization throughput or accuracy.
- No production security claim. The RBAC/ABAC/risk pipeline was not modified
  and was not independently audited.
- No claim of a fresh-clone reproducibility pass. That is planned.

## Compatibility and security

**Breaking changes.** None. No source file in `src/`, `benchmarks/`, or
`tests/` was modified. No API surface was changed. No container image was
modified.

**Retained interfaces.**

- The `./dev` entrypoint's subcommand names (`up`, `down`, `health`, `demo`,
  `test`, `experiment`) are unchanged.
- The `Correlation` field name and format are unchanged for the outcomes
  where it is emitted (ALLOW, STEP_UP).
- The DENY response shape is unchanged.

**Unresolved gate findings.**

- The DENY decision on `reports/write` does not carry a `Correlation` field.
  This is documented as a secondary observation and is explicitly out of
  scope. It is not bypassed â€” the log shows the missing field, and the
  qualification document states so.
- The four Windows workarounds are applied manually. No pre-build check
  prevents a regression. This is why the `.gitattributes` rule and the
  CRLF check are PLANNED, not IMPLEMENTED.

**Sensitive values.** No bearer tokens, passwords, API keys, or `.env`
content is present in the staged diff. The only match against the
`sanitization` pattern is the public GitHub username in the qualification
document title and in the clone URL â€” these are public metadata, not secrets.

**History and deployed resources.** No `git rebase`, no `git commit --amend`
after push, no `git push --force`. No deployed resource was created,
modified, or deleted by this submission.

## Review checklist

- [x] Meaningful tests and applicable security scans executed
      â€” `./dev test` 168/168; no security scan was applicable because no
      source was modified. The staged diff was grepped for secrets and
      usernames.
- [x] Diff and filenames reviewed for secrets, personal data and protected
      material â€” see "Compatibility and security" above. Only public
      identifiers remain.
- [x] Evidence is public-approved and limitations are factual
      â€” the `Limitations` field from `05-experiment.log` is quoted
      verbatim; the DENY correlation gap is stated as unresolved.
- [x] No Git history rewrite or deployed-resource changes
      â€” all commits are additive; no force-push was performed; no deployed
      resource was touched.
- [x] Owner publication authorization confirmed
      â€” submitted via the AEGYTHON qualification form by the repository
      owner (`chalasanisreenivasulu2-glitch`).
