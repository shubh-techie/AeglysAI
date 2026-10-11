# Local publication gates

Requirements: Git, Python 3.10 or newer, and Gitleaks **8.30.1** on PATH.
Install the checksum-verified upstream binary into a directory outside the repo:

```sh
sh scripts/security/install-gitleaks.sh /tmp/aeglysai-security-tools
export PATH="/tmp/aeglysai-security-tools:$PATH"
python3 -m unittest discover -s scripts/security/tests -v
python3 scripts/security/scan.py staged
python3 scripts/security/scan.py tracked
python3 scripts/security/scan.py history
```

Optional actual Docker context verification (local Docker daemon required):

```sh
python3 scripts/security/tests/check_docker_context.py
```

The installer supports macOS arm64 and Linux x64. Other platforms require a
manually verified upstream binary. Checksums were verified against the
[upstream release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1).
Command behavior follows the [versioned documentation](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md).

Enable the repository hook explicitly when ready:

```sh
git config --local core.hooksPath .githooks
```

This changes local Git configuration; this task only provides the hook and does
not install it. Inspect existing hooks first and integrate them if needed.
The hook runs both checks on exact staged blobs, including forced additions and
rename destinations. Deletions require no content scan. Symlinks, submodules and
unmerged index entries require manual review and fail closed. No commit is made
by a scanner or test; tests commit synthetic fixtures in disposable repositories.

Default `--check all` runs secrets and disclosure checks. The `--check secrets`
and `--check disclosure` diagnostic modes are partial checks, never sufficient
for publication approval. A missing/wrong scanner, command error, timeout or
malformed report returns exit 2. Findings return exit 1; completed clean selected
checks return 0. An empty staged check does not certify unstaged changes.

Tracked mode scans working-tree contents of tracked files, including changes.
History mode requires a non-shallow clone and scans all **locally reachable**
references. It cannot inspect remote-only refs, forks, deleted refs, caches or
downloads. Neither command fetches, pushes or rewrites Git. Output contains only
JSON-escaped suspicious paths and abbreviated commit references, plus gate status.
Reports and exact index snapshots use owner-only temporary directories outside
the repo and are removed on normal completion. Do not set TMPDIR inside the repo.
No report upload or persistent raw-secret evidence is produced.

Default Gitleaks rules plus a Service Bus shared-access-key rule apply. There is
no history baseline, path allowlist, `.gitleaksignore` override or inline allow
comment bypass. Archives and encoded data receive bounded secret scanning;
unsupported formats/encryption, detector limits and false negatives remain risks.
Confidentiality checks detect reserved private paths and explicit markers in
plain bytes; they cannot classify arbitrary prose or compressed invention text.
Human review of the complete staged diff and any archive members remains required.

[Security CI](../../.github/workflows/security.yml) installs the same pinned
scanner, tests the gates and scans tracked contents plus full local history.
Installation/checksum/scanner errors fail the job. Existing findings intentionally
fail it; do not blanket-exempt history to make CI green. No remote workflow run
or required-check configuration has been performed or verified by this task.
Workflow files can themselves be changed in a PR; requiring trusted checks and
protecting their configuration are owner-managed repository settings.

Ignore protections leave approved existing synthetic results recoverable. The
new `research/results/local-*` guard blocks future untracked local runs, but
already tracked local artifacts are still visible to scans. Before publishing,
review their environment metadata, raw observations and source archives.
