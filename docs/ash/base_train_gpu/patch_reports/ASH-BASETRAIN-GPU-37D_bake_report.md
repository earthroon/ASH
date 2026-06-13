# ASH-BASETRAIN-GPU-37D Bake Report

## Result

Baked static artifact status: `BLOCKED_37C_RECEIPT_NOT_FOUND`

## Added

- `crates/base_train/src/ash_basetrain_gpu_37d_selected_group_row_block_gpu_upload_plan.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_37d_selected_group_row_block_gpu_upload_plan.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37D.md`
- `artifacts/ASH_BASETRAIN_GPU_37D_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PLAN.json`
- `artifacts/ASH_BASETRAIN_GPU_37D_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37D_STATIC_CHECKS.json`
- `artifacts/ASH_BASETRAIN_GPU_37D_BAKE_MANIFEST.json`

## Guard

The baked archive intentionally excludes `artifacts/ASH_BASETRAIN_GPU_37C_SELECTED_GROUP_ROW_BLOCK_F32_DECODE_SMOKE.json` so a local PASS receipt is not overwritten by a static sample.

## Static checks

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-37D",
  "source_file": "crates/base_train/src/ash_basetrain_gpu_37d_selected_group_row_block_gpu_upload_plan.rs",
  "source_safetensors_file_open_call_present": false,
  "seek_call_present": false,
  "read_exact_call_present": false,
  "f32_from_le_bytes_present": false,
  "read_to_end_call_present": false,
  "mmap_runtime_call_present": true,
  "wgpu_runtime_call_present": false,
  "hex_crate_reference_present": false,
  "actual_gpu_device_request_marker_present": false,
  "actual_gpu_buffer_creation_marker_present": false,
  "actual_queue_upload_marker_present": false,
  "actual_dispatch_marker_present": false,
  "rust_if_keyword_count": 1,
  "rust_match_keyword_count": 9,
  "live_37c_receipt_same_path_included": true,
  "expected_static_verdict": "BLOCKED_37C_RECEIPT_NOT_FOUND"
}
```
