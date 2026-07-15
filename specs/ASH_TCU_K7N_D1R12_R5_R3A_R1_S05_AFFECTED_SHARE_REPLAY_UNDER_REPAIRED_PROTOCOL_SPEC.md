# ASH-TCU-K7N-D1R12-R5-R3A-R1 SPEC

## S05 Affected-Share Replay Under Repaired Protocol

## Patch Identity

```text
ASH-TCU-K7N-D1R12-R5-R3A-R1_S05_AFFECTED_SHARE_REPLAY_UNDER_REPAIRED_PROTOCOL
```

PASS marker:

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3A_R1_S05_AFFECTED_SHARE_REPLAY_UNDER_REPAIRED_PROTOCOL_COHORT_REPLICATION_WEIGHT_AUTHORITY_RESEALED
```

Failure marker:

```text
FAIL_ASH_TCU_K7N_D1R12_R5_R3A_R1_S05_AFFECTED_SHARE_REPLAY_UNDER_REPAIRED_PROTOCOL_PARENT_RUNTIME_OR_PROTECTED_STATE_VIOLATION
```

## Direct Parent

```text
R5-R5E execution=d1r12-r5-r5e-662d21d4f4a660b2614f
R5-R5E outcome=target_regression_reappears_under_repaired_protocol
```

Inherited repaired state:

```text
control_surface_id=b587d580b44201c3883993b87cd6ff732844ffbe034e53323245479e5d463e31
target_a_persistence=not_reproduced
target_b_persistence=cohort_conditional
repaired_control_authoritative_red_count=0
measurement_validity=true
```

Evidence parents:

```text
R5-R3A execution=d1r12-r5-r3a-4a90e29fdb0d0b0ee771
R5-R3A outcome=s05_control_spillover

R5-R3B execution=d1r12-r5-r3b-e6d3724554de93dc66a0
R5-R3B outcome=cold_start_only_transient
```

## Purpose

Replay the exact two S05 targets and three frozen controls under the repaired R5-R5E measurement protocol. Reseal cohort replication, target persistence, reproduced authoritative-red cardinality, effective-weight ownership, reproduced affected share, bucket independence and the non-committing S05 route-authority recommendation.

No target or control reselection is permitted.

## Target and Policy

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
shape_id=S05_M1_N1_K4
parent_classification=conditional_hold
historical_authoritative_red_bucket_count=2
historical_affected_effective_traffic_share=0.0174244486795535

route_wide_min_red_bucket_count=2
route_wide_min_affected_share=0.40
route_wide_min_dimension_count=2
single_bucket_weight_cap=0.25
```

Affected share is a route-wide qualification input, not the cause of latency regression.

## State Ownership

R5-R5E owns the repaired measurement context, source-label derivation, profiler and timestamp ownership, role-neutral invocation contract and frozen control surface.

R5-R3A-R1 owns only:

```text
three-segment cohort replay
cohort replication classification
target persistence reseal
reproduced authoritative-red cardinality
reproduced effective traffic share
bucket independence reseal
non-committing route-authority recommendation
```

Forbidden mutations:

```text
measurement protocol
control surface
R2 policy
route or bucket classification
effective traffic weights
route registry or epoch
model, sampler or KV state
production output
```

## Frozen Surface

```text
target_bucket_count=2
control_bucket_count=3
targets_unique=true
controls_unique=true
targets_controls_disjoint=true
same_route=true
same_shape=true
cross_shape_fallback=false
```

## Replay Budget

Each target runs three cohorts, each split into three independent 32-pair child segments:

```text
warm_steady=96 pairs
queue_isolated=96 pairs
parent_matched_nominal_contention=96 pairs
```

Global budget:

```text
target A pairs=288
target B pairs=288
target pairs=576
control pairs=96
total pairs=672
Burn-first=336
TensorCube-first=336
process epochs=21
```

Each segment receives 16 excluded warmup pairs and 32 recorded pairs.

