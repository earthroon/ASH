# ASH-TOK-TENSOR-36 Acceptance Report

## Scope
Decode candidate is promoted to decoded text state only. Assistant emit, user visible output commit, runtime sequence append, KV mutation, chat buffer mutation, training mutation, and safetensors mutation remain blocked.

## SSOT
- SSOT owner: `ASH_TOK_TENSOR_36_DECODE_EXECUTION_RECEIPT.json`
- Scope: `decode_candidate -> decoded_text_state`, no assistant emit, no runtime append.
- Gate mask: `banked_u64`
- Descriptor version: `2`

## Verdict
`PASS_ASH_TOK_TENSOR_36_TOKENIZER_TENSOR_ADAPTER_DECODE_EXECUTION_GATE_DECODE_CANDIDATE_NO_ASSISTANT_EMIT_NO_RUNTIME_APPEND`
