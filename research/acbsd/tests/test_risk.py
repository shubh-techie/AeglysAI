import unittest
from research.acbsd.risk import RECOMMENDATIONS, expectation_check, recommend


class RiskTests(unittest.TestCase):
    def test_boundaries_and_expectations(self):
        self.assertEqual(recommend(.24999, 3)['recommendation'], 'MONITOR')
        self.assertEqual(recommend(.25, 3)['recommendation'], 'INVESTIGATE')
        self.assertEqual(recommend(.5, 1)['recommendation'], 'ESCALATE')
        self.assertEqual(recommend(.75, 2)['recommendation'], 'CONTAINMENT_REVIEW')
        self.assertTrue(all(f['aligned'] for f in expectation_check()))

    def test_consistency_and_monotonicity(self):
        for c in (1, 2, 3):
            levels = [RECOMMENDATIONS.index(recommend(e/100, c)['recommendation']) for e in range(101)]
            self.assertEqual(levels, sorted(levels))
            self.assertEqual(recommend(.7, c), recommend(.7, c))
        for e in range(101):
            levels = [RECOMMENDATIONS.index(recommend(e/100, c)['recommendation']) for c in (1, 2, 3)]
            self.assertEqual(levels, sorted(levels))

    def test_invalid_evidence_fails_closed(self):
        for e,c,v in [(float('nan'),1,True), (float('inf'),1,True), (-1,1,True),
                      (1.1,1,True), (.5,0,True), (.5,True,True), (.5,1,False)]:
            with self.assertRaises(ValueError):
                recommend(e,c,v)
