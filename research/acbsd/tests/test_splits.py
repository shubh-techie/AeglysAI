import json
from pathlib import Path
import tempfile
import unittest

from research.acbsd.dataset import generate, load_dataset, write_dataset
from research.acbsd.splits import export


class SplitExportTests(unittest.TestCase):
    def test_exports_preserve_observations_and_isolate_instances(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_dataset(root/'dataset', *generate(volume=1000, split='chronological'))
            report = export(root/'dataset', root/'splits')
            self.assertEqual(sum(p['rows'] for p in report['partitions'].values()), 1000)
            instances, exported = {}, []
            for partition in report['partitions']:
                events = [json.loads(line) for line in (root/'splits'/f'{partition}-events.jsonl').read_text().splitlines()]
                truth = [json.loads(line) for line in (root/'splits'/f'{partition}-ground_truth.jsonl').read_text().splitlines()]
                self.assertEqual([e['event_id'] for e in events], [t['event_id'] for t in truth])
                exported.extend(events)
                for label in truth:
                    self.assertEqual(instances.setdefault(label['instance_id'], partition), partition)
            original = load_dataset(root/'dataset')[0]
            self.assertEqual(sorted(exported, key=lambda e: e['event_id']), original)
            with self.assertRaises(FileExistsError):
                export(root/'dataset', root/'splits')
