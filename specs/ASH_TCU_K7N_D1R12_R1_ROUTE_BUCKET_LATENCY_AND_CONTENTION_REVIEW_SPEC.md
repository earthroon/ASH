# ASH-TCU-K7N-D1R12-R1 SPEC

## Route-Bucket Latency and Contention Review

### Identity

- Patch: `ASH-TCU-K7N-D1R12-R1_ROUTE_BUCKET_LATENCY_AND_CONTENTION_REVIEW`
- Parent execution: `d1r12-53213adfb2efe946ce74`
- Parent outcome: `stop_canary_preserve_17_signature_shadow`
- Route epoch: `1`
- Active routes: `17`
- Parent health: `11 healthy / 0 degraded / 6 hold`

PASS:

```text
PASS_ASH_TCU_K7N_D1R12_R1_ROUTE_BUCKET_LATENCY_AND_CONTENTION_REVIEW_HOLD_CAUSES_CLASSIFIED_REGISTRY_UNCHANGED
```

Hard failure:

```text
FAIL_ASH_TCU_K7N_D1R12_R1_ROUTE_BUCKET_LATENCY_AND_CONTENTION_REVIEW_EVIDENCE_OR_STATE_OWNERSHIP_VIOLATION
```

## Purpose

Classify the six D1R12 hold routes as confirmed critical-path latency, contention-bounded regression, diagnostic shadow occupancy, measurement-limited, evidence-insufficient, or parent aggregation not reproduced. This is a review-only stage and authorizes no registry mutation, canary reactivation, or production promotion.

## Parent Boundary

Required D1R12 state:

```text
execution_id=d1r12-53213adfb2efe946ce74
route_epoch_before=1
route_epoch_after=1
shadow_dispatch_success_count=50176
shadow_dispatch_failure_count=0
parity_sample_count=416
parity_failing_sample_count=0
guard_mutation_count=0
natural_cutover_count=0
drill_cutover_count=1
output_authority=burn
```

Required parent artifacts include the D1R12 manifest, final seal, report, canary schedule, route-bucket health receipt, canary-session receipt, and active D1R9 registry.

## Evidence Gap and Replay Boundary

D1R12 exported route-level tail and occupancy receipts but did not export the complete exact timing stream carrying route, shape, sequence, KV, cadence, and contention dimensions. D1R12-R1 must not fabricate those missing samples.

D1R12-R1 therefore performs bounded paired replay for only the six hold routes using the parent D1R12 schedule as the bucket SSOT:

```text
attempts per held route <=4096
total held-route replay attempts <=24576
healthy control replay per route <=1024
```

Each replay sample records a same-bucket Burn-only baseline, Burn-authoritative canary duration, TensorCube shadow duration, occupancy, logical queue depth, and the six-dimensional bucket key. Replay uses the same Burn device and queue and remains non-authoritative.

## Canonical Review Key

```text
route_id × shape_id × sequence_bucket × kv_bucket × cadence_class × contention_class
```

## Measurement Gates

Baseline quality:

```text
Exact >=32
Strong >=16
Weak >=8
Insufficient <8
```

Percentile validity:

```text
p50 >=8 samples
p95 >=32 samples
p99 >=128 samples
```

Timestamp resolution:

```text
Reliable >=32 timestamp quanta
Marginal >=8 and <32
Resolution Limited <8
```

Burn-ready latency gates:

```text
Green: p50<=1.10, p95<=1.20, p99<=1.30
Red: p50>1.20 OR p95>1.35 OR p99>1.50
```

Occupancy bounds:

```text
median<=2.25, p95<=2.75, p99<=3.00
```

Confirmed critical-path red requires Exact or Strong baseline quality, a valid triggering percentile, a stable denominator, and Reliable or Marginal timestamp resolution.

## Classification

Bucket classes:

```text
healthy
confirmed_red
conditional_red
diagnostic_only
measurement_limited
evidence_insufficient
```

Route classes:

```text
hold_confirmed
conditional_hold
hold_not_reproduced_by_evidence
measurement_review_required
evidence_insufficient
```

## Protected State

The active registry bytes, route epoch, whitelist, holdlist, K7N shader, RHS ABI, pipeline layout, Burn source, model weights, sampler ownership, and KV ownership must remain unchanged.

Required authority counters:

```text
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
sampler_substitution_count=0
kv_state_mutation_count=0
output_authority=burn
```

## Outcomes

Exactly one outcome:

```text
OUTCOME_ASH_TCU_K7N_D1R12_R1_CONFIRMED_ROUTE_BUCKET_PERFORMANCE_HOLDS
OUTCOME_ASH_TCU_K7N_D1R12_R1_CONDITIONAL_BUCKET_HOLDS_ONLY
OUTCOME_ASH_TCU_K7N_D1R12_R1_PARENT_HOLD_CLASSIFICATION_NOT_REPRODUCED
OUTCOME_ASH_TCU_K7N_D1R12_R1_MEASUREMENT_RESOLUTION_OR_BASELINE_REVIEW_REQUIRED
OUTCOME_ASH_TCU_K7N_D1R12_R1_PARENT_EVIDENCE_INSUFFICIENT
```

## Normal PASS Boundary

```text
active routes reviewed=17
parent healthy routes=11
parent hold routes=6
hold routes derived from parent evidence=true
paired replay attempts<=24576
replay failures=0
route epoch before=1
route epoch after=1
active registry unchanged=true
output authority=burn
one review outcome selected=true
```

PASS means the review completed consistently. It does not mean the six routes are healthy or unsafe and does not authorize canary reactivation or TensorCube production output promotion.

## Next State

```text
confirmed holds -> D1R12-R2 confirmed hold mitigation
conditional holds -> D1R12-R2 conditional scope reduction
hold not reproduced -> D1R12-R2 aggregation repair
measurement review -> D1R12-R2 timestamp and baseline recalibration
evidence insufficient -> D1R12-R2 evidence reconstruction
```
