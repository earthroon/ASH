# ASH-ATTN-INTERCONNECT-W1 명세

## Runtime Shape Authority /
## Fixed Kernel Profile /
## Dynamic Query-KV Geometry /
## q_seq=1 Incremental Admission /
## Model Spec-Runtime Tensor Dimension Reconciliation Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W1`  
> Build revision: `W1-runtime-shape-authority-fixed-profile-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W0-R2` PASS  
> Parent binding: Headwise output authority + TensorCube `ShadowObserverOnly`  
> production attention output authority: `Headwise` 유지  
> TensorCube live Q/K dispatch: 아직 금지  
> TensorCube stage pointer mutation: 금지  
> 후속 패치: `W2 Lease Provenance / Generation Domain Separation`

---

# 0. 목적과 패치 경계

W0는 Headwise와 TensorCube Stage10을 동일 모델 인스턴스에 결속했지만, TensorCube Stage8-10의 host path는 아직 fixture geometry에 묶여 있다.

현재 확인된 고정 가정:

```text
Q shape                     [1, 32, 16, 64]
K shape                     [1, 4, 64, 64]
query heads                 32
KV heads                     4
GQA group size               8
query rows/tile             16
KV tokens/window            64
KV blocks/window             4
head dimension              64
```

W1은 이 가운데 커널의 구조적 profile과 런타임 외부 geometry를 분리한다.

```text
고정 kernel profile
  rows_per_query_tile       16
  columns_per_kv_block      16
  subgroup_size             32
  head_dim                  64
  panel_width                8
  panel_count                8
  quadrants                  4
  row_pair_iterations        8
  stats_record_bytes        16

동적 outer geometry
  batch
  query_heads
  kv_heads
  gqa_group_size
  q_seq
  kv_seq
  q_tile_count
  kv_block_count
  selected_batch
  q_token_base
  active_query_rows
  q_absolute_position_base
  kv_absolute_position_base
```

W1의 핵심 산출은 계산 결과가 아니라 다음 두 계약이다.

```text
1. AttentionRuntimeShapeAuthoritySnapshot
2. TensorCubeStage10DispatchPlan
```

W1 PASS가 뜻하는 것:

```text
결속된 ModelSpec의 attention geometry와 런타임 Q/K/V tensor dimensions를
하나의 fail-closed shape authority로 조정할 수 있다.

현재 16x16-subgroup32-head_dim64 profile에서
q_seq=1 incremental geometry와 dynamic kv_seq geometry를
정확한 dispatch plan으로 변환할 수 있다.
```

W1 PASS가 뜻하지 않는 것:

```text
실제 live Q/K RawWgpuBufferLease를 TensorCube가 소비했다.
TensorCube Stage10이 live decode hot path에서 dispatch됐다.
TensorCube가 V를 읽었다.
TensorCube가 attention context를 생성했다.
Headwise와 TensorCube의 수치 parity가 통과했다.
TensorCube output authority가 생겼다.
```

---

# 1. Parent SSOT

W1은 W0-R2의 Rust 산출물을 부모로 요구한다.

필수 부모 상태:

```text
W0 runtime artifact pass                      true
W0 local manifest pass                        true
model_instance_id                             exact
model_instance_binding_digest                 exact
headwise_authority                            verified_hold_active_reference
output_authority                              headwise
tensorcube_role                               shadow_observer_only
TensorCube active stage                       Stage10Active
TensorCube feature mask                       0x00000000000003ff
TensorCube generation                         44
route_mutation_count                          0
stage_mutation_count                          0
input_artifact_mutation_count                 0
negative_controls                             34/34
child_artifacts                               26/26
```

W1은 부모 receipt를 수정하거나 재발행하지 않는다.

```text
W0 binding write                              0
Headwise route write                          0
TensorCube stage pointer write                0
Headwise candidate promotion                  0
TensorCube dispatch                           0
```

---

# 2. Shape Authority의 귀속 위치

## 2.1 Static authority

Static attention geometry의 SSOT는 결속된 `NativeWgpuModel.spec`의 `ModelSpec.dimensions`다.

```rust
ModelSpec.dimensions.hidden_size
ModelSpec.dimensions.num_attention_heads
ModelSpec.dimensions.num_key_value_heads
ModelSpec.dimensions.head_dim
ModelSpec.dimensions.max_position_embeddings
ModelSpec.attention.attention_type
ModelSpec.attention.sliding_window
```

`VerifiedModelInstanceBinding`은 모델 인스턴스 정체성을 봉인하지만 attention dimensions를 직접 포함하지 않는다.

따라서 다음은 금지한다.

```text
instance_binding_digest에서 heads/head_dim을 역추론
CLI의 --query-heads 값을 production SSOT로 채택
TensorCube fixture constants를 model shape로 간주
Headwise runtime spec hint를 model dimensions보다 우선
Q/K tensor shape만 보고 model geometry를 새로 정의
```

## 2.2 Dynamic authority

호출별 dynamic geometry의 SSOT는 실제 런타임 tensor dimensions와 검증된 causal position snapshot이다.

```text
Q tensor dimensions
K tensor dimensions
V tensor dimensions, shape witness only
HeadwiseCausalPositionSnapshot
selected batch
```

권위 순서:

