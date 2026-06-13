# SFT-GPU-PERF-11 Static Validation Result

## Scope

Static validation for SFT-GPU-PERF-11 CPU Reference vs GPU Batch-Parallel Regression / Loss+Grad Parity Seal.

## Files Checked

- `crates/lora_train/src/cpu_gpu_batch_parallel_regression.rs`
- `crates/lora_train/tests/cpu_gpu_batch_parallel_regression.rs`
- `acceptance_reports/SFT-GPU-PERF-11_cpu_gpu_batch_parallel_regression_loss_grad_parity.md`
- `crates/lora_train/src/lib.rs`

## Static Checks

- module file exists
- test file exists
- acceptance report exists
- `lib.rs` module export exists
- public re-exports exist
- source contains CPU/GPU parity receipt
- source contains tolerance profile
- source contains metric result structs
- source rejects CPU fallback / full logits / logits readback
- source rejects batch size one when configured
- source rejects active token order mismatch
- source rejects loss / pass1 / grad / delta / AdamW parity failures
- test file contains 10 acceptance tests
- brace balance checked by static scanner

## Native Rust Test Status

`cargo` was not available in this container, so native Rust tests were not executed here.

## Result

PASS_STATIC
PENDING_NATIVE_TESTS
