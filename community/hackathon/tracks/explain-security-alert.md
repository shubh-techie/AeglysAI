# Explain My Security Alert

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Turn a structured synthetic alert into a clear, grounded explanation. Any language; AeglysAI integration is optional.

## Input contract and synthetic example

The keys and units in this example define the minimum input contract. Numeric
counters/timestamps must be finite and nonnegative. IDs must be nonblank and unique,
except duplicates explicitly exercised by the submission's replay handling. Document
any additional fields or unsupported cases. Reject malformed input without printing
secrets or personal data.

```json
{
  "alerts": [
    {
      "id": "alert-001",
      "severity": "review",
      "signals": [
        "new synthetic device",
        "five failed synthetic attempts"
      ],
      "action": "mock step-up"
    }
  ]
}
```

## Minimum acceptance criteria

Return alert ID, observed signals, proposed action and uncertainty. Explain only provided evidence and separate recommendation from enforcement. A rule-based solution is welcome. Include an offline entrypoint, dependencies, input/output documentation,
automated tests, deterministic reproduction instructions and limitations. Output
JSON with input identifiers (or test-array indices), your result and an explanation;
document the output schema and demonstrate it on the supplied input.

## Suggested tests

Test missing signals, contradictory signals, unknown severity and input attempting to override instructions. Include at least a normal case, an edge case and invalid-input rejection.
No specific output or threshold is prescribed by the challenge.

## Safety and limitations

No secret input, hosted-model upload or unsupported accusation about a real person. If using an external service, provide a fully offline alternative and disclose it. Use only synthetic data and follow the [safety guide](../SAFETY.md).
