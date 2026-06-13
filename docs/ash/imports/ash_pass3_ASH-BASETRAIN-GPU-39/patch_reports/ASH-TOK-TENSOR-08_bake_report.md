# ASH-TOK-TENSOR-08 Bake Report

## Scope

Baked the grouped safetensors header/shape probe surface after ASH-TOK-TENSOR-07.

## Added

- `crates/model_core/src/ash_tok_tensor_08_grouped_safetensors_header_shape_probe.rs`
- `crates/model_core/src/bin/ash_tok_tensor_08_grouped_safetensors_header_shape_probe.rs`
- JSON receipts for header probe, tensor key/shape index, key candidates, and axis candidates

## Guarded

- No full safetensors fs::read
- No payload decode
- No tensor_to_f32_vec
- No row parity PASS claim
- No model forward / optimizer step / weight commit

## Local note

The actual safetensors artifact is external and is not packaged. Therefore this bake installs the bounded header-only probe implementation and static deferred receipts. Run the binary with `ASH_TOK_TENSOR_08_SAFETENSORS_PATH` to populate real header evidence locally.
