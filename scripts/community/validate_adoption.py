#!/usr/bin/env python3
import os
from pathlib import Path
import sys
DEPENDENCY_ROOT = Path(os.environ.get('AEGLYSAI_COMMUNITY_ROOT', Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(DEPENDENCY_ROOT / 'scripts/community'))
try:
    from contract_tools import cli, schema_errors, timestamp, public_reference
except ImportError:
    print('FAIL: community contract dependency unavailable', file=sys.stderr)
    raise SystemExit(2)
ROOT = Path(__file__).resolve().parents[2]

SCHEMA = ROOT / 'community/adoption/schemas/adoption-1.0.0.schema.json'


def validate(record):
    errors = schema_errors(record, SCHEMA)
    if errors:
        return errors
    rows = record['records']
    ids = {r['id'] for r in rows}
    by_id = {r['id']: r for r in rows}
    if len(ids) != len(rows):
        errors.append('duplicate-adoption')
    corrected_ids = set()
    for row in rows:
        refs = [row['source']['reference'], row['execution']['reference'], row['verification']['review_reference']]
        refs.extend(c['reference'] for c in row['citations'])
        if any(not public_reference(ref, record['data_kind']) for ref in refs):
            errors.append('nonpublic-reference')
        if record['data_kind'] == 'PUBLIC_AGGREGATE' and row['source']['sha256'] == '0' * 64:
            errors.append('dummy-provenance')
        for citation in row['citations']:
            if citation['kind'] == 'doi' and not citation['reference'].startswith('https://doi.org/10.'):
                errors.append('doi-reference')
        if row['verification']['status'] == 'verified':
            if not row['verification']['review_reference'] or row['record_state'] == 'withdrawn':
                errors.append('review-required')
            if row['claim_kind'] in ('independent-adoption', 'independent-reproduction'):
                independent = row['independence']
                if independent['classification'] != 'external' or independent['relationship'] != 'independent':
                    errors.append('not-independent')
                if row['execution']['status'] != 'executed' or not row['execution']['reference']:
                    errors.append('execution-required')
        correction = row['correction']
        if correction:
            previous = correction['previous_id']
            if previous == row['id'] or previous not in ids or previous in corrected_ids:
                errors.append('correction-reference')
            elif by_id[previous]['record_state'] != 'superseded':
                errors.append('prior-not-superseded')
            corrected_ids.add(previous)
    # A correction chain must terminate; cyclic assertions cannot be authoritative.
    for row in rows:
        seen = set()
        current = row
        while current.get('correction'):
            previous = current['correction']['previous_id']
            if previous in seen:
                errors.append('correction-cycle')
                break
            seen.add(previous)
            if previous not in by_id:
                break
            current = by_id[previous]
    return sorted(set(errors))


if __name__ == '__main__':
    sys.exit(cli(validate, 'Validate independent adoption assertions offline; human provenance review required.'))
