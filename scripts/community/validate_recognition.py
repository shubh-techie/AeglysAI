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

SCHEMA = ROOT / 'community/contributors/schemas/recognition-1.0.0.schema.json'


def validate(record):
    errors = schema_errors(record, SCHEMA)
    if errors:
        return errors
    ids = set()
    for item in record['recognitions']:
        if item['id'] in ids:
            errors.append('duplicate-recognition')
        ids.add(item['id'])
        try:
            timestamp(item['recorded_at'])
        except ValueError:
            errors.append('timestamp')
        consent = item['consent']
        publication = item['publication']
        for ref in [item['contribution_reference'], consent['review_reference']]:
            if not public_reference(ref, record['data_kind']):
                errors.append('nonpublic-reference')
        if publication['state'] == 'published':
            if consent['state'] != 'granted' or consent['scope'] != 'public-attribution' or not consent['review_reference']:
                errors.append('consent-required')
            if not publication['review_approved'] or not item['contribution_accepted'] or not item['contribution_reference'] or item['credit_mode'] == 'none':
                errors.append('publication-review-required')
        if consent['state'] == 'withdrawn' or publication['state'] == 'withdrawn':
            if (consent['state'] != 'withdrawn' or consent['scope'] != 'none' or consent['review_reference'] is not None
                    or publication['state'] != 'withdrawn' or publication['review_approved']
                    or item['credit_mode'] != 'none' or item['contribution_reference'] is not None):
                errors.append('withdrawal-minimization')
    return sorted(set(errors))


if __name__ == '__main__':
    sys.exit(cli(validate, 'Validate public-safe contributor recognition offline.'))
