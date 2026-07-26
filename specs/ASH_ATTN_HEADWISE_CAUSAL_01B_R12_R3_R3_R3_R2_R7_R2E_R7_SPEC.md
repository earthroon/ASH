# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E-R7

## Self-Primed Paired Timestamp Block / Pipeline Transition Exclusion / Mirrored Round-Level Bucket Interleave / Signed Bias and Core Performance Separation Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E-R7
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E
PARENT_RUNTIME=R2E-R6 observed HOLD artifact
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PERFORMANCE_SEMANTICS=steady-state-same-path-self-primed-v1
PRODUCTION_ROUTE_MUTATION=forbidden
CANDIDATE_OUTPUT_COMMIT=forbidden
KERNEL_ARITHMETIC_MUTATION=forbidden
NUMERICAL_TOLERANCE_WIDENING=forbidden
PERFORMANCE_SAMPLE_FILTERING=forbidden
SELECTIVE_RERUN=forbidden
PREBAKED_RUNTIME_EVIDENCE=forbidden
```

R7 preserves the R2E-R6 candidate and reference WGSL byte identity and repairs only the paired GPU timestamp measurement topology. It proves that the already observed core speedup remains valid after each path is self-primed and bucket history is mirrored at global-round granularity.

## 1. Parent binding

The parent R2E artifact may have `pass=false` because order or epoch validity was not proven. R7 must nevertheless require:

```text
patch_id=...R2E
long_kv_numerical_preflight_pass=true
long_bucket_improvement_pass=true
shared_load_reuse_pass=true
active_path_unchanged_pass=true
negative_control_expected=140
```

R7 reads the parent static-check artifact through the parent manifest and requires exact candidate and reference WGSL SHA-256 parity before GPU initialization. Parent HOLD evidence is not promoted or rewritten.

## 2. Immutable kernel boundary

The following identities remain byte-exact:

```text
headwise_gqa4_cluster_attention.wgsl
headwise_gqa4_performance_reference_single_head.wgsl
candidate workgroup topology=128x1x1
reference workgroup topology=32x1x1
candidate token tile=32
candidate denominator canonicalization arithmetic
texture coordinate and page-table policy
shared K/V reuse factor=4
```

Allowed changes are limited to Rust measurement orchestration, dedicated primer scratch, scheduling, receipt fields, CLI registry, and verdict wiring.

## 3. Compared workload

One pair covers:

```text
batch=1
seq_q=1
query heads=4
KV heads=1
head dimension=64
visible KV length=bucket
```

Reference remains four single-query-head texture-KV dispatches. Candidate remains one four-query-head GQA4 cluster dispatch. Device, Queue, Q values, immutable K/V textures, page-table generation, causal visibility, scale, and logical output shape are identical.

## 4. Self-primed blocks

Reference block:

```text
select reference pipeline
reference primer dispatches x4 into dedicated primer scratch
bind first measured reference head
reference_begin timestamp
measured reference dispatches x4
reference_end timestamp
```

Candidate block:

```text
select candidate pipeline
candidate primer dispatch x1 into dedicated primer scratch
bind measured candidate output
candidate_begin timestamp
measured candidate dispatch x1
candidate_end timestamp
```

Primer and measured paths use identical shader, geometry, inputs, page generation, and visibility. Only output scratch ownership differs.

Primer output is never read back, committed, included in raw promotion samples, or used as production output.

## 5. Transition-exclusion truth

The measured candidate span contains one candidate attention dispatch only. The measured reference span contains the four canonical reference attention dispatches.

The following are forbidden between each path's begin/end timestamps:

```text
pipeline transition
primer dispatch
allocation
buffer clear
scratch resize
texture population
page-table mutation
timestamp resolve
readback copy
host wait
telemetry copy
guard dispatch
O-projection
residual
downstream dispatch
```

The reference path necessarily selects heads 1 through 3 with three bind-group changes inside its combined four-head span. These are intrinsic reference head-selection commands, not pipeline-transition contamination. Rust must publish their exact count separately as:

```text
reference_timed_head_bind_group_switch_count = measured_pairs * 3
```

This count must never be reported as zero. Candidate timed bind-group switch count is zero because its measured bind group is selected before `candidate_begin`.

## 6. Pair topology

AB:

```text
self-primed reference block
self-primed candidate block
```

BA:

```text
self-primed candidate block
self-primed reference block
```

Each pair uses one command encoder, one compute pass, and one submission. Four timestamp indices remain assigned to reference begin/end and candidate begin/end. Per-kernel submission and per-pair readback remain zero.

## 7. Round-rotated pair order

Each bucket visit contains 32 pairs and exactly 16 AB plus 16 BA. Order is derived deterministically:

```text
order_bit = pair_index_in_round XOR global_round_index XOR bucket_position_in_round
0=AB
1=BA
```

This prevents a bucket, round parity, or ring slot from permanently owning one path order.

## 8. Mirrored global-round schedule

R7 replaces bucket-major epochs with 32 global rounds. Every global round visits all eight buckets once and measures 32 pairs per visit.

Schedule A:

```text
128,2048,256,1536,384,1024,512,768
```

Schedule B is the exact reverse:

```text
768,512,1024,384,1536,256,2048,128
```

Even global rounds use A. Odd global rounds use B.

Per bucket:

```text
32 visits
1024 pairs
512 mirrored_a samples
512 mirrored_b samples
512 AB samples
512 BA samples
```

The legacy inherited CLI values `gqa4-pair-order=interleaved-ab-ba` and `gqa4-epoch-order=ascending,descending` remain ancestry tokens only. The R7 schedule and order policy fields are authoritative.

## 9. Warmup

Warmup uses four mirrored global rounds, 32 pairs per bucket visit, and the same self-primed block topology. Warmup timestamps are not retained and warmup pairs are excluded from all promotion statistics.

## 10. Raw-sample authority

All 8,192 measured pairs are retained. Every sample includes:

```text
global_round_index
mirrored_epoch
bucket_position_in_round
kv_length
pair_index
pair_index_in_round
order
query_set_ring_slot
resolve_ring_slot
readback_ring_slot
reference_ns
candidate_ns
candidate_to_reference_ratio
```

Filtering, trimming, outlier deletion, selective rerun, ratio clamping, median-of-medians substitution, and synthetic sample insertion are forbidden.

## 11. Signed order receipt

Per bucket Rust publishes:

```text
reference_ab_median_ns
reference_ba_median_ns
candidate_ab_median_ns
candidate_ba_median_ns
reference_order_bias_signed_ratio
candidate_order_bias_signed_ratio
reference_order_bias_ratio
candidate_order_bias_ratio
```

Formula:

```text
signed=(median_AB-median_BA)/combined_median
absolute=abs(signed)
```

Positive means AB is slower. Negative means AB is faster. Order validity remains:

```text
reference absolute <= 0.05
candidate absolute <= 0.05
```

## 12. Signed mirrored-epoch receipt

Per bucket Rust publishes A/B medians, signed ratios, and absolute ratios for reference and candidate.

```text
signed=(median_mirrored_a-median_mirrored_b)/combined_median
absolute=abs(signed)
```

Mirrored-epoch validity remains:

```text
reference absolute <= 0.07
candidate absolute <= 0.07
```

## 13. Core performance separation

Core non-inferiority excludes order and epoch validity:

```text
effective pairs >= 512
paired sign-test upper-tail probability <= 0.05
ratio median <= 1.05
ratio p95 <= 1.10
```

Long improvement remains:

```text
ratio median <= 0.95
ratio p95 <= 1.05
at least 3 of 5 eligibility buckets improved
1024,1536,2048 all improved
```

Canonical fields:

```text
all_bucket_core_noninferiority_pass
long_bucket_core_improvement_pass
core_performance_pass
order_bias_validity_pass
mirrored_epoch_validity_pass
measurement_validity_pass
candidate_eligibility_pass
```

Eligibility authority:

```text
candidate_eligibility_pass =
    core_performance_pass
    AND measurement_validity_pass
    AND shared_load_reuse_pass
    AND primer_topology_pass
    AND primer_isolation_pass
    AND pipeline_transition_exclusion_pass
    AND mirrored_schedule_pass
    AND signed_bias_receipt_pass
    AND isolation_pass
