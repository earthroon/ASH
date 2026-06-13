# SFT-GPU-PERF-06 Bake Report

## Added files

- `crates/lora_train/src/batch_parallel_vocab_tile_pass2_grad.rs`
- `crates/lora_train/tests/batch_parallel_vocab_tile_pass2_grad.rs`
- `acceptance_reports/SFT-GPU-PERF-06_batch_parallel_vocab_tile_pass2_gradient_token_block_reduce.md`
- `acceptance_reports/SFT-GPU-PERF-06_static_validation_result.md`

## Modified files

- `crates/lora_train/src/lib.rs`

## Baked contract

PERF-06 consumes the PERF-04 batch-axis train plan and PERF-05 batch-parallel pass1 receipt, then creates a pass2 gradient plan with:

- active_token x vocab_tile dispatch records
- GPU-side token-block reduce descriptors
- grad_B tile shard descriptors
- grad_lora_mid token block descriptors
- grad_A partial descriptors
- target subtraction and mean loss normalization guards
- no CPU grad accumulation / no full logits / no logits readback / no CPU fallback guards

## Runtime status

Native Rust tests were not executed in this container because `cargo`/`rustc` are unavailable. Static validation was performed and recorded separately.
