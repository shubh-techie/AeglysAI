# AEGLYSAI-DATA-001 exploratory smoke results

**EXPERIMENTAL / SYNTHETIC**. Run date 2026-10-13. This is a single-seed
software/framework evaluation, not production performance or H1–H4 validation.

[summary.json](summary.json) preserves measured metrics, uncertainty, dependencies,
model parameters, feature allowlist, thresholds and timing/environment boundaries.
[dataset-manifest.json](dataset-manifest.json) preserves the exact versioned
configuration, label/split distributions, event/truth hashes and generating source
hashes. [source](source) captures the exact public-safe implementation and tests.

Full 4,000-row inputs and 3,135 held-out prediction rows remain locally in ignored
`research/results/local-acbsd-data001-final-dataset/` and
`research/results/local-acbsd-data001-final-benchmark/`. The summary records their
hashes. They are deliberately not included in this small reviewable result bundle.
Earlier task runs remain in their original ignored directories. The final run changes
only metadata/failure recording from the first successful run; detector hyperparameters,
threshold protocol and generator ranges were not tuned using viewed test results.

Reproduce from the repository root using the [ACBSD commands](../../acbsd/README.md)
with seed 42, 20 identities, 12 workloads, duration 86400, volume 4000,
workload_communication holdout, benchmark seed 42 and 200 bootstrap replicates.
Use fresh output directories. Predictions and metrics can be compared against the
stored hash/values; latency and runtime vary. Manifests may differ if executed with
other source files or environment metadata. To replay the exact source, copy `source/`
to `research/acbsd/` in a separate reproduction checkout. Do not overwrite this
working tree or rewrite Git history. No model binary serialization is required;
seeded fitting is reproducible under the pinned dependencies.

The generator and its benchmark deliberately share an illustrative simulation
vocabulary. Random Forest misses the entirely held-out communication family;
Isolation Forest flags all 60 benign operational-surge test examples. Retaining
these results is essential to interpreting the benchmark honestly.
