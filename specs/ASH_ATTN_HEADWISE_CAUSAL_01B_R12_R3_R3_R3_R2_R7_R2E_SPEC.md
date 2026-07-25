# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E

## GQA4 Cluster Kernel Cost Decomposition / Shared Texture-Load Reuse Performance Receipt / Paired GPU Timestamp Atlas / Kernel-Only Non-Inferiority and Candidate Eligibility Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PRODUCTION_ROUTE_MUTATION=forbidden
PRODUCTION_GUARD_REBIND=forbidden
DOWNSTREAM_COMMIT=forbidden
PERFORMANCE_SAMPLE_FILTERING=forbidden
PREBAKED_RUNTIME_EVIDENCE=forbidden
```

R7-R2E measures the promoted R7-R2D GQA4 cluster candidate against four single-query-head immutable texture-KV reference dispatches representing the same four-head logical workload. Both paths execute in one compute pass, one command encoder, and one queue submission per pair. GPU timestamps are written inside the compute pass. The revision proves kernel-only non-inferiority and candidate eligibility. It does not promote the production route.

The reference is the R7-R2C immutable texture-KV single-head surface, not a buffer-K/V substitute. Each reference head loads one RGBA K texel and one RGBA V texel per dimension group and token, so the measured physical texture-load ratio is exactly four reference loads to one cluster load.

## 1. Parent binding

The parent R7-R2D artifact and manifest must report:

```text
gpu=true
topology_pass=true
structural_pass=true
numerical_envelope_pass=true
shared_load_reuse_pass=true
barrier_uniformity_pass=true
active_path_unchanged_pass=true
pass=true
```

The R7-R2D residency, buffer-Q identity, immutable texture-KV identity, GQA4 coordinate authority, subgroup topology, and fixed numerical envelope remain authoritative.

## 2. Long-KV capacity closure

The R7-R2D validation matrix ended at 384 tokens and used a 12-entry shared physical-page tile table. R7-R2E measures through 2048 tokens, which requires 64 token tiles at tile width 32.

R7-R2E therefore defines an explicit candidate capacity extension:

```text
physical workgroup topology=128x1x1
logical topology=4xsubgroup32
token tile=32
maximum KV length=2048
maximum tile count=64
shared physical-page tile table entries=64
```

The table expansion changes capacity only. Query-head ownership, K/V texture coordinates, exact integer textureLoad, subgroup reductions, online softmax, output ownership, and production isolation remain unchanged.

Before timestamp collection, every performance bucket must pass the R7-R2D numerical and structural validation surfaces. Timestamp evidence is forbidden when long-KV numerical preflight fails.

## 3. Compared logical workload

One paired sample covers:

```text
batch=1
query position=1
query heads=4
shared KV head=1
head dimension=64
visible KV length=bucket
```

Reference:

```text
four single-query-head immutable texture-KV attention dispatches
one dispatch per query head
one combined timestamp span
```

Candidate:

```text
one R7-R2E long-capacity GQA4 cluster dispatch
four query heads sharing one immutable texture-KV tile stream
one timestamp span
```

The two paths share Device, Queue, Q values, immutable K/V textures, page-table identity, page generation, scale, causal visibility, query-head set, and output shape. Their output scratch buffers must not alias each other or production output.

## 4. Performance buckets

```text
performance buckets=128,256,384,512,768,1024,1536,2048
eligibility buckets=512,768,1024,1536,2048
short cost-model buckets=128,256,384,512
```

The immutable residency contains 16 sealed pages of 128 tokens. Missing pages, stale generation, texture rebuild, or page-table mutation cause HOLD.

## 5. Paired GPU timestamp atlas

Required features:

```text
TIMESTAMP_QUERY
TIMESTAMP_QUERY_INSIDE_ENCODERS
TIMESTAMP_QUERY_INSIDE_PASSES
```

CPU timers cannot substitute for GPU timestamps.

Each pair owns four query indices:

```text
reference_begin
reference_end
candidate_begin
candidate_end
```

Canonical geometry:

```text
pairs per round=32
timestamps per pair=4
queries per round=128
measurement rounds per bucket=32
measurement pairs per bucket=1024
warmup pairs per bucket=128
timestamp query-set ring capacity=4
resolve-buffer ring capacity=4
readback-buffer ring capacity=4
```

Each pair uses exactly one compute pass, one encoder, and one queue submission. Reference and candidate may switch pipelines inside the pass. No per-kernel submission or per-pair readback is permitted. Timestamp resolution and compact timestamp readback occur once per round, outside timed spans.

## 6. Pair and epoch order

Pair order is balanced interleaved AB/BA:

```text
even pair=reference then candidate
odd pair=candidate then reference
```

Bucket epochs are:

```text
ascending=128 to 2048
descending=2048 to 128
```

Each bucket receives 512 samples in each epoch and 512 samples in each pair order. Unequal counts cause HOLD.

## 7. Timed-span isolation

Timed spans contain only attention dispatches.

Forbidden inside either span:

```text
allocation
pipeline creation
bind-group creation
scratch resize
buffer clear
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

