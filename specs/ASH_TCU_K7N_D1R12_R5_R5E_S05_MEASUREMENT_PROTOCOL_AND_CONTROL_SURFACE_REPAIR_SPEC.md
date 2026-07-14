# ASH-TCU-K7N-D1R12-R5-R5E SPEC

## S05 Measurement Protocol and Control Surface Repair

### Patch identity

```text
ASH-TCU-K7N-D1R12-R5-R5E_S05_MEASUREMENT_PROTOCOL_AND_CONTROL_SURFACE_REPAIR
```

PASS:

```text
PASS_ASH_TCU_K7N_D1R12_R5_R5E_S05_MEASUREMENT_PROTOCOL_AND_CONTROL_SURFACE_REPAIR_PROVENANCE_REBOUND_CONTROL_SURFACE_REVALIDATED
```

HOLD:

```text
HOLD_ASH_TCU_K7N_D1R12_R5_R5E_S05_MEASUREMENT_PROTOCOL_AND_CONTROL_SURFACE_REPAIR_EVIDENCE_INDETERMINATE
```

FAIL:

```text
FAIL_ASH_TCU_K7N_D1R12_R5_R5E_S05_MEASUREMENT_PROTOCOL_AND_CONTROL_SURFACE_REPAIR_PARENT_EVIDENCE_RUNTIME_OR_PROTECTED_STATE_VIOLATION
```

## Required parents

```text
R5-R3A execution=d1r12-r5-r3a-4a90e29fdb0d0b0ee771
R5-R3A outcome=s05_control_spillover

R5-R4 execution=d1r12-r5-r4-0ddeb339a126f0debe29
R5-R4 outcome=s05_measurement_surface_contaminated

R5-R3B execution=d1r12-r5-r3b-e6d3724554de93dc66a0
R5-R3B outcome=cold_start_only_transient
```

The patch must bind final seals and manifests for all required parents and fail closed on any execution, outcome, digest, or artifact mismatch.

## Observed contradiction

R5-R3A segment markers were correct, but the native bootstrap source label was repeatedly:

```text
ASH-TCU-K7N-D1R12-R5-R3B.control_healthy
```

The source owner audit identifies the call chain:

```text
R5-R3A::run_segment
-> R5-R3B::run_segment
-> R5-R3B::source_for_cohort
-> prepare_target_shape
-> bootstrap_existing_device
```

R5-R3A cohort names were not recognized by the R5-R3B matcher and fell into its default branch. Execution bucket ownership remained in `D1R12R5R3BSegmentPlan.bucket`.

Required pre-repair classification when parent bucket bindings are exact:

```text
pre_repair_contamination_class=stale_source_label_only
```

This classification does not dismiss the control red. The exact R5-R3A control surface must be replayed under the repaired protocol.

## Measurement-context SSOT

R5-R5E introduces one canonical process-local measurement context containing patch, execution, segment, route, shape, bucket digest, role, cohort, process epoch, replay-plan digest, execution-order digest, contention-contract digest, runtime registry identity, profiler identity, timestamp-query identity, pipeline-cache scope, measurement-context ID, runtime source label, and context digest.

The runtime source label must be derived from the canonical context:

```text
ASH-TCU-K7N-D1R12-R5-R5E.<bucket_role>.<cohort>.<segment_id>
```

Forbidden runtime source prefixes:

```text
ASH-TCU-K7N-D1R12-R5-R3A
ASH-TCU-K7N-D1R12-R5-R3B
```

One child process equals one process epoch, one canonical context, and one runtime source label.

## Shared helper repair

Approved existing helper mutation:

```text
crates/burn_webgpu_backend/src/
tensorcube_k7n_d1r12_r5_r3b_s13_single_red_persistence_replay.rs
```

Required helper:

```text
run_segment_with_source(..., runtime_source_label)
```

Existing `run_segment()` must retain R5-R3B behavior by delegating through `source_for_cohort()`. R5-R5E must use only the explicit-source helper.

## Frozen control surface

