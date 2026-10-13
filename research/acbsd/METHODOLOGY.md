# ACBSD exploratory research methodology

Date: 2026-10-13. Protocol version 1.0.0, specified before the task's benchmark run.
The first run is exploratory framework validation, not confirmatory H1–H4 evidence.

## Experimental unit and partitioning

Generate up to five temporally adjacent observation windows per scenario instance.
A shared base rate/failure/peer-novelty value and stable entities create within-group
correlation; per-window bounded jitter adds variation. Instants lie strictly inside
the configured duration from 2026-01-01 UTC. This is a synthetic simulation horizon,
not a claim of historical activity. Each count describes an illustrative 60-second
observation window ending at that instant; overlap is permitted and the summaries
are not aggregated from raw logs. Increasing event volume increases overlapping
windows rather than proving an offered-load model.

The default holdout assigns every workload-communication instance to `holdout`.
Each remaining instance is randomly assigned to train/validation/test with 60/20/20
probabilities using the configured seed. This excludes related rows across partitions.
Validation and test therefore contain known families; holdout measures one unseen
anomaly family. The manifest contains actual sizes, labels and family counts.

Entity and temporal ranges overlap between partitions. Identifiers and timestamps
are excluded from features, but correlated distributions can still inflate results.
Instances are asserted independent by construction, not verified against real data.
There is no claim of future-time or unseen-entity generalization. DATA-001 used random grouping. DATA-002 implements chronological boundaries;
entity-disjoint evaluation and real-window leakage analysis remain planned.
Scenario fields are provenance only; no grouping/label column goes into inference.

## Features and models

The fixed inference allowlist is request count, failure ratio, unexpected privilege
indicator, peer novelty and scheduled-operation marker. Ratios are in [0,1]; count
is a nonnegative integer; privilege and scheduled marker are binary. Asset criticality
is excluded from detectors and used only for recommendation severity.
StandardScaler is fitted once on training observations only. Both tree models use
its transformation; the deterministic model operates on raw observations.

1. Deterministic score is the maximum of failure_ratio/0.6, privilege_delta,
   peer_novelty/0.6 and request_count/500 multiplied by (1-scheduled_operation),
   clipping each ratio to [0,1]. The rule is transparent and generator-aware.
2. Random Forest is supervised: 100 trees, depth 8, minimum leaf size 2,
   balanced class weights, random seed 42, one worker. Other defaults are pinned to
   scikit-learn 1.6.1 and recorded through `get_params()`.
3. Isolation Forest fits all training observations without labels: 100 trees,
   automatic sample count (up to 256), automatic contamination, seed 42, one worker.
   Negated `score_samples` makes larger values more anomalous. Its operational
   threshold is selected separately; it is not a calibrated malicious probability.

