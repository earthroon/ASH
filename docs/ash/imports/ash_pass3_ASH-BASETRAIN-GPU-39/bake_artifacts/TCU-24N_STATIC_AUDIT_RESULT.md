# TCU-24N Static Audit Result

## Status

`PASS_STATIC_TCU_24N_WITH_NATIVE_TESTS_NOT_RUN`

## Static checks performed

- New backend module exists.
- New backend module is exported from `burn_webgpu_backend/src/lib.rs`.
- New orchestrator report module exists.
- New orchestrator report module is exported from `orchestrator_local/src/lib.rs`.
- Runtime JSON artifacts exist.
- Acceptance report exists.
- Bake report exists.
- Apply execution remains forbidden by config and report fields.
- Quarantine release remains forbidden by config and report fields.
- Current pointer mutation remains forbidden by config and report fields.

## Native tests

Not run. This container does not provide `cargo` or `rustc`.

## Command set for native verification

```bash
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_config_gate
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_source_recovery_gate
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_reentry_gate
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_pointer_guard
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_rollback_preflight
cargo test -p burn_webgpu_backend tcu_24n_qwave_apply_preflight_no_apply_or_release
cargo test -p orchestrator_local tcu_24n_qwave_apply_preflight_report
cargo run -p orchestrator_local --bin tcu_24n_qwave_apply_preflight_audit
```
