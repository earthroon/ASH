# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D

## RGBA Texture GQA4 Parallel Cluster Kernel / Shared KV Tile Population / Four Query-Head Concurrent Consumption / Kernel-Only Numerical and Structural Validation Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
PATCH_CLASS=gqa4-cluster-kernel,shared-kv-tile,four-query-head-concurrency,subgroup-parallelism,kernel-numerical-validation,kernel-structural-validation
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PRODUCTION_ROUTE_MUTATION=forbidden
PRODUCTION_GUARD_REBIND=forbidden
DOWNSTREAM_COMMIT=forbidden
PERFORMANCE_PROMOTION=forbidden
PREBAKED_RUNTIME_EVIDENCE=forbidden
```

R7-R2D introduces a kernel-only shadow candidate in which one workgroup executes four query heads sharing one KV head. Immutable RGBA4 K/V texture tiles are loaded once into workgroup memory and consumed by all four query heads. This revision validates structure and numerical correctness only. It does not promote a production texture route or claim performance superiority.

## 1. Parent authority

The promoted R7-R2C artifact and manifest must seal buffer-Q plus immutable texture-KV binding, query-head to KV-head mapping, logical-page to physical-page mapping, exact integer `textureLoad`, raw K/V parity, attention parity, page-generation lock, payload-readback zero, shadow isolation, and unchanged production path.

R7-R2D must not create another Device, Queue, dispatcher, route authority, output ABI authority, texture residency owner, page-table owner, or GQA mapping authority.

## 2. GQA4 meaning

`GQA4` means four query heads per cluster sharing one KV head. It does not mean that the model has four KV heads.

```text
q_heads=32
kv_heads=4
query_heads_per_kv=8
query_heads_per_cluster=4
clusters_per_kv_head=2
```

Required:

```text
query_heads_per_kv % query_heads_per_cluster=0
query_heads_per_cluster=4
clusters_per_kv_head=2
```

## 3. Revisions

```text
backend_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
model_core_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
active_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
active_route_policy_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
texture_residency_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
hybrid_texture_binding_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
gqa4_cluster_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D
cli_contract_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D
```

Cross-component revision equality is forbidden.

## 4. Dispatch and subgroup topology

```text
dispatch.x=seq_q
dispatch.y=kv_head_count
dispatch.z=clusters_per_kv_head
workgroup_size=(32,4,1)
workgroup_invocations=128
```

Coordinate authority:

```text
q_position=workgroup_id.x
kv_head=workgroup_id.y
cluster_index=workgroup_id.z
query_head_base=kv_head*query_heads_per_kv+cluster_index*4
query_head=query_head_base+local_invocation_id.y
```

Canonical clusters:

```text
KV0: Q0..3, Q4..7
KV1: Q8..11, Q12..15
KV2: Q16..19, Q20..23
KV3: Q24..27, Q28..31
```

The adapter must expose subgroup size 32. Four subgroups map exactly to four query-head lanes:

```text
subgroup_size=32
subgroup_count=4
subgroup_id=local_invocation_id.y
subgroup_invocation_id=local_invocation_id.x
```

This mapping must be verified by an executed compact GPU topology probe. It must not be inferred from the workgroup declaration. Mismatch causes HOLD without scalar fallback.

## 5. Tile and shared-memory layout

```text
token_tile_size=32
head_dim=64
dimension_groups=16
page_tokens=128
tiles_per_page=4
```

Canonical workgroup storage:

```text
shared_q=4*16 vec4<f32>=1024 bytes
shared_kv_tile=32*16 vec4<f32>=8192 bytes
shared_tile_weight=4*32 f32=512 bytes
shared reduction state=64 bytes
shared physical-page table=48 bytes
declared total=9840 bytes
hard budget=12288 bytes
```

K and V must time-share one `shared_kv_tile`. Simultaneous full-size K and V arrays are forbidden. Runtime must verify that declared bytes fit both the fixed budget and the device limit. Silent reduced-tile fallback is forbidden.

## 6. Shared K/V population and accounting

For one cluster tile:

```text
physical K loads=active_tokens*dimension_groups
physical V loads=active_tokens*dimension_groups
logical K reads=physical K loads*4
logical V reads=physical V loads*4
K reuse factor=4
V reuse factor=4
```

For a full tile:

```text
K textureLoad count=512 vec4
V textureLoad count=512 vec4
naive four-head count=2048 vec4
```

Required zero counters:

```text
query_head_specific_k_texture_load_count
query_head_specific_v_texture_load_count
shared_k_multi_writer_count
shared_v_multi_writer_count
shared_entry_unowned_count
shared_overwrite_before_consume_count
```

One physical-page LUT lookup is allowed per cluster tile. Query heads must not perform independent page-table lookups.

K/V payload access remains exact integer `textureLoad` with mip zero. Samplers, normalized coordinates, filtering, nonzero mip levels, sRGB formats, and `textureSample` are forbidden.

## 7. Q, score, softmax, and V phases

Q remains a same-device storage buffer. One cluster loads exactly 64 Q vec4 values.

Each subgroup lane owns one token for one query head and computes the 64-dimensional score in ascending scalar FMA order. Q identity, shared K identity, per-token score, causal visibility, and tile maximum require bitwise identity with the R7-R2C reference.

Causal visibility:

```text
visible_kv_count=seq_kv-seq_q+query_position+1
```

Each subgroup independently performs:

```text
tile_max=subgroupMax(score)
tile_sum=subgroupAdd(exp(score-tile_max))
```

Running denominator state:

```text
Mnew=max(M,Mt)
previous_scale=exp(M-Mnew)
tile_scale=exp(Mt-Mnew)
Lnew=L*previous_scale+Lt*tile_scale
```

After K consumption, the same shared allocation is repopulated from V texture. One invocation owns one output vec4. Output multi-writer, unowned output, out-of-range write, and candidate-kernel global atomics are forbidden.

## 8. Barrier contract

All workgroup barriers must be in uniform control flow. Required synchronization covers initial Q/page publication, K population, K consumer completion, probability publication, V population, and V consumer completion.

Forbidden:

```text
divergent barrier
lane-local return before barrier
causal branch around barrier
shared overwrite before all consumers finish
```

## 9. Reference and numerical policy

Reference:

```text
R7-R2C operation-order-preserving buffer K/V attention
```

Candidate:

```text
buffer Q
immutable texture K/V
phase-reused shared KV tile
four-query-head cluster execution
subgroup tile reductions
online tiled denominator
```

Bitwise exact:

```text
score
tile maximum
```

Fixed denominator envelope:

```text
max ULP <= 16
max relative error <= 2.0e-6
non-finite count=0
```

Fixed probability envelope:

```text
max absolute error <= 2.0e-6
max relative error <= 2.0e-5
mean absolute error <= 2.0e-7
non-finite count=0
```

Fixed output envelope:

```text
max absolute error <= 5.0e-5
max relative error <= 5.0e-4 when abs(reference)>=1.0e-4
mean absolute error <= 5.0e-6
root mean square error <= 1.0e-5
non-finite count=0
```

Tolerance widening after observing results, vendor-specific silent tolerance, sample filtering, NaN removal, and outlier deletion are forbidden.

## 10. Validation matrix

```text
batch=1
q_heads=32
kv_heads=4
head_dim=64
page_tokens=128

