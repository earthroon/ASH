# MODELCORE-COMPILE-11 — Ownership / Borrow Seal

## Purpose

Resolve remaining Rust ownership and borrow ordering errors without changing runtime behavior.

## Changed Files

- `crates/model_core/src/runtime_lora.rs`
- `crates/model_core/src/generation_sampling.rs`

## Changes

- Replaced long-lived post-move use of borrowed measured trace references with scalar snapshots before moving `traces` into `ModuleLocalNativePerformanceProfile`.
- Preserved measured trace count, checkpoint parity sample count, ratio denominators, and mismatch reporting semantics.
- Dropped the borrowed `measured` reference vector before moving `traces` into the profile.
- Cloned `severity` only for the persisted recovery-state snapshot because the same enum value is intentionally owned by both `GpuSamplingRecoveryState.last_severity` and each returned `GpuSamplingRecoveryUpdateDecision`.

## Non-Goals

- No runtime_lora schema changes.
- No generation telemetry schema changes.
- No NativeWgpuModel boundary changes.
- No sampling policy changes.
- No config changes.

## Prohibited Shortcuts Avoided

- Did not clone `traces`.
- Did not remove measured-step mismatch reporting.
- Did not replace ownership errors with default/no-op behavior.
- Did not alter recovery severity classification or decision flow.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_11_check.log"
```

Expected cleared patterns:

```text
E0505
cannot move out of `traces` because it is borrowed
E0382
borrow of moved value: `severity`
```

Allowed remaining patterns:

```text
warnings only, or any new non-ownership compile errors discovered after prior gates
```
