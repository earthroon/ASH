# ASH-BASETRAIN-GPU-21-0 Bake Report

## Result

Baked source package created.

## Added files

```txt
crates/base_train/src/ash_basetrain_gpu_21_0_raw_logits_payload_export.rs
crates/base_train/src/bin/ash_basetrain_gpu_21_0_raw_logits_payload_export.rs
acceptance_reports/ASH-BASETRAIN-GPU-21-0.md
patch_reports/ASH-BASETRAIN-GPU-21-0_bake_report.md
ASH_BASETRAIN_GPU_HANDOFF_AFTER_21_0.md
ASH_BASETRAIN_GPU_21_0_STATIC_CHECKS.txt
ASH_BASETRAIN_GPU_21_0_LOCAL_VALIDATION.txt
ASH_BASETRAIN_GPU_21_0_OPERATOR_COMMANDS.ps1
```

## Modified files

```txt
crates/base_train/src/lib.rs
```

## Runtime boundary

This patch opens WGPU dispatch/readback replay only to materialize raw logits bytes. It does not compute loss or mutate weights.

## Local validation

`cargo` is not available in the bake environment. The generated operator commands are included for local Windows execution.
