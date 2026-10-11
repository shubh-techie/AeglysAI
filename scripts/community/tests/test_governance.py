from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[3]


class GovernanceTests(unittest.TestCase):
    def test_governance_evidence_and_templates_exist(self):
        for name in ['CONTRIBUTING.md','CODE_OF_CONDUCT.md','SECURITY_AND_DISCLOSURE_POLICY.md',
                     'community/README.md','community/ROADMAP.md','community/evidence/README.md',
                     '.github/ISSUE_TEMPLATE/community-task.md','.github/pull_request_template.md']:
            self.assertTrue((ROOT/name).is_file())

    def test_governance_local_links_resolve(self):
        for path in [ROOT/'CONTRIBUTING.md',ROOT/'CODE_OF_CONDUCT.md',ROOT/'community/evidence/README.md']:
            for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                target=target.split('#')[0]
                if target and ':' not in target:self.assertTrue((path.parent/target).exists())

    def test_roadmap_covers_all_eight_packages(self):
        text=(ROOT/'community/ROADMAP.md').read_text()
        for number in range(1,9):self.assertIn(f'COM-{number:03d}',text)
