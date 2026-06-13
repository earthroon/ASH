# MODELCORE-COMPILE-13T-F-FIX — PaddedTokenBatch Import Seal

## Purpose

Repair the residual model_core compile error introduced by the ReferenceModel bridge API patch.

`reference_checkpoint.rs` now uses `PaddedTokenBatch`, but the type was not imported from `reference_math`.

## Changed Files

- crates/model_core/src/reference_checkpoint.rs

## Changes

- Added `PaddedTokenBatch` to the existing `crate::reference_math` import list.

## Non-Goals

- No ReferenceModel API redesign.
- No lora_train callsite changes.
- No runtime health changes.
- No warning hygiene sweep.
- No config changes.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_F_FIX_lora_train_check.log"
```

Expected cleared patterns:

```text
cannot find type `PaddedTokenBatch`
cannot find struct, variant or union type `PaddedTokenBatch`
```
