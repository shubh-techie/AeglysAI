# Find the Anomaly

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Flag unusual synthetic measurements using a simple baseline and explain the method. Any language; AeglysAI integration is optional.

## Input contract and synthetic example

The keys and units in this example define the minimum input contract. Numeric
counters/timestamps must be finite and nonnegative. IDs must be nonblank and unique,
except duplicates explicitly exercised by the submission's replay handling. Document
any additional fields or unsupported cases. Reject malformed input without printing
secrets or personal data.

```json
{
  "training_values": [
    10,
    11,
    9,
    10,
    12,
    10
  ],
  "test_values": [
    11,
    10,
    30,
    9
  ]
}
```

## Minimum acceptance criteria

Separate training from test data. Fit any preprocessing only on training data. Return scores or flags with a declared threshold and explain limitations. Include an offline entrypoint, dependencies, input/output documentation,
automated tests, deterministic reproduction instructions and limitations. Output
JSON with input identifiers (or test-array indices), your result and an explanation;
document the output schema and demonstrate it on the supplied input.

## Suggested tests

Test constant training data, extreme values, malformed numbers and repeated seeded runs. Keep any evaluation labels separate from decision input. Include at least a normal case, an edge case and invalid-input rejection.
No specific output or threshold is prescribed by the challenge.

## Safety and limitations

Do not claim detection accuracy without independent test labels; the tiny example is not a quality benchmark. Use only synthetic data and follow the [safety guide](../SAFETY.md).
