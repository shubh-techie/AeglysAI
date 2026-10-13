"""Transparent evidence-to-recommendation reference; no execution authority."""
import math

RECOMMENDATIONS = ('MONITOR', 'INVESTIGATE', 'ESCALATE', 'CONTAINMENT_REVIEW')
RISK_CATEGORIES = ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')


def recommend(evidence, criticality, validated=True):
    if type(validated) is not bool or not validated:
        raise ValueError('validated evidence required')
    if type(evidence) not in (int, float) or not math.isfinite(evidence) or not 0 <= evidence <= 1:
        raise ValueError('evidence must be finite and normalized')
    if type(criticality) is not int or criticality not in (1, 2, 3):
        raise ValueError('criticality must be 1..3')
    # Asset context increases severity only after substantive anomaly evidence.
    level = 0 if evidence < .25 else 1 if evidence < .5 else 2
    if evidence >= .75 and criticality >= 2:
        level = 3
    elif evidence >= .5 and criticality == 3:
        level = 3
    return {'risk': RISK_CATEGORIES[level], 'recommendation': RECOMMENDATIONS[level],
            'evidence': evidence, 'criticality': criticality, 'reference_version': '1.0.0'}


def expectation_check():
    """Independent reference fixtures; detection metrics are never used as correctness."""
    fixtures = [('normal_auth', .1, 3, 'MONITOR'), ('normal_api', .1, 1, 'MONITOR'),
                ('normal_workload', .1, 2, 'MONITOR'), ('operational_surge', .1, 3, 'MONITOR'),
                ('failed_auth', .4, 1, 'INVESTIGATE'), ('api_frequency', .6, 1, 'ESCALATE'),
                ('privilege_usage', .9, 3, 'CONTAINMENT_REVIEW'),
                ('workload_communication', .6, 2, 'ESCALATE')]
    return [{'family': f, 'expected': expected, 'actual': recommend(e, c)['recommendation'],
             'aligned': recommend(e, c)['recommendation'] == expected} for f, e, c, expected in fixtures]
