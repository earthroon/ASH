# MODELCORE-COMPILE-13T-G-FIX — Half/Cpu Branch Return Boundary Seal

## Purpose

Seal the remaining `ModuleLocalPackedBatchHalf` vs `ModuleLocalPackedBatchCpu` branch return mismatch after MODELCORE-COMPILE-13T-G.

## Changed Files

- `crates/lora_train/src/training.rs`

## Changes

- Kept the strict-quarantine native branch return type as `ModuleLocalPackedBatchCpu`.
- Replaced the stale direct `fallback_batch` return in the successful native/update branch with explicit CPU materialization through `materialize_module_local_packed_half_batch_checked(...)`.
- Replaced the CPU materialization branch block that materialized-and-returned the half fallback with direct return of the CPU materialized batch.
- Preserved denial behavior through the existing `bail!(...)` branch.

## Non-Goals

- No `cli_vendor187` unsafe env repair.
- No `module_local_batching` ownership repair.
- No warning hygiene sweep.
- No runtime/config/dump execution.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\\target\\MODELCORE_COMPILE_13T_G_FIX_lora_train_check.log"
```

Expected cleared patterns:

```text
ModuleLocalPackedBatchHalf
ModuleLocalPackedBatchCpu
if and else have incompatible types
```

Allowed remaining patterns:

```text
cli_vendor187 unsafe set_var
module_local_batching reason moved
warnings
```
