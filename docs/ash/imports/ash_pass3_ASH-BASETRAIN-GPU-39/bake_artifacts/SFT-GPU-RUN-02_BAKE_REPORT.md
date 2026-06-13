# SFT-GPU-RUN-02 Bake Report

## Commit

SFT-GPU-RUN-02 — Strict GPU Train Artifact Intake / Adapter Registry Binding Seal

## Base

SFT-GPU-RUN-01 strict native GPU LoRA train run baked package.

## Added

- `crates/ash_core/src/sft_gpu_artifact_intake.rs`
- `crates/ash_core/tests/sft_gpu_run_02_artifact_intake.rs`
- `crates/lora_train/src/strict_gpu_artifact_intake.rs`
- `crates/lora_train/tests/strict_gpu_artifact_intake.rs`
- `crates/burn_webgpu_backend/src/strict_gpu_artifact_registry.rs`
- `crates/burn_webgpu_backend/tests/strict_gpu_artifact_registry.rs`
- `acceptance_reports/SFT-GPU-RUN-02_artifact_intake_registry_binding.md`
- `bake_artifacts/SFT-GPU-RUN-02_BAKE_REPORT.md`
- `bake_artifacts/SFT-GPU-RUN-02_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-GPU-RUN-02_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- strict GPU train artifact intake
- artifact digest verification
- adapter registry append-only intake
- registry candidate binding
- promotion eligibility mark
- duplicate artifact guard

## Closed

- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- CPU fallback source
- CPU materialized source

## Notes

This bake intakes artifacts produced by RUN-01 as registry candidates. It does not promote, attach, switch current pointers, mutate lifecycle state, or bind ASH current state.
