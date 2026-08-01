# ASH-ATTN-INTERCONNECT-W5

## Texture06 Live Chunk Descriptor Adoption /
## Q Raw Buffer·K RGBA32F Texture Mixed Binding /
## TensorCube Stage10 Live Shadow Dispatch /
## Dynamic Query Tile·KV Chunk Geometry /
## Global-Position Causal Mask /
## GQA Query-to-KV Head Mapping /
## Chunk-Local Row Max·Shifted Exp-Sum /
## Queue-Ordered Upload·Consume Dependency /
## Submission-Fenced Consumer Owner-Zero /
## Raw-K Oracle GPU Parity /
## No Texture-to-Buffer Rehydration /
## No V·No Stage11·No Stage12 /
## Headwise FullActive Output Authority Preservation /
## No Attention Output Mutation Seal

> Status: implementation target rev.1
> Parent: `ASH-ATTN-INTERCONNECT-W4` physical PASS
> Build revision: `W5-live-q-buffer-k-texture-stage10-shadow-r1`
> Production output authority: `HeadwiseFullActive`

---

## 0. Objective

W5 consumes the live Q/K provenance and Texture-06 completed K chunk produced under W4 and opens the first real TensorCube Stage10 shadow dispatch.

```text
Headwise Q RawWgpuBufferLease
+ Texture-06 completed K rgba32float D2Array chunk
-> TensorCube Stage10 candidate
-> chunk-local row max / shifted exp-sum / admitted count
-> canonical raw-K oracle
-> GPU compact parity receipt
```

W5 does not compute the final attention context and does not mutate the production route.

---

## 1. Fixed kernel profile

```text
query_heads       32
kv_heads           4
gqa_group_size     8
head_dim           64
query_tile_rows    16
kv_block_columns   16
subgroup_size      32
```

Dynamic dimensions:

```text
q_seq
q_tile_index
active_query_rows
chunk_token_start
chunk_token_count
kv_block_count
absolute q/k positions
```

Unsupported fixed geometry fails closed.

---

## 2. Input authority

W5 accepts only W4-sealed live inputs.

```text
Q source     RawWgpuBufferLease / RawBorrowed / read-only
K candidate Texture-06 rgba32float D2Array slot
K oracle    canonical RawWgpuBufferLease / read-only
V source     not bound
```

Required provenance:

```text
model instance and epoch
layer index
session and decode step
source KV generation
partition generation and digest
device identity
queue lineage
causal snapshot
W4 invocation identity digest
```

Any mixed provenance is rejected.

---

## 3. K texture layout

```text
format        rgba32float
view          D2Array
x             head_dim / 4
y             chunk-local token
array layer   kv head
component     head_dim mod 4
```

Candidate shader reads K with `textureLoad`. The following path is forbidden:

```text
K texture -> copy_texture_to_buffer -> temporary K buffer -> TensorCube
```

---

## 4. Stage10 candidate ABI

For each query row, query head, and 16-column KV block, Stage10 emits one 16-byte record:

```text
word 0  row-local max score bits
word 1  shifted exp-sum bits
word 2  admitted causal element count
word 3  flags
```

The candidate computes:

```text
score = dot(Q, K) * scale
causal admission = absolute_key_position <= absolute_query_position
local_max = max(admitted scores)
local_exp_sum = sum(exp(score - local_max))
```

Masked lanes contribute neither max nor exp-sum.

---

## 5. Raw-K oracle

The oracle consumes the same Q lease and canonical K raw lease. It must not read the candidate texture through a rehydration buffer.

Candidate and oracle share:

```text
query tile geometry
chunk geometry
GQA mapping
absolute position mapping
causal mask
scale
statistics ABI
```

GPU verification compares all statistics records and reads back only a compact status buffer.

```text
statistics payload readback count  0
compact readback count             1 per submission group
```

---

## 6. Queue ordering and lifetime

W4 upload and W5 candidate/oracle/compare commands are encoded in queue order under the same submission lifetime.

```text
K upload
-> candidate texture read
-> raw-K oracle read
-> GPU compare
-> submission completion
-> W5 consumer owner-zero
-> W4 slot retirement selection
-> slot owner-zero
-> Free
```

The slot cannot return to `Free` while a Stage10 consumer owner remains.

