# ASH-BASETRAIN-GPU-36G Bake Report

## Result

Baked from 36F ZIP with a new bounded row view read smoke runner.

## Added implementation

- crates/base_train/src/ash_basetrain_gpu_36g_bounded_row_view_read_smoke.rs
- crates/base_train/src/bin/ash_basetrain_gpu_36g_bounded_row_view_read_smoke.rs

## Static receipt

- artifacts/ASH_BASETRAIN_GPU_36G_BOUNDED_ROW_VIEW_READ_SMOKE.json
- static status: BLOCKED_36F_RECEIPT_NOT_FOUND

## Important boundary

The 36F live input receipt path was removed from the baked ZIP:

```txt
artifacts/ASH_BASETRAIN_GPU_36F_CPU_TENSOR_VIEW_CANDIDATE_MATERIALIZATION_PREFLIGHT.json
```

This prevents stale/static 36F output from overwriting the operator's local PASS receipt.

## Runtime behavior on PASS

- Opens `source_shard_path` from the validated 36F candidate_ref.
- Seeks to each planned row view offset.
- Reads exactly 3 rows * 8192 bytes = 24576 bytes.
- Generates per-row byte SHA256 digests.
- Does not decode F32.
- Does not materialize CPU tensor view.
- Does not upload to GPU.

## Static checks

```txt
ASH-BASETRAIN-GPU-36G STATIC CHECKS
patch_id=ASH-BASETRAIN-GPU-36G
source_sha256=db6407e756609c48dcc342fa6f0f5363a3074f8970961c8988b2104c6b81d7bc
bin_sha256=cfe3b6cb95217d937fed229fa780f43409e16aef4de3b09802e6047c64a7ac6b
static_receipt_sha256=8522174f88e5bdb0fc8003109bdf7cdb2e8d0ae84200ac03c408157e42e4b780
hex_crate_reference_present=false
source_safetensors_file_open_call_present=true
seek_call_present=true
read_exact_call_present=true
read_to_end_call_present=false
mmap_runtime_call_present=false
wgpu_runtime_call_present=false
match_keyword_present=true
if_keyword_count=0
bounded_row_view_read_smoke=true
limited_full_row_bytes_only=true
planned_row_read_bytes=24576
f32_decode_allowed=false
cpu_tensor_view_materialized=false
full_tensor_load_allowed=false
gpu_upload_allowed=false
live_input_36f_receipt_same_path_included=false
```

## Build note

The bake container does not provide cargo/rustc, so local cargo build/run must be performed by the operator.
