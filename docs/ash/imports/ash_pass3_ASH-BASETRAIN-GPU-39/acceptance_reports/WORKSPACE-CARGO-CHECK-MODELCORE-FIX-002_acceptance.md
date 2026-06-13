# WORKSPACE-CARGO-CHECK-MODELCORE-FIX-002 Acceptance

## Result

PATCHED_NOT_EXECUTED_IN_CONTAINER

## Confirmed Patch Scope

- Patched `crates/model_core/src/qw55a_vtc16_backend_bridge.rs` serde failure by replacing `[f32; 64]` with `Vec<f32>` and preserving the 64-value invariant through validation.
- Patched `crates/model_core/src/tokenizer_v5_embedding_lmhead_row_parity.rs` default report builder call by adding missing `runtime_vocab_size` and `now_unix_ms` arguments.
- Patched `crates/model_core/src/tokenizer_v5_local_artifact_hash_parity.rs` moved-value errors by extracting parity booleans before moving probes into the report.
- Patched `crates/model_core/src/tokenizer_v5_embedding_tensor_read_probe.rs` moved-value error by capturing `pending_reason` before moving `path_receipt` into the pending report.

## Not Executed Here

`cargo check --workspace --all-targets` was not executed in this container because cargo/rustc are not available.

## Forbidden / Preserved

- No runtime apply.
- No checkpoint write.
- No model weight mutation.
- No attention compute.
- No lm_head/logits/sampler/generation.
