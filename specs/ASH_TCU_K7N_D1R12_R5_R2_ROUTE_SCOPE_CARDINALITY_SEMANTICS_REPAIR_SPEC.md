# ASH-TCU-K7N-D1R12-R5-R2 SPEC

## Route-Scope Cardinality Semantics Repair

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D1R12-R5-R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR`
- PASS marker: `PASS_ASH_TCU_K7N_D1R12_R5_R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR_EXPLICIT_DOMAINS_PARENT_CLASSIFICATION_PRESERVED`
- Failure marker: `FAIL_ASH_TCU_K7N_D1R12_R5_R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR_SEMANTIC_PROJECTION_OR_PROTECTED_STATE_VIOLATION`
- GitHub path: `specs/ASH_TCU_K7N_D1R12_R5_R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR_SPEC.md`

Patch class:

```text
route-scope cardinality semantic repair
+ ambiguous receipt-field retirement
+ explicit cardinality-domain introduction
+ semantic overlay generation
+ source/report SSOT convergence
+ historical parent receipt preservation
+ route classification preservation
+ aggregation-policy preservation
+ no replay
+ no threshold mutation
+ no promotion
```

## 2. Direct Parents

### R4 runtime parent

```text
execution_id=d1r12-r4-69c1e6aec6a09d5506f1
selected_outcome=non_coverage_policy_regression_persists
active_route_count=17
canonical_bucket_count=1401
authoritative_red_bucket_count=3
healthy_route_count=9
amber_route_count=6
conditional_hold_route_count=2
confirmed_hold_route_count=0
observation_hold_route_count=0
invalid_route_count=0
classification_drift_count=8
output_authority=burn
```

### R5-R1 audit parent

```text
execution_id=d1r12-r5-r1-7a8b3d1656b3d6213586
selected_outcome=cardinality_aliasing_confirmed
cardinality_aliasing_confirmed=true
single_bucket_authority_cap_bypass_confirmed=false
single_bucket_authority_cap_absent=true
cardinality_gate_causal_to_s05_classification=false
cardinality_gate_causal_to_s13_classification=false
affected_share_gate_causal_to_s05_classification=true
red_count_gate_causal_to_s13_classification=true
```

## 3. Confirmed Defect

The R4 route receipt field `affected_dimension_count` is produced by counting whether the four authoritative-red value sets are non-empty:

```text
sequence_bucket
kv_bucket
cadence_class
contention_class
```

One red bucket populates all four sets, so one red bucket can serialize as:

```text
affected_dimension_count=4
```

The value does not mean four independent causal dimensions, four independent red observations, four evidence families, or four corroborated axes. The field name therefore overstates its semantic authority.

The R5-R1 audit also proved that this aliasing did not cause the two conditional holds:

```text
S05 conditional_hold cause=affected_effective_traffic_share gate
S13 conditional_hold cause=authoritative_red_bucket_count gate
```

R5-R2 must repair the semantic projection without changing either classification.

## 4. Purpose

R5-R2 must:

1. establish one canonical owner for route-scope cardinality semantics;
2. separate structural slots, red-bucket count, distinct values, varied domains and single-axis corroboration;
3. deprecate `affected_dimension_count` as an authoritative field;
4. preserve all 17 R4 route classifications;
5. preserve all 1,401 bucket classifications;
6. preserve S05 and S13 causal-gate findings;
7. write a non-destructive semantic overlay keyed by parent route receipt digest;
8. preserve R2 policy, registry, route epoch and Burn authority;
9. authorize no replay, threshold change or route-health promotion.

## 5. Ownership

### R2 owns

```text
aggregation thresholds
route-scope gate thresholds
health precedence
effective-share semantics
red-count gate semantics
single-bucket weight cap
```

### R4 owns

```text
merged bucket evidence
bucket classifications
route classifications
classification drift
runtime outcome
```

### R5-R1 owns

```text
cardinality provenance audit
causal-gate findings
cap-semantics findings
```

### R5-R2 owns

```text
corrected cardinality vocabulary
route semantic overlay schema
legacy deprecation metadata
semantic parity audit
source ownership audit
R5-R2 report, verdict and seal
```

R5-R2 does not own classification policy or runtime state.

## 6. Explicit Semantic Domains

### 6.1 `dimension_slot_count`

Number of workload fields in the canonical key.

```text
dimension_slot_count=4
```

Structural only. Not evidence authority.

### 6.2 `authoritative_red_bucket_count`

Number of unique authoritative-red canonical buckets.

```text
S05=2
S13=1
```

### 6.3 Distinct red values by domain

```text
distinct_red_sequence_value_count
distinct_red_kv_value_count
distinct_red_cadence_value_count
distinct_red_contention_value_count
```

Expected:

```text
S05 sequence=2 kv=2 cadence=2 contention=1
S13 sequence=1 kv=1 cadence=1 contention=1
```

### 6.4 `varied_red_domain_count`

Number of domains containing more than one authoritative-red value.

```text
S05=3
S13=0
```

### 6.5 `single_axis_corroborated_domain_count`

Number of domains for which at least one authoritative-red pair differs only in that domain and matches in the other three.

```text
S05=0
S13=0
```

### 6.6 `independent_red_evidence_family_count`

No production policy currently defines an evidence family relation. R5-R2 must serialize:

```text
independent_red_evidence_family_count=null
independent_red_evidence_family_policy=not_authorized
```

### 6.7 `affected_effective_traffic_share`

Remains valid and means the sum of authoritative-red effective weights after per-bucket weight capping. It must not be multiplied by any dimension count.

## 7. Legacy Field Retirement

The parent field remains available only as a compatibility value:

```text
legacy_affected_dimension_count
legacy_affected_dimension_semantics=non_empty_authoritative_red_domain_set_count
legacy_field_deprecated=true
legacy_field_authoritative=false
```

It must not be read by new route-classification or promotion control flow.

## 8. New Route Semantic Receipt

```rust
pub struct D1R12R5R2RouteScopeSemanticReceipt {
    pub route_id: String,
    pub shape_id: String,
    pub parent_route_receipt_digest: String,
    pub parent_r4_classification: String,
    pub preserved_classification: String,
    pub classification_preserved: bool,
    pub dimension_slot_count: usize,
    pub authoritative_red_bucket_count: usize,
    pub distinct_red_sequence_value_count: usize,
    pub distinct_red_kv_value_count: usize,
    pub distinct_red_cadence_value_count: usize,
    pub distinct_red_contention_value_count: usize,
    pub varied_red_domain_count: usize,
    pub single_axis_corroborated_domain_count: usize,
    pub independent_red_evidence_family_count: Option<usize>,
    pub independent_red_evidence_family_policy: String,
    pub legacy_affected_dimension_count: u64,
    pub legacy_affected_dimension_semantics: String,
    pub legacy_field_deprecated: bool,
    pub legacy_field_authoritative: bool,
    pub affected_effective_traffic_share: f64,
    pub classification_causal_gate: String,
    pub cardinality_gate_causal: bool,
    pub receipt_schema: String,
    pub receipt_digest: String,
}
```

Schema:

```text
ash_tensorcube_k7n_d1r12_r5_r2_route_scope_semantic_receipt_v1
```

## 9. Expected S05 Projection

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
parent_r4_classification=conditional_hold
preserved_classification=conditional_hold
classification_preserved=true
dimension_slot_count=4
authoritative_red_bucket_count=2
distinct_red_sequence_value_count=2
distinct_red_kv_value_count=2
distinct_red_cadence_value_count=2
distinct_red_contention_value_count=1
varied_red_domain_count=3
single_axis_corroborated_domain_count=0
independent_red_evidence_family_count=null
legacy_affected_dimension_count=4
legacy_field_deprecated=true
legacy_field_authoritative=false
affected_effective_traffic_share=0.0174244486795535
classification_causal_gate=affected_effective_traffic_share
cardinality_gate_causal=false
```

