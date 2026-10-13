"""Offline exploratory anomaly benchmark; fit on train, tune on validation only."""
import argparse
from collections import Counter
import importlib.metadata
import json
import platform
from pathlib import Path
import subprocess
import time

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (auc, average_precision_score, confusion_matrix,
                             precision_recall_curve, roc_auc_score)
from sklearn.preprocessing import StandardScaler

from .dataset import FEATURES, PARTITIONS, digest, encode, load_dataset, source_hashes
from .risk import evaluate_recommendations, expectation_check, recommend


def features(events):
    # Never consume labels, identifiers, timestamps, category or asset context.
    return np.asarray([[e[k] for k in FEATURES] for e in events], dtype=float)


def deterministic_scores(x):
    return np.maximum.reduce([np.clip(x[:, 1]/.6, 0, 1), x[:, 2],
                              np.clip(x[:, 3]/.6, 0, 1),
                              np.clip(x[:, 0]/500, 0, 1)*(1-x[:, 4])])


def metrics(y, scores, threshold):
    y, scores = np.asarray(y), np.asarray(scores)
    pred = scores >= threshold
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel().tolist()
    divide = lambda n, d: n/d if d else None
    result = dict(n=len(y), positives=int(y.sum()), confusion_matrix=[[tn, fp], [fn, tp]],
                  precision=divide(tp, tp+fp), recall=divide(tp, tp+fn),
                  f1=divide(2*tp, 2*tp+fp+fn), false_positive_rate=divide(fp, fp+tn),
                  roc_auc=None, pr_auc=None, average_precision=None)
    if len(set(y.tolist())) == 2:
        precision, recall, _ = precision_recall_curve(y, scores)
        result.update(roc_auc=float(roc_auc_score(y, scores)), pr_auc=float(auc(recall, precision)),
                      average_precision=float(average_precision_score(y, scores)))
    return result


def select_threshold(y, scores):
    if set(y.tolist()) != {0, 1}:
        raise ValueError('validation requires both classes')
    candidates = np.unique(np.r_[scores, np.nextafter(max(scores), np.inf)])
    # Highest threshold resolves tied F1 values conservatively; no test labels.
    def objective(threshold):
        flags = scores >= threshold
        tp = int(np.sum(flags & (y == 1)))
        fp = int(np.sum(flags & (y == 0)))
        fn = int(np.sum(~flags & (y == 1)))
        return (2*tp/(2*tp+fp+fn), threshold)
    return float(max(candidates, key=objective))


def cluster_intervals(labels, scores, threshold, repetitions=200, seed=42):
    groups = {}
    for index, t in enumerate(labels):
        groups.setdefault(t['instance_id'], []).append(index)
    keys = list(groups)
    rng = np.random.default_rng(seed)
    samples = {k: [] for k in ('precision', 'recall', 'f1', 'false_positive_rate', 'roc_auc', 'pr_auc')}
    for _ in range(repetitions):
        indices = [i for g in rng.choice(keys, size=len(keys), replace=True) for i in groups[g]]
        m = metrics([labels[i]['anomaly'] for i in indices], scores[indices], threshold)
        for key in samples:
            if m[key] is not None:
                samples[key].append(m[key])
    return {k: {'low': float(np.quantile(v, .025)), 'high': float(np.quantile(v, .975)),
                'eligible_replicates': len(v)} if v else None for k, v in samples.items()}


