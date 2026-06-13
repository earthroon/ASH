# TCU-20 Bake Report

## Commit
TCU-20 — TensorCube Long-Horizon Health Ledger / Backend Drift Score

## Source SSOT
ash_pass3_TCU-19_tensorcube_emergency_demotion_safe_tensor_mode_baked.zip

## Added
- crates/ash_core/src/tensorcube_health_ledger.rs
- crates/ash_core/src/tensorcube_long_horizon_health.rs
- crates/ash_core/tests/tcu_20_tensorcube_health_ledger.rs
- crates/ash_core/tests/tcu_20_backend_drift_score.rs
- crates/ash_core/tests/tcu_20_health_recommendations.rs
- crates/ash_core/tests/tcu_20_append_only_chain.rs
- crates/orchestrator_local/src/bin/tcu_20_tensorcube_long_horizon_health_audit.rs
- crates/orchestrator_local/src/tcu_20_tensorcube_long_horizon_health_report.rs
- crates/orchestrator_local/tests/tcu_20_tensorcube_long_horizon_health_report.rs

## Sealed Outputs
- workspace/runtime/tensorcube/ash_tensorcube_health_ledger_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_health_ledger_snapshot_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_backend_drift_score_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_health_score_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_long_horizon_health_report_latest.json
- workspace/runtime/tensorcube/ash_tensorcube_health_recommendation_candidate_latest.json

## Runtime Boundary
TCU-20 emits ledger entries, scores, drift signals, and recommendations only.
It does not mutate runtime pointers, LoRA attachments, TensorCube/GPU buffers, backend config, or routing policy.

## Rust-native Commands Sealed
```bash
cargo test -p ash_core tcu_20_tensorcube_health_ledger
cargo test -p ash_core tcu_20_backend_drift_score
cargo test -p ash_core tcu_20_health_recommendations
cargo test -p ash_core tcu_20_append_only_chain
cargo test -p orchestrator_local tcu_20_tensorcube_long_horizon_health_report
cargo run -p orchestrator_local --bin tcu_20_tensorcube_long_horizon_health_audit
```

## Local Container Note
cargo/rustc were not available in this container, so Rust-native commands are sealed but not executed here.
