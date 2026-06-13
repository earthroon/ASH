# MODELCORE-COMPILE-13T-B — Model Core Schema Drift Callsite Seal

## Purpose

Align lora_train callsites with the current model_core runtime_lora schema without changing model_core schema.

## Changed Files

- crates/lora_train/src/module_local_batching.rs
- crates/lora_train/src/native_e2e_step.rs
- crates/lora_train/src/training.rs

## Changes

- Bound source/candidate LoRA byte length fields to current local variable names.
- Added explicit adapter fingerprint fields to the readback preview initializer with `None` values for the non-fingerprint preview path.
- Added an explicit type annotation for `ModuleLocalNativeLoraParamLayout` in candidate semantics layout validation.
- Replaced `native_step_started` field reads with `native_step_started()` method calls.
- Replaced the stale direct `native_step_started = false` assignment by clearing `native_e2e_stage` and preserving existing explicit state resets.
- Replaced stale `raw_reasons` pushes with `ModuleLocalNativeE2ETrainReason::Unknown(...)` entries on the current `reasons` field.
- Updated the unit-test setup to mark native start through `native_packed_half_used` instead of the removed field.
- Added `update_a_values` and `update_b_values` to `ModuleLocalCpuReferenceStepSnapshot` construction.
- Narrowed `learning_rate_for_step(...)` from f64 to f32 at the native train contract boundary.
- Replaced `train_contract.rank` with `train_contract.lora_rank`.
- Replaced `native_candidate_gate.is_ready()` with `native_candidate_gate.is_ready_for_candidate()`.
- Replaced the missing E2E bridge `with_grad_handle_pair(...)` call with explicit grad handle field binding on `ModuleLocalNativeSourcePlusDeltaE2EBridgeRequest`.

## Non-Goals

- No runtime health compact initializer repair.
- No ReferenceModel API restoration.
- No training.rs vendor telemetry/scope restoration.
- No CLI unsafe env repair.
- No config changes.
- No warning hygiene sweep.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\\target\\MODELCORE_COMPILE_13T_B_lora_train_check.log"
```

Expected cleared patterns:

```text
source_lora_a_byte_len
source_lora_b_byte_len
candidate_lora_a_byte_len
candidate_lora_b_byte_len
ModuleLocalNativeAdapterSyncReadbackPreview
native_step_started
raw_reasons
ModuleLocalCpuReferenceStepSnapshot
expected f32, found f64
train_contract.rank
is_ready
with_grad_handle_pair
```

Allowed remaining patterns belong to later 13T gates:

```text
RuntimeHealthCompact missing fields
ReferenceModel capture/module weight API residuals
training.rs vendor telemetry/scope residuals
cli_vendor187 unsafe set_var
orchestration runtime float inference
module_local_batching reason moved
batch type mismatch
```
