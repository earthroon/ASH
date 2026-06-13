# ASH-BASETRAIN-GPU-37Q-R1 Acceptance Report

## Verdict

```txt
BAKED_STATIC_ONLY
```

## Confirmed Static Acceptance

- `PATCH_ID` changed to `ASH-BASETRAIN-GPU-37Q-R1`.
- `BASE_PATCH_ID` preserves `ASH-BASETRAIN-GPU-37Q`.
- PASS status now uses the 37Q-R1 source-rebind seal.
- Default 37P-R1 and 37F receipt paths are present.
- 37P validator accepts both legacy 37P and 37P-R1 receipts.
- 37P-R1 status is accepted by prefix, not by the old 37P exact status.
- Unsupported patch id and unsupported status are split.
- 37P-R1 source binding checks confirm 37F pass/source read and no placeholder/static/bake intake.
- 37F payload receipt blocked codes are split from 37P receipt blocked codes.
- Runtime receipt artifact write is implemented in the 37Q bundle.
- No forward/backward/optimizer/safetensors mutation guards remain false.

## Not Run

```txt
cargo build = NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
runtime_gpu_probe = NOT_RUN_LOCAL_GPU_REQUIRED
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37q_selected_group_row_block_multi_workgroup_reduction_diagnostic_kernel -- --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
