# AeglysAI Cloud-Native Behavioral Security Dataset (ACBSD)

**IMPLEMENTED** offline generator, validation, grouped partitions and recommendation
reference. **EXPERIMENTAL** synthetic anomaly benchmark. Model D production
integration, authorization, adaptive response and rollback remain **PLANNED**.
No external logs, credentials, production traffic or private research are used.

Run all commands from the repository root. Python 3.12.9 was used locally;
generation and verification need only the standard library. The benchmark uses
[pinned requirements](requirements.txt); initial installation needs package access.
Use a virtual environment outside the repository:

```sh
python3 -m venv /tmp/acbsd-venv
/tmp/acbsd-venv/bin/pip install -r research/acbsd/requirements.txt
/tmp/acbsd-venv/bin/python -m unittest discover -s research/acbsd/tests -v
python3 -m research.acbsd.dataset --seed 42 --identities 20 --workloads 12 \
  --duration 86400 --volume 4000 --output research/results/local-acbsd-dataset
python3 -m research.acbsd.verify research/results/local-acbsd-dataset
/tmp/acbsd-venv/bin/python -m research.acbsd.benchmark \
  --dataset research/results/local-acbsd-dataset \
  --output research/results/local-acbsd-benchmark --seed 42 --bootstrap 200
```

Output directories must be new. Choose a fresh suffix for each run; existing
artifacts are never overwritten. CLI setup/fit/evaluation failures leave a
`failure.json` containing the error type and configuration in a fresh output directory. `local-*` results are already ignored by the
repository. Retain failed/unfavorable runs locally and record failures in the
[validation record](VALIDATION.md); do not silently delete experiments.
Use `--scenarios` for a version-1 catalogue with explicit probabilities summing to
one. `--holdout` selects a family excluded entirely from fitting and calibration;
it defaults to `workload_communication`. Small random samples can omit families or
classes; the benchmark rejects missing partitions or single-class train/validation.

The small [example](examples/smoke-v1/manifest.json) is a contract demonstration,
not an evaluation dataset. Reproduce its event and truth files with seed 42,
20 identities, 12 workloads, 86400 seconds and volume 200 in a fresh directory.
Manifest source hashes reflect the generating source snapshot, so later source
changes can change the manifest while event bytes remain identical.

Artifacts:

- `events.jsonl`: strictly ordered synthetic observation windows; no labels.
- `ground_truth.jsonl`: independent scenario assignment, labels and partition joined
  by event ID; never input to inference. A related instance stays in one partition.
- `manifest.json`: full catalogue/configuration, SHA-256, source hashes, quality and
  imbalance reports. `verify` checks hashes and deterministic event regeneration.
- Benchmark `summary.json`: versions, environment, source commit/dirty flag,
  hyperparameters, thresholds, metrics, grouped confidence intervals and runtime.
- Benchmark `predictions.jsonl`: actual held-out scores, decisions and recommendations.
- Benchmark `source/`: exact public-safe Python/config/test snapshot for replay.
  Run the source as `research/acbsd/` in a fresh reproduction checkout with the
  pinned dependencies; documentation and Git history are not copied.

See [SPEC-019](../../docs/aeglysai/specs/SPEC-019-SYNTHETIC-BEHAVIORAL-DATASET.md),
[ADR-013](../../docs/aeglysai/adr/ADR-013-SYNTHETIC-BEHAVIORAL-RESEARCH.md),
[dataset card](DATASET_CARD.md), [methodology](METHODOLOGY.md),
[roadmap](ROADMAP.md), [traceability](TRACEABILITY.md) and
[actual validation](VALIDATION.md). All existing disclosure gates still apply;
public-safe synthetic inputs do not clear the repository's historical findings.