## Cohort Replication

```text
stable_red = pooled authoritative red and at least 2 of 3 segments red
stable_non_red = pooled non-red and 0 of 3 segments red
discordant = pooled and segment-majority disagree, or exactly 1 red segment
indeterminate = invalid baseline, timestamp, ratio, parity or missing segment
```

Target persistence:

```text
persistent = warm stable_red and isolated or nominal stable_red
cohort_conditional = at least one stable_red cohort without persistent rule
not_reproduced = all three cohorts stable_non_red
cohort_unstable = at least one discordant cohort and no indeterminate cohort
indeterminate = at least one indeterminate cohort
```

## Reproduced Authority

A target contributes route authority only when it is `persistent` or `cohort_conditional` and at least one production-relevant cohort is `stable_red`.

```text
reproduced_authoritative_red_bucket_count=0|1|2
```

Only reproduced targets receive their immutable canonical effective weight. Partial or confidence-scaled weights are forbidden.

## Outcome Matrix

```text
0 reproduced red -> no_s05_authoritative_red_reproduced
1 reproduced red -> single_s05_authoritative_red_bucket_reproduced
2 independent red and share < 0.40 -> dual_independent_red_conditional_hold_supported
2 independent red and share >= 0.40 -> dual_independent_red_confirmed_hold_supported
2 non-independent red -> dual_red_non_independent
control red >= 1 -> repaired_protocol_control_spillover
weight integrity failure -> affected_share_reconstruction_invalid
invalid or unstable measurement -> measurement_indeterminate
```

Conclusive outcomes flow to:

```text
ASH-TCU-K7N-D1R12-R5-R4-R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN
```

## Implementation Files

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r3a_r1_s05_affected_share_replay.rs
crates/model_core/src/vocab_atlas_shadow_s05_affected_share_replay_repaired_protocol_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r3a_r1_s05_affected_share_replay_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r3a_r1_s05_affected_share_replay.rs
```

Required export seals:

```text
ASH_TCU_K7N_D1R12_R5_R3A_R1_BACKEND_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R1_BACKEND_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R1_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R3A_R1_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
```

Direct backend or model source inclusion is forbidden.

## Protected State

Required unchanged state:

```text
R5-R3A immutable artifact tree
R5-R3B immutable artifact tree
R5-R5E immutable artifact tree
R2 aggregation policy
active route registry and epoch
R5-R5E measurement protocol
R5-R5E frozen control surface
route and bucket classifications
effective weights
output authority=burn
runtime_output_changed=false
```

## Required Output

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3A_R1_S05_AFFECTED_SHARE_REPLAY_UNDER_REPAIRED_PROTOCOL_COHORT_REPLICATION_WEIGHT_AUTHORITY_RESEALED

target_a_pair_count=288
target_b_pair_count=288
target_pair_count=576
control_pair_count=96
total_pair_count=672
burn_first_pair_count=336
tensorcube_first_pair_count=336
process_epoch_count=21

target_a_warm_replication=<status>
target_a_isolated_replication=<status>
target_a_nominal_replication=<status>
target_b_warm_replication=<status>
target_b_isolated_replication=<status>
target_b_nominal_replication=<status>

target_a_persistence=<status>
target_b_persistence=<status>
reproduced_authoritative_red_bucket_count=<0|1|2>
reproduced_affected_effective_traffic_share=<value>
effective_weight_sum_exact=<bool>
duplicate_weight_contribution_count=<n>
bucket_independence_status=<status>
control_authoritative_red_count=<n>
measurement_validity=<bool>
route_authority_support=<status>
route_authority_recommendation=<recommendation>
route_classification_change_count=0
bucket_classification_change_count=0
policy_mutation_count=0
selected_outcome=<outcome>
next_state=<next state>
output_authority=burn
runtime_output_changed=false
execution_id=<generated>
local_manifest=<path>
```
