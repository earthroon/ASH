# ASH-TCU-K7N-D1R12-R2 SPEC

## Canary Health Aggregation Repair

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R12-R2_CANARY_HEALTH_AGGREGATION_REPAIR`
- Primary parent: `d1r12-53213adfb2efe946ce74`
- Review parent: `d1r12-r1-81808fbaa9fee04e70fe`
- Route epoch: `1`
- Active exact-signature routes: `17`

PASS:

```text
PASS_ASH_TCU_K7N_D1R12_R2_CANARY_HEALTH_AGGREGATION_REPAIR_PARENT_HOLDS_RECOMPUTED_VALIDITY_AWARE_REGISTRY_UNCHANGED
```

Hard failure:

```text
FAIL_ASH_TCU_K7N_D1R12_R2_CANARY_HEALTH_AGGREGATION_REPAIR_AGGREGATION_OR_PROTECTED_STATE_VIOLATION
```

## 2. Parent Boundary

Required D1R12 state:

```text
execution_id=d1r12-53213adfb2efe946ce74
canary_outcome=stop_canary_preserve_17_signature_shadow
healthy_route_count=11
hold_route_count=6
route_epoch_before=1
route_epoch_after=1
output_authority=burn
```

Required D1R12-R1 state:

```text
execution_id=d1r12-r1-81808fbaa9fee04e70fe
selected_outcome=parent_hold_classification_not_reproduced
reviewed_route_count=17
review_bucket_count=564
replay_attempt_count=23704
replay_failure_count=0
confirmed_hold_route_count=0
conditional_hold_route_count=0
hold_not_reproduced_count=6
aggregation_defect_suspected=true
```

## 3. Purpose

D1R12-R2 repairs the D1R12 route-health aggregation layer. It does not rerun the production-like canary by default and does not modify the active route registry.

The repair must prevent the following evidence from being promoted directly into route-wide performance hold:

```text
invalid p99
weak or insufficient baseline
near-zero denominator ratio
resolution-limited timing
occupancy-only red
queue-depth-only red
shadow-tail-only red
single sparse bucket
unweighted maximum reduction
coverage-reserve overweighting
```

## 4. State Ownership

D1R9 owns:

```text
active registry
route membership
route epoch
quarantine
rollback authority
```

D1R12 owns the immutable original canary evidence and outcome.

D1R12-R1 owns the immutable paired replay evidence and bucket review receipts.

D1R12-R2 owns only:

```text
aggregation policy
bucket validity masks
repaired bucket health
repaired route health
parent classification diff
aggregation defect receipt
repair outcome
```

## 5. Canonical Bucket Key

```text
route_id
× shape_id
× sequence_bucket
× kv_bucket
× cadence_class
× contention_class
```

## 6. Validity Policy

Percentile sample floors:

```text
p50 >= 8
p95 >= 32
p99 >= 128
```

Baseline quality:

```text
exact >= 32
strong >= 16
weak >= 8
insufficient < 8
```

Only exact and strong baselines may create definitive red.

Timestamp resolution:

```text
reliable >= 32 quanta
marginal >= 8 quanta
resolution_limited < 8 quanta
```

Ratio authority requires a baseline of at least 8 timestamp quanta. Hidden denominator clamping is forbidden.

## 7. Critical-Path Gates

Burn-ready latency is the only direct critical-path metric.

Green:

```text
p50 <= 1.10
p95 <= 1.20
p99 <= 1.30
```

Red:

```text
p50 > 1.20
OR p95 > 1.35
OR p99 > 1.50
```

A red threshold has authority only when its percentile is valid, the baseline is exact or strong, the ratio is stable, and timestamp resolution is reliable or marginal.

## 8. Diagnostic Separation

Occupancy bounds:

```text
median <= 2.25
p95 <= 2.75
p99 <= 3.00
```

Queue-depth p99 ratio:

```text
<= 2.00
```

Occupancy, queue depth, shadow-ready latency, and shadow completion lag are diagnostic unless corroborated by authoritative Burn-ready latency red.

Diagnostic-only evidence cannot create a route hold.

## 9. Evidence Weighting

Bucket evidence weights:

```text
exact        1.00
strong       0.75
weak         0.25
insufficient 0.00
```

Effective weight:

```text
evidence quality weight × normalized replay request share
```

Single-bucket authority is capped at `0.25`.

## 10. Route-Wide Hold Gate

A route-wide hold requires all of:

```text
confirmed critical-path red buckets >= 2
affected effective traffic share >= 0.40
affected workload dimension count >= 2
D1R12-R1 reproduction evidence present
no measurement-limited dominance
```

A single bucket cannot create route-wide hold.

## 11. Conditional Hold Gate

Conditional hold requires authoritative red evidence that is isolated to a bounded workload condition and does not satisfy the route-wide gate.

Examples:

```text
heavy_contention_only
near_runtime_limit_kv_only
sustained_burst_only
very_long_sequence_only
```

## 12. Observation Hold

Observation hold is separate from performance hold.

It applies only when:

```text
confirmed red = 0
conditional red = 0
measurement-limited or evidence-insufficient share >= 0.50
```

## 13. Repaired Route Health

```text
invalid
confirmed_hold
conditional_hold
observation_hold
amber
healthy
```

Precedence follows the order above. Diagnostic-only evidence is excluded from hold precedence.

## 14. Defect Taxonomy

```text
invalid_percentile_promoted
weak_baseline_promoted
near_zero_ratio_inflation
diagnostic_occupancy_promoted
shadow_tail_promoted
single_bucket_route_escalation
unweighted_maximum_reduction
precedence_ordering_bug
coverage_reserve_overweighted
missing_validity_mask
other
```

At least one defect flag must be recorded when a parent hold changes classification.

## 15. Determinism

Given identical D1R12 artifact digests, D1R12-R1 artifact digests, and aggregation policy digest, repaired route health must be byte-identical.

Canonical ordering uses `BTreeMap`, `BTreeSet`, and sorted receipt vectors.

## 16. Protected State

The following remain byte-identical:

```text
active D1R9 registry
route epoch
D1R12 final seal and manifest
D1R12 report and route health
D1R12-R1 final seal and manifest
D1R12-R1 report, bucket receipts, route receipts and summary
whitelist
holdlist
K7N shader
RHS ABI
pipeline layout
Burn source
model weights
sampler ownership
KV ownership
```

Required authority counters:

```text
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
sampler_substitution_count=0
kv_state_mutation_count=0
output_authority=burn
```

## 17. Required Artifacts

```text
ash_tensorcube_k7n_d1r12_r2_parent_reconciliation_latest.json
ash_tensorcube_k7n_d1r12_r2_aggregation_policy_latest.json
ash_tensorcube_k7n_d1r12_r2_bucket_validity_masks_latest.json
ash_tensorcube_k7n_d1r12_r2_baseline_quality_latest.json
ash_tensorcube_k7n_d1r12_r2_ratio_stability_latest.json
ash_tensorcube_k7n_d1r12_r2_diagnostic_evidence_latest.json
ash_tensorcube_k7n_d1r12_r2_repaired_bucket_health_latest.json
ash_tensorcube_k7n_d1r12_r2_repaired_route_health_latest.json
ash_tensorcube_k7n_d1r12_r2_parent_classification_diff_latest.json
ash_tensorcube_k7n_d1r12_r2_aggregation_defect_receipt_latest.json
ash_tensorcube_k7n_d1r12_r2_aggregation_repair_summary_latest.json
ash_tensorcube_k7n_d1r12_r2_protected_state_guard_latest.json
ash_tensorcube_k7n_d1r12_r2_report_latest.json
ash_tensorcube_k7n_d1r12_r2_verdict_latest.json
ash_tensorcube_k7n_d1r12_r2_final_seal_latest.json
ash_tensorcube_k7n_d1r12_r2_local_manifest_latest.json
```

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r2/<execution_id>/
```

