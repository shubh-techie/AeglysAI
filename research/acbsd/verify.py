"""Verify artifact hashes, schema, leakage and deterministic regeneration."""
import argparse
from pathlib import Path
import tempfile
from .dataset import encode, generate, load_dataset


def verify(path):
    events, truth, manifest = load_dataset(path)
    config = manifest['config']
    with tempfile.TemporaryDirectory(prefix='acbsd-verify-') as temporary:
        scenarios = Path(temporary)/'scenarios.json'
        scenarios.write_bytes(encode(config['scenarios']))
        rebuilt = generate(seed=config['seed'], identities=config['identities'],
                           workloads=config['workloads'], duration=config['duration_seconds'],
                           volume=config['volume'], scenario_path=scenarios, holdout=config['holdout'], split=config.get('split', 'random'))
    if rebuilt != (events, truth, config):
        raise ValueError('deterministic regeneration mismatch')
    return manifest['quality']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset')
    print(verify(parser.parse_args().dataset))
