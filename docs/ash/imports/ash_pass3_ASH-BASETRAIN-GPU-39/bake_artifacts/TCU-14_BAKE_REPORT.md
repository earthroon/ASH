# TCU-14 Bake Report

## Commit
TCU-14 — TensorCube Native Path Preflight / Same-Device Borrow Gate

## Base SSOT
ash_pass3_TCU-13_tensorcube_runtime_telemetry_canonical_snapshot_baked.zip

## Added
- crates/ash_core/src/tensorcube_native_path_preflight.rs
- crates/ash_core/tests/tcu_14_tensorcube_native_path_preflight.rs
- crates/ash_core/tests/tcu_14_same_device_borrow_gate.rs
- crates/ash_core/tests/tcu_14_native_path_blockers.rs
- crates/ash_core/tests/tcu_14_bridge_integration.rs
- crates/orchestrator_local/src/tcu_14_tensorcube_native_path_preflight_report.rs
- crates/orchestrator_local/src/bin/tcu_14_tensorcube_native_path_preflight_audit.rs
- crates/orchestrator_local/tests/tcu_14_tensorcube_native_path_preflight_report.rs
- acceptance_reports/TCU-14_tensorcube_native_path_preflight_same_device_borrow_gate.md

## Modified
- crates/ash_core/src/lib.rs
- crates/ash_core/src/tensorcube_health_ash_bridge.rs
- crates/orchestrator_local/src/lib.rs

## Static status
PASS_STATIC_AUDIT_TCU_14

## Boundary
No runtime pointer mutation, no LoRA attach/detach, no TensorCube buffer mutation, no SFT/DPO training, no Python validator.
