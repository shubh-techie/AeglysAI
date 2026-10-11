#!/usr/bin/env python3
"""Offline evidence contract validation; never print submitted values."""
import argparse
import datetime
import ipaddress
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

MAX_BYTES = 1024 * 1024
SCHEMA = Path(__file__).resolve().parents[2] / 'community/evidence/schemas/evidence-1.0.0.schema.json'


def load_json(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    return parse_json_bytes(raw)


def parse_json_bytes(raw):
    if len(raw) > MAX_BYTES:
        raise ValueError('size limit')
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate field')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite')))


def validate(record, require_verified=False, schema_path=SCHEMA):
    from jsonschema import Draft202012Validator, FormatChecker
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    if any(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)):
        return ['schema']
    errors = []
    identifiers = set()
    expected = 'synthetic' if record['data_kind'] == 'SYNTHETIC' else 'public-aggregate'
    for metric in record['metrics']:
        if metric['id'] in identifiers:
            errors.append('duplicate-metric')
        identifiers.add(metric['id'])
        try:
            start = datetime.datetime.fromisoformat(metric['period']['start'].replace('Z', '+00:00'))
            end = datetime.datetime.fromisoformat(metric['period']['end'].replace('Z', '+00:00'))
            if start.tzinfo is None or end.tzinfo is None:
                return ['schema']
        except ValueError:
            return ['schema']
        if start >= end:
            errors.append('period-order')
        dedup = metric['deduplication']
        if metric['count'] != dedup['raw_count'] - dedup['excluded_count']:
            errors.append('deduplication-count')
        if metric['source']['kind'] != expected:
            errors.append('source-kind')
        for reference in [metric['source']['reference'], metric['verification']['review_reference']]:
            host = urlsplit(reference).hostname or ''
            forbidden = host in ('localhost', 'localhost.localdomain') or host.endswith('.local')
            try:
                forbidden = forbidden or not ipaddress.ip_address(host).is_global
            except ValueError:
                pass
            if forbidden:
                errors.append('nonpublic-reference')
            if expected == 'public-aggregate' and (host.endswith('.invalid') or host.endswith('.example')):
                errors.append('synthetic-reference')
        if require_verified and metric['verification']['status'] != 'verified':
            errors.append('unverified')
        if expected == 'public-aggregate' and metric['source']['sha256'] == '0' * 64:
            errors.append('dummy-digest')
    return sorted(set(errors))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--require-verified', action='store_true')
    args = parser.parse_args(argv)
    try:
        errors = validate(load_json(args.record), args.require_verified)
    except Exception:
        print('FAIL: evidence validation unavailable or input invalid', file=sys.stderr)
        return 2
    if errors:
        print('FAIL: ' + ', '.join(errors), file=sys.stderr)
        return 1
    print('PASS: evidence contract; source truth and publication approval require human review')
    return 0


if __name__ == '__main__':
    sys.exit(main())
