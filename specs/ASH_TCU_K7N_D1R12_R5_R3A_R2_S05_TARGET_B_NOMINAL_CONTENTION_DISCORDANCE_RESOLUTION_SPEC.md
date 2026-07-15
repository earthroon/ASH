# ASH-TCU-K7N-D1R12-R5-R3A-R2

## S05 Target-B Nominal-Contention Discordance Resolution

### Patch identity

```text
ASH-TCU-K7N-D1R12-R5-R3A-R2_S05_TARGET_B_NOMINAL_CONTENTION_DISCORDANCE_RESOLUTION
```

PASS:

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3A_R2_S05_TARGET_B_NOMINAL_CONTENTION_DISCORDANCE_RESOLUTION_COHORT_CAUSALITY_RESOLVED
```

HOLD:

```text
HOLD_ASH_TCU_K7N_D1R12_R5_R3A_R2_S05_TARGET_B_NOMINAL_CONTENTION_DISCORDANCE_RESOLUTION_EVIDENCE_REMAINS_UNSTABLE
```

### Direct parent

```text
execution_id=d1r12-r5-r3a-r1-c942dc2153e48041d06f
selected_outcome=measurement_indeterminate

target_a_persistence=not_reproduced
target_b_persistence=cohort_unstable
target_b_nominal_replication=discordant
control_authoritative_red_count=0
measurement_validity=true
```

Measurement parent:

```text
execution_id=d1r12-r5-r5e-662d21d4f4a660b2614f
selected_outcome=target_regression_reappears_under_repaired_protocol
```

### Fixed target

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
shape_id=S05_M1_N1_K4
target_role=target_b
target_cohort=parent_matched_nominal_contention
control_surface_id=b587d580b44201c3883993b87cd6ff732844ffbe034e53323245479e5d463e31
```

The exact Target-B bucket and three physical controls frozen by R5-R5E are reused. Target and control reselection, cross-shape fallback and health-result-dependent selection are forbidden.

### Replay budget

```text
parent_segment_count=3
parent_pair_count=96

new_target_segment_count=12
recorded_pairs_per_target_segment=32
unrecorded_warmup_pairs_per_segment=16
new_target_pair_count=384

control_pair_count=96
total_new_pair_count=480
burn_first_pair_count=240
tensorcube_first_pair_count=240
process_epoch_count=15
```

Each target segment contains 16 Burn-first and 16 TensorCube-first pairs. Each segment runs in a fresh child process.

### Measurement protocol

Runtime source labels are derived from the child measurement context:

```text
ASH-TCU-K7N-D1R12-R5-R3A-R2.<bucket_role>.<cohort>.<segment_id>
```

Required mismatch counts:

```text
source_label_mismatch_count=0
measurement_context_mismatch_count=0
bucket_binding_mismatch_count=0
profiler_owner_mismatch_count=0
timestamp_query_owner_mismatch_count=0
role_dependent_invocation_count=0
contention_fixture_mismatch_count=0
segment_order_imbalance_count=0
```

The parent-matched nominal-contention fixture digest must have a unique count of one.

### Discordance reconstruction

The three immutable R5-R3A-R1 Target-B nominal segment receipts are loaded individually. The audit records their segment IDs, authoritative-red state, p50/p95/p99 ratios, classification, baseline quality, timestamp resolution, process epoch, queue distributions and execution-order distribution.

Aggregate-only parent reconstruction is forbidden.

### Classification

Each new 32-pair segment and the pooled 384-pair generation use the unchanged R2 bucket policy.

```text
stable_red:
  pooled authoritative red
  and red segment count >= 8
  and indeterminate segment count = 0

stable_non_red:
  pooled non-red
  and red segment count <= 1
  and indeterminate segment count = 0

minority_red_unstable: red segment count 2..=4
split_cohort_unstable: red segment count 5..=7
pooled_majority_conflict: pooled and segment-majority states disagree
indeterminate: required measurement evidence invalid
```

### Causality audits

Execution order is audited using independent 192-pair Burn-first and TensorCube-first strata. Exactly one red stratum establishes an execution-order effect.

Queue causality is empirical. Segment p95 queue-wait and queue-depth values are ranked. A queue condition is recognized only when every red segment is inside the highest four-segment empirical stratum and non-red segments exist under the same fixture. No fixed queue threshold is added.

Process-epoch statuses:

```text
not_clustered
insufficient_evidence
early_epoch_cluster
late_epoch_cluster
contiguous_epoch_cluster
dispersed
```

All-red and all-non-red generations are not treated as epoch clusters. A single red epoch is insufficient evidence, not a cluster.

### Outcomes

```text
target_b_nominal_stable_red
target_b_nominal_stable_non_red
target_b_nominal_execution_order_conditioned
target_b_nominal_queue_conditioned
target_b_nominal_process_epoch_clustered
target_b_nominal_discordance_persists
control_surface_contaminated
contention_fixture_mismatch
measurement_indeterminate
```

Outcome constants used in Rust match expressions must be module-qualified as `r3a_r2::OUTCOME_*`.

### Next states

```text
stable red
-> ASH-TCU-K7N-D1R12-R5-R3A-R3_S05_SINGLE_TARGET_B_AFFECTED_SHARE_AUTHORITY_RESEAL

stable non-red
-> ASH-TCU-K7N-D1R12-R5-R3A-R3_S05_ZERO_REPRODUCED_RED_BRANCH_SEAL

execution-order conditioned
-> ASH-TCU-K7N-D1R12-R5-R3A-R2-R1_TARGET_B_NOMINAL_EXECUTION_ORDER_SENSITIVITY_AUDIT

queue conditioned
-> ASH-TCU-K7N-D1R12-R5-R3A-R2-R2_TARGET_B_NOMINAL_QUEUE_CAUSALITY_QUALIFICATION

process-epoch clustered
-> ASH-TCU-K7N-D1R12-R5-R3A-R2-R3_TARGET_B_NOMINAL_PROCESS_EPOCH_STABILITY_AUDIT

control contamination
-> ASH-TCU-K7N-D1R12-R5-R5E-R2_S05_CONTROL_SURFACE_CONTAMINATION_REAUDIT
```

Persistent discordance remains non-authoritative and has no automatic next patch.

### Implementation surface

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r3a_r2_target_b_nominal_contention_resolution.rs
crates/model_core/src/vocab_atlas_shadow_s05_target_b_nominal_contention_resolution_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r3a_r2_target_b_nominal_contention_resolution_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r3a_r2_target_b_nominal_contention_resolution.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Required backend and model export surfaces each include an export-surface seal, crate-root fingerprint seal and crate-root repair seal.

### Protected state

R5-R3A, R5-R3A-R1, R5-R3B, R5-R4 and R5-R5E immutable artifact trees, the R2 aggregation policy and active route registry are hashed before and after execution.

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
output_authority=burn
runtime_output_changed=false
```

### Exit codes

```text
stable or causally classified outcome=0
discordance persists=5
measurement indeterminate=5
control surface contaminated=6
contention fixture mismatch=7
runtime or parity failure=9
protected state violation=70
```

### PASS meaning

PASS means the parent discordance was reconstructed, the repaired measurement protocol and frozen control surface were reused, twelve fresh Target-B nominal segments plus three control sentinels were measured, order/queue/epoch effects were separated, and one non-committing Target-B nominal resolution was selected.

PASS does not mutate Target-B persistence, S05 route health, effective weights, R2 policy, route registry, route epoch or production output.