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


def evaluate_recommendations(events, truth, recommendations):
    """Evaluation-only policy: benign monitor; anomalies escalate/review by asset.

    This is a declared synthetic binary policy, not incident severity ground truth.
    Truth is consumed after inference only. Intermediate INVESTIGATE remains covered
    by the independent graded fixtures.
    """
    if not len(events) == len(truth) == len(recommendations):
        raise ValueError('recommendation row count')
    families = {}
    consistent = aligned = 0
    for event, label, actual in zip(events, truth, recommendations):
        expected = ('MONITOR' if not label['anomaly'] else
                    'ESCALATE' if event['asset_criticality'] == 1 else 'CONTAINMENT_REVIEW')
        repeated = recommend(actual['evidence'], event['asset_criticality'])
        consistent += actual == repeated
        match = actual['recommendation'] == expected
        aligned += match
        family = families.setdefault(label['family'], {'n': 0, 'aligned': 0})
        family['n'] += 1
        family['aligned'] += match
    for values in families.values():
        values['alignment'] = values['aligned']/values['n']
    return {'policy': 'benign MONITOR; anomalous criticality 1 ESCALATE, 2/3 CONTAINMENT_REVIEW',
            'n': len(events), 'aligned': aligned, 'alignment': aligned/len(events) if events else None,
            'repeat_consistency': consistent/len(events) if events else None, 'per_scenario': families}