```

A validity failure must not rewrite `core_performance_pass=false`.

## 14. Primer receipt

Rust publishes measured and warmup primer dispatch counts, dedicated scratch ownership, zero primer readback, zero primer promotion samples, zero timed primer dispatches, and zero timed pipeline switches.

Canonical measured counts:

```text
reference primer dispatches=8192*4
candidate primer dispatches=8192
reference measured dispatches=8192*4
candidate measured dispatches=8192
pipeline switches before primer=8192*2
reference intrinsic timed head bind changes=8192*3
```

These counts are accumulated while commands are encoded. The topology and transition verdicts are derived from the accumulated command receipt rather than assigned as unconditional constants.

## 15. Progress observability

Each bucket visit and global round emits progress outside timestamp spans:

```text
[r7-r2e-r7][measure] ...
[r7-r2e-r7][round] ...
```

Long silent measurement intervals are forbidden.

## 16. CLI extension

```text
--gqa4-measurement-block-policy self-primed-paired-block-v1
--gqa4-primer-policy same-path-exact-geometry-v1
--gqa4-primer-output-policy dedicated-isolated-scratch-v1
--gqa4-pipeline-transition-policy excluded-before-primer-v1
--gqa4-transition-exclusion-scope pipeline-primer-allocation-resolve-v1
--gqa4-reference-timed-head-bind-policy intrinsic-four-head-sequence-v1
--gqa4-bucket-schedule-policy alternating-mirrored-round-interleave-v1
--gqa4-pair-order-policy round-bucket-rotated-ab-ba-v1
--gqa4-bias-report-policy signed-and-absolute-v1
--gqa4-performance-verdict-policy core-validity-separated-v1
--gqa4-performance-semantics steady-state-same-path-self-primed-v1
--gqa4-mirrored-schedule-a 128,2048,256,1536,384,1024,512,768
--gqa4-mirrored-schedule-b 768,512,1024,384,1536,256,2048,128
--gqa4-global-rounds 32
--gqa4-pairs-per-bucket-visit 32
```

Required booleans cover both self primers, geometry and input identity, primer scratch isolation, zero primer readback and promotion samples, pipeline and primer exclusion, reference intrinsic bind-switch accounting, mirrored schedule exactness, round-level interleave, pair-order rotation, signed receipts, core/validity separation, and eligibility authority order.

## 17. Negative controls

Parent 140 controls remain bound through the parent artifact. R7 executes 120 additional controls, ten each for:

```text
parent identity
kernel identity freeze
reference primer topology
candidate primer topology
primer scratch isolation
pipeline transition exclusion
timed-span purity
mirrored bucket schedule
pair and epoch balance
signed bias receipt
core and validity separation
raw-sample and artifact authority
```

Total bound evidence count is 260. R7 controls are runtime-generated and no prebaked outcomes are accepted.

## 18. PASS

PASS requires:

```text
parent evidence bound
candidate/reference WGSL hashes unchanged
all long-KV numerical preflights pass
self-primer topology and isolation pass
zero timed primer and pipeline-switch counts
reference intrinsic head-bind count exact
32 mirrored global rounds complete
8192 raw pairs retained
AB/BA and mirrored A/B counts exact
all bucket core non-inferiority pass
long core improvement pass
all order validity gates pass
all mirrored-epoch validity gates pass
measurement validity pass
shared K/V reuse factor=4
payload readback=0
candidate output commit=0
production consumer=0
active route unchanged
parent 140 plus R7 120 controls bound/pass
Rust artifact and manifest emitted
```

## 19. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3-R3-R2-R7-R2E-R7_SELF_PRIMED_PAIRED_TIMESTAMP_MEASUREMENT_VALIDITY_AND_CORE_PERFORMANCE_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2E_R7_MEASUREMENT_VALIDITY_OR_CANDIDATE_ELIGIBILITY_NOT_PROVEN
```

Representative failure dimensions:

```text
kernel_identity_freeze
self_primer
pipeline_transition_exclusion
mirrored_schedule
core_noninferiority
long_core_improvement
order_bias_validity
mirrored_epoch_validity
measurement_validity
candidate_eligibility
raw_sample_authority
active_path_unchanged
```

## 20. Non-goals

R7 does not promote the production route, bind the production guard, commit candidate output, alter attention arithmetic, widen tolerances, optimize the kernel, filter samples, or claim cold-start performance.
