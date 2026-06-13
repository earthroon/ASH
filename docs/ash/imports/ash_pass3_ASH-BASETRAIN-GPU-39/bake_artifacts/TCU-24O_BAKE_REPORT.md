# TCU-24O Bake Report

## Baked commit

`TCU-24O — Operator-Approved Guarded Apply Attempt Candidate / Shadow Commit Plan`

## Source SSOT

`ash_pass3_TCU-24N_qwave_guarded_apply_attempt_preflight_reentry_gate_baked.zip`

## Added files

```text
crates/burn_webgpu_backend/src/qwave_backend_shadow_commit.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_source_preflight_gate.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_operator_approval.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_cas_precondition.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_plan.rs
crates/burn_webgpu_backend/tests/tcu_24o_qwave_shadow_commit_no_execution.rs
crates/orchestrator_local/src/tcu_24o_qwave_shadow_commit_report.rs
crates/orchestrator_local/src/bin/tcu_24o_qwave_shadow_commit_audit.rs
crates/orchestrator_local/tests/tcu_24o_qwave_shadow_commit_report.rs
```

## Runtime JSON

```text
workspace/runtime/tensorcube/ash_qwave_shadow_commit_config_latest.json
workspace/runtime/tensorcube/ash_qwave_shadow_commit_source_preflight_gate_latest.json
workspace/runtime/tensorcube/ash_qwave_shadow_commit_operator_approval_latest.json
workspace/runtime/tensorcube/ash_qwave_shadow_commit_cas_precondition_latest.json
workspace/runtime/tensorcube/ash_qwave_shadow_commit_plan_latest.json
workspace/runtime/tensorcube/ash_qwave_shadow_commit_report_latest.json
```

## Sealed false flags

```text
operator_approval_allows_execution = false
shadow_commit_execution_allowed = false
compare_and_swap_execution_allowed = false
apply_attempt_execution_allowed = false
quarantine_release_execution_allowed = false
health_score_persistence_allowed = false
runtime_apply_allowed = false
current_backend_pointer_mutation_allowed = false
active_backend_mutation_allowed = false
production_default_change_allowed = false
direct_replacement_allowed = false
backend_policy_mutation_allowed = false
fastest_candidate_auto_apply_allowed = false
tensorcube_matmul_replacement_enabled = false
subgroup_fast_path_enabled = false
```

## Native test status

Rust-native tests were not run in this container because `cargo` / `rustc` are unavailable.

## Static status

```text
PASS_STATIC_TCU_24O_WITH_NATIVE_TESTS_NOT_RUN
```
