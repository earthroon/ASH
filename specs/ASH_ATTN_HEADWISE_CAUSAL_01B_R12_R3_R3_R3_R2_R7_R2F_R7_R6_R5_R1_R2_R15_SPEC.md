# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R15

## TensorCube Stage 10 Per-Row Block Max·Sum Reduction / Finite Admitted-Score Domain / Subgroup Row Reduction / Masked-Lane Zero Contribution / All-Masked Block Non-Reduction / Block Statistics Final-Write-Once / Exact Stage9 Fallback / Generation 42→43→44 Seal

## Authority

```text
PARENT_PATCH=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R14
PARENT_BUILD_REVISION=R2-R14-R3-embedded-wgsl-rebuild-attestation-v1
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage9Active
PARENT_FEATURE=tensorcube-causal-valid-past-kv-block-mask-v1
PARENT_MASK=0x00000000000001ff
PARENT_GENERATION=42

STAGE=Stage10Active
STAGE_ID=tensorcube-stage-10-per-row-block-statistics-v1
FEATURE=tensorcube-per-row-block-max-exp-sum-reduction-v1
FEATURE_BIT=9
CHILD_MASK=0x00000000000003ff
PREPARED_GENERATION=43
COMMITTED_GENERATION=44

IMPLEMENTATION_REVISION=R2-R15-stage10-row-block-max-exp-sum-v1
CLI_EXTENSION_KEYS=200
CANONICAL_REGISTRY_KEYS=2400
CANONICAL_RESPONSE_FILE_LINES=4800
ATLAS_GROUPS=43
NEGATIVE_CONTROLS=1100
CHILD_ARTIFACTS=48
CHILD_ARTIFACT_LIST_SHA256=19393c76ca559efb8e6dcb866f7f0a5a250d1a75f45a72c55a95500b1621c2d4
DEFAULT_VERDICT=HOLD
```

R2-R15 activates exactly one capability beneath sealed Stage 9: block-local row maximum, shifted exponential sum, explicit validity/class metadata, and one terminal statistics-record write per row-block. Cross-KV-block merge, normalized probabilities, V binding, weighted-V accumulation, KV writes, and production-route activation remain outside this patch.

## Parent admission

The exact R2-R14 parent must prove:

```text
pass=true
stage=Stage9Active
feature_mask_after=0x01ff
past_length=48
valid_length=64
current_query_length=16
q_absolute_base=48
kv_absolute_base=0
logical_tiles=128/128
grid=4x32x4
workgroups=512/512
admitted_score_lanes=28928/28928
masked_score_lanes=3840/3840
full_row_blocks=1568/1568
partial_row_blocks=480/480
empty_row_blocks=0/0
inactive_row_blocks=0/0
all twenty Stage9 decision counters=0
bit_exact_parity=true
same_device=true
same_queue_lineage=true
KV writes=0
payload movement counters=0
compact decision=1 readback, 80 bytes
generations=40/41/42
Atlas groups=39/39
negative controls=1000/1000
child artifacts=44/44
```

R2-R15 binds the parent runtime artifact, local manifest, exact Stage9 pointer, Stage9 score/mask/class surfaces, sequence snapshot, Q/K view identity, candidate/oracle/verify shaders, embedded-shader receipt, device/queue digest, Atlas digest, CLI digest, artifact-list digest, and scientific terminal by SHA-256.

## State transition

```text
0x00000000000001ff -> 0x00000000000003ff
xor=0x0000000000000200
popcount(xor)=1
bits 0..8 retained
bit 9 added
bits >=10 zero

Stage9Active generation 42
-> Stage10Prepared generation 43
-> Stage10Active generation 44
```

The attention route remains `HeadwiseActive`.

## Stage9 metadata authority

Stage10 consumes the exact Stage9 score, 16-bit row-block mask, and row-block class surfaces. It may validate them but may not reconstruct admission from score values, `-infinity`, sequence lengths, block coordinates, or finiteness.

```text
Full     <-> popcount(mask)=16
Partial  <-> popcount(mask)=1..15
Empty    <-> popcount(mask)=0 and query row active
Inactive <-> query row inactive
```

Parent mask and class digests remain immutable through Stage10 execution.

## Geometry and row-block bijection

```text
query heads=32
KV blocks/query head=4
rows/tile=16
columns/row-block=16
score tiles=128
row-blocks=2048
score scalars=32768

tile_dispatch_id=query_head_id*4+kv_block_id
row_block_id=tile_dispatch_id*16+query_row
```

Required closure:

```text
forward mappings=2048/2048
inverse mappings=2048/2048
unique IDs=2048/2048
duplicate IDs=0
missing IDs=0
out-of-range IDs=0
```

