# ASH-BASETRAIN-GPU-36C Bake Report

## Summary

Added ASH-BASETRAIN-GPU-36C as a receipt-only row alignment probe. The patch consumes the ASH-BASETRAIN-GPU-36B bounded F32 window sanity receipt and computes row stride plus first/middle/last window row alignment without opening the safetensors file.

## Added files

- `crates/base_train/src/ash_basetrain_gpu_36c_bounded_weight_slice_row_alignment_probe.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_36c_bounded_weight_slice_row_alignment_probe.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-36C.md`
- `patch_reports/ASH-BASETRAIN-GPU-36C_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_36C_BOUNDED_WEIGHT_SLICE_ROW_ALIGNMENT_PROBE.json`
- `artifacts/ASH_BASETRAIN_GPU_36C_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_36C_BAKE_MANIFEST.json`

## Guard preservation

- `file_open_used = false`
- `bounded_window_re_read_executed = false`
- `selected_group_full_slice_read = false`
- `selected_group_weight_bytes_read = false`
- `full_tensor_load_executed = false`
- `full_tensor_stats_generated = false`
- `safetensors_header_read_executed = false`
- `runtime_gpu_buffer_created = false`
- `gpu_upload_executed = false`
- `forward_executed = false`
- `selected_group_backward_executed = false`
- `optimizer_step_executed = false`
- `safetensors_mutation_present = false`

## Path isolation

This ZIP does not include the live input receipt path for ASH-BASETRAIN-GPU-36B, so extracting the bake should not overwrite local PASS receipts.

## Build note

The bake environment does not include `cargo` or `rustc`; cargo build must be verified locally.
