# Recognition, consent and withdrawal

Contract version: 1.0.0. Public records identify accepted artifacts, not people.
No names, email addresses, handles, profiles, awards or endorsement fields are
accepted by the recognition schema. Even public URLs must be reviewed for privacy.

Credit modes: artifact-only, anonymous or none. Declining recognition does not
change technical review. Before publishing either artifact credit or anonymous
thanks, obtain explicit consent for public attribution, verify acceptance and record
an approved public-safe review reference. Keep identity and original consent proof
in owner-controlled storage outside Git; the JSON assertion is not proof of consent.
No private reporting/consent channel is configured by this implementation. The
owner must establish one before collecting real consent or recognition records.

Ask the owner for an approved private withdrawal channel without posting personal
information publicly. Withdrawal sets consent and publication to withdrawn, scope
to none, credit mode to none and removes contribution/review references. A minimal
opaque artifact-record tombstone prevents accidental republishing; it contains no
person identifier. Maintainers must remove public displays/caches they control and
avoid republishing withdrawn records. Offline validators enforce minimization, not
an actual deletion service or legal right determination. Git history and external
copies cannot be promised erased; do not rewrite history automatically.

Corrections require a new reviewed record and factual acceptance evidence. Never
invent contributor identities, accepted work, awards or endorsements. Retention
policy, responsible reviewer and consent-channel approval remain owner decisions.

Validate with `python scripts/community/validate_recognition.py RECORD.json` using
the pinned community environment. Synthetic fixtures never count as real recognition.
