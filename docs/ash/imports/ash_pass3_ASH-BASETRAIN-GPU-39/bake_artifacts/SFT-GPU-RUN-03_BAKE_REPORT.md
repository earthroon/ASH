# SFT-GPU-RUN-03 Bake Report

## Commit

SFT-GPU-RUN-03 — GPU Train Regression Matrix / Multi-Step Loss Direction Seal

## Base

Baked on top of `ash_pass3_SFT-GPU-RUN-02_artifact_intake_registry_binding_baked.zip`.

## Added

- `crates/ash_core/src/sft_gpu_train_regression_matrix.rs`
- `crates/ash_core/tests/sft_gpu_run_03_regression_matrix.rs`
- `crates/lora_train/src/gpu_train_regression_matrix.rs`
- `crates/lora_train/tests/gpu_train_regression_matrix.rs`
- `crates/burn_webgpu_backend/src/gpu_train_regression_receipt.rs`
- `crates/burn_webgpu_backend/tests/gpu_train_regression_receipt.rs`
- `acceptance_reports/SFT-GPU-RUN-03_gpu_train_regression_matrix.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- strict GPU train regression matrix
- fixture / seed / step matrix evidence
- per-fixture native GPU receipt
- no CPU fallback matrix guard
- loss direction matrix
- adapter delta stability matrix
- artifact parity matrix

## Closed

- CPU fallback
- CPU materialized train path
- silent backend demotion
- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding

## Notes

Runtime GPU execution is not performed in this environment. This bake adds static SSOT, validation types, fail-closed guards, and tests. Actual strict GPU matrix execution remains pending on the target machine.