All pipelines, bind groups, scratch buffers, timestamp objects, readback buffers, residency pages, and page-table entries are created and frozen before measurement.

## 8. Raw-sample authority

All 8,192 paired samples are retained in the runtime receipt.

Forbidden:

```text
sample trimming
outlier deletion
failed-round deletion
selective rerun
zero-duration replacement
negative-delta correction
median-of-medians substitution
synthetic sample insertion
vendor-specific smoothing
```

A malformed sample fails its whole bucket. A failed bucket is not removed from the verdict.

## 9. Statistics

Per reference, candidate, and paired ratio distribution, Rust emits:

```text
count
minimum
median
mean
p90
p95
p99
maximum
standard deviation
median absolute deviation
```

Methods:

```text
median=sorted midpoint
quantile=nearest rank
ratio=candidate_ns/reference_ns
```

Reference duration zero or non-finite timestamps cause HOLD. Ratio denominator clamping is forbidden.

## 10. Order and thermal gates

Order bias:

```text
abs(median_AB-median_BA)/combined_median <= 0.05
```

The gate applies independently to reference and candidate.

Epoch bias:

```text
abs(median_ascending-median_descending)/combined_median <= 0.07
```

The gate applies independently to reference and candidate. An invalid order or thermal bucket fails the full revision.

## 11. Non-inferiority

Canonical policy:

```text
test=paired-sign-upper-bound-v1
alpha=0.05
margin ratio=1.05
minimum effective pairs=512
tie policy=exclude boundary
```

Each bucket additionally requires:

```text
median candidate/reference ratio <= 1.05
p95 candidate/reference ratio <= 1.10
paired sign-test upper-tail probability <= 0.05
order-bias gate pass
thermal-epoch gate pass
```

All performance buckets must pass non-inferiority.

## 12. Candidate eligibility

Long-bucket practical improvement requires:

```text
median candidate/reference ratio <= 0.95
p95 candidate/reference ratio <= 1.05
```

Candidate eligibility requires:

```text
all performance buckets non-inferior
at least 3 of 5 eligibility buckets improved
1024 bucket improved
1536 bucket improved
2048 bucket improved
shared K reuse factor=4
shared V reuse factor=4
physical load reduction exact
order and thermal gates pass
active production path unchanged
```

Non-inferiority alone must never be reported as superiority or eligibility.

## 13. Shared-load and byte receipt

For each bucket:

```text
candidate physical K vec4 loads=KV length*16
candidate physical V vec4 loads=KV length*16
reference physical K textureLoad count=candidate*4
reference physical V textureLoad count=candidate*4
candidate K reuse factor=4
candidate V reuse factor=4
```

RGBA32F texel size is 16 bytes. Logical reads, physical texture loads, shared-memory consumer reads, and byte counts remain separate fields. Shared-memory reads cannot be labeled texture traffic.

## 14. Cost decomposition

Promotion evidence uses only uninstrumented monolithic kernel timestamps.

R7-R2E diagnostic cost decomposition uses:

```text
actual paired elapsed-time distributions
physical and logical K/V load accounting
RGBA32F physical-byte accounting
shared-memory consumer-read accounting
short-KV fixed-plus-token linear fit
```

