# ASH-BASETRAIN-GPU-37Q Bake Report

## Source SSOT

- ASH-BASETRAIN-GPU-37P PASS receipt: required at runtime, not included in this ZIP
- ASH-BASETRAIN-GPU-37F PASS receipt: required at runtime, not included in this ZIP

## Baked State

Static artifact is sealed as `BLOCKED_37P_RECEIPT_NOT_FOUND`.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37q_selected_group_row_block_multi_workgroup_reduction_diagnostic_kernel -- --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
