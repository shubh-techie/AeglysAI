# Contributing to AeglysAI

AeglysAI researches secure distributed systems with synthetic, reproducible examples.
Start with the [community index](community/README.md) and [roadmap](community/ROADMAP.md).

1. Discuss a focused public-safe change in an issue. State acceptance criteria.
2. Use a local branch and one reviewable change per proposal. Preserve history,
   project conventions, .NET 8 and inward architecture dependencies.
3. Add meaningful tests. Run the applicable build/test commands in README and
   the [security gates](scripts/security/README.md). A failed or unavailable scan
   blocks publication; never use an exclusion to hide a finding.
4. Review filenames and the full diff for secrets, personal data and unapproved
   disclosure. Keep restricted evidence outside the repository.
5. Describe observed results, limitations and reproduction steps in the PR template.
   Repository-owner publication approval and reviewer acceptance remain separate
   from passing tests. Agents must follow AGENTS.md and stop for review before commits.

Community metrics follow the [evidence standard](community/evidence/README.md).
Synthetic fixtures are examples, not evidence of adoption or impact.
Hackathon participants may use any language; integration is optional.

Follow the [conduct policy](CODE_OF_CONDUCT.md) and
[security/disclosure policy](SECURITY_AND_DISCLOSURE_POLICY.md).
Do not include private vulnerability details in a public issue. No private reporting
address or response-time guarantee is currently established; request an approved
private channel from the owner without disclosing the sensitive details.