```text
VerifiedModelInstanceBinding
  -> bound ModelSpec attention geometry
  -> HeadwiseCausalPositionSnapshot
  -> actual Q/K/V dimensions
  -> TensorCube kernel profile admission
  -> TensorCubeStage10DispatchPlan
```

어느 단계도 이전 단계를 조용히 보정하지 않는다.

---

# 3. 신규 타입

## 3.1 AttentionModelShapeAuthoritySnapshot

Schema:

```text
ash.attn.interconnect.w1.model-shape-authority.v1
```

필드:

```text
schema
patch_id
build_revision
model_instance_id
model_instance_binding_digest
effective_runtime_binding_digest
model_spec_id
model_name
model_spec_version
hidden_size
num_layers
query_heads
kv_heads
gqa_group_size
head_dim
max_position_embeddings
attention_type
sliding_window
hidden_size_factorization_exact
kv_hidden_size
profile_candidate_id
model_attention_geometry_digest
snapshot_digest
pass
failures
```

Canonical 검증:

```text
query_heads > 0
kv_heads > 0
head_dim > 0
query_heads % kv_heads == 0
gqa_group_size == query_heads / kv_heads
hidden_size == query_heads * head_dim
kv_hidden_size == kv_heads * head_dim
max_position_embeddings > 0
model_instance identity exact
```

`kv_hidden_size`는 model dimension에서 유도한 값이며 별도 authority가 아니다.

## 3.2 TensorCubeFixedKernelProfile

Schema:

```text
ash.attn.interconnect.w1.fixed-kernel-profile.v1
```

Profile ID:

```text
tensorcube-stage10-16x16-sg32-hd64-v1
```

필드와 exact 값:

```text
rows_per_query_tile          16
columns_per_kv_block         16
subgroup_size_required       32
head_dim_required            64
panel_width                   8
panel_count                   8
quadrants                     4
row_pair_iterations           8
stats_record_bytes           16
score_element_bytes           4
masked_score_bits            0xff800000
profile_digest
```

Profile admission:

```text
runtime head_dim == model head_dim == 64
device subgroup size supports exact 32 path
storage buffer alignment valid
required dispatch dimensions within device limits
required buffer sizes within device limits
```

미지원 시:

```text
TensorCube shape admission = ShadowDisabledUnsupportedProfile
Headwise execution = unchanged
route mutation = 0
stage mutation = 0
error swallowed as successful TensorCube admission = 금지
```

## 3.3 RuntimeAttentionShapeObservation

Schema:

```text
ash.attn.interconnect.w1.runtime-shape-observation.v1
```

필드:

```text
model_instance_id
route_id
decode_session_id
position_epoch
selected_batch
q_shape[4]
k_shape[4]
v_shape[4]
q_dtype_bytes
k_dtype_bytes
v_dtype_bytes
q_layout
k_layout
v_layout
causal_snapshot_digest
observation_digest
```

Canonical layout:

```text
Q = [batch, query_heads, q_seq, head_dim]
K = [batch, kv_heads, kv_seq, head_dim]
V = [batch, kv_heads, kv_seq, head_dim]
```

W1에서 V는 shape reconciliation witness일 뿐 TensorCube binding 대상이 아니다.

## 3.4 AttentionRuntimeShapeReconciliationReceipt

Schema:

```text
ash.attn.interconnect.w1.shape-reconciliation.v1
```

필드:

```text
model_shape_authority_digest
runtime_observation_digest
kernel_profile_digest
model_instance_id
route_id
batch
query_heads
kv_heads
gqa_group_size
head_dim
q_seq
kv_seq
q_shape_matches_model
k_shape_matches_model
v_shape_matches_model
kv_shape_pair_exact
causal_shape_exact
max_position_domain_valid
kernel_profile_admitted
unsupported_reason
reconciliation_digest
pass
failures
```

## 3.5 TensorCubeStage10DispatchSpec

Schema:

```text
ash.attn.interconnect.w1.stage10-dispatch-spec.v1
```

한 `DispatchSpec`은 한 batch와 한 query 16-row tile을 나타낸다.

필드:

```text
model_instance_id
kernel_profile_id
route_id
selected_batch
batch_count
query_heads
kv_heads
gqa_group_size
head_dim
q_seq
kv_seq
q_tile_index
q_tile_count
q_token_base
active_query_rows
q_absolute_position_base
kv_token_base
kv_absolute_position_base
kv_block_count
logical_score_tiles
row_block_count
score_scalars
score_bytes_unaligned
score_tile_stride_bytes
statistics_records
statistics_bytes
stage9_grid_x
stage9_grid_y
stage9_grid_z
stage10_grid_x
stage10_grid_y
stage10_grid_z
dispatch_spec_digest
```

## 3.6 TensorCubeStage10DispatchPlan

Schema:

```text
ash.attn.interconnect.w1.stage10-dispatch-plan.v1
```

필드:

```text
model_instance_id
shape_reconciliation_digest
kernel_profile_digest
batch_count
q_tile_count_per_batch
kv_block_count
dispatch_spec_count
dispatch_specs
planner_only
live_qk_dispatch_performed        false
tensorcube_output_commit          false
headwise_output_authority         true
plan_digest
pass
failures
```

W1의 plan은 실행 계획이다. live Q/K buffer ownership이나 generation provenance는 W2 이후에 추가한다.

---

# 4. Model Spec와 runtime tensor dimension 조정

## 4.1 Model geometry

