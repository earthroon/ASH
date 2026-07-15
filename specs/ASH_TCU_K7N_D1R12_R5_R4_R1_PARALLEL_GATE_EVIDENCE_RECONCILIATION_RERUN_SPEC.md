# ASH-TCU-K7N-D1R12-R5-R4-R1 SPEC

## Parallel-Gate Evidence Reconciliation Rerun

### Patch identity

- Patch ID: `ASH-TCU-K7N-D1R12-R5-R4-R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN`
- PASS: `PASS_ASH_TCU_K7N_D1R12_R5_R4_R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_ROUTE_AUTHORITY_RECONCILED`
- HOLD: `HOLD_ASH_TCU_K7N_D1R12_R5_R4_R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_EVIDENCE_NOT_CONCLUSIVE`
- FAIL: `FAIL_ASH_TCU_K7N_D1R12_R5_R4_R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_PARENT_BINDING_OR_PROTECTED_STATE_VIOLATION`

## Purpose

Bind the conclusive repaired S05 branch and the conclusive S13 cold-start-only branch into one parallel-gate authority decision. This patch performs no latency replay, GPU dispatch, route mutation, bucket mutation, policy mutation, registry mutation, route-epoch advancement or production promotion.

Normal expected conclusion:

```text
S05 persistent authority=false
S13 persistent authority=false
combined persistent authority count=0
combined persistent effective weight=0
current hold evidence=superseded historical evidence only
```

The patch emits a deterministic, non-committing route-mutation input for a later mutation-plan patch.

## Required parents

### S05 parent

```text
patch=ASH-TCU-K7N-D1R12-R5-R3A-R3
execution=d1r12-r5-r3a-r3-0ba517ce6b0c8a27c181
outcome=zero_reproduced_red_branch_sealed
```

Required S05 state:

```text
target_a_persistence=not_reproduced
target_b_persistence=not_reproduced
reproduced_authoritative_red_bucket_count=0
reproduced_affected_effective_traffic_share=0
control_surface_status=clean
measurement_validity=true
s05_branch_status=conclusive
```

### S13 parent

```text
patch=ASH-TCU-K7N-D1R12-R5-R3B
execution=d1r12-r5-r3b-e6d3724554de93dc66a0
outcome=cold_start_only_transient
```

Required S13 state:

```text
cold_start_authoritative_red=true
warm_steady_authoritative_red=false
isolated_queue_authoritative_red=false
nominal_contention_authoritative_red=false
persistent_authoritative_red=false
persistent_effective_weight_contribution=0
control_authoritative_red_count=0
```

### Historical reconciliation parent

```text
patch=ASH-TCU-K7N-D1R12-R5-R4
execution=d1r12-r5-r4-0ddeb339a126f0debe29
outcome=s05_measurement_surface_contaminated
```

The historical recommendation is superseded by the repaired S05 branch.

## State ownership

R5-R3A-R3 owns the final S05 persistence, reproduced-red cardinality, reproduced effective share and clean-control result. R5-R3B owns the S13 cold-start observation, warm/steady non-persistence, control validity and target weight provenance.

R5-R4-R1 owns only normalized branch authority, identity compatibility, persistent authority cardinality, effective-weight reconciliation, evidence freshness, current hold support, a non-committing route recommendation and a route-mutation input.

## No-replay constitution

```text
replay_execution_count=0
gpu_dispatch_count=0
new_measurement_pair_count=0
new_process_epoch_count=0
child_process_count=0
```

## Normalized authority states

S05:

```text
branch_status=conclusive
persistent_authoritative_red=false
authoritative_red_bucket_count=0
persistent_effective_weight_contribution=0
measurement_validity=true
control_surface_valid=true
evidence_status=current
route_authority_contribution=false
```

S13:

```text
branch_status=conclusive
cold_start_transient_observed=true
persistent_authoritative_red=false
persistent_effective_weight_contribution=0
measurement_validity=true
control_surface_valid=true
evidence_status=current
route_authority_contribution=false
```

The S13 cold-start observation remains non-authoritative diagnostic history.

## Branch compatibility

Both route IDs must exist in the active D1R9 registry. Their route entries must share parent D1R8 identity, decision digest, whitelist digest, runtime authority, active registry epoch and Burn output authority. Parent protected-state receipts must confirm unchanged sampler, KV and aggregation-policy contracts.

Normal status:

```text
branch_compatibility_status=compatible
branch_independence_status=not_applicable_zero_authority
```

## Persistent authority and weight

