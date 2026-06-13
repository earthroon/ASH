# MODELCORE-COMPILE-13T-I — Ownership Move Residual Seal

## Purpose

Seal remaining `lora_train` ownership move errors after type and unsafe boundary repairs.

## Changed Files

- `crates/lora_train/src/module_local_batching.rs`
- `crates/lora_train/src/training.rs`

## Changes

- Reworked `validate_train_storage_access` so the access failure predicate is evaluated once and the non-`Copy` `ModuleLocalNativeTrainInputPreflightReason` is pushed at most once.
- Preserved `vendor15_long_run_stability_telemetry` for later summary/performance harness reads by cloning it when storing the owned runtime-health copy.
- Avoided fake/default telemetry construction.
- Preserved reason and telemetry reporting semantics.

## Non-Goals

- No CLI env unsafe repair.
- No warning hygiene sweep.
- No schema redesign.
- No dump runtime execution.
- No config changes.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_I_lora_train_check.log"
```

Expected cleared patterns:

```text
use of moved value: `reason`
use of moved value: `vendor15_long_run_stability_telemetry`
E0382
```
