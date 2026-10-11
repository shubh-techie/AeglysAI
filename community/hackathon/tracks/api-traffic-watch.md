# API Traffic Watch

Status: **IMPLEMENTED** challenge specification; participant solution not supplied.

## Goal

Summarize synthetic request windows and recommend review or a simulated rate limit. Any language; AeglysAI integration is optional.

## Input contract and synthetic example

The keys and units in this example define the minimum input contract. Numeric
counters/timestamps must be finite and nonnegative. IDs must be nonblank and unique,
except duplicates explicitly exercised by the submission's replay handling. Document
any additional fields or unsupported cases. Reject malformed input without printing
secrets or personal data.

```json
{
  "window_seconds": 60,
  "events": [
    {
      "id": "request-001",
      "actor": "synthetic-client-a",
      "second": 1,
      "path": "/sample"
    },
    {
      "id": "request-002",
      "actor": "synthetic-client-a",
      "second": 2,
      "path": "/sample"
    }
  ]
}
```

## Minimum acceptance criteria

Declare window boundaries and threshold. Count without double-counting duplicate IDs. Produce a window summary and distinguish recommendations from executed mock controls. Include an offline entrypoint, dependencies, input/output documentation,
automated tests, deterministic reproduction instructions and limitations. Output
JSON with input identifiers (or test-array indices), your result and an explanation;
document the output schema and demonstrate it on the supplied input.

## Suggested tests

Test an empty window, exact boundaries, late events, duplicate events and different synthetic actors. Include at least a normal case, an edge case and invalid-input rejection.
No specific output or threshold is prescribed by the challenge.

## Safety and limitations

No real endpoints, traffic capture or network blocking. Use only local mocked actions. Use only synthetic data and follow the [safety guide](../SAFETY.md).
