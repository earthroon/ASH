# ASH-BASETRAIN-GPU-37R Bake Report

## Files Added

- `crates/base_train/src/bin/ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-37R.md`
- `patch_reports/ASH-BASETRAIN-GPU-37R_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_37R_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_37R_STATIC_CHECKS.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_BAKE_MANIFEST.json`

## Static Notes

- 37R is a receipt intake and parity gate bin.
- The 37Q runtime receipt bundled in the source 37Q ZIP was a container placeholder and is excluded from the final ZIP to avoid overwriting local PASS evidence.
- The 37R runtime artifact bundled in this ZIP is a `PENDING_RUNTIME` placeholder. Running the bin locally writes the real 37R receipt.
- No `.sha256` files are included.

## Runtime Notes

Cargo was not available in the container, so local build/run is required.