```text
model_q_heads = ModelSpec.dimensions.num_attention_heads
model_kv_heads = ModelSpec.dimensions.num_key_value_heads
model_head_dim = ModelSpec.dimensions.head_dim
model_hidden_size = ModelSpec.dimensions.hidden_size
model_gqa_group = model_q_heads / model_kv_heads
```

필수 등식:

```text
model_hidden_size == model_q_heads * model_head_dim
model_q_heads % model_kv_heads == 0
```

## 4.2 Runtime Q

```text
Q rank == 4
Q.batch > 0
Q.heads == model_q_heads
Q.q_seq > 0
Q.head_dim == model_head_dim
Q element width == 4 bytes
```

## 4.3 Runtime K/V

```text
K rank == 4
V rank == 4
K.batch == Q.batch
V.batch == Q.batch
K.heads == model_kv_heads
V.heads == model_kv_heads
K.kv_seq > 0
V.kv_seq == K.kv_seq
K.head_dim == model_head_dim
V.head_dim == model_head_dim
K element width == 4 bytes
V element width == 4 bytes
```

## 4.4 Causal snapshot

```text
snapshot.seq_q == Q.q_seq
snapshot.seq_kv == K.kv_seq
snapshot digest exact
snapshot route contract exact
snapshot q range is suffix-aligned in KV range
```

W1은 `past_length`, `valid_length`, `q_absolute_base`, `kv_absolute_base`를 CLI에서 독립적으로 받지 않는다. 기존 `valid_length`는 token count와 absolute end를 혼용할 수 있으므로 W1 ABI에서 분리한다.

유도:

```text
q_absolute_position_base = snapshot.q_position_base
kv_absolute_position_base = snapshot.kv_position_base
kv_valid_token_count = snapshot.seq_kv
kv_valid_end_exclusive = snapshot.kv_position_base + snapshot.seq_kv
past_token_count = snapshot.q_position_base - snapshot.kv_position_base
```

Suffix-aligned contract에서는 다음도 성립해야 한다.

```text
past_token_count == snapshot.seq_kv - snapshot.seq_q
```

Position 계산은 u64 checked arithmetic으로 수행하고, 현재 WGSL u32 ABI로 내릴 때 checked conversion을 통과해야 한다. snapshot validation이 실패하면 어떤 값도 유도하지 않는다.

## 4.5 Position domain

```text
q_end_exclusive = q_position_base + q_seq
kv_end_exclusive = kv_position_base + kv_seq
q_end_exclusive == kv_end_exclusive
kv_seq <= max_position_embeddings
```

`sliding_window > 0`이면서 물리 K lease가 full-domain이 아닌 ring/window layout이면 W1 profile은 admission하지 않는다. 해당 layout은 W2 provenance와 이후 KV residency 명세에서 별도 profile로 다룬다.

---

# 5. q_seq=1 Incremental Admission

`HeadwiseCausalRouteId::IncrementalDecode`의 canonical 조건:

```text
q_seq == 1
kv_seq >= 1
q_position_base == kv_position_base + kv_seq - 1
suffix_aligned == true
```

W1 dispatch derivation:

```text
q_tile_count               1
q_tile_index               0
q_token_base               0
active_query_rows          1
inactive_query_rows        15
kv_block_count             ceil_div(kv_seq, 16)
stage9 grid                [kv_block_count, query_heads, 4]
stage10 grid               [kv_block_count, query_heads, 1]
```

중요 경계:

```text
Q lease shape를 [B,H,16,D]로 위조 금지
Q payload에 15개 fake row append 금지
host repack/padding 금지
inactive row에서 Q read 금지
inactive row score는 MASKED_SCORE_BITS
inactive row class는 Inactive
inactive row Stage10 stats는 canonical invalid record
```

Canonical inactive record:

```text
row_max_bits               0xff800000
row_exp_sum_bits           0x00000000
admitted_count             0
statistics_valid           0
class                      Inactive
final_write_complete       1
```

q_seq=1에서 record 수 자체는 profile tile 구조를 유지한다.

```text
statistics_records = query_heads * kv_block_count * 16
active row-blocks = query_heads * kv_block_count
inactive row-blocks = query_heads * kv_block_count * 15
```

이 구조는 물리 tile 크기와 의미상 활성 query 길이를 섞지 않는다.

---

# 6. Dynamic Query Geometry

## 6.1 Query tile count

```text
q_tile_count = ceil_div(q_seq, 16)
```

각 tile:

```text
q_token_base = q_tile_index * 16
active_query_rows = min(16, q_seq - q_token_base)
q_absolute_position_base = snapshot.q_position_base + q_token_base
```

## 6.2 Multi-tile query

q_seq > 16은 여러 독립 `DispatchSpec`으로 분할한다.

예:

```text
q_seq 17
  tile 0: q_token_base 0,  active rows 16
  tile 1: q_token_base 16, active rows 1

q_seq 31
  tile 0: active rows 16
  tile 1: active rows 15

q_seq 32
  tile 0: active rows 16
  tile 1: active rows 16
```

W1은 tile 순서를 다음으로 고정한다.

```text
selected_batch ascending
q_tile_index ascending
```

unordered dispatch plan, tile deduplication, trailing tile omission은 금지한다.

## 6.3 Query bounds

각 tile의 모든 active row에 대해:

```text
q_token_base + row < q_seq
q_absolute_position_base + row < kv_end_exclusive
```

inactive row에서는 Q index를 생성하거나 Q buffer를 읽지 않는다.

---

# 7. Dynamic KV Geometry

## 7.1 KV block count

기존 fixture 상수 `KV_TOKENS=64`, `KV_BLOCKS=4`를 production geometry authority에서 제거한다.

```text
kv_block_count = ceil_div(kv_seq, 16)
```

예:

```text
kv_seq 1    -> 1 block
kv_seq 15   -> 1 block
kv_seq 16   -> 1 block
kv_seq 17   -> 2 blocks
kv_seq 63   -> 4 blocks
kv_seq 64   -> 4 blocks
kv_seq 65   -> 5 blocks
```

## 7.2 Tail block

마지막 KV block이 partial이면 Stage9 mask가 storage validity와 causal validity를 함께 소유한다.

```text
storage_token = kv_token_base + block * 16 + column
storage_valid = storage_token < kv_seq
position_valid = key_absolute_position < kv_valid_end_exclusive
causal_valid = key_absolute_position <= query_absolute_position
admitted = active_query_row && storage_valid && position_valid && causal_valid
```

다음은 금지한다.

```text
kv_seq를 다음 16배수로 물리 확장
K payload host padding
64-token window로 강제 절단
마지막 partial block을 Full로 분류
score == -inf에서 storage validity 역추론
```

## 7.3 Dispatch and allocation formulas

한 query tile 기준:

```text
logical_score_tiles = query_heads * kv_block_count
row_block_count = logical_score_tiles * 16
score_scalars = logical_score_tiles * 16 * 16
statistics_records = row_block_count
statistics_bytes = row_block_count * 16
```

Dispatch:

```text
Stage9 candidate
  dispatch_workgroups(kv_block_count, query_heads, 4)

Stage9 classify
  dispatch_workgroups(ceil_div(row_block_count, 64), 1, 1)

Stage10 candidate
  dispatch_workgroups(kv_block_count, query_heads, 1)

Stage10 oracle/verify
  dispatch_workgroups(ceil_div(row_block_count, 64), 1, 1)
```

모든 곱셈은 checked arithmetic을 사용한다.

```text
u32 overflow
usize overflow
u64 byte-size overflow
device max dispatch dimension overflow
device max storage binding overflow
```

중 하나라도 발생하면 TensorCube shape admission을 거부하고 Headwise를 유지한다.

---

# 8. Dynamic Head Geometry

Production authority는 현재 결속된 모델의 geometry를 사용한다.

Canonical current model profile gate:

```text
query_heads                32
kv_heads                    4
gqa_group_size              8
head_dim                   64
```

그러나 Rust planner는 다음 상수를 production shape로 하드코딩하면 안 된다.

```text
QUERY_HEADS=32
KV_HEADS=4
GQA_GROUP_SIZE=8
```

유도:

```text
query_heads = model shape authority.query_heads
kv_heads = model shape authority.kv_heads
gqa_group_size = query_heads / kv_heads
```

Validation-only alternate geometry fixtures:

```text
8 query heads / 2 KV heads / group 4 / head_dim 64
16 query heads / 4 KV heads / group 4 / head_dim 64
24 query heads / 6 KV heads / group 4 / head_dim 64
```

이 fixture들은 planner 범용성 검증용이며 production model authority로 승격되지 않는다.

필수:

```text
fixture provenance = ValidationFixture
production_admission_count = 0
model_instance binding replacement = 0
Headwise route mutation = 0
```

---

# 9. Stage8 Host Refactor

기존 `run_tensorcube_stage8_real_qk_binding_on_existing_device`의 shape authority를 fixture 상수에서 `TensorCubeStage10DispatchSpec`으로 이동한다.

기존 제거 대상:

```rust
const QUERY_HEADS: u32 = 32;
const KV_HEADS: u32 = 4;
const GQA_GROUP_SIZE: u32 = 8;
const Q_ROWS: u32 = 16;
const KV_TOKENS: u32 = 64;
const KV_BLOCKS: u32 = 4;
```

유지되는 structural profile constants:

```rust
const ROWS_PER_QUERY_TILE: u32 = 16;
const COLUMNS_PER_KV_BLOCK: u32 = 16;
const HEAD_DIM_PROFILE: u32 = 64;
const QUADRANTS: u32 = 4;
```

Stage8 Q/K identity 검증:

```text
shape rank exact
model heads exact
model head_dim exact
q_seq/kv_seq actual dimensions exact
bytes_per_element 4
RawBorrowed
BorrowedBuffer
buffer present
buffer offset alignment exact
len_elements == product(shape)
len_bytes == len_elements * 4
selected batch in range
active query window in range
all dynamic KV blocks in range by mask
```

W1에서는 generation domain을 재설계하지 않는다. 기존 generation fields는 보존하고 W2에서 타입 분리한다.

---

# 10. Stage9 WGSL Param Contract

## 10.1 Structural constants

WGSL에 명시적으로 남긴다.

```wgsl
const HEAD_DIM: u32 = 64u;
const ROWS_PER_QUERY_TILE: u32 = 16u;
const COLUMNS_PER_KV_BLOCK: u32 = 16u;
const PANEL_WIDTH: u32 = 8u;
const PANEL_COUNT: u32 = 8u;
const QUADRANTS: u32 = 4u;
```

