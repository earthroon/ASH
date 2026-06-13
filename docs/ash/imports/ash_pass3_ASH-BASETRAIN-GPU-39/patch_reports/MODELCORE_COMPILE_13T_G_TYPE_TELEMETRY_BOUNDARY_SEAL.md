# MODELCORE-COMPILE-13T-G — Type / Telemetry Field Boundary Residual Seal

## Purpose

Seal remaining lora_train type boundary and telemetry field drift errors after ReferenceModel bridge repair.

## Changed Files

- crates/lora_train/src/orchestration_runtime.rs
- crates/lora_train/src/training.rs

## Changes

- Added explicit `f32` typing for runtime instability clamp.
- Replaced `&String::to_path_buf()` usage with explicit `PathBuf::from(manifest_path.as_str())`.
- Rebound stale vendor10 candidate delta dispatch/readback field access to current `ModuleLocalNativeSourcePlusDeltaE2ESmokeTelemetry` fields through narrow helpers.
- Replaced stale projected output rank access with the known training config LoRA rank.
- Converted unavailable CPU reference values in quarantined native n-step input to `None` at `Option<T>` boundaries.
- Set unavailable native source+delta byte lengths to zero only in the quarantined route where input/source+delta readiness is already false.
- Preserved CPU fallback materialization for validation while keeping the fallback branch return type as `ModuleLocalPackedBatchHalf`.

## Non-Goals

- No `cli_vendor187` unsafe env repair.
- No `module_local_batching` ownership repair.
- No warning hygiene sweep.
- No dump runtime execution.
- No model_core schema changes.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\\target\\MODELCORE_COMPILE_13T_G_lora_train_check.log"
```

Expected cleared patterns:

```text
clamp
to_path_buf
candidate_delta_dispatch_submitted
candidate_delta_readback_verified
no field `rank`
mismatched types
ModuleLocalPackedBatchHalf
ModuleLocalPackedBatchCpu
```
