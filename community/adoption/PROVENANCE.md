# Source, research citation and external-reference review

Use an immutable public source commit, reviewed artifact SHA-256 and a reproducible
execution reference. The source digest is of exact approved artifact bytes; reviewers
must recompute it. Never test suspected credentials or scrape participant profiles.
A nonzero syntactically valid hash is not evidence that bytes were checked.

For research citations, verify the primary publication, authorship/date and the
specific technical statement before citing it. Resolve an actual DOI or public
reference manually through an approved browser; validators fetch nothing.
A DOI reference uses https://doi.org/10. followed by the real identifier. No real
citation is provided by synthetic examples, and no citation implies endorsement.
Check for corrections/retractions and record uncertainty. Keep confidential sources
and private URLs out of public evidence. A URL's public syntax does not certify
that its content is safe to publish.

Use `python scripts/community/validate_adoption.py RECORD.json` in the pinned
environment. Public aggregate records reject dummy digests and synthetic domains.
Verified independent records are eligible for further level-5 review, not automatic
monthly aggregation; an approved evidence-standard record is still required.
