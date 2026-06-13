# ASH-BASETRAIN-GPU-37P Bake Report

## Patch

Selected Group Row-Block Parallel Reduction Diagnostic Kernel / Workgroup Arithmetic Smoke No Forward Seal

## Summary

37P adds a new base_train binary and source module that promotes the 37O single-invocation arithmetic smoke to a single-workgroup 256-sample parallel reduction smoke.

## SSOT

- Input: ASH_BASETRAIN_GPU_37O_SELECTED_GROUP_ROW_BLOCK_WINDOW_SUM_DIAGNOSTIC_KERNEL.json
- Input: ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
- Output: ASH_BASETRAIN_GPU_37P_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json

## Notes

Cargo was not available in the container, so the local operator must run the cargo command after extraction.
