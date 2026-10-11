#!/usr/bin/env python3
"""Read-only publication gates. Output filenames/short commits, never matched text."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

VERSION = "8.30.1"
CONFIG = Path(__file__).resolve().parents[2] / ".gitleaks.toml"
PRIVATE_DIRS = {"patent-private", "private-research", "attorney-private",
                "evidence-private", "confidential-local", ".aws", ".azure", ".ssh", ".local"}
PRIVATE_NAMES = {"invention_candidates.md", "patent-claims.md", "patent_claims.md",
                 "attorney-communications.md", "credentials.local.json", "secrets.json"}
MARKERS = [re.compile(pattern, re.I) for pattern in (
    rb"BEGIN[ _-]CONFIDENTIAL", rb"ATTORNEY[ -]CLIENT PRIVILEGED",
    rb"CLASSIFICATION[ \t]*:[ \t]*CONFIDENTIAL[ -]INVENTION", rb"UNPUBLISHED[ -]PATENT[ -]DRAFT",
    rb"working patent research candidate\s*:")]


class ScanError(Exception):
    pass


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        raise ScanError("Git inspection failed; output suppressed")
    return result.stdout


def protected_path(name):
    path = PurePosixPath(name.lower())
    base = path.name
    return (bool(set(path.parts) & PRIVATE_DIRS) or base in PRIVATE_NAMES
            or ".confidential." in base or ".patent-draft." in base
            or base.startswith(".env") and base != ".env.example"
            or base.endswith((".key", ".pem", ".pfx", ".p12", ".jwk", ".snk", ".publishsettings"))
            or base.endswith(".secrets.json") or base.startswith("gitleaks-report")
            or base == "appsettings.local.json" or base.startswith("appsettings.") and base.endswith(".local.json")
            or name.lower().startswith("research/results/local-"))


def disclosure(name, content):
    return protected_path(name) or any(pattern.search(content) for pattern in MARKERS)


def report(name, commit=""):
    # JSON escaping prevents control characters or CI annotation injection in paths.
    print(json.dumps({"path": name, **({"commit": commit[:8]} if commit else {})}))


def entries(root, mode):
    """Yield exact index blobs for staged checks; never inspect an unstaged replacement."""
    if mode == "staged":
        if git(root, "ls-files", "--unmerged", "-z"):
            raise ScanError("Unmerged index; resolve it before scanning")
        names = git(root, "diff", "--cached", "--name-only", "--no-renames",
                    "--diff-filter=ACMT", "-z").split(b"\0")
        for raw in filter(None, names):
            name = os.fsdecode(raw)
            rows = git(root, "ls-files", "--stage", "-z", "--", name).split(b"\0")
            row = next(row for row in rows if row and row.split(b"\t", 1)[1] == raw)
            permissions, oid, stage = row.split(b"\t", 1)[0].split()
            if permissions not in (b"100644", b"100755") or stage != b"0":
                raise ScanError("Non-regular staged file; manual review required")
            yield name, git(root, "cat-file", "blob", oid.decode())
    else:
        for raw in filter(None, git(root, "ls-files", "-z").split(b"\0")):
            name = os.fsdecode(raw)
            file = root / name
            if file.is_symlink() or not file.is_file():
                raise ScanError("Tracked file missing or non-regular; manual review required")
            yield name, file.read_bytes()


def scanner():
    executable = shutil.which("gitleaks")
    if not executable:
        raise ScanError("Gitleaks 8.30.1 is required; scan did not run")
    version = subprocess.run([executable, "version"], capture_output=True, timeout=15)
    if version.returncode or version.stdout.decode().strip().lstrip("v") != VERSION:
        raise ScanError("Expected Gitleaks 8.30.1; scan did not run")
    return executable


def secrets(executable, target, history=False):
    # All raw diagnostics remain private and temporary; only paths leave this process.
    with tempfile.TemporaryDirectory(prefix="aeglysai-secret-scan-") as temporary:
        private = Path(temporary)
        result_path = private / "report.json"
        command = [executable, "git" if history else "dir", str(target),
                   "--config", str(CONFIG), "--gitleaks-ignore-path", str(private / "no-ignore"),
                   "--ignore-gitleaks-allow", "--redact=100", "--no-banner", "--no-color",
                   "--exit-code", "10", "--report-format", "json", "--report-path", str(result_path),
                   "--timeout", "180", "--max-decode-depth", "2", "--max-archive-depth", "2"]
        if history:
            command.append("--log-opts=--all --full-history")
        result = subprocess.run(command, capture_output=True, timeout=210)
        if result.returncode not in (0, 10) or not result_path.is_file():
            raise ScanError("Secret scanner failed; diagnostics suppressed")
        findings = json.loads(result_path.read_text())
        if not isinstance(findings, list) or (result.returncode == 10) != bool(findings):
            raise ScanError("Invalid scanner report; gate closed")
        paths = set()
        for finding in findings:
            name = finding["File"]
            if not history:
                file = Path(name)
                if file.is_absolute():
                    name = file.relative_to(target).as_posix()
            paths.add((name, finding.get("Commit", "")))
        for name, commit in sorted(paths):
            report(name, commit)
        return bool(findings)


def history_disclosure(root):
    seen = set()
    found = False
    for commit in git(root, "rev-list", "--all").decode().splitlines():
        for row in filter(None, git(root, "ls-tree", "-r", "-z", commit).split(b"\0")):
            meta, raw = row.split(b"\t", 1)
            permissions, kind, oid = meta.split()
            name = os.fsdecode(raw)
            key = (name, oid)
            if key in seen:
                continue
            seen.add(key)
            if kind != b"blob":
                raise ScanError("Historical submodule requires separate review")
            if disclosure(name, git(root, "cat-file", "blob", oid.decode())):
                report(name, commit)
                found = True
    return found


def run(root, mode, check):
    if Path(tempfile.gettempdir()).resolve().is_relative_to(root.resolve()):
        raise ScanError("Temporary evidence storage must be outside the repository")
    if mode == "history" and git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
        raise ScanError("History scan requires a full clone")
    executable = scanner() if check in ("all", "secrets") else None
    failed = False
    if mode == "history":
        if check in ("all", "disclosure"):
            failed = history_disclosure(root)
        if executable:
            failed = secrets(executable, root, history=True) or failed
    else:
        with tempfile.TemporaryDirectory(prefix="aeglysai-index-scan-") as temporary:
            snapshot = Path(temporary)
            for name, content in entries(root, mode):
                path = PurePosixPath(name)
                if path.is_absolute() or ".." in path.parts:
                    raise ScanError("Unsafe repository path")
                if check in ("all", "disclosure") and disclosure(name, content):
                    report(name)
                    failed = True
                if executable:
                    file = snapshot / name
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_bytes(content)
                    file.chmod(0o600)
            if executable:
                failed = secrets(executable, snapshot) or failed
    print("FAIL: publication gate requires review" if failed else "PASS: selected scans completed")
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["staged", "tracked", "history"])
    parser.add_argument("--check", choices=["all", "disclosure", "secrets"], default="all")
    args = parser.parse_args()
    try:
        root = Path(os.fsdecode(git(Path.cwd(), "rev-parse", "--show-toplevel")).strip())
        return run(root, args.mode, args.check)
    except (ScanError, OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.TimeoutExpired):
        print("ERROR: scan unavailable or incomplete; gate closed. Check tooling and repository integrity.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
