# ASH-BASETRAIN-GPU-37D Acceptance Report

## Patch

Selected Group Row-Block GPU Upload Plan / F32-Decoded Representative Blocks To GPU Staging Upload Candidate No Dispatch Seal

## Static baked result

`BLOCKED_37C_RECEIPT_NOT_FOUND`

This is expected for the baked archive because the live 37C PASS receipt is intentionally not bundled.

## Required local command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37d_selected_group_row_block_gpu_upload_plan -- --row-block-f32-decode-receipt .\artifacts\ASH_BASETRAIN_GPU_37C_SELECTED_GROUP_ROW_BLOCK_F32_DECODE_SMOKE.json
```

## PASS target

`PASS_ASH_BASETRAIN_GPU_37D_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PLAN_F32_DECODED_REPRESENTATIVE_BLOCKS_TO_GPU_STAGING_UPLOAD_CANDIDATE_NO_DISPATCH`

## Contract

- Reads the 37C receipt only.
- Creates representative GPU staging/upload layout plan.
- Does not open source safetensors.
- Does not re-read row blocks.
- Does not decode F32 again.
- Does not request GPU device.
- Does not create GPU buffers.
- Does not queue upload.
- Does not dispatch.
