# CORE-REBRAND-001 — AeglysAI repository migration

Date: 2026-10-03. Status: **IMPLEMENTED** documentation/branding in the working
tree, pending review; no commit or push. AeglysAI continues the existing project.

## Audit method and classifications

The [occurrence audit](CORE-REBRAND-001-AUDIT.tsv) records every match in tracked
text files before editing, with original file, line, column, classification and
disposition. The case-insensitive search covers `AegisAI`, `Aegis AI`, `AEGISAI`,
`aegisai`, and consequently the requested old domain/repository URL patterns.
Git internals and ignored build/editor artifacts are excluded. Original line
numbers deliberately refer to the starting revision, `37f37d9`.

| Classification | Original matches | Disposition |
| --- | ---: | --- |
| CURRENT_BRAND | 26 | Updated display branding and clone instructions |
| HISTORICAL | 367 | Preserved milestone/task records, snapshots, baseline scope, commit titles and experiment provenance |
| CODE_IDENTIFIER | 246 | Preserved namespaces, projects, assemblies and proposed module names |
| COMPATIBILITY_IDENTIFIER | 50 | Preserved document paths, Docker/environment, JWT and telemetry contracts |
| REPOSITORY_URL | 0 | No hard-coded old repository URL found in the starting tracked files |

No `Aegis AI` or `aegisai.world` occurrence was found. No current-brand old-name
reference remains. Remaining old-name matches in the original files are the
663 preserved matches above; new old-name mentions explain the rebrand in
README/history and compatibility in README. This report, the new log entry and
the audit itself also intentionally retain historical names and search terms.
The old repository name in the appended history milestone is HISTORICAL.

## Current branding and links

README, agent instructions, target/system/research architecture, research scope,
research problem/program/contribution/claims display names, ADR-006's current
platform reference, threat model, readiness title and experiment README now use
AeglysAI. Research wording changes are limited to the platform's display name;
claims, statuses, hypotheses and measurements are unchanged.

README now supplies the canonical repository link and clone command:
https://github.com/shubh-techie/AeglysAI. The primary website is
https://aeglysai.com, linked from README and recorded in project history.
These addresses are supplied by the task; no availability claim is made.
There were no README badges, contribution/security documents, or issue/PR
templates to update. The existing origin fetch/push URL already pointed to
https://github.com/shubh-techie/AeglysAI.git; no remote edit was required.

## Compatibility and historical preservation

No code identifiers were renamed. `AegisAI.sln`, project/assembly/namespace
names and code links stay unchanged. `docs/aegisai/`, SPEC filename/task IDs,
experiment directories and recorded hashes remain stable. Proposed service
names remain planning identifiers, not newly implemented services.

`aegisai-local` Compose project name and `AEGISAI_PORT` remain unchanged to
preserve existing Compose resources and setup commands. Local JWT issuer
`https://aegisai-local.example.invalid` and audience `aegisai-local-development`
remain paired across token generation and validation. `AegisAI.Authorization`
and `aegisai.authorization.*` telemetry names remain subscriber-compatible.
No database/topic/API/configuration identifier is renamed.

CI contains only references to the retained solution filename. `.github/workflows/ci.yml`,
Docker configuration, `dev`, source and tests are unchanged; CI behavior is preserved.
Historical PROJECT_HISTORY and DEVELOPMENT_LOG content is preserved and extended,
not rewritten. CURRENT_STATE and MIGRATION_PLAN remain historical snapshots;
SPEC-003/SPEC-012 record their original named task/baseline. Dated research
provenance remains intact. RESEARCH_HYPOTHESES is byte-identical.

## Validation

Validation outcomes are recorded in the appended
[development log](DEVELOPMENT_LOG.md). No new research experiment or result was
produced. The migration branch is `chore/aeglysai-repo-migration`.
HEAD remains `37f37d99f7d9eda725b9452ed7db0a15e4b43c56`; historical commits
are unchanged. All original tag objects remain:

| Tag | Tag object |
| --- | --- |
| research-baseline-v0.1 | e34b35e5198835a82e08e6008df713697d769e14 |
| securing-microservices-legacy | 284ea1ac65b54498ccca31b1405296246d7d845d |
| v0.1.0 | b7bf77195e9842a25e8b44d7a8ecb6922733d401 |

The legacy tag still resolves to `b9518fa5f3926aa43e666170cd0e66bb61193f4e`.
No history rewrite, tag edit, commit or push was performed.

## Files changed

Modified:

- `AGENTS.md`
- `README.md`
- `docs/aegisai/PROJECT_HISTORY.md`
- `docs/aegisai/DEVELOPMENT_LOG.md`
- `docs/aegisai/RESEARCH_SCOPE.md`
- `docs/aegisai/TARGET_ARCHITECTURE.md`
- `docs/aegisai/V01_READINESS.md`
- `docs/aegisai/adr/ADR-006-POLICY-BOUNDED-ADAPTIVE-SECURITY.md`
- `docs/aegisai/architecture/RESEARCH_ARCHITECTURE.md`
- `docs/aegisai/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/aegisai/research/CLAIMS_REGISTER.md`
- `docs/aegisai/research/PROPOSED_CONTRIBUTION.md`
- `docs/aegisai/research/RESEARCH_PROBLEM.md`
- `docs/aegisai/research/RESEARCH_PROGRAM.md`
- `docs/aegisai/threat-model/THREAT_MODEL_V1.md`
- `research/README.md`

Added: this report and `CORE-REBRAND-001-AUDIT.tsv`.

Final Git status: 16 modified files and two untracked files, nothing staged,
on `chore/aeglysai-repo-migration`. Restore/build and all 168 tests passed;
build had zero warnings/errors. Documentation validation and `git diff --check`
passed. No commit or push.
