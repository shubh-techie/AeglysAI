# ACBSD 1.0.0 dataset card

Date: 2026-10-13. **SYNTHETIC / EXPERIMENTAL**. Maintainer: AeglysAI repository owner.
No root license is present; this task grants no additional data or software license.
Public-safe construction does not itself authorize publication or redistribution.

## Purpose and provenance

Support reproducible exploration for “An AI-Based Framework for Behavioral Anomaly
Detection and Incident Response in Cloud-Native Infrastructure” and the public-safe
behavioral evaluation portion of Model D. Each row is a wholly simulated observation
window associated with fictional `identity-NNNN` and `workload-NNNN` entities.
The source is a versioned hand-authored catalogue and Python's seeded PRNG, without
external datasets or learned production distributions. Ground truth is assigned
from the selected family before detection, never inferred from model output.
Anomaly means synthetic behavioral deviation, not proven malicious intent.

Only documentation-network `192.0.2.0/24` addresses are emitted. Addresses are
illustrative aliases and can repeat when identities exceed 254. No people,
organizations, tokens, credentials, free text, payloads, real hostnames or logs exist.
Identity/workload relationships are stable within an instance; the same entities
can participate in other independent instances, including other partitions.

## Composition and quality

The catalogue has three ordinary benign families, four anomaly families and a
benign operational surge. Expected instance anomaly prevalence is 32%, but the
realized event distribution is sampled and reported in each manifest. Probabilities
apply to instances, each producing up to five correlated windows. No prevalence
matches a measured operational environment. All values are required and finite;
missing values and extra fields are rejected rather than silently imputed.

Quality checks cover row counts, schema, identifiers, timestamps, categories,
relationships, documentation addresses, repeated feature-payload diagnostics, labels,
scenario-group leakage, holdout-family exclusion and file integrity. Hashes detect
accidental changes; they are not signatures or a trust boundary against a malicious
party modifying both data and manifest. Verification also regenerates the data.

## Limits and use boundaries

Suitable for software validation, exploratory feature/threshold experiments,
hard-negative comparison and failure analysis. Unsuitable for production deployment,
claims of real attack detection, novelty, calibrated incident risk or patent claims.
The scheduled-operation marker is an idealized trusted context signal; perfect
availability is a strong simplification. Privilege and peer-novelty features are
simulated summaries, without live RBAC or topology derivation. Workloads do not
execute containers or communicate. Counts and failure ratios are sampled summaries,
not reconstructed from raw request logs; arbitrary window placement can overlap.

Temporal bursts are correlated but traffic arrival times, changing roles, service
lifecycles, mixed incidents, drift, outages and adversarial evasion are not modeled.
Default random grouped splitting shares entities and chronological ranges.
DATA-002 chronological mode separates evaluation window boundaries by more than
60 seconds but still shares entities across independent instances. Family holdout
is only one narrow generalization test and contains anomalies only by default.
Feature ranges partially encode the generator's definition of abnormality; high
scores can reflect an easy simulation. Multi-seed and more realistic evaluations
remain planned. The completed [DATA-002 run](DATA002_REPORT.md) contains 50,000
windows, with 32.74% anomaly labels; this is not measured production prevalence.
Native Kubernetes audit fields, raw window aggregation and analyst feedback are absent. Recommendations are offline outputs, never containment actions.
