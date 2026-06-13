# TCU-17 Bake Report

## Commit
TCU-17 — TensorCube Runtime Splice Replay / Determinism Seal

## Base SSOT
ash_pass3_TCU-16_tensorcube_lora_hot_reload_buffer_lease_seal_baked.zip

## Added
- crates/ash_core/src/tensorcube_runtime_splice_replay.rs
- crates/ash_core/tests/tcu_17_tensorcube_runtime_splice_replay.rs
- crates/ash_core/tests/tcu_17_splice_replay_determinism.rs
- crates/ash_core/tests/tcu_17_splice_replay_environment.rs
- crates/ash_core/tests/tcu_17_bridge_integration.rs
- crates/orchestrator_local/src/tcu_17_tensorcube_runtime_splice_replay_report.rs
- crates/orchestrator_local/src/bin/tcu_17_tensorcube_runtime_splice_replay_audit.rs
- crates/orchestrator_local/tests/tcu_17_tensorcube_runtime_splice_replay_report.rs
- acceptance_reports/TCU-17_tensorcube_runtime_splice_replay_determinism_seal.md
- workspace/runtime/tensorcube/ash_tensorcube_runtime_splice_replay_input_seal_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_runtime_splice_replay_comparison_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_runtime_splice_replay_report_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_runtime_splice_determinism_report_latest.json

## Modified
- crates/ash_core/src/lib.rs
- crates/ash_core/src/tensorcube_health_ash_bridge.rs
- crates/ash_core/src/runtime_drift_monitor.rs
- crates/orchestrator_local/src/lib.rs

## Static Result
PASS_STATIC_AUDIT_TCU_17

## Rust-native verification commands
```bash
cargo test -p ash_core tcu_17_tensorcube_runtime_splice_replay
cargo test -p ash_core tcu_17_splice_replay_determinism
cargo test -p ash_core tcu_17_splice_replay_environment
cargo test -p ash_core tcu_17_bridge_integration
cargo test -p orchestrator_local tcu_17_tensorcube_runtime_splice_replay_report
cargo run -p orchestrator_local --bin tcu_17_tensorcube_runtime_splice_replay_audit
```

## Container limitation
cargo/rustc are not available in this container, so Rust-native tests are sealed but not executed here.
