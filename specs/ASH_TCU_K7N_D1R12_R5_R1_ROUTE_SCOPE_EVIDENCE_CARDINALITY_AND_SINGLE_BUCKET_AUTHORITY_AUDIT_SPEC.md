# ASH-TCU-K7N-D1R12-R5-R1 SPEC

## Route-Scope Evidence Cardinality and Single-Bucket Authority Audit

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D1R12-R5-R1_ROUTE_SCOPE_EVIDENCE_CARDINALITY_AND_SINGLE_BUCKET_AUTHORITY_AUDIT`
- Normal audit PASS: `PASS_ASH_TCU_K7N_D1R12_R5_R1_ROUTE_SCOPE_EVIDENCE_CARDINALITY_AND_SINGLE_BUCKET_AUTHORITY_AUDIT_PROVENANCE_RESOLVED_PARENT_IMMUTABLE`
- Hard failure: `FAIL_ASH_TCU_K7N_D1R12_R5_R1_ROUTE_SCOPE_EVIDENCE_CARDINALITY_AND_SINGLE_BUCKET_AUTHORITY_AUDIT_PROVENANCE_OR_PROTECTED_STATE_VIOLATION`
- GitHub path: `specs/ASH_TCU_K7N_D1R12_R5_R1_ROUTE_SCOPE_EVIDENCE_CARDINALITY_AND_SINGLE_BUCKET_AUTHORITY_AUDIT_SPEC.md`

Patch class:

```text
route-scope evidence provenance audit
+ affected-dimension cardinality reconstruction
+ single-bucket weight/authority semantic separation
+ authoritative-red relationship graph
+ non-committing counterfactual classifications
+ source ownership audit
+ no replay execution
+ no route-health mutation
+ no aggregation-policy mutation
+ no threshold relaxation
+ no parent rewrite
+ Burn authority preserved
```

## 2. Direct Parent

Required parent:

```text
ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR
execution_id=d1r12-r4-69c1e6aec6a09d5506f1
selected_outcome=non_coverage_policy_regression_persists
```

Required parent summary:

```text
active_route_count=17
canonical_bucket_count=1401
parent_attempt_count=49152
topup_attempt_count=14270
merged_attempt_count=63422
underfloor_bucket_count_after=0

healthy_route_count=9
amber_route_count=6
conditional_hold_route_count=2
confirmed_hold_route_count=0
observation_hold_route_count=0
invalid_route_count=0
classification_drift_count=8

deterministic_recompute=true
output_authority=burn
runtime_output_changed=false
```

Required bucket distribution:

```text
healthy=686
diagnostic_only=659
amber=53
confirmed_critical_path_red=3
```

## 3. Trigger Evidence

### S05

```text
route=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
confirmed_red_bucket_count=2
affected_dimension_count=4
affected_effective_traffic_share=0.0174244486795535
replay_classification=conditional_hold
```

The two red buckets differ across sequence, KV and cadence, while both use light contention.

### S13

```text
route=ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
confirmed_red_bucket_count=1
affected_dimension_count=4
affected_effective_traffic_share=0.014705882352941176
replay_classification=conditional_hold
```

The single red bucket is `very_long × high × sustained_burst × nominal`.

## 4. Purpose

R5-R1 must reconstruct the exact path:

```text
merged bucket health
→ authoritative-red selection
→ dimension-value sets
→ affected_dimension_count
→ effective traffic accumulation
→ weight cap
→ confirmed route-wide gate
→ conditional gate
→ final route classification
```

The audit must distinguish:

1. structural dimension slot count;
2. unique authoritative-red bucket count;
3. distinct values per dimension;
4. dimensions with more than one red value;
5. single-axis corroboration pairs;
6. effective traffic share;
7. per-bucket effective-weight cap;
8. route-wide authority semantics.

No one domain may silently substitute for another.

## 5. State Ownership

R2 owns aggregation thresholds and policy values.

R4 owns persisted merged bucket and route receipts.

R5-R1 owns only:

```text
source provenance
cardinality domain matrix
red-bucket relationship graph
weight-cap semantic audit
route-scope projection trace
counterfactual non-committing classifications
audit verdict and next-state contract
```

R5-R1 does not own or mutate route classification.

## 6. Confirmed Source Questions

The local Rust audit must inspect and hash:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_route_health.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_bucket_health.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r2_route_scope.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r2_aggregation_policy.rs
```

