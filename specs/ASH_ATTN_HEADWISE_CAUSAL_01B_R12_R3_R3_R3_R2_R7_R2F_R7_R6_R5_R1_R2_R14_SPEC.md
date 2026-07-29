# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R14

## TensorCube Stage 9 Causal Sequence Boundary / Valid-Length·Past-Length Ownership / KV-Block Admission Mask / Masked-Lane Neutralization / All-Masked Row Exclusion / Exact Stage8 Fallback / Generation 40→41→42 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R13
PARENT_VERDICT=PASS
PARENT_STAGE=Stage8Active
PARENT_FEATURE=tensorcube-real-qk-runtime-view-binding-v1
PARENT_MASK=0x00000000000000ff
PARENT_GENERATION=40

STAGE=Stage9Active
STAGE_ID=tensorcube-stage-9-causal-sequence-boundary-v1
FEATURE=tensorcube-causal-valid-past-kv-block-mask-v1
FEATURE_BIT=8
CHILD_MASK=0x00000000000001ff
PREPARED_GENERATION=41
COMMITTED_GENERATION=42

IMPLEMENTATION_REVISION=R2-R14-stage9-causal-sequence-boundary-v1
CLI_EXTENSION_KEYS=184
CANONICAL_REGISTRY_KEYS=2200
CANONICAL_RESPONSE_FILE_LINES=4400
ATLAS_GROUPS=39
NEGATIVE_CONTROLS=1000
CHILD_ARTIFACTS=44
CHILD_ARTIFACT_LIST_SHA256=4e37b3756186641e56b40acb00ea051cef8cca91afcde1cbd4724590925b89ac
DEFAULT_VERDICT=HOLD
```

R2-R14 adds only the temporal admission boundary beneath sealed Stage 8 live Q/K binding. Softmax, V binding, KV writes, normalization, and production-route activation remain forbidden.

## 1. Sequence SSOT

The following values are separate authorities and may not be inferred from one another except through explicit checked relations:

```text
past_length
valid_length
current_query_length
q_storage_token_base
q_absolute_position_base
kv_storage_token_base
kv_absolute_position_base
```

Canonical gate scenario:

```text
past_length=48
current_query_length=16
valid_length=64
q_storage_token_base=0
q_absolute_position_base=48
kv_storage_token_base=0
kv_absolute_position_base=0
kv_window_span=64
```

Required relations:

```text
valid_length = past_length + current_query_length
1 <= current_query_length <= 16
q_absolute_position_base = past_length
```

Storage coordinates and absolute sequence positions are not interchangeable.

## 2. Lane admission

The only admissible predicate is:

```text
lane_admitted =
    query_row_active
    && key_in_storage_range
    && key_absolute_position < valid_length
    && key_absolute_position <= query_absolute_position
```

Diagonal admission is required. Replacing `<=` with `<` is terminal HOLD.

Stage7/8 coordinate inheritance remains:

```text
workgroup_id.x = kv_block_id
workgroup_id.y = query_head_id
workgroup_id.z = quadrant_id
kv_head_id = query_head_id / 8

