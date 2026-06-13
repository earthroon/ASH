# ASH-BASETRAIN-GPU-37M Bake Report

## Result

Baked.

## Added Files

```txt
crates/base_train/src/ash_basetrain_gpu_37m_selected_group_row_block_diagnostic_dispatch_regression.rs
crates/base_train/src/bin/ash_basetrain_gpu_37m_selected_group_row_block_diagnostic_dispatch_regression.rs
acceptance_reports/ASH-BASETRAIN-GPU-37M.md
patch_reports/ASH-BASETRAIN-GPU-37M_bake_report.md
artifacts/ASH_BASETRAIN_GPU_37M_SELECTED_GROUP_ROW_BLOCK_DIAGNOSTIC_DISPATCH_REGRESSION.json
artifacts/ASH_BASETRAIN_GPU_37M_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_37M_STATIC_CHECKS.json
artifacts/ASH_BASETRAIN_GPU_37M_BAKE_MANIFEST.json
```

## Runtime Contract

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37m_selected_group_row_block_diagnostic_dispatch_regression -- --dispatch-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37L_SELECTED_GROUP_ROW_BLOCK_DISPATCH_SMOKE.json --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json --repeat-count 8
```

## Guard Notes

- Upstream live receipts are not packaged at their canonical runtime paths.
- No `.sha256` files are included.
- 37M uses JSON atlas tiled receipt layout.
- Forward/backward/optimizer/mutation remain sealed.
