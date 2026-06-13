# 16AI-QW-38G-R6A-LORA-RT-02B-E — Backoff Invocation Failure Evidence / Stderr Tail Receipt Seal

## Status

PASS_STATIC_BAKE_PENDING_LOCAL_POWERSHELL_RUN

## Implemented

- Replaced RT-02B-D ambiguous all-scale failure reporting with invocation-aware attempt states.
- Added per-attempt stdout_tail and stderr_tail capture into backoff receipt.
- Separated attempt_status into FAIL_ORCHESTRATOR_INVOCATION, INFERENCE_COMPLETED_BUT_REJECTED, and ACCEPTED.
- Skips mojibake evaluation when output artifact is missing.
- Skips delta evaluation when apply receipt is missing.
- Splits all-invocation-failure status into FAIL_BACKOFF_INVOCATION_ALL_ATTEMPTS_FAILED.
- Fixes selected_scale=null consistency: selected_attempt_* fields stay null when no selected attempt exists.
- Runs scale 0.00 as adapter-off baseline by setting domainAdapterEnabled=false and nulling adapter paths/receipts.
- Keeps ProcessStartInfo wrapper from RT-02B-C/D.

## SSOT

RT-02B-D showed all attempts exiting with code 1 and missing apply receipts. This is invocation failure evidence, not adapter quality evaluation. RT-02B-E seals the difference in receipt fields and records stderr/stdout tails for the next root-cause patch.

## Files

- workspace/examples/lora_rt02b_full_backoff.ps1
- workspace/examples/lora_rt02b_scale_sweep_low.ps1
- workspace/examples/lora_rt02b_verify.ps1

## Expected final statuses

- FAIL_BACKOFF_INVOCATION_ALL_ATTEMPTS_FAILED when every attempt exits nonzero.
- FAIL_ADAPTER_BACKOFF_ALL_COMPLETED_ATTEMPTS_REJECTED when inference completes but guards reject all attempts.
- PASS_ADAPTER_DISABLED_SAFE_BASELINE_SELECTED when adapter-off scale 0.00 baseline is selected.
- PASS_ADAPTER_BACKOFF_SAFE_OUTPUT_SELECTED when a lower adapter-on scale is selected.
