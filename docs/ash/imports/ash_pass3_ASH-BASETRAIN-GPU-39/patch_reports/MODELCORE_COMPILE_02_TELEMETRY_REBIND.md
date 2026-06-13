# MODELCORE-COMPILE-02 — Runtime Splice Telemetry API Rebind

## Purpose

Rebind runtime splice telemetry APIs inside `model_core` without replacing snapshot semantics with take/drain semantics.

## Changed Files

- `crates/model_core/src/generation_telemetry.rs`
- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/lib.rs`

## Changes

- Added direct `anyhow::Result` import in `generation_telemetry.rs`.
- Added direct backend imports for `snapshot_runtime_splice_telemetry_summary` and `with_runtime_splice_telemetry_label`.
- Kept `take_runtime_splice_telemetry_summary` only for compact/drain summary emission.
- Promoted `with_tensorcube_runtime_splice_label` to `pub(crate)`.
- Explicitly imported `with_tensorcube_runtime_splice_label` in `decode_state.rs`.
- Removed unused root-level `snapshot_runtime_splice_telemetry_summary` / `take_runtime_splice_telemetry_summary` imports from `lib.rs`.
- Intentionally kept root-level `with_runtime_splice_telemetry_label` in `lib.rs` because `decode_state.rs`, `generation_sampling.rs`, and `native_wgpu.rs` currently consume it through `use super::*`.

## Non-Goals

- No sampling helper extraction.
- No reference math extraction.
- No runtime_lora schema repair.
- No NativeWgpuModel accessor repair.
- No config path changes.

## Prohibited Shortcut Avoided

`snapshot_runtime_splice_telemetry_summary()` was not replaced with `take_runtime_splice_telemetry_summary()`.

## Validation

Cargo is not available in this execution environment, so local compile verification could not be run here.

Run locally:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_02_check.log"
```

Expected cleared patterns:

```text
cannot find function snapshot_runtime_splice_telemetry_summary
cannot find function with_runtime_splice_telemetry_label
cannot find function with_tensorcube_runtime_splice_label
E0107 at generation_telemetry.rs:699
```

Expected remaining families are still owned by later commits:

```text
sampling helper inaccessible
reference checkpoint math helper inaccessible
runtime_lora schema drift
NativeWgpuModel private field/method access
model_layers runtime_lora hook access
```
