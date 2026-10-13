# AEGLYSAI-DATA-001 validation record

Date: 2026-10-13. **EXPERIMENTAL — SYNTHETIC ONLY**. Local Darwin arm64, Python
3.12.9; .NET SDK 8.0.204. HEAD `70dd66c4df3540b0b47d5b229b744131d351b8d0`, dirty
working tree including pre-existing community amendments. No commit/push/PR/publication.

## Actual checks

| Check | Observed result | Runtime boundary |
| --- | --- | --- |
| Research unittest suite | 15 passed | 1.015 s unittest wall time |
| Generate/validate/write 4,000 windows in temporary storage | Passed, 800 instances | 0.170952 s perf_counter wall time |
| Hash/schema/grouping/regeneration verify of that dataset | Passed | 0.158712 s perf_counter wall time |
| Existing .NET Release tests | 168 passed, 0 skipped/failed | Application 22 ms; architecture 1 ms; domain 21 ms; integration 8 s; experiments 15 ms, test-runner durations; full build wall time not captured |
| Security-gate unit tests, Gitleaks 8.30.1 on PATH | 27 passed | 9.909 s unittest wall time |
| Existing community tests in pinned environment | 89 passed | 1.768 s unittest wall time |
| Final three-model benchmark, 200 bootstrap replicates | Executed successfully | 1.206311 s runner wall time excluding final artifact writes |

.NET command: `dotnet test AeglysAI.sln -c Release --no-restore -m:1 --disable-build-servers`.
The first sandboxed attempt failed at MSBuild IPC; the permitted retry passed.
The first dependency download failed under restricted network access; the permitted
installation of pinned packages into a temporary venv succeeded. Initial security
tests failed without the pinned scanner on PATH; initial community tests failed
without jsonschema. Correct environment retries passed. These are setup failures,
not silently discarded behavioral results. No test or scanner policy was bypassed.

Versioned benchmark dependencies: numpy 2.2.6, scipy 1.15.3, scikit-learn 1.6.1,
joblib 1.4.2, threadpoolctl 3.6.0. Source snapshot and all model parameters are in
[the result bundle](../results/acbsd-data001-smoke/README.md). Hosted CI execution
and required-check settings were not verified; only a local CI job definition was added.

## Actual dataset and benchmark

Seed 42, 20 identities, 12 workloads, 86400 seconds, 4000 windows. Training:
2175 rows (555 anomalies); validation: 780 (165); test: 700 (215); scenario-family
holdout: 345 (all anomalous workload communication). Overall 1280/4000 = 32%
anomaly labels. Test has 60 benign operational-surge windows. Expected instance
probabilities and actual family counts are in the stored manifest.

| Model | Threshold | Test precision | Test recall | Test F1 | Test FPR | ROC-AUC | PR-AUC | Surge FPR | Holdout recall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Deterministic | .568 | 1.0000 | .9116 | .9538 | .0000 | .9950 | .9917 | .0000 | .9971 |
| Random Forest | .824932 | 1.0000 | .9721 | .9858 | .0000 | .9993 | .9988 | .0000 | .0000 |
| Isolation Forest | .475391 | .7610 | .8884 | .8197 | .1237 | .8878 | .6006 | 1.0000 | 1.0000 |

Confusion matrices [[TN,FP],[FN,TP]]: deterministic [[485,0],[19,196]], Random
Forest [[485,0],[6,209]], Isolation Forest [[425,60],[24,191]]. Holdout matrices:
[[0,0],[1,344]], [[0,0],[345,0]] and [[0,0],[0,345]] respectively. Holdout FPR,
ROC-AUC and PR-AUC are undefined because no benign examples are present. Random
Forest holdout precision is undefined because it flags no examples.

Grouped percentile 95% F1 intervals with 200 eligible resamples: deterministic
[.9053,.9911], Random Forest [.9672,1.0000], Isolation Forest [.7334,.8986]. These
condition on the fitted model/threshold and synthetic population, not external
validity. All other computed intervals and per-family metrics are in summary.json.

Test median batch-average scoring latency: deterministic .017946 microseconds/event,
Random Forest 3.762321, Isolation Forest 4.912887. These average 700-event vectorized
batches across ten warmed repetitions; they are not single-event latency or full
incident-response overhead. The summary preserves p95 and holdout measurements.

Eight declared recommendation fixtures align (8/8); tests pass for consistency,
threshold boundaries, monotonicity and rejecting invalid/unvalidated evidence.
This validates the reference rules only. Detector mistakes still cause inappropriate
recommendations. No containment, authorization or Kubernetes actions execute.

The first successful run took 1.108620 s. It is retained locally along with its raw
artifacts. The final run fixes timing-boundary wording for the raw deterministic
scorer and adds failure/provenance recording; measured quality values are identical.
No detector/scenario parameter was changed after inspecting held-out results.

## Security, disclosure and documentation

Full tracked-content and locally reachable history gates return failure (exit 1)
on existing unresolved findings; they are publication blockers. An empty staged
scan cannot certify these uncommitted/untracked additions. A separate disposable
snapshot scan of task files uses the unchanged gate and pinned scanner; its final
outcome, documentation checks and handoff review are recorded in [HANDOFF](HANDOFF.md).
No exemptions, fingerprint exceptions or security settings were changed. Human
review remains necessary; synthetic construction does not clear existing history,
license gaps or protected material elsewhere in the repository. Scanner reports
contain paths only and stay in temporary local storage; no matched content is exposed.

The package does not modify AeglysAI-Portal, production .NET source, legacy history,
private mechanisms or real data. See [dataset card](DATASET_CARD.md) and
[methodology](METHODOLOGY.md) for representativeness, leakage and research-question limits.

## DATA-002 follow-up

See the [DATA-002 report](DATA002_REPORT.md) for the audited 50k generation,
chronological boundary protection, exports, actual benchmarks, recommendation
comparison, retained failures and security results. DATA-001's record above is
historical; DATA-002 does not claim real-cloud or Model D production readiness.
