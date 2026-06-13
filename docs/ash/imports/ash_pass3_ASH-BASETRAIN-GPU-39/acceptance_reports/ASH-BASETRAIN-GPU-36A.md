# ASH-BASETRAIN-GPU-36A

## Bounded Weight Slice Read Smoke / Read Plan To Limited Byte Window Probe No Tensor Full Load No GPU Upload Seal

Static baked status: `BLOCKED_36_RECEIPT_NOT_FOUND`.

Local PASS requires:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_36a_bounded_weight_slice_read_smoke -- --read-plan-receipt .\artifacts\ASH_BASETRAIN_GPU_36_SELECTED_GROUP_WEIGHT_SLICE_LOAD_PREFLIGHT.json
```

Expected local PASS status:

```txt
PASS_ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE_READ_PLAN_TO_LIMITED_BYTE_WINDOW_PROBE_NO_TENSOR_FULL_LOAD_NO_GPU_UPLOAD
```

Guards:

- `selected_group_full_slice_read=false`
- `full_tensor_load_executed=false`
- `safetensors_header_read_executed=false`
- `gpu_upload_executed=false`
- `rust_if_keyword_used=false`
- `rust_match_keyword_used=false`

Path isolation: previous R3B/36 receipt artifact paths are not included in this bake package.
