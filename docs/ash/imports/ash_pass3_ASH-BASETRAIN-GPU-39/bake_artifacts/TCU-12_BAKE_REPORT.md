# TCU-12 Bake Report

## Status
PASS_TCU_12_TENSORCUBE_ASH_APPLY_DRIFT_BRIDGE

## Base SSOT
ash_pass3_ASH-50_online_calibration_ledger_drift_monitor_baked.zip

## Added
- `crates/ash_core/src/tensorcube_health_ash_bridge.rs`
- TCU-12 ash_core tests for bridge signals, apply blockers, rollback triggers, drift signals
- `crates/orchestrator_local/src/tcu_12_tensorcube_health_ash_bridge_report.rs`
- `crates/orchestrator_local/src/bin/tcu_12_tensorcube_health_ash_bridge_audit.rs`
- TCU-12 acceptance and static audit artifacts
- runtime/tensorcube snapshot JSON outputs

## Preserved Boundary
- No runtime pointer mutation.
- No LoRA attach/detach.
- No SFT/DPO training execution.
- No Python validator.
- TCU-12 uses ASH-side bridge observation structs; model_core direct dependency remains untouched.
