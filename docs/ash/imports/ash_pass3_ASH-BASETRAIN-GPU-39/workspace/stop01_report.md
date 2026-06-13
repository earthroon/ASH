# 16AI-QW-38G-R6A-STOP-01 Report

## Patch
Safe Stop Controlled Execute Seal

## SSOT
SALAD-03B post-check + SALAD-02 risk + runtime stop capability.

## Implemented
- Added `crates/model_core/src/stop01_safe_stop.rs`.
- Added `Stop01Mode`, `Stop01Reason`, `Stop01Action`.
- Added safe-stop gate, synthetic execution receipt, runtime trait, summary aggregation.
- Wired STOP-01 into `sampler_parity::append_receipt()` after SALAD-03B.
- Exported STOP-01 API from `model_core/src/lib.rs`.

## Contracts
- Default mode is `Off`.
- Controlled execution requires `ASH_STOP01_MODE=controlled_execute` and `ASH_STOP01_BEHAVIOR_CHANGE_ALLOWED=true`.
- `output_tail_truncated=false` is fixed by contract.
- `eos_bias_stop_executed=false` is fixed by default.
- No runtime stop is executed without gate and receipt.

## Runtime Status
This bake is static. Cargo/runtime smoke was not executed in this container.
