# SFT-GPU-PERF-08 Bake Report

## Patch

SFT-GPU-PERF-08 — GPU Microbatch Scheduler / Batch Packing & Occupancy Seal

## Files Added

- `crates/lora_train/src/gpu_microbatch_scheduler.rs`
- `crates/lora_train/tests/gpu_microbatch_scheduler.rs`
- `acceptance_reports/SFT-GPU-PERF-08_gpu_microbatch_scheduler_batch_packing_occupancy.md`
- `acceptance_reports/SFT-GPU-PERF-08_static_validation_result.md`
- `bake_artifacts/SFT-GPU-PERF-08_BAKE_REPORT.md`

## Files Modified

- `crates/lora_train/src/lib.rs`

## Core Contract

PERF-08 consumes a PERF-04 active token matrix and creates a deterministic GPU-only microbatch packing plan with VRAM estimates, pass1/pass2/update dispatch estimates, occupancy summary, shrink-retry policy, and strict no CPU fallback/no logits readback guards.

## Runtime Status

Native Rust tests were not executed in this container because `cargo` is unavailable. Static validation checked file presence, exports, guard strings, test names, and balanced braces.