It must determine whether the current R3 route-health implementation:

```text
creates one set per dimension
inserts every authoritative-red bucket value into all four sets
counts how many dimension sets are non-empty
```

If so, one red bucket produces `affected_dimension_count=4`.

This is classified as:

```text
dimension_slot_count_used_as_evidence_cardinality
```

## 7. Cardinality Domains

For S05 and S13, derive all of the following.

### Dimension slot count

```text
4
```

### Authoritative-red bucket count

```text
S05=2
S13=1
```

### Distinct value counts

Expected:

```text
S05:
sequence=2
kv=2
cadence=2
contention=1

S13:
sequence=1
kv=1
cadence=1
contention=1
```

### Varied dimension count

A dimension is varied only when the red set contains more than one value.

```text
S05=3
S13=0
```

### Single-axis corroboration

Two red buckets corroborate one axis only when they differ on exactly one dimension and match on the other three.

Expected:

```text
S05=0
S13=0
```

The S05 pair has Hamming distance 3.

## 8. Effective Traffic Audit

Required arithmetic:

```text
S05:
0.00871222433977675 + 0.00871222433977675
= 0.0174244486795535

S13:
0.014705882352941176
```

The audit must prove:

```text
no duplicate red-bucket weight
no dimension-expanded weight multiplication
no diagnostic-red double count
```

## 9. Single-Bucket Cap Semantics

The loaded R2 policy contains:

```text
single_bucket_weight_cap=0.25
route_wide_min_red_bucket_count=2
route_wide_min_affected_share=0.40
route_wide_min_dimension_count=2
```

R5-R1 must distinguish:

```text
per-bucket effective-weight cap
vs
single-bucket route-authority cap
```

A weight cap is not an authority cap.

The audit must record whether an authority cap exists at all, and must not claim a bypass when only a weight cap exists.

## 10. Route-Scope Causality Trace

For each audited route, report which gate prevented confirmed hold.

### S05 expected trace

```text
red_count gate: pass
affected-share gate: fail
cardinality gate: pass under current implementation
confirmed gate: fail
conditional gate: pass
```

Therefore current cardinality is not causal to S05 conditional hold. The affected-share threshold is causal to failure of confirmed hold, while any-red conditional fallback selects conditional hold.

### S13 expected trace

```text
red_count gate: fail
affected-share gate: fail
cardinality gate: pass under current implementation
confirmed gate: fail
conditional gate: pass
```

Therefore current cardinality is not causal to S13 conditional hold. The minimum red-bucket count is already insufficient for confirmed hold, while any-red conditional fallback selects conditional hold.

## 11. Counterfactual Models

Compute without committing:

1. current implementation;
2. unique-red-bucket cardinality;
3. varied-dimension cardinality;
4. single-axis corroboration cardinality;
5. strict single-bucket route-authority cap.

The current model must reproduce:

```text
S05=conditional_hold
S13=conditional_hold
```

The strict authority-cap model may downgrade S13 to bounded amber, but this is diagnostic only and must not mutate R4.

## 12. Audit Findings

Possible findings:

```text
DimensionSlotCountUsedAsEvidenceCardinality
SingleBucketMultiDimensionContribution
SingleBucketAuthorityCapBypass
SingleBucketAuthorityCapAbsent
EffectiveTrafficDoubleCount
MultiAxisPairMisclassifiedAsIndependentCorroboration
PolicySemanticAmbiguity
CurrentSemanticsReproducedNoImplementationDefect
ParentEvidenceInconsistent
```

Expected source-level finding:

