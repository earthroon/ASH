# ASH-44 Bake Report

## SSOT
Input SSOT: ASH-43 baked tree.

## Added
- crates/ash_core/src/plasticity_rollback.rs
- crates/ash_core/src/adapter_pointer_lineage.rs
- crates/ash_core/src/rollback_preflight.rs
- crates/ash_core/src/rollback_lineage_report.rs
- crates/orchestrator_local/src/ash_44_rollback_lineage_report.rs
- crates/orchestrator_local/src/bin/ash_44_plasticity_rollback_lineage_audit.rs
- ASH-44 tests and acceptance report

## Guardrails
- No rollback execution
- No current pointer mutation
- No adapter registry mutation
- No runtime hot reload
- requires_explicit_rollback=true
- rollback_started=false
- Python validator absent
