"""Shared offline helpers; operator-owned paths, bounded input and redacted CLI errors."""
import argparse
import datetime
import hashlib
import ipaddress
from pathlib import Path
import sys
from urllib.parse import urlsplit
from validate_evidence import load_json, parse_json_bytes, validate as validate_evidence

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_SCHEMA = ROOT / 'community/evidence/schemas/evidence-1.0.0.schema.json'


def schema_errors(record, path, evidence_reference=False):
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    registry = Registry()
    if evidence_reference:
        evidence = load_json(EVIDENCE_SCHEMA)
        Draft202012Validator.check_schema(evidence)
        registry = registry.with_resource(evidence['$id'], Resource.from_contents(evidence))
    validator = Draft202012Validator(schema, format_checker=FormatChecker(), registry=registry)
    return ['schema'] if any(validator.iter_errors(record)) else []


def timestamp(value):
    parsed = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timezone')
    return parsed


def public_reference(value, data_kind):
    if value is None:
        return True
    host = urlsplit(value).hostname or ''
    bad = not host or host in ('localhost', 'localhost.localdomain') or host.endswith('.local')
    try:
        bad = bad or not ipaddress.ip_address(host).is_global
    except ValueError:
        pass
    if data_kind == 'PUBLIC_AGGREGATE':
        bad = bad or host.endswith(('.invalid', '.example'))
    return not bad


def safe_file(root, relative):
    if '\\' in relative or Path(relative).is_absolute() or any(p in ('.', '..') for p in relative.split('/')):
        raise ValueError('artifact path')
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('artifact boundary')
    return path


def snapshot(root, path, digest):
    from validate_evidence import MAX_BYTES
    resolved = safe_file(root, path)
    with resolved.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('snapshot integrity')
    return parse_json_bytes(raw)


def cli(validate, description, artifact=False):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('record', type=Path)
    if artifact:
        parser.add_argument('--artifact-root', required=True, type=Path)
        parser.add_argument('--publication', action='store_true')
    args = parser.parse_args()
    try:
        data = load_json(args.record)
        errors = validate(data, args.artifact_root, args.publication) if artifact else validate(data)
    except Exception:
        print('FAIL: contract unavailable, invalid input or artifact integrity failure', file=sys.stderr)
        return 2
    if errors:
        print('FAIL: ' + ', '.join(sorted(set(errors))), file=sys.stderr)
        return 1
    print('PASS: offline contract; human source, consent and publication approval remain required')
    return 0
