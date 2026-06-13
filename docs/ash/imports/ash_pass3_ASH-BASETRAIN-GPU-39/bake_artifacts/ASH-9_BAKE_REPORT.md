# ASH-9 Bake Report

## Commit
ASH-9 — lora_train/runtime/artifact_store integration

## Base
ASH-8 — Public API / CLI bridge rebaked

## Added
- `crates/runtime/src/ash_runtime_bridge.rs`
- `crates/runtime/tests/ash_runtime_bridge.rs`
- `crates/lora_train/src/ash_curriculum_bridge.rs`
- `crates/lora_train/tests/ash_curriculum_bridge.rs`
- `crates/artifact_store/src/ash_promotion_store.rs`
- `crates/artifact_store/tests/ash_promotion_store.rs`
- `crates/orchestrator_local/src/ash_integration.rs`
- `crates/orchestrator_local/tests/ash_integration.rs`

## Rust-native validation commands
```powershell
cargo test -p runtime ash_runtime_bridge
cargo test -p lora_train ash_curriculum_bridge
cargo test -p artifact_store ash_promotion_store
cargo test -p orchestrator_local ash_integration
```

## Python
No ASH-9 Python validator was added.

## Audit bin
```powershell
cargo run -p orchestrator_local --bin ash_9_integration_audit
```
