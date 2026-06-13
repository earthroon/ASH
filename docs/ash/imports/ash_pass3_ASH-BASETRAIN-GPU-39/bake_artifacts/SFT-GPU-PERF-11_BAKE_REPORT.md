# SFT-GPU-PERF-11 Bake Report

## Patch

SFT-GPU-PERF-11 — CPU Reference vs GPU Batch-Parallel Regression / Loss+Grad Parity Seal

## Base

`ash_pass3_SFT-GPU-PERF-10_vocab_tail_shape_compile_cache_pass2_dispatch_latency_baked.zip`

## Added / Modified

- `crates/lora_train/src/cpu_gpu_batch_parallel_regression.rs`
- `crates/lora_train/tests/cpu_gpu_batch_parallel_regression.rs`
- `acceptance_reports/SFT-GPU-PERF-11_cpu_gpu_batch_parallel_regression_loss_grad_parity.md`
- `acceptance_reports/SFT-GPU-PERF-11_static_validation_result.md`
- `bake_artifacts/SFT-GPU-PERF-11_BAKE_REPORT.md`
- `crates/lora_train/src/lib.rs`

## Contract

This patch consumes CPU reference and GPU batch-parallel result summaries and emits a deterministic regression receipt only when required parity metrics pass within the configured tolerance profile.

## Hard Guards

- batch size > 1 when required
- active token order match
- finite CPU/GPU results
- loss parity
- per-token logprob parity
- pass1 max/logsumexp parity
- grad_B / grad_lora_mid / grad_A parity
- A/B delta parity
- AdamW state parity
- no CPU fallback
- no full logits buffer
- no logits readback

## Runtime Status

Static validation only in this container. Native Rust execution remains pending due to missing cargo/rustc.
