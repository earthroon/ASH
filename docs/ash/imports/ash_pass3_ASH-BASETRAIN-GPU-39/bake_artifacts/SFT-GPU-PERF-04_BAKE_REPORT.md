# SFT-GPU-PERF-04 Bake Report

## Patch

SFT-GPU-PERF-04 — Batch Axis Train Plan / Active Token Matrix Seal

## Files Added

- `crates/lora_train/src/batch_axis_train_plan.rs`
- `crates/lora_train/tests/batch_axis_train_plan.rs`
- `acceptance_reports/SFT-GPU-PERF-04_batch_axis_train_plan_active_token_matrix.md`
- `acceptance_reports/SFT-GPU-PERF-04_static_validation_result.md`

## Files Modified

- `crates/lora_train/src/lib.rs`

## Implemented Contract

- Creates `BatchAxisTrainPlan` and `BatchAxisTrainPlanReceipt`.
- Extracts active response tokens from `response_loss_mask` and `attention_mask`.
- Preserves original `batch_index`, `token_position`, target token id, hidden row index, and hidden row offset.
- Computes target vocab tile index/start/end for each active token.
- Splits active tokens into microbatches without losing original batch indices.
- Rejects CPU per-token serial loop, full logits buffer, and logits readback flags.
- Exports the module through `lora_train` crate root for PERF-05/PERF-06 consumption.

## Non-Goals

- Does not rewrite pass1/pass2 GPU kernels yet.
- Does not perform batch-parallel dispatch yet.
- Does not modify AdamW update logic yet.

## Runtime Status

Native Rust tests were not executed in this container because `cargo` is unavailable. Static validation was performed and recorded in `SFT-GPU-PERF-04_static_validation_result.md`.