## 10.2 Dynamic params

Stage9 candidate가 실제 사용하는 값만 uniform ABI에 둔다.

```text
output_tile_stride_f32
query_heads
kv_heads
gqa_group_size
kv_block_count
q_seq
kv_seq
q_token_base
kv_token_base
selected_batch
q_elements
k_elements
current_query_length
q_absolute_base
kv_absolute_base
kv_valid_end_exclusive
```

제거 대상:

```text
tile_count, shader에서 불필요하면 제거
head_dim, fixed profile constant와 중복
kv_window_span, 미사용
sequence_generation, shader 미사용
source_generation, shader 미사용
reserved
quadrants, fixed profile constant와 중복
```

host-only validation value를 WGSL uniform에 장식처럼 넣지 않는다.

## 10.3 Dynamic class counts

기존 Stage9 verifier의 literal count 검사는 제거한다.

```wgsl
full == 1568
partial == 480
empty == 0
inactive == 0
```

대신 geometry로부터 expected class를 각 row-block에서 계산하고, GPU expected counts와 actual class counts를 비교한다.

필수:

```text
q_seq=1에서 inactive count nonzero
kv_seq=1에서 partial/empty 분류 exact
kv_seq=17에서 tail block partial exact
literal canonical fixture count comparison 0
```

---

# 11. Stage10 WGSL Param Contract

현재 Stage10 candidate/oracle/verify가 공유하는 Params에는 shader별 미사용 필드가 섞여 있다.

W1은 shader별 최소 ABI로 분리한다.

## 11.1 Candidate params

```text
output_tile_stride_f32
query_heads
kv_block_count
subgroup_size_expected
```

Candidate structural constants:

```text
rows_per_query_tile = 16
columns_per_kv_block = 16
row_pair_iterations = 8
```

## 11.2 Oracle params

```text
output_tile_stride_f32
row_block_count
kv_block_count
```

## 11.3 Verify params

```text
output_tile_stride_f32
row_block_count
kv_block_count
kv_seq
kv_token_base
current_query_length
q_absolute_base
kv_absolute_base
kv_valid_end_exclusive
```

## 11.4 제거 대상

```text
tile_count, 사용하지 않는 shader ABI에서 제거
rows_per_tile
columns_per_row
past_length
sequence_generation
source_generation
reserved
query_heads, 사용하지 않는 shader ABI에서 제거
```

`subgroup_size_expected`는 candidate에서 실제 builtin subgroup size 검증에 사용하므로 유지한다.

---

# 12. q_seq=1 GPU 의미 보존

Stage9 candidate의 query row admission은 physical tile row가 아니라 semantic active row를 사용한다.

```text
query_row_active = row < current_query_length
```

Q read는 반드시 다음 guard 내부에만 존재한다.

```text
query_row_active
&& q_token_base + row < q_seq
&& key storage valid
&& causal valid
```

Stage10 candidate는 inactive row의 Stage9 class를 소비하고 reduction을 수행하지 않는다.

```text
Inactive row
  score payload read        0
  exp evaluation            0
  admitted count            0
  final invalid record      1회
```

q_seq=1 positive gate는 다음을 증명한다.

```text
active Q rows               query_heads
inactive Q rows             query_heads * 15
inactive Q read attempts    0
masked K read attempts      0
out-of-range Q/K access     0
final writes                row_block_count
missing/duplicate writes    0
```

---

# 13. Shape Matrix

## 13.1 Canonical positive matrix

Current model geometry:

```text
batch       1
heads       32/4
head_dim    64
```

Required q_seq:

```text
1, 2, 15, 16
```

Required kv_seq:

```text
1, 15, 16, 17, 63, 64, 65
```

Causal route가 성립하는 조합을 모두 실행한다.

```text
q_seq 1   with kv_seq 1,15,16,17,63,64,65       7 cases
q_seq 2   with kv_seq 15,16,17,63,64,65          6 cases
q_seq 15  with kv_seq 15,16,17,63,64,65          6 cases
q_seq 16  with kv_seq 16,17,63,64,65             5 cases
                                                      total 24
```

Route 구성:

```text
q_seq == 1                  IncrementalDecode
q_seq == kv_seq, q_seq > 1  FullPrefill
2 <= q_seq < kv_seq         ChunkedDecode
q_seq > kv_seq              positive matrix에서 금지
```

## 13.2 Query tiling extension matrix

```text
q_seq 17, 31, 32
kv_seq 32, 33, 65
```

Planner와 per-tile Stage9-10 parity를 검증한다.

## 13.3 Alternate validation-only head geometry

```text
8/2/64
16/4/64
24/6/64
```

최소 각 1건의 q_seq=1, kv_seq=17 planner case를 실행한다.

## 13.4 Batch extension matrix

```text
batch 2 / q_seq 1 / kv_seq 17 / selected_batch 0
batch 2 / q_seq 1 / kv_seq 17 / selected_batch 1
batch 2 / q_seq 16 / kv_seq 16 / selected_batch 0
batch 2 / q_seq 16 / kv_seq 16 / selected_batch 1
```

선택된 batch 외의 Q/K/V address를 읽지 않아야 한다.

## 13.5 Required total

```text
canonical dynamic cases             24
query tiling extension cases         9
alternate geometry cases             3
batch extension cases                4
minimum positive cases              40
```

