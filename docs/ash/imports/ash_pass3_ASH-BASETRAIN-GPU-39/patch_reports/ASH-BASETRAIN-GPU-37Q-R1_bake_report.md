# ASH-BASETRAIN-GPU-37Q-R1 Bake Report

## Result

```txt
BAKED_STATIC_ONLY
```

## Applied

- 37Q now accepts `ASH-BASETRAIN-GPU-37P-R1` as a valid upstream patch id.
- 37Q now accepts `PASS_ASH_BASETRAIN_GPU_37P_R1*` status prefix.
- Legacy 37P exact PASS acceptance remains.
- 37P unsupported patch id/status errors are split.
- 37P-R1 source binding is checked for 37F pass/source read and no placeholder/static/bake intake.
- 37F payload receipt errors use payload-specific blocked codes.
- Runtime receipt artifact writing was added for R1 and legacy 37Q paths.

## Verification

```txt
cargo build = NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
runtime GPU probe = NOT_RUN_LOCAL_GPU_REQUIRED
static checks = PASS
```

## Local Run

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37q_selected_group_row_block_multi_workgroup_reduction_diagnostic_kernel -- --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
