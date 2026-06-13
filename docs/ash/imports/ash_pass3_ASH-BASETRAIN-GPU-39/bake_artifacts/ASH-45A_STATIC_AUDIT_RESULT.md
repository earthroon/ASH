# ASH-45A Static Audit Result

## Status
PASS_STATIC_AUDIT_ASH_45A

## Static Checks
- `crates/ash_core/src/calibration_attribution.rs` exists.
- `AshCalibrationAttributionClass` is defined.
- `AshCalibrationAttributionTrace` is defined.
- `AshCalibrationAttributionDecision` is defined.
- `AshEventTagRouterCalibrationEvidence` carries attribution fields.
- `event_tag_router_calibration.rs` blocks global perf pressure from adapter penalty.
- `event_tag_router_calibration.rs` blocks unrelated rollback from adapter threshold raise.
- `build_ash_45_event_tag_router_calibration_audit_report()` emits ASH-45A audit fields.
- `crates/orchestrator_local/tests/ash_45a_adapter_scoped_calibration_report.rs` exists.
- `tools/validate_ash_45a_static.py` does not exist.

## Not Executed
`cargo test` and `cargo run` were not executed because the current container has no Rust toolchain.
