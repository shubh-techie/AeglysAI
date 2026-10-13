import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from research.acbsd import benchmark
from research.acbsd.dataset import generate, write_dataset


class BenchmarkTests(unittest.TestCase):
    def test_metrics_denominators_and_score_orientation(self):
        m = benchmark.metrics([0,0,1,1], np.array([.1,.7,.2,.9]), .5)
        self.assertEqual(m['confusion_matrix'], [[1,1],[1,1]])
        self.assertEqual(m['precision'], .5)
        self.assertEqual(m['recall'], .5)
        self.assertEqual(m['false_positive_rate'], .5)
        empty = benchmark.metrics([0,0], [.1,.2], .5)
        self.assertIsNone(empty['precision'])
        self.assertIsNone(empty['recall'])
        self.assertIsNone(empty['roc_auc'])
        self.assertIsNone(empty['pr_auc'])
        self.assertEqual(empty['false_positive_rate'], 0)

    def test_feature_allowlist_ignores_truth_and_identifiers(self):
        events, _, _ = generate(volume=20)
        altered = copy.deepcopy(events)
        for e in altered:
            e.update(anomaly=True, family='secret', identity_id='anything', timestamp='anything', asset_criticality=3)
        np.testing.assert_array_equal(benchmark.features(events), benchmark.features(altered))

    def test_surge_is_not_flagged_by_volume_alone(self):
        x = np.array([[900,0,0,0,1], [900,0,0,0,0]])
        np.testing.assert_array_equal(benchmark.deterministic_scores(x), [0,1])

    def test_threshold_uses_validation_and_cluster_intervals(self):
        y = np.array([0,0,1,1])
        scores = np.array([.1,.2,.8,.9])
        self.assertEqual(benchmark.select_threshold(y, scores), .8)
        labels = [{'anomaly': bool(v), 'instance_id': str(i//2)} for i,v in enumerate(y)]
        self.assertEqual(benchmark.cluster_intervals(labels,scores,.8,20),
                         benchmark.cluster_intervals(labels,scores,.8,20))

    def test_end_to_end_train_only_fit_and_test_label_independence(self):
        data = generate(volume=1000)
        train_n = sum(t['partition'] == 'train' for t in data[1])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_dataset(root/'data', *data)
            original = benchmark.StandardScaler.fit
            sizes = []
            def fit(scaler, values, *args, **kwargs):
                sizes.append(len(values))
                return original(scaler, values, *args, **kwargs)
            with patch.object(benchmark.StandardScaler, 'fit', fit):
                result = benchmark.run(root/'data', root/'results', bootstrap=10)
            self.assertEqual(sizes, [train_n])
            self.assertEqual(set(result['models']), {'deterministic','random_forest','isolation_forest'})
            self.assertTrue(all(m['partitions']['test']['n'] > 0 for m in result['models'].values()))
            # Keep validation inputs untouched, invert only held-out labels in loader.
            loaded = benchmark.load_dataset(root/'data')
            inverted = copy.deepcopy(loaded)
            for t in inverted[1]:
                if t['partition'] in ('test','holdout'):
                    t['anomaly'] = not t['anomaly']
            with patch.object(benchmark, 'load_dataset', return_value=inverted):
                other = benchmark.run(root/'data', root/'other', bootstrap=10)
            self.assertEqual([m['threshold'] for m in result['models'].values()],
                             [m['threshold'] for m in other['models'].values()])
            a = [json.loads(line)['score'] for line in (root/'results/predictions.jsonl').read_text().splitlines()]
            b = [json.loads(line)['score'] for line in (root/'other/predictions.jsonl').read_text().splitlines()]
            self.assertEqual(a, b)

    def test_failed_cli_run_is_recorded_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'failure'
            argv = ['benchmark', '--dataset', str(Path(directory)/'missing'), '--output', str(output)]
            with patch('sys.argv', argv), self.assertRaises(FileNotFoundError):
                benchmark.main()
            failure = json.loads((output/'failure.json').read_bytes())
            self.assertEqual(failure['status'], 'FAILED')
            original = (output/'failure.json').read_bytes()
            with patch('sys.argv', argv), self.assertRaises(FileExistsError):
                benchmark.main()
            self.assertEqual((output/'failure.json').read_bytes(), original)
