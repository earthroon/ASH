# MODELCORE-COMPILE-13S — LoRA Train Compile Residual Seal

## Purpose

Resolve the remaining `lora_train` compile residuals after the runtime crate reached warning-only status.

## Changed Files

- crates/lora_train/src/governance_runtime.rs
- crates/lora_train/src/pipeline.rs

## Changes

- Closed `evaluate_counterfactual_policies()` before the following test helper/test items.
- Kept the function return expression as the `collect()` result instead of discarding it with a semicolon.
- Renamed the later counterfactual trust helper to avoid colliding with the earlier test helper when test items are compiled.
- Replaced the giant `serde_json::json!({ ... })` object in `native_end_to_end_summary_from_runtime_health()` with a `serde_json::Map` assembled by individual `summary.insert(...)` calls.
- Preserved all existing field keys and value expressions in the native E2E summary.

## Non-Goals

- No recursion-limit increase.
- No LoRA dump runtime execution.
- No config changes.
- No model_core/runtime schema changes.
- No warning hygiene sweep.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13S_lora_train_check.log"
```

Expected cleared patterns:

```text
expected `;`, found keyword `fn`
recursion limit reached while expanding `$crate::json_internal!`
```

Allowed remaining patterns:

```text
warnings only, or newly surfaced compile errors outside 13S scope
```
