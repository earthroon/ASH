# ASH-TOK-TENSOR-32 Bake Report

Baked from `ASH-TOK-TENSOR-31` work tree.

## Changed Files

- `crates/model_core/src/ash_tok_tensor_32_tokenizer_tensor_adapter_sampling_execution_gate.rs`
- `crates/model_core/src/bin/ash_tok_tensor_32_tokenizer_tensor_adapter_sampling_execution_gate.rs`
- `crates/model_core/src/wgpu_review_gate_policy.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/Cargo.toml`
- `crates/base_train/src/config.rs`
- `crates/base_train/src/pipeline.rs`
- `crates/base_train/src/training.rs`

## Closed Paths

Token selection, selected-token state, decode, decoded text, runtime append, KV mutation, loss/backward, optimizer, weight commit, safetensors mutation, and checkpoint finalization remain blocked.

## Mask Pressure

`ALLOW_SAMPLING_EXECUTION = 1 << 60` and `ALLOW_SAMPLING_STATE = 1 << 61`; next gates should lift to a mask bank or equivalent.

## Verdict

```txt
PASS_ASH_TOK_TENSOR_32_TOKENIZER_TENSOR_ADAPTER_SAMPLING_EXECUTION_GATE_SAMPLING_CANDIDATE_NO_TOKEN_SELECTION_NO_DECODE
```
