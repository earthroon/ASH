# ASH-BASETRAIN-GPU-25 Bake Report

## Scope

Added GPU local loss repeatability audit using the ASH-BASETRAIN-GPU-24 local loss WGSL shader.

## Files added

- `crates/base_train/src/ash_basetrain_gpu_25_gpu_local_loss_repeatability_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_25_gpu_local_loss_repeatability_audit.rs`
- `ASH_BASETRAIN_GPU_25_OPERATOR_COMMANDS.ps1`
- `ASH_BASETRAIN_GPU_25_STATIC_CHECKS.txt`
- `ASH_BASETRAIN_GPU_25_LOCAL_VALIDATION.txt`
- `ASH_BASETRAIN_GPU_HANDOFF_AFTER_25.md`
- `acceptance_reports/ASH-BASETRAIN-GPU-25.md`

## Boundary

No backward, no optimizer, no full-vocab loss, no dataset training loss, no safetensors mutation.

## Local build note

Sandbox cargo is unavailable. Operator local cargo build/run is required for runtime PASS.
