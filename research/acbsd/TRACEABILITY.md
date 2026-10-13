# AEGLYSAI-DATA-001 requirements-to-tests traceability

| Requirement | Implementation/evidence | Meaningful check |
| --- | --- | --- |
| Seed/entity/duration/volume configuration and eight families | dataset.py, scenarios/v1.json | test_bad_configuration_and_partial_instance; test_all_families_and_hard_negative |
| Ordered correlated data, independent truth, stable group entities | dataset.py generate/validate | test_quality_rejects_mutations; test_groups_and_family_holdout |
| Versioned reproducibility and integrity | dataset.py, verify.py, manifest | test_reproducible_bytes_and_seed_effect; test_tamper_and_no_overwrite |
| Schema, unique IDs, relationship/IP/category/missingness/duplicate checks | dataset.py validate | test_quality_rejects_mutations |
| Benign operational hard negatives | catalogue, deterministic score | test_all_families_and_hard_negative; test_surge_is_not_flagged_by_volume_alone |
| Train/validation/test and family holdout, no group leakage | separate ground_truth.jsonl | test_groups_and_family_holdout; mutated partition rejected |
| No label/scenario/ID inference features | FEATURES allowlist, benchmark features | test_feature_allowlist_ignores_truth_and_identifiers |
| Train-only transformations, held-out labels excluded from threshold selection | benchmark run/select_threshold | test_end_to_end_train_only_fit_and_test_label_independence |
| Failed runs preserved without overwrite | benchmark CLI failure.json | test_failed_cli_run_is_recorded_without_overwriting |
| Three executable baseline models and exact parameters | benchmark.py, summary/predictions/source snapshot | end-to-end test plus actual exploratory run |
| Precision/recall/F1/FPR/confusion/AUC/PR/latency, per-family hard negative comparison | metrics/partition summaries | test_metrics_denominators_and_score_orientation; actual run |
| Imbalance and grouped confidence intervals | manifest quality; cluster_intervals | test_threshold_uses_validation_and_cluster_intervals; actual run |
| Recommendation correctness separate from detection | risk.py, eight fixtures | test_boundaries_and_expectations; test_consistency_and_monotonicity |
| Invalid evidence rejected, recommendations only | risk.py; no external resource clients | test_invalid_evidence_fails_closed; source review |
| Existing .NET and gates preserved | unchanged production and security source | actual validation in VALIDATION.md |
| Dataset card/methodology/ADR/SPEC/roadmap/log | linked documents | offline Markdown targets/fences and Git whitespace checks |

Tests live in [tests](tests). Exact outcomes, setup failures and runtimes are in
[VALIDATION](VALIDATION.md). Passing correctness tests does not establish synthetic
representativeness, operational safety, paper hypotheses or disclosure clearance.
