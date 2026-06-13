# TCU-15 Bake Report

## Commit
TCU-15 — TensorCube Host Fallback Pressure Guard

## Base SSOT
ash_pass3_TCU-14_tensorcube_native_path_preflight_same_device_borrow_gate_baked.zip

## Added
- crates/ash_core/src/tensorcube_fallback_pressure_guard.rs
- crates/ash_core/tests/tcu_15_tensorcube_fallback_pressure_guard.rs
- crates/ash_core/tests/tcu_15_pressure_score.rs
- crates/ash_core/tests/tcu_15_pressure_decision.rs
- crates/ash_core/tests/tcu_15_bridge_integration.rs
- crates/orchestrator_local/src/tcu_15_tensorcube_fallback_pressure_guard_report.rs
- crates/orchestrator_local/src/bin/tcu_15_tensorcube_fallback_pressure_guard_audit.rs
- crates/orchestrator_local/tests/tcu_15_tensorcube_fallback_pressure_guard_report.rs
- acceptance_reports/TCU-15_tensorcube_host_fallback_pressure_guard.md

## Modified
- crates/ash_core/src/lib.rs
- crates/ash_core/src/tensorcube_health_ash_bridge.rs
- crates/orchestrator_local/src/lib.rs

## Static status
PASS_STATIC_AUDIT_TCU_15

## Boundary
No runtime pointer mutation, no LoRA attach/detach, no TensorCube buffer mutation, no host fallback execution, no CPU materialize execution, no SFT/DPO training, no Python validator.
