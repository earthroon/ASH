# ASH-TOK-TENSOR-11 Bake Report

## Patch

Tokenizer Tensor Adapter BaseTrain Bind Candidate / Adapter Input Route No Full Model Apply Seal

## Files

- `crates/base_train/src/config.rs`
- `crates/base_train/src/pipeline.rs`
- `crates/base_train/src/training.rs`
- `crates/model_core/src/ash_tok_tensor_11_tokenizer_tensor_adapter_basetrain_bind_candidate.rs`
- `crates/model_core/src/bin/ash_tok_tensor_11_tokenizer_tensor_adapter_basetrain_bind_candidate.rs`
- `ASH_TOK_TENSOR_11_*` receipt and contract artifacts

## Result

The adapter input route is bound as a BaseTrain candidate route only. Position alignment and feature mask requirements are explicit. No model hidden apply, full model forward, optimizer step, commit, or safetensors mutation is permitted in this patch.
