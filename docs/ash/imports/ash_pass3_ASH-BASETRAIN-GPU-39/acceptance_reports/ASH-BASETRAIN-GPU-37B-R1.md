# ASH-BASETRAIN-GPU-37B-R1 Acceptance Report

## Title
Combined Row-Block Plan Digest Source Rebind / Schedule Summary Digest Binding No Read Logic Change Seal

## SSOT correction
37A seals `combined_row_block_streaming_plan_digest_hex` under `row_block_schedule_summary`, not under `source_binding`.

37B previously copied the digest from `row_block_schedule_summary` into its output `source_binding`, but still blocked by requiring the input 37A `source_binding.combined_row_block_streaming_plan_digest_hex`.

R1 removes that false requirement. The `source_binding` object itself is still required as an upstream boundary, while the combined row-block streaming plan digest is bound from `row_block_schedule_summary` as the SSOT.

## Boundary
- No representative block selection change.
- No read budget change.
- No F32 decode.
- No GPU upload.
- No full selected group read.
- No mutation.

## Expected local result
`PASS_ASH_BASETRAIN_GPU_37B_SELECTED_GROUP_ROW_BLOCK_STREAMING_READ_SMOKE_SEQUENTIAL_ROW_BLOCK_PLAN_TO_BOUNDED_MULTI_BLOCK_READ_NO_GPU_UPLOAD`
