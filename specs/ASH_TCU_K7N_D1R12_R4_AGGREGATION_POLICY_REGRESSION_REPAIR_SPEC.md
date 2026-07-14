# ASH-TCU-K7N-D1R12-R4 SPEC

## Aggregation Policy Regression Repair

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR`
- Normal PASS: `PASS_ASH_TCU_K7N_D1R12_R4_AGGREGATION_POLICY_REGRESSION_REPAIR_COVERAGE_FLOOR_TOPUP_SEVENTEEN_ROUTES_HEALTHY_NO_THRESHOLD_MUTATION`
- Hard failure: `FAIL_ASH_TCU_K7N_D1R12_R4_AGGREGATION_POLICY_REGRESSION_REPAIR_COVERAGE_REPAIR_OR_PROTECTED_STATE_VIOLATION`
- GitHub path: `specs/ASH_TCU_K7N_D1R12_R4_AGGREGATION_POLICY_REGRESSION_REPAIR_SPEC.md`

Patch class:

```text
replay coverage-floor diagnosis
+ canonical bucket deficit computation
+ deterministic bounded top-up schedule
+ immutable parent evidence merge
+ aggregation-policy immutability validation
+ observation-hold regression repair
+ seventeen-route health reproduction
+ Burn-authoritative shadow execution
+ no threshold relaxation
+ no parent rewrite
+ no registry mutation
+ no production promotion
```

## 2. Direct Parents

```text
R3 patch=ASH-TCU-K7N-D1R12-R3_REPAIRED_CANARY_HEALTH_REPLAY
R3 execution=d1r12-r3-6458db8a777cd4f936c5
R3 outcome=repaired_policy_regression

