# SFT-GPU-PERF-12 Bake Report

## Patch

SFT-GPU-PERF-12 — Real Batch-Parallel Multi-Step Train Run / No Serial Batch Fallback Seal

## Base

Baked on top of `ash_pass3_SFT-GPU-PERF-11_cpu_gpu_batch_parallel_regression_loss_grad_parity_baked.zip`.

## Implemented

- Added `real_batch_parallel_train_run.rs`.
- Added `RealBatchParallelTrainRunInput`.
- Added `RealBatchParallelTrainStepReceipt`.
- Added `RealBatchParallelArtifactReceipt`.
- Added `RealBatchParallelTrainRunReceipt`.
- Added `RealBatchParallelTrainRunDecision`.
- Added `RealBatchParallelTrainRunError`.
- Added `build_real_batch_parallel_train_run_receipt(...)`.
- Added acceptance tests.
- Updated `crates/lora_train/src/lib.rs` with module export and public re-exports.

## Guarded Behaviors

- `effective_batch_size > 1` is required when configured.
- completed multi-step run is required.
- PERF-11 parity receipt evidence is required.
- every step must carry PERF-04 through PERF-10 receipt evidence plus PERF-03A warm-step evidence.
- step 2+ requires nonzero A delta and nonzero grad_lora_mid.
- B delta must be nonzero.
- finite loss/grad/delta required.
- final adapter artifact must be created, nonempty, finite, and fingerprinted.
- serial batch fallback, per-sample loop, per-token dispatch, CPU fallback, full logits, logits readback, synthetic delta, and loss clamp are rejected.

## Native Test Status

Not executed in this container because `cargo` / `rustc` were unavailable.

## Result

Baked artifact created with static validation report.