seq_q/seq_kv:
1/128
2/256
8/384
```

All eight clusters and all query positions must execute. Boundary coverage includes tokens 0, 1, 30, 31, 32, 33, 126, 127, 128, 129, 254, 255, 256, 257, 382, and 383. For `seq_q=8, seq_kv=384`, visible counts 377 through 384 must all be validated.

## 11. Readback and isolation

Allowed CPU readback:

```text
compact subgroup topology decision
compact numerical decision
aggregate counters
first-fault index
fixed error maxima and aggregates
```

Forbidden CPU readback:

```text
Q tensor
K tensor
V tensor
score tensor
probability tensor
output tensor
shared-memory dump
```

Allowed consumers are the GQA4 shadow kernel, topology probe, numerical comparator, and fault-injection validation path. Production attention, guard, O-projection, residual, decode output, route probes, and performance-route activation are forbidden. Candidate output commit and production consumer counts must be zero.

## 12. CLI extension

```text
--gqa4-cluster-policy four-query-heads-one-kv-head-v1
--gqa4-workgroup-policy subgroup32-x4-v1
--gqa4-workgroup-size 128
--gqa4-subgroup-size 32
--gqa4-subgroups-per-workgroup 4
--gqa4-query-heads-per-cluster 4
--gqa4-token-tile-size 32
--gqa4-shared-kv-policy single-population-four-consumers-v1
--gqa4-shared-memory-policy phase-reused-k-then-v-v1
--gqa4-softmax-policy subgroup-online-tiled-v1
--gqa4-reference-policy r2c-hybrid-single-query-head-v1
--gqa4-numerical-envelope-policy fixed-f32-cluster-v1
--gqa4-validation-surface kernel-only-shadow-v1
--gqa4-causal-tail-policy partial-visible-tile-mask-v1
--gqa4-output-policy dedicated-shadow-cluster-output-v1
--gqa4-operation-accounting-policy logical-physical-separated-v1
```

Required booleans:

```text
--require-gqa4-cluster-width-exact true
--require-gqa4-subgroup-size-exact true
--require-gqa4-subgroup-head-map-exact true
--require-gqa4-query-head-coverage-exact true
--require-gqa4-cross-kv-cluster-zero true
--require-gqa4-shared-k-load-reuse-four true
--require-gqa4-shared-v-load-reuse-four true
--require-gqa4-query-head-specific-k-load-zero true
--require-gqa4-query-head-specific-v-load-zero true
--require-gqa4-shared-memory-budget true
--require-gqa4-uniform-barriers true
--require-gqa4-global-atomic-zero true
--require-gqa4-integer-textureload true
--require-gqa4-kv-sampler-zero true
--require-gqa4-kv-filtering-zero true
--require-gqa4-kv-mipmap-zero true
--require-gqa4-score-bitwise-parity true
--require-gqa4-fixed-numerical-envelope true
--require-gqa4-non-finite-zero true
--require-gqa4-payload-readback-zero true
--require-gqa4-production-consumer-zero true
--require-gqa4-candidate-output-commit-zero true
--require-gqa4-active-route-unchanged true
--require-gqa4-first-fault-capture true
```

Unknown, duplicate, missing, token-adhered, silently defaulted, and last-write-wins keys remain forbidden.

## 13. Negative controls and Rust evidence

At least 120 executed controls are required, ten each for cluster ownership, subgroup topology, shared K tile, shared V tile, barrier safety, page/texture access, score/softmax, output, workgroup memory, readback/isolation, active path, and operation accounting.

Rust emits parent binding, cluster topology, subgroup topology, structural receipts, numerical receipts, workgroup-memory receipt, texture-fetch receipt, readback-zero receipt, shadow-isolation receipt, active-path snapshots, negative-control outcomes, CLI receipts, runtime artifact, local manifest, and verdict.

The code ZIP must not contain specs, scripts, manifests, artifacts, receipts, verdicts, runtime JSON, PowerShell, batch files, or run-command files.

## 14. PASS

```text
R7-R2C parent binding pass
cluster width=4
clusters per KV head=2
query-head coverage exact
workgroup size=128
subgroup size=32
subgroup count=4
subgroup-to-head mapping exact
workgroup storage within fixed budget
K reuse factor=4
V reuse factor=4
query-head-specific K/V loads=0
cross-KV clusters=0
duplicate or missing query heads=0
barrier divergence=0
candidate global atomics=0
score bit mismatches=0
tile-max bit mismatches=0
denominator, probability and output envelopes pass
non-finite count=0
payload readback count=0
candidate output commit count=0
production consumer count=0
active production path unchanged
all negative controls pass
Rust artifact and manifest emitted
```

Success verdict:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2D_RGBA_TEXTURE_GQA4_PARALLEL_CLUSTER_KERNEL_NUMERICAL_AND_STRUCTURAL_VALIDATION_SEALED
```

