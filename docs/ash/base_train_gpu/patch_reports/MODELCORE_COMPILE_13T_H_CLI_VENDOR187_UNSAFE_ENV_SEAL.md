# MODELCORE-COMPILE-13T-H — CLI Vendor187 Unsafe Env Seal

## Purpose

Seal Rust 2024 unsafe process-environment mutation boundaries in `cli_vendor187.rs`.

## Changed Files

- `crates/lora_train/src/cli_vendor187.rs`

## Changes

- Added a centralized `set_vendor187_env` helper.
- Added a `set_vendor187_env_bool` helper for boolean env flags.
- Replaced direct `std::env::set_var` calls with the sealed helper.
- Kept the unsafe block localized to one helper with a SAFETY comment.
- Preserved existing env key/value semantics.
- Preserved boolean env values as `"1"` / `"0"`.
- Preserved optional env values as `Some(...)`-only mutations.

## Safety Boundary

Vendor187 env overrides are applied during CLI option bootstrap before runtime execution and worker thread startup. The helper centralizes the legacy process-env mutation boundary instead of scattering unsafe blocks across individual callsites.

## Non-Goals

- No ownership repair.
- No training pipeline repair.
- No CLI option schema redesign.
- No warning hygiene sweep.
- No runtime dump execution.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_H_lora_train_check.log"
```

Expected cleared patterns:

```text
call to unsafe function `set_var` is unsafe and requires unsafe block
cli_vendor187.rs
E0133
```

Allowed remaining patterns:

```text
E0382 reason move residual
E0382 vendor15_long_run_stability_telemetry move residual
warnings
```
