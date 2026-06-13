# TCU-24H Bake Report

## Added files

```text
crates/burn_webgpu_backend/src/qwave_atlas_backend_router.rs
crates/burn_webgpu_backend/tests/tcu_24h_qwave_backend_router_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_24h_qwave_backend_router_source_evidence_gate.rs
crates/burn_webgpu_backend/tests/tcu_24h_qwave_backend_candidate_score.rs
crates/burn_webgpu_backend/tests/tcu_24h_qwave_backend_advisory_decision.rs
crates/burn_webgpu_backend/tests/tcu_24h_qwave_backend_no_apply_or_production_switch.rs
crates/orchestrator_local/src/tcu_24h_qwave_backend_router_report.rs
crates/orchestrator_local/src/bin/tcu_24h_qwave_backend_router_audit.rs
crates/orchestrator_local/tests/tcu_24h_qwave_backend_router_report.rs
workspace/runtime/tensorcube/ash_qwave_backend_router_config_latest.json
workspace/runtime/tensorcube/ash_qwave_backend_candidate_scores_latest.json
workspace/runtime/tensorcube/ash_qwave_backend_advisory_decision_latest.json
workspace/runtime/tensorcube/ash_qwave_backend_router_report_latest.json
acceptance_reports/TCU-24H_qwave_atlas_backend_selection_candidate_advisory_router.md
bake_artifacts/TCU-24H_BAKE_REPORT.md
bake_artifacts/TCU-24H_STATIC_AUDIT_RESULT.md
```

## Modified files

```text
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
```

## Safety seal

```text
Router may nominate.
Router may rank.
Router may block.
Router must not apply.
```

## Native test status

Native Rust/Cargo execution was not available in the bake container. Static audit only.
