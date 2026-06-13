# ASH-TOK-TENSOR-09 Acceptance Report

## Title

Grouped Embedding LMHead Row Parity Probe / Header-Resolved Key Only No Full Tensor Load Seal

## PASS

```txt
PASS_ASH_TOK_TENSOR_09_GROUPED_EMBEDDING_LMHEAD_ROW_PARITY_PROBE_HEADER_RESOLVED_KEY_ONLY_NO_FULL_TENSOR_LOAD
```

## Scope

Header-resolved embedding/lm_head vocab-axis row parity probe only. This patch does not decode tensor payload, does not load full tensors, does not run model forward, and does not claim row value parity.

## Sealed true

- header_resolved_key_only
- embedding_vocab_axis_parity_checked
- lm_head_vocab_axis_parity_checked

## Sealed false

- row_value_parity_checked
- tensor_payload_decoded
- full_tensor_load_executed
- tensor_to_f32_vec_executed
- full_embedding_materialized
- full_lm_head_materialized
- model_forward_executed
- optimizer_step_executed
- weight_commit_executed
- safetensors_mutation
- checkpoint_finalization_executed

## Degraded evidence state

The external safetensors asset is not packaged in this bake by SSOT. Actual embedding/lm_head keys, shapes, hidden_dim, and lm_head orientation remain deferred until the local external header probe is run.
