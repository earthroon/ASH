# ASH-BASETRAIN-GPU-37K Bake Report

## Result

Baked static patch package for `ASH-BASETRAIN-GPU-37K`.

## Files added

- `crates/base_train/src/ash_basetrain_gpu_37k_selected_group_row_block_bound_resource_upload_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_37k_selected_group_row_block_bound_resource_upload_candidate.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37K.md`
- `patch_reports/ASH-BASETRAIN-GPU-37K_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_37K_SELECTED_GROUP_ROW_BLOCK_BOUND_RESOURCE_UPLOAD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37K_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37K_STATIC_CHECKS.json`
- `artifacts/ASH_BASETRAIN_GPU_37K_BAKE_MANIFEST.json`

## Static guard result

`STATIC_CHECK_PASS`

## Notes

The source uses JSON atlas tiled parallel sections rather than a single giant `json!` macro. No `*.sha256` files are included. Live upstream PASS receipts are not included to avoid overwriting local runtime receipts.

## Container limitation

`cargo`/`rustc` are unavailable in the bake container, so runtime build/execution is not claimed here.
