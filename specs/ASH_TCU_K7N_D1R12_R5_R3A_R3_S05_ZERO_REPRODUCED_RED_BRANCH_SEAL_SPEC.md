# ASH-TCU-K7N-D1R12-R5-R3A-R3 SPEC

## S05 Zero Reproduced Red Branch Seal

### Patch identity

- Patch ID: `ASH-TCU-K7N-D1R12-R5-R3A-R3_S05_ZERO_REPRODUCED_RED_BRANCH_SEAL`
- PASS: `PASS_ASH_TCU_K7N_D1R12_R5_R3A_R3_S05_ZERO_REPRODUCED_RED_BRANCH_SEAL_REPAIRED_EVIDENCE_AUTHORITY_CLOSED`
- HOLD: `HOLD_ASH_TCU_K7N_D1R12_R5_R3A_R3_S05_ZERO_REPRODUCED_RED_BRANCH_SEAL_PARENT_EVIDENCE_NOT_CONCLUSIVE`
- FAIL: `FAIL_ASH_TCU_K7N_D1R12_R5_R3A_R3_S05_ZERO_REPRODUCED_RED_BRANCH_SEAL_PARENT_BINDING_OR_PROTECTED_STATE_VIOLATION`

## Purpose

Close the repaired S05 evidence branch without another performance replay. The patch must seal:

- Target A persistence: `not_reproduced`
- Target B persistence: `not_reproduced`
- Repaired control authoritative-red count: `0`
- Reproduced authoritative-red target count: `0`
- Reproduced affected effective traffic share: `0`
- Current hold evidence: `stale_historical_evidence_only`
- Route authority support: `no_current_s05_route_hold_support`
- Non-committing recommendation: `retire_stale_s05_route_hold_preserve_diagnostic_history`

## Direct parent

Required R5-R3A-R2 state:

```text
execution_id=d1r12-r5-r3a-r2-a6afb5530c48b709bc9f
selected_outcome=target_b_nominal_stable_non_red
new_authoritative_red_segment_count=1
new_non_red_segment_count=11
new_indeterminate_segment_count=0
new_generation_pooled_authoritative_red=false
target_b_nominal_resolution=stable_non_red
control_authoritative_red_count=0
measurement_validity=true
recommended_target_b_persistence=not_reproduced
route_branch_recommendation=close_s05_replay_with_zero_reproduced_authoritative_red_buckets
```

Additional evidence parents:

```text
R5-R3A-R1 execution=d1r12-r5-r3a-r1-c942dc2153e48041d06f
R5-R3A-R1 outcome=measurement_indeterminate
R5-R5E execution=d1r12-r5-r5e-662d21d4f4a660b2614f
R5-R5E outcome=target_regression_reappears_under_repaired_protocol
original R5-R3A execution=d1r12-r5-r3a-4a90e29fdb0d0b0ee771
original R5-R3A outcome=s05_control_spillover
```

