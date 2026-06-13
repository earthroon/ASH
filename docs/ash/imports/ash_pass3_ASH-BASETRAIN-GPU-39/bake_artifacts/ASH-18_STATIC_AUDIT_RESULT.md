# ASH-18 Static Audit Result

## Status
PASS_STATIC_ASH_18_COACTIVATION_LEDGER_HEBBIAN_UPDATE

## Required files

- crates/ash_core/src/coactivation_ledger.rs: OK (13686 bytes)
- crates/ash_core/src/hebbian_update.rs: OK (19338 bytes)
- crates/orchestrator_local/src/ash_18_coactivation_ledger_report.rs: OK (3819 bytes)
- crates/orchestrator_local/src/bin/ash_18_coactivation_ledger_audit.rs: OK (1143 bytes)
- crates/ash_core/tests/ash_18_coactivation_ledger.rs: OK (3453 bytes)
- crates/ash_core/tests/ash_18_hebbian_update.rs: OK (3630 bytes)
- crates/orchestrator_local/tests/ash_18_coactivation_ledger_report.rs: OK (1996 bytes)
- acceptance_reports/ASH-18_coactivation_ledger_hebbian_path_cost_update.md: OK (1118 bytes)
- bake_artifacts/ASH-18_BAKE_REPORT.md: OK (2079 bytes)

## Contract checks

- coactivation types: OK
- hebbian types: OK
- explicit apply: OK
- audit log: OK
- no python validator: OK
- ash_core lib export: OK
- orchestrator export: OK