# ASH-BASETRAIN-GPU-21 Bake Report

## Patch

`ASH-BASETRAIN-GPU-21 Local Window Loss Smoke / Fixed Target 1 Over Window 2048 Logits Candidate No Backward No Optimizer Seal`

## Files Added

- `crates/base_train/src/ash_basetrain_gpu_21_local_window_loss_smoke.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_21_local_window_loss_smoke.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-21.md`
- `patch_reports/ASH-BASETRAIN-GPU-21_bake_report.md`

## Contract

This bake intentionally requires an explicit raw logits payload. The previous receipts contained digest and sample evidence, not the complete 8192-byte logits payload. Therefore this implementation refuses to claim `loss_scalar_created = true` unless the payload file is supplied and digest-matched.

## Required Runtime Env

`ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH=<path-to-8192-byte-f32-le-logits>`

## Closed Boundaries

- no new WGPU device
- no new dispatch
- no new readback
- no full-vocab loss
- no dataset/training label claim
- no backward
- no optimizer
- no safetensors mutation
