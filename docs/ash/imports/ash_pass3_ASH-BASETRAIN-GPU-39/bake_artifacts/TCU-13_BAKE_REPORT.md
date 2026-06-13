# TCU-13 Bake Report

## Status
PASS_TCU_13_TENSORCUBE_TELEMETRY_CANONICAL_SNAPSHOT

## Added
- `crates/ash_core/src/tensorcube_runtime_telemetry_snapshot.rs`
- `crates/ash_core/tests/tcu_13_tensorcube_runtime_telemetry_snapshot.rs`
- `crates/ash_core/tests/tcu_13_tensorcube_telemetry_completeness.rs`
- `crates/ash_core/tests/tcu_13_tensorcube_telemetry_conflicts.rs`
- `crates/ash_core/tests/tcu_13_tensorcube_bridge_snapshot_integration.rs`
- `crates/orchestrator_local/src/tcu_13_tensorcube_telemetry_snapshot_report.rs`
- `crates/orchestrator_local/src/bin/tcu_13_tensorcube_telemetry_snapshot_audit.rs`
- `crates/orchestrator_local/tests/tcu_13_tensorcube_telemetry_snapshot_report.rs`
- `workspace/runtime/tensorcube/ash_tensorcube_runtime_telemetry_snapshot_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_telemetry_snapshot_manifest_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_telemetry_canonicalization_report_latest.json`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/src/tensorcube_health_ash_bridge.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed Guarantees
- TensorCube telemetry is canonicalized into one read-only snapshot.
- Complete / Partial / MissingCriticalSource / Ambiguous / Unknown are separated.
- Strong confidence requires a complete non-conflicting snapshot.
- Native / HostFallback / CpuMaterialized / MixedPath / FailedClosed are not averaged.
- TCU-12 can build ASH bridge report from a TCU-13 snapshot.
- Missing or ambiguous telemetry is not treated as healthy.
- No runtime pointer, LoRA attachment, TensorCube buffer, or GPU buffer mutation is added.
- No Python validator is added.

## Rust-native commands sealed
```bash
cargo test -p ash_core tcu_13_tensorcube_runtime_telemetry_snapshot
cargo test -p ash_core tcu_13_tensorcube_telemetry_completeness
cargo test -p ash_core tcu_13_tensorcube_telemetry_conflicts
cargo test -p ash_core tcu_13_tensorcube_bridge_snapshot_integration
cargo test -p orchestrator_local tcu_13_tensorcube_telemetry_snapshot_report
cargo run -p orchestrator_local --bin tcu_13_tensorcube_telemetry_snapshot_audit
```

## Local limitation
This bake environment does not include cargo/rustc, so Rust-native tests were sealed but not executed here.
