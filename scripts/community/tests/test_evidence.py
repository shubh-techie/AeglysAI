import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('evidence', ROOT / 'scripts/community/validate_evidence.py')
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = evidence.load_json(ROOT / 'community/evidence/fixtures/valid/synthetic-all-levels.json')

    def test_all_five_levels_valid(self):
        self.assertEqual(evidence.validate(self.fixture), [])
        self.assertEqual([m['level'] for m in self.fixture['metrics']], [1, 2, 3, 4, 5])

    def test_invalid_fixtures_rejected(self):
        for path in (ROOT / 'community/evidence/fixtures/invalid').glob('*.json'):
            with self.subTest(path=path.name):
                self.assertTrue(evidence.validate(evidence.load_json(path)))

    def test_level_and_unit_must_match(self):
        self.fixture['metrics'][0]['unit'] = 'participants'
        self.assertEqual(evidence.validate(self.fixture), ['schema'])

    def test_timezone_required_and_actual_date_checked(self):
        for value in ['2026-10-01T00:00:00', '2026-02-30T00:00:00Z', '2026-10-01 00:00:00+00:00']:
            with self.subTest(value=value):
                self.fixture['metrics'][0]['period']['start'] = value
                self.assertEqual(evidence.validate(self.fixture), ['schema'])

    def test_equal_period_rejected(self):
        m = self.fixture['metrics'][0]
        m['period']['end'] = m['period']['start']
        self.assertIn('period-order', evidence.validate(self.fixture))

    def test_duplicate_ids(self):
        self.fixture['metrics'][1]['id'] = self.fixture['metrics'][0]['id']
        self.assertIn('duplicate-metric', evidence.validate(self.fixture))

    def test_synthetic_cannot_masquerade_as_real_source(self):
        self.fixture['metrics'][0]['source']['kind'] = 'public-aggregate'
        self.assertIn('source-kind', evidence.validate(self.fixture))

    def test_draft_not_verified(self):
        self.assertEqual(evidence.validate(self.fixture, True), ['unverified'])

    def test_unknown_fields_rejected_at_every_boundary(self):
        for target in [self.fixture, self.fixture['metrics'][0], self.fixture['metrics'][0]['source'],
                       self.fixture['metrics'][0]['period'], self.fixture['metrics'][0]['verification']]:
            with self.subTest(target=type(target).__name__):
                target['personal_data'] = 'synthetic placeholder'
                self.assertEqual(evidence.validate(self.fixture), ['schema'])
                del target['personal_data']

    def test_nonpublic_or_credential_urls_rejected(self):
        for value in ['https://localhost/source', 'https://127.0.0.1/source',
                      'https://example.invalid/source?token=demo', 'https://user@example.invalid/source']:
            self.fixture['metrics'][0]['source']['reference'] = value
            self.assertTrue(evidence.validate(self.fixture))

    def test_nonnegative_and_integer_counts(self):
        for value in [-1, 1.5, True]:
            self.fixture['metrics'][0]['count'] = value
            self.assertEqual(evidence.validate(self.fixture), ['schema'])

    def test_public_source_rejects_dummy_provenance(self):
        self.fixture['data_kind'] = 'PUBLIC_AGGREGATE'
        for m in self.fixture['metrics']:
            m['source']['kind'] = 'public-aggregate'
        self.assertIn('dummy-digest', evidence.validate(self.fixture))
        self.assertIn('synthetic-reference', evidence.validate(self.fixture))

    def test_json_duplicate_fields_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'record.json'
            for text in ['{"schema_version":"1.0.0","schema_version":"2.0.0"}', '{"count":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):
                    evidence.load_json(p)

    def test_size_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'oversize.json'
            p.write_bytes(b' ' * (evidence.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                evidence.load_json(p)

    def test_cli_redacts_values_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'input.json'
            p.write_text('{"private_note":"DO_NOT_PRINT_SENTINEL"}')
            r = subprocess.run([sys.executable, str(ROOT / 'scripts/community/validate_evidence.py'), str(p)],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn('DO_NOT_PRINT_SENTINEL', r.stdout + r.stderr)
            missing = subprocess.run([sys.executable, '-S', str(ROOT / 'scripts/community/validate_evidence.py'), str(p)],
                                     capture_output=True, text=True)
            self.assertEqual(missing.returncode, 2)

    def test_blank_definitions_and_unknown_version_rejected(self):
        self.fixture['metrics'][0]['definition'] = '   '
        self.assertEqual(evidence.validate(self.fixture), ['schema'])
        self.setUp()
        self.fixture['schema_version'] = '2.0.0'
        self.assertEqual(evidence.validate(self.fixture), ['schema'])

    def test_verified_synthetic_is_only_contract_verified(self):
        for m in self.fixture['metrics']:
            m['verification']['status'] = 'verified'
        self.assertEqual(evidence.validate(self.fixture, True), [])
        self.assertEqual(self.fixture['data_kind'], 'SYNTHETIC')

    def test_missing_schema_fails(self):
        with self.assertRaises(OSError):
            evidence.validate(self.fixture, schema_path=ROOT / 'missing.schema.json')
