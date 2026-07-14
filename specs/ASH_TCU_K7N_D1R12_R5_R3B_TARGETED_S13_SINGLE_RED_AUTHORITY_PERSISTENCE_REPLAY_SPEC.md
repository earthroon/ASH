# ASH-TCU-K7N-D1R12-R5-R3B SPEC

## Targeted S13 Single-Red Authority Persistence Replay

## 1. Patch Identity

```text
ASH-TCU-K7N-D1R12-R5-R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY
```

PASS marker:

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY_EVIDENCE_CLASSIFIED_PARENT_POLICY_IMMUTABLE
```

Failure marker:

```text
FAIL_ASH_TCU_K7N_D1R12_R5_R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY_RUNTIME_EVIDENCE_OR_PROTECTED_STATE_VIOLATION
```

GitHub path:

```text
specs/ASH_TCU_K7N_D1R12_R5_R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY_SPEC.md
```

Patch class:

```text
targeted single-bucket persistence replay
+ paired Burn/TensorCube measurement
+ cold/warm decomposition
+ isolated/nominal contention decomposition
+ balanced execution-order audit
+ shape-local controls
+ fresh-process persistence audit
+ non-committing authority counterfactuals
+ no policy mutation
+ no route-health mutation
+ no production promotion
```

## 2. Required Parents

R4 runtime evidence:

```text
execution_id=d1r12-r4-69c1e6aec6a09d5506f1
selected_outcome=non_coverage_policy_regression_persists
```

R5-R1 causal audit:

```text
execution_id=d1r12-r5-r1-7a8b3d1656b3d6213586
selected_outcome=cardinality_aliasing_confirmed
cardinality_gate_causal_to_s13_classification=false
red_count_gate_causal_to_s13_classification=true
single_bucket_authority_cap_absent=true
```

Direct R5-R2 parent:

```text
execution_id=d1r12-r5-r2-c3396b7fd36a7f5b0a1e
selected_outcome=semantic_repair_completed
route_classification_change_count=0
bucket_classification_change_count=0
output_authority=burn
runtime_output_changed=false
```

## 3. Exact Target

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
shape_id=S13_M1_N16_K5
sequence_bucket=very_long
kv_bucket=high
cadence_class=sustained_burst
contention_class=nominal
```

Required parent evidence:

```text
sample_count=32
classification=confirmed_critical_path_red
authoritative_red=true
diagnostic_red=true
baseline_quality=exact
timestamp_resolution_class=reliable
ratio_stable=true
p50_valid=true
p95_valid=true
p99_valid=false
burn_ready_p50_ratio=0.9166666666666666
burn_ready_p95_ratio=1.3846153846153846
effective_weight=0.014705882352941176
```

Parent S13 route state:

```text
classification=conditional_hold
authoritative_red_bucket_count=1
varied_red_domain_count=0
single_axis_corroborated_domain_count=0
classification_causal_gate=authoritative_red_bucket_count
cardinality_gate_causal=false
```

## 4. Purpose

R5-R3B determines whether the historical S13 authoritative-red bucket is persistent across process, warmup, queue and execution-order boundaries.

It must distinguish:

```text
persistent target-specific tail regression
persistent contention-bound regression
cold-start-only transient
execution-order or queue-protocol bias
shape-local control spillover
historical red not reproduced
measurement indeterminate
```

The patch measures persistence only. It must keep:

```text
single_red_route_authority_policy_status=unadjudicated
```

## 5. Replay Scope

```text
target_bucket_count=1
shape_local_control_bucket_count=3
targeted_canonical_bucket_count=4
```

No cross-route or cross-shape fallback is permitted.

### Control C1

Cadence-only neighbor:

```text
same route, shape, sequence, KV and contention
different cadence
Hamming distance=1
```

### Control C2

Contention-only neighbor:

```text
same route, shape, sequence, KV and cadence
different contention
Hamming distance=1
```

### Control C3

Nearest healthy shape-local reference:

```text
same route and shape
classification=healthy
baseline_quality=exact
timestamp_resolution_class=reliable
ratio_stable=true
```

Selection is deterministic by classification priority, parent sample count, traffic share and canonical lexical order.

## 6. Pair Budget

Target:

```text
cold_start=32
warm_steady=96
queue_isolated=64
parent_matched_nominal_contention=64
target_total=256
```

Controls:

```text
cadence_control=32
contention_control=32
healthy_reference_control=32
control_total=96
```

Global:

```text
total_new_paired_samples=352
burn_first=176
tensorcube_first=176
```

One pair contains:

```text
Burn baseline
Burn-ready canary measurement
TensorCube shadow measurement
parity validation
execution-order receipt
```

## 7. Process Topology

The implementation must use child processes and local staging.

```text
cold processes=32, one recorded pair each
warm segments=3, 16 excluded warmups + 32 recorded pairs each
isolated segments=2, 32 recorded pairs each
nominal segments=2, 32 recorded pairs each
control segments=3, 16 excluded warmups + 32 recorded pairs each
total process epochs=42
```

Child staging root:

```text
workspace/runtime/tensorcube/.staging/<execution_id>/segments/
```

A child may write only its plan and segment bundle under staging. The parent verifies all segment and plan digests before immutable artifact promotion.

## 8. Execution Order

Execution order is derived only from the global pair ordinal:

```text
even ordinal=Burn first
odd ordinal=TensorCube first
```

Measured latency or health may not influence order assignment.

## 9. Measurement Contract

Every paired receipt records:

```text
route, shape and canonical bucket
cohort and process epoch
segment and global pair ordinal
execution order
cold/warm state
Burn baseline latency
Burn-ready latency
TensorCube ready latency
ready ratio
queue wait projection
logical queue depth
occupancy
GPU timestamp period
resolution class
parity status
output authority
runtime output mutation status
```