## Target and surface

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
shape_id=S05_M1_N1_K4
control_surface_id=b587d580b44201c3883993b87cd6ff732844ffbe034e53323245479e5d463e31
```

Required final target state:

```text
target_a_persistence=not_reproduced
target_b_persistence=not_reproduced
target_a_contributes_route_authority=false
target_b_contributes_route_authority=false
historical_authoritative_red_bucket_count=2
reproduced_authoritative_red_bucket_count=0
authoritative_red_retirement_count=2
```

Required control state:

```text
control_a_authoritative_red=false
control_b_authoritative_red=false
shared_control_authoritative_red=false
control_authoritative_red_count=0
control_surface_status=clean
```

## Evidence precedence

Target A:

```text
R5-R3A-R1 three-cohort replay
> R5-R5E repaired-protocol result
> original R5-R3A result
```

Target B:

```text
R5-R3A-R2 expanded nominal replay
> R5-R3A-R1 nominal discordance
> R5-R5E cohort-conditional result
> original R5-R3A result
```

## No-replay constitution

```text
replay_execution_count=0
gpu_dispatch_count=0
new_measurement_pair_count=0
new_process_epoch_count=0
child_process_count=0
```

No replay helper may be called by this patch.

## Weight authority

Required canonical equality:

```text
target_a_canonical_effective_weight + target_b_canonical_effective_weight
= 0.0174244486795535
```

Required integrity:

```text
effective_weight_sum_exact=true
duplicate_weight_contribution_count=0
unknown_weight_owner_count=0
diagnostic_weight_leak_count=0
non_authoritative_weight_leak_count=0
dimension_expanded_weight_multiplication_count=0
```

Final authority values:

```text
target_a_reproduced_effective_weight=0
target_b_reproduced_effective_weight=0
reproduced_affected_effective_traffic_share=0
bucket_independence_status=no_reproduced_pair
```

Canonical weights are preserved. Only evidence eligibility becomes zero.

## Superseded evidence registry

The branch seal must register five superseded conclusions:

1. Original R5-R3A target authority conclusion
2. Original R5-R3A control spillover conclusion
3. R5-R4 measurement-surface contamination conclusion
4. R5-R5E Target B cohort-conditional conclusion
5. R5-R3A-R1 Target B nominal discordance and indeterminate branch conclusion

Parent artifacts remain immutable and are not deleted.

## Route authority

```text
historical_route_classification=conditional_hold
current_hold_evidence_status=stale_historical_evidence_only
route_authority_support=no_current_s05_route_hold_support
route_authority_recommendation=retire_stale_s05_route_hold_preserve_diagnostic_history
recommendation_non_committing=true
s05_branch_status=conclusive
```

R5-R3A-R3 does not mutate the active route classification. R5-R4-R1 owns reconciliation.

## Outcomes

Primary PASS outcome:

```text
zero_reproduced_red_branch_sealed
```

Other outcomes:

```text
residual_reproduced_red_detected
control_surface_not_clean
weight_provenance_invalid
parent_evidence_not_conclusive
parent_evidence_mismatch
protected_state_violation
```

Priority:

```text
protected state violation
> parent mismatch
> parent not conclusive
> weight invalid
> control not clean
> residual red
> zero-red branch sealed
```

## Next state

```text
ASH-TCU-K7N-D1R12-R5-R4-R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN
```

R5-R4-R1 must bind the R5-R3A-R3 execution, selected outcome, final seal, local manifest and reconciliation input together with the existing R5-R3B evidence branch.

## Implementation surface

```text
crates/model_core/src/vocab_atlas_shadow_s05_zero_reproduced_red_branch_seal_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r3a_r3_zero_reproduced_red_branch_seal_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r3a_r3_zero_reproduced_red_branch_seal.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend module is added.

Required export seals:

```text
ASH_TCU_K7N_D1R12_R5_R3A_R3_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R3_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R3_MODEL_CRATE_ROOT_EXPORT_REPAIR_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R3_ORCHESTRATOR_REPORT_SURFACE_SEAL
```

## Required artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r3a_r3/<execution_id>/
```

Latest mirrors include parent reconciliation, target evidence precedence, target final state, control final state, weight provenance, reproduced share, independence final state, superseded evidence registry, stale hold classification, route recommendation, branch summary, R5-R4-R1 reconciliation input, determinism audit, protected-state guard, report, verdict, final seal and local manifest.

All loaded parent artifacts must match the SHA-256 entries in their parent local manifests.

## Protected state

Required zero mutation counts:

```text
parent_artifact_rewrite_count=0
measurement_protocol_mutation_count=0
control_surface_mutation_count=0
contention_contract_mutation_count=0
route_classification_change_count=0
bucket_classification_change_count=0
policy_mutation_count=0
threshold_mutation_count=0
effective_weight_mutation_count=0
registry_mutation_count=0
route_epoch_change_count=0
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
output_authority=burn
runtime_output_changed=false
```

## PASS meaning

PASS means the repaired S05 evidence branch is complete, both target regressions are non-reproduced, the control surface is clean, reproduced route-authority share is zero, and a deterministic non-committing R5-R4-R1 input has been generated.

PASS does not remove the active hold, rewrite route or bucket health, mutate policy, delete historical evidence, modify S13, promote TensorCube output or establish production readiness.
