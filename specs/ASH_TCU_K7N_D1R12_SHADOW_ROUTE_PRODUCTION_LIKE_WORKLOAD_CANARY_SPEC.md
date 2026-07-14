# ASH-TCU-K7N-D1R12 SPEC

## Shadow Route Production-Like Workload Canary

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R12_SHADOW_ROUTE_PRODUCTION_LIKE_WORKLOAD_CANARY`
- Parent execution: `d1r11-ab55edc55fd5fa4ef6a9`
- Parent outcome: `continue_17_signature_shadow`
- Active route epoch: `1`
- Active exact-signature routes: `17`

PASS:

```text
PASS_ASH_TCU_K7N_D1R12_SHADOW_ROUTE_PRODUCTION_LIKE_WORKLOAD_CANARY_TRACE_PROFILE_VALID_CANARY_STABLE_BURN_ONLY_CUTOVER_VERIFIED
```

Hard failure:

```text
FAIL_ASH_TCU_K7N_D1R12_SHADOW_ROUTE_PRODUCTION_LIKE_WORKLOAD_CANARY_OUTPUT_AUTHORITY_OR_CANARY_CONTAINMENT_VIOLATION
```

D1R12 exercises the 17 non-authoritative exact-signature shadow routes under a deterministic production-like canary. It does not grant TensorCube output, sampler or KV authority.

## 2. Parent SSOT

Required D1R11 state:

```text
execution_id=d1r11-ab55edc55fd5fa4ef6a9
soak_outcome=continue_17_signature_shadow
route_epoch_after=1
sustained_healthy_route_count=17
degraded_route_count=0
quarantined_route_count=0
active_route_count_after=17
failure_recovery_drills_valid=true
output_authority=burn
```

The D1R11 manifest, final seal, soak receipt, sustained health receipts, route counters and active D1R9 registry must reconcile before GPU initialization.

## 3. Profile Source Boundary

No external production trace is bundled into the source archive. D1R12 derives route coverage from the verified D1R11 69,632-request sustained-soak evidence and applies a sealed deterministic canary frequency and scheduler-bucket projection.

```text
source_kind=d1r11_sustained_soak_route_coverage_with_canonical_canary_frequency_projection_v1
source_event_count=69632
source_window_count=8
parent_soak_derived_projection=true
```

This is production-like canary evidence, not a claim that real production traffic was observed.

## 4. Canary Schedule

```text
total requests=65536
Burn-only baseline=4096
exact-signature canary=49152
route skip and miss=8192
Burn-only cutover verification=4096
post-recovery diagnostic exact probes=1024
```

The 1,024 recovery probes are diagnostic follow-up and are not included in the 65,536 canary request count.

The 49,152 exact requests preserve the sealed projected histogram. Every route receives at least 256 requests and no route exceeds 50 percent of exact traffic. Histogram Jensen-Shannon divergence must be at most 0.02.

## 5. Route Miss Coverage

The 8,192 skip requests contain 1,024 requests from each class:

```text
holdlist
unknown signature
stride mismatch
shader digest mismatch
ABI digest mismatch
pipeline-layout mismatch
runtime-authority mismatch
trace-derived miss
```

Every skip executes Burn and must not dispatch TensorCube.

## 6. Workload Dimensions

Required sequence buckets:

```text
short
medium
long
very_long
```

Required KV buckets:

```text
empty_or_initial
low
medium
high
near_runtime_limit
```

Required cadence classes:

```text
idle
steady
micro_burst
sustained_burst
```

Required contention classes:

```text
none
light
nominal
heavy
```

At least 64 KV-growth lanes, 128 burst lanes and 64 idle restoration gaps must be represented. At least 25 percent of exact requests must use nominal or heavy same-queue pressure.

## 7. Runtime Ownership

```text
Burn output authority=authoritative
Burn sampler authority=authoritative
Burn KV authority=authoritative
TensorCube output authority=false
TensorCube output commit=false
TensorCube sampler substitution=false
TensorCube KV mutation=false
```

TensorCube uses the same Burn device and queue. It may not create an extra authoritative device or queue.

## 8. Parity and Guard

```text
sample interval=128 successful shadow dispatches
minimum samples per route=8
minimum aggregate samples=416
absolute tolerance=0.00001
relative tolerance=0.00001
guard pattern=0x7FC12345
guard words>=16
```

The control route requires exact-bit parity. All routes require zero failing elements, zero NaN or infinity mismatches and zero guard mutations.

## 9. Tail and Occupancy Gates

Green Burn-ready latency ratios:

```text
p50<=1.10
p95<=1.20
p99<=1.30
```

Red Burn-ready latency ratios:

```text
p50>1.20
p95>1.35
p99>1.50
```

Bounded occupancy:

```text
median<=2.25
p95<=2.75
p99<=3.00
```

Queue-depth p99 ratio must remain at or below 2.00.

## 10. Canary Session Gate

Required state flow:

```text
prepared
→ observing
→ cutover_pending
→ burn_only
→ recovery_pending
→ observing
→ completed
```

The canary gate controls only new shadow submissions. It must not change route membership, route epoch, whitelist, holdlist or route health.

## 11. Cutover Drill

The default drill injects a supervisor-only failure-rate breach:

```text
11 failures / 1000 attempts = 0.011
```

Required result:

```text
drill_cutover_count=1
natural_cutover_count=0
next admitted request Burn-only=true
post-cutover Burn requests=4096
post-cutover Burn successes=4096
post-cutover shadow submissions=0
```

The injected supervisor evidence must not corrupt GPU output or the active registry.

## 12. Explicit Recovery

Recovery requires an explicit operator action and revalidation of:

```text
active registry digest
route epoch
17 active routes
Burn authority
resource lifetime
queue state
```

After recovery, 1,024 diagnostic exact requests must complete with 100 percent shadow success while Burn remains authoritative.

## 13. Resource and Device Gates

At canary checkpoints:

```text
live temporary shadow buffers=0
live parity readback buffers=0
mapped buffers=0
pending callbacks=0
pending submissions=0
```

Natural device-lost, out-of-memory, validation-error and queue-submission-failure counts must all be zero.

## 14. Outcomes

Exactly one outcome is sealed:

```text
OUTCOME_ASH_TCU_K7N_D1R12_CONTINUE_17_SIGNATURE_CANARY
OUTCOME_ASH_TCU_K7N_D1R12_CONTINUE_CANARY_WITH_OBSERVATION_HOLD
OUTCOME_ASH_TCU_K7N_D1R12_STOP_CANARY_PRESERVE_17_SIGNATURE_SHADOW
OUTCOME_ASH_TCU_K7N_D1R12_ACTIVE_REGISTRY_ROLLBACK_EXECUTED
```

The drill cutover is recorded separately from natural cutover.

## 15. Protected State

Forbidden mutations:

```text
whitelist expansion
holdlist promotion
S15 admission
route membership mutation
route epoch mutation
K7N shader mutation
ABI mutation
pipeline-layout mutation
Burn authority mutation
sampler ownership mutation
KV ownership mutation
model-weight mutation
```

## 16. Required Source Files

Backend modules include parent reconciliation, workload profile and expansion, schedule, session gate, actual canary runtime, route hit and skip telemetry, sequence/KV/cadence/contention projection, parity and guards, latency and occupancy, resources, cutover, recovery, health, receipts, authority guard, audit and verdict.

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_production_like_canary_contract.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_production_like_canary_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_shadow_route_production_like_workload_canary.rs
```