```text
DimensionSlotCountUsedAsEvidenceCardinality=true
SingleBucketMultiDimensionContribution=true
SingleBucketAuthorityCapBypass=false unless a real authority cap is found
```

## 13. Outcomes

Exactly one outcome:

```text
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_CARDINALITY_ALIASING_CONFIRMED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_SINGLE_BUCKET_AUTHORITY_CAP_BYPASS_CONFIRMED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_MIXED_CARDINALITY_AND_CAP_DEFECT_CONFIRMED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_CURRENT_ROUTE_SCOPE_SEMANTICS_REPRODUCED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_POLICY_SEMANTICS_AMBIGUOUS
OUTCOME_ASH_TCU_K7N_D1R12_R5_R1_PARENT_EVIDENCE_INCONSISTENT
```

Priority:

```text
parent inconsistency
mixed defect
cap bypass
cardinality aliasing
policy ambiguity
current semantics reproduced
```

A conclusive defect is a successful audit and returns process exit code 0.

## 14. Required Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r1/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/
```

Required:

```text
ash_tensorcube_k7n_d1r12_r5_r1_parent_reconciliation_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_authoritative_red_bucket_index_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_source_cardinality_trace_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_bucket_dimension_contributions_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_red_bucket_relationship_graph_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_cardinality_domain_matrix_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_single_bucket_authority_cap_audit_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_route_scope_projection_trace_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_effective_traffic_audit_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_s05_counterfactual_classifications_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_s13_counterfactual_classifications_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_source_ownership_audit_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_determinism_audit_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_protected_state_guard_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_audit_summary_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_report_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_verdict_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_final_seal_latest.json
ash_tensorcube_k7n_d1r12_r5_r1_local_manifest_latest.json
```

All must be generated by local Rust.

## 15. Protected State

Before and after hash:

```text
R4 immutable artifact directory
R2 aggregation policy
active route registry
route epoch owner
```

Required:

```text
parent artifacts unchanged=true
aggregation policy unchanged=true
route registry unchanged=true
route epoch unchanged=true
replay execution count=0
route-health mutation count=0
threshold mutation count=0
output_authority=burn
runtime_output_changed=false
```

## 16. Implementation Surface

Backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r1_route_scope_audit.rs
```

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_route_scope_evidence_cardinality_audit_contract.rs
```

Orchestrator report:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r1_route_scope_evidence_cardinality_audit_report.rs
```

Binary:

```text
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r1_route_scope_evidence_cardinality_audit.rs
```

Registration:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Normal crate exports are mandatory. Direct `#[path = ...]` source inclusion from the orchestrator binary is forbidden.

## 17. Normal Audit PASS Conditions

```text
parent R4 exact=true
three authoritative-red buckets exact=true
S05 and S13 route receipts exact=true
source producer unique=true
cardinality domains complete=true
weight-cap semantics resolved=true
effective traffic arithmetic exact=true
current model reproduced=true
counterfactuals deterministic=true
one outcome selected=true
parent artifacts unchanged=true
policy unchanged=true
registry unchanged=true
route epoch unchanged=true
output authority=burn
runtime output changed=false
```

## 18. Expected Outcome

Expected from the current source, but not hard-coded as a substitute for audit:

```text
selected_outcome=cardinality_aliasing_confirmed
cardinality_aliasing_confirmed=true
single_bucket_authority_cap_bypass_confirmed=false
single_bucket_authority_cap_absent=true
```

Expected causal separation:

```text
cardinality_gate_causal_to_s05_classification=false
cardinality_gate_causal_to_s13_classification=false
affected_share_gate_causal_to_s05_classification=true
red_count_gate_causal_to_s13_classification=true
```

## 19. Next-State Contract

For cardinality aliasing:

```text
ASH-TCU-K7N-D1R12-R5-R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR
```

The next patch must repair the meaning of `affected_dimension_count` without rewriting R4 evidence. A later targeted persistence replay remains required to determine whether the three p95 red buckets persist after semantic repair.

R5-R1 authorizes no threshold change, no route-health mutation, no replay expansion and no TensorCube output promotion.
