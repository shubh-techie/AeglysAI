# ADR-007 — Local and CI disclosure gates

Date: 2026-10-11

Status: implemented and locally tested; uncommitted, pending review.

## Context

Ignore rules cannot protect tracked history or force-added content. Existing
research and historical credential candidates require human review. Automatic
scans must not leak matched text or turn missing tooling into a passing gate.

## Decision

Use a checksum-pinned Gitleaks release with default rules and a focused additional
credential rule. Add separate path/marker confidentiality checks. Scan exact
staged blobs locally, current tracked contents and all locally reachable history
in CI. Fail on findings and incomplete scans. Suppress raw scanner diagnostics;
print only JSON-escaped paths and short commit references. Store temporary
snapshots/reports outside the repository and remove them on normal completion.

Keep confidential work in controlled external storage. Supply an opt-in hook;
do not modify the owner's Git configuration automatically. Do not add blanket
history exclusions, remove existing materials, rewrite history, configure remotes
or upload reports. Human disclosure review and explicit publication authorization
remain required. See [SPEC-013](../specs/SPEC-013-DISCLOSURE-PROTECTION.md).

## Consequences and limits

Existing findings intentionally fail CI until reviewed remediation is authorized.
Heuristics may overflag synthetic metadata and miss arbitrary confidential prose.
Local hooks can be bypassed; a workflow alone does not enforce a merge restriction.
Docker build exclusions do not control repository bind mounts. Scanner snapshots
can contain protected data transiently, so storage permissions and removal matter;
crash remnants require owner cleanup. No algorithm or invention claims are recorded.