R3-R1 patch=ASH-TCU-K7N-D1R12-R3-R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR
R3-R1 execution=d1r12-r3-r1-6fdba52826fce5e88749
R3-R1 status=PASS_ASH_TCU_K7N_D1R12_R3_R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR_REGRESSION_TRUTH_RESTORED_PARENT_IMMUTABLE
```

Required parent state:

```text
active_route_count=17
replay_attempt_count=49152
replay_failure_count=0
parity_sample_count=544
parity_failing_sample_count=0
restart_count=2
replay_bucket_count=1401
healthy_route_count=11
amber_route_count=1
conditional_hold_route_count=0
confirmed_hold_route_count=0
observation_hold_route_count=5
invalid_route_count=0
false_hold_count=0
classification_drift_count=6
deterministic_recompute=true
route_epoch_before=1
route_epoch_after=1
output_authority=burn
runtime_output_changed=false
```

Required R2 comparison state is seventeen healthy routes and zero routes in every other class.

## 3. Purpose

R4 determines whether the R3 regression was caused by canonical-bucket replay coverage underallocation. It derives every bucket deficit from persisted R3 samples, executes only the missing requests, merges immutable parent and top-up evidence, and recomputes health using the byte-identical R2 aggregation policy.

R4 is not a threshold-tuning stage and is not a production-promotion stage.

## 4. Ownership and Non-Goals

- D1R9 owns route registry membership, epoch, quarantine and rollback.
- D1R12 owns the production-like schedule and workload identity.
- D1R12-R2 owns all aggregation thresholds and precedence.
- D1R12-R3 owns immutable 49,152-request replay evidence.
- D1R12-R3-R1 owns corrected truth projection.
- D1R12-R4 owns deficit analysis, top-up execution, merged health and the repair outcome.

R4 forbids threshold relaxation, health-aware request selection, route or shape substitution, bucket merging, parent rewriting, registry mutation, sampler or KV transfer, TensorCube authoritative output and D1R13 promotion.

## 5. Parent Reconciliation Gate

Before GPU execution:

```text
R3 execution and outcome exact
R3-R1 execution and status exact
all parent final seals and manifests readable
R3-R1 parent_artifacts_unchanged=true
R2 policy digest exact
active registry digest exact
registry schema=ash_tensorcube_shadow_route_registry_v1
route epoch=1
active route count=17
output authority=burn
```

Any mismatch stops before deficit planning.

## 6. Canonical Bucket and Deficit Contract

Canonical key:

```text
route_id
× shape_id
× sequence_bucket
× kv_bucket
× cadence_class
× contention_class
```

The unchanged R2 floors are:

```text
p50 valid >= 8
p95 valid >= 32
p99 valid >= 128
exact baseline >= 32
strong baseline >= 16
weak baseline >= 8
insufficient < 8
```

R4 mandatory repair floor:

```text
merged canonical-bucket sample count >= 32
```

R4 does not force p99 validity. A bucket below 128 retains `p99_valid=false`.

For every persisted bucket:

```text
required_topup = max(0, 32 - parent_sample_count)
planned_topup_attempt_count = sum(required_topup)
planned_merged_attempt_count = 49152 + planned_topup_attempt_count
```

Expected but locally re-derived:

```text
canonical_bucket_count=1401
planned_topup_attempt_count=14270
planned_merged_attempt_count=63422
maximum_merged_attempt_count=65536
```

The binary must not silently force the expected count if persisted evidence derives another value.

## 7. Defect Confirmation and Planner Purity

The selected defect may be `replay_bucket_coverage_floor_underallocation` only when:

- at least one canonical bucket is below 32;
- all five observation-hold routes have underfloor-bucket dominance;
- replay and parity failures are zero;
- deterministic recompute is true;
- policy, registry and parent artifacts are unchanged;
- authoritative runtime-red evidence does not independently explain the holds.

The planner may inspect only bucket identity, parent sample count, repair floor, stable ordering and budget. It must not inspect route health labels.

Canonical ordering is route, shape, sequence, KV, cadence, contention and top-up ordinal. `BTreeMap`, `BTreeSet` or stable sorting are required. Hash, filesystem, thread or GPU completion order is forbidden.

## 8. Runtime Contract

R4 executes three fresh child-process segments, creating two restart boundaries. Each top-up request reuses the original parent schedule identity and performs:

```text
Burn baseline
→ original contention pressure
→ Burn canary
→ TensorCube shadow
→ parity sampling
→ discard TensorCube output
```

Required runtime state:

```text
topup_replay_failure_count=0
device_lost_count=0
pipeline_rebuild_failure_count=0
registry_reload_failure_count=0
aggregation_policy_reload_failure_count=0
topup_plan_reload_failure_count=0
evidence_merge_failure_count=0
restart_count>=2
post_restart_topup_attempt_count>=1024 per restart
```

Control routes require bit-exact parity. Other routes use the existing K7N tolerance. New top-up parity samples must be at least 256 and merged parity samples at least 800, with zero failures.

## 9. Evidence Merge and Health Recompute

```text
merged_sample_count = parent_sample_count + topup_sample_count
```

Parent deletion, mutation, double counting, duplicate ordinals, duplicate top-up keys and cross-bucket reassignment are forbidden.

After merge every canonical bucket must satisfy:

```text
sample_count>=32
baseline_quality=exact
p50_valid=true
p95_valid=true
```

Global requirements:

```text
underfloor_bucket_count_after=0
weak_baseline_bucket_count_after=0
insufficient_baseline_bucket_count_after=0
unclassified_bucket_count=0
duplicate_bucket_key_count=0
```

Health is recomputed with the unchanged R2 policy. Coverage repair must not force a route healthy. Remaining authoritative red or bounded amber selects a non-normal outcome.

Expected normal route state:

```text
healthy=17
amber=0
conditional_hold=0
confirmed_hold=0
observation_hold=0
invalid=0
false_hold_count=0
classification_drift_count=0
```

## 10. Determinism and Protected State

Two independent derivations must produce byte-identical deficit plans, top-up plans, bucket receipts, route receipts, summary digest and selected outcome.

Hash before and after:

- all immutable R3 and R3-R1 artifacts;
- active registry and route epoch;
- R2 aggregation policy;
- whitelist and holdlist;
- shader, ABI and pipeline layout;
- Burn source and model weights;
- sampler and KV contracts.

Only R4 source and R4 local Rust artifacts may change.

Throughout R4:

```text
output_authority=burn
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
sampler_substitution_count=0
kv_state_mutation_count=0
runtime_output_changed=false
```

## 11. Required Local Rust Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r4/<execution_id>/
```

