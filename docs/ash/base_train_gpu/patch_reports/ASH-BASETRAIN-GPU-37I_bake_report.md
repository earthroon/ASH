# ASH-BASETRAIN-GPU-37I Bake Report

## 확정
- Added 37I source and bin.
- Added atlas-tiled receipt sections, avoiding giant `serde_json::json!` macro expansion.
- Added static BLOCK artifact and static checks.
- Removed upstream 37H receipt artifact from ZIP collision path.
- `.sha256` files included: none.

## Static verdict
```json
{
  "patch_id": "ASH-BASETRAIN-GPU-37I",
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
  "create_buffer_call_present": false,
  "queue_write_buffer_present": false,
  "copy_buffer_to_buffer_present": false,
  "map_async_present": false,
  "create_bind_group_call_present": false,
  "dispatch_workgroups_present": false,
  "hex_crate_reference_present": false,
  "json_atlas_tiling_marker_present": true,
  "receipt_tile_function_count": 9,
  "receipt_digest_tile_function_count": 3,
  "rust_if_keyword_count": 0,
  "rust_match_keyword_count": 11,
  "live_37h_receipt_same_path_included": false,
  "sha256_files_in_tree": [],
  "static_verdict": "STATIC_CHECK_PASS"
}
```

## 판단불가
- Cargo build/run was not executed in this container because cargo/rustc are unavailable.
