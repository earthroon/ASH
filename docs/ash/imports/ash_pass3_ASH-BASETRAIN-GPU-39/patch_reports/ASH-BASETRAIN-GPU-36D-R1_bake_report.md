# ASH-BASETRAIN-GPU-36D-R1 Bake Report

## Patch

ASH-BASETRAIN-GPU-36D-R1  
Adjacent Window Block Constant Name Buildfix /  
Out Of Range Symbol Rebind No Logic Change Seal

## Change Summary

The 36D source referenced an undefined constant name at two adjacent window plan overflow sites.

```txt
BLOCK_ADJ_WINDOW_PLAN_OUTSIDE_READ_RANGE
```

The source already defined the intended constant as:

```txt
BLOCK_ADJ_WINDOW_OUTSIDE_READ_RANGE
```

R1 replaces the two unresolved references with the defined constant.

## No Logic Change

The BLOCK status string remains:

```txt
BLOCKED_ADJACENT_WINDOW_PLAN_OUTSIDE_READ_RANGE
```

No adjacent window offsets, read limits, F32 stats, continuity pair logic, or guard fields were changed.

## Local Verification Needed

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_36d_bounded_weight_slice_row_sample_continuity_probe
cargo run -p base_train --bin ash_basetrain_gpu_36d_bounded_weight_slice_row_sample_continuity_probe -- --row-alignment-receipt .\artifacts\ASH_BASETRAIN_GPU_36C_BOUNDED_WEIGHT_SLICE_ROW_ALIGNMENT_PROBE.json
```
