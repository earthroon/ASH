# ASH-TOK-TENSOR-35 Acceptance Report

## Scope
Selected token state is promoted to decode candidate only. Actual decode, assistant emit, user visible output commit, runtime sequence append, KV mutation, chat buffer mutation, training mutation, and safetensors mutation remain blocked.

## SSOT
- SSOT owner: `ASH_TOK_TENSOR_35_DECODE_REVIEW_RECEIPT.json`
- Scope: `selected_token_state -> decode_candidate`, no assistant emit, no runtime append.
- Gate mask: `banked_u64`
- Descriptor version: `2`

## Verdict
`PASS_ASH_TOK_TENSOR_35_TOKENIZER_TENSOR_ADAPTER_DECODE_REVIEW_GATE_SELECTED_TOKEN_STATE_NO_ASSISTANT_EMIT_NO_RUNTIME_APPEND`
