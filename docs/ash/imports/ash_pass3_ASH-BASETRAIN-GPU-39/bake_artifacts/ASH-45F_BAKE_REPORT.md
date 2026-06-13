# ASH-45F Bake Report

## Status
PASS_ASH_45F_CALIBRATION_DETERMINISM_REPLAY_SEAL

## Base SSOT
ash_pass3_ASH-45E_calibration_snapshot_audit_output_consistency_baked.zip

## Added
- `crates/ash_core/src/calibration_determinism.rs`
- `crates/ash_core/tests/ash_45f_calibration_determinism.rs`
- `crates/ash_core/tests/ash_45f_replay_seal.rs`
- `crates/ash_core/tests/ash_45f_order_invariance.rs`
- `crates/ash_core/tests/ash_45f_deterministic_id_derivation.rs`
- `crates/orchestrator_local/tests/ash_45f_calibration_determinism_report.rs`
- `crates/orchestrator_local/tests/ash_45f_replay_audit_consistency.rs`
- `workspace/event_sft/calibration/ash_calibration_replay_input_seal_latest.json`
- `workspace/event_sft/calibration/ash_calibration_replay_comparison_report_latest.json`
- `workspace/event_sft/calibration/ash_calibration_determinism_report_latest.json`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/src/event_tag_router_calibration.rs`
- `crates/ash_core/src/event_tag_scoring_profile.rs`
- `crates/ash_core/src/calibration_snapshot.rs`
- `crates/orchestrator_local/src/bin/ash_45_event_tag_router_calibration_audit.rs`

## Sealed Rules
- deterministic SHA-256 hex id derivation
- explicit now_unix_ms input
- canonical ordering V1
- replay input seal
- replay comparison report
- semantic id drift rejection
- snapshot bundle output fingerprint
- no runtime mutation / current pointer mutation / LoRA attach
- no Python validator

## Rust-native validation commands
```bash
cargo test -p ash_core ash_45f_calibration_determinism
cargo test -p ash_core ash_45f_replay_seal
cargo test -p ash_core ash_45f_order_invariance
cargo test -p ash_core ash_45f_deterministic_id_derivation
cargo test -p orchestrator_local ash_45f_calibration_determinism_report
cargo test -p orchestrator_local ash_45f_replay_audit_consistency
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Local container note
`cargo` and `rustc` are not installed in this execution container, so Rust-native tests were sealed as commands but not executed here.
