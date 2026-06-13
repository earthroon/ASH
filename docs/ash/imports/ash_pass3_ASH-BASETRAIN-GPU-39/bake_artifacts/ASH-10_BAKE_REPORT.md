# ASH-10 Bake Report

## Commit
ASH-10 — Synapse Registry Persistence / Rollback Apply

## Base
ASH-9 — lora_train/runtime/artifact_store integration

## Files
- crates/artifact_store/src/ash_synapse_registry_store.rs
- crates/artifact_store/src/ash_rollback_store.rs
- crates/artifact_store/tests/ash_synapse_registry_store.rs
- crates/artifact_store/tests/ash_rollback_store.rs
- crates/orchestrator_local/src/ash_persistence_integration.rs
- crates/orchestrator_local/src/bin/ash_10_persistence_audit.rs
- crates/orchestrator_local/tests/ash_persistence_integration.rs
- acceptance_reports/ASH-10_synapse_registry_persistence_rollback_apply.md

## Rust-native validation commands
```powershell
cargo test -p artifact_store ash_synapse_registry_store
cargo test -p artifact_store ash_rollback_store
cargo test -p orchestrator_local ash_persistence_integration
cargo run -p orchestrator_local --bin ash_10_persistence_audit
```

## Python validator
No ASH-10 Python validator is present.

## Status
Baked. Runtime compile must be verified in the user's Rust environment.
