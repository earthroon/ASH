# 16AI-QW-38G-R6A-LORA-RT-02B-D

## Attempt Failure Tolerant Backoff Wrapper Hotfix

### SSOT

RT-02B-C fixed PowerShell native stderr isolation, but the wrapper still treated any single scale attempt with `orchestrator_local exit_code != 0` as a fatal script error.

For backoff semantics, a failed scale attempt is evidence, not a wrapper failure. The wrapper must record the failed scale, preserve stdout/stderr log paths, append reject reasons, and continue to the next lower scale.

### Changes

- Replaced per-attempt `throw "orchestrator_local exit_code=..."` with a structured run result.
- Each attempt now records `exit_code`, `log_path`, and `stderr_path`.
- Nonzero exit code adds `ORCHESTRATOR_EXIT_CODE_<n>` to reject reasons.
- Backoff continues to the next scale instead of aborting at scale 0.15 or any other single failed attempt.
- Verify script displays `exit_code` per attempt.

### Expected behavior

If scale `0.15` exits with code `1`, the trace should contain:

```json
{
  "scale": 0.15,
  "exit_code": 1,
  "accepted": false,
  "reject_reasons": ["ORCHESTRATOR_EXIT_CODE_1", "..."]
}
```

Then the script should continue to scale `0.10`, `0.05`, and `0.0` unless a safe accepted attempt is found.

### Validation

Static validation only in the container. PowerShell and cargo are not available in this environment.
