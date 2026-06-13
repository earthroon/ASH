# QW-50-R0K — model_core transition semantic prior import/export fix

## Scope

- Target crate: `model_core`
- Target files:
  - `crates/model_core/src/lib.rs`
  - `crates/model_core/src/cpu_oracle_sampler.rs`

## Fix

- Moved `GpuSemanticPriorConfig` import from the stale `burn_webgpu_backend` root import list to the actual public module path `burn_webgpu_backend::gpu_sampling::GpuSemanticPriorConfig`.
- Imported transition controlled helpers into `cpu_oracle_sampler.rs` from `crate::decode_transition_guard`:
  - `transition_controlled_enable_config_from_env`
  - `apply_transition_controlled_decision`
  - `TransitionControlledAction`
- Did not add stub implementations or compatibility shims.

## Guard

- No semantic prior policy mutation.
- No transition controlled decision mutation.
- No sampler trace field alignment included in this patch.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Static Pattern Check

See `artifacts/compile_recovery/qw50_r0k_static_pattern_check.json`.

## Verification

```txt
cargo check -p model_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
