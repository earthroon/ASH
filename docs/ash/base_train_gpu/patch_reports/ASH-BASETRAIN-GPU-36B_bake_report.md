# ASH-BASETRAIN-GPU-36B Bake Report

## Added files
- `crates/base_train/src/ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-36B.md`
- `artifacts/ASH_BASETRAIN_GPU_36B_BOUNDED_WEIGHT_SLICE_F32_WINDOW_SANITY.json`
- `artifacts/ASH_BASETRAIN_GPU_36B_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_36B_BAKE_MANIFEST.json`

## Baked static verdict
`BLOCKED_36A_RECEIPT_NOT_FOUND`

## Path isolation
Previous live input receipts are not included at these paths:

- `artifacts/ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json`
- `artifacts/ASH_BASETRAIN_GPU_36_SELECTED_GROUP_WEIGHT_SLICE_LOAD_PREFLIGHT.json`
- `artifacts/ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE.json`

## Static checks
36B Rust source was scanned for standalone `if` / `match` tokens and passed.

## Runtime boundary
36B may open the source shard and re-read the same bounded 3 windows from 36A. It may decode only those bytes as F32 samples. It must not load the full tensor, parse a safetensors header, upload to GPU, run forward/backward, create an optimizer step, or mutate weights.