## 10. Expected S13 Projection

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
parent_r4_classification=conditional_hold
preserved_classification=conditional_hold
classification_preserved=true
dimension_slot_count=4
authoritative_red_bucket_count=1
distinct_red_sequence_value_count=1
distinct_red_kv_value_count=1
distinct_red_cadence_value_count=1
distinct_red_contention_value_count=1
varied_red_domain_count=0
single_axis_corroborated_domain_count=0
independent_red_evidence_family_count=null
legacy_affected_dimension_count=4
legacy_field_deprecated=true
legacy_field_authoritative=false
affected_effective_traffic_share=0.014705882352941176
classification_causal_gate=authoritative_red_bucket_count
cardinality_gate_causal=false
```

## 11. Classification Preservation Contract

For all routes:

```text
parent_r4_classification=r5_r2_preserved_classification
```

Required counts:

```text
route_classification_change_count=0
bucket_classification_change_count=0
healthy=9
amber=6
conditional_hold=2
confirmed_hold=0
observation_hold=0
invalid=0
classification_drift=8
```

R5-R2 must not claim health repair.

## 12. Semantic Overlay

R4 route-health artifacts remain immutable. R5-R2 writes one overlay per route keyed by:

```text
route_id
shape_id
parent_route_receipt_digest
semantic_receipt_digest
```

Required overlay count:

```text
17
```

## 13. Source Ownership

Canonical owner:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r2_route_scope_cardinality_semantics.rs
```

