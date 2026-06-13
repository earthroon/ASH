# SFT-GPU-PERF-07 Bake Report

## Baked Patch

SFT-GPU-PERF-07 — Batch-Reduced LoRA A/B Update / Cross-Batch AdamW Seal

## Files Added / Modified

- `crates/lora_train/src/batch_reduced_lora_ab_update.rs`
- `crates/lora_train/tests/batch_reduced_lora_ab_update.rs`
- `acceptance_reports/SFT-GPU-PERF-07_batch_reduced_lora_ab_update_cross_batch_adamw.md`
- `acceptance_reports/SFT-GPU-PERF-07_static_validation_result.md`
- `bake_artifacts/SFT-GPU-PERF-07_BAKE_REPORT.md`
- `crates/lora_train/src/lib.rs`

## Contract

PERF-07 consumes PERF-06 grad shard evidence and emits a batch-reduced LoRA A/B update plan plus receipt. It binds the update to the PERF-03A warm-step gate so that first-step zero A delta is allowed only for explicit B-zero-init with nonzero B delta, while step 2+ requires nonzero grad_lora_mid and nonzero A delta.

## Mutation Boundary

This patch creates an update receipt model and test coverage. It does not introduce CPU fallback, synthetic delta, delta clamp, full logits buffer, or logits readback paths.

## Runtime Status

`cargo` is unavailable in this container, so native Rust tests were not executed here. Static file/export/guard checks are recorded in `SFT-GPU-PERF-07_static_validation_result.md`.