Latest mirrors under `workspace/runtime/tensorcube/` include parent reconciliation, regression snapshot, bucket index, deficit map, defect receipt, top-up plan and schedule, baseline pairs, samples, parity and restart receipts, merged evidence, bucket and route health, route repairs, R2/R3/R4 diff, false-hold audit, determinism audit, repair summary, protected-state guard, report, verdict, final seal and local manifest.

All artifacts and the manifest are generated by the local Rust binary and are not included in the source ZIP.

## 12. Implementation Surface

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r4_regression_repair.rs
crates/model_core/src/vocab_atlas_shadow_aggregation_policy_regression_repair_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r4_aggregation_policy_regression_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r4_aggregation_policy_regression_repair.rs
```

Registrations are required in backend `lib.rs`, model `lib.rs` and orchestrator `Cargo.toml`. R3 runtime helper visibility may be widened only inside the backend crate to reuse the sealed Burn, shadow, shape preparation and request-bucket implementation.

## 13. Outcomes

Exactly one:

```text
coverage_regression_repaired
bounded_amber_remains
replay_budget_insufficient
non_coverage_policy_regression_persists
runtime_repair_instability
parent_evidence_inconsistent
```

Priority is parent inconsistency, runtime instability, budget insufficiency, non-coverage regression, bounded amber, then coverage repaired.

## 14. Normal PASS Conditions

```text
selected defect=replay_bucket_coverage_floor_underallocation
canonical buckets=1401
repair floor=32
parent attempts=49152
topup attempts=14270
merged attempts=63422
merged attempts<=65536
underfloor, weak and insufficient buckets after=0
healthy routes=17
all other route classes=0
false holds=0
classification drift=0
topup replay and parity failures=0
restart count>=2
deterministic recompute=true
route epoch, registry, policy and parents unchanged=true
output authority=burn
runtime output changed=false
```

## 15. Verdicts and Next State

Normal PASS verdict:

```text
the_d1r12_r4_aggregation_policy_regression_repair_confirmed_replay_bucket_coverage_floor_underallocation_derived_a_health_blind_deterministic_bounded_topup_plan_from_the_immutable_parent_schedule_raised_every_canonical_bucket_to_the_unchanged_thirty_two_sample_exact_baseline_and_p95_floor_recomputed_all_seventeen_routes_as_healthy_with_zero_observation_holds_zero_false_holds_zero_classification_drift_zero_runtime_or_parity_failure_and_preserved_the_parent_evidence_route_epoch_registry_aggregation_policy_shader_abi_pipeline_model_sampler_kv_and_burn_output_authority
```

Hard failure verdict:

```text
the_d1r12_r4_aggregation_policy_regression_repair_failed_to_confirm_or_repair_the_parent_coverage_regression_within_the_sealed_replay_budget_or_left_underfloor_buckets_observation_holds_false_holds_classification_drift_runtime_instability_parity_failure_nondeterminism_or_mutated_parent_registry_policy_runtime_model_sampler_kv_or_output_authority_state
```

Next-state mapping:

```text
coverage_regression_repaired
→ ASH-TCU-K7N-D1R12-R5_REPAIRED_CANARY_SUSTAINED_SOAK

bounded_amber_remains
→ ASH-TCU-K7N-D1R12-R5_BOUNDED_AMBER_ROUTE_SCOPE_REVIEW

replay_budget_insufficient
→ ASH-TCU-K7N-D1R12-R5_REPLAY_BUDGET_EXPANSION_REVIEW

non_coverage_policy_regression_persists
→ ASH-TCU-K7N-D1R12-R5_AGGREGATION_POLICY_REGRESSION_ROOT_CAUSE_REPAIR

runtime_repair_instability
→ ASH-TCU-K7N-D1R12-R5_REPAIR_RUNTIME_STABILITY

parent_evidence_inconsistent
→ ASH-TCU-K7N-D1R12-R5_PARENT_EVIDENCE_RECONSTRUCTION
```

No outcome authorizes D1R13 or TensorCube production output.