Canonical cost model:

```text
T_reference(kv)=F_reference+kv*C_reference
T_candidate(kv)=F_candidate+kv*C_candidate
```

The model emits intercept, token slope, and R-squared for both paths. It is diagnostic-only and cannot replace raw timestamp evidence. Instrumented promotion sample count must be zero.

## 15. CLI extension

```text
--gqa4-performance-policy paired-gpu-timestamp-atlas-v1
--gqa4-performance-surface kernel-only-v1
--gqa4-reference-execution-policy four-single-query-heads-one-span-v1
--gqa4-candidate-execution-policy one-four-head-cluster-one-span-v1
--gqa4-performance-buckets 128,256,384,512,768,1024,1536,2048
--gqa4-eligibility-buckets 512,768,1024,1536,2048
--gqa4-warmup-pairs-per-bucket 128
--gqa4-measurement-pairs-per-bucket 1024
--gqa4-measurement-rounds-per-bucket 32
--gqa4-pairs-per-round 32
--gqa4-pair-order interleaved-ab-ba
--gqa4-epoch-order ascending,descending
--gqa4-timestamps-per-pair 4
--gqa4-queries-per-round 128
--gqa4-timestamp-ring-capacity 4
--gqa4-resolve-ring-capacity 4
--gqa4-readback-ring-capacity 4
--gqa4-statistics-source raw-paired-samples-v1
--gqa4-median-method sorted-midpoint-v1
--gqa4-quantile-method nearest-rank-v1
--gqa4-noninferiority-test paired-sign-upper-bound-v1
--gqa4-noninferiority-alpha 0.05
--gqa4-noninferiority-margin-ratio 1.05
--gqa4-minimum-effective-pairs 512
--gqa4-tie-policy exclude-boundary
--gqa4-cost-decomposition-policy diagnostic-only-separated-v1
--gqa4-short-kv-cost-model linear-fixed-plus-token-v1
--gqa4-candidate-eligibility-policy long-bucket-three-win-v1
--gqa4-long-kv-page-table-policy shared-64-tile-capacity-v1
--gqa4-long-kv-preflight-policy numerical-before-timestamp-v1
```

Required Boolean keys:

```text
--require-gqa4-timestamp-query-feature true
--require-gqa4-inside-pass-timestamps true
--require-gqa4-one-encoder-per-pair true
--require-gqa4-one-submission-per-pair true
--require-gqa4-per-kernel-submit-zero true
--require-gqa4-per-pair-readback-zero true
--require-gqa4-wait-outside-timed-span true
--require-gqa4-allocation-outside-timed-span true
--require-gqa4-clear-outside-timed-span true
--require-gqa4-resolve-outside-timed-span true
--require-gqa4-input-identity true
--require-gqa4-generation-lock true
--require-gqa4-scratch-isolation true
--require-gqa4-raw-sample-retention true
--forbid-gqa4-sample-filtering true
--forbid-gqa4-selective-rerun true
--require-gqa4-ab-ba-balance true
--require-gqa4-order-bias-gate true
--require-gqa4-thermal-epoch-gate true
--require-gqa4-shared-load-receipt true
--require-gqa4-logical-physical-byte-separation true
--require-gqa4-reuse-factor-four true
--require-gqa4-diagnostic-promotion-separation true
--require-gqa4-operation-accounting true
--require-gqa4-cost-model-receipt true
--require-gqa4-all-bucket-noninferiority true
--require-gqa4-long-bucket-improvement true
--require-gqa4-1024-eligibility true
--require-gqa4-1536-eligibility true
--require-gqa4-2048-eligibility true
--require-gqa4-long-kv-capacity-preflight true
--require-gqa4-long-kv-numerical-preflight true
--require-gqa4-authority-commit-order true
```

The inherited R7-R2D keys `--require-gqa4-production-consumer-zero`, `--require-gqa4-candidate-output-commit-zero`, and `--require-gqa4-active-route-unchanged` remain authoritative and are validated again without duplicate registry ownership.

Unknown, duplicate, missing, token-adhered, silently defaulted, or last-write-wins keys are forbidden.

## 16. Negative controls

