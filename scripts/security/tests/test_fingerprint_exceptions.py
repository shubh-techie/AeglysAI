"""Native Gitleaks regression tests for twelve immutable historical occurrences.

All new credential fixtures are manufactured in disposable repositories. Neither
actual historical credentials nor matched text is printed by these tests.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / '.gitleaks.toml'


def approved_blocks():
    text = CONFIG.read_text()
    section = text.split('[[rules]]\nid = "generic-api-key"\n', 1)[1]
    return section.split('[[rules.allowlists]]')[1:]


def field(block, name):
    if name == 'commits':
        return re.search(r'commits = \["([0-9a-f]{40})"\]', block).group(1)
    return re.search(name + r" = \['''([^\n]+)'''\]", block).group(1)


class HistoricalFingerprintExceptionTests(unittest.TestCase):
    def setUp(self):
        self.executable = shutil.which('gitleaks')
        self.assertIsNotNone(self.executable, 'Pinned Gitleaks is required; tests cannot certify unavailable scans')
        version = subprocess.run([self.executable, 'version'], capture_output=True, text=True)
        self.assertTrue(version.returncode == 0 and version.stdout.strip().lstrip('v') == '8.30.1', 'Pinned scanner version is required')
        self.temporary = tempfile.TemporaryDirectory(prefix='aeglysai-fingerprint-test-')
        self.addCleanup(self.temporary.cleanup)
        self.private = Path(self.temporary.name)
        self.repo = self.private / 'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Synthetic Security Fixture')
        self.git('config', 'user.email', 'synthetic@example.invalid')
        self.block = approved_blocks()[0]
        self.original_commit = field(self.block, 'commits')
        self.original_path = 'research/results/aegisai009-smoke/environment.json'
        data = json.loads(self.actual_git('show', self.original_commit + ':' + self.original_path))
        original = self.actual_git('show', self.original_commit + ':' + self.original_path).decode()
        self.line = next(line for line in original.splitlines() if re.fullmatch(field(self.block, 'regexes'), line))
        self.digest = next(v for k, v in data['SourceHashes'].items() if json.dumps(k) + ': ' + json.dumps(v) in self.line)
        self.fixture = '{"SourceHashes": {\n' + self.line + '\n    "safe": "public"\n}}\n'

    def git(self, *args):
        result = subprocess.run(['git', *args], cwd=self.repo, capture_output=True)
        self.assertEqual(result.returncode, 0, 'Disposable fixture Git operation failed')
        return result.stdout

    def actual_git(self, *args):
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, 'Approved historical evidence unavailable; full clone required')
        return result.stdout

    def write(self, path, content):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)

    def commit(self):
        self.git('add', '--all')
        self.git('commit', '-qm', 'Manufactured security regression fixture')
        return self.git('rev-parse', 'HEAD').decode().strip()

    def configure(self, commit):
        # Substitute one approval context ONLY inside this private test config.
        # Production configuration and actual repository commits are untouched.
        self.test_config = self.private / 'fixture.gitleaks.toml'
        self.test_config.write_text(CONFIG.read_text().replace(self.original_commit, commit, 1))

    def scan(self, mode='git'):
        report = self.private / 'report.json'
        command = [self.executable, mode, str(self.repo), '--config', str(self.test_config),
                   '--redact=100', '--no-banner', '--no-color', '--ignore-gitleaks-allow',
                   '--gitleaks-ignore-path', str(self.private / 'no-ignore'), '--exit-code', '10',
                   '--report-format', 'json', '--report-path', str(report)]
        if mode == 'git':
            command.append('--log-opts=--all --full-history')
        result = subprocess.run(command, capture_output=True)
        self.assertIn(result.returncode, (0, 10), 'Native scan unavailable or incomplete')
        findings = json.loads(report.read_text())
        self.assertEqual(result.returncode == 10, bool(findings), 'Inconsistent native report')
        return findings

    def test_configuration_has_only_twelve_exact_and_scopes(self):
        blocks = approved_blocks()
        self.assertEqual(len(blocks), 12)
        approved_paths = {'research/results/aegisai009-smoke/environment.json',
                          'research/results/aegisai010-local-smoke/environment.json',
                          'research/results/local-validation/environment.json'}
        context = set()
        for block in blocks:
            self.assertIn('condition = "AND"', block)
            self.assertIn('regexTarget = "line"', block)
            self.assertNotIn('stopwords', block)
            path = field(block, 'paths')
            self.assertIn(path, {'^' + re.escape(p) + '$' for p in approved_paths})
            regex = field(block, 'regexes')
            self.assertTrue(regex.startswith('^[\\r\\n]*') and regex.endswith('[\\r\\n]*$'))
            self.assertEqual(len(re.findall(r'[0-9a-f]{64}', regex)), 1)
            context.add((field(block, 'commits'), path, regex))
        self.assertEqual(len(context), 12)

    def test_all_twelve_occurrences_recompute_public_source_bytes(self):
        for block in approved_blocks():
            commit = field(block, 'commits')
            for path in ['research/results/aegisai009-smoke/environment.json',
                         'research/results/aegisai010-local-smoke/environment.json',
                         'research/results/local-validation/environment.json']:
                if re.fullmatch(field(block, 'paths'), path):
                    raw = self.actual_git('show', commit + ':' + path)
                    data = json.loads(raw)
                    matched = [line for line in raw.decode().splitlines() if re.fullmatch(field(block, 'regexes'), line)]
                    self.assertEqual(len(matched), 1, 'Approved exact-line evidence mismatch')
                    hashes = [(p, h) for p, h in data['SourceHashes'].items() if json.dumps(p) + ': ' + json.dumps(h) in matched[0]]
                    self.assertEqual(len(hashes), 1, 'Approved source field ambiguous')
                    source_path, expected = hashes[0]
                    source = self.actual_git('show', data['GitCommit'] + ':' + source_path)
                    self.assertTrue(hashlib.sha256(source).hexdigest() == expected, 'Approved public-source digest mismatch')

    def test_approved_historical_field_is_exempt(self):
        self.write(self.original_path, self.fixture)
        self.configure(self.commit())
        self.assertFalse(self.scan())

    def test_same_hash_in_client_secret_and_cloud_key_still_detected(self):
        content = self.fixture.rstrip()[:-1] + ', "ClientSecret": "' + self.digest + '", "connection": "SharedAccess' + 'Key=' + 'AbCdEf0123456789' * 3 + '"}\n'
        self.write(self.original_path, content)
        self.configure(self.commit())
        rules = {r['RuleID'] for r in self.scan()}
        self.assertIn('generic-api-key', rules)
        self.assertIn('azure-servicebus-shared-access-key', rules)

    def test_approved_commit_does_not_exempt_other_path(self):
        self.write(self.original_path, self.fixture)
        self.write('other/environment.json', self.fixture)
        self.configure(self.commit())
        self.assertTrue(any(r['File'] == 'other/environment.json' for r in self.scan()))

    def test_replayed_field_in_new_commit_is_not_exempt(self):
        self.write(self.original_path, self.fixture)
        self.configure(self.commit())
        self.write(self.original_path, '{}')
        self.commit()
        self.write(self.original_path, self.fixture)
        replay = self.commit()
        self.assertTrue(any(r['Commit'] == replay for r in self.scan()))

    def test_changed_value_is_not_exempt(self):
        changed = hashlib.sha256(b'manufactured different credential-like value').hexdigest()
        self.write(self.original_path, self.fixture.replace(self.digest, changed))
        self.configure(self.commit())
        self.assertTrue(any(r['RuleID'] == 'generic-api-key' for r in self.scan()))

    def test_directory_scan_has_no_historical_exception(self):
        self.write(self.original_path, self.fixture)
        self.configure(self.commit())
        self.assertTrue(any(r['RuleID'] == 'generic-api-key' for r in self.scan('dir')))

    def test_staged_directory_snapshot_has_no_historical_exception(self):
        self.write(self.original_path, self.fixture)
        self.configure(self.commit())
        self.git('add', self.original_path)
        self.assertTrue(any(r['RuleID'] == 'generic-api-key' for r in self.scan('dir')))

    def test_malformed_native_configuration_closes_gate(self):
        self.write('safe.txt', 'Public manufactured fixture')
        self.git('add', 'safe.txt')
        shutil.copytree(ROOT / 'scripts/security', self.repo / 'scripts/security', ignore=shutil.ignore_patterns('__pycache__'))
        (self.repo / '.gitleaks.toml').write_text('[[rules')
        environment = os.environ.copy()
        environment['PATH'] = str(Path(self.executable).parent) + os.pathsep + environment['PATH']
        result = subprocess.run(['python3', str(self.repo / 'scripts/security/scan.py'), 'staged'],
                                cwd=self.repo, env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, 'Unavailable native scan must close the gate')

    def test_disclosure_boundaries_unchanged(self):
        self.write('tempkey.jwk', '{}')
        self.write('docs/research/INVENTION_CANDIDATES.md', 'Manufactured protected-path fixture')
        self.git('add', '--all')
        environment = os.environ.copy()
        environment['PATH'] = str(Path(self.executable).parent) + os.pathsep + environment['PATH']
        # Original script/config are copied without changing scanner implementation.
        shutil.copytree(ROOT / 'scripts/security', self.repo / 'scripts/security', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copyfile(CONFIG, self.repo / '.gitleaks.toml')
        result = subprocess.run(['python3', str(self.repo / 'scripts/security/scan.py'), 'staged'],
                                cwd=self.repo, env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('tempkey.jwk', result.stdout)
        self.assertIn('INVENTION_CANDIDATES.md', result.stdout)


if __name__ == '__main__':
    unittest.main()
