# Portal integration contract — research repository handover

Consume only an owner-reviewed, approved immutable repository commit. Current local
proposals are not yet public releases. No Portal source is modified by this task.

| Contract | Path | Version |
| --- | --- | --- |
| Base community evidence | community/evidence/schemas/evidence-1.0.0.schema.json | 1.0.0 |
| Monthly reporting envelope | community/reporting/schemas/monthly-impact-1.0.0.schema.json | 1.0.0 |
| Contributor recognition | community/contributors/schemas/recognition-1.0.0.schema.json | 1.0.0 |
| Independent adoption assertions | community/adoption/schemas/adoption-1.0.0.schema.json | 1.0.0 |

All use JSON Schema Draft 2020-12. Schema identifiers are versioned identifiers,
not promises of hosted schema URLs. Register the evidence schema locally under
`https://aeglysai.com/schemas/community-evidence/1.0.0`; never resolve references
through the network. Use server-side schema AND semantic validation. The monthly
validator is scripts/community/validate_monthly.py, with pinned dependencies in
scripts/community/requirements.txt; the base validator is validate_evidence.py.

```sh
python3 -m venv /tmp/aeglysai-community-env
/tmp/aeglysai-community-env/bin/python -m pip install -r scripts/community/requirements.txt
/tmp/aeglysai-community-env/bin/python scripts/community/validate_monthly.py   community/reporting/fixtures/valid/synthetic-monthly.json   --artifact-root community/reporting/fixtures/snapshots
/tmp/aeglysai-community-env/bin/python -m unittest discover -s scripts/community/tests -v
```

The pending synthetic example passes ordinary validation and MUST fail with
`--publication`. Every invalid fixture under community/reporting/fixtures/invalid
must fail. Recognition and adoption validators accept their respective positive
synthetic fixtures; their statuses never establish real consent/independence.

For ingestion, require version 1.0.0, duplicate-key rejection, finite numbers,
strict integer handling, valid timezone-aware dates, 1 MiB JSON limits and local
artifact integrity checks. Preserve exact integer values; do not silently round
large counts in frontend number types. Refuse missing snapshots or prior revisions.
Artifact roots and the validator dependency root are operator-owned configuration,
never request-controlled paths. Reject traversal and escaping symlinks. No automatic
URL fetch, hosted-model upload or unapproved raw evidence import is permitted.

Store immutable report revisions and approved public-safe source bytes; retain hashes
and the release commit. Show source, period, coverage, limitations, verification,
quality and revision explicitly. Label SYNTHETIC prominently and never combine it
with PUBLIC_AGGREGATE outcomes. Do not display pending/withdrawn reports as approved,
or draft metrics as verified. The server must authorize reviewer actions; a client
cannot make itself verified or approved by sending those JSON fields.

Consent withdrawal hides recognition and minimizes records; this repository supplies
the contract and procedure, not Portal deletion/storage code. Retention, consent
channel, reviewer identity/access controls and archival publication are owner
privacy/security decisions. Do not use adoption assertions directly as evidence
counts; convert only after the approved base-evidence review protocol.

Cross-repository end-to-end interoperability is NOT VERIFIED here. The contracts
have local tests; consuming them requires a separate authorized Portal implementation.


## Event-stage classification — review 002

Registered applicants, qualification submissions, qualified applicants, selected competitors, final project submissions, verified projects, finalists, winners and independently adopted implementations are distinct populations. Registration is an accepted official Form record; qualification submission is a submitted evidence packet; qualification requires organizer eligibility/evidence approval; selection requires an explicit organizer decision. Final submission is a selected team's delivered project; verified project means acceptance criteria and reproducibility reviewed; finalist means shortlisted under Round 1; winner means a Round 2 ranking/award decision. Independent adoption requires external independence and executed technical evidence, regardless of competition success.

For each published aggregate declare its event, period, counted unit (applicant, team, submission or implementation), source snapshot, reviewer, exclusions and deduplication method. Applicant counts deduplicate private registration records; team/project counts deduplicate stable internal team/project records; adoption counts deduplicate independent implementation outcomes. Keep these mappings private. Report missing evidence as unknown, never zero. Do not sum stages, infer transitions or equate projects with people. Publish only approved privacy-safe aggregates.


## Version compatibility and event reporting boundary

All four schema files remain byte-for-byte unchanged at version 1.0.0. Existing evidence status values and monthly metric units remain authoritative. These contracts do not encode the nine event stages as dedicated structured fields. Do not add unknown fields, invent status values, reinterpret existing units or encode participant-level administration data in them.

Distinct event-stage displays need an explicitly versioned reporting extension and migration review before Portal ingestion. Specify stage identifiers, units, immutable aggregate snapshots, period/event scope, deduplication and publication/privacy approval; test old and new consumers separately and retain immutable historical 1.0.0 reports. No such extension is implemented or released by this review. Existing 1.0.0 evidence/reporting can be reviewed for integration; a complete structured event-stage dashboard is NOT READY. Official Form URLs and organizational privacy/access decisions are also unverified.

Event applicant/qualification/selection counts use individuals; team submission, verified project and finalist/winner counts use explicitly declared teams or projects. Every team member qualifies independently; team size is 1–4. Private team-ID/registration mappings never enter public evidence. Publication consent is separate from judging consent. Competition outcomes remain distinct from independent adoption.
