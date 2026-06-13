# ASH-BASETRAIN-GPU-37A Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-37A`

`Selected Group Full Row-Block Streaming Plan / CPU Tensor View Candidate To Sequential Row-Block Atlas Schedule No Read No GPU Upload Seal`

## SSOT

Input SSOT is the operator-provided 36G PASS receipt:

`artifacts/ASH_BASETRAIN_GPU_36G_BOUNDED_ROW_VIEW_READ_SMOKE.json`

The baked package intentionally does **not** include that live input receipt path, preventing overwrite of the operator's local PASS receipt.

## Scope

37A converts the selected group candidate from a bounded row smoke lineage into a full selected-group row-block schedule.

- Target tensor: `model.embed_tokens.weight`
- Shape expected from 36G candidate: `[48259, 2048]`
- Row stride: `8192` bytes
- Selected group byte range: `395337728` bytes
- Default block rows: `256`
- Expected full blocks: `188`
- Expected tail block: `131` rows
- Expected total blocks: `189`

## PASS status

`PASS_ASH_BASETRAIN_GPU_37A_SELECTED_GROUP_FULL_ROW_BLOCK_STREAMING_PLAN_CPU_TENSOR_VIEW_CANDIDATE_TO_SEQUENTIAL_ROW_BLOCK_ATLAS_SCHEDULE_NO_READ_NO_GPU_UPLOAD`

## Static baked status

`BLOCKED_36G_RECEIPT_NOT_FOUND`

This is expected for the baked artifact without local operator receipt input.

## Closed guards

- `file_open_used = false`
- `row_block_read_executed = false`
- `f32_decode_executed = false`
- `cpu_tensor_view_materialized = false`
- `selected_group_full_slice_read = false`
- `full_tensor_load_executed = false`
- `gpu_upload_executed = false`
- `forward_executed = false`
- `selected_group_backward_executed = false`
- `optimizer_step_executed = false`
- `safetensors_mutation_present = false`

## Operator commands

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37a_selected_group_full_row_block_streaming_plan
```

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37a_selected_group_full_row_block_streaming_plan -- --bounded-row-read-receipt .\artifacts\ASH_BASETRAIN_GPU_36G_BOUNDED_ROW_VIEW_READ_SMOKE.json
```

```powershell
Get-Content .\artifacts\ASH_BASETRAIN_GPU_37A_SELECTED_GROUP_FULL_ROW_BLOCK_STREAMING_PLAN.json |
  ConvertFrom-Json |
  Select-Object patch_id,status,verdict,pass
```

```powershell
$r = Get-Content .\artifacts\ASH_BASETRAIN_GPU_37A_SELECTED_GROUP_FULL_ROW_BLOCK_STREAMING_PLAN.json -Raw | ConvertFrom-Json
$r.row_block_schedule_summary | ConvertTo-Json -Depth 8
$r.tail_block_summary | ConvertTo-Json -Depth 8
```

## Next

`ASH-BASETRAIN-GPU-37B`

`Selected Group Row-Block Streaming Read Smoke / Sequential Row-Block Plan To Bounded Multi-Block Read No GPU Upload Seal`
