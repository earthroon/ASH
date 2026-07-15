# ASH-TCU-K7N-D1R12-R5-R4-R1-R2

## PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_WITH_REPAIRED_IDENTITY_BINDING

## 1. Patch identity

```text
patch_id=ASH-TCU-K7N-D1R12-R5-R4-R1-R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_WITH_REPAIRED_IDENTITY_BINDING
PASS=PASS_ASH_TCU_K7N_D1R12_R5_R4_R1_R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_REPAIRED_IDENTITY_AND_RUNTIME_AUTHORITY_RECONCILED
HOLD=HOLD_ASH_TCU_K7N_D1R12_R5_R4_R1_R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_REPAIR_EVIDENCE_NOT_CONCLUSIVE
FAIL=FAIL_ASH_TCU_K7N_D1R12_R5_R4_R1_R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_PARENT_BINDING_OR_PROTECTED_STATE_VIOLATION
```

## 2. Purpose

Recompute the R5-R4-R1 parallel-gate evidence decision after binding:

1. R5-R4-R1-R1 identity repair evidence;
2. R5-R4-R1-R1-R1 runtime applicability evidence;
3. final S05 and S13 persistence evidence;
4. the active D1R9 route registry and R2 aggregation policy.

The patch is evidence-only. It does not replay measurements, execute the sampler, allocate or append KV state, mutate route health, change the registry, advance the route epoch, or promote TensorCube output.

## 3. Required parents

```text
R5-R4-R1-R1-R1 execution=d1r12-r5-r4-r1-r1-r1-da7a5c7289b58773602e
R5-R4-R1-R1-R1 outcome=branch_local_fields_removed_from_shared_identity

R5-R4-R1-R1 execution=d1r12-r5-r4-r1-r1-30b3cfbcc502474baf95
R5-R4-R1-R1 outcome=sampler_or_kv_contract_incompatible

R5-R4-R1 execution=d1r12-r5-r4-r1-0fa8776fe8b41b5ef209
R5-R4-R1 outcome=branch_compatibility_invalid

S05 execution=d1r12-r5-r3a-r3-0ba517ce6b0c8a27c181
S05 outcome=zero_reproduced_red_branch_sealed

S13 execution=d1r12-r5-r3b-e6d3724554de93dc66a0
S13 outcome=cold_start_only_transient
```

Every consumed artifact must be present in its parent local manifest and match its SHA-256 entry.

## 4. Scope and identity constitution

```text
parallel_gate_scope_id=parallel_gate_scope:ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58|ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
scope_member_count=2
route_identity_comparison_mode=distinct_members_same_parallel_scope
shape_identity_comparison_mode=branch_specific_shape
decision_digest_ownership=branch_local_route_decision
decision_digest_excluded_from_shared_model_identity=true
```

S05 and S13 remain different physical routes. Compatibility is based on scope membership, branch-role ownership, shared D1R8 parent generation, whitelist digest, runtime authority, registry epoch, Burn output authority, and the repaired runtime applicability receipt. Route-specific decision digests are not shared model identity.

## 5. Runtime applicability

Required direct-parent receipt state:

```text
combined_runtime_contract_compatibility=compatible_after_branch_local_exclusion
sampler_runtime_applicability=not_applicable_non_invoked
kv_runtime_applicability=not_applicable_non_invoked
legacy_omitted_receipt_count=4
authority_relevant_mismatch_count=0
missing_required_receipt_count=0
r5_r4_r1_r2_reconciliation_rerun_eligible=true
```

No missing sampler or KV value may be silently substituted. Non-applicability is valid only because the S05 and S13 branches are TensorCube measurement branches and the runtime audit sealed the non-invocation proof.

## 6. Branch semantics

### S05

```text
target_a_persistence=not_reproduced
target_b_persistence=not_reproduced
persistent_authority=false
persistent_effective_weight=0
reproduced_authoritative_red_bucket_count=0
reproduced_affected_effective_traffic_share=0
historical_authoritative_red_bucket_count=2
measurement_validity=true
control_surface_status=clean
control_authoritative_red_count=0
```

### S13

```text
cold_start_authoritative_red=true
warm_steady_authoritative_red=false
isolated_queue_authoritative_red=false
nominal_contention_authoritative_red=false
single_red_persistence_status=cold_start_only_transient
persistent_authority=false
persistent_effective_weight=0
control_authoritative_red_count=0
```

Repair receipts may repair identity ownership and runtime applicability only. They cannot rewrite branch performance evidence.

## 7. Reconciliation result

Normal result:

```text
repaired_branch_compatibility_status=compatible_after_identity_and_runtime_repair
remaining_failed_dimension_count=0
remaining_indeterminate_dimension_count=0
branch_independence_status=not_applicable_zero_authority
persistent_authority_owner_count=0
combined_persistent_authority_contribution_count=0
combined_persistent_effective_weight_contribution=0
effective_weight_reconciliation_status=exact_zero
```

Required weight integrity:

```text
duplicate_weight_contribution_count=0
unknown_weight_owner_count=0
superseded_weight_leak_count=0
transient_weight_leak_count=0
diagnostic_weight_leak_count=0
cross_branch_weight_alias_count=0
```

## 8. Hold evidence and recommendation

```text
current_route_classification=conditional_hold
current_hold_evidence_status=superseded_historical_evidence_only
parallel_gate_route_authority_support=no_current_persistent_hold_support
route_authority_recommendation=retire_conditional_hold_preserve_shadow_observation_and_diagnostic_history
proposed_successor_semantics=shadow_observation_without_route_hold
```

Historical red evidence remains immutable diagnostic history. The S13 cold-start transient remains diagnostic and cannot support persistent route hold authority.

Eligibility is separated:

```text
route_hold_retirement_evidence_eligible=true
route_hold_retirement_plan_eligible=true
route_hold_retirement_mutation_eligible=not_evaluated_reconciliation_only
```

The exact successor classification is not hardcoded. If the active registry does not expose an exact post-hold enum, resolution is deferred:

```text
successor_classification_resolution_status=deferred_to_r5_r6_active_registry_contract
proposed_successor_classification=unresolved_until_retirement_mutation_plan
```

## 9. State ownership

- S05 parent owns S05 measurement, control, persistence, authority and weight.
- S13 parent owns S13 transient classification, measurement, control, authority and weight.
- R5-R4-R1-R1 owns scope membership, branch roles and decision-digest ownership.
- R5-R4-R1-R1-R1 owns runtime applicability and legacy omitted-receipt classification.
- Active D1R9 registry owns route entries, registry generation and route epoch.
- R5-R4-R1-R2 owns the final repaired reconciliation, hold-support decision, evidence eligibility and R5-R6 plan input.
- R5-R4-R1-R2 does not own or perform the actual mutation.

## 10. Required implementation

```text
crates/model_core/src/vocab_atlas_shadow_parallel_gate_evidence_reconciliation_repaired_identity_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r4_r1_r2_parallel_gate_evidence_reconciliation_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r4_r1_r2_parallel_gate_evidence_reconciliation.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend module is added.

## 11. Required export seals

```text
ASH_TCU_K7N_D1R12_R5_R4_R1_R2_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_R2_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_R2_MODEL_CRATE_ROOT_EXPORT_REPAIR_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_R2_ORCHESTRATOR_REPORT_SURFACE_SEAL
```

The binary must resolve the contract and all model seals from the `model_core` crate root.

## 12. Required output artifacts

```text
parent_reconciliation
identity_repair_binding
runtime_compatibility_binding
s05_normalized_authority
s13_normalized_authority
repaired_branch_compatibility
branch_independence
persistent_authority_cardinality
effective_weight_reconciliation
evidence_freshness_registry
historical_evidence_registry
parallel_gate_matrix
current_hold_support
route_authority_recommendation
successor_classification_resolution
reconciliation_receipt
hold_retirement_plan_input
determinism_audit
protected_state_guard
report
verdict
final_seal
local_manifest
```

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r4_r1_r2/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r5_r4_r1_r2_*_latest.json
```

## 13. Protected-state requirements

```text
parent_artifact_rewrite_count=0
replay_execution_count=0
gpu_dispatch_count=0
new_measurement_pair_count=0
route_classification_change_count=0
bucket_classification_change_count=0
policy_mutation_count=0
effective_weight_mutation_count=0
registry_mutation_count=0
route_epoch_change_count=0
sampler_contract_mutation_count=0
kv_contract_mutation_count=0
production_output_commit_count=0
output_authority=burn
runtime_output_changed=false
```

The full semantic reconciliation must be recomputed twice and produce an exact digest match.

## 14. Outcomes and exit codes

```text
parallel_gate_no_persistent_hold_support_reconciled=0
repaired_identity_receipt_invalid=5
runtime_compatibility_receipt_invalid=5
branch_semantics_drifted=5
persistent_authority_reintroduced=6
current_hold_support_still_present=6
effective_weight_reconciliation_invalid=7
parent_evidence_mismatch=8
protected_state_violation=70
```

Outcome priority:

```text
protected state violation
parent evidence mismatch
identity receipt invalid
runtime receipt invalid
branch semantics drifted
persistent authority reintroduced
effective-weight invalid
current hold support present
normal reconciliation PASS
```

## 15. Normal PASS and next state

```text
selected_outcome=parallel_gate_no_persistent_hold_support_reconciled
next_state=ASH-TCU-K7N-D1R12-R5-R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN
```

PASS means the repaired identity and runtime receipts are valid, S05 and S13 both contribute zero persistent authority and zero persistent weight, and no current evidence supports `conditional_hold`.

PASS does not mean that the hold was already removed, the registry was mutated, the route epoch advanced, or TensorCube became production-authoritative.

## 16. CLI contract

```text
value_argument_count=28
switch_flag_count=116
```

The complete command is delivered separately as `R5_R4_R1_R2_CARGO_RUN.txt`. No PowerShell script is part of this patch.
