# MODELCORE-COMPILE-13T-A — Import / Re-export Path Residual Seal

## Purpose

Repair lora_train import path residuals after model_core/runtime compile gates.

## Changed Files

- crates/lora_train/src/pipeline_selection.rs
- crates/lora_train/src/bridge.rs
- crates/lora_train/src/training.rs
- crates/lora_train/src/module_local_batching.rs

## Changes

- Imported `HardCaseReplayCompact` through the crate root re-export instead of `hard_case`.
- Imported `is_module_local_trace_supported_target` through the crate root re-export.
- Imported `prepare_module_local_train_input_with_backend` through the crate root re-export.
- Imported `ModuleLocalNativeLoraParamLayout` from `model_core` root.

## Non-Goals

- No schema field renames.
- No runtime health compact repair.
- No native_e2e_step repair.
- No training.rs telemetry scope repair.
- No config changes.
- No warning hygiene sweep.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_A_lora_train_check.log"
```

Expected cleared patterns:

```text
HardCaseReplayCompact
is_module_local_trace_supported_target
prepare_module_local_train_input_with_backend
ModuleLocalNativeLoraParamLayout
```

Allowed remaining patterns:

```text
source_lora_a_byte_len
candidate_lora_a_byte_len
native_step_started
raw_reasons
RuntimeHealthCompact missing fields
training.rs telemetry/scope residuals
cli_vendor187 unsafe set_var
```
