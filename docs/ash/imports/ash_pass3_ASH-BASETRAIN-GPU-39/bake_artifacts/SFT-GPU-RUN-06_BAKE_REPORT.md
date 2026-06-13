# SFT-GPU-RUN-06 Bake Report

## Patch

SFT-GPU-RUN-06 — GPU-Trained Adapter Runtime Attach Dry-run / Current Pointer Guard Seal

## Base

ash_pass3_SFT-GPU-RUN-05_gpu_trained_operator_approval_baked.zip

## Added

- crates/ash_core/src/sft_gpu_runtime_attach_dry_run.rs
- crates/ash_core/tests/sft_gpu_run_06_runtime_attach_dry_run.rs
- crates/lora_train/src/gpu_trained_runtime_attach_dry_run.rs
- crates/lora_train/tests/gpu_trained_runtime_attach_dry_run.rs
- crates/burn_webgpu_backend/src/gpu_trained_runtime_attach_dry_run.rs
- crates/burn_webgpu_backend/tests/gpu_trained_runtime_attach_dry_run.rs
- acceptance_reports/SFT-GPU-RUN-06_runtime_attach_dry_run.md
- bake_artifacts/SFT-GPU-RUN-06_BAKE_REPORT.md
- bake_artifacts/SFT-GPU-RUN-06_STATIC_VALIDATION.txt
- bake_artifacts/SFT-GPU-RUN-06_STATIC_SCAN.txt
- bake_artifacts/SFT-GPU-RUN-06_FILE_DIGESTS.sha256

## Modified

- crates/ash_core/src/lib.rs
- crates/lora_train/src/lib.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- runtime attach dry-run
- adapter load sanity check
- target module compatibility check
- artifact revalidation
- promotion intent consumption dry-run
- textureLoad guard revalidation
- current pointer unchanged guard

## Closed

- promotion apply
- runtime current pointer update
- current pointer switch
- slot ready mark
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## Validation

Static validation only in this environment. `cargo`, `rustc`, and `rustfmt` are unavailable here, so compile/runtime validation remains pending for the target machine.
