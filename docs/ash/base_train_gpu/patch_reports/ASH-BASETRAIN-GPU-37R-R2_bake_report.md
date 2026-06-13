# ASH-BASETRAIN-GPU-37R-R2 Bake Report

## Result

```txt
BAKE_STATUS = COMPLETE
STATIC_CHECKS = PASS
CARGO_BUILD = NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
RUNTIME_GPU = NOT_RUN_LOCAL_GPU_REQUIRED
```

## Patch Intent

37R-R2 fixes source binding, not parity math. The prior 37R run read the 37Q-R1 receipt and computed a digest, but rejected it because the validator only accepted exact `ASH-BASETRAIN-GPU-37Q`. This patch accepts the R1 receipt as a supported upstream receipt and stops reporting unsupported patch IDs as parse failures.

## Modified Code

```txt
crates/base_train/src/bin/ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate.rs
```

## Added Artifacts

```txt
specs/ASH_BASETRAIN_GPU_37R_R2_SPEC.md
artifacts/ASH_BASETRAIN_GPU_37R_R2_BAKE_MANIFEST.json
artifacts/ASH_BASETRAIN_GPU_37R_R2_STATIC_CHECKS.json
artifacts/ASH_BASETRAIN_GPU_37R_R2_STATIC_CHECKS.txt
acceptance_reports/ASH-BASETRAIN-GPU-37R-R2.md
patch_reports/ASH-BASETRAIN-GPU-37R-R2.diff
patch_reports/ASH-BASETRAIN-GPU-37R-R2_bake_report.md
```

## No Silent Adoption

No forward, optimizer, checkpoint, or weight mutation path was opened by this patch.