Target:

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
shape_id=S05_M1_N1_K4
```

Freeze the exact R5-R3A buckets:

```text
target_red_a
target_red_b
control_a
control_b
control_shared
```

No control reselection is allowed.

Required invariants:

```text
target count=2
control count=3
all physical buckets unique=true
targets and controls disjoint=true
same route=true
same shape=true
cross-shape fallback=false
```

For every child:

```text
expected bucket digest
=
executed bucket digest
=
reported bucket digest
```

## Invocation and provenance identity

Invocation digest includes execution-affecting fields only: route, shape, sequence bucket, KV bucket, cadence, contention, cohort, warmup, pressure, queue depth, cold-start state and execution order.

It excludes bucket role, probe role, display label and artifact filename.

Provenance digest includes invocation digest plus bucket role, segment ID, runtime source label, measurement-context ID and pair index.

Changing only reporting role may change provenance but must not change invocation identity.

## Replay budget

Canonical revalidation:

```text
target pairs=320
control pairs=96
canonical pairs=416
canonical process epochs=13
```

Role-neutral probes:

```text
physical buckets=5
canonical-role pairs per bucket=8
neutral-alias pairs per bucket=8
probe pairs=80
probe process epochs=10
```

Global:

```text
total pairs=496
Burn-first=248
TensorCube-first=248
process epochs=23
```

Every process epoch is a fresh child process.

## Repaired protocol invariants

Required normal values:

```text
source_label_mismatch_count=0
measurement_context_mismatch_count=0
bucket_binding_mismatch_count=0
role_dependent_invocation_count=0
profiler_owner_mismatch_count=0
timestamp_query_owner_mismatch_count=0
replay_failure_count=0
parity_failure_count=0
duplicate_request_key_count=0
```

Canonical replay uses the unchanged R2 aggregation and bucket policy. Role-neutral probes establish invocation invariance only and do not establish route health.

## Post-repair outcomes

### Evidence clean

```text
post_repair_evidence_state=control_clean_targets_not_reproduced
selected_outcome=protocol_contamination_repaired_s05_evidence_clean
next_state=ASH-TCU-K7N-D1R12-R5-R4-R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN
```

### Provenance-clean control spillover

```text
post_repair_evidence_state=provenance_clean_control_spillover_persists
selected_outcome=provenance_clean_true_control_spillover_persists
next_state=ASH-TCU-K7N-D1R12-R5-R5F_S05_SHAPE_LOCAL_SHARED_SURFACE_CAUSAL_AUDIT
```

### Target regression reappears

```text
post_repair_evidence_state=target_regression_reappears
selected_outcome=target_regression_reappears_under_repaired_protocol
next_state=ASH-TCU-K7N-D1R12-R5-R3A-R1_S05_AFFECTED_SHARE_REPLAY_UNDER_REPAIRED_PROTOCOL
```

### Role-dependent invocation

```text
post_repair_evidence_state=role_dependent_invocation_detected
selected_outcome=role_dependent_invocation_path_detected
next_state=ASH-TCU-K7N-D1R12-R5-R5E-R1_ROLE_NEUTRAL_INVOCATION_OWNERSHIP_REPAIR
```

### Indeterminate

```text
post_repair_evidence_state=measurement_indeterminate
selected_outcome=repair_evidence_indeterminate
next_state=none_measurement_protocol_not_conclusive
```

## State ownership

R5-R5E owns source-label owner audit, canonical context construction, process-local ownership receipts, frozen control surface, role-neutral invocation probes, repaired target/control replay, post-repair evidence state and non-committing recommendation.

R5-R5E does not own route or bucket classification mutation, R2 threshold mutation, effective-weight mutation, route registry or epoch mutation, shader arithmetic, model weights, sampler behavior, KV behavior or production output.

## Implementation files

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r5e_measurement_protocol.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r5e_s05_control_surface_repair.rs
crates/model_core/src/vocab_atlas_shadow_s05_measurement_protocol_repair_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r5e_measurement_protocol_control_surface_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r5e_measurement_protocol_control_surface_repair.rs
```

Registration surfaces:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Required export seals:

```text
ASH_TCU_K7N_D1R12_R5_R5E_BACKEND_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R5E_BACKEND_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R5E_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R5E_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
```

Direct backend or model source inclusion is forbidden.

## Protected state

Required normal values:

```text
parent_artifact_rewrite_count=0
route_classification_change_count=0
bucket_classification_change_count=0
policy_mutation_count=0
threshold_mutation_count=0
effective_weight_mutation_count=0
registry_mutation_count=0
route_epoch_change_count=0
unapproved_source_mutation_count=0
TensorCube authoritative output count=0
production output commit count=0
output_authority=burn
runtime_output_changed=false
```

## Required output artifacts

R5-R5E must emit parent reconciliation, source-owner audit, contamination classification, measurement-context constitution, runtime registry ownership, profiler ownership, timestamp-query ownership, pipeline-cache scope audit, control-surface freeze, control-binding receipts, replay plan, execution-order schedule, child-segment receipts, canonical samples, role-neutral probe samples, invocation identity audit, source-label parity audit, context-isolation audit, role-neutral invocation audit, target cohort health, target persistence, control spillover revalidation, repaired S05 branch summary, determinism audit, protected-state guard, report, verdict, final seal and local manifest.

## PASS meaning

PASS means source-label ownership was rebound to a canonical process-local context, the exact R5-R3A control surface was frozen, role metadata was proven not to alter invocation identity, target and control evidence was regenerated under the repaired protocol, one post-repair evidence state was selected, and parent route, bucket, policy, registry and Burn output authority remained unchanged.

PASS does not mean S05 classification changed or TensorCube was promoted.
