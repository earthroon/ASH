# SFT-GPU-RUN-08 Bake Report

## Commit

SFT-GPU-RUN-08 -- GPU-Trained Current Pointer Switch / TextureLoad Revalidation Seal

## Source SSOT

`ash_pass3_SFT-GPU-RUN-07_promotion_apply_candidate_baked.zip`

## Added

- `crates/ash_core/src/sft_gpu_current_pointer_switch.rs`
- `crates/ash_core/tests/sft_gpu_run_08_current_pointer_switch.rs`
- `crates/lora_train/src/gpu_trained_current_pointer_switch.rs`
- `crates/lora_train/tests/gpu_trained_current_pointer_switch.rs`
- `crates/burn_webgpu_backend/src/gpu_trained_current_pointer_switch.rs`
- `crates/burn_webgpu_backend/tests/gpu_trained_current_pointer_switch.rs`
- `acceptance_reports/SFT-GPU-RUN-08_current_pointer_switch.md`
- `bake_artifacts/SFT-GPU-RUN-08_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-GPU-RUN-08_STATIC_SCAN.txt`
- `bake_artifacts/SFT-GPU-RUN-08_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- reviewed promotion apply commit
- runtime current pointer update
- current pointer switch
- slot ready mark
- rollback ledger commit
- textureLoad revalidation
- post-switch health handoff candidate

## Closed

- unreviewed promotion apply
- rollback execution
- lifecycle mutation
- slot action apply
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample weight fetch

## Validation

Static validation passed. Runtime compilation and guarded pointer switch remain pending because `cargo`, `rustc`, and target backend runtime are unavailable in this environment.
