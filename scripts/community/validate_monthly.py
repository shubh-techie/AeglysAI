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
import datetime
try:
    from contract_tools import snapshot, validate_evidence
except ImportError:
    print('FAIL: evidence dependency unavailable', file=sys.stderr)
    raise SystemExit(2)
SCHEMA = ROOT / 'community/reporting/schemas/monthly-impact-1.0.0.schema.json'


def validate(record, artifact_root, publication=False, _validate_history=True):
    errors = schema_errors(record, SCHEMA, evidence_reference=True)
    if errors:
        return errors
    try:
        start = timestamp(record['period']['start'])
        end = timestamp(record['period']['end'])
        year, month = map(int, record['period']['month'].split('-'))
        expected_start = datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc)
        expected_end = datetime.datetime(year + (month == 12), month % 12 + 1, 1, tzinfo=datetime.timezone.utc)
        if start != expected_start or end != expected_end:
            errors.append('calendar-period')
    except ValueError:
        return ['calendar-period']
    sources = {}
    digests = set()
    for item in record['source_snapshots']:
        if item['id'] in sources or item['sha256'] in digests:
            errors.append('duplicate-snapshot')
        digests.add(item['sha256'])
        raw = snapshot(artifact_root, item['artifact_path'], item['sha256'])
        if raw != item['record']:
            errors.append('snapshot-record-mismatch')
        source_errors = validate_evidence(raw)
        if source_errors:
            errors.append('invalid-evidence')
            continue
        if raw['data_kind'] != record['data_kind']:
            errors.append('data-kind-mismatch')
        sources[item['id']] = {m['id']: m for m in raw['metrics']}
    metric_ids = set()
    used = set()
    seen_provenance = set()
    for metric in record['metrics']:
        if metric['id'] in metric_ids:
            errors.append('duplicate-metric')
        metric_ids.add(metric['id'])
        counts = 0
        all_verified = True
        full_coverage = False
        intervals = []
        for ref in metric['references']:
            key = (ref['snapshot_id'], ref['metric_id'])
            if key in used:
                errors.append('duplicate-reference')
            used.add(key)
            source = sources.get(key[0], {}).get(key[1])
            if source is None:
                errors.append('unknown-evidence')
                all_verified = False
                continue
            if (source['definition'], source['unit'], source['level']) != (metric['definition'], metric['unit'], metric['level']):
                errors.append('metric-contract-mismatch')
            s = timestamp(source['period']['start'])
            e = timestamp(source['period']['end'])
            if s < start or e > end:
                errors.append('evidence-outside-period')
            provenance = (source['id'], source['source']['reference'], source['source']['sha256'], s, e)
            if provenance in seen_provenance:
                errors.append('duplicate-provenance')
            seen_provenance.add(provenance)
            intervals.append((s, e))
            counts += source['count']
            all_verified &= source['verification']['status'] == 'verified'
        # Coverage is a union of intervals; gaps cannot be labelled full-period.
        cursor = start
        for s, e in sorted(intervals):
            if s > cursor:
                break
            cursor = max(cursor, e)
        full_coverage = cursor >= end
        if metric['coverage'] == 'full-period' and not full_coverage:
            errors.append('unsupported-coverage')
        excluded = metric['deduplication']['excluded_count']
        if excluded > counts or metric['value'] != counts - excluded:
            errors.append('aggregation-count')
        if metric['verification']['status'] == 'verified' and not all_verified:
            errors.append('unverified-source')
    quality = record['data_quality']
    if (quality['status'] == 'complete') != (not quality['issues']):
        errors.append('data-quality-status')
    approval = record['publication']
    approved = approval['state'] == 'approved'
    if approved:
        if not approval['review_reference'] or not approval['approved_at']:
            errors.append('approval-required')
        else:
            if not public_reference(approval['review_reference'], record['data_kind']):
                errors.append('nonpublic-reference')
            try:
                if timestamp(approval['approved_at']) < end:
                    errors.append('premature-approval')
            except ValueError:
                errors.append('approval-timestamp')
        if quality['status'] != 'complete' or any(m['verification']['status'] != 'verified' for m in record['metrics']):
            errors.append('publication-not-verified')
    elif approval['approved_at'] is not None or approval['review_reference'] is not None:
        errors.append('inactive-approval')
    if publication and not approved:
        errors.append('publication-not-approved')
    revision = record['revision']
    history = revision['history']
    if len(history) != revision['number'] - 1:
        errors.append('revision-history')
    if not _validate_history:
        return sorted(set(errors))
    history_paths = set()
    for index, historical in enumerate(history, 1):
        if historical['revision'] != index or historical['artifact_path'] in history_paths:
            errors.append('revision-order')
        history_paths.add(historical['artifact_path'])
        previous = snapshot(artifact_root, historical['artifact_path'], historical['sha256'])
        if schema_errors(previous, SCHEMA, evidence_reference=True):
            errors.append('invalid-history')
            continue
        if validate(previous, artifact_root, False, _validate_history=False):
            errors.append('invalid-history-semantics')
        if (previous['report_id'] != record['report_id'] or previous['period'] != record['period']
                or previous['data_kind'] != record['data_kind'] or previous['revision']['number'] != index
                or previous['revision']['history'] != history[:index - 1]):
            errors.append('history-contract-mismatch')
    return sorted(set(errors))


if __name__ == '__main__':
    sys.exit(cli(validate, 'Validate monthly reporting and pinned local artifacts offline.', artifact=True))
