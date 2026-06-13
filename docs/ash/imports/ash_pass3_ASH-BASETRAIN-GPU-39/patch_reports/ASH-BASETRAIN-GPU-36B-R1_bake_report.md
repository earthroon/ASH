# ASH-BASETRAIN-GPU-36B-R1 Bake Report

## Patch
ASH-BASETRAIN-GPU-36B-R1

## Title
Local Hex Encoder Buildfix / Remove Unlinked Hex Crate Dependency No Logic Change Seal

## Changed files
- `crates/base_train/src/ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-36B-R1.md`
- `patch_reports/ASH-BASETRAIN-GPU-36B-R1_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_36B_R1_LOCAL_HEX_ENCODER_BUILDFIX_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_36B_R1_LOCAL_HEX_ENCODER_BUILDFIX_BAKE_MANIFEST.json`

## Buildfix
Replaced:

```rust
hex::encode(hasher.finalize())
```

with a local lower-hex encoder using a fixed lookup table.

## Dependency policy
No new dependency was added. `Cargo.toml` was not changed.

## Logic policy
No 36B bounded read, F32 stats, receipt schema, or guard logic was intentionally changed.

## Path isolation
Previous live input receipts are not included at these paths:

- `artifacts/ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json`
- `artifacts/ASH_BASETRAIN_GPU_36_SELECTED_GROUP_WEIGHT_SLICE_LOAD_PREFLIGHT.json`
- `artifacts/ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE.json`

## Static checks
- `hex::encode` removed from 36B Rust source.
- `use hex` absent.
- `extern crate hex` absent.
- Local lookup table encoder present.
