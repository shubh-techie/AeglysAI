# Security and disclosure policy

Use synthetic data and server-owned authorization context for public examples.
Keep credentials in environment variables, local secret storage or a secret
manager. Do not place customer data, production logs or private keys in Git.

Keep confidential invention materials, legal communications, private research
and unapproved evidence in access-controlled storage **outside this repository**.
A private branch of a public repository is not a confidentiality boundary.
Ignore rules are backup guards: they do not protect tracked files, force-added
files, history, archives, bind mounts or content under an unexpected filename.

Before proposing a commit, inspect staged filenames and the staged diff; run
the [local security gates](scripts/security/README.md). Publication requires
explicit owner authorization. Automated scanners are heuristics and cannot
determine whether an invention is safe to disclose. Obtain human review for
uncertain material. Do not place protected details in issues, pull requests,
CI logs, uploaded artifacts or public vulnerability reports.

On suspected exposure, stop related publication, retain restricted evidence,
notify the owner through an approved private channel, and arrange credential
revocation/rotation where applicable. Do not test suspected credentials against
external services. Removal from the current tree does not remove past exposure.
Do not rewrite history or change repository settings without owner authorization.
Legal disclosure assessment belongs to qualified counsel.

No dedicated private reporting address or response-time commitment is established
here. Ask the repository owner for an approved private reporting channel without
including sensitive details in the public request.
