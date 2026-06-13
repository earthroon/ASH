# ASH-50 Bake Report

## Commit
ASH-50 — Online Calibration Ledger / Drift Monitor

## Status
PASS_ASH_50_RUNTIME_DRIFT_MONITOR

## Added
- `crates/ash_core/src/online_calibration_ledger.rs`
- `crates/ash_core/src/runtime_drift_monitor.rs`
- `crates/orchestrator_local/src/bin/ash_50_online_calibration_ledger_audit.rs`
- `crates/orchestrator_local/src/ash_50_online_calibration_ledger_report.rs`
- ASH-50 ash_core tests
- ASH-50 orchestrator tests
- ledger/drift snapshots under `workspace/runtime/ledger/`

## Sealed Behavior
- Append-only ledger entries
- Hash-chain validation using previous entry hash
- Apply / rollback / safe-mode event extraction
- Drift signal detection for repeated apply failure, repeated rollback, safe mode, perf/telemetry regression, determinism drift, and lineage mismatch
- Drift recommendations are candidates only

## Non-goals preserved
- No runtime router config mutation
- No current pointer mutation
- No LoRA attach/detach
- No SFT/DPO training execution
- No Python validator

## Rust-native validation commands
```bash
cargo test -p ash_core ash_50_online_calibration_ledger
cargo test -p ash_core ash_50_ledger_append_only
cargo test -p ash_core ash_50_runtime_drift_monitor
cargo test -p ash_core ash_50_drift_recommendations
cargo test -p orchestrator_local ash_50_online_calibration_ledger_report
cargo run -p orchestrator_local --bin ash_50_online_calibration_ledger_audit
```
