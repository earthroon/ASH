# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R13

## TensorCube Stage 8 Real Q·K Operand Binding / Runtime Tensor View Identity / Query-Head·KV-Head GQA Broadcast / Head·Token·Channel Address Bijection / Synthetic Fixture Production Non-Admission / Exact Stage7 Fallback / Generation 38→39→40 Seal

## Authority

```text
PARENT_STAGE=Stage7Active
PARENT_FEATURE=tensorcube-multi-tile-head-kv-block-dispatch-grid-v1
PARENT_MASK=0x000000000000007f
PARENT_GENERATION=38

STAGE=Stage8Active
FEATURE=tensorcube-real-qk-runtime-view-binding-v1
FEATURE_BIT=7
CHILD_MASK=0x00000000000000ff
PREPARED_GENERATION=39
COMMITTED_GENERATION=40

IMPLEMENTATION_REVISION=R2-R13-stage8-real-qk-runtime-view-binding-v1
CLI_EXTENSION_KEYS=142
CANONICAL_REGISTRY_KEYS=2016
CANONICAL_RESPONSE_FILE_LINES=4032
ATLAS_GROUPS=35
NEGATIVE_CONTROLS=900
CHILD_ARTIFACTS=40
CHILD_ARTIFACT_LIST_SHA256=fd7c3c8a2f7a92961e0ae47edb19a035499021d1df979ca3ec0a1b3625802314
```

R2-R13 activates exactly one feature beneath sealed Stage 7. It binds the Stage7 dispatch coordinates to strict live Q/K `RawWgpuBufferLease` views. Causal masking, softmax, V binding, KV writes, and production attention-route activation remain out of scope.

## Runtime-view SSOT

The existing strict live raw bridge is the only admissible operand seam. Every Q/K view binds:

```text
underlying buffer identity
byte offset and binding size
shape and canonical axis order
element type and bytes per element
selected batch and token bases
active raw-handle state and seam identity
device and queue lineage
view generation and source generation
provenance class
```

Canonical views:

```text
Q axis order=[batch, query_head, query_token, channel]
Q selected shape=[1,32,16,64]
Q index=(((batch*32+query_head)*Sq+query_token)*64+channel)

K axis order=[batch, kv_head, kv_token, channel]
K selected shape=[1,4,64,64]
K index=(((batch*4+kv_head)*Skv+kv_token)*64+channel)

element type=f32
bytes per element=4
channel stride=1
token stride=64
```

Transpose, gather, negative stride, inner padding, f16, bf16, quantized views, candidate-specific Q/K bakes, and readback-reupload paths are forbidden.

## Storage bijection and GQA broadcast

Q and K storage bijections are proved separately from the intended GQA sharing relationship.

```text
Q selected scalars=1*32*16*64=32768
Q selected bytes=131072
Q forward mappings=32768/32768
Q inverse mappings=32768/32768
Q unique addresses=32768/32768

K selected scalars=1*4*64*64=16384
K selected bytes=65536
K forward mappings=16384/16384
K inverse mappings=16384/16384
K unique addresses=16384/16384

kv_head_id=query_head_id/8
query-head mappings=32/32
KV groups=4/4
heads per group=8/8
```

K broadcast is an intentional 8:1 mapping and is not mislabeled as a storage-address bijection.

## Stage7 coordinate inheritance

```text
workgroup_id.x=kv_block_id
workgroup_id.y=query_head_id
workgroup_id.z=quadrant_id
kv_head_id=query_head_id/8

grid=4x32x4
dispatch calls=1
workgroups=512
logical tiles=128
```

Candidate Q coordinate:

```text
Q[selected_batch, query_head_id, q_token_base+row, channel]
```

Candidate K coordinate:

```text
K[selected_batch, query_head_id/8, kv_token_base+kv_block_id*16+column, channel]
```

Quadrant identity affects output ownership only and may not alter Q/K addresses.

## Alias and movement boundary

