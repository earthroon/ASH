# ASH-BASETRAIN-GPU-37E Bake Report

## Files added

- `crates/base_train/src/ash_basetrain_gpu_37e_selected_group_row_block_gpu_upload_smoke.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_37e_selected_group_row_block_gpu_upload_smoke.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37E.md`
- `patch_reports/ASH-BASETRAIN-GPU-37E_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_37E_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_SMOKE.json`
- `artifacts/ASH_BASETRAIN_GPU_37E_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37E_STATIC_CHECKS.json`
- `artifacts/ASH_BASETRAIN_GPU_37E_BAKE_MANIFEST.json`

## Boundary

This patch is the first actual representative GPU upload smoke for ASH-BASETRAIN-GPU-37. It intentionally permits:

- source shard bounded segment re-read,
- wgpu adapter/device/queue request,
- actual GPU buffer creation,
- actual `queue.write_buffer` upload.

It still forbids:

- compute shader module creation,
- compute pipeline creation,
- bind group creation,
- dispatch,
- GPU readback,
- full selected group upload,
- F32 decode rerun,
- CPU tensor view materialization,
- forward/backward/optimizer/mutation.

## Static bake status

`BLOCKED_37D_RECEIPT_NOT_FOUND` is the expected static sealed result because the live 37D PASS receipt is operator-local and was not bundled.

## Notes

No `*.sha256` files were added.
