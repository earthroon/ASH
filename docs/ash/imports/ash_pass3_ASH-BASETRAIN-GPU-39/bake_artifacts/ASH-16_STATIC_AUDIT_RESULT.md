# ASH-16 static audit result

## Status
PASS_STATIC_ASH16_FILE_CONTRACT

## Checked files
- `crates/ash_core/src/adapter_synapse.rs`
- `crates/ash_core/src/weighted_synapse_router.rs`
- `crates/ash_core/src/runtime_router.rs`
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/ash_16_synapse_route_report.rs`
- `crates/orchestrator_local/src/lib.rs`
- `crates/orchestrator_local/src/bin/ash_16_weighted_synapse_audit.rs`
- `crates/ash_core/tests/ash_16_weighted_synapse_router.rs`
- `crates/orchestrator_local/tests/ash_16_synapse_route_report.rs`

## Guards
- `tools/validate_ash_16_static.py` absent
- ASH-16 graph/route/report/audit tokens present
- delimiter sanity passed