모든 positive case에서:

```text
planner pass
Stage9 candidate-oracle parity exact
Stage10 candidate-oracle parity exact
compact counters all zero
host payload movement zero
route/stage mutation zero
```

---

# 14. Decision Counters

Schema:

```text
ash.attn.interconnect.w1.decision-counters.v1
```

Canonical 32 counters:

```text
model_instance_mismatch
model_shape_snapshot_digest_mismatch
model_hidden_size_factorization_mismatch
model_query_head_zero
model_kv_head_zero
model_gqa_divisibility_mismatch
model_head_dim_mismatch
runtime_q_rank_mismatch
runtime_k_rank_mismatch
runtime_v_rank_mismatch
runtime_batch_mismatch
runtime_query_head_mismatch
runtime_kv_head_mismatch
runtime_head_dim_mismatch
runtime_kv_sequence_mismatch
runtime_empty_query
runtime_empty_kv
causal_snapshot_digest_mismatch
causal_snapshot_shape_mismatch
causal_route_mismatch
position_domain_overflow
max_position_domain_mismatch
kernel_profile_mismatch
subgroup_size_mismatch
query_tile_plan_mismatch
kv_block_plan_mismatch
dispatch_dimension_overflow
buffer_size_overflow
fixture_production_admission
route_mutation_detected
stage_mutation_detected
output_authority_mutation_detected
```

PASS 조건은 전부 0이다.

첫 nonzero counter 이름, case ID, model shape, runtime shape, causal snapshot을 함께 출력한다.

---

# 15. Negative Controls

최소 48건을 실제 실행한다.

## 15.1 Model authority

```text
01 model instance id mismatch
02 model binding digest mismatch
03 effective runtime binding mismatch
04 model q_heads zero
05 model kv_heads zero
06 q_heads not divisible by kv_heads
07 hidden_size != q_heads * head_dim
08 model head_dim 80 unsupported profile
09 max_position_embeddings zero
10 model shape snapshot digest flip
```

## 15.2 Runtime Q/K/V

```text
11 Q rank 3
12 K rank 3
13 V rank 3
14 batch mismatch Q/K
15 batch mismatch Q/V
16 Q heads mismatch model
17 K heads mismatch model
18 V heads mismatch model
19 Q head_dim mismatch
20 K head_dim mismatch
21 V head_dim mismatch
22 K/V seq mismatch
23 q_seq zero
24 kv_seq zero
25 selected batch out of range
26 Q element width != 4
27 K element width != 4
28 V element width != 4
```

## 15.3 Causal and dynamic geometry

```text
29 snapshot digest flip
30 snapshot seq_q != Q q_seq
31 snapshot seq_kv != K kv_seq
32 IncrementalDecode q_seq != 1
33 IncrementalDecode q_position not final KV position
34 FullPrefill q_seq != kv_seq
35 ChunkedDecode q_seq < 2
36 suffix alignment false
37 q_seq > kv_seq
38 position arithmetic overflow
39 kv_seq > max_position_embeddings
40 q tile omission
41 q tile duplication
42 kv block count floor division
43 partial tail promoted to Full
44 dispatch x exceeds device limit
45 statistics byte-size overflow
```

## 15.4 Authority and isolation

```text
46 validation fixture production admission
47 Headwise output authority mutation attempt
48 TensorCube stage pointer mutation attempt
```

각 negative control:

```text
rejected == true
Headwise route unchanged == true
TensorCube stage unchanged == true
W0 receipt unchanged == true
TensorCube live dispatch count == 0
partial W1 binding write == 0
partial artifact count == 0
```

---

# 16. State Ownership

## 16.1 Immutable model slot

`NativeWgpuModel`에 다음 immutable slot을 추가한다.

```text
AttentionModelShapeAuthoritySlot
```

결속 시점:

```text
VerifiedModelInstanceBinding 결속 이후
첫 attention forward 이전
```

쓰기 규칙:

```text
first exact bind             1회
same digest rebind           idempotent
other digest overwrite       reject
```

## 16.2 Per-call values

다음은 전역 mutable SSOT가 아니다.

```text
RuntimeAttentionShapeObservation
AttentionRuntimeShapeReconciliationReceipt
TensorCubeStage10DispatchPlan
```

이들은 호출별 immutable value다.

전역 `last_shape`, 조용한 recent-shape cache, 다른 layer의 shape 재사용은 금지한다.

## 16.3 W1 runtime observation boundary

W1 implementation이 production Headwise 함수에 들어갈 수 있는 동작은 순수 shape reconciliation까지다.

허용:

```text
q.dims(), k.dims(), v.dims() 읽기
ModelSpec dimensions 읽기
causal snapshot 검증
planner 생성
unsupported reason 반환
```

금지:

```text
RawWgpuBufferLease 획득
TensorCube shader dispatch
Q/K buffer bind
payload map/readback
TensorCube output commit
Headwise result 변경
```

live lease tap은 W4에서 수행한다.

---

# 17. 구현 파일 경계

신설 권장:

```text
crates/model_core/src/attention_runtime_shape_authority.rs
crates/burn_webgpu_backend/src/tensorcube_stage10_dispatch_spec.rs
crates/orchestrator_local/src/attention_interconnect_w1_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w1_gate.rs
specs/cli/ash_attn_interconnect_w1.args
```

