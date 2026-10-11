# Monthly impact reporting contract

Contract version: **1.0.0**. Underlying evidence version: **1.0.0** unchanged.
See [schema](schemas/monthly-impact-1.0.0.schema.json),
[Portal integration guide](PORTAL-INTEGRATION.md),
[synthetic report](fixtures/valid/synthetic-monthly.json) and
[pinned source bytes](fixtures/snapshots/source-evidence.json).

The report is an offline envelope, independent of frontend/framework implementation.
It does not implement a Portal, collection API, scheduler or publication service.
Every fixture is synthetic and proves no community result.

Periods are UTC calendar months, half-open [start, end). Every metric declares its
level, unchanged definition/unit, evidence references, aggregation and exclusions,
coverage, verification and limitations. Count = sum of referenced already-deduplicated
evidence counts minus declared cross-source exclusions. Never sum different levels
into a total impact score. Duplicate snapshots/metric references and incompatible
metric definitions are rejected. Cross-source exclusion truth requires human review;
no raw person identifiers are exported for deduplication.

Source snapshots pin exact bytes with SHA-256, safe relative artifact paths and an
embedded evidence record. Bytes must parse to that same record and conform to both
evidence schema and semantics. Do not reserialize archives and silently update hashes.
Partial-period evidence must remain labelled partial; full coverage requires a gapless
union of source intervals. Complete data quality means no declared processing issues;
it does not imply full coverage, adoption or source truth. Incomplete quality requires
an explicit issue and blocks approved publication.

Evidence verification remains draft/verified. Monthly publication uses its own
pending/approved/withdrawn state; these are not new evidence statuses. Approval
requires complete quality, verified metrics/sources, a reviewed public approval
reference and timestamp at/after period end. Human owner authorization remains
required even when the JSON claims approval. `--publication` rejects pending or
withdrawn reports; validation alone has no publishing side effect.

Revisions are immutable releases. Revision 1 has no history; later revisions include
all earlier revisions in order with exact raw-file hashes, same report ID/month/data
kind and matching prefixes. Archive every referenced source and prior report alongside
its original approval state. Retain a reason for correction; do not overwrite the
old release or imply the historical values were always corrected. Validators check
archived report semantics against their own retained sources. Up to 21 revisions,
20 current sources, 100 metrics and 1 MiB per JSON artifact keep processing bounded.
More requires an explicit future contract change, not truncation.

See [task status](STATUS.md) and [task roadmap](ROADMAP.md).
