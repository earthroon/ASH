# QW-50-R0J — burn_webgpu_backend preflight test field alias fix

## Scope

- Target crate: `burn_webgpu_backend`
- Target file:
  - `crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_no_apply_or_release.rs`

## Fix

- Replaced stale test access `report.quarantine_release_execution_allowed` with the current SSOT location `report.config.quarantine_release_execution_allowed`.
- Preserved no-apply, no-runtime-apply, no-pointer-mutation, and no-production-default-change assertions.
- Did not add a compatibility alias field to `QWaveBackendApplyPreflightReport`.

## Guard

- No backend apply execution.
- No quarantine release execution.
- No runtime pointer mutation.
- No production apply.
- No model_core or ash_core modifications.

## Verification

```txt
cargo check -p burn_webgpu_backend --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