Exactly 140 executed controls are required, ten each for:

```text
parent and identity
timestamp capability
pair topology
order and epoch
raw samples
statistics
shared-load accounting
timed-span contamination
cost decomposition
non-inferiority
candidate eligibility
isolation
capacity and ring safety
artifact authority
```

Expected count is derived from the registry. Fault injection must not mutate production route state.

## 17. Rust outputs

Rust emits, at minimum:

```text
parent binding receipt
static checks
active path before/after snapshots
performance receipt
all raw paired samples
bucket statistics and ratios
order and epoch bias receipts
shared-load and byte accounting
cost decomposition
short-KV model
candidate eligibility receipt
negative-control registry and outcomes
strict CLI receipts and canonical command
runtime artifact
local manifest
verdict
```

The code ZIP excludes specs, scripts, manifests, artifacts, receipts, verdicts, runtime JSON, PowerShell, batch files, and run-command files.

## 18. PASS

```text
parent R7-R2D pass
long-KV 64-tile capacity preflight pass
all 128 to 2048 numerical preflights pass
timestamp features pass
one pass, encoder, and submission per pair
per-kernel submit count=0
per-pair readback count=0
timed contamination counts=0
all 8192 raw samples retained
sample filtering count=0
selective rerun count=0
AB/BA balance exact
ascending/descending epochs complete
order-bias gate pass
thermal-epoch gate pass
K/V reuse factor=4
physical load reduction exact
all buckets non-inferior
required long buckets improved
candidate eligibility pass
payload readback count=0
candidate output commit count=0
production consumer count=0
active production path unchanged
140/140 negative controls pass
Rust artifact and manifest emitted
```

## 19. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2E_GQA4_CLUSTER_KERNEL_PERFORMANCE_NONINFERIOR_AND_CANDIDATE_ELIGIBLE_SEALED
```

Representative HOLD:

```text
HOLD_..._R2E_LONG_KV_CAPACITY_OR_NUMERICAL_PREFLIGHT_INCOMPLETE
HOLD_..._R2E_GPU_TIMESTAMP_ATLAS_CAPABILITY_INCOMPLETE
HOLD_..._R2E_PAIRED_KERNEL_MEASUREMENT_TOPOLOGY_INVALID
HOLD_..._R2E_TIMED_KERNEL_SPAN_CONTAMINATED
HOLD_..._R2E_RAW_PAIRED_SAMPLE_AUTHORITY_INVALID
HOLD_..._R2E_SHARED_TEXTURE_LOAD_REUSE_RECEIPT_INCOMPLETE
HOLD_..._R2E_GQA4_KERNEL_NONINFERIORITY_NOT_PROVEN
HOLD_..._R2E_GQA4_KERNEL_CANDIDATE_ELIGIBILITY_NOT_PROVEN
HOLD_..._R2E_PERFORMANCE_CANDIDATE_ESCAPED_INTO_PRODUCTION_PATH
```

## 20. Rollback and next revision

Rollback removes the R7-R2E long-KV candidate capacity extension, reference benchmark shader, paired timestamp atlas, performance gate, cost model, CLI extension, and R7-R2E evidence. R7-R2D correctness evidence, R7-R2C hybrid binding, R7-R2B residency, and the active production buffer route remain intact.

Next:

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F
GQA4 Cluster Guard Binding /
Matched Output Scratch and Downstream Contract /
Guarded End-to-End Paired GPU Timestamp /
Production-Route Shadow Eligibility Seal
```

## 21. Final seal statement

The four-head immutable texture-KV reference and GQA4 cluster candidate processed identical logical attention inputs. Every pair used one compute pass, one encoder, one submission, four inside-pass GPU timestamps, balanced AB/BA ordering, ascending and descending epochs, and unfiltered raw samples. Long-KV capacity and numerical parity were validated before timing. Candidate physical K/V traffic was exactly one quarter of the four-head reference texture traffic, while logical work remained identical. All buckets met the fixed non-inferiority contract and the required long buckets demonstrated stable practical improvement without order bias, thermal inconsistency, timed-span contamination, payload readback, sample filtering, output commit, or production-route mutation.