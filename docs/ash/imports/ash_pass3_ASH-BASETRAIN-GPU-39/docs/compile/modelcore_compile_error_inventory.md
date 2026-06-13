# MODELCORE-COMPILE-00 - Compile Failure Inventory Seal

## Purpose

This document records the current `model_core` compile failure state before structural repair.

This commit is documentation-only. It must not modify Rust source code.

The compile failure is owned by `crates/model_core` module-contract drift, not by tokenizer/config/dataset path resolution.

## Reproduction

```powershell
Set-Location "D:\1111113232\DUST\1\ash_pass3"
cargo check -p model_core
```

Alternative reproduction through LoRA dump:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6
```

## State Attribution

```text
state_owner = crates/model_core
ssot = cargo compile error log
reproducible = true
compile_status = failing before repair commits
```

## Error Families

### A. Runtime Splice Telemetry API Drift

Representative files:

```text
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
vendor_fork_scaffold/burn-fusion-local/src/external_alias_barrier.rs
```

Symptoms:

```text
cannot find function snapshot_runtime_splice_telemetry_summary
cannot find function with_runtime_splice_telemetry_label
```

Classification:

```text
API name/export contract mismatch.
```

Next commit:

```text
MODELCORE-COMPILE-02
```

Forbidden fix:

```text
Do not replace snapshot_* with take_*.
```

Reason:

```text
take_* may drain or reset telemetry state; snapshot_* must be read-only.
```

### B. Shared Sampling Helper Boundary Drift

Representative files:

```text
crates/model_core/src/reference_checkpoint.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/native_wgpu.rs
```

Symptoms:

```text
apply_banned_token_mask exists but is inaccessible
apply_repetition_penalty exists but is inaccessible
has_repeating_suffix exists but is inaccessible
has_repeating_ngram exists but is inaccessible
StreamingTextHoldback exists but is inaccessible
max_stop_holdback_chars exists but is inaccessible
check_generation_cancel exists but is inaccessible
append_token_piece_to_text exists but is inaccessible
detect_stop_hit exists but is inaccessible
```

Classification:

```text
Pure sampling helpers are owned by feature modules instead of a shared helper boundary.
```

Next commit:

```text
MODELCORE-COMPILE-03
```

Forbidden fix:

```text
Do not blindly make native_wgpu.rs or generation_sampling.rs helpers pub(crate).
```

### C. Reference Checkpoint Math Helper Boundary Drift

Representative files:

```text
crates/model_core/src/reference_checkpoint.rs
crates/model_core/src/native_wgpu.rs
```

Symptoms:

```text
PaddedTokenBatch exists but is inaccessible
build_padded_token_batch exists but is inaccessible
embed_token_batch exists but is inaccessible
linear_apply exists but is inaccessible
linear_apply_batched exists but is inaccessible
rms_norm_vec exists but is inaccessible
rms_norm_batched exists but is inaccessible
causal_attention exists but is inaccessible
causal_attention_batched exists but is inaccessible
add_batched exists but is inaccessible
silu exists but is inaccessible
silu_mul_batched exists but is inaccessible
capture_module_from_batched_hidden exists but is inaccessible
apply_reference_loras_batched exists but is inaccessible
```

Classification:

```text
Reference math primitives are private to reference_checkpoint.rs but consumed by native_wgpu.rs.
```

Next commit:

```text
MODELCORE-COMPILE-04
```

Forbidden fix:

```text
Do not turn reference_checkpoint.rs into a public math warehouse.
```

### D. Runtime LoRA Telemetry Hook Boundary Drift

Representative files:

```text
crates/model_core/src/model_layers.rs
crates/model_core/src/runtime_lora.rs
```

Symptoms:

```text
note_runtime_lora_raw_fallback exists but is inaccessible
note_runtime_lora_bound_slice_empty exists but is inaccessible
note_runtime_lora_prepared_hit exists but is inaccessible
note_runtime_lora_prepared_miss exists but is inaccessible
note_runtime_lora_prepared_set_cache_invalidation exists but is inaccessible
note_runtime_lora_prepared_set_cache_miss exists but is inaccessible
```

Classification:

```text
model_layers.rs directly depends on runtime_lora.rs internal telemetry functions.
```

Next commit:

```text
MODELCORE-COMPILE-05
```

Forbidden fix:

```text
Do not expose runtime_lora internal stats objects to model_layers.rs.
```

### E. NativeWgpuModel Internal Boundary Drift

Representative files:

```text
crates/model_core/src/native_wgpu.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/generation_sampling.rs
```

Symptoms:

```text
field model is private
field device is private
field gpu_sampling_runtime is private
field gpu_penalty_runtime is private
field runtime_handles is private
field structure_routing_state is private
field active_penalty_coeffs is private
method active_attached_loras is private
method slice_last_logits_row is private
method slice_last_hidden_row is private
method should_materialize_cpu_last_row is private
method try_grouped_query_attention_via_atlas is private
method cat_seq_dim_4 is private
method apply_logit_postprocessors is private
method select_next_token is private
method select_next_token_with_sampling is private
method prefill is private
method decode_step is private
method prefill_with_sampling_choice is private
method decode_step_with_sampling_choice is private
```

Classification:

```text
NativeWgpuModel impl was split across modules without accessor/gateway boundaries.
```

Next commits:

```text
MODELCORE-COMPILE-06
MODELCORE-COMPILE-07
```

Forbidden fix:

```text
Do not make NativeWgpuModel fields pub(crate).
```

### F. Runtime LoRA Schema Drift

Representative file:

```text
crates/model_core/src/runtime_lora.rs
```

Symptoms:

```text
adapter_commit_delta_payload not found in scope
checkpoint_parity_latency_ms not found
memory_high_water_delta_ratio not found
native_step_started field missing
summary_string method missing on reason enums
struct initializer missing new fields
ModuleLocalNativeSourcePlusDeltaCommitBridgeRequest grad_* fields missing
ModuleLocalNativeAdapterSyncReadbackPreview fingerprint fields missing
ModuleLocalNativeDedicatedNstepStepResult result fields missing
```

Classification:

```text
runtime_lora structs and telemetry summaries are from different schema generations.
```

Next commit:

```text
MODELCORE-COMPILE-08
```

Forbidden fix:

```text
Do not fill unknown schema values with false, 0, or None silently.
```

### G. Result Alias / Type Inference Drift

Representative files:

```text
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/generation_sampling.rs
```

Symptoms:

```text
Result<T> expected two generic arguments
type annotations needed
```

Classification:

```text
Result alias/import boundary is unclear after module split.
```

Next commit:

```text
MODELCORE-COMPILE-10
```

### H. Ownership / Borrow Drift

Representative files:

```text
crates/model_core/src/runtime_lora.rs
crates/model_core/src/generation_sampling.rs
```

Symptoms:

```text
cannot move out of traces because it is borrowed
borrow of moved value severity
```

Classification:

```text
Local ownership-order issue, not the architectural root cause.
```

Next commit:

```text
MODELCORE-COMPILE-11
```

## Global Fix Order

```text
00 inventory only
01 module boundary SSOT
02 telemetry API rebind
03 shared sampling helpers extraction
04 reference math helper boundary
05 runtime_lora hook boundary
06 NativeWgpuModel accessor boundary
07 decode/sampling impl cohesion
08 runtime_lora schema reconciliation
09 native full checkpoint execution path contract
10 Result alias/type inference seal
11 ownership/borrow seal
12 model_core compile seal
13 lora_train compile seal
14 lora dump config path seal
15 smoke dump runtime seal
16 full dump runtime seal
```

## Hard Prohibitions

```text
- Do not replace snapshot telemetry with take telemetry.
- Do not make all private helpers pub(crate) blindly.
- Do not make NativeWgpuModel fields public.
- Do not fill missing telemetry/schema values with 0/false/None without explicit reason.
- Do not modify configs while model_core cannot compile.
- Do not treat tokenizer/model/dataset paths as the root cause of this compile failure.
```

## Acceptance Criteria

```text
- This document exists.
- No Rust source file is modified.
- Error families A-H are recorded.
- Each family has a next commit target.
- Silent correction prohibitions are explicitly listed.
```

## Commit Message

```text
MODELCORE-COMPILE-00: seal compile failure inventory
```
