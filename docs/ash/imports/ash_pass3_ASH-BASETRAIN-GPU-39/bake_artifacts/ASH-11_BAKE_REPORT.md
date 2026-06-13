# ASH-11 Bake Report

## Commit
ASH-11 — Runtime Current Pointer Consumption / Explicit Base-Only Gate

## Files
- crates/runtime/src/ash_current_pointer.rs
- crates/runtime/tests/ash_current_pointer.rs
- crates/runtime/src/lib.rs
- crates/orchestrator_local/src/ash_runtime_pointer_integration.rs
- crates/orchestrator_local/src/bin/ash_11_runtime_pointer_audit.rs
- crates/orchestrator_local/tests/ash_runtime_pointer_integration.rs
- crates/orchestrator_local/src/lib.rs
- acceptance_reports/ASH-11_runtime_current_pointer_explicit_base_only_gate.md

## Contract
Runtime consumes persisted current adapter pointer metadata. If the current pointer is empty, runtime must require an explicit base-only request instead of silently falling back to base.

## Validation commands
```powershell
cargo test -p runtime ash_current_pointer
cargo test -p orchestrator_local ash_runtime_pointer_integration
cargo run -p orchestrator_local --bin ash_11_runtime_pointer_audit
```

## Python
No ASH-11 Python validator was added.