수정 권장:

```text
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_native_smoke.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_causal_sequence_boundary_16x16.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_causal_sequence_boundary_oracle.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_causal_sequence_boundary_verify.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_row_block_max_exp_sum_16x16_subgroup32.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_row_block_max_exp_sum_oracle.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_row_block_max_exp_sum_verify.wgsl
crates/orchestrator_local/Cargo.toml
```

수정 금지:

```text
W0 binding receipt semantics
Headwise route LUT policy
Headwise candidate HOLD state
TensorCube active stage pointer
TensorCube feature mask
TensorCube generation
KV cache implementation
V binding
weighted-V accumulation
decode output commit
```

---

# 18. Rust 산출물

출력 디렉터리:

```text
workspace/runtime/attention/interconnect/w1
```

Rust gate가 실행 시 다음 32개 child artifact를 순서대로 산출한다.

```text
identity.json
parent_w0_binding.json
model_instance_binding.json
model_spec_geometry.json
model_shape_authority.json
fixed_kernel_profile.json
runtime_shape_observation_contract.json
causal_shape_reconciliation.json
q_geometry_plan.json
kv_geometry_plan.json
dispatch_plan.json
q_seq1_incremental_admission.json
prefill_admission.json
chunked_admission.json
dynamic_head_geometry_validation.json
stage8_host_refactor.json
stage9_shader_param_contract.json
stage9_dynamic_class_count_validation.json
stage10_shader_param_contract.json
stage10_dynamic_row_block_validation.json
shape_matrix_execution.json
alternate_geometry_fixture_validation.json
unsupported_geometry_rejection.json
no_route_mutation.json
no_stage_mutation.json
no_output_authority_change.json
no_live_qk_dispatch.json
negative_control_outcomes.json
decision_counters.json
static_checks.json
verdict.json
runtime_artifact.json
```

Canonical ordered list:

```text
child_artifact_expected           32
child_artifact_list_sha256         fc465ab871825f8c7b2b327856e5c56609da093f7a5e5f5684c34620ee87366c
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w1_runtime_artifact.json

schema = ash.attn.interconnect.w1.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w1_local_manifest.json

schema = ash.attn.interconnect.w1.local_manifest.v1
manifest self excluded from hash graph
```

코드 ZIP에는 다음을 넣지 않는다.

```text
명세 Markdown
W1 runtime artifact
W1 local manifest
W1 child artifact
SHA-256 sidecar
신규 helper PowerShell script
신규 helper CMD script
```

artifact와 manifest는 Rust gate가 실행 시 산출한다.

---

# 19. CLI 계약

Binary:

```text
ash_attn_interconnect_w1_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w1.args
```

Canonical keys:

```text
--repo-root
--parent-w0-runtime-artifact
--parent-w0-local-manifest
--verified-model-instance-binding
--model-spec
--expected-model-instance-id
--expected-query-heads
--expected-kv-heads
--expected-head-dim
--expected-kernel-profile-id
--expected-subgroup-size
--rows-per-query-tile
--columns-per-kv-block
--canonical-q-seq-matrix
--canonical-kv-seq-matrix
--query-tiling-extension-matrix
--alternate-validation-head-geometries
--require-q-seq-one-admission
--require-dynamic-kv-block-count
--require-model-runtime-reconciliation
--require-causal-snapshot-reconciliation
--forbid-fixture-production-admission
--forbid-live-qk-dispatch
--forbid-output-commit
--forbid-route-mutation
--forbid-stage-mutation
--minimum-positive-cases
--minimum-negative-controls
--negative-control-mode
--out-dir
--binding-epoch
```

Canonical count:

```text
31 key/value pairs
62 non-empty response-file lines
```

금지:

```text
unknown key
duplicate key
blank line
unordered key sequence
CLI heads overriding ModelSpec
CLI q_seq/kv_seq replacing actual runtime shape
```

`--expected-query-heads`, `--expected-kv-heads`, `--expected-head-dim`은 gate expectation이며 production authority가 아니다. 실제 `ModelSpec`과 다르면 gate가 실패한다.

---

# 20. Static Checks

필수 정적 검사:

```text
fixture equality Q [1,32,16,64] exact comparison count       0
fixture equality K [1,4,64,64] exact comparison count       0
production QUERY_HEADS constant use count                   0
production KV_HEADS constant use count                      0
production KV_BLOCKS=4 authority use count                  0
production KV_TOKENS=64 authority use count                 0
Stage9 literal class counts 1568/480 verifier use count     0
Stage10 rows_per_tile uniform field                         0
Stage10 columns_per_row uniform field                       0
unused WGSL uniform fields                                  0
q_seq=1 positive gate case                                  >=1
kv_seq=65 positive gate case                                >=1
alternate head planner case                                 >=3
route pointer write call                                    0
stage pointer CAS/write call                                0
TensorCube output commit call                               0
live Q/K dispatch from Headwise path                        0
```

WGSL 변경 시:

```text
disk candidate SHA-256 == embedded candidate SHA-256
disk oracle SHA-256 == embedded oracle SHA-256
disk verify SHA-256 == embedded verify SHA-256
```

`burn_webgpu_backend`의 stale embedded WGSL을 방지하기 위해 해당 package의 정상 재컴파일 증거를 artifact에 기록한다.

---

# 21. Runtime Gate

