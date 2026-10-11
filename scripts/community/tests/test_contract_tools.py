import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'scripts/community'))
import contract_tools
from validate_evidence import MAX_BYTES


class SnapshotIntegrityTests(unittest.TestCase):
    def test_hash_and_parse_use_same_bytes_when_file_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);path = root/'source.json';raw = b'{"synthetic":1}'
            path.write_bytes(raw);expected = hashlib.sha256(raw).hexdigest()
            real_hash = hashlib.sha256
            def mutate_after_hash(data):
                digest = real_hash(data)
                path.write_bytes(b'{"synthetic":2}')
                return digest
            with patch('contract_tools.hashlib.sha256', side_effect=mutate_after_hash):
                parsed = contract_tools.snapshot(root,'source.json',expected)
            self.assertEqual(parsed, {'synthetic':1})
            self.assertEqual(path.read_bytes(),b'{"synthetic":2}')

    def test_duplicate_json_fields_rejected_in_pinned_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = b'{"synthetic":1,"synthetic":2}'
            (Path(tmp)/'source.json').write_bytes(raw)
            with self.assertRaises(ValueError):
                contract_tools.snapshot(tmp,'source.json',hashlib.sha256(raw).hexdigest())

    def test_oversized_pinned_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = b' '*(MAX_BYTES+1);(Path(tmp)/'source.json').write_bytes(raw)
            with self.assertRaises(ValueError):
                contract_tools.snapshot(tmp,'source.json',hashlib.sha256(raw).hexdigest())
