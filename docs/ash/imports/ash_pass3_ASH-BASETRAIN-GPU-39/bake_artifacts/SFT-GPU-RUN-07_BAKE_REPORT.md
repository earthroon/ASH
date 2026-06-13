# SFT-GPU-RUN-07 Bake Report

## Commit

SFT-GPU-RUN-07 — GPU-Trained Promotion Apply Candidate / Rollback Ledger Seal

## Base

ash_pass3_SFT-GPU-RUN-06_runtime_attach_dry_run_baked.zip

## Added

- crates/ash_core/src/sft_gpu_promotion_apply_candidate.rs
- crates/ash_core/tests/sft_gpu_run_07_promotion_apply_candidate.rs
- crates/lora_train/src/gpu_trained_promotion_apply_candidate.rs
- crates/lora_train/tests/gpu_trained_promotion_apply_candidate.rs
- crates/burn_webgpu_backend/src/gpu_trained_promotion_apply_candidate.rs
- crates/burn_webgpu_backend/tests/gpu_trained_promotion_apply_candidate.rs
- acceptance_reports/SFT-GPU-RUN-07_promotion_apply_candidate.md
- bake_artifacts/SFT-GPU-RUN-07_BAKE_REPORT.md
- bake_artifacts/SFT-GPU-RUN-07_STATIC_VALIDATION.txt
- bake_artifacts/SFT-GPU-RUN-07_STATIC_SCAN.txt
- bake_artifacts/SFT-GPU-RUN-07_FILE_DIGESTS.sha256

## Modified

- crates/ash_core/src/lib.rs
- crates/lora_train/src/lib.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- promotion apply candidate
- apply plan
- apply preflight
- rollback ledger candidate
- rollback handle
- rollback restore pointer
- fallback target
- failure recovery candidate
- textureLoad pre-apply guard

## Closed

- actual promotion apply
- runtime current pointer update
- current pointer switch
- slot ready mark
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- runtime SFT training / gradient / optimizer

## Validation

Static validation only. The current execution environment does not provide cargo, rustc, or rustfmt.
