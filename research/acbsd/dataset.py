"""Versioned synthetic observation windows and independent scenario provenance."""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import ipaddress
import json
from pathlib import Path
import random
import platform
import re

from . import VERSION

SCENARIOS = Path(__file__).parent / 'scenarios/v1.json'
FEATURES = ('request_count', 'failure_ratio', 'privilege_delta', 'peer_novelty', 'scheduled_operation')
EVENT_KEYS = {'event_id', 'timestamp', 'identity_id', 'workload_id', 'peer_workload_id',
              'source_ip', 'category', 'asset_criticality', *FEATURES}
TRUTH_KEYS = {'event_id', 'instance_id', 'family', 'anomaly', 'partition'}
PARTITIONS = ('train', 'validation', 'test', 'holdout')
START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_hashes():
    root = Path(__file__).parent
    return {str(p.relative_to(root)): digest(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file() and p.suffix in ('.py', '.json', '.txt')
            and 'examples' not in p.parts and '__pycache__' not in p.parts}


def generate(seed=42, identities=20, workloads=12, duration=86400, volume=4000,
             scenario_path=SCENARIOS, holdout='workload_communication'):
    for value in (seed, identities, workloads, duration, volume):
        if type(value) is not int:
            raise ValueError('integer configuration required')
    if identities < 1 or workloads < 2 or duration < 1 or volume < 1:
        raise ValueError('positive sizes; at least two workloads')
    scenario_bytes = Path(scenario_path).read_bytes()
    catalog = json.loads(scenario_bytes)
    families = dict(sorted(catalog['families'].items()))
    if catalog['version'] != VERSION or holdout not in families:
        raise ValueError('unsupported version or holdout')
    probabilities = [f['probability'] for f in families.values()]
    if any(type(p) not in (int, float) or not 0 <= p <= 1 for p in probabilities) or abs(sum(probabilities)-1) > 1e-9:
        raise ValueError('probabilities must sum to one')
    for params in families.values():
        if set(params) != {'probability', 'category', 'anomaly', 'rate', 'failure', 'privilege', 'novelty', 'scheduled'}:
            raise ValueError('scenario schema')
        if params['category'] not in ('authentication', 'api', 'workload') or type(params['anomaly']) is not bool or type(params['scheduled']) is not bool:
            raise ValueError('scenario vocabulary')
        for key in ('rate', 'failure', 'privilege', 'novelty'):
            bounds = params[key]
            if len(bounds) != 2 or any(type(v) not in (int, float) for v in bounds) or not 0 <= bounds[0] <= bounds[1] < float('inf'):
                raise ValueError('scenario bounds')
            if key != 'rate' and bounds[1] > 1:
                raise ValueError('scenario ratio')
        if params['privilege'] not in ([0, 0], [1, 1]):
            raise ValueError('privilege bounds must be fixed binary')
    rng = random.Random(seed)
    events, truth = [], []
    # Correlated bursts of up to five windows; gaps separate instances.
    for instance in range((volume + 4)//5):
        family = rng.choices(list(families), weights=probabilities)[0]
        params = families[family]
        partition = 'holdout' if family == holdout else rng.choices(PARTITIONS[:3], [.6, .2, .2])[0]
        identity, workload = rng.randrange(identities), rng.randrange(workloads)
        peer = (workload + rng.randrange(1, workloads)) % workloads
        base = {k: rng.uniform(*params[k]) for k in ('rate', 'failure', 'novelty')}
        criticality = rng.randrange(1, 4)
        for offset in range(min(5, volume - len(events))):
            index = len(events)
            event_id = f'evt-{index:09d}'
            events.append(dict(event_id=event_id,
                timestamp=(START + timedelta(seconds=duration*(index+1)/(volume+1))).isoformat(timespec='microseconds'),
                identity_id=f'identity-{identity:04d}', workload_id=f'workload-{workload:04d}',
                peer_workload_id=f'workload-{peer:04d}', source_ip=f'192.0.2.{identity % 254 + 1}',
                category=params['category'], asset_criticality=criticality,
                request_count=max(0, round(base['rate'] * rng.uniform(.8, 1.2))),
                failure_ratio=round(min(1, max(0, base['failure'] + rng.uniform(-.05, .05))), 6),
                privilege_delta=int(params['privilege'][0]),
                peer_novelty=round(min(1, max(0, base['novelty'] + rng.uniform(-.05, .05))), 6),
                scheduled_operation=params['scheduled']))
            truth.append(dict(event_id=event_id, instance_id=f'instance-{instance:08d}', family=family,
                              anomaly=params['anomaly'], partition=partition))
    config = dict(version=VERSION, data_kind='SYNTHETIC', seed=seed, identities=identities,
                  workloads=workloads, duration_seconds=duration, volume=volume, holdout=holdout,
                  scenario_sha256=digest(encode(catalog)), scenarios=catalog)
    validate(events, truth, config)
    return events, truth, config


def validate(events, truth, config):
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(config['version'] == VERSION and config['data_kind'] == 'SYNTHETIC', 'version/kind')
    require(len(events) == len(truth) == config['volume'], 'row count')
    require(len({e['event_id'] for e in events}) == len(events), 'duplicate event id')
    require(len({t['event_id'] for t in truth}) == len(truth), 'duplicate truth id')
    labels = {t['event_id']: t for t in truth}
    groups, payloads, previous = {}, set(), START
    for event in events:
        require(set(event) == EVENT_KEYS and all(v is not None for v in event.values()), 'schema/missing value')
        require(re.fullmatch(r'evt-\d{9}', event['event_id']) is not None, 'event id')
        time = datetime.fromisoformat(event['timestamp'])
        require(time.tzinfo == timezone.utc and previous < time < START + timedelta(seconds=config['duration_seconds']), 'timestamp')
        previous = time
        for key, prefix, limit in [('identity_id', 'identity', config['identities']),
                                   ('workload_id', 'workload', config['workloads']),
                                   ('peer_workload_id', 'workload', config['workloads'])]:
            value = event[key]
            require(isinstance(value, str) and re.fullmatch(prefix+r'-\d{4,}', value) is not None, 'entity format')
            require(0 <= int(value.split('-')[1]) < limit, 'entity reference')
        require(event['workload_id'] != event['peer_workload_id'], 'self peer')
        require(ipaddress.ip_address(event['source_ip']) in ipaddress.ip_network('192.0.2.0/24'), 'documentation IP')
        require(event['source_ip'] == f"192.0.2.{int(event['identity_id'].split('-')[1]) % 254 + 1}", 'identity IP relationship')
        require(event['category'] in ('authentication', 'api', 'workload'), 'category')
        require(type(event['request_count']) is int and event['request_count'] >= 0, 'count')
        require(type(event['privilege_delta']) is int and event['privilege_delta'] in (0, 1), 'privilege')
        require(type(event['asset_criticality']) is int and event['asset_criticality'] in (1, 2, 3), 'criticality')
        require(type(event['scheduled_operation']) is bool, 'scheduled')
        for key in ('failure_ratio', 'peer_novelty'):
            require(type(event[key]) in (float, int) and 0 <= event[key] <= 1, 'ratio')
        payload = encode({k: v for k, v in event.items() if k not in ('event_id', 'timestamp')})
        require(payload not in payloads, 'duplicate observation payload')
        payloads.add(payload)
        require(event['event_id'] in labels, 'truth join')
        t = labels[event['event_id']]
        require(set(t) == TRUTH_KEYS and re.fullmatch(r'instance-\d{8}', t['instance_id']) is not None, 'truth schema')
        require(t['family'] in config['scenarios']['families'] and t['partition'] in PARTITIONS, 'truth vocabulary')
        scenario = config['scenarios']['families'][t['family']]
        require(type(t['anomaly']) is bool and t['anomaly'] == scenario['anomaly'] and event['category'] == scenario['category'], 'provenance')
        require((t['partition'] == 'holdout') == (t['family'] == config['holdout']), 'family leakage')
        relationship = (t['partition'], t['family'], event['identity_id'], event['workload_id'], event['peer_workload_id'])
        require(groups.setdefault(t['instance_id'], relationship) == relationship, 'group leakage/relationship')
    return {'rows': len(events), 'instances': len(groups),
            'labels': dict(Counter(str(t['anomaly']) for t in truth)),
            'families': dict(Counter(t['family'] for t in truth)),
            'partitions': {p: dict(Counter(str(t['anomaly']) for t in truth if t['partition'] == p)) for p in PARTITIONS}}


def write_dataset(path, events, truth, config):
    quality = validate(events, truth, config)
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for name, rows in [('events.jsonl', events), ('ground_truth.jsonl', truth)]:
        data = b''.join((json.dumps(r, sort_keys=True, allow_nan=False)+'\n').encode() for r in rows)
        (path/name).write_bytes(data)
        hashes[name] = digest(data)
    (path/'manifest.json').write_bytes(encode(dict(config=config, quality=quality, files=hashes,
                                                  source_hashes=source_hashes(), generator_python=platform.python_version())))


def load_dataset(path):
    path = Path(path)
    manifest = json.loads((path/'manifest.json').read_bytes())
    if set(manifest['files']) != {'events.jsonl', 'ground_truth.jsonl'}:
        raise ValueError('unexpected artifact names')
    for name, expected in manifest['files'].items():
        if digest((path/name).read_bytes()) != expected:
            raise ValueError('integrity mismatch')
    config = manifest['config']
    if digest(encode(config['scenarios'])) != config['scenario_sha256']:
        raise ValueError('scenario integrity mismatch')
    events, truth = [[json.loads(line) for line in (path/name).read_text().splitlines()]
                     for name in ('events.jsonl', 'ground_truth.jsonl')]
    if validate(events, truth, config) != manifest['quality']:
        raise ValueError('quality report mismatch')
    return events, truth, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    for name, default in [('seed', 42), ('identities', 20), ('workloads', 12), ('duration', 86400), ('volume', 4000)]:
        parser.add_argument('--'+name, type=int, default=default)
    parser.add_argument('--scenarios', type=Path, default=SCENARIOS)
    parser.add_argument('--holdout', default='workload_communication')
    args = vars(parser.parse_args())
    output = args.pop('output')
    args['scenario_path'] = args.pop('scenarios')
    write_dataset(output, *generate(**args))
    print(json.dumps(load_dataset(output)[2]['quality'], sort_keys=True))


if __name__ == '__main__':
    main()
