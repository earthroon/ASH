# SFT-GPU-OBS-02 Bake Report

## Patch

`SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal`

## Added Files

```txt
crates/ash_core/src/sft_gpu_long_horizon_health_ledger.rs
crates/ash_core/tests/sft_gpu_obs_02_long_horizon_health_ledger.rs
crates/lora_train/src/gpu_adapter_health_ledger.rs
crates/lora_train/tests/gpu_adapter_health_ledger.rs
crates/burn_webgpu_backend/src/gpu_runtime_drift_ledger.rs
crates/burn_webgpu_backend/tests/gpu_runtime_drift_ledger.rs
acceptance_reports/SFT-GPU-OBS-02_long_horizon_health_ledger.md
acceptance_reports/SFT-GPU-OBS-02_static_verification.log
docs/roadmap/SFT-GPU-OBS-02_after_bake.md
patch_reports/SFT-GPU-OBS-02_bake_report.md
```

## Modified Files

```txt
crates/ash_core/src/lib.rs
crates/lora_train/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
```

## Contract

- OBS-01 source seal required.
- previous health ledger digest required.
- observation entries required.
- duplicate observation order rejected.
- timestamp reversal rejected.
- health/smoke/fallback/rollback/digest/backend/textureLoad/safety trends computed.
- runtime drift ledger event is append-only.
- registry/current/lifecycle/runtime-training mutations remain closed.

## Static Verification

Performed in container:

- Rust delimiter balance check on added files.
- Module export wiring check.
- Required file presence check.

Not performed:

- `cargo test` because cargo/rustc/rustfmt are unavailable in this container.
