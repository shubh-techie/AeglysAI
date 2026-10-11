import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/community'))
import validate_monthly as monthly
from contract_tools import load_json


class MonthlyTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = ROOT / 'community/reporting/fixtures'
        self.data = load_json(self.fixtures / 'valid/synthetic-monthly.json')
        self.artifacts = self.fixtures / 'snapshots'

    def test_positive_fixtures_and_revision(self):
        for p in (self.fixtures / 'valid').glob('*.json'):
            self.assertEqual(monthly.validate(load_json(p), self.artifacts), [])

    def test_negative_fixtures(self):
        for p in (self.fixtures / 'invalid').glob('*.json'):
            self.assertTrue(monthly.validate(load_json(p), self.artifacts))

    def test_pending_rejected_for_publication(self):
        self.assertIn('publication-not-approved', monthly.validate(self.data, self.artifacts, True))

    def test_approved_synthetic_is_still_synthetic(self):
        data = load_json(self.fixtures / 'valid/synthetic-approved-monthly.json')
        self.assertEqual(monthly.validate(data, self.artifacts, True), [])
        self.assertEqual(data['data_kind'], 'SYNTHETIC')

    def test_duplicate_reference_does_not_double_count(self):
        m = self.data['metrics'][0]
        m['references'].append(copy.deepcopy(m['references'][0]))
        m['value'] = 6
        self.assertIn('duplicate-reference', monthly.validate(self.data, self.artifacts))

    def test_duplicate_source(self):
        self.data['source_snapshots'].append(copy.deepcopy(self.data['source_snapshots'][0]))
        self.assertIn('duplicate-snapshot', monthly.validate(self.data, self.artifacts))

    def test_same_evidence_reserialized_cannot_double_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for p in self.artifacts.glob('*.json'):shutil.copyfile(p, root/p.name)
            other = copy.deepcopy(self.data['source_snapshots'][0])
            raw = json.dumps(other['record'], separators=(',', ':')).encode()
            (root/'reserialized.json').write_bytes(raw)
            other.update({'id':'synthetic-source-002', 'artifact_path':'reserialized.json',
                          'sha256':hashlib.sha256(raw).hexdigest()})
            self.data['source_snapshots'].append(other)
            self.data['metrics'][0]['references'].append({'snapshot_id':other['id'],
                                                        'metric_id':self.data['metrics'][0]['references'][0]['metric_id']})
            self.data['metrics'][0]['value'] = 6
            self.assertIn('duplicate-provenance', monthly.validate(self.data, root))

    def test_unknown_metric(self):
        self.data['metrics'][0]['references'][0]['metric_id'] = 'missing-source-metric'
        self.assertIn('unknown-evidence', monthly.validate(self.data, self.artifacts))

    def test_definition_or_unit_change_rejected(self):
        for key, value in [('definition', 'Changed meaning'), ('unit', 'participants'), ('level', 5)]:
            data = copy.deepcopy(self.data)
            data['metrics'][0][key] = value
            self.assertIn('metric-contract-mismatch', monthly.validate(data, self.artifacts))

    def test_full_coverage_claim_requires_source_coverage(self):
        self.data['metrics'][0]['coverage'] = 'full-period'
        self.assertIn('unsupported-coverage', monthly.validate(self.data, self.artifacts))

    def test_calendar_month_and_december_boundary(self):
        self.data['period']['end'] = '2026-10-31T00:00:00Z'
        self.assertIn('calendar-period', monthly.validate(self.data, self.artifacts))
        self.data['period'] = {'month':'2026-12', 'start':'2026-12-01T00:00:00Z', 'end':'2027-01-01T00:00:00Z'}
        errors = monthly.validate(self.data, self.artifacts)
        self.assertNotIn('calendar-period', errors)
        self.assertIn('evidence-outside-period', errors)

    def test_exclusions_and_count_arithmetic(self):
        m = self.data['metrics'][0]
        m['deduplication']['excluded_count'] = 1
        m['value'] = 2
        self.assertEqual(monthly.validate(self.data, self.artifacts), [])
        m['deduplication']['excluded_count'] = 10
        self.assertIn('aggregation-count', monthly.validate(self.data, self.artifacts))

    def test_draft_sources_cannot_be_promoted(self):
        self.data['metrics'][0]['verification']['status'] = 'verified'
        self.assertIn('unverified-source', monthly.validate(self.data, self.artifacts))

    def test_incomplete_quality_blocks_approval(self):
        data = load_json(self.fixtures / 'valid/synthetic-approved-monthly.json')
        data['data_quality'] = {'status':'incomplete', 'issues':['Synthetic missing observation.']}
        self.assertIn('publication-not-verified', monthly.validate(data, self.artifacts, True))

    def test_inconsistent_quality(self):
        self.data['data_quality']['issues'] = ['Missing observation']
        self.assertIn('data-quality-status', monthly.validate(self.data, self.artifacts))

    def test_approval_before_period_end_rejected(self):
        data = load_json(self.fixtures / 'valid/synthetic-approved-monthly.json')
        data['publication']['approved_at'] = '2026-10-10T00:00:00Z'
        self.assertIn('premature-approval', monthly.validate(data, self.artifacts))

    def test_withdrawn_publication_not_approved(self):
        self.data['publication']['state'] = 'withdrawn'
        self.assertIn('publication-not-approved', monthly.validate(self.data, self.artifacts, True))

    def test_missing_snapshot_and_bad_hash_fail_closed(self):
        self.data['source_snapshots'][0]['sha256'] = 'f'*64
        with self.assertRaises(ValueError):
            monthly.validate(self.data, self.artifacts)
        self.data['source_snapshots'][0]['artifact_path'] = 'missing.json'
        with self.assertRaises(OSError):
            monthly.validate(self.data, self.artifacts)

    def test_traversal_and_symlink_escape_rejected(self):
        self.data['source_snapshots'][0]['artifact_path'] = 'sub/../source-evidence.json'
        with self.assertRaises(ValueError):
            monthly.validate(self.data, self.artifacts)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'artifacts';root.mkdir()
            (root/'source-evidence.json').symlink_to(self.artifacts/'source-evidence.json')
            self.setUp()
            with self.assertRaises(ValueError):
                monthly.validate(self.data, root)

    def test_embedded_record_cannot_diverge(self):
        self.data['source_snapshots'][0]['record']['metrics'][0]['definition'] = 'Different source'
        self.assertIn('snapshot-record-mismatch', monthly.validate(self.data, self.artifacts))

    def test_data_kind_cannot_be_relabelled_real(self):
        self.data['data_kind'] = 'PUBLIC_AGGREGATE'
        self.assertIn('data-kind-mismatch', monthly.validate(self.data, self.artifacts))

    def test_revision_requires_full_history(self):
        self.data['revision']['number'] = 2
        self.assertIn('revision-history', monthly.validate(self.data, self.artifacts))

    def test_revision_id_and_digest_are_verified(self):
        data = load_json(self.fixtures / 'valid/synthetic-revised-monthly.json')
        data['report_id'] = 'unrelated-report'
        self.assertIn('history-contract-mismatch', monthly.validate(data, self.artifacts))
        data['revision']['history'][0]['sha256'] = 'f'*64
        with self.assertRaises(ValueError):
            monthly.validate(data, self.artifacts)

    def test_invalid_archived_aggregation_rejected_even_with_matching_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for p in self.artifacts.glob('*.json'):shutil.copyfile(p, root/p.name)
            data = load_json(self.fixtures/'valid/synthetic-revised-monthly.json')
            prior = load_json(root/'monthly-revision-1.json');prior['metrics'][0]['value'] = 100
            raw = json.dumps(prior).encode();(root/'monthly-revision-1.json').write_bytes(raw)
            data['revision']['history'][0]['sha256'] = hashlib.sha256(raw).hexdigest()
            self.assertIn('invalid-history-semantics', monthly.validate(data, root))

    def test_unknown_status_and_version_rejected(self):
        for key, value in [('schema_version','2.0.0')]:
            self.data[key] = value
            self.assertEqual(monthly.validate(self.data, self.artifacts), ['schema'])
        self.setUp();self.data['metrics'][0]['verification']['status'] = 'approved'
        self.assertEqual(monthly.validate(self.data, self.artifacts), ['schema'])

    def test_source_snapshots_are_not_ignored(self):
        for p in self.artifacts.glob('*.json'):
            r = subprocess.run(['git', 'check-ignore', '--quiet', str(p)], cwd=ROOT)
            self.assertEqual(r.returncode, 1)

    def test_cli_redacts_failure_and_missing_dependency(self):
        p = self.fixtures / 'valid/synthetic-monthly.json'
        r = subprocess.run([sys.executable,str(ROOT/'scripts/community/validate_monthly.py'),str(p),
                            '--artifact-root', str(ROOT/'missing-artifacts')],capture_output=True,text=True)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn('Traceback', r.stderr)
