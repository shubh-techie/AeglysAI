import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]


class HackathonContractTests(unittest.TestCase):
    def test_exactly_five_distinct_tracks_and_runnable_json_inputs(self):
        tracks = list((ROOT / 'community/hackathon/tracks').glob('*.md'))
        self.assertEqual(len(tracks), 5)
        names = set()
        for path in tracks:
            text = path.read_text()
            names.add(text.splitlines()[0])
            self.assertIn('Any language; AeglysAI integration is optional.', text)
            for heading in ['## Goal', '## Input contract', '## Minimum acceptance criteria',
                            '## Suggested tests', '## Safety and limitations']:
                self.assertIn(heading, text)
            blocks = re.findall(r'```json\n(.*?)\n```', text, re.S)
            self.assertEqual(len(blocks), 1)
            data = json.loads(blocks[0])
            self.assertIsInstance(data, dict)
            self.assertTrue(data)
        self.assertEqual(len(names), 5)

    def test_examples_have_expected_minimum_contracts(self):
        contracts = {'smart-login-guardian': {'events'}, 'find-the-anomaly': {'training_values', 'test_values'},
                     'api-traffic-watch': {'window_seconds', 'events'}, 'explain-security-alert': {'alerts'},
                     'predict-the-outage': {'training', 'test'}}
        for slug, keys in contracts.items():
            with self.subTest(track=slug):
                text = (ROOT / f'community/hackathon/tracks/{slug}.md').read_text()
                example = json.loads(re.search(r'```json\n(.*?)\n```', text, re.S).group(1))
                self.assertEqual(set(example), keys)

    def test_templates_checklists_and_safety_are_present(self):
        for name in ['templates/PROJECT-README.md', 'templates/SUBMISSION.md', 'REPRODUCIBILITY.md', 'SAFETY.md']:
            self.assertTrue((ROOT / 'community/hackathon' / name).is_file())
        self.assertIn('offline', (ROOT / 'community/hackathon/templates/SUBMISSION.md').read_text())
        self.assertIn('complete reference solutions', (ROOT / 'community/hackathon/README.md').read_text())

    def test_all_local_community_markdown_links_resolve(self):
        files = list((ROOT / 'community/hackathon').rglob('*.md'))
        for path in files:
            text = path.read_text()
            self.assertEqual(text.count('```') % 2, 0, str(path))
            for target in re.findall(r'\]\(([^)]+)\)', text):
                target = target.split('#')[0]
                if not target or ':' in target:
                    continue
                self.assertTrue((path.parent / target).exists(), f'{path.name}: missing link')


class QualificationComplianceTests(unittest.TestCase):
    def test_qualification_is_ordered_and_not_optional(self):
        text = (ROOT / 'community/hackathon/QUALIFICATION.md').read_text()
        sequence = 'REGISTER → FORK AEGLYSAI → CLONE & RUN BASELINE → UNDERSTAND & DOCUMENT → SUBMIT SANITIZED QUALIFICATION EVIDENCE → ORGANIZER REVIEW → SELECTION → BUILD & COMPETE'
        self.assertIn(sequence, text)
        for field in ['registration ID', 'GitHub username', 'fork URL', 'qualification branch', 'qualification document URL', 'sanitized build/run/test evidence']:
            self.assertIn(field, text)
        self.assertIn('Qualification does not guarantee selection', text)
        self.assertIn('Model D knowledge is not required', text)
        self.assertIn('https://github.com/shubh-techie/AeglysAI', text)
        self.assertIn('official Google Form', text)
        for field in ['Architecture', 'Setup', 'One observation', 'One proposed improvement', 'Validation results']:
            self.assertIn(field, (ROOT / 'community/hackathon/templates/QUALIFICATION.md').read_text())

    def test_competition_requires_reproducible_project_and_short_demo(self):
        text = (ROOT / 'community/hackathon/templates/SUBMISSION.md').read_text()
        for field in ['Exactly one approved challenge track', 'Public source-code repository URL', 'Reproducible README', '120 seconds or less', 'AI/ML or intelligent-technique explanation', 'Dataset/model licensing and attribution', 'Optional application demo URL', 'No mandatory webcam footage', 'qualification remains mandatory']:
            self.assertIn(field, text)
        self.assertNotIn('combine tracks', (ROOT / 'community/hackathon/README.md').read_text())

    def test_judging_rounds_each_total_one_hundred_and_have_integrity_rules(self):
        text = (ROOT / 'community/hackathon/JUDGING.md').read_text()
        weights = [int(v) for v in re.findall(r'\| (\d+) \|', text)]
        self.assertEqual(weights, [30, 25, 20, 15, 10, 35, 25, 20, 15, 5])
        self.assertEqual(sum(weights[:5]), 100)
        self.assertEqual(sum(weights[5:]), 100)
        for rule in ['Round 1 shortlists', 'Round 2 ranks', '5–10 finalist teams', 'Round 1 ties', 'Round 2 ties', 'Recuse conflicted judges', 'Do not publish individual judging scores']:
            self.assertIn(rule, text)

    def test_workspace_keeps_administration_private_without_database(self):
        text = (ROOT / 'community/hackathon/WORKSPACE.md').read_text()
        for rule in ['Google Forms', 'Private Google Sheets', 'Private Google Drive', 'GitHub', 'AeglysAI-Portal', 'No application database is required', 'Never publish private participant data, judging scores or confidential patent material']:
            self.assertIn(rule, text)


class ParticipationAmendmentTests(unittest.TestCase):
    def test_every_member_must_qualify_and_team_changes_are_reviewed(self):
        text = (ROOT / 'community/hackathon/TEAMS.md').read_text()
        for rule in ['1–4 participants', 'Individual participation', 'exactly one team lead', 'individually qualified and selected', 'unique team ID', 'approved registration ID', 'no duplicate active team membership', 'cutoff with timezone', 'PENDING CONFIGURATION', 'prior roster', 'documented organizer exception', 'Freeze an approved roster']:
            self.assertIn(rule, text)
        qualification = (ROOT / 'community/hackathon/QUALIFICATION.md').read_text()
        self.assertIn('No team member may bypass qualification', qualification)
        self.assertIn('including the team lead', qualification)
        self.assertIn('architecture understanding, one observation, one proposed improvement', qualification)

    def test_executable_projects_and_separate_publication_consent(self):
        text = (ROOT / 'community/hackathon/templates/SUBMISSION.md').read_text()
        for rule in ['Team ID', 'accessible video-file links', 'no mandatory uploads into GitHub or Google Forms', 'Publication consent is handled separately from judging consent', 'actual executable behavior', 'meaningful intelligent functionality', 'No restrictions on programming language or framework', 'proof of concept', 'No enterprise-scale deployment']:
            self.assertIn(rule, text)

    def test_independent_judging_assistance_and_meet_boundaries(self):
        text = (ROOT / 'community/hackathon/JUDGING.md').read_text()
        for rule in ['Qualification eligibility is separate from competition scoring', 'AI assistance is permitted when disclosed', 'Pre-existing libraries and frameworks are allowed', 'technical clarification', 'Google Meet', 'Recuse conflicted judges', 'Round 1 ties', 'Round 2 ties']:
            self.assertIn(rule, text)
        self.assertIn('No custom application database or authentication service', (ROOT / 'community/hackathon/WORKSPACE.md').read_text())
