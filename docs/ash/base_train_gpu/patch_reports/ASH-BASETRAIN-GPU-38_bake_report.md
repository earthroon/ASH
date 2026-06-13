# ASH-BASETRAIN-GPU-38 Bake Report

## Patch

ASH-BASETRAIN-GPU-38 — Selected Group Row Block GPU Forward Candidate / Atlas Weight Stream To Bounded MatVec Output Seal / No Optimizer No Weight Mutation No Training Commit

## Files added

- crates/base_train/src/ash_basetrain_gpu_38_selected_group_row_block_gpu_forward_candidate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_38_selected_group_row_block_gpu_forward_candidate.rs
- specs/ASH_BASETRAIN_GPU_38_SPEC.md
- artifacts/ASH_BASETRAIN_GPU_38_BAKE_MANIFEST.json
- artifacts/ASH_BASETRAIN_GPU_38_STATIC_CHECKS.json
- artifacts/ASH_BASETRAIN_GPU_38_STATIC_CHECKS.txt
- acceptance_reports/ASH-BASETRAIN-GPU-38.md

## Verification

- Static string/contract checks: PASS
- Cargo build: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- Runtime GPU probe: NOT_RUN_LOCAL_GPU_REQUIRED

## Local run command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_38_selected_group_row_block_gpu_forward_candidate -- `
  --reduction-parity-receipt .\artifacts\ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json `
  --multi-workgroup-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
