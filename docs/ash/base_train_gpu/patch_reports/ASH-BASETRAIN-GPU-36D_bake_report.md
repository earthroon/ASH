# ASH-BASETRAIN-GPU-36D Bake Report

## Result

Baked.

## Added Files

- `crates/base_train/src/ash_basetrain_gpu_36d_bounded_weight_slice_row_sample_continuity_probe.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_36d_bounded_weight_slice_row_sample_continuity_probe.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-36D.md`
- `patch_reports/ASH-BASETRAIN-GPU-36D_bake_report.md`
- `artifacts/ASH_BASETRAIN_GPU_36D_BOUNDED_WEIGHT_SLICE_ROW_SAMPLE_CONTINUITY_PROBE.json`
- `artifacts/ASH_BASETRAIN_GPU_36D_STATIC_CHECKS.txt`
- `artifacts/ASH_BASETRAIN_GPU_36D_BAKE_MANIFEST.json`

## Baked Static Verdict

`BLOCKED_36C_RECEIPT_NOT_FOUND`

The static artifact is a sealed no-input result. Local PASS requires an explicit 36C PASS receipt.

## Important Implementation Note

36C currently preserves row contract and row alignment, but not `source_shard_path` inline. 36D resolves the source shard by following the 36C-bound upstream 36B receipt path and verifying the 36B receipt digest before reading `read_plan_ref.source_shard_path`.

This is source-chain binding, not invented path recovery.

## Runtime Scope

36D may open the source safetensors file and read only adjacent bounded windows totaling at most 12288 bytes. It must not read the full tensor or upload to GPU.

## Build Status

Cargo build was not executed in the bake container because `cargo/rustc` is unavailable here.