`submission_serial` is local ordering evidence. Physical completion requires callback or equivalent submission completion evidence.

---

## 7. GQA mapping

```text
kv_head = query_head / gqa_group_size
```

Required:

```text
query_heads % kv_heads == 0
gqa_group_size == 8
query_head < 32
kv_head < 4
```

Any mapping outside the fixed v1 profile fails closed.

---

## 8. Causal position authority

Causal admission uses absolute positions, not chunk-local indices.

```text
query_abs = q_absolute_position_base + q_token
key_abs   = kv_absolute_position_base + chunk_token_start + local_token
admit     = key_abs <= query_abs
```

Capacity tail and tokens outside committed coverage are never admitted.

---

## 9. Authority preservation

Required counters:

```text
TensorCube Stage10 candidate dispatch  > 0
TensorCube Stage10 oracle dispatch     > 0
TensorCube compare dispatch            > 0
TensorCube Stage11 dispatch            0
TensorCube Stage12 dispatch            0
TensorCube output commit               0
attention output mutation              0
production route mutation              0
V read                                 0
texture-to-buffer rehydration          0
```

The production writer remains Headwise FullActive.

---

## 10. Runtime artifact wave map

Artifacts use the Atlas Parallel Streaming Wave Map builder rather than one giant `json!` tree.

Suggested waves:

```text
Wave 0  identity / geometry / policy
Wave 1  parent and authority provenance
Wave 2  pipeline and shader identity
Wave 3  chunk statistics parity receipts
Wave 4  submission and owner-zero receipts
Wave 5  zero-authority counters and PASS closure
```

Merge order:

```text
wave ordinal -> lane ordinal -> lexical key
```

Duplicate keys fail closed.

---

## 11. Negative controls

```text
wrong W4 identity
wrong model/layer/session/step
stale partition generation
non-RawBorrowed Q or K
wrong texture format or view
chunk outside committed coverage
wrong GQA profile
wrong subgroup size
candidate/oracle record mismatch
non-finite admitted result
zero write or duplicate write
texture-to-buffer copy
V binding
Stage11 or Stage12 dispatch
TensorCube output commit
slot reuse before consumer owner-zero
production authority mutation
```

---

## 12. Verification gate

The verification gate checks:

```text
build revision and parent artifact admission
fixed profile closure
CLI key closure
mixed Q-buffer/K-texture binding presence
raw-K oracle presence
GPU compact verifier presence
no rehydration call path
no V/Stage11/Stage12/output writer path
artifact wave-map deterministic merge
```

---

## 13. Physical gate

The physical gate must observe:

```text
native WGPU bootstrap
subgroup size exactly 32
live W4 Q/K provenance
Texture-06 K chunk upload
candidate textureLoad dispatch
raw-K oracle dispatch
GPU compact parity PASS
submission completion
consumer owner-zero
Headwise authority unchanged
```

---

## 14. Completion definition

W5 is complete only when real W4 live Q and Texture-06 K chunks execute TensorCube Stage10 shadow dispatch with exact candidate/oracle statistics parity, while V consumption, Stage11, Stage12, context commit, output mutation, and route mutation remain zero.

## PASS token

```text
PASS_ASH_ATTN_INTERCONNECT_W5_TEXTURE06_LIVE_CHUNK_DESCRIPTOR_Q_RAW_BUFFER_K_RGBA32F_TEXTURE_MIXED_BINDING_TENSORCUBE_STAGE10_LIVE_SHADOW_DYNAMIC_QUERY_TILE_KV_CHUNK_GEOMETRY_CAUSAL_MASK_GQA_MAPPING_CHUNK_LOCAL_MAX_EXP_SUM_QUEUE_ORDERED_DEPENDENCY_SUBMISSION_FENCED_CONSUMER_NO_TEXTURE_TO_BUFFER_REHYDRATION_NO_V_NO_STAGE11_NO_STAGE12_HEADWISE_FULLACTIVE_OUTPUT_AUTHORITY_NO_OUTPUT_MUTATION_SEALED
```

## W6 handoff

W5 hands W6 device-local chunk statistics in canonical chunk order:

```text
partition generation
query tile identity
chunk token range
candidate statistics buffer
exact coverage digest
submission and consumer lifetime receipt
```

W6 may open cross-chunk online softmax merge, but W5 grants no Stage11 authority itself.