```text
s05_persistent_authority_contribution_count=0
s13_persistent_authority_contribution_count=0
combined_persistent_authority_contribution_count=0
s05_persistent_effective_weight_contribution=0
s13_persistent_effective_weight_contribution=0
combined_persistent_effective_weight_contribution=0
```

Required integrity counters:

```text
duplicate_weight_contribution_count=0
unknown_weight_owner_count=0
superseded_weight_leak_count=0
transient_weight_leak_count=0
diagnostic_weight_leak_count=0
cross_branch_weight_alias_count=0
```

The S13 parent effective weight remains provenance only and contributes zero persistent authority because its observation is cold-start-only.

## Evidence freshness

Current:

```text
R5-R3A-R3=current
R5-R3B=current
```

Superseded or incorporated:

```text
R5-R3A=superseded
R5-R4=superseded
R5-R5E=superseded by R5-R3A-R3
R5-R3A-R1=superseded
R5-R3A-R2=incorporated into R5-R3A-R3
```

## Current hold decision

Required result:

```text
current_route_classification=conditional_hold
current_hold_evidence_status=superseded_historical_evidence_only
parallel_gate_route_authority_support=no_current_persistent_hold_support
route_authority_recommendation=retire_conditional_hold_preserve_shadow_observation_and_diagnostic_history
```

The recommendation is non-committing.

Semantic successor:

```text
proposed_successor_semantics=shadow_observation_without_route_hold
```

No concrete classification enum may be invented. If the active registry has no hold-retirement successor contract, emit:

```text
proposed_successor_classification=unresolved_active_registry_hold_retirement_contract
```

## Mutation eligibility

`route_hold_retirement_mutation_eligible=true` only when both parent outcomes and manifests match, both branches are conclusive and valid, branch compatibility is valid, combined persistent authority and weight are zero, all weight integrity counters are zero and protected state is unchanged.

Eligibility is not mutation.

## Outcomes

```text
parallel_gate_no_persistent_hold_support
s05_parent_semantic_contradiction
s13_parent_semantic_contradiction
branch_compatibility_invalid
branch_measurement_or_control_invalid
weight_reconciliation_invalid
parent_evidence_mismatch
protected_state_violation
```

Normal next state:

```text
ASH-TCU-K7N-D1R12-R5-R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN
```

## Required implementation files

```text
crates/model_core/src/vocab_atlas_shadow_parallel_gate_evidence_reconciliation_rerun_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r4_r1_parallel_gate_evidence_reconciliation_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r4_r1_parallel_gate_evidence_reconciliation.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend module is added.

## Required export seals

```text
ASH_TCU_K7N_D1R12_R5_R4_R1_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_MODEL_CRATE_ROOT_EXPORT_REPAIR_SEAL
ASH_TCU_K7N_D1R12_R5_R4_R1_ORCHESTRATOR_REPORT_SURFACE_SEAL
```

## Required runtime artifacts

```text
parent_reconciliation
s05_normalized_authority
s13_normalized_authority
branch_compatibility
branch_independence
persistent_authority_cardinality
effective_weight_reconciliation
evidence_freshness_registry
superseded_reconciliation_registry
parallel_gate_matrix
current_hold_support
route_authority_recommendation
route_mutation_input
branch_summary
determinism_audit
protected_state_guard
report
verdict
final_seal
local_manifest
```

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r4_r1/<execution_id>/
```

## Protected state

Before and after hashes must cover R5-R3A-R3, R5-R3B, historical R5-R4 and R5-R5E immutable artifact trees, the R2 policy, active route registry, route epoch and Burn backend source.

Required zero mutations:

```text
route_classification_change_count=0
bucket_classification_change_count=0
policy_mutation_count=0
effective_weight_mutation_count=0
registry_mutation_count=0
route_epoch_change_count=0
runtime_output_changed=false
output_authority=burn
```

## CLI contract

Binary:

```text
ash_tcu_k7n_d1r12_r5_r4_r1_parallel_gate_evidence_reconciliation
```

The implementation requires exactly 20 value arguments and 118 switches. The canonical PowerShell command is retained with the local full spec and bake handoff.

## Exit codes

```text
no persistent hold support=0
S05 or S13 semantic contradiction=5
branch measurement or control invalid=5
branch compatibility invalid=6
weight reconciliation invalid=7
parent evidence mismatch=8
protected state violation=70
```

## PASS meaning

PASS means S05 contributes no persistent authority, S13 contributes only cold-start diagnostic evidence, no persistent effective traffic weight remains and conditional-hold retirement is eligible for planning.

PASS does not remove the hold, mutate the registry, advance the route epoch, invent a successor enum, delete diagnostic history or promote TensorCube output.
