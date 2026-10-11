# Predict the Outage

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Predict a synthetic service-health warning using past measurements. Any language; AeglysAI integration is optional.

## Input contract and synthetic example

The keys and units in this example define the minimum input contract. Numeric
counters/timestamps must be finite and nonnegative. IDs must be nonblank and unique,
except duplicates explicitly exercised by the submission's replay handling. Document
any additional fields or unsupported cases. Reject malformed input without printing
secrets or personal data.

```json
{
  "training": [
    {
      "minute": 1,
      "latency_ms": 20,
      "error_count": 0
    },
    {
      "minute": 2,
      "latency_ms": 22,
      "error_count": 0
    }
  ],
  "test": [
    {
      "minute": 3,
      "latency_ms": 70,
      "error_count": 4
    }
  ]
}
```

## Minimum acceptance criteria

Use a chronological split. Declare prediction horizon and threshold; use only information available at prediction time. Report warnings and limitations, not proven outage prevention. Include an offline entrypoint, dependencies, input/output documentation,
automated tests, deterministic reproduction instructions and limitations. Output
JSON with input identifiers (or test-array indices), your result and an explanation;
document the output schema and demonstrate it on the supplied input.

## Suggested tests

Test missing timestamps, unordered events, missing values and future-label leakage. A simple trend rule is acceptable. Include at least a normal case, an edge case and invalid-input rejection.
No specific output or threshold is prescribed by the challenge.

## Safety and limitations

No production monitoring or cloud actions. Evaluation quality requires separately held-out labels, not a claim based on this example. Use only synthetic data and follow the [safety guide](../SAFETY.md).