grid=4×32×4
dispatch calls=1
workgroups=512
logical tiles=128
```

## 3. KV-block mask and classes

For each `(query_head, kv_block, query_row)`, Stage 9 creates one 16-bit mask. Bit `column` is one only when the corresponding score lane is admitted.

```text
Full      popcount=16
Partial   popcount=1..15
Empty     popcount=0 and query row active
Inactive  query row inactive
```

Empty and Inactive are distinct states. Downstream reduction must consume explicit Stage9 class/admission metadata and may not reconstruct it from score values.

Canonical scenario totals:

```text
active query rows=512
inactive query rows=0
admitted score lanes=28928
masked score lanes=3840
full row-blocks=1568
partial row-blocks=480
empty row-blocks=0
inactive row-blocks=0
```

## 4. Masked-lane neutralization

Canonical masked score:

```text
MASKED_SCORE_BITS=0xff800000
MASKED_SCORE_VALUE=-infinity
```

For a masked lane:

```text
score FMA=0
K payload read=0
score bits=0xff800000
```

For an inactive query row:

```text
Q payload read=0
K payload read=0
score FMA=0
row-block reduction admission=false
class=Inactive
```

Q/K payload reads must be control-flow dominated by the admission predicate. Unconditional loads followed by `select`, zero-score masks, minimum-finite sentinels, NaN sentinels, and positive infinity are forbidden.

The contract proves WGSL control-flow dominance and runtime counters; it does not claim ISA-level absence of speculative memory transactions.

## 5. All-masked exclusion

An active row-block with mask zero is `Empty` and is not admitted to downstream row reduction. A query row outside `current_query_length` is `Inactive`. These states may not be collapsed.

Negative-control families include:

```text
single-token decode: past=63, current=1, valid=64
future-window all-masked: past=0, current=16, valid=16, kv_absolute_base=16
partial current query: past=0, current=10, valid=10
strict-less-than diagonal rejection
load-before-admission rejection
masked sentinel mutation rejection
```

## 6. Candidate and oracle

Candidate and GPU oracle read the exact same strict live Q/K `RawWgpuBufferLease` ranges inherited from Stage 8.

Candidate:

```text
single 4×32×4 dispatch
per-lane admission before Q/K read
Stage8 ordered 8-panel × 8-FMA grouping for admitted scores
canonical -infinity for masked scores
GPU row-mask and row-class metadata
final write exactly once
```

Oracle:

```text
same Q/K buffers, offsets, shapes, and sequence metadata
direct-scalar GPU schedule
same ordered panel-local FMA grouping
same physical tile stride
```

Parity is bit-exact. CPU-only, f64, host-copied, repacked, and tolerance-based oracles are forbidden.

## 7. Compact decision

Exactly one 80-byte readback contains twenty measured u32 counters:

```text
output mismatch
unexpected non-finite
valid-length mismatch
past-length mismatch
query-row admission mismatch
key-validity mismatch
causal-predicate mismatch
block-mask mismatch
block-classification mismatch
full/partial/empty/inactive count mismatch
all-masked exclusion mismatch
masked sentinel mismatch
masked K-read attempt
inactive Q-read attempt
out-of-range operand read
sequence-generation mismatch
device/queue lineage mismatch
hidden copy/repack/host movement
Stage8 inheritance mismatch
final-write ownership mismatch
```

PASS requires all counters to be zero. Canonical masked `-infinity` is not counted as an unexpected non-finite value.

```text
compact decision readbacks=1
compact decision bytes=80
payload readbacks=0
payload buffer maps=0
host materializations=0
host uploads=0
cross-device copies=0
KV writes=0
```

Atlas receipts, child artifacts, runtime artifact, and manifest serialize measured counter values. Literal zero and literal PASS evidence are forbidden.

## 8. Exact fallback and pointer

```text
Stage9 -> Stage8 -> Stage7 -> Stage6 -> Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required direct fallback drill:

```text
Stage8 fallback tiles=128/128
Stage8 fallback workgroups=512/512
Stage8 fallback scalars=32768/32768
direct lower fallbacks=0
```

Failure preserves the exact Stage8 pointer, feature mask `0x00ff`, and generation 40. Stage9 output, mask, and class publication remain zero on failure.

Pointer publication uses compare-and-swap generation `40→41→42`; post-CAS failure restores the exact parent pointer bytes.

## 9. Evidence closure

```text
R2-R14 extension keys=184
canonical registry keys=2200
response-file key/value pairs=2200
response-file non-empty lines=4400
Atlas groups=39/39
negative controls=1000/1000
child artifacts=44/44
child artifact ordered suffix list exact
child artifact list SHA-256=4e37b3756186641e56b40acb00ea051cef8cca91afcde1cbd4724590925b89ac
```

Count-only artifact acceptance is forbidden. Expected child count is derived from one canonical ordered suffix array.

## 10. PASS token

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R14_TENSORCUBE_STAGE9_CAUSAL_SEQUENCE_BOUNDARY_STAGE8_PARENT_VALID_LENGTH_PAST_LENGTH_OWNERSHIP_KV_BLOCK_ADMISSION_MASK_MASKED_LANE_NEGATIVE_INFINITY_NEUTRALIZATION_ALL_MASKED_ROW_EXCLUSION_STAGE8_REFERENCE_PARITY_EXACT_FALLBACK_AND_GENERATION_40_41_42_SEALED
```

Any parent identity, sequence authority, storage/absolute coordinate, causal predicate, block mask, class, sentinel, read exclusion, all-masked exclusion, parity, device, movement, fallback, pointer, generation, Atlas, CLI, artifact-list, manifest, binary, shader, or negative-control mismatch is terminal HOLD.