The module owns field definitions, derivation, legacy label, schema version and receipt digest. Report and binary code may consume but must not independently redefine the semantics.

Direct backend source inclusion from the orchestrator is forbidden. Normal crate exports are required.

## 14. Protected State

Hash before and after:

```text
R4 immutable artifact tree
R5-R1 immutable artifact tree
R4 bucket-health latest
R4 route-health latest
R2 aggregation policy
active route registry
```

Required:

```text
parent_artifacts_unchanged=true
aggregation_policy_unchanged=true
route_registry_unchanged=true
route_epoch_unchanged=true
replay_execution_count=0
threshold_mutation_count=0
output_authority=burn
runtime_output_changed=false
```

## 15. Outcomes

### Normal

```text
semantic_repair_completed
```

### Failures

```text
parent_semantic_projection_mismatch
semantic_owner_ambiguous
classification_mutation_detected
protected_state_violation
```

Priority:

```text
protected state violation
classification mutation
parent projection mismatch
semantic owner ambiguity
semantic repair completed
```

Exit codes:

```text
semantic_repair_completed=0
parent_semantic_projection_mismatch=5
semantic_owner_ambiguous=6
classification_mutation_detected=7
protected_state_violation=70
```

## 16. Required Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r2/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/
```

Required artifact stems:

```text
parent_reconciliation
legacy_semantics_snapshot
cardinality_domain_constitution
route_scope_semantic_receipts
semantic_overlay_index
s05_semantic_projection
s13_semantic_projection
counterfactual_cardinality_matrix
classification_preservation_audit
source_ownership_audit
semantic_parity_audit
determinism_audit
protected_state_guard
repair_summary
report
verdict
final_seal
local_manifest
```

All artifacts must be generated by the local Rust binary.

## 17. Required Implementation Files

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r2_route_scope_cardinality_semantics.rs
crates/model_core/src/vocab_atlas_shadow_route_scope_cardinality_semantics_repair_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r2_route_scope_cardinality_semantics_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r2_route_scope_cardinality_semantics_repair.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

## 18. Required Command

Use the command supplied with the baked artifact. It must require both parent executions, load the R4 and R5-R1 evidence surfaces, derive all 17 semantic overlays, require S05/S13 exact cardinalities, preserve classifications, write R5-R2-only artifacts, and prohibit replay, threshold mutation and production promotion.

## 19. Expected PASS Output

```text
PASS_ASH_TCU_K7N_D1R12_R5_R2_ROUTE_SCOPE_CARDINALITY_SEMANTICS_REPAIR_EXPLICIT_DOMAINS_PARENT_CLASSIFICATION_PRESERVED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R2_SEMANTIC_REPAIR_COMPLETED
route_scope_semantic_receipt_count=17
semantic_overlay_count=17
dimension_slot_count=4
s05_authoritative_red_bucket_count=2
s05_varied_red_domain_count=3
s05_single_axis_corroborated_domain_count=0
s05_legacy_affected_dimension_count=4
s05_classification=conditional_hold
s05_classification_causal_gate=affected_effective_traffic_share
s13_authoritative_red_bucket_count=1
s13_varied_red_domain_count=0
s13_single_axis_corroborated_domain_count=0
s13_legacy_affected_dimension_count=4
s13_classification=conditional_hold
s13_classification_causal_gate=authoritative_red_bucket_count
legacy_field_deprecated=true
legacy_field_authoritative=false
route_classification_change_count=0
bucket_classification_change_count=0
selected_outcome=semantic_repair_completed
output_authority=burn
runtime_output_changed=false
```

## 20. PASS Meaning and Next State

PASS means the ambiguous field has been retired from authority, explicit semantic domains have been written, and all parent classifications remain unchanged.

PASS does not mean either conditional hold has been repaired.

On PASS, authorize two independent evidence branches:

```text
ASH-TCU-K7N-D1R12-R5-R3A_TARGETED_S05_AFFECTED_SHARE_GATE_AUDIT
ASH-TCU-K7N-D1R12-R5-R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY
```

A later reconciliation patch must merge both branches before any route-health repair or promotion decision.
