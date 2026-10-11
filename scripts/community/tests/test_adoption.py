import copy
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/community'))
import validate_adoption as adoption
from contract_tools import load_json


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(ROOT / 'community/adoption/fixtures/valid/synthetic-reproduction.json')
        self.row = self.data['records'][0]

    def test_positive_fixture(self):
        self.assertEqual(adoption.validate(self.data), [])

    def test_synthetic_third_party_integration_fixture(self):
        data = load_json(ROOT / 'community/adoption/fixtures/valid/synthetic-integration.json')
        self.assertEqual(adoption.validate(data), [])
        self.assertEqual(data['records'][0]['claim_kind'], 'independent-adoption')
        self.assertEqual(data['data_kind'], 'SYNTHETIC')

    def test_negative_fixtures(self):
        for p in (ROOT / 'community/adoption/fixtures/invalid').glob('*.json'):
            self.assertTrue(adoption.validate(load_json(p)))

    def test_affiliated_external_is_not_independent(self):
        self.row['independence']['relationship'] = 'affiliated'
        self.assertIn('not-independent', adoption.validate(self.data))

    def test_internal_usage_not_independent_adoption(self):
        self.row['claim_kind'] = 'usage'
        self.row['independence']['classification'] = 'maintainer'
        self.assertEqual(adoption.validate(self.data), [])
        self.row['claim_kind'] = 'independent-adoption'
        self.assertIn('not-independent', adoption.validate(self.data))

    def test_engagement_and_person_fields_rejected(self):
        for key in ['stars', 'forks', 'hackathon_participants', 'email']:
            self.row[key] = 10
            self.assertEqual(adoption.validate(self.data), ['schema'])
            del self.row[key]

    def test_draft_unknown_relationship_allowed_but_not_verified(self):
        self.row['verification']['status'] = 'draft'
        self.row['independence']['relationship'] = 'unknown'
        self.assertEqual(adoption.validate(self.data), [])
        self.row['verification']['status'] = 'verified'
        self.assertIn('not-independent', adoption.validate(self.data))

    def test_real_data_cannot_use_dummy_source(self):
        self.data['data_kind'] = 'PUBLIC_AGGREGATE'
        errors = adoption.validate(self.data)
        self.assertIn('dummy-provenance', errors)
        self.assertIn('nonpublic-reference', errors)

    def test_verified_requires_review(self):
        self.row['verification']['review_reference'] = None
        self.assertIn('review-required', adoption.validate(self.data))

    def test_corrected_record_requires_superseded_prior(self):
        new = copy.deepcopy(self.row)
        new['id'] = 'synthetic-correction-002'
        new['correction'] = {'previous_id': self.row['id'], 'reason': 'Synthetic correction.'}
        self.data['records'].append(new)
        self.assertIn('prior-not-superseded', adoption.validate(self.data))
        self.row['record_state'] = 'superseded'
        self.assertEqual(adoption.validate(self.data), [])

    def test_duplicate_and_cyclic_records_rejected(self):
        self.data['records'].append(copy.deepcopy(self.row))
        self.assertIn('duplicate-adoption', adoption.validate(self.data))
        self.data['records'].pop()
        self.row['record_state'] = 'superseded'
        self.row['correction'] = {'previous_id': self.row['id'], 'reason': 'Invalid self correction.'}
        self.assertIn('correction-cycle', adoption.validate(self.data))

    def test_withdrawal_is_not_verified(self):
        self.row['record_state'] = 'withdrawn'
        self.assertIn('review-required', adoption.validate(self.data))
        self.row['verification']['status'] = 'draft'
        self.assertEqual(adoption.validate(self.data), [])

    def test_invalid_doi_reference(self):
        self.row['citations'] = [{'kind': 'doi', 'reference': 'https://example.invalid/synthetic/ref'}]
        self.assertIn('doi-reference', adoption.validate(self.data))
