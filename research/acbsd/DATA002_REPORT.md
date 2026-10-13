# AEGLYSAI-DATA-002 research readiness report

Date: 2026-10-13. **IMPLEMENTED** generation/validation/export software;
**EXPERIMENTAL** completed synthetic experiments. Real-world effectiveness remains
**NOT VERIFIED**. No expected performance values are presented as observed results.
Branch: `research/AEGLYSAI-DATA-002-dataset-validation`. Uncommitted work based on
DATA-001 `a497b232ea09d0f237d468460fb98791695182f6`.

## 1. DATA-001 audit

Remote read-only Git query confirmed DATA-001 branch at the above commit and main at
`711c1556e27bd226c08fb6a8c7b0d9040b4c88ee`. Local main remains
`bcd4f47554445e37a47a0c9945602701fc7ebd43`; origin/main matches the live query.
DATA-001 is not in main's ancestry. Its commit changes 61 files, including unrelated
community amendments: that commit's contents must not be attributed solely to the
dataset package. Review with `git show --stat a497b23` and
`git diff a497b23^ a497b23 -- research/acbsd research/results/acbsd-data001-smoke`.
GitHub's public pulls API returned an empty list for the exact DATA-001 head branch;
no matching PR was verified. No hosted CI run was verified.

| Component | Audit status and evidence |
| --- | --- |
| Generator | IMPLEMENTED: `dataset.py`; fresh smoke and 50k execution confirmed |
| Catalogue | IMPLEMENTED: `scenarios/v1.json`, eight families, explicit probabilities |
| Event/truth schema | IMPLEMENTED: strict key/type/entity checks in `dataset.py`; separate JSONL files; standalone JSON Schema MISSING |
| Actual sample | IMPLEMENTED: tracked 200-row `examples/smoke-v1`, verified again; stored DATA-001 4k manifest/summary exist; large DATA-001 event files are not tracked |
| Validation/regeneration | IMPLEMENTED: `validate`, `load_dataset`, `verify`; rejects tampering and reproduces observations |
| Train/validation/test | IMPLEMENTED random instance grouping; chronological boundary protection was MISSING and added here |
| Family holdout | IMPLEMENTED: all workload-communication instances excluded from train/validation/test |
| Baselines/preprocessing | IMPLEMENTED: three scorers, training-only scaler, validation-only thresholds; executed here |
| Recommendation rules | IMPLEMENTED: non-enforcing reference and eight fixtures; full-dataset expectation comparison added here |
| Documentation/tests | IMPLEMENTED: ADR-013, SPEC-019, card/methodology/roadmap/log and initial 15 tests; now 19 tests pass |
| Kubernetes raw audit, raw session streams, entity-disjoint evaluation | MISSING; workload summaries do not implement these |
| Real-cloud/Model D production performance | NOT VERIFIED; no Model D integration or private mechanisms |

## 2. Exact reproducibility commands

```sh
# Existing pinned environment used for this run; create a new one if unavailable:
python3 -m venv /tmp/aeglysai-data001-venv
/tmp/aeglysai-data001-venv/bin/pip install -r research/acbsd/requirements.txt
/tmp/aeglysai-data001-venv/bin/python -m unittest discover -s research/acbsd/tests -v
python3 -m research.acbsd.dataset --seed 42 --volume 1000 --split chronological \
  --output research/results/local-acbsd-data002-smoke-window-safe
python3 -m research.acbsd.verify research/results/local-acbsd-data002-smoke-window-safe
python3 -m research.acbsd.dataset --seed 42 --identities 100 --workloads 40 \
  --duration 604800 --volume 50000 --split chronological \
  --output research/results/local-acbsd-data002-50k-final
python3 -m research.acbsd.verify research/results/local-acbsd-data002-50k-final
python3 -m research.acbsd.splits --dataset research/results/local-acbsd-data002-50k-final \
  --output research/results/local-acbsd-data002-splits-final
/tmp/aeglysai-data001-venv/bin/python -m research.acbsd.benchmark \
  --dataset research/results/local-acbsd-data002-50k-final \
  --output research/results/local-acbsd-data002-benchmark-window-safe --seed 42 --bootstrap 200
```

