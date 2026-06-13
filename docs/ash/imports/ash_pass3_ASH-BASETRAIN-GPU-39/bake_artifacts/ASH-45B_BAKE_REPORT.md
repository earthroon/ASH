# ASH-45B Bake Report

## Status
PASS_ASH_45B_MANUAL_REVIEW_TELEMETRY_REGRESSION_SAFETY_SEAL

## Base SSOT
ash_pass3_ASH-45A_adapter_scoped_calibration_evidence_isolation_baked.zip

## Implemented
- Added `crates/ash_core/src/calibration_safety.rs`.
- Added safety flags/decision/seal contracts.
- Extended calibration evidence with `telemetry_regression_seen` and `safety_flags`.
- Extended scoring adjustment with `safety_decision`, `safety_seal`, and `positive_adjustment_suppressed`.
- Extended profile/report counts with safety suppression, telemetry regression, and unsafe manual-review counts.
- Applied group-level safety seal during scoring adjustment build.
- Updated audit report status to ASH-45B while preserving ASH-45A attribution checks.
- Added Rust-native test files for ASH-45B safety behavior.

## Guardrails
- No runtime router config mutation.
- No routing policy mutation.
- No temporal overlay mutation.
- No current pointer mutation.
- No LoRA attach/detach.
- No hot reload.
- No Python validator.

## Rust-native commands sealed
```bash
cargo test -p ash_core ash_45b_calibration_safety
cargo test -p ash_core ash_45b_manual_review_safety
cargo test -p ash_core ash_45b_telemetry_regression_safety
cargo test -p orchestrator_local ash_45b_calibration_safety_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Local limitation
This container has no `cargo`/`rustc`, so only static file checks were performed here.
