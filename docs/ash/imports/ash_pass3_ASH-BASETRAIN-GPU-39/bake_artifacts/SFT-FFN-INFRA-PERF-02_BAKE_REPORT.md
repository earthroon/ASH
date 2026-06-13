# SFT-FFN-INFRA-PERF-02 Bake Report

## Patch

SFT-FFN-INFRA-PERF-02 — Serialization / Hash Unification / Numeric Norm / Report Render Hygiene Seal

## Base

SFT-FFN-INFRA-PERF-01 hot path allocation hygiene baked archive.

## Added

- crates/ash_core/src/infra_numeric.rs
- crates/ash_core/src/infra_report.rs
- crates/ash_core/src/infra_perf_02.rs
- crates/ash_core/tests/sft_ffn_infra_perf_02_serialization_hash_numeric_report.rs
- crates/burn_webgpu_backend/src/ffn_infra_perf_02_hygiene.rs
- acceptance_reports/SFT-FFN-INFRA-PERF-02_serialization_hash_numeric_report_hygiene.md
- bake_artifacts/SFT-FFN-INFRA-PERF-02_BAKE_REPORT.md
- bake_artifacts/SFT-FFN-INFRA-PERF-02_STATIC_VALIDATION.txt
- bake_artifacts/SFT-FFN-INFRA-PERF-02_FILE_DIGESTS.sha256

## Modified

- crates/ash_core/src/lib.rs
- crates/ash_core/src/capability.rs
- crates/ash_core/src/atlas_sft_native_smoke_artifact_binding.rs
- crates/ash_core/src/atlas_sft_synapse_binding_candidate.rs
- crates/ash_core/src/calibration_snapshot.rs
- crates/lora_train/src/lm_head_runtime_delta_verify.rs
- crates/lora_train/src/lm_head_vocab_atlas_gpu_update.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- serde_json audit JSON renderer
- manual JSON escape removal
- hash centralization through infra_hash
- stable L2 norm helpers
- markdown report rendering boundary
- PERF-02 hygiene seal types/tests
- backend hygiene boundary shell

## Closed

- capability schema semantic change
- legacy digest rewrite
- hash algorithm replacement
- report schema rewrite
- template engine dependency
- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding

## Local Rust Verification

Not executed in this environment because cargo/rustc/rustfmt are unavailable.
