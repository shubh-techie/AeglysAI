# Code and dependency safety

Use local synthetic data. Never request production logs, participant credentials,
private accounts, unpublished inventions or attorney materials. Respect third-party
licenses and do not upload protected input to external tools.

Declare dependencies, versions and installation steps. Review their provenance and
licenses; use lockfiles when the language supports them. No opaque executable
attachments or scripts that require administrator access. Keep network/service calls
optional and offer an offline path. Review dependency vulnerabilities with an
appropriate language tool; report checks actually run and unresolved issues.

Test only local mock resources. Do not connect production identity providers,
cloud accounts or live enforcement. Input values cannot override authorization or
safety boundaries. Keep subprocess execution, file paths and resource usage bounded.
Scanners and successful tests do not certify safety. Follow the repository
[security/disclosure policy](../../SECURITY_AND_DISCLOSURE_POLICY.md).
