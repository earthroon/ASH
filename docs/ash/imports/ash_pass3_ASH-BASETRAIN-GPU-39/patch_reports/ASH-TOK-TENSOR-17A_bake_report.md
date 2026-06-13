# ASH-TOK-TENSOR-17A Bake Report

## Base

`ASH-TOK-TENSOR-16` baked ZIP.

## Added

- `crates/model_core/src/wgpu_review_gate_policy.rs`
- `crates/model_core/src/wgpu_review_gate_receipt.rs`
- `crates/model_core/src/wgpu_review_gate_runtime.rs`
- `crates/model_core/src/shaders/ash_tok_tensor_17a_gate_mask_reduce.wgsl`
- `crates/model_core/src/shaders/ash_tok_tensor_17a_token_bounds_review.wgsl`
- `crates/model_core/src/shaders/ash_tok_tensor_17a_logits_selection_review.wgsl`
- `crates/model_core/src/ash_tok_tensor_17a_wgpu_review_gate_kernelization.rs`
- `crates/model_core/src/bin/ash_tok_tensor_17a_wgpu_review_gate_kernelization.rs`
- static JSON/receipt/check artifacts.

## Seal

No assistant emit. No runtime append. No KV mutation. No loss backward. No optimizer. No weight commit.
