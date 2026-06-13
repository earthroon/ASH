# ASH-BASETRAIN-GPU-17 Bake Report

## Scope

Bakes a new runtime output audit module and direct bin for 2048-window logits readback.

## Files added / changed

- crates/base_train/src/ash_basetrain_gpu_17_chunk_window_logits_expansion_output_audit.rs
- crates/base_train/src/bin/ash_basetrain_gpu_17_chunk_window_logits_expansion_output_audit.rs
- crates/base_train/Cargo.toml
- acceptance_reports/ASH-BASETRAIN-GPU-17.md
- patch_reports/ASH-BASETRAIN-GPU-17_bake_report.md
- ASH_BASETRAIN_GPU_17_STATIC_CHECKS.txt
- ASH_BASETRAIN_GPU_17_LOCAL_VALIDATION.txt
- ASH_BASETRAIN_GPU_HANDOFF_AFTER_17.md

## Runtime additions

- 2048 dispatch replay
- 8192-byte staging buffer
- copy_buffer_to_buffer to staging
- map_async readback
- f32 byte audit
- finite scan
- sample capture over 13 indices
- boundary verification
- sha256 raw byte digest

## Not opened

- Full logits claim
- Generation/decode
- Loss/backward
- Optimizer
- Weight commit
- Safetensors mutation
