# ASH-BASETRAIN-GPU-37L Acceptance Report

## Verdict

STATIC BAKE: `BLOCKED_37K_RECEIPT_NOT_FOUND` until the operator supplies local 37K and 37F PASS receipts.

Expected runtime PASS:

```txt
PASS_ASH_BASETRAIN_GPU_37L_SELECTED_GROUP_ROW_BLOCK_DISPATCH_SMOKE_UPLOADED_BOUND_RESOURCE_TO_DIAGNOSTIC_WRITE_READBACK
```

## Opened in 37L

- bounded source `File::open` / `SeekFrom::Start` / `read_exact`
- `queue.write_buffer`
- `create_command_encoder`
- `begin_compute_pass`
- `set_pipeline`
- `set_bind_group`
- `dispatch_workgroups(5144, 1, 1)`
- diagnostic `copy_buffer_to_buffer`
- diagnostic `map_async` readback

## Still sealed

- full tensor load
- f32 decode as tensor view
- forward
- backward
- optimizer
- delta candidate
- checkpoint write
- safetensors mutation

## Required command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37l_selected_group_row_block_dispatch_smoke -- --bound-resource-upload-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_37K_SELECTED_GROUP_ROW_BLOCK_BOUND_RESOURCE_UPLOAD_CANDIDATE.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
