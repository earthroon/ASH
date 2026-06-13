# ASH-BASETRAIN-GPU-37P-R1 Bake Report

## Status

```txt
PASS_STATIC_BAKE_CHECKS
```

## Scope

37P-R1 rebinds 37P to explicit/default 37O runtime PASS receipt intake, splits 37F payload receipt/source failures away from 37O locator failures, and routes the 37P bin through runtime artifact write.

## Implemented

- `PATCH_ID` advanced to `ASH-BASETRAIN-GPU-37P-R1` while preserving `base_patch_id = ASH-BASETRAIN-GPU-37P`.
- Added `--window-sum-receipt` with legacy `--window-sum-diagnostic-receipt` fallback.
- Added default 37O runtime receipt path: `artifacts/ASH_BASETRAIN_GPU_37O_SELECTED_GROUP_ROW_BLOCK_WINDOW_SUM_DIAGNOSTIC_KERNEL.json`.
- Added default 37F runtime receipt path: `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`.
- Added 37O wrong artifact kind guard for `BAKE_MANIFEST` and `STATIC_CHECKS` inputs.
- Split 37O read/parse/not-pass/schema/wrong-kind status codes.
- Split 37F receipt/source/schema/read status codes.
- Changed run flow to validate 37O before checking 37F, preventing missing 37F from being reported as missing 37O.
- Added `artifact_write` receipt section.
- Added `write_default_artifact()` and changed the 37P bin to write both R1 and legacy runtime receipt paths.
- Preserved no forward/no optimizer/no weight mutation guard fields.

## Verification

Cargo verification was not run because `cargo` is unavailable in this container. Static bake checks passed by source inspection.

## Runtime Contract

Local GPU runtime still must execute:

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37p_selected_group_row_block_parallel_reduction_diagnostic_kernel
cargo run -p base_train --bin ash_basetrain_gpu_37p_selected_group_row_block_parallel_reduction_diagnostic_kernel -- --window-sum-receipt .\artifacts\ASH_BASETRAIN_GPU_37O_SELECTED_GROUP_ROW_BLOCK_WINDOW_SUM_DIAGNOSTIC_KERNEL.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## Next

If 37P-R1 writes PASS runtime receipt, continue to:

```txt
ASH-BASETRAIN-GPU-37Q-R1
Parallel Reduction Receipt Source Rebind /
37P PASS Receipt Locator No Placeholder Intake Seal
No Forward No Optimizer No Weight Mutation
```
