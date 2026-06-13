# MODELCORE-COMPILE-01 - model_core Module Boundary SSOT

## Purpose

This document defines ownership boundaries inside `crates/model_core`.

The current compile failure state shows that multiple modules call helpers, fields, methods, and telemetry functions across private module boundaries without a stable contract.

This document is the SSOT for later compile repair commits.

This commit is documentation-only. It must not modify Rust source code.

## State Attribution

```text
state_owner = crates/model_core/src module boundary
ssot = docs/architecture/model_core_module_boundary_ssot.md
reproducible = by comparing later code changes against this boundary document
```

## Module Ownership Map

### native_wgpu.rs

Owns:

```text
- NativeWgpuModel runtime state
- native GPU inference model
- wgpu device/queue/runtime handles
- raw bridge handles
- GPU sampling runtime handles
- GPU penalty runtime handles
- structure routing state
- native decode/generation runtime integration
```

Must not expose directly:

```text
- model field
- device field
- runtime_handles field
- gpu_sampling_runtime field
- gpu_penalty_runtime field
- active_penalty_coeffs field
- structure_routing_state field
```

Allowed exposure pattern:

```text
- narrow accessor
- gateway method
- command/query wrapper
```

Forbidden exposure pattern:

```text
pub(crate) field model
pub(crate) field device
pub(crate) field runtime_handles
pub(crate) field gpu_sampling_runtime
pub(crate) field gpu_penalty_runtime
```

### decode_state.rs

Owns:

```text
- DecodeState
- KV cache step state
- prefill/decode state machine
- token-by-token state transition
```

May access NativeWgpuModel only through:

```text
- decode-specific gateway methods
- explicit accessors provided by native_wgpu.rs
- shared helper modules
```

Must not access:

```text
self.model
self.device
self.runtime_handles
self.gpu_sampling_runtime
self.gpu_penalty_runtime
```

Allowed pattern:

```rust
let logits = self.forward_logits_for_decode(input)?;
let device = self.device_for_decode();
```

Forbidden pattern:

```rust
let logits = self.model.forward_logits(...);
let device = &self.device;
```

### generation_sampling.rs

Owns:

```text
- sampling configuration resolution
- logit post-processing
- banned token mask application
- repetition penalty application
- next token selection
- stop sequence / holdback handling
- sampling telemetry assembly
```

Must not own:

```text
- NativeWgpuModel internal fields
- raw wgpu device fields
- reference checkpoint math primitives
```

May depend on:

```text
crate::sampling_helpers
crate::generation_telemetry
NativeWgpuModel sampling gateway methods
```

### reference_checkpoint.rs

Owns:

```text
- ReferenceModel orchestration
- full checkpoint backed CPU/reference execution path
- reference forward/logits behavior
```

Must not permanently own:

```text
- generic sampling helpers
- generic tensor math primitives shared with native path
```

Helpers to extract later:

```text
sampling_helpers.rs:
- apply_banned_token_mask
- apply_repetition_penalty
- has_repeating_suffix
- has_repeating_ngram
- StreamingTextHoldback
- max_stop_holdback_chars
- check_generation_cancel
- append_token_piece_to_text
- detect_stop_hit

reference_math.rs:
- PaddedTokenBatch
- BatchedHidden
- linear_apply
- linear_apply_batched
- rms_norm_vec
- rms_norm_batched
- causal_attention
- causal_attention_batched
- add_batched
- silu
- silu_mul_batched
- build_padded_token_batch
- embed_token_batch
- capture_module_from_batched_hidden
```

### model_layers.rs

Owns:

```text
- Tensor layer primitives
- grouped query attention
- model layer operations
```

Must not own:

```text
- runtime_lora telemetry state
- runtime_lora hot path stats
```

Allowed dependency:

```text
runtime_lora_hooks.rs
```

Forbidden dependency:

```text
direct mutation of runtime_lora stats internals
```

### runtime_lora.rs

Owns:

```text
- LoRA runtime schema
- native train protocol structures
- native commit plan/result schema
- runtime LoRA telemetry
- LoRA hot path stats
- native training stage states
```

Must expose:

```text
- stable types
- stable constructors
- hook functions
- explicit not_run/unknown/failure reason values
```

Must not allow:

```text
- silent fallback to 0
- silent fallback to false
- silent fallback to None when state is semantically unknown
```

