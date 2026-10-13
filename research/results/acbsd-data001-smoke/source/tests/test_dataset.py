import copy
import json
from pathlib import Path
import tempfile
import unittest

from research.acbsd.dataset import (FEATURES, SCENARIOS, generate, load_dataset,
                                   validate, write_dataset)
from research.acbsd.verify import verify


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.data = generate(volume=1000)

    def test_reproducible_bytes_and_seed_effect(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory)/'a', Path(directory)/'b'
            write_dataset(a, *self.data)
            write_dataset(b, *generate(volume=1000))
            for name in ('events.jsonl', 'ground_truth.jsonl', 'manifest.json'):
                self.assertEqual((a/name).read_bytes(), (b/name).read_bytes())
            self.assertEqual(verify(a)['rows'], 1000)
        self.assertNotEqual(self.data[0], generate(seed=43, volume=1000)[0])

    def test_all_families_and_hard_negative(self):
        events, truth, config = self.data
        self.assertEqual(set(config['scenarios']['families']), {t['family'] for t in truth})
        surge = [e for e, t in zip(events, truth) if t['family'] == 'operational_surge']
        self.assertTrue(any(e['request_count'] > 100 for e in surge))
        self.assertTrue(all(e['scheduled_operation'] for e in surge))
        self.assertTrue(all(not t['anomaly'] for t in truth if t['family'] == 'operational_surge'))
        self.assertTrue(all(e['privilege_delta'] == 1 for e, t in zip(events, truth) if t['family'] == 'privilege_usage'))
        self.assertFalse(set(FEATURES) & {'event_id', 'family', 'anomaly', 'instance_id', 'partition', 'asset_criticality'})

    def test_groups_and_family_holdout(self):
        groups = {}
        for t in self.data[1]:
            groups.setdefault(t['instance_id'], set()).add(t['partition'])
            self.assertEqual(t['partition'] == 'holdout', t['family'] == 'workload_communication')
        self.assertTrue(all(len(p) == 1 for p in groups.values()))

    def assert_bad(self, edit):
        data = copy.deepcopy(self.data)
        edit(*data)
        with self.assertRaises((ValueError, TypeError)):
            validate(*data)

    def test_quality_rejects_mutations(self):
        edits = [lambda e,t,c: e[0].update(request_count=None),
                 lambda e,t,c: e[0].update(request_count=True),
                 lambda e,t,c: e[0].update(source_ip='8.8.8.8'),
                 lambda e,t,c: e[0].update(identity_id='identity-9999'),
                 lambda e,t,c: e[0].update(category='production'),
                 lambda e,t,c: e[0].update(peer_novelty=float('nan')),
                 lambda e,t,c: e[1].update(event_id=e[0]['event_id']),
                 lambda e,t,c: e[1].update(timestamp=e[0]['timestamp']),
                 lambda e,t,c: t[1].update(partition='holdout' if t[0]['partition'] != 'holdout' else 'train'),
                 lambda e,t,c: t[0].update(anomaly=not t[0]['anomaly']),
                 lambda e,t,c: e[0].update(label=True)]
        for edit in edits:
            with self.subTest(edit=edit):
                self.assert_bad(edit)
        def duplicate(e, t, c):
            e[1].update({k: v for k, v in e[0].items() if k not in ('event_id', 'timestamp')})
        self.assert_bad(duplicate)

    def test_tamper_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'data'
            write_dataset(path, *self.data)
            with self.assertRaises(FileExistsError):
                write_dataset(path, *self.data)
            with (path/'events.jsonl').open('ab') as stream:
                stream.write(b'\n')
            with self.assertRaisesRegex(ValueError, 'integrity'):
                load_dataset(path)

    def test_bad_configuration_and_partial_instance(self):
        for config in ({'volume': 0}, {'identities': 0}, {'workloads': 1}, {'duration': -1}, {'seed': True}):
            with self.assertRaises(ValueError):
                generate(**config)
        self.assertEqual(len(generate(volume=7)[0]), 7)
        catalog = json.loads(SCENARIOS.read_text())
        catalog['families']['normal_auth']['probability'] = .9
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/'bad.json'
            p.write_text(json.dumps(catalog))
            with self.assertRaises(ValueError):
                generate(scenario_path=p)
