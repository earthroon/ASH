# TCU-21 — TensorCube Health Recommendation Review Gate / Operator Approval Queue

## Status

`PASS_TCU_21_TENSORCUBE_HEALTH_RECOMMENDATION_REVIEW_RECEIPT`

## SSOT

Input SSOT:

- `ash_pass3_TCU-20_tensorcube_long_horizon_health_ledger_backend_drift_score_baked.zip`

New TCU-21 scope:

- Intake TCU-20 `AshTensorCubeHealthRecommendation` candidate.
- Seal it into an operator review queue item.
- Seal operator decision receipt for approve / reject / hold / request-more-evidence.
- Preserve TCU-20 health ledger and ASH-50 ledger cross-reference fields.
- Keep approval as policy-update-candidate eligibility only.

## Implemented files

- `crates/ash_core/src/tensorcube_health_recommendation_review.rs`
- `crates/ash_core/tests/tcu_21_tensorcube_health_recommendation_review_gate.rs`
- `crates/ash_core/tests/tcu_21_operator_decision_receipt.rs`
- `crates/ash_core/tests/tcu_21_no_runtime_mutation.rs`
- `crates/orchestrator_local/src/tcu_21_tensorcube_health_recommendation_review_report.rs`
- `crates/orchestrator_local/src/bin/tcu_21_tensorcube_health_recommendation_review_audit.rs`
- `crates/orchestrator_local/tests/tcu_21_tensorcube_health_recommendation_review_report.rs`
- `workspace/runtime/tensorcube/ash_tensorcube_health_recommendation_review_queue_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_health_recommendation_review_receipt_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_health_recommendation_review_report_latest.json`

## Acceptance criteria

1. TCU-20 recommendation candidate is intaked as a pending review item.
2. Review item preserves `source_recommendation_id`.
3. Review item preserves `source_score_ids`.
4. Review item preserves `source_backend_drift_signal_ids`.
5. Review item preserves `source_tcu20_ledger_id` and `source_tcu20_last_entry_hash`.
6. Review item may preserve `source_ash50_ledger_id`.
7. Operator decisions support approve / reject / hold / request-more-evidence.
8. Request-more-evidence requires `requested_evidence_refs`.
9. Operator decision requires non-empty `operator_id`.
10. Operator decision requires non-empty `reason`.
11. Review receipt seals resulting status.
12. Approved receipt sets `approved_policy_update_candidate_allowed = true`.
13. Approved receipt still sets `runtime_mutation_allowed = false`.
14. Approved receipt still sets `backend_config_mutation_allowed = false`.
15. Approved receipt still sets `lora_attach_detach_allowed = false`.
16. Approved receipt still sets `safe_tensor_mode_apply_allowed = false`.
17. Existing TCU-20 ledger entries are not modified.
18. Review queue snapshot counts pending / approved / rejected / held / more-evidence states.
19. Review item hash excludes `reason` and `warnings`.
20. Review receipt hash excludes `reason` and `warnings`.
21. Append-only review item chain validates `previous_review_item_hash`.

## Non-opened gates

The following remain closed in TCU-21:

- Runtime mutation
- Backend config mutation
- LoRA attach / detach
- LoRA hot reload apply
- Safe tensor mode direct apply
- Automatic policy update
- Existing ledger correction by mutation

## Repro commands for Rust-capable environment

```bash
cargo test -p ash_core tcu_21_tensorcube_health_recommendation_review_gate
cargo test -p ash_core tcu_21_operator_decision_receipt
cargo test -p ash_core tcu_21_no_runtime_mutation
cargo test -p orchestrator_local tcu_21_tensorcube_health_recommendation_review_report
cargo run -p orchestrator_local --bin tcu_21_tensorcube_health_recommendation_review_audit
```

## Local container note

This bake container did not provide `cargo` or `rustc`, so native Rust tests could not be executed here. Static file creation and artifact integrity checks were performed instead.
