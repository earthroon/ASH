# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

## Reference-vs-Atlas Kernel Cost Decomposition /
## Short-KV Dispatch Overhead and Long-KV Memory Traffic Attribution /
## GQA2 Tile Occupancy and Softmax Reduction Optimization /
## Production Crossover Route Evidence Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.runtime_artifact.v1
local_manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.local_manifest.v1
promotion_scope=incremental_decode_only
negative_control_count=1220
```

Revisions:

```text
kernel_cost_decomposition_revision=R2-R7
short_kv_overhead_revision=R2-R7
long_kv_memory_attribution_revision=R2-R7
gqa2_occupancy_revision=R2-R7
softmax_reduction_revision=R2-R7
production_crossover_revision=R2-R7
```

R7 changes bounded kernel candidates, analytical cost receipts, performance attribution and crossover evidence. Attention semantics, causal visibility, Q/K/V and output layouts, guard/downstream math, R6-R1 scratch usage, mirrored input identity and paired non-inferiority policy remain unchanged.

## 1. Bound evidence

R6-R1 established resource and validation truth. Matched guarded E2E showed Atlas winning at `seq_kv=8,16`, tying at `32`, and losing to Reference from `64` through `2048`. Kernel-only probes showed long-KV GQA2 beating Single Atlas, so Single-vs-GQA2 evidence cannot establish Reference-vs-Atlas route authority.

R7 separates:

```text
cost attribution authority
kernel candidate authority
matched E2E production authority
```

## 2. Cost domains

Required domains:

```text
HostPreparation
CommandEncoding
QueueSubmission
PipelineDispatchFixed
QLoad
KLoad
QKDotProduct
SoftmaxMaxReduction
SoftmaxExponentiation
SoftmaxSumReduction
SoftmaxNormalization
VLoad
ValueAccumulation
OutputStore
GuardAndDownstream
```

Host clocks, GPU timestamps and analytical estimates are never merged into one authority. Analytical byte estimates are not reported as hardware counters.

## 3. Cost receipts

For Reference and active Atlas route, each canonical bucket records:

```text
Q/K/V scalar loads
output stores
QK FMA count
exp count
max and sum reduction count
reciprocal count
value FMA count
workgroup barriers
subgroup shuffle proxy
global atomic count
```

Memory receipts distinguish:

```text
logical K/V bytes
estimated physical K/V bytes
duplicate-load bytes
padding bytes
K read amplification
V read amplification
estimated effective bytes/ns
```

`hardware_counter_measured=false` is mandatory for analytical traffic receipts.

## 4. Short-KV model

Buckets:

```text
8,16,32,64,128
```

Model:

```text
T(seq_kv)=fixed_overhead_ns+per_token_ns*seq_kv+residual
```

Reference and Single Atlas are fitted independently from matched GPU timestamp medians. The model is diagnostic-only and cannot promote a route.

## 5. GQA2 optimized candidate

Canonical R7 candidate:

```text
candidate_id=gqa2_kv32_dpl2_sg2_qh2_vc32_softmax_online_single_v2
kernel_id=subgroup32_gqa2_long_kv_tiled_v2
KV tile=32
head dimensions=64
workgroup size=64
subgroup size=32
subgroups per workgroup=2
query heads consumed per workgroup=2
K workgroup tile bytes=8192
V workgroup tile bytes=8192
total workgroup memory=16384 bytes
```

Compared with the previous tile-8 implementation, tile-32 reduces workgroup barrier pairs per 2048-token pass from 256 to 64. This is a candidate optimization, not a predeclared performance victory.

Required properties:

```text
K/V loaded once per tile per two-query-head workgroup
online max/denominator/value accumulation
intermediate global softmax traffic=0
global atomics=0
f32 accumulation retained
partial final tile bounded
out-of-range access count=0
```

## 6. Candidate registry

One registry owns IDs, shader entry points, tile geometry, softmax strategy, diagnostic status and promotion eligibility.

Canonical entries include:

```text
Reference online-softmax fallback
Single Atlas short-KV route
GQA2 tile-32 v2
GQA2 tile-64 diagnostic-only declaration
```

Candidate lifecycle:

```text
Declared
StaticRejected
Compiled
ParityRejected
ScreenRejected
FullBenchmark
E2EConfirmation
PromotionEligible
Held
```

A diagnostic-only or rejected candidate cannot become a production route.

## 7. Measurement boundary

Production authority continues to use monolithic matched guarded E2E samples. Cost decomposition and operation/traffic estimates are diagnostic-only.

Required zero counters:

```text
instrumented_production_sample_count=0
timed_pipeline_creation_count=0
timed_shader_compilation_count=0
timed_bind_group_creation_count=0
raw_sample_drop_count=0
raw_sample_rewrite_count=0
```

## 8. Occupancy and softmax receipts

R7 records static occupancy proxies:

```text
workgroup size
subgroup count
workgroup memory bytes
active and inactive lanes
lane utilization ratio
estimated live scalar pressure class
```

These are static estimates, not achieved occupancy or compiler register counts.

Softmax receipts record:

```text
strategy
reduction levels
barriers per tile
intermediate global reads/writes
global atomics
numerical parity
```

## 9. P95 outlier attribution

The canonical `seq_kv=256` bucket retains all raw samples. An outlier is classified relative to the raw Atlas median and reported by round and AB/BA order.

Forbidden:

```text
outlier deletion
winsorization
filtered p95 promotion
selective failed-round rerun
```

If the outlier disappears, the receipt says `not-reproduced`. If it remains without a deterministic source, it remains an explicit HOLD component.

## 10. Production crossover evidence

Per measured bucket, production winner is selected only from matched guarded E2E evidence:

```text
AtlasShortKv
ReferenceOnlineSoftmax
AtlasGqa2Optimized
```

Reference is mandatory fallback. GQA2-vs-Single kernel evidence cannot substitute for Reference-vs-Atlas evidence.

The evidence LUT is bounded to canonical measured buckets. Any interpolation into unmeasured ranges requires a later explicit promotion patch.

Tie policy:

```text
prefer-existing-production
```

## 11. Route authority

```text
cost receipts -> diagnostic authority only
occupancy and traffic -> candidate design authority only
kernel-only benchmark -> kernel candidate authority
matched guarded E2E -> production route authority
```

A candidate requires parity, kernel median/p95, non-inferiority, order-bias, thermal validity, matched E2E, guard, canary and rollback truth before promotion.

## 12. CLI additions

```text
--kernel-cost-decomposition true
--kernel-stage-profile-mode diagnostic-only
--require-instrumented-production-samples-zero true
--cost-profile-buckets 8,16,32,64,128,256,512,1024,2048
--require-operation-accounting true
--require-memory-traffic-accounting true
--require-logical-physical-byte-separation true
--short-kv-model linear-fixed-plus-token-v1
--short-kv-buckets 8,16,32,64,128
--require-short-kv-fixed-overhead-attribution true
--gqa2-candidate-search bounded-matrix-v1
--gqa2-kv-tiles 32,64,128
--gqa2-dimensions-per-lane 1,2,4
--gqa2-subgroups-per-workgroup 1,2,4
--gqa2-query-heads-per-workgroup 1,2
--gqa2-value-chunks 16,32,64
--maximum-kernel-candidates 36
--softmax-strategies existing,online-single,online-two-level,subgroup-fused
--require-softmax-numerical-parity true
--require-global-atomic-zero true
--require-shared-kv-load-receipt true
--require-vector-load-alignment-receipt true
--require-workgroup-memory-budget true
--require-register-pressure-proxy true
--require-lane-utilization-receipt true
--candidate-screen-pairs 128
--candidate-full-pairs 1024
--candidate-full-rounds 32
--candidate-full-pairs-per-round 32
--require-candidate-vs-current-atlas true
--require-candidate-vs-reference true
--require-matched-e2e-confirmation true
--require-p95-outlier-attribution true
--forbid-raw-sample-filtering true
--forbid-selective-round-rerun true
--production-route-policy evidence-lut-v4
--require-crossover-neighbor-stability true
--require-explicit-tie-policy true
--route-tie-policy prefer-existing-production
--require-reference-fallback true
--expected-negative-controls 1220
```

## 13. Negative controls

R7 inherits 1160 controls and adds 60:

```text
cost decomposition=10
memory traffic=10
occupancy and softmax=10
candidate lifecycle=10
performance and outlier=10
crossover and routing=10
```

Required aggregate:

```text
count=1220
executed=1220
skipped=0
fail=0
```

## 14. PASS boundary

PASS requires complete cost and traffic receipts, valid bounded candidate registry, parity-safe candidates, no timed compilation/allocation, valid short-KV model, no raw-sample filtering, resolved or non-reproduced p95 outlier, stable production crossover receipts, deterministic evidence LUT, reachable Reference fallback, matched guarded E2E non-inferiority for every adopted Atlas route, guard/canary/rollback truth and 1220 negative controls.

Diagnostic closure without a Reference-noninferior Atlas candidate is a valid HOLD.

## 15. Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_REFERENCE_VS_ATLAS_KERNEL_COST_DECOMPOSITION_SHORT_KV_DISPATCH_OVERHEAD_LONG_KV_MEMORY_TRAFFIC_ATTRIBUTION_GQA2_TILE_OCCUPANCY_SOFTMAX_REDUCTION_OPTIMIZATION_PRODUCTION_CROSSOVER_ROUTE_EVIDENCE_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

Diagnostic HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_COST_DECOMPOSITION_ESTABLISHED_NO_ATLAS_CANDIDATE_NON_INFERIOR_TO_REFERENCE
```

Evidence HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_KERNEL_COST_OR_CROSSOVER_EVIDENCE_INCOMPLETE
```

## 16. Final authority boundary

```text
Reference remains fallback wherever Atlas does not win.
Tile-32 v2 receives no authority from design intent alone.
Operation and traffic models explain cost but cannot pass performance.
Only raw matched E2E evidence changes the production winner.
```
