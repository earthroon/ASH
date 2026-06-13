# ASH-BASETRAIN-GPU-22 Bake Report

## Added

- `crates/base_train/src/ash_basetrain_gpu_22_loss_scalar_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_22_loss_scalar_audit.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-22.md`
- `patch_reports/ASH-BASETRAIN-GPU-22_bake_report.md`
- `ASH_BASETRAIN_GPU_HANDOFF_AFTER_22.md`
- `ASH_BASETRAIN_GPU_22_OPERATOR_COMMANDS.ps1`
- `ASH_BASETRAIN_GPU_22_STATIC_CHECKS.txt`
- `ASH_BASETRAIN_GPU_22_LOCAL_VALIDATION.txt`
- `ASH_BASETRAIN_GPU_22_ZIP_INTEGRITY.txt`

## Intent

Static audit of the ASH-BASETRAIN-GPU-21 local-window NLL scalar.

## No-open Boundary

No new GPU dispatch, no payload export, no new loss expansion, no backward, no optimizer, no safetensors mutation.

## Build note

Container environment has no `cargo`; local build/run remains operator-side SSOT.
