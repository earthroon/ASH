# ASH-BASETRAIN-GPU-37N Bake Report

## Summary

Baked 37N as a progressive multi-word diagnostic kernel patch. The patch expands the 37M stable single-word diagnostic dispatch path into an 8-sample payload window readback check.

## Files Added

- `crates/base_train/src/ash_basetrain_gpu_37n_selected_group_row_block_multi_word_diagnostic_kernel.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_37n_selected_group_row_block_multi_word_diagnostic_kernel.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37N.md`
- `patch_reports/ASH-BASETRAIN-GPU-37N_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_37N_SELECTED_GROUP_ROW_BLOCK_MULTI_WORD_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37N_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37N_STATIC_CHECKS.json`
- `artifacts/ASH_BASETRAIN_GPU_37N_BAKE_MANIFEST.json`

## SSOT Boundary

Input SSOT is external/local:

- 37M PASS receipt: `ASH_BASETRAIN_GPU_37M_SELECTED_GROUP_ROW_BLOCK_DIAGNOSTIC_DISPATCH_REGRESSION.json`
- 37F PASS receipt: `ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

Those live upstream receipts are not included in this ZIP to avoid overwriting operator-local PASS artifacts.

## Static Guard Notes

- `dispatch_workgroups` is intentionally present and allowed.
- `copy_buffer_to_buffer` and `map_async` are intentionally present and allowed.
- `read_to_end` is absent.
- runtime mmap materialization is absent.
- `f32::from_le_bytes` is absent; comparison is raw `u32::from_le_bytes` bitcast style.
- no `*.sha256` files are included.

## Cargo Build

Cargo/rustc were unavailable in this container, so runtime build/run is operator-side.