## 17. Normal PASS Boundary

```text
parent evidence valid=true
profile valid=true
total canary requests=65536
exact route hits=49152
route skips=8192
cutover verification requests=4096
parity samples>=416
parity failures=0
guard mutations=0
natural cutovers=0
drill cutovers=1
post-cutover shadow submissions=0
post-recovery exact probes=1024
route epoch after=1
active route count after=17
TensorCube authoritative outputs=0
shadow output commits=0
production output commits=0
sampler substitutions=0
KV mutations=0
```

## 18. Next State

```text
continue 17-signature canary
→ ASH-TCU-K7N-D1R13_SHADOW_ROUTE_LIMITED_RUNTIME_CANARY_PROMOTION_REVIEW

observation hold
→ ASH-TCU-K7N-D1R12-R1_ROUTE_BUCKET_LATENCY_AND_CONTENTION_REVIEW

stop canary and preserve registry
→ ASH-TCU-K7N-D1R12-R2_CANARY_CONTAINMENT_AND_WORKLOAD_PROFILE_REVIEW

active registry rollback
→ ASH-TCU-K7N-D1R12-RB1_ACTIVE_REGISTRY_CANARY_FAILURE_POSTMORTEM
```

D1R12 authorizes no TensorCube production output promotion under any outcome.