Representative HOLD outcomes:

```text
HOLD_..._R7_R2D_GQA4_CLUSTER_TOPOLOGY_INVALID
HOLD_..._R7_R2D_SUBGROUP32_FOUR_HEAD_MAPPING_INVALID
HOLD_..._R7_R2D_SHARED_KV_TILE_REUSE_INCOMPLETE
HOLD_..._R7_R2D_WORKGROUP_BARRIER_UNIFORMITY_INVALID
HOLD_..._R7_R2D_CLUSTER_SCORE_BITWISE_PARITY_INCOMPLETE
HOLD_..._R7_R2D_TILED_SOFTMAX_OR_OUTPUT_NUMERICAL_ENVELOPE_EXCEEDED
HOLD_..._R7_R2D_GQA4_CLUSTER_KERNEL_ESCAPED_INTO_PRODUCTION_PATH
```

## 15. Fail-closed, rollback, next revision

The gate must not silently fall back to scalar or single-head execution after subgroup or cluster failure, reload K/V per query head after shared-memory failure, widen numerical tolerances, remove NaN or outlier samples, perform CPU tensor parity, or commit candidate output to production.

Rollback removes the R7-R2D shader, topology probe, numerical comparator, shadow scratch, CLI extension, and R7-R2D evidence while preserving R7-R2B residency, R7-R2C hybrid binding and reference, and the active production buffer route.

Next revision:

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E
GQA4 Cluster Kernel Cost Decomposition /
Shared Texture-Load Reuse Performance Receipt /
Paired GPU Timestamp Atlas /
Kernel-Only Non-Inferiority and Candidate Eligibility Seal
```
