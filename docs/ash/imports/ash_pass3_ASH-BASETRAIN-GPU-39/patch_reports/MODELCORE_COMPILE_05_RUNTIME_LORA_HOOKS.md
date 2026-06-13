# MODELCORE-COMPILE-05 — Model Layer Telemetry Hook Boundary

## Purpose

Introduce a narrow runtime LoRA telemetry hook boundary between `model_layers.rs` and `runtime_lora.rs`.

`model_layers.rs` emits LoRA hot-path events through `runtime_lora_hooks.rs` without owning or directly accessing runtime_lora telemetry internals.

## Changed Files

- `crates/model_core/src/lib.rs`
- `crates/model_core/src/runtime_lora.rs`
- `crates/model_core/src/runtime_lora_hooks.rs`
- `crates/model_core/src/model_layers.rs`

## Changes

- Added `runtime_lora_hooks.rs`.
- Registered `mod runtime_lora_hooks;`.
- Promoted selected runtime_lora note functions to `pub(super)`.
- Exposed crate-internal hook wrappers from `runtime_lora_hooks.rs`.
- Imported hook wrappers in `model_layers.rs`.

## Hook Surface

- `note_runtime_lora_raw_fallback`
- `note_runtime_lora_bound_slice_empty`
- `note_runtime_lora_prepared_hit`
- `note_runtime_lora_prepared_miss`
- `note_runtime_lora_prepared_set_cache_invalidation`
- `note_runtime_lora_prepared_set_cache_miss`

## Non-Goals

- No runtime_lora schema reconciliation.
- No NativeWgpuModel accessor repair.
- No decode_state repair.
- No generation_sampling repair.
- No grouped_query_attention repair.
- No config changes.
- No telemetry counter behavior changes.

## Prohibited Shortcuts Avoided

- Did not expose `runtime_lora_hot_path_stats`.
- Did not make `RuntimeLoraHotPathStatsAtomics` public.
- Did not make all runtime_lora internals `pub(crate)`.
- Did not replace event hooks with silent no-op functions.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_05_check.log"
```

Expected cleared patterns:

```text
note_runtime_lora_raw_fallback not found
note_runtime_lora_bound_slice_empty not found
note_runtime_lora_prepared_hit not found
note_runtime_lora_prepared_miss not found
note_runtime_lora_prepared_set_cache_invalidation not found
note_runtime_lora_prepared_set_cache_miss not found
exists but is inaccessible
```

Allowed remaining patterns:

```text
grouped_query_attention inaccessible
NativeWgpuModel private field/method access
runtime_lora schema drift
execution_path missing
Result/type inference residuals
ownership/borrow drift
```
