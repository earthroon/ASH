# TCU-22 — TensorCube Backend Policy Update Candidate / Feature-Gated Apply

## Status

`PASS_STATIC_TCU_22_WITH_NATIVE_TESTS_NOT_RUN`

## SSOT

Base ZIP:

`ash_pass3_TCU-21_tensorcube_health_recommendation_review_gate_baked.zip`

This bake adds TCU-22 on top of the TCU-21 operator approval queue. TCU-22 consumes an approved TCU-21 review receipt and seals only backend policy update candidate / feature gate / dry-run apply plan receipt artifacts.

## Acceptance Criteria

1. TCU-21 Approved review receipt can be intaken as a backend policy update candidate.
2. Non-approved TCU-21 receipts are rejected.
3. Receipts with `approved_policy_update_candidate_allowed = false` are rejected.
4. Receipts that try to open runtime/backend/LoRA/safe tensor mutation are rejected.
5. Candidate preserves `source_review_receipt_id`, `source_review_item_id`, and `source_recommendation_id`.
6. Candidate preserves TCU-20 ledger ID and last entry hash cross-reference.
7. Candidate preserves ASH-50 ledger ID cross-reference.
8. Feature gate supports `Disabled`, `CandidateOnly`, and `DryRunOnly`.
9. Only `DryRunOnly` can create a dry-run apply plan receipt.
10. Direct backend apply is never allowed.
11. Backend config mutation is never allowed.
12. Runtime mutation is never allowed.
13. LoRA attach/detach is never allowed.
14. Safe tensor mode direct apply is never allowed.
15. Dry-run apply plan receipt contains `proposed_policy_diff_summary`.
16. Candidate hash chain excludes `reason` and `warnings`.
17. Existing TCU-21 receipt, TCU-20 ledger, and ASH-50 ledger are not modified.

## Sealed Policy

```text
Approved review receipt permits candidate generation, not backend mutation.
```

## Added Core Files

```text
crates/ash_core/src/tensorcube_backend_policy_update_candidate.rs
crates/ash_core/tests/tcu_22_policy_update_candidate_from_approved_review.rs
crates/ash_core/tests/tcu_22_feature_gate_apply_blockers.rs
crates/ash_core/tests/tcu_22_no_backend_config_mutation.rs
crates/ash_core/tests/tcu_22_policy_update_candidate_hash_chain.rs
```

## Added Orchestrator Files

```text
crates/orchestrator_local/src/tcu_22_tensorcube_backend_policy_update_candidate_report.rs
crates/orchestrator_local/src/bin/tcu_22_tensorcube_backend_policy_update_candidate_audit.rs
crates/orchestrator_local/tests/tcu_22_tensorcube_backend_policy_update_candidate_report.rs
```

## Added Runtime Snapshots

```text
workspace/runtime/tensorcube/ash_tensorcube_backend_policy_update_candidate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_backend_policy_feature_gate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_backend_policy_apply_plan_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_backend_policy_update_report_latest.json
```

## Mutation Seal

The following are sealed false in candidate, gate, and dry-run apply plan receipt:

```text
runtime_mutation_allowed = false
backend_config_mutation_allowed = false
lora_attach_detach_allowed = false
safe_tensor_mode_apply_allowed = false
direct_apply_allowed = false
```

## Native Test Commands

Run in a Rust-capable environment:

```bash
cargo test -p ash_core tcu_22_policy_update_candidate_from_approved_review
cargo test -p ash_core tcu_22_feature_gate_apply_blockers
cargo test -p ash_core tcu_22_no_backend_config_mutation
cargo test -p ash_core tcu_22_policy_update_candidate_hash_chain
cargo test -p orchestrator_local tcu_22_tensorcube_backend_policy_update_candidate_report
cargo run -p orchestrator_local --bin tcu_22_tensorcube_backend_policy_update_candidate_audit
```

## Native Test Status

Native Rust tests were not run in this bake environment because `cargo` / `rustc` are unavailable.
