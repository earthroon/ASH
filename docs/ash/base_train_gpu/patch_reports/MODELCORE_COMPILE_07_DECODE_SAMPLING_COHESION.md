# MODELCORE-COMPILE-07 — Decode / Sampling Impl Cohesion Pass

## Purpose

Resolve remaining cross-module private method access between `decode_state.rs`, `generation_sampling.rs`, and shared model layer primitives.

Rust privacy is module-based, not impl-based. Even methods attached to `NativeWgpuModel` remain inaccessible across sibling modules unless they are exposed through a deliberate crate-internal boundary.

## Changed Files

- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/model_layers.rs`
- `crates/model_core/src/native_wgpu.rs`

## Changes

- Promoted decode state machine gateway methods to `pub(crate)`:
  - `prefill`
  - `decode_step`
  - `prefill_with_sampling_choice`
  - `decode_step_with_sampling_choice`
- Promoted model layer primitive to `pub(crate)`:
  - `grouped_query_attention`
- Added explicit `grouped_query_attention` imports where the native/decode paths use the shared primitive.
- Kept `NativeWgpuModel` fields private.
- Kept `runtime_lora` schema untouched.
- Kept reference math untouched.

## Non-Goals

- No runtime_lora schema reconciliation.
- No execution_path repair.
- No config changes.
- No public field exposure.
- No generation algorithm changes.
- No sampling policy changes.

## Prohibited Shortcuts Avoided

- Did not expose NativeWgpuModel fields.
- Did not move decode/generation code into one giant file.
- Did not duplicate `grouped_query_attention`.
- Did not replace decode state machine with fallback/no-op behavior.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_07_check.log"
```

Expected cleared patterns:

```text
method `prefill` is private
method `decode_step` is private
method `prefill_with_sampling_choice` is private
method `decode_step_with_sampling_choice` is private
function `grouped_query_attention` exists but is inaccessible
```

Allowed remaining patterns:

```text
runtime_lora schema drift
execution_path missing on NativeWgpuModel
Result/type inference residuals
ownership/borrow drift
native_step_started field drift
adapter_commit_delta_payload drift
```
