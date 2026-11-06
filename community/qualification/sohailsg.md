# AeglysAI qualification technical evidence

All results below were observed on my own machine. Where I could not check something, I say so.

## Fork, branch and commit

- Fork: https://github.com/sohailsg/AeglysAI
- Branch: https://github.com/sohailsg/AeglysAI/tree/qualification/sohailsg
- Base commit: `48047e46aee115181dc0fd67a45105a0b7a45a45` ("fix(docker): resolve NuGet-Migrations mutex initialization")

## Architecture

AeglysAI decides whether a request should be allowed. The code is split into four layers, and each layer only depends on the ones below it. A test in `tests/AeglysAI.ArchitectureTests` checks this rule.

- **Domain** (`src/AeglysAI.Domain`): the basic concepts, such as subject, resource, action, role, permission and risk. It has no connection to the outside world.
- **Application** (`src/AeglysAI.Application`): the decision rules. It contains the role check, the attribute check, the risk score and the audit event.
- **Infrastructure** (`src/AeglysAI.Infrastructure`): where the policy data comes from. Today this is fixed example data held in memory, not a database.
- **API** (`src/AeglysAI.Api`): the web layer. It checks the login token, receives requests, and writes the audit log.

How a request flows (read from the code, then confirmed with `curl`):
1. The caller sends a login token (JWT).
2. Every route except `/health` requires a valid token.
3. The resource and action in the request are checked (not blank, at most 256 characters).
4. The decision engine runs. The user's identity is taken from the token, never from the request body.
5. The answer is returned with an `X-Correlation-ID` header, and one audit line is logged.

## Models A, B and C

- **Model A** checks roles only. Anything not explicitly allowed is denied.
- **Model B** adds attribute rules. Missing information means deny.
- **Model C** adds a risk score. The result can be ALLOW, DENY, STEP_UP (ask for stronger login) or LIMIT. In the demo, `reports` + `read` gave STEP_UP with a risk score of 0.300 (Medium). STEP_UP and LIMIT are only advice returned to the caller. Nothing in this repository enforces them yet.

## Setup and prerequisites

- The supported way is Docker with Compose and a shell: `./dev up`.
- The project needs the .NET 8 SDK (`global.json` pins 8.0.204). The SDK is inside the Docker image.
- My computer has only .NET SDK 10.0.114, so `dotnet` commands run directly on it fail inside this repository. I used the Docker route only. I did not try installing .NET 8 on the host.

## Problems found

I found these by running the project and trying things that could go wrong.

1. **Broken requests show internal error details (main finding).**
   - If I send broken JSON (`{bad`) or an extra field to `/authorization/evaluate`, the API replies with HTTP 400 and a long message that includes internal code names and stack lines.
   - The local Docker setup runs the API in "Development" mode (`ASPNETCORE_ENVIRONMENT: Development` in `deployment/docker/compose.yaml`), which is the likely cause.
   - Other bad requests were handled well: no token and a changed token gave 401, a blank or too-long resource gave a clean 400 message, a wrong content type gave 415, and GET gave 405.
   - I found no test for a broken or unknown-field body.
   - Not confirmed: whether this also happens in Production. The API refuses to start in Production with the local login setup ("Local trust requires Development..."), which is intended. I have no real login provider to test with.

2. **`./dev health` crashes with a stack trace when the API is off.** It shows an unhandled error pointing to `AeglysAI.DevTools/Program.cs` line 40 and exits with code 134, instead of a short message such as "API is not running".

3. **`./dev up` leaves a leftover container when port 5080 is busy.** It fails with a Docker port error (exit 1) and leaves a stopped `aegisai-local-api-1` container until `./dev down` is run. I did not test the `AEGLYSAI_PORT` setting.

4. **`./dev` with an unknown command exits with code 0.** It prints the usage line but reports success, so a script cannot tell it failed.

5. **The repository's own publication check fails.** With Gitleaks installed, `scan.py tracked` lists 3 files and `scan.py history` lists 14 entries, both ending with "publication gate requires review". The tool hides what it matched, so I do not know the reason. This agrees with the README, which says audit findings are not cleared.

6. **Setup is harder than the README suggests.** The host needs the .NET 8 SDK (see above). Two Python test suites also failed until I installed `scikit-learn` and the pinned Gitleaks scanner. After installing them, both passed.

7. **Small points.** Empty values appear as `(null)` in audit lines and the date uses a US style (`11/06/2026`). Names mix `aegisai` and `aeglysai`; code comments say this is intentional for compatibility.

## Proposed improvement (PLANNED, not implemented)

Make broken request bodies return the same short JSON error as the other 400 responses (for example `{"error":"Request body is not valid."}`), with no internal details, in every environment.

- **Why it is useful:** clients get one consistent error format, internal names are not exposed even in the demo setup, and the behaviour is protected against future mistakes.
- **How I would check it:**
  1. Write tests for broken JSON and an unknown field that check for HTTP 400, the short JSON error, and no stack text. Confirm they fail on the current code.
  2. Make the change.
  3. Run `./dev test` and expect all existing tests plus the new ones to pass.
  4. Repeat the `curl` requests above and compare before and after.

## Validation results

Environment: Ubuntu 22.04.5 LTS, Linux 6.8.0-138, Docker 29.8.0, Docker Compose v5.5.1, Python 3.10.12. The .NET build and tests ran inside the container image (`mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim`).

| Command | Result |
|---|---|
| `./dev up` | Built, started, health check returned `{"status":"healthy"}` |
| `./dev demo` | Anonymous call rejected; Model A ALLOW, Model B ALLOW, Model C STEP_UP, `write` DENY (`NoMatchingPermission`) |
| `./dev test` | Exit 0. Architecture 4, Domain 14, Application 53, Experiments 4, Integration 93 passed; 0 failed, 0 skipped |
| `./dev down`, then `./dev up` | Both worked |
| `python3 -m unittest discover -s scripts/community/tests` | 89 passed |
| `python3 scripts/community/check_docs.py` | PASS (local links only; web links not checked) |
| `python3 -m unittest discover -s research/acbsd/tests` | Without `scikit-learn`: 14 ran, 1 import error. With it installed in a temporary virtual environment: 19 passed |
| `python3 -m unittest discover -s scripts/security/tests` | Without Gitleaks: 27 ran, 14 failed. With the checksum-verified Gitleaks 8.30.1 on `PATH`: 27 passed |

Limitations:
- One machine and one run of each command.
- No run on a host with .NET 8 installed.
- No Production run with a real login provider.
- I did not inspect what the publication check matched.
- `curl` results were checked against the local Development container only.

## Evidence location

The full `./dev test` log is on my machine only. I will upload a sanitized copy and give the link in the Google Form.
