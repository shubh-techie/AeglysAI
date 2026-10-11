# Smart Login Guardian

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Classify synthetic login attempts as allow, review or deny with a clear explanation. Any language; AeglysAI integration is optional.

## Input contract and synthetic example

The keys and units in this example define the minimum input contract. Numeric
counters/timestamps must be finite and nonnegative. IDs must be nonblank and unique,
except duplicates explicitly exercised by the submission's replay handling. Document
any additional fields or unsupported cases. Reject malformed input without printing
secrets or personal data.

```json
{
  "events": [
    {
      "id": "login-001",
      "actor": "synthetic-user-a",
      "minute": 1,
      "failed_attempts": 0,
      "new_device": false
    },
    {
      "id": "login-002",
      "actor": "synthetic-user-b",
      "minute": 2,
      "failed_attempts": 5,
      "new_device": true
    }
  ]
}
```

## Minimum acceptance criteria

A deterministic policy must distinguish at least two situations, explain its signals, reject invalid counters and produce one result per event. Choose and document your own thresholds. Include an offline entrypoint, dependencies, input/output documentation,
automated tests, deterministic reproduction instructions and limitations. Output
JSON with input identifiers (or test-array indices), your result and an explanation;
document the output schema and demonstrate it on the supplied input.

## Suggested tests

Test normal login, repeated failures, missing device context and duplicate IDs. Include at least a normal case, an edge case and invalid-input rejection.
No specific output or threshold is prescribed by the challenge.

## Safety and limitations

The actor is a synthetic label, never a real account. No identity-provider connection. No live sign-in blocking. Use only synthetic data and follow the [safety guide](../SAFETY.md).
