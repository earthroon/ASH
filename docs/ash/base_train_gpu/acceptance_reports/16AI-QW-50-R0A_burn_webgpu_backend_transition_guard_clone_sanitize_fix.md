# QW-50-R0A — burn_webgpu_backend transition guard clone/sanitize fix

## Scope

- Target crate: `burn_webgpu_backend`
- Target file: `crates/burn_webgpu_backend/src/gpu_sampling.rs`
- Patch type: compile recovery / ownership fix

## Applied Fix

- Removed direct `v.transition_guard.sanitized()` access behind shared reference in `GpuSamplingUniform::from_config_with_top_k`.
- Added local `sanitized_transition_guard = v.transition_guard.clone().sanitized();`.
- Reused the sanitized policy values for `transition_soft_penalty_scale` and `transition_max_soft_penalty`.
- Kept transition guard policy values and runtime sampling semantics unchanged.

## Guard

- No ash_core files were intentionally modified by this patch.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.
- No transition guard threshold or default policy mutation.

## Static Verification

- `v.transition_guard.sanitized()` no longer appears in `gpu_sampling.rs`.
- The sanitized transition guard is computed once in the function scope.

## Native Verification

`cargo check` was not executed in this container because `cargo` / `rustc` are unavailable.

Recommended local command:

```powershell
cargo check -p burn_webgpu_backend --lib
```

## Status

`PENDING_LOCAL_CARGO_CHECK`
