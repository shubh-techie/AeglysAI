# SPEC-019 — ACBSD synthetic behavioral dataset and benchmark

Date: 2026-10-13. Version 1.0.0. Task AEGLYSAI-DATA-001.
Status: IMPLEMENTED offline tools; EXPERIMENTAL synthetic evaluation.

## Architecture

`research/acbsd/dataset.py` owns generation, schema/data quality and JSONL manifests;
`verify.py` checks integrity and regeneration; `scenarios/v1.json` owns scenario
parameters. `benchmark.py` consumes verified artifacts, extracts allowlisted features,
fits training-only transformations/models and chooses validation thresholds. `risk.py`
accepts validated evidence and synthetic criticality independently of ground truth.
All code stays outside the .NET production dependency graph. A–C contracts and
results retain their meaning; no production authorization or response changes occur.

## Event contract

Every field is required; null, nonfinite values, unknown fields and unsupported
versions are rejected. JSONL rows use these fields:

| Field | Type and meaning | Detector input |
| --- | --- | --- |
| event_id | Unique `evt-` plus 9 digits, local to dataset | No |
| timestamp | Strictly increasing microsecond UTC ISO-8601 time | No |
| identity_id | Fictional `identity-NNNN`, bounded by configured entity count | No |
| workload_id | Fictional `workload-NNNN`, configured entity reference | No |
| peer_workload_id | Different configured fictional workload | No |
| source_ip | Identity-derived documentation address in 192.0.2.0/24 | No |
| category | authentication, api or workload | No |
| request_count | Nonnegative integer summary of illustrative 60-second window | Yes |
| failure_ratio | Finite [0,1] failed-operation proportion | Yes |
| privilege_delta | Integer 0/1 unexpected privilege indicator | Yes |
| peer_novelty | Finite [0,1] simulated unfamiliar-peer score | Yes |
| scheduled_operation | Boolean synthetic trusted operational context | Yes |
| asset_criticality | Integer 1/2/3 synthetic context for recommendations | No |

A ground-truth row contains exactly event_id, instance_id (`instance-` plus 8 digits),
family, anomaly (Boolean), and partition (train/validation/test/holdout). Version,
synthetic designation, all generator settings, canonical scenario SHA-256, actual
quality distributions, source hashes and artifact hashes live in the manifest.
IDs are scoped to each dataset; merge datasets only with explicit dataset provenance.
Feature schemas never admit ground-truth columns. Labels follow scenario assignment
independently of detector decisions. Missing-value handling is rejection, not imputation.

## Scenario catalogue

Probabilities are instance probabilities; normal-window jitter can overlap anomaly
ranges. Privilege is fixed binary; other continuous base ranges get bounded jitter.
Full exact parameters and scheduling flags are in
[scenarios/v1.json](../../../research/acbsd/scenarios/v1.json).

| Family | Probability | Label | Base rate range | Main behavior |
| --- | --- | --- | --- | --- |
| normal_auth | .20 | benign | 1–15 | Ordinary identity authentication, failure 0–.1 |
| normal_api | .20 | benign | 10–100 | Ordinary API observations |
| normal_workload | .20 | benign | 10–100 | Ordinary workload communication, novelty 0–.15 |
| failed_auth | .08 | anomaly | 10–90 | Correlated failed authentication, failure .35–1 |
| api_frequency | .08 | anomaly | 80–900 | Unscheduled elevated API volume |
| privilege_usage | .08 | anomaly | 10–100 | Unexpected privilege indicator 1 |
| workload_communication | .08 | anomaly | 10–100 | Peer novelty .35–1; default family holdout |
| operational_surge | .08 | benign hard negative | 80–900 | Scheduled legitimate operational volume |

Each instance has up to five ordered correlated windows with shared entities and
base signals. Rate jitter is .8–1.2; failure/novelty jitter is ±.05 clipped to [0,1].
Anomalies are deviations by simulation design, not externally validated attacks.

## Acceptance and evaluation

Require deterministic event/provenance regeneration; unique IDs; valid ordered
timestamps; stable group entities; strict vocabulary and missingness; exact duplicate
payload detection; independent truth; hashes and distribution reporting. Preserve
instance groups in one split and holdout family outside all fitting/calibration.
Record actual versions, hyperparameters, metrics, undefined denominators, latency
boundary, bootstrap limits, source/environment and failed runs. Recommendations
must be consistent/monotonic and match declared synthetic reference fixtures.

Reproduction, interpretation and acceptance evidence:
[README](../../../research/acbsd/README.md),
[dataset card](../../../research/acbsd/DATASET_CARD.md),
[methodology](../../../research/acbsd/METHODOLOGY.md),
[traceability](../../../research/acbsd/TRACEABILITY.md),
[validation](../../../research/acbsd/VALIDATION.md).
Existing [SPEC-013](../../aegisai/specs/SPEC-013-DISCLOSURE-PROTECTION.md) remains
binding. No new confidential authorization, orchestration or rollback is specified.
