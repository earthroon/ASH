# SFT-GPU-RUN-09 Bake Report

## Commit

SFT-GPU-RUN-09 -- GPU-Trained Current Adapter Post-Switch Health / Smoke Seal

## Source SSOT

`ash_pass3_SFT-GPU-RUN-08_current_pointer_switch_baked.zip`

## Added

- `crates/ash_core/src/sft_gpu_post_switch_health.rs`
- `crates/ash_core/tests/sft_gpu_run_09_post_switch_health.rs`
- `crates/lora_train/src/gpu_trained_post_switch_health.rs`
- `crates/lora_train/tests/gpu_trained_post_switch_health.rs`
- `crates/burn_webgpu_backend/src/gpu_trained_post_switch_health.rs`
- `crates/burn_webgpu_backend/tests/gpu_trained_post_switch_health.rs`
- `acceptance_reports/SFT-GPU-RUN-09_post_switch_health.md`
- `bake_artifacts/SFT-GPU-RUN-09_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-GPU-RUN-09_STATIC_SCAN.txt`
- `bake_artifacts/SFT-GPU-RUN-09_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- post-switch smoke
- current adapter digest check
- runtime current adapter active check
- health snapshot write
- fallback readiness check
- rollback availability check
- textureLoad post-switch guard

## Closed

- new current pointer update
- promotion apply rerun
- rollback execution
- lifecycle mutation
- slot action apply
- demotion apply
- quarantine apply
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## Validation

Static validation passed. Runtime compilation and target post-switch smoke remain pending because `cargo`, `rustc`, `rustfmt`, and target backend runtime are unavailable in this environment.