Q/K may use different buffers or disjoint ranges of one allocation. Overlapping Q/K ranges are HOLD. Q/K alias with candidate output, status, or coverage surfaces is forbidden.

```text
Q copy=0
K copy=0
Q/K repack=0
Q/K bridge host upload=0
host materialization=0
payload readback=0
payload buffer map=0
cross-device copy=0
KV writes=0
```

The zero-copy claim is limited to the strict live operand-adoption boundary.

## Synthetic fixture production non-admission

```text
RuntimeProjection:
  validation_only=false
  production_admissible=true

ValidationFixture:
  validation_only=true
  production_admissible=false
  candidate publication=0
  pointer write=0
  feature-mask write=0
```

Correct numerical output cannot promote a ValidationFixture. Missing, forged, or substituted provenance is terminal HOLD.

The implementation harness creates deterministic validation tensors and then adopts them only through the existing strict live raw-buffer bridge. This proves the runtime-view seam, byte-range identity, GQA mapping, and same-device candidate/reference execution. It does not claim that the complete model Q/K projection call graph is already promoted.

## Candidate and reference

Candidate uses the inherited Stage7 `4x32x4` grid and Stage6 ordered eight-panel f32 arithmetic. The GPU reference reads the exact same Q/K buffers, offsets, and ranges using a direct-scalar schedule. CPU-only, host-copied, repacked, fixture-substituted, f64, or tolerance-based oracles are forbidden.

Parity is bit-exact.

## Compact decision

Exactly one 64-byte readback contains sixteen measured u32 counters:

```text
output mismatch
non-finite
Q view identity mismatch
K view identity mismatch
Q address mapping mismatch
K address mapping mismatch
Q bounds mismatch
K bounds mismatch
GQA broadcast mismatch
head-token-channel coordinate mismatch
Q/K overlap or alias
view/source generation mismatch
device/queue lineage mismatch
synthetic fixture production admission
hidden copy/repack/host movement
Stage7 grid inheritance mismatch
```

PASS requires every counter to be zero. Atlas groups, child artifacts, runtime artifact, and manifest serialize the measured runtime values. Literal zero, literal `all_zero=true`, and literal PASS evidence are forbidden.

## Exact fallback and pointer

```text
Stage8 -> Stage7 -> Stage6 -> Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required direct drill:

```text
Stage7 fallback tiles=128/128
Stage7 fallback workgroups=512/512
Stage7 fallback scalars=32768/32768
direct lower fallbacks=0
```

Failure preserves the exact Stage7 pointer, feature mask `0x7f`, and generation 38. Stage8 publication uses a compare-and-swap transition `38→39→40`; post-CAS failure restores the exact parent pointer bytes.

## Evidence closure

```text
R2-R13 extension keys=142
canonical registry keys=2016
response-file key/value pairs=2016
response-file non-empty lines=4032
Atlas groups=35/35
negative controls=900/900
child artifacts=40/40
child artifact ordered suffix list exact
child artifact list SHA-256=fd7c3c8a2f7a92961e0ae47edb19a035499021d1df979ca3ec0a1b3625802314
```

Count-only child-artifact acceptance is forbidden. The expected count is derived from the canonical ordered suffix array.

## PASS token

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R13_TENSORCUBE_STAGE8_REAL_QK_RUNTIME_VIEW_BINDING_STAGE7_PARENT_QUERY_HEAD_KV_HEAD_GQA_BROADCAST_HEAD_TOKEN_CHANNEL_ADDRESS_BIJECTION_SYNTHETIC_FIXTURE_PRODUCTION_NON_ADMISSION_STAGE7_REFERENCE_PARITY_EXACT_FALLBACK_AND_GENERATION_38_39_40_SEALED
```

Any parent identity, view identity, shape, stride, range, address, GQA, provenance, alias, movement, parity, fallback, pointer, generation, Atlas, CLI, artifact-list, manifest, binary, shader, or negative-control mismatch is terminal HOLD.