PASS 조건:

```text
parent W0-R2 closure exact
model instance identity exact
model shape authority bound exactly once
model hidden-size factorization exact
runtime Q/K/V shape reconciliation exact
kernel profile 16x16-sg32-hd64 admitted
q_seq=1 incremental planner admitted
kv_seq=1,15,16,17,63,64,65 admitted
q tiling 17,31,32 exact
positive matrix >= 40 cases
negative controls >= 48 cases
Stage9 dynamic candidate-oracle parity exact
Stage10 dynamic candidate-oracle parity exact
all 32 decision counters zero
validation fixture production admission zero
Headwise output authority unchanged
TensorCube live dispatch zero
route mutation zero
stage mutation zero
child artifacts 32/32
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
model_instance=<id>
shape_authority=model_spec_plus_runtime_dims
kernel_profile=tensorcube-stage10-16x16-sg32-hd64-v1
canonical_heads=32/4/64
q_seq_one=admitted
kv_geometry=dynamic_ceil_div_16
positive_cases=40/40
negative_controls=48/48
live_qk_dispatch=0
output_authority=headwise
route_mutation=0
stage_mutation=0
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W1_RUNTIME_SHAPE_AUTHORITY_FIXED_KERNEL_PROFILE_DYNAMIC_QUERY_KV_GEOMETRY_Q_SEQ_1_INCREMENTAL_ADMISSION_MODEL_SPEC_RUNTIME_TENSOR_DIMENSION_RECONCILIATION_HEADWISE_OUTPUT_AUTHORITY_PRESERVED_NO_ROUTE_MUTATION_NO_STAGE_MUTATION_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W1_MODEL_SHAPE_AUTHORITY_RUNTIME_TENSOR_RECONCILIATION_FIXED_PROFILE_Q_SEQ_1_OR_DYNAMIC_KV_GEOMETRY_NOT_PROVEN
```

---

# 22. 직접 Cargo 실행

저장소 루트에서 직접 실행한다.

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p burn_webgpu_backend

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w1_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w1.args"
```

정상 시작 revision:

```text
W1-runtime-shape-authority-fixed-profile-v1
```

별도 실행 스크립트는 canonical 경로로 인정하지 않는다.

---

# 23. 실패 처리

첫 실패를 SSOT로 삼는다.

```text
model authority mismatch
runtime tensor mismatch
causal snapshot mismatch
kernel profile unsupported
query tiling mismatch
KV block derivation mismatch
WGSL dynamic count mismatch
device limit rejection
artifact closure mismatch
```

금지되는 수리:

```text
q_seq=1을 16으로 덮어쓰기
kv_seq를 64로 clamp
heads를 32/4로 clamp
head_dim을 64로 조용히 변환
missing K/V seq를 Q seq로 복사
invalid causal snapshot 재생성
unsupported profile에서 TensorCube dispatch 강행
Headwise output을 TensorCube result로 대체
```

미지원 geometry는 명시적 `ShadowDisabledUnsupportedProfile` receipt를 남기고 Headwise에 영향을 주지 않는다.

---

# 24. W1 이후 경계

W1 이후에 확정되는 것:

```text
누가 static attention shape를 소유하는지
누가 dynamic q_seq/kv_seq를 소유하는지
16x16-sg32-hd64의 고정 profile 경계
q_seq=1의 active/inactive row 의미
kv_seq의 dynamic block derivation
Stage8-10의 fixture equality 제거
```

W2에서 추가할 것:

```text
model_instance_id
layer_index
decode_step
route_id
primitive_id
stream_id
buffer identity/offset/size
device identity
headwise_route_generation
kv_cache_generation
decode_sequence_generation
tensor_storage_generation
tensorcube_stage_generation
candidate_nonce
freshness epoch
```

W3에서 추가할 것:

```text
cached pipelines
persistent scratch ring
submit-fenced reuse
blocking map 없는 runtime executor
```

W4에서 처음 허용할 것:

```text
실제 Headwise Q/K RawWgpuBufferLease shadow tap
TensorCube Stage9-10 live shadow dispatch
Headwise output authority 유지
```

---

# 25. 최종 봉인 문장

W1 PASS 시 다음만 확정한다.

```text
결속된 NativeWgpu 모델 인스턴스의 ModelSpec attention geometry와
호출별 실제 Q/K/V tensor dimensions 및 causal position snapshot이
하나의 fail-closed runtime shape authority로 조정되었다.

TensorCube Stage10의 현재 물리 커널 profile은
16 query rows x 16 KV columns, subgroup 32, head dimension 64로 명시되었고,
query heads, KV heads, q_seq, kv_seq, query tile count, KV block count는
검증된 model/runtime geometry에서 동적으로 유도된다.

q_seq=1 incremental decode는 fake query padding이나 host repack 없이
active row 1개와 inactive row 15개를 가진 정확한 dispatch plan으로 admission되었다.

Headwise는 유일한 attention output authority를 유지하며,
TensorCube live Q/K dispatch, output commit, route mutation, stage mutation은 발생하지 않았다.
```

아직 금지되는 주장:

```text
TensorCube가 실제 live Q/K를 읽었다.
TensorCube가 incremental decode에서 실행됐다.
TensorCube가 attention context를 생성했다.
TensorCube와 Headwise의 최종 수치 parity가 통과했다.
```
