# ASH-TOK-TENSOR-36 Bake Report

## Files Added
- `crates/model_core/src/ash_tok_tensor_36_tokenizer_tensor_adapter_decode_execution_gate.rs`
- `crates/model_core/src/bin/ash_tok_tensor_36_tokenizer_tensor_adapter_decode_execution_gate.rs`
- `ASH_TOK_TENSOR_36_DECODE_EXECUTION_RECEIPT.json`
- `ASH_TOK_TENSOR_36_DECODE_CANDIDATE_INPUT_CONTRACT.json`
- `ASH_TOK_TENSOR_36_NO_ASSISTANT_EMIT_NO_RUNTIME_APPEND_CONTRACT.json`
- `ASH_TOK_TENSOR_36_GATE_MASK_BANK_BIND_CONTRACT.json`
- `ASH_TOK_TENSOR_36_WGPU_GATE_POLICY_BIND_CONTRACT.json`
- `ASH_TOK_TENSOR_36_STATIC_CHECKS.txt`

## Guarded Closed Paths
- assistant emit
- user visible output commit
- runtime sequence append
- KV cache mutation
- chat buffer mutation
- loss/backward/optimizer/weight commit
- safetensors mutation

## Verdict
`PASS_ASH_TOK_TENSOR_36_TOKENIZER_TENSOR_ADAPTER_DECODE_EXECUTION_GATE_DECODE_CANDIDATE_NO_ASSISTANT_EMIT_NO_RUNTIME_APPEND`
