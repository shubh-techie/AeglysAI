import copy
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/community'))
import validate_recognition as recognition
from contract_tools import load_json


class RecognitionTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(ROOT / 'community/contributors/fixtures/valid/synthetic-recognition.json')
        self.item = self.data['recognitions'][0]

    def test_positive_and_withdrawal_fixtures(self):
        for p in (ROOT / 'community/contributors/fixtures/valid').glob('*.json'):
            self.assertEqual(recognition.validate(load_json(p)), [])

    def test_negative_fixtures(self):
        for p in (ROOT / 'community/contributors/fixtures/invalid').glob('*.json'):
            self.assertTrue(recognition.validate(load_json(p)))

    def test_publication_requires_explicit_consent(self):
        for state in ['not-requested', 'withdrawn']:
            self.item['consent']['state'] = state
            self.assertTrue(recognition.validate(self.data))

    def test_publication_requires_review_and_acceptance(self):
        for key in ['contribution_accepted', 'contribution_reference']:
            data = copy.deepcopy(self.data)
            data['recognitions'][0][key] = False if key == 'contribution_accepted' else None
            self.assertTrue(recognition.validate(data))
        self.item['publication']['review_approved'] = False
        self.assertIn('publication-review-required', recognition.validate(self.data))

    def test_no_person_fields(self):
        for key in ['name', 'email', 'handle', 'award', 'endorsement']:
            self.item[key] = 'synthetic marker'
            self.assertEqual(recognition.validate(self.data), ['schema'])
            del self.item[key]

    def test_anonymous_still_requires_consent(self):
        self.item['credit_mode'] = 'anonymous'
        self.item['consent']['state'] = 'not-requested'
        self.assertIn('consent-required', recognition.validate(self.data))

    def test_withdrawal_requires_tombstone(self):
        self.item['publication']['state'] = 'withdrawn'
        self.assertIn('withdrawal-minimization', recognition.validate(self.data))

    def test_duplicate_records(self):
        self.data['recognitions'].append(copy.deepcopy(self.item))
        self.assertIn('duplicate-recognition', recognition.validate(self.data))

    def test_invalid_date(self):
        self.item['recorded_at'] = '2026-02-30T00:00:00Z'
        self.assertIn('timestamp', recognition.validate(self.data))

    def test_nonpublic_reference(self):
        self.item['contribution_reference'] = 'https://localhost/source'
        self.assertIn('nonpublic-reference', recognition.validate(self.data))

    def test_draft_does_not_require_publication_consent(self):
        self.item['publication']['state'] = 'draft'
        self.item['publication']['review_approved'] = False
        self.item['consent'] = {'state': 'not-requested', 'scope': 'none', 'review_reference': None}
        self.assertEqual(recognition.validate(self.data), [])

    def test_onboarding_documents_complete(self):
        for name in ['QUICKSTART.md', 'GOOD-FIRST-ISSUES.md', 'LIFECYCLE.md', 'HACKATHON-TRANSITION.md', 'RECOGNITION.md']:
            self.assertTrue((ROOT / 'community/contributors' / name).is_file())
