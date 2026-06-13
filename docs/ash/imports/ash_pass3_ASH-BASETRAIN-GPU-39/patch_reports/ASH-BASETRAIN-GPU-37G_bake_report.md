# ASH-BASETRAIN-GPU-37G Bake Report

## Patch

`ASH-BASETRAIN-GPU-37G` — Selected Group Row-Block GPU Upload Promotion Gate / Verified Readback Buffer To Dispatch Candidate No Forward No Backward Seal

## Files added

```txt
crates/base_train/src/ash_basetrain_gpu_37g_selected_group_row_block_gpu_upload_promotion_gate.rs
crates/base_train/src/bin/ash_basetrain_gpu_37g_selected_group_row_block_gpu_upload_promotion_gate.rs
acceptance_reports/ASH-BASETRAIN-GPU-37G.md
patch_reports/ASH-BASETRAIN-GPU-37G_bake_report.md
artifacts/ASH_BASETRAIN_GPU_37G_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PROMOTION_GATE.json
artifacts/ASH_BASETRAIN_GPU_37G_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_37G_STATIC_CHECKS.json
artifacts/ASH_BASETRAIN_GPU_37G_BAKE_MANIFEST.json
```

## Static checks

```json
{
  "source_file_open_call_present": false,
  "seek_from_start_present": false,
  "read_exact_call_present": false,
  "f32_from_le_bytes_present": false,
  "read_to_end_call_present": false,
  "mmap_runtime_call_present": false,
  "wgpu_runtime_call_present": false,
  "request_adapter_present": false,
  "request_device_present": false,
  "create_buffer_present": false,
  "queue_write_buffer_present": false,
  "copy_buffer_to_buffer_present": false,
  "map_async_present": false,
  "create_shader_module_present": false,
  "create_compute_pipeline_present": false,
  "create_bind_group_present": false,
  "dispatch_workgroups_present": false,
  "hex_crate_reference_present": false,
  "rust_if_keyword_count": 0,
  "rust_match_keyword_count": 11,
  "live_37f_receipt_same_path_included": false
}
```

## Local build/run

Not executed in this container because `cargo` is unavailable.

## Upstream receipt handling

The live 37F PASS receipt path is intentionally not included in this archive:

```txt
artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```
