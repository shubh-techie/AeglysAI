"""Security gate integration tests in disposable repositories; no real secrets."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scan.py"
HOOK = SCRIPT.parents[2] / ".githooks" / "pre-commit"
spec = importlib.util.spec_from_file_location("scan", SCRIPT)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aegisai-gate-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("config", "user.name", "Synthetic Test")
        self.write("safe.txt", "Synthetic public fixture\n")
        self.git("add", "safe.txt")
        self.git("commit", "-qm", "synthetic baseline")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def write(self, name, value):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(value)

    def run_gate(self, mode="staged", check="disclosure", env=None):
        return subprocess.run(["python3", str(SCRIPT), mode, "--check", check],
                              cwd=self.root, capture_output=True, text=True, env=env)

    def test_safe_staged_file_passes(self):
        self.write("safe.txt", "Updated public fixture\n")
        self.git("add", "safe.txt")
        self.assertEqual(0, self.run_gate().returncode)

    def test_forced_private_paths_block(self):
        for name in ["private-research/model.cs", "a.confidential.md", ".env.local",
                     "key.pem", "research/results/local-test/summary.json"]:
            with self.subTest(name=name):
                self.write(name, "synthetic")
                self.git("add", "-f", name)
                self.assertEqual(1, self.run_gate().returncode)
                self.git("reset", "-q", "HEAD", "--", name)

    def test_staged_content_cannot_be_hidden_by_unstaged_replacement(self):
        marker = "BEGIN" + " CONFIDENTIAL"
        self.write("safe.txt", marker + "\nSYNTHETIC_PRIVATE_CANARY")
        self.git("add", "safe.txt")
        self.write("safe.txt", "Public unstaged replacement")
        result = self.run_gate()
        self.assertEqual(1, result.returncode)
        self.assertIn("safe.txt", result.stdout)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn("SYNTHETIC_PRIVATE_CANARY", result.stdout + result.stderr)

    def test_unstaged_marker_is_not_staged_content(self):
        self.write("safe.txt", "Safe staged content")
        self.git("add", "safe.txt")
        self.write("safe.txt", "BEGIN" + " CONFIDENTIAL")
        self.assertEqual(0, self.run_gate().returncode)

    def test_policy_guidance_passes_but_explicit_classification_blocks(self):
        self.write("safe.txt", "Keep confidential invention materials outside the repository.")
        self.git("add", "safe.txt")
        self.assertEqual(0, self.run_gate().returncode)
        self.write("safe.txt", "CLASSIFICATION:" + " CONFIDENTIAL" + " INVENTION")
        self.git("add", "safe.txt")
        self.assertEqual(1, self.run_gate().returncode)

    def test_rename_to_private_filename_blocks(self):
        self.git("mv", "safe.txt", "safe.patent-draft.md")
        self.assertEqual(1, self.run_gate().returncode)

    def test_deletion_is_allowed(self):
        self.git("rm", "safe.txt")
        self.assertEqual(0, self.run_gate().returncode)

    def test_symlink_is_not_followed(self):
        (self.root / "link.txt").symlink_to("safe.txt")
        self.git("add", "link.txt")
        self.assertEqual(2, self.run_gate().returncode)

    def test_missing_scanner_closes_gate(self):
        env = os.environ.copy()
        tools = self.root / "tools"
        tools.mkdir()
        for tool in ("python3", "git"):
            import shutil
            (tools / tool).symlink_to(shutil.which(tool))
        env["PATH"] = str(tools)
        self.assertEqual(2, self.run_gate(check="all", env=env).returncode)

    def test_temporary_snapshots_cannot_be_created_inside_repository(self):
        env = os.environ.copy()
        env["TMPDIR"] = str(self.root)
        env["TEMP"] = str(self.root)
        env["TMP"] = str(self.root)
        self.assertEqual(2, self.run_gate(env=env).returncode)

    def test_actual_gitignore_blocks_private_material_preserves_public_fixtures(self):
        self.write(".gitignore", (SCRIPT.parents[2] / ".gitignore").read_text())
        for name in ["patent-private/draft.md", "nested/private-research/model.cs",
                     "a.confidential.docx", "nested/.aws/credentials", "local.snk",
                     "research/results/local-test/report.json", "gitleaks-report.json"]:
            with self.subTest(name=name):
                result = subprocess.run(["git", "check-ignore", "--no-index", "-q", name], cwd=self.root)
                self.assertEqual(0, result.returncode)
        for name in [".env.example", "docs/aegisai/specs/SPEC-012-RESEARCH-DEFINITION.md",
                     "src/AegisAI.Domain/Public.cs", "research/results/approved-synthetic/summary.json"]:
            with self.subTest(name=name):
                result = subprocess.run(["git", "check-ignore", "--no-index", "-q", name], cwd=self.root)
                self.assertEqual(1, result.returncode)

    def test_wrong_scanner_version_and_runtime_failure_close_gate(self):
        tools = self.root / "fake-tools"
        tools.mkdir()
        env = os.environ.copy()
        env["PATH"] = str(tools) + os.pathsep + env["PATH"]
        executable = tools / "gitleaks"
        executable.write_text('#!/bin/sh\necho 0.0.0\n')
        executable.chmod(0o700)
        self.assertEqual(2, self.run_gate(check="all", env=env).returncode)
        executable.write_text('#!/bin/sh\nif [ "$1" = version ]; then echo 8.30.1; exit 0; fi\necho SYNTHETIC_DIAGNOSTIC_CANARY >&2\nexit 2\n')
        result = self.run_gate(check="all", env=env)
        self.assertEqual(2, result.returncode)
        self.assertNotIn("SYNTHETIC_DIAGNOSTIC_CANARY", result.stdout + result.stderr)

    def test_history_keeps_deleted_disclosure_visible(self):
        self.write("draft.md", "BEGIN" + " CONFIDENTIAL\nsynthetic")
        self.git("add", "draft.md")
        self.git("commit", "-qm", "synthetic disclosure")
        self.git("rm", "draft.md")
        self.git("commit", "-qm", "synthetic removal")
        result = self.run_gate("history")
        self.assertEqual(1, result.returncode)
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        self.assertEqual("draft.md", rows[0]["path"])
        self.assertEqual(8, len(rows[0]["commit"]))

    def test_real_scanner_detects_synthetic_servicebus_key_without_output(self):
        # Manufactured test token, assembled to avoid a stored secret-looking fixture.
        value = "AbCdEf0123456789" * 3
        self.write("fixture.txt", "SharedAccess" + "Key=" + value)
        self.git("add", "fixture.txt")
        result = self.run_gate(check="secrets")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("fixture.txt", result.stdout)
        self.assertNotIn(value, result.stdout + result.stderr)

    def test_real_scanner_safe_and_empty_index_pass(self):
        self.assertEqual(0, self.run_gate(check="all").returncode)
        self.write("safe.txt", "Public staged fixture")
        self.git("add", "safe.txt")
        self.assertEqual(0, self.run_gate(check="all").returncode)

    def test_hook_runs_gate_and_blocks_synthetic_secret(self):
        (self.root / "scripts/security").mkdir(parents=True)
        (self.root / "scripts/security/scan.py").symlink_to(SCRIPT)
        self.write("fixture.txt", "SharedAccess" + "Key=" + "AbCdEf0123456789" * 3)
        self.git("add", "fixture.txt")
        result = subprocess.run(["sh", str(HOOK)], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(1, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
