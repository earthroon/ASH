# SFT-GPU-PERF-05 Bake Report

## Patch

SFT-GPU-PERF-05 — Batch-Parallel Vocab Tile Pass1 LogSumExp / No Per-Sample Serial Loop Seal

## Base

ash_pass3_SFT-GPU-PERF-04_batch_axis_train_plan_active_token_matrix_baked.zip

## Added / Modified Files

- crates/lora_train/src/batch_parallel_vocab_tile_pass1.rs
- crates/lora_train/tests/batch_parallel_vocab_tile_pass1.rs
- acceptance_reports/SFT-GPU-PERF-05_batch_parallel_vocab_tile_pass1_logsumexp.md
- acceptance_reports/SFT-GPU-PERF-05_static_validation_result.md
- bake_artifacts/SFT-GPU-PERF-05_BAKE_REPORT.md
- crates/lora_train/src/lib.rs

## Implemented Contract

- Consumes PERF-04 BatchAxisTrainPlan artifacts.
- Builds a pass1 plan with active_token x vocab_tile dispatch records.
- Preserves microbatch ranges and original active token order.
- Creates per-active-token max_logit/logsumexp/target_logit descriptors.
- Rejects per-sample serial loop, per-token serial dispatch, full logits buffer, logits readback, and CPU fallback flags.
- Requires tail tile GPU dispatch when the vocab size is not divisible by tile size.
- Exports module through lora_train crate root for PERF-06 consumption.

## Native Test Status

`cargo test -p lora_train --test batch_parallel_vocab_tile_pass1 -- --nocapture` was attempted, but cargo/rustc is unavailable in this container.

## Result

PASS_STATIC / PENDING_NATIVE_TEST