All three thresholds maximize validation F1; ties use the highest threshold.
No test or holdout label selects thresholds or preprocessing. Isolation Forest
fitting is unsupervised; its threshold calibration is label-assisted. No hyperparameter
search is claimed. Versioned library references:
[Random Forest](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.RandomForestClassifier.html),
[Isolation Forest](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.IsolationForest.html),
[precision-recall curve](https://scikit-learn.org/1.6/modules/generated/sklearn.metrics.precision_recall_curve.html).
These API sources were checked for the pinned version; no literature novelty review
or citation-based research conclusion is claimed.

## Metrics and uncertainty

Report held-out precision TP/(TP+FP), recall TP/(TP+FN), F1 2TP/(2TP+FP+FN),
confusion matrix [[TN,FP],[FN,TP]], false-positive rate FP/(FP+TN), ROC-AUC and
trapezoidal PR-AUC from ranked continuous scores. Average precision is separately
reported to avoid conflating the two PR summaries. Undefined denominators yield
JSON null; ROC/PR metrics require both classes. Per-family labels are constant,
so their ranking AUCs are undefined. Per-scenario precision/recall/FPR use the same
fixed threshold. Operational-surge FPR and counts explicitly measure hard negatives.

Default confidence intervals resample whole scenario instances 200 times with
replacement, seed 42, and take 2.5/97.5 percentiles, retaining all correlated windows
in selected groups. Undefined replicates are omitted with eligible counts reported.
Intervals condition on the fitted model and threshold: they do not include training,
seed, simulator or deployment uncertainty. Single-class holdout cannot estimate FPR
or AUC. Scores within a family may overlap and the supervised model can miss unseen
families; unfavorable observations must remain in the results.

Latency is measured after one batch warm-up, ten serial repetitions, using
perf_counter_ns. Median/p95 are percentiles of ten batch-average microseconds/event,
including scaler and scorer but excluding feature extraction, I/O, recommendation,
network and authorization. These are not single-request tail latencies. Run the
benchmark with no concurrent test/build loads. Record actual dependencies, platform,
architecture, Python, Git commit/dirty state, source hashes/snapshot, dataset manifest
hash and runtime. Event bytes are deterministic under the documented Python version;
timings and cross-version floating-point/model behavior need not be.

## Recommendation evaluation and paper scope

The reference maps normalized validated evidence and asset criticality to LOW,
MODERATE, HIGH or CRITICAL and MONITOR, INVESTIGATE, ESCALATE or CONTAINMENT_REVIEW.
Below .25 monitor; [.25,.5) investigate; at least .5 escalate; at least .75 with
criticality 2/3, or at least .5 with criticality 3, require containment review.
Invalid/unvalidated evidence raises an error. Criticality alone never triggers an
incident. The benchmark uses a binary detector flag as evidence 0/1, explicitly
uncalibrated. This yields monitor/escalate/review; intermediate investigate is tested
with reference fixtures. No model score is presented as a trusted live incident.

Eight independent synthetic expectation fixtures, boundary checks, repeatability and
monotonicity across evidence/criticality validate recommendation logic separately
from detector performance. Expected recommendations are declared reference examples,
not evidence that synthetic anomalies have been detected or operations are safe.
No containment execution, Kubernetes modification, adaptive authorization, response
or rollback is implemented.

The dataset supports the paper's exploratory detection/false-alarm comparison and
transparent recommendation study. For existing RQ1 it supplies labeled behavioral
software evaluation, not an A–D authorization comparison or evidence ablation. RQ4
gets only narrow scoring latency and false-positive costs. RQ2 policy safety and RQ3
resilience require separate future, approved protocols and remain unanswered. The
paper's full incident-response and operational effectiveness claims are unsupported.

## DATA-002 protocol extension (exploratory)

The [completed report](DATA002_REPORT.md) specifies the actual 50k run. Optional
chronological mode assigns instance positions to 60/20/20, removes the holdout
family and inserts two 60-second gaps within the configured duration. Duration must
exceed 120 seconds. Validators enforce more than 60 seconds between train/validation
and validation/test endpoints, preventing overlap of their illustrative trailing
windows. The holdout spans the horizon but is excluded from all fitting/calibration.
Independent instances may reuse entities; raw continuous sessions are not modeled.

Repeated feature values at distinct timestamps are permitted and counted in quality
report 1.1.0; duplicate identifiers and non-increasing timestamps remain rejected.
No artificial jitter was added to force feature uniqueness. Random-mode output and
the existing sample remain backwards-compatible. This correction was prompted by
the failed 50k generation, before the first successful 50k benchmark.

Recommendation evaluation compares actual outputs with a declared evaluation-only
binary policy: benign monitor; anomalies escalate for criticality 1, review for 2/3.
Labels are consumed after inference. This measures detection plus policy alignment,
not independent expert severity, intervention outcomes or response safety. Repeat
consistency and per-family alignment are reported separately from graded fixtures.
Model inference and all hyperparameters are unchanged from DATA-001. Final window
gaps were added after the preliminary exploratory benchmark; both runs are retained,
and identical detection metrics result because features/partition membership are
unchanged. This is not a preregistered confirmatory experiment.