Schema changes require:

```text
- struct field update
- constructor/default update
- summary/update report update
- reason propagation update
```

### generation_telemetry.rs

Owns:

```text
- generation step telemetry
- tensorcube/runtime splice label summaries
- sampling/generation telemetry aggregation
```

Must not drain telemetry when snapshot is requested.

Allowed API semantics:

```text
snapshot_* = read-only copy/summary
take_* = read and reset/drain
with_*_label = scoped label binding around closure
```

Forbidden substitution:

```text
snapshot_* -> take_*
```

## Shared Helper Modules To Introduce

Later commits may create:

```text
crates/model_core/src/sampling_helpers.rs
crates/model_core/src/reference_math.rs
crates/model_core/src/runtime_lora_hooks.rs
```

### sampling_helpers.rs

Purpose:

```text
Pure text/token sampling helpers shared by reference and native generation paths.
```

May contain:

```text
- banned token masking
- repetition penalty
- repeat detection
- stop sequence holdback
- cancellation check
- token piece append
- stop hit detection
```

Must not contain:

```text
- NativeWgpuModel
- wgpu runtime handles
- LoRA commit state
```

### reference_math.rs

Purpose:

```text
CPU/reference full checkpoint math primitives shared by reference checkpoint and native capture bridge paths.
```

May contain:

```text
- linear/rms/attention helpers
- batched hidden helpers
- padded token batch helpers
- capture helper functions
```

Must not contain:

```text
- GPU runtime dispatch
- sampling policy
- telemetry mutation
```

### runtime_lora_hooks.rs

Purpose:

```text
Small hook surface for model_layers.rs to notify runtime_lora.rs without owning telemetry internals.
```

May contain:

```text
- note_raw_fallback
- note_bound_slice_empty
- note_prepared_hit
- note_prepared_miss
- note_prepared_set_cache_invalidation
- note_prepared_set_cache_miss
```

Must not expose:

```text
- full hot path stats object
- mutable telemetry internals
```

## Visibility Policy

```text
private:
  implementation detail used only inside one module

pub(super):
  used by sibling module under a planned parent module

pub(crate):
  stable internal crate API with documented reason

pub:
  external crate API only
```

Default rule:

```text
Do not use pub(crate) to solve a compile error unless the API belongs to a shared crate-level contract.
```

## Access Pattern Rules

### NativeWgpuModel

Forbidden:

```rust
self.model
self.device
self.gpu_sampling_runtime
self.gpu_penalty_runtime
self.runtime_handles
self.structure_routing_state
self.active_penalty_coeffs
```

Allowed:

```rust
self.forward_logits_for_decode(...)
self.device_for_decode()
self.structure_routing_state()
self.with_gpu_sampling_runtime(...)
```

### Telemetry

Forbidden when the intended semantic is before/after comparison:

```rust
take_runtime_splice_telemetry_summary()
```

Allowed:

```rust
snapshot_runtime_splice_telemetry_summary()
```

or creation of a true snapshot API.

### Missing Runtime State

Forbidden when the runtime state is unknown:

```rust
value: None
value: false
value: 0
```

Allowed:

```rust
value: RuntimeState::Unknown { reason: "..." }
value: Some(NotRun { reason: "..." })
```

## Commit Dependency Map

```text
MODELCORE-COMPILE-02 depends on 01 telemetry semantics.
MODELCORE-COMPILE-03 depends on 01 sampling_helpers ownership.
MODELCORE-COMPILE-04 depends on 01 reference_math ownership.
MODELCORE-COMPILE-05 depends on 01 runtime_lora_hooks ownership.
MODELCORE-COMPILE-06 depends on 01 NativeWgpuModel accessor policy.
MODELCORE-COMPILE-08 depends on 01 runtime_lora schema policy.
```

## Acceptance Criteria

```text
- This document exists.
- No Rust source file is modified.
- NativeWgpuModel ownership boundary is declared.
- sampling_helpers extraction target is declared.
- reference_math extraction target is declared.
- runtime_lora_hooks target is declared.
- telemetry snapshot/take distinction is declared.
- silent 0/false/None correction is explicitly forbidden.
```

## Commit Message

```text
MODELCORE-COMPILE-01: seal model_core module boundary SSOT
```