All 352 pairs require successful parity.

## 10. Classification Contract

Cohort bucket health must be derived through the unchanged R2 aggregation policy.

Required fields:

```text
baseline_quality
timestamp_resolution_class
ratio_stable
p50_valid
p95_valid
p99_valid
authoritative_red
diagnostic_red
classification
```

No cohort-specific threshold is permitted.

## 11. Persistence Outcomes

### Persistent target-specific regression

```text
warm red=true
isolated red=true
nominal red=true
at least three target cohorts red
order effect=false
control red count=0
```

### Persistent contention-bound regression

```text
nominal red=true
warm red=true
isolated red=false
control red count=0
```

### Cold-start-only transient

```text
cold red=true
warm red=false
isolated red=false
nominal red=false
```

### Order or queue-protocol bias

```text
Burn-first and TensorCube-first classifications differ
or isolated/nominal topology produces an order-sensitive contradiction
```

### Control spillover

```text
control_authoritative_red_count>=1
```

### Historical red not reproduced

```text
new authoritative target cohort count<=1
measurement valid
control spillover=false
```

### Measurement indeterminate

Required for incomplete controls, missing segments, unstable measurement or nondeterministic recomputation.

## 12. Authority Counterfactuals

The patch writes non-committing projections for:

```text
current one-red policy
persistence-qualified single red
two-independent-red-bucket requirement
target-specific-persistence requirement
```

Every projection must set:

```text
policy_mutated=false
non_committing=true
```

No counterfactual may update the parent bucket or route classification.

## 13. Protected State

Before and after digests must cover:

```text
R4 immutable artifact tree
R5-R1 immutable artifact tree
R5-R2 immutable artifact tree
R2 aggregation policy
active route registry
route epoch
shader and ABI surfaces
pipeline layout
Burn source
model weights
sampler contract
KV contract
```

Required:

```text
parent_artifacts_unchanged=true
aggregation_policy_unchanged=true
route_registry_unchanged=true
route_epoch_unchanged=true
route_classification_change_count=0
bucket_classification_change_count=0
threshold_mutation_count=0
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
output_authority=burn
runtime_output_changed=false
```

## 14. Export Surface

Normal crate exports are required:

```text
ASH_TCU_K7N_D1R12_R5_R3B_BACKEND_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R3B_MODEL_EXPORT_SURFACE_SEAL
```

The R5-R3B binary must not use `#[path = "..."]` to include backend or model implementation sources. Private GPU runtime access remains inside `burn_webgpu_backend`.

## 15. Required Implementation Files

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r3b_s13_single_red_persistence_replay.rs
crates/model_core/src/vocab_atlas_shadow_s13_single_red_persistence_replay_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r3b_s13_single_red_persistence_replay_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r3b_s13_single_red_persistence_replay.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

## 16. Required Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r3b/<execution_id>/
```

Latest root:

```text
workspace/runtime/tensorcube/
```

Required stems:

```text
export_surface_receipt
parent_reconciliation
target_bucket_snapshot
control_selection_receipts
replay_plan
execution_order_schedule
child_segment_receipts
target_paired_samples
control_paired_samples
cold_warm_audit
contention_isolation_audit
execution_order_audit
restart_persistence_audit
control_normalization_audit
cohort_bucket_health
persistence_classification
authority_counterfactuals
determinism_audit
protected_state_guard
report
verdict
final_seal
local_manifest
```

All runtime artifacts must be generated by the local Rust binary.

## 17. PASS Semantics

R5-R3B may PASS with any conclusive persistence result.

PASS means:

```text
target and controls completed
all paired parity passed
cold/warm and isolated/nominal evidence separated
execution order audited
single-red persistence classified
parent policy and classification preserved
one conclusive outcome selected
```

PASS does not mean:

```text
S13 conditional hold removed
single-red route authority approved
threshold changed
TensorCube production promotion authorized
```

## 18. Exit Codes

```text
conclusive persistence result=0
measurement indeterminate=5
runtime or parity failure=6
parent evidence mismatch=7
protected state violation=70
```

## 19. Expected Output Shape

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3B_TARGETED_S13_SINGLE_RED_AUTHORITY_PERSISTENCE_REPLAY_EVIDENCE_CLASSIFIED_PARENT_POLICY_IMMUTABLE
OUTCOME_ASH_TCU_K7N_D1R12_R5_R3B_<OUTCOME>
target_pair_count=256
control_pair_count=96
total_pair_count=352
burn_first_pair_count=176
tensorcube_first_pair_count=176
cold_start_authoritative_red=<bool>
warm_steady_authoritative_red=<bool>
isolated_queue_authoritative_red=<bool>
nominal_contention_authoritative_red=<bool>
control_authoritative_red_count=<n>
order_effect_detected=<bool>
queue_causality=<label>
single_red_persistence_status=<label>
single_red_route_authority_policy_status=unadjudicated
route_classification_change_count=0
bucket_classification_change_count=0
selected_outcome=<outcome>
next_state=ASH-TCU-K7N-D1R12-R5-R4_PARALLEL_GATE_EVIDENCE_RECONCILIATION
output_authority=burn
runtime_output_changed=false
execution_id=<generated>
```

## 20. Next State

Every conclusive R5-R3B outcome authorizes drafting only:

```text
ASH-TCU-K7N-D1R12-R5-R4_PARALLEL_GATE_EVIDENCE_RECONCILIATION
```

The reconciliation requires both:

```text
completed R5-R3A S05 affected-share gate audit
completed R5-R3B S13 persistence replay
```

R5-R3B alone cannot authorize route-health mutation or production promotion.
