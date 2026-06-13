# ASH-BASETRAIN-GPU-37A Bake Report

## Result

Baked patch files were added for 37A.

## Added files

- `crates/base_train/src/ash_basetrain_gpu_37a_selected_group_full_row_block_streaming_plan.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_37a_selected_group_full_row_block_streaming_plan.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37A.md`
- `patch_reports/ASH-BASETRAIN-GPU-37A_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_37A_SELECTED_GROUP_FULL_ROW_BLOCK_STREAMING_PLAN.json`
- `artifacts/ASH_BASETRAIN_GPU_37A_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37A_BAKE_MANIFEST.json`

## No live input overwrite

The baked zip excludes:

- `artifacts/ASH_BASETRAIN_GPU_36G_BOUNDED_ROW_VIEW_READ_SMOKE.json`

This prevents static baked BLOCK output from overwriting the user's local 36G PASS receipt.

## Runtime

The container did not provide `cargo`/`rustc`, so local build/run is deferred to the operator environment.

## Contract

37A is plan-only:

- no source safetensors open
- no seek/read
- no F32 decode
- no CPU tensor materialization
- no GPU upload
- no forward/backward/optimizer
- no mutation
