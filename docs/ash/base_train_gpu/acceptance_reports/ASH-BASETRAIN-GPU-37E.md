# ASH-BASETRAIN-GPU-37E Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-37E`

## Title

Selected Group Row-Block GPU Upload Smoke / Representative Staging Plan To Actual GPU Buffer No Dispatch Seal

## SSOT

Input SSOT is the operator-provided runtime PASS receipt:

`artifacts/ASH_BASETRAIN_GPU_37D_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PLAN.json`

This baked ZIP intentionally does **not** include that live 37D receipt path, to avoid overwriting the operator's local PASS receipt with a static BLOCK sample.

## Scope

37E opens the first actual GPU upload smoke boundary for the selected representative row blocks:

- reads only the three representative source byte segments from the safetensors file,
- verifies each segment byte digest against the 37D segment contract,
- creates an actual wgpu adapter/device/queue,
- creates one representative storage buffer,
- uploads the contiguous 5,267,456 byte payload via `queue.write_buffer`,
- emits a GPU upload smoke receipt,
- does not dispatch,
- does not read back,
- does not run forward/backward/optimizer,
- does not mutate safetensors or write checkpoints.

## Expected PASS

```text
PASS_ASH_BASETRAIN_GPU_37E_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_SMOKE_REPRESENTATIVE_STAGING_PLAN_TO_ACTUAL_GPU_BUFFER_NO_DISPATCH
```

## Static sealed result in bake environment

```text
BLOCKED_37D_RECEIPT_NOT_FOUND
```

This is expected because the container does not carry the operator's live 37D PASS receipt.

## Local command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37e_selected_group_row_block_gpu_upload_smoke -- --gpu-upload-plan-receipt .\artifacts\ASH_BASETRAIN_GPU_37D_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PLAN.json
```

## Acceptance checks

- 37D receipt is explicitly supplied and PASS.
- 37D representative segment layout is closed: 3 segments, 5,267,456 payload bytes, 1,316,864 f32 samples, no gap, no overlap, no padding.
- Source segments are read with bounded `seek + read_exact` only.
- Segment byte digests match 37D.
- Actual GPU adapter/device/queue is acquired.
- Actual storage buffer is created with `COPY_DST | STORAGE | COPY_SRC`.
- `queue.write_buffer` uploads exactly 5,267,456 bytes.
- Dispatch/readback/forward/backward/optimizer/mutation are false.
