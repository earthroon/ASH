# ASH-BASETRAIN-GPU-37B Bake Report

## Result
Baked static sealed output: `BLOCKED_37A_RECEIPT_NOT_FOUND`.

## Implemented
- Added 37B source/bin runner.
- Added representative block selection for `block_000000`, `block_000094`, `block_000188_tail`.
- Added bounded read cap: `5,267,456` bytes.
- Added per-block byte SHA256 digest and combined smoke digest fields.
- Excluded live 37A receipt path from the ZIP.

## Static checks
```json
{
  "patch_id": "ASH-BASETRAIN-GPU-37B",
  "source_file": "crates/base_train/src/ash_basetrain_gpu_37b_selected_group_row_block_streaming_read_smoke.rs",
  "bin_file": "crates/base_train/src/bin/ash_basetrain_gpu_37b_selected_group_row_block_streaming_read_smoke.rs",
  "hex_crate_reference_present": false,
  "source_safetensors_file_open_call_present": true,
  "seek_call_present": true,
  "read_exact_call_present": true,
  "read_to_end_call_present": false,
  "mmap_runtime_call_present": false,
  "wgpu_guard_field_present": true,
  "wgpu_runtime_call_present": false,
  "f32_decode_marker_present": false,
  "live_37a_receipt_same_path_included": false,
  "rust_if_keyword_count": 0,
  "rust_match_keyword_count": 3,
  "selected_block_ids": [
    "block_000000",
    "block_000094",
    "block_000188_tail"
  ],
  "max_bounded_row_block_read_bytes": 5267456,
  "expected_read_bytes": {
    "block_000000": 2097152,
    "block_000094": 2097152,
    "block_000188_tail": 1073152
  },
  "logic_boundary": "bounded representative row-block byte read only; no f32 decode; no gpu upload; no full selected group read"
}
```

## Build note
Cargo/rustc were not available in this container, so local cargo build/run must be performed by operator.
