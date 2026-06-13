# MODELCORE-COMPILE-06 — NativeWgpuModel Accessor / Extension Boundary Seal

## Purpose

Seal `NativeWgpuModel` internal state behind narrow crate-internal accessors and gateway methods.

`decode_state.rs` and `generation_sampling.rs` should not directly access private fields such as `model`, `device`, `gpu_sampling_runtime`, `runtime_handles`, `structure_routing_state`, `active_penalty_coeffs`, or `gpu_penalty_runtime`.

## Changed Files

- `crates/model_core/src/native_wgpu.rs`
- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/generation_sampling.rs`

## Added Accessors / Gateways

- `device_for_generation`
- `has_gpu_sampling_runtime_handles`
- `gpu_sampling_runtime_ref`
- `gpu_penalty_runtime_ref`
- `active_penalty_coeffs_ref`
- `decode_layer_kv_specs`
- `decode_layers`
- `embed_tokens_for_decode`
- `final_norm_for_decode`
- `forward_logits_for_generation`
- `lm_head_vocab_size`
- `project_last_hidden_to_logits`
- `try_dispatch_adjusted_logits_raw_lease_for_sampling`
- `apply_gpu_penalty_cpu_row_for_sampling`
- `sample_from_structure_rerank_subset_for_sampling`
- `apply_structure_rerank_subset_with_telemetry_for_sampling`
- `apply_structure_rerank_cpu_row_with_telemetry_for_sampling`
- `gpu_penalty_routing_scalar_for_sampling`

## Visibility Adjustments

Selected methods were promoted to `pub(crate)` only where they represent a command/query boundary rather than raw state exposure:

- `active_attached_loras`
- `current_adapter_gate_telemetry`
- `resolve_sampling_with_structure_prior`
- `text_density_repetition_window`
- `text_density_repetition_penalty`
- `should_use_kv_cache_router`
- `should_use_gpu_argmax_router`
- `try_grouped_query_attention_via_atlas`
- `cat_seq_dim_4`
- `slice_last_logits_row`
- `slice_last_hidden_row`
- `should_materialize_cpu_last_row`
- `apply_logit_postprocessors`
- `select_next_token_with_sampling`
- `select_next_token`

## Non-Goals

- No `runtime_lora` schema repair.
- No `execution_path` repair.
- No `grouped_query_attention` repair.
- No module tree migration.
- No config changes.
- No public field exposure.

## Prohibited Shortcuts Avoided

- Did not make `model` public.
- Did not make `device` public.
- Did not make `gpu_sampling_runtime` public.
- Did not make `runtime_handles` public.
- Did not make `structure_routing_state` public.
- Did not make `active_penalty_coeffs` public.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_06_check.log"
```

Expected reduced patterns:

```text
field `model` of struct `NativeWgpuModel` is private
field `device` of struct `NativeWgpuModel` is private
field `gpu_sampling_runtime` of struct `NativeWgpuModel` is private
field `runtime_handles` of struct `NativeWgpuModel` is private
field `structure_routing_state` of struct `NativeWgpuModel` is private
field `active_penalty_coeffs` of struct `NativeWgpuModel` is private
```

Allowed remaining patterns:

```text
grouped_query_attention exists but is inaccessible
runtime_lora schema drift
execution_path missing
prefill/decode_step cross-module private access
Result/type inference residuals
ownership/borrow drift
```
