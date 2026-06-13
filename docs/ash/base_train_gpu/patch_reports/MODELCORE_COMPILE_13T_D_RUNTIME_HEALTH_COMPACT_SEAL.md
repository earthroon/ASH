# MODELCORE-COMPILE-13T-D — Runtime Health Compact / Runtime Isolation Telemetry Seal

## Purpose

Repair runtime health compact schema drift and restore the vendor17 runtime isolation telemetry contract in `lora_train`.

## Changed Files

- `crates/lora_train/src/runtime_health.rs`

## Changes

- Added `ModuleLocalNativeRuntimeIsolationTelemetry`.
- Added `build_module_lora_native_runtime_isolation_telemetry`.
- Filled missing `RuntimeHealthCompact` initializer fields:
  - `module_lora_native_baseline_promotion_seal`
  - `module_lora_native_gpu_dispatch_audit`
  - `module_lora_native_checkpoint_overhead`
  - `module_lora_reason_hygiene`
- Kept unavailable compact telemetry as explicit `None` in constructors that do not receive those sources.

## Non-Goals

- No `training.rs` vendor10 scope restoration.
- No `ReferenceModel` bridge API restoration.
- No CLI unsafe env repair.
- No batch type repair.
- No config changes.
- No warning hygiene sweep.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_D_lora_train_check.log"
```

Expected cleared patterns:

```text
ModuleLocalNativeRuntimeIsolationTelemetry
build_module_lora_native_runtime_isolation_telemetry
RuntimeHealthCompact
module_lora_native_baseline_promotion_seal
module_lora_native_checkpoint_overhead
module_lora_native_gpu_dispatch_audit
```