## 18. Implementation Surface

Backend modules:

```text
parent reconciliation
aggregation policy
bucket key and validity
percentile validity
baseline quality
ratio stability
timestamp resolution
critical-path latency
diagnostic evidence
occupancy and contention aggregation
bucket health and weight
route scope and route health
health precedence
parent diff
defect taxonomy
aggregation audit
repair summary
protected state guard
contract audit
verdict
```

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_canary_health_aggregation_contract.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r2_canary_health_aggregation_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r2_canary_health_aggregation_repair.rs
```

## 19. Outcomes

Exactly one outcome:

```text
OUTCOME_ASH_TCU_K7N_D1R12_R2_AGGREGATION_DEFECT_CONFIRMED_AND_REPAIRED
OUTCOME_ASH_TCU_K7N_D1R12_R2_PARENT_HOLDS_REMAIN_VALID
OUTCOME_ASH_TCU_K7N_D1R12_R2_MEASUREMENT_POLICY_STILL_INSUFFICIENT
OUTCOME_ASH_TCU_K7N_D1R12_R2_PARENT_EVIDENCE_INCONSISTENT
```

Outcome priority:

```text
parent evidence inconsistent
parent holds remain valid
measurement policy insufficient
aggregation defect confirmed and repaired
```

## 20. Normal PASS Boundary

```text
active routes reviewed=17
parent hold routes reviewed=6
review buckets consumed=564
route epoch before=1
route epoch after=1
active registry unchanged=true
protected parent evidence unchanged=true
invalid percentile promotion after repair=0
weak baseline promotion after repair=0
near-zero ratio authority after repair=0
diagnostic-only hold promotion after repair=0
single-bucket route-wide promotion after repair=0
output_authority=burn
one outcome selected=true
```

PASS means the aggregation repair completed consistently. It does not authorize canary reactivation, D1R13, or TensorCube production output promotion.

## 21. Next State

```text
aggregation defect repaired
→ ASH-TCU-K7N-D1R12-R3_REPAIRED_CANARY_HEALTH_REPLAY

parent holds valid
→ ASH-TCU-K7N-D1R12-R3_CONFIRMED_HOLD_SCOPE_MITIGATION

measurement policy insufficient
→ ASH-TCU-K7N-D1R12-R3_MEASUREMENT_POLICY_RECALIBRATION

parent evidence inconsistent
→ ASH-TCU-K7N-D1R12-R3_PARENT_EVIDENCE_RECONSTRUCTION
```
