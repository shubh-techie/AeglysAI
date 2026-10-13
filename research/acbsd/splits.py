"""Export verified grouped partitions without fitting or consuming evaluation labels."""
import argparse
import json
from pathlib import Path

from .dataset import PARTITIONS, digest, encode, load_dataset
from .verify import verify


def export(dataset, output):
    verify(dataset)
    events, truth, _ = load_dataset(dataset)
    lookup = {t['event_id']: t for t in truth}
    destination = Path(output)
    destination.mkdir(parents=True, exist_ok=False)
    report = {'dataset_manifest_sha256': digest((Path(dataset)/'manifest.json').read_bytes()),
              'partitions': {}}
    for partition in PARTITIONS:
        selected = [e for e in events if lookup[e['event_id']]['partition'] == partition]
        labels = [lookup[e['event_id']] for e in selected]
        files = {}
        for kind, rows in [('events', selected), ('ground_truth', labels)]:
            name = f'{partition}-{kind}.jsonl'
            data = ''.join(json.dumps(r, sort_keys=True, allow_nan=False)+'\n' for r in rows).encode()
            (destination/name).write_bytes(data)
            files[name] = {'sha256': digest(data), 'bytes': len(data)}
        report['partitions'][partition] = {'rows': len(selected), 'files': files}
    (destination/'manifest.json').write_bytes(encode(report))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', required=True)
    print(json.dumps(export(**vars(parser.parse_args())), sort_keys=True))
