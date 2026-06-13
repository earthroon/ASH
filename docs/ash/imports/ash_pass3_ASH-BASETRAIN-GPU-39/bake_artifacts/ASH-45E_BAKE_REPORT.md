# ASH-45E Bake Report

## Commit
ASH-45E — Calibration Snapshot / Audit Output Consistency

## Result
PASS_ASH_45E_CALIBRATION_SNAPSHOT_AUDIT_OUTPUT_CONSISTENCY

## Implemented
- Added `crates/ash_core/src/calibration_snapshot.rs`.
- Added snapshot bundle, manifest, file entry, count seal, and consistency status contracts.
- Added `snapshot_bundle_id`, `snapshot_consistency_status`, and `snapshot_count_consistent` to calibration report.
- Added `snapshot_bundle_id` and `source_snapshot_manifest_id` to scoring profile candidate.
- Extended ASH-45 audit report with ASH-45E snapshot consistency fields.
- Added Rust-native test files for snapshot bundle, count consistency, bundle validation, and orchestrator report/export checks.
- Added bundle-derived latest JSON snapshots under `workspace/event_sft/calibration/`.

## Policy Preserved
- No runtime router config mutation.
- No ASH-38 routing policy mutation.
- No ASH-34 temporal overlay mutation.
- No current pointer mutation.
- No LoRA attach/detach.
- No runtime hot reload.
- No Python validator.

## Rust-native commands sealed
```bash
cargo test -p ash_core ash_45e_calibration_snapshot
cargo test -p ash_core ash_45e_snapshot_count_consistency
cargo test -p ash_core ash_45e_snapshot_bundle_validation
cargo test -p orchestrator_local ash_45e_calibration_snapshot_report
cargo test -p orchestrator_local ash_45e_snapshot_export_consistency
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Environment note
This bake environment does not include `cargo` / `rustc`, so Rust-native commands are sealed but not executed here.
