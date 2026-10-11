# Community evidence standard

Schema version: **1.0.0**, [JSON Schema](schemas/evidence-1.0.0.schema.json), Draft 2020-12.
The schema and semantic validator form one contract. Neither certifies source truth.

| Level | Metric definition | Suitable source | Deduplication and verification |
| --- | --- | --- | --- |
| 1 Reach | Number of content view events in the period, not unique people | Reviewed public aggregate or access-controlled analytics summary | Remove known bot/retry events; document platform limitations; reconcile totals |
| 2 Interest | Unique expressions of interest in the period | Reviewed aggregate of opted-in interest signals | One signal per declared unit; reconcile against private source without exporting identities |
| 3 Participation | Participants meeting a declared attendance/submission criterion | Reviewed organizer aggregate | One eligible participant per period; reviewer checks criterion and aggregate |
| 4 Contribution | Accepted, attributable technical contributions in the period | Public merged change or maintainer acceptance record | One accepted change per stable public artifact; review acceptance and reproducibility |
| 5 Independent technical impact | Independent reproductions or uses with verified technical outcomes | Public external technical report and review | One independent outcome per declared unit; review independence, execution and limitations |

Counts at different levels are not interchangeable, summed into adoption, or inferred
from each other. Reach is not participation; contributions are not proven impact.
All metrics must declare definition, source reference/digest, timezone-aware start
and end, deduplication unit/method and raw/excluded totals, verification method/status,
review reference and limitations. Count equals raw minus excluded. IDs must be unique.
Periods are half-open [start, end) and require start < end. A version change is required
for an incompatible schema change; never reinterpret previously published records.

Keep identities, email addresses, tokens, raw IP/device logs, unapproved research,
legal communications and confidential drafts outside Git. Even pseudonymous raw
participant identifiers belong outside this public aggregate contract. Public source
URLs cannot include credentials, queries or fragments. Do not publish private source
URLs. Never fetch sources automatically during validation.

Before marking verified, a reviewer must inspect source authenticity, reconcile the
period and exclusions, check privacy/publication approval, recompute the digest and
record a public-safe review. Level 5 additionally requires documented independence
from the project and an executed technical outcome. A self-declared JSON status does
not establish that these checks occurred. Draft records are not verified evidence.

SYNTHETIC records must use synthetic sources; PUBLIC_AGGREGATE records must use
public aggregate sources. Verified synthetic records remain fixture checks, never
real adoption or impact. Source digests are SHA-256 of the exact reviewed public-safe
source bytes. The zero digest in synthetic fixtures is a declared dummy value and
is not an observed source hash. Missing/private evidence blocks a real verified claim.

Run locally in an isolated environment:

```sh
python3 -m venv /tmp/aeglysai-community-env
/tmp/aeglysai-community-env/bin/python -m pip install -r scripts/community/requirements.txt
/tmp/aeglysai-community-env/bin/python scripts/community/validate_evidence.py community/evidence/fixtures/valid/synthetic-all-levels.json
/tmp/aeglysai-community-env/bin/python -m unittest discover -s scripts/community/tests -v
```

Use `--require-verified` when reviewing a publication that claims verified evidence.
A malformed schema, record, missing dependency or failed verification exits nonzero.
Diagnostics print error categories and positions, never submitted field values.
[Valid](fixtures/valid/synthetic-all-levels.json) and invalid fixtures are synthetic.

See [task status](STATUS.md) and [task roadmap](ROADMAP.md).


## Event-stage classification — review 002

Registered applicants, qualification submissions, qualified applicants, selected competitors, final project submissions, verified projects, finalists, winners and independently adopted implementations are distinct populations. Registration is an accepted official Form record; qualification submission is a submitted evidence packet; qualification requires organizer eligibility/evidence approval; selection requires an explicit organizer decision. Final submission is a selected team's delivered project; verified project means acceptance criteria and reproducibility reviewed; finalist means shortlisted under Round 1; winner means a Round 2 ranking/award decision. Independent adoption requires external independence and executed technical evidence, regardless of competition success.

For each published aggregate declare its event, period, counted unit (applicant, team, submission or implementation), source snapshot, reviewer, exclusions and deduplication method. Applicant counts deduplicate private registration records; team/project counts deduplicate stable internal team/project records; adoption counts deduplicate independent implementation outcomes. Keep these mappings private. Report missing evidence as unknown, never zero. Do not sum stages, infer transitions or equate projects with people. Publish only approved privacy-safe aggregates.

Event applicant/qualification/selection counts use individuals; team submission, verified project and finalist/winner counts use explicitly declared teams or projects. Every team member qualifies independently; team size is 1–4. Private team-ID/registration mappings never enter public evidence. Publication consent is separate from judging consent. Competition outcomes remain distinct from independent adoption.
