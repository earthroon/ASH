# SFT-GPU-SAFETY-01 Bake Report

## Patch

GPU Train OOM / Timeout / Device Lost Recovery Seal

## Added

- `crates/ash_core/src/sft_gpu_safety_recovery.rs`
- `crates/ash_core/tests/sft_gpu_safety_01_recovery.rs`
- `crates/lora_train/src/gpu_train_failure_recovery.rs`
- `crates/lora_train/tests/gpu_train_failure_recovery.rs`
- `crates/burn_webgpu_backend/src/gpu_fault_recovery.rs`
- `crates/burn_webgpu_backend/tests/gpu_fault_recovery.rs`
- `acceptance_reports/SFT-GPU-SAFETY-01_fault_recovery.md`
- `docs/roadmap/SFT-GPU-SAFETY-01_to_SAFETY-02_after_bake.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Contract

SAFETY-01 records GPU faults as failed/held receipts, rejects CPU fallback success, marks partial artifacts for quarantine, and blocks registry intake / promotion / current pointer paths.

## Verification Limitation

Cargo was unavailable in the container; static validation was used instead of Rust compilation.