def run(dataset, output, seed=42, bootstrap=200):
    if Path(output).exists():
        raise FileExistsError('output directory must be new')
    start = time.perf_counter()
    if bootstrap < 1:
        raise ValueError('positive bootstrap replicates required')
    events, truth, manifest = load_dataset(dataset)
    lookup = {t['event_id']: t for t in truth}
    truth = [lookup[e['event_id']] for e in events]
    indices = {p: [i for i, t in enumerate(truth) if t['partition'] == p] for p in PARTITIONS}
    if any(not indices[p] for p in PARTITIONS):
        raise ValueError('all partitions required; generate a larger sample')
    x = features(events)
    y = np.asarray([t['anomaly'] for t in truth], dtype=int)
    if set(y[indices['train']].tolist()) != {0, 1}:
        raise ValueError('training requires both classes')
    scaler = StandardScaler().fit(x[indices['train']])
    transformed = scaler.transform(x)
    rf = RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=2,
                                class_weight='balanced', random_state=seed, n_jobs=1)
    rf.fit(transformed[indices['train']], y[indices['train']])
    isolation = IsolationForest(n_estimators=100, max_samples='auto', contamination='auto',
                                random_state=seed, n_jobs=1)
    # Unsupervised fit on all training observations, without their labels.
    isolation.fit(transformed[indices['train']])
    scorers = {'deterministic': lambda values: deterministic_scores(values),
               'random_forest': lambda values: rf.predict_proba(scaler.transform(values))[:, 1],
               'isolation_forest': lambda values: -isolation.score_samples(scaler.transform(values))}
    result = dict(status='EXPERIMENTAL', data_kind='SYNTHETIC', seed=seed,
                  dataset_manifest_sha256=digest((Path(dataset)/'manifest.json').read_bytes()),
                  dataset_config=manifest['config'], dataset_quality=manifest['quality'],
                  features=list(FEATURES), dependency_versions={name: importlib.metadata.version(name)
                    for name in ('numpy', 'scipy', 'scikit-learn', 'joblib', 'threadpoolctl')},
                  environment={'python': platform.python_version(), 'platform': platform.system(),
                               'architecture': platform.machine(), 'processor': platform.processor()},
                  source_hashes=source_hashes(), models={}, bootstrap=dict(repetitions=bootstrap,
                    seed=seed, unit='scenario instance', interval='percentile 95%; fixed fitted model/threshold'),
                  recommendation_expectations=expectation_check())
    for key, command in [('commit', ['git', 'rev-parse', 'HEAD']),
                         ('dirty', ['git', 'status', '--porcelain'])]:
        value = subprocess.check_output(command, text=True).strip()
        result[key] = bool(value) if key == 'dirty' else value
    raw = []
    for name, score in scorers.items():
        val = indices['validation']
        threshold = select_threshold(y[val], score(x[val]))
        model_result = dict(threshold=threshold, threshold_selection='maximum validation F1; highest threshold on ties',
                            parameters=rf.get_params() if name == 'random_forest' else
                            isolation.get_params() if name == 'isolation_forest' else
                            {'failure_scale': .6, 'novelty_scale': .6, 'count_scale': 500}, partitions={})
        for partition in ('test', 'holdout'):
            ids = indices[partition]
            values = x[ids]
            score(values)  # warm-up excluded
            elapsed = []
            for _ in range(10):
                tick = time.perf_counter_ns()
                scores = score(values)
                elapsed.append((time.perf_counter_ns()-tick)/len(ids)/1000)
            labels = [truth[i] for i in ids]
            summary = metrics(y[ids], scores, threshold)
            summary['ci95'] = cluster_intervals(labels, scores, threshold, bootstrap, seed)
            summary['latency_us_per_event'] = dict(median=float(np.median(elapsed)),
                p95=float(np.quantile(elapsed, .95)), batch_size=len(ids), repeats=10,
                boundary=('warm batch scoring; excludes extraction/I/O/recommendations' if name == 'deterministic' else 'warm batch scoring, includes scaler; excludes extraction/I/O/recommendations'))
            summary['per_scenario'] = {}
            for family in sorted({t['family'] for t in labels}):
                local = [i for i, t in enumerate(labels) if t['family'] == family]
                summary['per_scenario'][family] = metrics(y[np.asarray(ids)[local]], scores[local], threshold)
            recommendations = []
            recommendation_records = []
            for local, index in enumerate(ids):
                # Binary evidence is deliberately transparent, not a calibrated probability.
                evidence = float(scores[local] >= threshold)
                recommendation = recommend(evidence, events[index]['asset_criticality'])
                recommendations.append(recommendation['recommendation'])
                recommendation_records.append(recommendation)
                raw.append(dict(event_id=events[index]['event_id'], model=name, partition=partition,
                                score=float(scores[local]), threshold=threshold, flagged=bool(evidence),
                                recommendation=recommendation))
            summary['recommendation_evaluation'] = evaluate_recommendations(
                [events[i] for i in ids], labels, recommendation_records)
            summary['recommendation_distribution'] = dict(Counter(recommendations))
            model_result['partitions'][partition] = summary
        result['models'][name] = model_result
    result['runtime_seconds'] = time.perf_counter()-start
    path = Path(output)
    path.mkdir(parents=True, exist_ok=False)
    # Exact public-safe implementation snapshot; no Git history, archives or env dump.
    root = Path(__file__).parent
    for name in result['source_hashes']:
        destination = path/'source'/name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((root/name).read_bytes())
    (path/'predictions.jsonl').write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in raw))
    result['predictions_sha256'] = digest((path/'predictions.jsonl').read_bytes())
    (path/'summary.json').write_bytes(encode(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--bootstrap', type=int, default=200)
    args = vars(parser.parse_args())
    try:
        result = run(**args)
    except (Exception, KeyboardInterrupt) as error:
        destination = Path(args['output'])
        # Preserve setup/fit/evaluation failures without touching prior runs.
        if not destination.exists():
            destination.mkdir(parents=True)
            (destination/'failure.json').write_bytes(encode(dict(status='FAILED',
                error_type=type(error).__name__, arguments=args, source_hashes=source_hashes())))
        raise
    print(json.dumps({name: {p: m['f1'] for p, m in model['partitions'].items()}
                      for name, model in result['models'].items()}, sort_keys=True))


if __name__ == '__main__':
    main()
