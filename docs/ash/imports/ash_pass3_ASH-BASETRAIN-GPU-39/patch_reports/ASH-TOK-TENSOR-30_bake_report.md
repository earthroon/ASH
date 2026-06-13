# ASH-TOK-TENSOR-30 Bake Report

## Applied files
- crates/model_core/src/ash_tok_tensor_30_tokenizer_tensor_adapter_logits_projection_execution_gate.rs
- crates/model_core/src/bin/ash_tok_tensor_30_tokenizer_tensor_adapter_logits_projection_execution_gate.rs
- crates/model_core/src/wgpu_review_gate_policy.rs
- crates/model_core/src/lib.rs
- crates/model_core/Cargo.toml
- crates/base_train/src/config.rs
- crates/base_train/src/pipeline.rs
- crates/base_train/src/training.rs

## Seal
`PASS_ASH_TOK_TENSOR_30_TOKENIZER_TENSOR_ADAPTER_LOGITS_PROJECTION_EXECUTION_GATE_LOGITS_CANDIDATE_NO_SAMPLING_NO_TOKEN_SELECTION`

## Closed paths
sampling=false, token_selection=false, decode=false, runtime_append=false, kv_mutation=false, loss_backward=false, optimizer_step=false, safetensors_mutation=false.