Run from repository root. Outputs must be new; use fresh suffixes on replay.
The existing pinned venv was reused without reinstalling packages. Python 3.12.9,
Darwin arm64, .NET SDK 8.0.204; model dependency versions and exact hyperparameters
are in the [actual summary](../results/acbsd-data002-evidence/summary.json).
Dataset schema/catalogue version 1.0.0, chronological quality report version 1.1.0;
model/recommendation implementations identified by captured source SHA-256, library
versions, parameters and seed (recommendation reference 1.0.0). Git HEAD alone does
not reproduce dirty source: use the captured local benchmark `source/` snapshot.

## 3. Generated paths, sizes and checksums

All final artifact sizes/hashes, including smoke, exported splits, predictions and
source snapshot, are in the [artifact manifest](../results/acbsd-data002-evidence/artifact-manifest.json).
Large JSONL files remain ignored and local. Small sanitized DATA-001 sample is reused.

| Final dataset file | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/results/local-acbsd-data002-50k-final/events.jsonl` | 18944515 | `17da05ed93310eab112c46adf01b13ecacf5d23f129464b06e9341230e44054d` |
| `research/results/local-acbsd-data002-50k-final/ground_truth.jsonl` | 6702225 | `3392d6f3444c2cd72c2e86e4c51cd7e77c876f2585add133e36cdc1ba341df12` |
| `research/results/local-acbsd-data002-50k-final/manifest.json` | 5929 | `419ebee7c38e28f50b1157a62dba7d8b0979a6abae2541815ce282deb6599e38` |

## 4. Counts, labels and scenarios

Seed **42**, 50,000 observation windows, 10,000 five-window scenario instances,
100 configured identities and 40 workloads over seven simulated days starting
2026-01-01 UTC. This simulated date is not project activity. Observed benign:
33,630 (67.26%); anomaly: 16,370 (32.74%). The 32% catalogue anomaly probability is
an illustrative imbalanced experiment, not measured production prevalence.
12 repeated feature payloads at distinct timestamps are legitimate observations;
no event or ground-truth identifiers repeat. This diagnostic is separate from
leakage: related rows stay in one instance and one partition.

| Family | Observed rows |
| --- | ---: |
| api_frequency | 4170 |
| failed_auth | 3955 |
| normal_api | 9760 |
| normal_auth | 9835 |
| normal_workload | 10075 |
| operational_surge | 3960 |
| privilege_usage | 4185 |
| workload_communication | 4060 |

## 5. Research partitions and leakage controls

| Partition | Benign | Anomaly | Total |
| --- | ---: | ---: | ---: |
| holdout | 0 | 4060 | 4060 |
| test | 6655 | 2585 | 9240 |
| train | 20265 | 7300 | 27565 |
| validation | 6710 | 2425 | 9135 |

Chronological split uses the first 60%, next 20%, final 20% of instance positions,
with holdout family removed from these partitions. Two inserted 60-second gaps
produce strictly more than 60 seconds between train/validation and validation/test
observation endpoints. Thus their illustrative trailing windows cannot overlap.
No scenario instance or its related identity/workload burst crosses partitions.
Entity IDs can recur across independent instances; this is not entity-disjoint.
Holdout spans the full simulation horizon but is never used for fitting/calibration.
There is no rolling feature state or cross-instance session history to leak.
Raw Kubernetes/user sessions and their linkage are unavailable, so no broader
real-session leakage guarantee is possible. Separate split JSONL files retain
original bytes and joins; exports do not alter benchmark partition assignments.

Features are only request count, failure ratio, privilege delta, peer novelty and
scheduled-operation context. Truth, family, IDs, timestamps, partition and resource
criticality are excluded from detector input. StandardScaler is fitted on training
only. Isolation Forest fitting is unsupervised but its threshold is label-assisted
on validation. Tests invert held-out labels and confirm thresholds/scores unchanged.
Scheduled operation is an idealized perfect marker; it separates high-volume benign
surges by construction. This is a simulation shortcut to disclose, not ground-truth
columns being accidentally passed to inference. Neither simulator ranges nor this
context guarantee operational realism.

## 6. Actual benchmark results

All values below are observed on the final dataset; no threshold uses test labels.
No hyperparameters or family ranges were changed in response to held-out metrics.
The deterministic threshold is validation-calibrated, despite the fixed score rule.

| Model | Threshold | Precision | Recall | F1 | ROC-AUC | PR-AUC | FPR | Median scoring µs/event | Holdout recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| deterministic | 0.360000 | 0.990948 | 0.974081 | 0.982442 | 0.997924 | 0.996226 | 0.003456 | 0.008581 | 1.000000 |
| isolation_forest | 0.455061 | 0.744750 | 0.974081 | 0.844117 | 0.890343 | 0.577916 | 0.129677 | 2.330010 | 1.000000 |
| random_forest | 0.532333 | 0.998446 | 0.994197 | 0.996317 | 0.999387 | 0.999068 | 0.000601 | 1.665803 | 0.344335 |

Benchmark runner runtime: 6.385822 seconds, excluding final artifact writes.
Latency uses ten warmed vectorized batch repetitions (9,240 test rows), excludes
feature extraction/I/O/recommendations and includes scaling for sklearn models.
It is not request tail latency or incident-response runtime. No concurrent builds
or tests ran during the final benchmark. Full p95, confusion matrices, average
precision and instance-bootstrap 95% intervals (200 replicates) are in the summary.
Holdout is anomaly-only: ROC/PR-AUC and FPR are undefined. Bootstrap intervals
condition on the fitted model, threshold and one simulator/seed.

| Test family | n | Deterministic recall / FPR | Random Forest recall / FPR | Isolation Forest recall / FPR |
| --- | ---: | --- | --- | --- |
| api_frequency | 890 | 0.924719 / undefined | 0.983146 / undefined | 0.924719 / undefined |
| failed_auth | 810 | 1.000000 / undefined | 1.000000 / undefined | 1.000000 / undefined |
| normal_api | 1960 | undefined / 0.000000 | undefined / 0.001531 | undefined / 0.006633 |
| normal_auth | 1840 | undefined / 0.000000 | undefined / 0.000000 | undefined / 0.013043 |
| normal_workload | 2050 | undefined / 0.000000 | undefined / 0.000488 | undefined / 0.010244 |
| operational_surge | 805 | undefined / 0.028571 | undefined / 0.000000 | undefined / 1.000000 |
| privilege_usage | 885 | 1.000000 / undefined | 1.000000 / undefined | 1.000000 / undefined |

Per-family precision and F1 (and undefined single-class AUCs) are also retained in
the summary. Random Forest's strong test results do not establish unseen-family
coverage: its holdout recall is only 34.43%. Isolation Forest flags every benign
surge test observation (FPR 1.0); retain this unfavorable result in the paper.

## 7. Recommendation evaluation

Before the final experiment, declared an evaluation-only binary reference policy:
benign → MONITOR; anomaly with criticality 1 → ESCALATE; anomaly with criticality
2/3 → CONTAINMENT_REVIEW. This is a transparent synthetic policy assumption, not
independent expert incident-severity annotation. Ground-truth anomaly/family is
consumed only after recommendations have been produced; severity is not model input.

| Model | Test expectation alignment | Holdout alignment | Repeat consistency |
| --- | ---: | ---: | ---: |
| deterministic | 0.990260 | 1.000000 | 1.000000 |
| isolation_forest | 0.899351 | 1.000000 | 1.000000 |
| random_forest | 0.997944 | 0.344335 | 1.000000 |

All eight existing graded fixtures align; those fixtures cover INVESTIGATE, which
binary model evidence 0/1 never emits. Dataset alignment therefore largely measures
detection correctness under the declared policy; it is not an independent response
quality result. Per-scenario alignment/distributions are retained. Consistency means
repeating the same evidence/context yields the same output, not cross-model agreement.
No enforcing action, containment, API call or Kubernetes operation occurs.

## 8. Limitations and Model D compatibility

| Model D input | Readiness / gap |
| --- | --- |
| Identity/workload correlation | IMPLEMENTED synthetic ID/peer relations within an instance; no authenticated identity binding, long-lived session or live topology |
| Contextual anomaly indicators | IMPLEMENTED simulated summary features; trusted context availability idealized |
| Recency/provenance | IMPLEMENTED UTC timestamp, synthetic kind, catalogue/source/dataset hashes; no observed ingestion time, freshness guarantee or cloud collector provenance |
| Resource criticality | IMPLEMENTED random 1–3 asset context; no real inventory or expert severity annotation |
| Behavioral windows | EXPERIMENTAL illustrative 60-second summaries and five-row bursts; raw event aggregation, lifecycle/change/drift and cross-session history MISSING |
| Risk inputs | IMPLEMENTED offline flag + criticality reference; calibrated risk, adaptive authorization and production integration MISSING |
| Feedback/evaluation | IMPLEMENTED truth join and held-out predictions; analyst feedback, adjudication and outcome history MISSING |

No unpublished Model D mechanism is implemented. API/authentication/workload
summaries are present; native Kubernetes verb/resource/namespace/service audit events
and actual services are MISSING. Data is fully synthetic, with no real attack or
production distribution. Entity-disjoint, multi-seed, rare-prevalence, imperfect
context and richer mixed-incident evaluations remain PLANNED. One family holdout
is insufficient for operational readiness. Paper licensing/disclosure review and
independent protocol/literature review are still required.

## 9. Required paper updates

Describe a completed synthetic exploratory experiment, the fixed catalogue and
realized counts, chronological instance grouping and 60-second boundary gaps.
Report validation-only thresholds, unsupervised fitting versus label-assisted
calibration, five allowed features, train-only preprocessing, per-family failures,
grouped conditional intervals and precise batch timing boundary. Include simulator
shortcuts and shared entities. Separate declared recommendation-policy alignment
from response effectiveness and from the eight reference-rule fixtures. No real
security incidents, containment efficacy, production benchmarks, A–D comparison,
patent mechanism validation or causal improvements have been demonstrated. Real-world
performance and expected improvements remain unverified/planned. No new literature
citation or research novelty claim was added by this task.

## 10. ADR/SPEC/log changes

Extended existing ADR-013 and SPEC-019 rather than creating duplicates. Updated
card, methodology, roadmap, reproducibility README, validation index and development
log to reference this report and its small evidence bundle. The original DATA-001
validation record is retained as historical evidence.

## 11. Validation and security

Research tests: **19 passed** (3.075 s); includes 50k generation, chronological
boundary mutation, training-only fitting, held-out label independence, recommendations
and lossless split exports. Final smoke, final 50k and the tracked DATA-001 example
validate and regenerate. Existing .NET Release suite: **168 passed**, zero failed or
skipped. Security gate tests with Gitleaks 8.30.1: **27 passed** (9.870 s).

Tracked and locally reachable history gates: **FAIL (exit 1)** on existing findings.
Current tracked findings remain visible at `docs/aegisai/research/INVENTION_CANDIDATES.md`
and existing AEGISAI-009/010 environment artifacts. Historical credential/disclosure
findings also remain. No policy, exception or historical content was changed.
Publication is blocked despite passing software tests. Task-only security snapshot: **PASS (exit 0)** using unchanged staged secrets and
disclosure checks on exact changed/new file contents in a disposable Git repository;
the real repository index was untouched. Markdown local-target/fence validation:
**PASS**; remote URLs and anchors were not checked. `git diff --check`: **PASS**.
Independent fresh temporary regeneration also produced byte-identical final event
and truth JSONL, in addition to `verify`'s object-level regeneration check.

Privacy validation allows only synthetic numbered entities and documentation-network
IPs, fixed categories and numeric/bool features; no free text, payloads, credentials,
real identities or enterprise logs. Source and generated-data inspection found no
real-data source. Scanner limits and human disclosure review still apply. Large
local files are excluded from proposed publication. AeglysAI-Portal, legacy tag,
historical commits and production source were not modified.

Failures retained: initial 50k rejected repeated feature values before writing;
its subsequent benchmark failed because no dataset existed and recorded failure.json.
A retry refused to overwrite that failed benchmark. Earlier successful artifacts are
retained locally; the final protocol adds window-boundary protection without changing
features or model settings, so detection metrics remain identical. Initial .NET run
could not bind its local test socket; approved retry passed. Restricted-network Git
query failed, then approved read-only query passed. Python GitHub API TLS verification
failed; system curl verified TLS and returned no matching public PR.

## 12. Proposed commit and PR (not executed)

Commit: `test(research): AEGLYSAI-DATA-002 validate synthetic security datasets`

PR: `AEGLYSAI-DATA-002: Reproducible Dataset Validation and ML Benchmarks`

Proposed description: DATA-001's generator rejected valid repeated feature payloads
at research volume and lacked chronological window separation. This change reports
feature repetitions, adds chronological grouped partitions with boundary gaps and
lossless exports, and measures offline recommendation alignment. Reproduces a
50,000-window synthetic experiment with three baselines, retaining unseen-family
and benign-surge failures. Attach tests and manifests; disclose failing historical
security gates. DATA-001 is absent from main, so a PR targeting main would include
its ancestor changes: choose/review the base explicitly before opening a PR.

No commit, push, PR, merge or publication has occurred. Review authorization is
required before any such action.
