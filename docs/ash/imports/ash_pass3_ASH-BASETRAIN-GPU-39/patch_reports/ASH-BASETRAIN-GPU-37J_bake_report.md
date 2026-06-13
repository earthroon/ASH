# ASH-BASETRAIN-GPU-37J Bake Report

## 확정

- Added `crates/base_train/src/ash_basetrain_gpu_37j_selected_group_row_block_bind_group_candidate.rs`.
- Added `crates/base_train/src/bin/ash_basetrain_gpu_37j_selected_group_row_block_bind_group_candidate.rs`.
- Added 37J static receipt, static checks, bake manifest, and acceptance report.
- Removed upstream static input receipt from this ZIP target: `artifacts/ASH_BASETRAIN_GPU_37I_SELECTED_GROUP_ROW_BLOCK_COMPUTE_PIPELINE_CANDIDATE.json`.
- No `*.sha256` files included.

## Static check result

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-37J",
  "static_check_status": "STATIC_CHECK_PASS",
  "json_atlas_tiling_marker_present": true,
  "receipt_tile_function_count": 9,
  "receipt_digest_tile_function_count": 3,
  "source_file_open_call_present": false,
  "seek_from_start_present": false,
  "read_exact_call_present": false,
  "f32_from_le_bytes_present": false,
  "read_to_end_call_present": false,
  "mmap_runtime_call_present": false,
  "request_adapter_present": true,
  "request_device_present": true,
  "create_shader_module_present": true,
  "create_bind_group_layout_present": true,
  "create_pipeline_layout_present": true,
  "create_compute_pipeline_present": true,
  "create_buffer_call_present": true,
  "actual_create_bind_group_call_present": true,
  "create_bind_group_layout_only_not_counted_as_actual_bind_group": true,
  "queue_write_buffer_present": false,
  "copy_buffer_to_buffer_present": false,
  "map_async_present": false,
  "dispatch_workgroups_present": false,
  "hex_crate_reference_present": false,
  "rust_if_keyword_count": 0,
  "rust_match_keyword_count": 11,
  "live_37i_receipt_same_path_included": false,
  "sha256_files_in_tree": [],
  "required_static_expectations": {
    "source_file_open_call_present": false,
    "read_exact_call_present": false,
    "f32_from_le_bytes_present": false,
    "read_to_end_call_present": false,
    "mmap_runtime_call_present": false,
    "request_adapter_present": true,
    "request_device_present": true,
    "create_shader_module_present": true,
    "create_bind_group_layout_present": true,
    "create_pipeline_layout_present": true,
    "create_compute_pipeline_present": true,
    "create_buffer_call_present": true,
    "actual_create_bind_group_call_present": true,
    "queue_write_buffer_present": false,
    "copy_buffer_to_buffer_present": false,
    "map_async_present": false,
    "dispatch_workgroups_present": false,
    "hex_crate_reference_present": false,
    "live_37i_receipt_same_path_included": false
  },
  "required_static_expectations_pass": true
}
```

## 판단불가

This container does not provide cargo/rustc, so actual build/run remains local-run required.