## Statistics record

Exactly one 16-byte record is owned by every row-block:

```wgsl
struct RowBlockStatsRecord {
    row_max_bits: u32,
    row_exp_sum_bits: u32,
    admitted_count: u32,
    flags: u32,
}
```

```text
records=2048
bytes/record=16
total bytes=32768

flags bit 0=statistics_valid
flags bits 1..2=Stage9 class
flags bit 3=final_write_complete
flags bits 4..31=0

Full=0
Partial=1
Empty=2
Inactive=3
```

Valid Full/Partial records contain finite `row_max`, finite `row_exp_sum`, admitted count 1..16, and `1.0 <= row_exp_sum <= admitted_count`.

Invalid Empty/Inactive records are written once using:

```text
row_max_bits=0xff800000
row_exp_sum_bits=0x00000000
admitted_count=0
statistics_valid=0
```

Consumers must use validity and class flags rather than infer validity from numeric payloads.

## Candidate dispatch and subgroup ownership

```text
dispatch_workgroups(x=4,y=32,z=1)
dispatch calls=1
workgroups=128
workgroup size=32
subgroup size=32
subgroups/workgroup=1
row-pair iterations/workgroup=8
rows/workgroup=16
```

The subgroup is divided into two independent 16-lane segments:

```text
lanes 0..15  -> even row
lanes 16..31 -> odd row
column=subgroup_lane_id%16
```

Only shuffle distances `1,2,4,8` are admitted. Distance 16 or cross-half contamination is HOLD.

## Finite admitted-score domain

For an admitted lane:

```text
score payload read=1
score must be finite
score bits remain Stage9-identical
```

For a masked lane:

```text
score payload read=0
max identity=-infinity
exp evaluation=0
exp contribution=+0.0
admitted count contribution=0
```

Canonical counts:

```text
admitted score reads=28928/28928
masked score reads=0/3840
finite admitted scores=28928/28928
```

NaN, positive infinity, or negative infinity in an admitted lane is terminal HOLD.

## Deterministic maximum

The row maximum is reduced over admitted lanes only. The reduction carries `(value_bits, source_column)` and uses this tie rule:

```text
larger value wins
equal value -> lower source column wins
```

The exact tree is:

```text
distance 1 -> 2 -> 4 -> 8
```

This preserves deterministic source identity, including equal-comparison cases such as signed zero.

## Shifted exponential sum

For valid Full/Partial blocks:

```text
shifted=score-row_max
shifted<=0
exp_term=exp(shifted)
row_exp_sum=sum(exp_term)
```

The sum uses the exact binary tree `1 -> 2 -> 4 -> 8`. Candidate and GPU oracle use the same operand order and GPU `exp` implementation, enabling bit-exact comparison. Sequential left folds, unordered atomic sums, f64 oracles, CPU reductions, and tolerance-only parity are forbidden.

Masked lanes never load score payload and never evaluate `exp`.

## Empty and Inactive non-reduction

For Empty or Inactive blocks:

```text
score reads=0
max reductions=0
exp evaluations=0
sum reductions=0
admitted count=0
statistics_valid=false
```

A canonical invalid record is still written once to preserve complete fixed-size ownership. Empty and Inactive classes may not be collapsed.

Required fixtures include:

```text
future-window all-masked:
  valid records=0
  Empty records=2048
  score reads=0
  exp evaluations=0

single-token decode:
  valid records=128
  Inactive records=1920
  admitted reads=2048

partial current query:
  valid Partial records=320
  Empty records=960
  Inactive records=768
  admitted reads=1760
```

## Final-write-once

```text
lane 0 owns even-row record
lane 16 owns odd-row record
```

Each owner assembles the full private record and commits it once after reduction.

```text
record writes=2048/2048
unique owners=2048/2048
write count/record=1
duplicate writes=0
missing writes=0
out-of-range writes=0
cross-row alias=0
cross-tile alias=0
```

Field-by-field writes from multiple lanes and intermediate statistics publication are forbidden.

## Candidate and GPU oracle

Candidate and oracle consume identical Stage9 score/mask/class buffers, offsets, strides, sequence snapshot, and device/queue lineage.

Candidate uses subgroup32 segmented reduction. Oracle reproduces the exact finite checks, tie comparator, max tree, shifted-exp computation, sum tree, invalid-record canonicalization, and record layout. Comparison covers all 16 bytes of every record bit-exactly.

## Compact decision

One 96-byte readback contains twenty-four measured u32 counters:

```text
output-record mismatch
unexpected admitted non-finite
Stage9 mask identity mismatch
Stage9 class identity mismatch
row-block mapping mismatch
admitted-count mismatch
max-reduction mismatch
max-domain/tie-rule mismatch
shifted-exp domain mismatch
exp-sum mismatch
exp-sum domain mismatch
masked score-read attempt
masked contribution mismatch
Empty/Inactive reduction attempt
invalid-record sentinel mismatch
statistics validity/class mismatch
final-write count mismatch
duplicate statistics write
missing statistics write
output alias/out-of-range access
sequence-generation mismatch
device/queue-lineage mismatch
hidden host movement
Stage9 inheritance mismatch
```

PASS requires all values to be zero.

```text
compact decision readbacks=1
compact decision bytes=96
score/mask/class/statistics payload readbacks=0
payload buffer maps=0
host materializations=0
host uploads=0
cross-device copies=0
KV writes=0
```

Atlas, child artifacts, runtime artifact, and manifest serialize runtime-measured counter values. Literal zero or literal PASS evidence is forbidden.

## Embedded WGSL attestation

Candidate, oracle, and verify WGSL are compiled into `burn_webgpu_backend` using `include_str!`. The gate compares each disk shader SHA-256 with the corresponding compiled embedded-source SHA-256 before dispatch. A stale backend library is terminal HOLD. The verification runner performs a package-scoped clean of `burn_webgpu_backend` before rebuilding.

## Exact fallback

```text
Stage10 -> Stage9 -> Stage8 -> Stage7 -> Stage6 -> Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required direct drill:

```text
Stage9 fallback score tiles=128/128
Stage9 fallback workgroups=512/512
Stage9 fallback score scalars=32768/32768
Stage9 fallback row masks=2048/2048
Stage9 fallback row classes=2048/2048
direct lower fallbacks=0
```

Failure preserves the exact Stage9 pointer, mask `0x01ff`, generation 42, and immutable parent score/mask/class surfaces. Partial Stage10 statistics are never reusable after fallback.

## Atlas and artifact closure

Exactly 43 canonical Atlas groups are required, covering identity, parent binding, Stage9 surfaces, feature transition, row-block mapping, statistics layout, subgroup topology, finite domain, deterministic max, shifted-exp sum, masked exclusion, invalid-block handling, final-write ownership, candidate/oracle parity, device/queue, host movement, compact decision, fallback, generation pointer, negatives, artifacts, manifest, and verdict.

```text
Atlas groups=43/43
negative controls=1100/1100
R2-R15 extension keys=200
canonical registry keys=2400
response-file key/value pairs=2400
response-file non-empty lines=4800
child artifacts=48/48
ordered artifact suffixes exact
ordered-list SHA-256=19393c76ca559efb8e6dcb866f7f0a5a250d1a75f45a72c55a95500b1621c2d4
```

Count-only artifact acceptance is forbidden. The expected count derives from one canonical ordered suffix array.

## PASS

```text
parent R2-R14 PASS exact
route=HeadwiseActive
Stage9Active -> Stage10Active
mask 0x01ff -> 0x03ff
added bits=1/1
row-blocks=2048/2048
candidate grid=4x32x1
workgroups=128/128
row-pair iterations=1024/1024
full records=1568/1568
partial records=480/480
valid records=2048/2048
invalid records=0/0
admitted reads=28928/28928
masked reads=0/3840
finite admitted scores=28928/28928
exp evaluations=28928/28928
masked exp evaluations=0
statistics writes=2048/2048
statistics bytes=32768/32768
all twenty-four counters=0
bit-exact parity=true
same device=true
same queue lineage=true
KV writes=0
host movement counters=0
compact decision=1 readback, 96 bytes
Stage9 fallback surfaces exact
direct lower fallbacks=0
generations=42/43/44
Atlas groups=43/43
negative controls=1100/1100
child artifacts=48/48
manifest closure exact
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R15_TENSORCUBE_STAGE10_PER_ROW_BLOCK_MAX_SUM_REDUCTION_STAGE9_PARENT_FINITE_ADMITTED_SCORE_DOMAIN_SUBGROUP16_SEGMENTED_ROW_REDUCTION_MASKED_LANE_ZERO_CONTRIBUTION_ALL_MASKED_BLOCK_NON_REDUCTION_BLOCK_STATISTICS_FINAL_WRITE_ONCE_STAGE9_REFERENCE_PARITY_EXACT_FALLBACK_AND_GENERATION_42_43_44_SEALED
```

Any parent identity, mask/class authority, finite-domain, reduction-tree, tie-rule, shifted-exp, invalid-block, record ownership, parity, movement, fallback, pointer, generation, Atlas, CLI, artifact-list, manifest, binary, embedded-shader, or negative-control mismatch is terminal HOLD.