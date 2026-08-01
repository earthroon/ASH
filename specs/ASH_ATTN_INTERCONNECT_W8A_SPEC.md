# ASH-ATTN-INTERCONNECT-W8A

## Dynamic Decode·Prefill Full-Path Context Parity / Policy-Derived Chunk Boundary Matrix / Multi-Layer Exact Invocation Identity / All-Masked·Causal Edge Matrix / GQA KV-Head Transition Sentinel / Repeated Replay Determinism / Scenario-Isolated Resource Epoch / Cross-Profile Compact Aggregate Receipt / No Sentinel Substitution / No Single-Profile Completion / No Full Context Readback / No Decode Route Mutation / No Production Writer Promotion Seal

- Patch ID: `ASH-ATTN-INTERCONNECT-W8A`
- Proposed build revision: `W8A-w8-r1d-dynamic-matrix-multilayer-replay-r1`
- Parent code baseline: `ASH-ATTN-INTERCONNECT-W8-R1D`
- Parent physical authority: `W8 Physical PASS`
- Scope class: full-path physical matrix closure / shadow-only / no production authority transfer
- Production writer before W8A: `HeadwiseFullActive`
- Production writer after W8A: `HeadwiseFullActive`
- TensorCube role after W8A: matrix-qualified device-local context candidate
- W8A role after W8A: cross-profile parity and replay-determinism authority

---

# 0. 명세 목적

W8은 다음 경로를 물리적으로 닫았다.

```text
동일 attention invocation

Headwise committed pre-output-projection context
                ≈
TensorCube Stage12 normalized context candidate
```

W8은 exact invocation identity, Q·K·V·partition lineage, causal·mask snapshot, BHQD↔BQHD semantic mapping, GQA, all-masked zero, device-local comparison과 dual-handle lifetime을 하나의 대표 full-path profile과 comparator sentinels에서 검증했다.

그러나 W8 PASS만으로 다음을 일반화할 수 없다.

```text
seq_kv가 작거나 커져도 같은가?
정확한 chunk 경계 전후에서도 같은가?
q_seq > 1인 실제 prefill full path에서도 같은가?
첫·중간·마지막 layer identity에서도 같은가?
같은 profile을 반복 실행해도 partition·context·receipt 의미가 재현되는가?
시나리오 사이에 stale handle이나 이전 generation이 새는가?
```

W8A는 이 미폐쇄 경계를 닫는다.

W8A의 핵심 문장은 다음이다.

```text
W8의 단일 physical PASS를
동적 decode·prefill geometry,
policy-derived chunk boundary,
first·middle·final layer identity,
causal·all-masked·GQA edge,
반복 replay와 scenario isolation으로 확장한다.
```

W8A는 TensorCube context를 DecodeState에 채택하지 않는다.
W8A는 production writer를 이동하지 않는다.
W8A는 W9A Decode shadow route에 진입하기 위한 matrix qualification evidence만 생성한다.

---

# 1. 현재 기준선과 증명 경계

## 1.1 W8에서 이미 닫힌 것

```text
W7 TensorCube Stage12 context candidate adoption
Headwise committed pre-output-projection context capture
exact invocation identity transaction
Q·K·V generation and logical-range lineage
frozen partition generation and digest lineage
causal·additional-mask snapshot binding
semantic BQHD context ABI
Headwise BHQD ↔ TensorCube BQHD direct index mapping
device-local tolerance parity
128-byte compact first-mismatch receipt
all-masked exact-zero semantics
GQA query-head → KV-head mapping
submission-fenced dual-handle lifetime
full context readback 0
Decode route mutation 0
production writer promotion 0
```

## 1.2 W8A가 새로 닫아야 하는 것

```text
full W4→W8 chain under dynamic seq_kv
full W4→W8 chain under q_seq > 1 prefill
policy-derived chunk boundary -1 / exact / +1
first·middle·final layer exact identity
last-visible causal boundary
active all-masked row under full path
GQA-distinct V distribution under q_seq > 1 full path
same-profile three-run semantic replay determinism
scenario-local source and resource epoch isolation
per-scenario owner-zero before next scenario
matrix completeness and no-skip proof
cross-profile compact aggregate receipt
```

## 1.3 W8A가 증명하지 않는 것

```text
TensorCube context의 DecodeState shadow adoption
output projection parity
logits parity
sampler·token parity
production writer promotion
multi-device·multi-driver qualification
batch > 1
다른 query-head·KV-head·head-dim geometry
장시간 decode soak와 VRAM plateau
device-loss recovery
BaseTrain forward/backward 공유
```

위 항목은 W9A·W9B·W9C·W9D·G202D 이후의 권한이다.

---

# 2. Authority Map

## 2.1 W8A 이전

| Surface | Authority | 상태 |
|---|---|---|
| Q/K/V prepared source | Headwise | production source |
| K/V dynamic residency | Texture-06 | live physical |
| Stage10·11·12 | TensorCube | verified candidate calculation |
| context writer | HeadwiseFullActive | production |
| context parity | W8 comparator | single-profile physical authority |
| Decode route | existing Headwise route | production |

## 2.2 W8A 이후

| Surface | Authority | 상태 |
|---|---|---|
| per-scenario Headwise context | HeadwiseFullActive | oracle + production writer |
| per-scenario TensorCube context | TensorCube | candidate only |
| per-scenario exact identity | W8 transaction | unchanged |
| scenario matrix planning | W8A matrix planner | qualification authority |
| replay semantic determinism | W8A digest closure | qualification authority |
| Decode route | existing Headwise route | unchanged |
| production writer | HeadwiseFullActive | unchanged |

## 2.3 절대 권한선

```text
W8A는 profile을 계획할 수 있다.
W8A는 candidate와 oracle을 비교할 수 있다.
W8A는 matrix qualification을 판정할 수 있다.

W8A는 production context를 선택할 수 없다.
W8A는 output projection 입력을 바꿀 수 없다.
W8A는 Decode route를 바꿀 수 없다.
W8A는 HeadwiseFullActive writer authority를 이동할 수 없다.
```

---

# 3. W8A R1 Geometry Admission

W8A R1은 W8의 모델 geometry를 유지한다.

```text
batch             1
query_head_count  32
kv_head_count     4
gqa_group_size    8
head_dim           64
scalar type        f32
semantic ABI       BQHD
```

W8A R1에서 동적으로 변화하는 축:

```text
q_seq
seq_kv
layer_index
q_position_base
kv_position_base
mask profile
fixture distribution
repeat ordinal
scenario execution epoch
```

금지:

```text
batch > 1을 W8A R1 PASS에 혼입
head geometry 변경
f16·bf16 혼합정밀도 승격
geometry 불일치를 자동 reshape로 은폐
```

다른 head geometry와 batch matrix는 별도 revision으로 분리한다.

---

# 4. 핵심 불변식

## INV-W8A-01 Full-path only

모든 양성 matrix scenario는 다음 전체 경로를 실행해야 한다.

```text
prepared Q/K/V
→ Headwise device-guarded dispatch
→ committed pre-output context capture
→ Texture-06 partition and residency
→ TensorCube Stage10
→ TensorCube Stage11
→ frozen partition replay
→ TensorCube Stage12
→ W8 exact identity bind
→ W8 device-local context parity
→ compact receipt
→ terminal owner-zero
```

`run_device_local_sentinel` 또는 synthetic context buffer만 실행한 scenario는 W8A live matrix count에 포함할 수 없다.

## INV-W8A-02 Parent comparator unchanged

W8A는 W8 comparator의 수학적 판정과 ABI를 변경하지 않는다.

```text
W8 status ABI                  32 words / 128 bytes
absolute tolerance             2.0e-4
relative tolerance             2.0e-3
relative floor                 1.0e-4
semantic context ABI           BQHD f32 v1
Headwise physical ABI          BHQD f32 v1
TensorCube physical ABI        BQHD f32 v1
```

Tolerance를 profile별로 조용히 확대하지 않는다.

## INV-W8A-03 Policy-derived boundary

chunk boundary scenario의 기준 `C`는 숫자를 하드코딩하지 않는다.

```text
C = same-device Texture-06 budget admission이 선택한 selected_chunk_tokens
```

다음이 하나의 frozen budget decision에 묶여야 한다.

```text
policy digest
budget input digest
budget decision digest
selected chunk tier C
slot ceiling
bytes per token per layer
```

## INV-W8A-04 Scenario isolation

각 scenario는 고유한 실행 epoch를 갖는다.

```text
scenario_execution_epoch
Q generation
K generation
V generation
partition generation
context owner IDs
row-class owner IDs
```

이전 scenario의 context·partition·owner handle을 재사용할 수 없다.

## INV-W8A-05 Per-scenario terminal drain

다음 scenario를 시작하기 전에 이전 scenario가 terminal owner-zero 상태여야 한다.

```text
Headwise context owner zero
TensorCube context owner zero
row classification owner zero
Texture-06 replay slot owner zero
W6 global state owner zero
pending submission count zero
```

## INV-W8A-06 No scenario skip

required descriptor는 전부 실행해야 한다.

```text
required scenario count == executed scenario count
required scenario ID set == executed scenario ID set
duplicate scenario ID count == 0
silent skipped scenario count == 0
```

## INV-W8A-07 Exact layer identity

layer sweep는 단순히 receipt의 숫자만 바꾸는 방식으로 통과할 수 없다.

```text
layer_index
invocation identity digest
authority snapshot digest
source generation lineage
scenario descriptor digest
```

모두 해당 layer role에 결합되어야 한다.

## INV-W8A-08 Replay semantic determinism

동일 repeat group의 세 실행은 실행 세대는 달라도 semantic input은 같아야 한다.

```text
same fixture seed
same source payload digest
same geometry
same layer
same positions
same mask snapshot semantics
same policy and budget decision
same selected chunk tier
```

반대로 invocation generation과 owner IDs는 달라야 한다.

## INV-W8A-09 No single-profile completion

다음 중 하나라도 빠지면 W8A PASS를 선언할 수 없다.

```text
decode tiny length
decode W8 continuity length
policy chunk boundary -1 / exact / +1
q_seq > 1 full-path prefill
first·middle·final layer sweep
all-masked full path
causal boundary full path
GQA distinct-head full path
three-run replay group
long multi-chunk profile
```

---

# 5. Canonical Matrix Inputs

## 5.1 Parent evidence

필수 parent:

```text
W8 physical runtime artifact
W8 physical local manifest
W7 physical runtime artifact
Texture-06 physical runtime artifact
model dimensions or runtime artifact
```

W8 parent artifact는 다음을 증명해야 한다.

```text
pass == true
HeadwiseFullActive preserved == true
full context readback count == 0
Decode route mutation count == 0
production writer promotion count == 0
```

## 5.2 Model dimension source

layer role과 long-context profile은 canonical model dimension source에서 파생한다.

필수 fields:

```text
model identity digest
layer count
max position embeddings
query head count
KV head count
head dimension
```

코드 내부에 layer count나 max position을 임의 하드코딩하지 않는다.

## 5.3 Layer role derivation

`L = model_layer_count`일 때:

```text
first_layer  = 0
middle_layer = floor((L - 1) / 2)
final_layer  = L - 1
```

Admission:

```text
L >= 3
first < middle < final
```

세 role이 중복되면 HOLD한다.

## 5.4 Long-context derivation

```text
C = selected_chunk_tokens
long_seq_kv = min(model_max_position_embeddings, max(384, 2*C + 1))
```

필수:

```text
model_max_position_embeddings >= 2*C + 1
long_seq_kv > C
long profile canonical chunk count >= 3 when C permits
```

모델 capacity가 부족하면 profile을 조용히 축소하지 않고 `W8ALongContextCapacityInsufficient`로 HOLD한다.

---

# 6. Scenario Descriptor Contract

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AttentionInterconnectW8AScenarioDescriptor {
    pub scenario_id: String,
    pub semantic_profile_id: String,
    pub execution_epoch: u64,
    pub repeat_group_id: Option<String>,
    pub repeat_ordinal: u32,

    pub batch: u32,
    pub q_seq: u32,
    pub seq_kv: u32,
    pub layer_index: u32,
    pub layer_role: String,

    pub q_position_base: u32,
    pub kv_position_base: u32,
    pub causal_enabled: bool,
    pub mask_profile: String,
    pub fixture_profile: String,
    pub fixture_seed: u64,

    pub selected_chunk_tokens: u32,
    pub expected_chunk_count: u32,
    pub expected_partial_final_chunk: bool,
    pub expected_all_masked_rows: u32,

    pub source_payload_digest: String,
    pub policy_digest: String,
    pub budget_decision_digest: String,
    pub descriptor_digest: String,
}
```

Descriptor는 GPU 실행 전에 immutable하게 생성된다.
실행 중 geometry, layer, mask, fixture seed를 변경할 수 없다.

---

# 7. Required Scenario Matrix

## 7.1 Decode base matrix

| ID | q_seq | seq_kv | layer | 목적 |
|---|---:|---:|---|---|
| `D001` | 1 | 1 | middle | 최소 active decode |
| `D016` | 1 | 16 | middle | 소형 단일 chunk |
| `D017` | 1 | 17 | middle | 소형 비정렬 길이 |
| `D192` | 1 | 192 | middle | 중간 길이 |
| `D384` | 1 | 384 | middle | W8 continuity |
| `DLONG` | 1 | derived long length | middle | 3+ chunk long profile |

기본 decode position:

```text
q_position_base = seq_kv - 1
kv_position_base = 0
causal = true
```

## 7.2 Policy-derived chunk boundary matrix

`C = selected_chunk_tokens`.

| ID | q_seq | seq_kv | 목적 |
|---|---:|---:|---|
| `DCM1` | 1 | C - 1 | boundary below |
| `DCEX` | 1 | C | exact boundary |
| `DCP1` | 1 | C + 1 | boundary above + partial final chunk |

Admission:

```text
C >= 2
DCM1.seq_kv == DCEX.seq_kv - 1
DCP1.seq_kv == DCEX.seq_kv + 1
DCP1.expected_chunk_count == 2
DCP1.expected_partial_final_chunk == true
```

## 7.3 Prefill full-path matrix

| ID | q_seq | seq_kv | layer | 목적 |
|---|---:|---:|---|---|
| `P02-S` | 2 | 2 | middle | 최소 self-prefill |
| `P02-M` | 2 | 64 | middle | history + two-query prefill |
| `P16-S` | 16 | 16 | middle | square prefill |
| `P16-M` | 16 | 64 | middle | multi-query history |
| `P16-L` | 16 | 192 | middle | multi-chunk prefill |

Prefill causal positioning:

```text
q_position_base = seq_kv - q_seq
kv_position_base = 0
query q의 absolute position = q_position_base + q
visible key t iff t <= absolute query position
```

필수:

```text
q_seq <= seq_kv
각 query row의 visible key count가 q에 따라 증가
Headwise와 TensorCube가 동일 causal snapshot digest 사용
```

## 7.4 Layer role anchors

다음 semantic profiles는 first·middle·final layer에서 실행한다.

```text
D384
DCP1
P16-M
```

실행 IDs:

```text
L-FIRST-D384
L-MIDDLE-D384
L-FINAL-D384

L-FIRST-DCP1
L-MIDDLE-DCP1
L-FINAL-DCP1

L-FIRST-P16M
L-MIDDLE-P16M
L-FINAL-P16M
```

middle-layer 기본 scenario와 중복되는 경우 execution record를 공유할 수 없다.
각 layer anchor는 고유 invocation과 source generation을 가져야 한다.

## 7.5 All-masked full-path scenario

| ID | q_seq | seq_kv | layer | mask |
|---|---:|---:|---|---|
| `AMZ` | 2 | 16 | middle | explicit all-masked additional mask |

필수:

```text
Headwise committed context exact +0.0
TensorCube context exact +0.0
active scalar tolerance 비교 대신 exact zero
row classification == ALL_MASKED
nonzero count == 0
NaN/Inf count == 0
```

Synthetic zero buffers로 대체할 수 없다.
실제 Headwise와 TensorCube full path가 동일 all-masked snapshot을 소비해야 한다.

## 7.6 Causal edge scenario

| ID | q_seq | seq_kv | layer | 목적 |
|---|---:|---:|---|---|
| `CAUSAL-LAST` | 2 | C + 1 | middle | query별 last visible key 경계 |

검증:

```text
query row 0 last visible = q_position_base
query row 1 last visible = q_position_base + 1
future key contribution exact zero
causal snapshot digest 일치
```

## 7.7 GQA distinct-head full-path scenario

| ID | q_seq | seq_kv | layer | fixture |
|---|---:|---:|---|---|
| `GQA-DISTINCT` | 2 | 64 | middle | KV head별 distinct V band |

V fixture는 KV head마다 겹치지 않는 수치 band를 사용한다.

```text
Q heads 0..7    → KV head 0 band
Q heads 8..15   → KV head 1 band
Q heads 16..23  → KV head 2 band
Q heads 24..31  → KV head 3 band
```

검증:

```text
mapped_kv_head == query_head / 8
cross-band contamination count == 0
Headwise/TensorCube context parity PASS
```

## 7.8 Unique semantic scenario count

최소 unique semantic descriptors:

```text
D001 D016 D017 D192 D384 DLONG
DCM1 DCEX DCP1
P02-S P02-M P16-S P16-M P16-L
AMZ CAUSAL-LAST GQA-DISTINCT
```

```text
minimum unique semantic scenario count = 17
```

Layer role expansion은 별도 physical executions로 계산한다.

---

# 8. Replay Determinism Matrix

다음 repeat groups는 각각 정확히 3회 실행한다.

```text
R-D384
R-DCP1
R-P16M
R-AMZ
```

각 group의 repeat ordinal:

```text
0
1
2
```

## 8.1 동일해야 하는 것

```text
semantic descriptor digest
source payload digest
policy digest
budget decision digest
selected chunk tokens
canonical partition shape digest
W8 semantic status digest
row classification digest
W8A compact context digest
all-masked semantic verdict
GQA semantic verdict
causal semantic verdict
```

## 8.2 달라야 하는 것

```text
scenario execution epoch
Q generation
K generation
V generation
partition generation
Headwise owner ID
TensorCube owner ID
row-class owner ID
submission serial
```

## 8.3 Replay verdict

```text
same semantic input
+ fresh execution/resource epoch
+ same semantic output digest
= replay deterministic PASS
```

동일 GPU handle을 세 번 읽는 것은 replay가 아니다.

---

# 9. W8A Compact Context Digest

W8A는 반복 실행의 semantic output 비교를 위해 device-local context digest를 생성한다.

## 9.1 입력

```text
TensorCube Stage12 normalized context candidate
semantic BQHD geometry
row classification buffer
scenario descriptor digest seed
```

## 9.2 출력 ABI

```text
8 × u32
32 bytes
```

권장 lanes:

```text
0  scalar count
1  active row count
2  all-masked row count
3  finite scalar count
4  hash lane A
5  hash lane B
6  hash lane C
7  hash lane D
```

네 hash lane은 서로 다른 seed와 mixing order를 사용한다.

## 9.3 Digest constraints

```text
GPU에서 생성
compact 32-byte readback만 허용
full context payload readback 금지
host-side context hashing 금지
single XOR lane 금지
scenario descriptor digest와 geometry를 seed에 포함
```

Digest는 암호학적 진위 증명이 아니라 동일 실행 의미의 replay comparator다.
Lineage authority는 artifact digest chain이 담당한다.

---

# 10. Per-Scenario Execution Transaction

각 scenario는 다음 순서로 실행한다.

```text
previous scenario terminal owner-zero admission
→ immutable descriptor adoption
→ fresh Q/K/V generations
→ Headwise dispatch and committed context capture
→ Texture-06 budget decision adoption
→ Stage10·11·12 full path
→ W8 exact invocation identity transaction
→ W8 device-local parity
→ W8A compact context digest
→ compact receipt readback
→ submission completion
→ all owners terminal drain
→ owner-zero receipt
→ next scenario admission
```

금지:

```text
다음 scenario를 이전 submission completion 전에 시작
context handle을 digest 이후 보존
row classification handle을 다음 scenario에 전달
budget decision을 scenario 도중 재선택
실패 후 같은 execution epoch로 재시도
```

---

# 11. Dynamic Q-Sequence Requirements

W8A는 q_seq를 런타임 geometry로 취급한다.

다음 구성요소가 `q_seq`를 동적으로 소비해야 한다.

```text
Headwise prepared tensor geometry
Headwise output context allocation
Stage10 q tile count
Stage11 row count
Stage12 numerator/context allocation
W8 comparator semantic indexing
row classification count
compact digest scalar count
CPU f64 physical-gate oracle
artifact geometry receipt
```

금지:

```text
q_seq=1 전용 index formula
row_count = query_head_count 하드코딩
Headwise context length = H*D 하드코딩
Stage12 context length = H*D 하드코딩
prefill scenario를 q_seq개의 decode 호출로 대체
```

Prefill은 하나의 invocation 안에서 `q_seq > 1`이어야 한다.

---

# 12. Dynamic Stage10·11·12 Geometry

## 12.1 Stage10

```text
row count = batch * query_head_count * q_seq
q tile count = ceil(q_seq / q_tile_tokens)
chunk-local statistic count = row count * chunk count
```

## 12.2 Stage11

```text
global state row count = batch * query_head_count * q_seq
canonical merge order = query tile → chunk ordinal → block index
```

모든 query row가 독립 running max와 denominator를 가져야 한다.

## 12.3 Stage12

```text
context element count = batch * q_seq * query_head_count * head_dim
row classification count = batch * q_seq * query_head_count
```

Stage12는 각 query row의 absolute position을 사용하여 causal mask를 재계산한다.

## 12.4 W8 comparator

Semantic index:

```text
[b, q, h, d]
```

Headwise physical:

```text
[((b * H + h) * Q + q) * D + d]
```

TensorCube physical:

```text
[((b * Q + q) * H + h) * D + d]
```

W8A에서 `q_seq=2`와 `q_seq=16`이 이 차이를 실제 full path로 노출한다.

---

# 13. Mask Snapshot Contract

## 13.1 Causal snapshot

필수 fields:

```text
causal enabled
q position base
kv position base
q_seq
seq_kv
last-visible formula version
snapshot digest
```

## 13.2 Additional mask snapshot

W8A R1 required kinds:

```text
NONE
ALL_MASKED
```

필수 fields:

```text
mask kind
mask dimensions
mask payload or canonical synthetic-rule digest
masked row count
snapshot digest
```

ALL_MASKED가 host에서 context를 zero-fill하는 방식이면 FAIL한다.
Mask는 Headwise와 TensorCube score path에 들어가야 한다.

## 13.3 Combined snapshot

```text
combined_mask_snapshot_digest =
  H(causal_snapshot_digest,
    additional_mask_snapshot_digest,
    geometry_digest)
```

W8 exact invocation identity에 결합한다.

---

# 14. Partition and Chunk Boundary Verification

각 scenario는 다음을 기록한다.

```text
selected_chunk_tokens
canonical chunk count
chunk token_start list
chunk token_count list
partial final chunk flag
partition generation
partition digest
canonical chunk order digest
```

## 14.1 Boundary assertions

```text
C-1 → chunk count 1
C   → chunk count 1, token_count C
C+1 → chunk count 2, final token_count 1
```

`C+1`에서 두 번째 chunk가 없으면 FAIL한다.

## 14.2 Long profile

```text
seq_kv = max(384, 2*C+1) within model capacity
chunk count >= 3 when C drives the maximum
```

첫·중간·마지막 chunk가 모두 Stage10·11·12 receipt에 나타나야 한다.

## 14.3 Frozen decision

W8A matrix 전체에서 같은 device budget policy revision을 사용한다.

```text
policy revision change count = 0
budget decision reselection for boundary trio = 0
selected C drift count = 0
```

---

# 15. Multi-Layer Exact Identity

각 layer anchor에서 identity는 다음을 포함한다.

```text
model instance identity
model instance epoch
layer index
layer role
scenario execution epoch
decode or prefill step identity
Q/K/V generation and range
partition generation and digest
mask snapshot
production authority snapshot
```

Layer 변경 시:

```text
layer index changes
identity digest changes
authority snapshot is newly captured
Q/K/V generations are fresh
partition generation is fresh
```

금지:

```text
middle-layer receipt를 first/final로 라벨만 변경
Q/K/V buffers를 generation 갱신 없이 재사용
layer가 달라도 동일 exact invocation digest 사용
```

---

# 16. Scenario-Isolated Resource Epoch

## 16.1 Resource epoch

```text
matrix_run_epoch
scenario_execution_epoch
source_generation_epoch
partition_generation_epoch
submission_epoch
```

각 epoch은 artifact에 기록한다.

## 16.2 No cross-scenario handle passage

다음 handle types는 scenario boundary를 넘을 수 없다.

```text
HeadwisePreOutputProjectionContextHandle
TensorCubeStage12ContextCandidateHandle
TensorCubeStage12ContextRowClassificationHandle
W6 global-state owner
Texture-06 slice consumer owner
staging or readback buffer owner
```

## 16.3 Admission

다음 scenario 시작 전:

```text
previous owners live count == 0
previous pending submissions == 0
previous readback maps outstanding == 0
```

실행 세대만 증가시키고 실제 handle이 살아 있으면 FAIL한다.

---

# 17. CPU Reference Boundary

W8A production runtime path는 CPU context payload를 읽지 않는다.

Physical gate에서는 검증 목적으로 scenario별 CPU f64 oracle을 사용할 수 있다.

허용:

```text
physical gate fixture Q/K/V는 host fixture로 존재
CPU f64 oracle context 계산
GPU compact context parity receipt와 CPU oracle 비교
```

금지:

```text
GPU context 전체를 매 scenario host로 readback
CPU context를 production candidate로 사용
CPU oracle 실패 시 GPU parity만으로 PASS
```

W8A 기본 physical gate의 positive matrix는 device-local Headwise↔TensorCube parity를 authority로 사용한다.
CPU f64는 대표 anchor subset에서 독립 oracle로 사용한다.

권장 CPU anchor subset:

```text
D001
D384
DCP1
P02-S
P16-M
AMZ
GQA-DISTINCT
```

---

# 18. Per-Scenario Compact Receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct AttentionInterconnectW8AScenarioReceipt {
    pub scenario_id: String,
    pub descriptor_digest: String,
    pub execution_epoch: u64,
    pub layer_index: u32,
    pub q_seq: u32,
    pub seq_kv: u32,

    pub source_payload_digest: String,
    pub invocation_identity_digest: String,
    pub partition_generation: u64,
    pub partition_shape_digest: String,
    pub mask_snapshot_digest: String,

    pub w8_receipt_digest: String,
    pub w8_status_semantic_digest: String,
    pub row_classification_digest: String,
    pub context_digest_words: [u32; 8],

    pub compared_scalar_count: u64,
    pub mismatch_count: u32,
    pub non_finite_count: u32,
    pub all_masked_nonzero_count: u32,
    pub gqa_violation_count: u32,
    pub layout_violation_count: u32,
    pub bounds_violation_count: u32,

    pub full_context_readback_count: u32,
    pub context_materialization_copy_count: u32,
    pub decode_route_mutation_count: u32,
    pub production_writer_promotion_count: u32,
    pub tensorcube_output_commit_count: u32,

    pub headwise_owner_zero: bool,
    pub tensorcube_owner_zero: bool,
    pub row_class_owner_zero: bool,
    pub texture_replay_owner_zero: bool,
    pub w6_global_state_owner_zero: bool,
    pub pending_submission_zero: bool,

    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 19. Replay Group Receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct AttentionInterconnectW8AReplayGroupReceipt {
    pub repeat_group_id: String,
    pub expected_repeat_count: u32,
    pub observed_repeat_count: u32,
    pub scenario_receipt_digests: Vec<String>,

    pub semantic_descriptor_digest: String,
    pub source_payload_digest: String,
    pub partition_shape_digest: String,
    pub w8_status_semantic_digest: String,
    pub row_classification_digest: String,
    pub context_digest_words: [u32; 8],

    pub unique_execution_epoch_count: u32,
    pub unique_q_generation_count: u32,
    pub unique_k_generation_count: u32,
    pub unique_v_generation_count: u32,
    pub unique_partition_generation_count: u32,
    pub unique_owner_id_count: u32,

    pub semantic_digest_mismatch_count: u32,
    pub stale_generation_count: u32,
    pub owner_reuse_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 20. Cross-Profile Aggregate Receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct AttentionInterconnectW8AAggregateReceipt {
    pub patch_id: String,
    pub build_revision: String,
    pub matrix_profile_id: String,
    pub parent_w8_artifact_digest: String,
    pub matrix_plan_digest: String,

    pub required_scenario_count: u32,
    pub executed_scenario_count: u32,
    pub passed_scenario_count: u32,
    pub failed_scenario_count: u32,
    pub skipped_scenario_count: u32,
    pub duplicate_scenario_count: u32,

    pub decode_scenario_count: u32,
    pub prefill_scenario_count: u32,
    pub layer_anchor_execution_count: u32,
    pub boundary_execution_count: u32,
    pub replay_execution_count: u32,

    pub total_compared_scalar_count: u64,
    pub total_mismatch_count: u64,
    pub total_non_finite_count: u64,
    pub total_all_masked_nonzero_count: u64,
    pub total_gqa_violation_count: u64,
    pub total_layout_violation_count: u64,
    pub total_bounds_violation_count: u64,

    pub replay_group_receipts: Vec<AttentionInterconnectW8AReplayGroupReceipt>,
    pub required_scenario_set_digest: String,
    pub executed_scenario_set_digest: String,

    pub cross_scenario_handle_reuse_count: u32,
    pub cross_layer_identity_collision_count: u32,
    pub stale_partition_generation_count: u32,
    pub scenario_terminal_drain_missing_count: u32,

    pub full_context_readback_count: u32,
    pub context_materialization_copy_count: u32,
    pub decode_route_mutation_count: u32,
    pub production_writer_promotion_count: u32,
    pub tensorcube_output_commit_count: u32,

    pub headwise_fullactive_authority_preserved: bool,
    pub matrix_complete: bool,
    pub replay_deterministic: bool,
    pub scenario_isolation_preserved: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 21. Verification Gate

## Binary

```text
ash_attn_interconnect_w8a_verification_gate
```

## 역할

GPU 실행 없이 다음을 검증한다.

```text
W8 parent artifact and manifest presence
W8 parent PASS and authority seal
W8A source registration
W8A matrix planner source
W8 full-path runner reuse
q_seq dynamic geometry markers
prefill causal-position markers
policy-derived C markers
first/middle/final derivation markers
scenario terminal drain markers
8-word context digest shader
CLI key uniqueness and pair format
forbidden production mutation markers absent
runtime output path allowlist
```

## Verification PASS 조건

```text
required source files present
required shader present
matrix plan contains all required semantic IDs
repeat count == 3
scenario skip forbidden
sentinel substitution forbidden
full context readback forbidden
Decode mutation forbidden
writer promotion forbidden
```

Verification PASS는 physical completion이 아니다.

---

# 22. Physical Gate

## Binary

```text
ash_attn_interconnect_w8a_physical_gate
```

## 실행 순서

```text
W8 parent artifact admission
→ model dimension admission
→ Texture-06 budget decision
→ canonical matrix plan freeze
→ one native device/queue bootstrap
→ scenarios in canonical order
→ per-scenario full path
→ per-scenario terminal drain
→ replay group comparison
→ aggregate receipt
→ runtime artifact and manifest publication
→ PASS token
```

## Device lifetime

W8A matrix run은 하나의 device/queue epoch를 공유한다.

```text
single device bootstrap
single queue lineage
multiple isolated scenario submissions
```

Scenario isolation은 device 재생성이 아니라 resource owner와 generation 격리로 증명한다.

## Canonical order

```text
decode base ascending seq_kv
→ chunk boundary C-1/C/C+1
→ prefill ascending q_seq then seq_kv
→ first/middle/final layer anchors
→ all-masked
→ causal edge
→ GQA distinct
→ repeat groups by group ID then ordinal
```

실행 순서가 plan digest와 다르면 FAIL한다.

---

# 23. CLI Contract

```text
--repo-root
--expected-patch-id
--expected-build-revision
--source-profile
--matrix-profile-id

--parent-w8-physical-artifact
--parent-w8-local-manifest
--parent-w7-physical-artifact
--parent-texture06-physical-artifact
--model-dimension-artifact

--require-w8-pass
--require-headwise-fullactive
--require-full-path-scenarios
--require-policy-derived-boundaries
--require-first-middle-final-layers
--require-prefill-qseq-two
--require-prefill-qseq-sixteen
--require-all-masked-zero
--require-causal-boundary
--require-gqa-distinct-profile
--require-replay-determinism
--repeat-count

--absolute-tolerance
--relative-tolerance
--relative-floor

--forbid-scenario-skip
--forbid-sentinel-substitution
--forbid-full-context-readback
--forbid-context-materialization-copy
--forbid-cross-scenario-handle-reuse
--forbid-decode-route-mutation
--forbid-production-writer-promotion
--forbid-tensorcube-output-commit

--run-output-root
--canonical-runtime-specification
--canonical-runtime-artifact
--canonical-local-manifest
```

Required values:

```text
--repeat-count 3
--forbid-scenario-skip true
--forbid-sentinel-substitution true
--forbid-full-context-readback true
--forbid-context-materialization-copy true
--forbid-cross-scenario-handle-reuse true
--forbid-decode-route-mutation true
--forbid-production-writer-promotion true
--forbid-tensorcube-output-commit true
```

Response-file은 key/value pair format을 유지한다.

---

# 24. Canonical Artifacts

```text
workspace/runtime/attention/interconnect/
  ash_attn_interconnect_w8a_verification_runtime_specification.json
  ash_attn_interconnect_w8a_verification_runtime_artifact.json
  ash_attn_interconnect_w8a_verification_local_manifest.json

  ash_attn_interconnect_w8a_physical_runtime_specification.json
  ash_attn_interconnect_w8a_physical_runtime_artifact.json
  ash_attn_interconnect_w8a_physical_local_manifest.json
```

Scenario-local execution evidence:

```text
workspace/runtime/attention/interconnect/w8a_physical/
  matrix_plan.json
  scenarios/<scenario-id>/compact_receipt.json
  repeat_groups/<group-id>/replay_receipt.json
```

위 파일은 전부 Rust가 실행 시 생성한다.
코드 ZIP이나 overlay ZIP에 runtime specification, manifest, artifact를 포함하지 않는다.

## 24.1 Runtime artifact lanes

```text
identity
parent_provenance
model_geometry
texture_policy
budget_decision
matrix_plan
required_scenario_set
executed_scenario_set
decode_profiles
prefill_profiles
chunk_boundary_profiles
layer_role_profiles
all_masked_closure
causal_boundary_closure
gqa_closure
repeat_determinism
scenario_isolation
owner_zero_closure
forbidden_path_counters
performance_observation_non_authoritative
final_verdict
```

## 24.2 Manifest contents

```text
source file digests
shader digests
CLI args digest
W8 parent artifact digest
W8 parent manifest digest
W7 parent artifact digest
Texture-06 parent artifact digest
model dimension artifact digest
matrix plan digest
runtime specification digest
physical artifact digest
adapter identity
driver/backend identity
PASS token
production authority before/after digest
```

---

# 25. PASS Criteria

## 25.1 Matrix completeness

```text
required scenario count == executed scenario count
passed scenario count == required scenario count
failed scenario count == 0
skipped scenario count == 0
duplicate scenario count == 0
required scenario set digest == executed scenario set digest
```

## 25.2 Per-scenario parity

모든 scenario에서:

```text
exact invocation identity PASS
Q/K/V generation lineage PASS
partition lineage PASS
causal·mask snapshot binding PASS
Headwise context capture live
TensorCube context candidate live
W8 device-local parity PASS
mismatch count 0
non-finite count 0
layout violation count 0
bounds violation count 0
GQA violation count 0
full context readback count 0
context materialization copy count 0
```

## 25.3 Dynamic geometry

```text
q_seq=1 decode set PASS
q_seq=2 full-path prefill PASS
q_seq=16 full-path prefill PASS
seq_kv 1/16/17/192/384 PASS
C-1/C/C+1 PASS
long multi-chunk PASS
```

## 25.4 Multi-layer

```text
first layer anchors PASS
middle layer anchors PASS
final layer anchors PASS
cross-layer stale handle count 0
cross-layer identity collision count 0
```

## 25.5 Replay determinism

```text
repeat count == 3 per required group
semantic input digest equal within group
compact context digest equal within group
partition shape digest equal within group
W8 status semantic digest equal within group
execution epochs unique
source generations unique
owner IDs unique
replay digest mismatch count 0
```

## 25.6 Lifetime

모든 scenario에서:

```text
Headwise owner zero
TensorCube owner zero
row-class owner zero
Texture-06 replay slot owner zero
W6 global state owner zero
pending submission count zero
scenario terminal drain observed
```

## 25.7 Authority preservation

```text
Decode route mutation count 0
production writer promotion count 0
TensorCube output commit count 0
HeadwiseFullActive authority before/after digest equal
```

## 25.8 Expected positive counts

```text
total compared scalar count > 0
per-scenario compact W8 status readback count == 1
per-scenario W8A context digest readback count == 1
per-scenario W8A context digest readback bytes == 32
full context payload readback bytes == 0
```

---

# 26. FAIL/HOLD Codes

## Parent and plan

```text
W8AParentW8ArtifactMissing
W8AParentW8ManifestMissing
W8AParentW8NotPass
W8AParentRevisionMismatch
W8AModelDimensionArtifactMissing
W8AModelGeometryMismatch
W8AMatrixPlanDigestMismatch
W8ARequiredScenarioMissing
W8ADuplicateScenarioId
W8AScenarioOrderMismatch
W8AScenarioSkipObserved
W8ASentinelSubstitutionObserved
```

## Policy and boundary

```text
W8ATexturePolicyMismatch
W8ABudgetDecisionMismatch
W8ASelectedChunkTierInvalid
W8AChunkBoundaryBelowOne
W8AChunkBoundaryRelationMismatch
W8AChunkCountMismatch
W8APartialFinalChunkMissing
W8ALongContextCapacityInsufficient
W8APartitionShapeDrift
```

## Geometry and layer

```text
W8AUnsupportedBatch
W8AUnsupportedHeadGeometry
W8AInvalidDecodePosition
W8AInvalidPrefillPosition
W8APrefillQSeqGreaterThanKv
W8ALayerCountBelowThree
W8ALayerRoleCollision
W8ALayerIdentityMismatch
W8ACrossLayerIdentityCollision
```

## Parity and semantics

```text
W8AContextParityFailed
W8AAllMaskedZeroFailed
W8ACausalBoundaryFailed
W8AGqaMappingFailed
W8AContextDigestMissing
W8AContextDigestMismatch
W8AReplaySemanticDigestMismatch
W8ANonFiniteContextObserved
```

## Lifetime and isolation

```text
W8APreviousScenarioOwnerStillLive
W8ACrossScenarioHandleReuse
W8AOwnerIdReuse
W8AStaleSourceGeneration
W8AStalePartitionGeneration
W8AScenarioTerminalDrainMissing
W8AHeadwiseOwnerZeroFailed
W8ATensorCubeOwnerZeroFailed
W8ARowClassOwnerZeroFailed
W8ATextureReplayOwnerZeroFailed
W8AW6GlobalStateOwnerZeroFailed
```

## Forbidden path

```text
W8AFullContextReadbackObserved
W8AContextMaterializationCopyObserved
W8ADecodeRouteMutationObserved
W8AProductionWriterPromotionObserved
W8ATensorCubeOutputCommitObserved
W8AToleranceMutationObserved
```

---

# 27. 금지 구현

```text
W8 P1/P2/P3 synthetic sentinel을 W8A live matrix로 카운트
q_seq=1 profile만 실행하고 prefill PASS 선언
first layer만 실행하고 multi-layer PASS 선언
layer_index 숫자만 바꾸고 source lineage 재사용
chunk size C를 코드에 하드코딩
C-1/C/C+1 profile마다 budget decision 재선택
실패 scenario를 skipped로 바꾸어 aggregate PASS
repeat group에서 동일 owner handle 재사용
repeat determinism을 mismatch_count==0만으로 선언
context digest를 host-side full payload로 계산
한 word XOR digest만으로 replay deterministic 선언
full context transpose 또는 clone buffer 생성
W8 tolerance를 profile별로 확대
identity mismatch 후 geometry만 맞춰 재시도
full score/probability matrix 생성
TensorCube context를 downstream output에 기록
Decode route selector 수정
HeadwiseFullActive authority pointer 수정
output projection 입력 선택 변경
실제 matrix GPU PASS 없이 completion 주장
W9A shadow route 코드를 W8A에 혼입
```

---

# 28. Required Static Assertions

```text
W8A_PATCH_ID == "ASH-ATTN-INTERCONNECT-W8A"
W8A_BUILD_REVISION == "W8A-w8-r1d-dynamic-matrix-multilayer-replay-r1"
W8A_MATRIX_PROFILE_ID == "ash.attn.interconnect.w8a.matrix.dynamic_decode_prefill_multilayer.r1"
W8A_REPEAT_COUNT == 3
W8A_CONTEXT_DIGEST_WORD_COUNT == 8
W8A_CONTEXT_DIGEST_BYTES == 32
W8_STATUS_WORD_COUNT == 32
W8_STATUS_BYTES == 128
W8_DEFAULT_ABS_TOLERANCE == 2.0e-4
W8_DEFAULT_REL_TOLERANCE == 2.0e-3
W8_DEFAULT_REL_FLOOR == 1.0e-4
```

Source scan assertions:

```text
positive matrix path calls full W4→W8 scenario runner
positive matrix path does not call sentinel-only runner
matrix planner derives C from budget decision
matrix planner derives first/middle/final from model layer count
scenario transition asserts terminal owner-zero
W8A context digest shader has 8 integer lanes
W8A source contains no production authority write
W8A gate asserts full_context_readback_count == 0
W8A gate asserts scenario_skip_count == 0
W8A gate asserts production_writer_promotion_count == 0
W8A gate asserts decode_route_mutation_count == 0
```

---

# 29. Proposed PASS Token

```text
PASS_ASH_ATTN_INTERCONNECT_W8A_DYNAMIC_DECODE_PREFILL_FULL_PATH_CONTEXT_PARITY_POLICY_DERIVED_CHUNK_BOUNDARY_MULTI_LAYER_EXACT_INVOCATION_ALL_MASKED_CAUSAL_GQA_REPLAY_DETERMINISM_SCENARIO_ISOLATED_OWNER_ZERO_CROSS_PROFILE_COMPACT_RECEIPT_NO_SENTINEL_SUBSTITUTION_NO_SINGLE_PROFILE_COMPLETION_NO_FULL_CONTEXT_READBACK_NO_DECODE_ROUTE_MUTATION_NO_WRITER_PROMOTION_SEALED
```

---

# 30. Completion Statement

W8A는 다음 문장이 Rust-generated runtime artifact와 physical PASS로 재현될 때 완료된다.

```text
W8에서 검증된 Headwise committed pre-output context와
TensorCube Stage12 candidate의 device-local parity가,

seq_kv 1·16·17·192·384,
Texture-06 policy가 선택한 chunk tier의 C-1·C·C+1,
동적으로 파생된 long multi-chunk profile,
q_seq 2·16의 실제 prefill full path,
first·middle·final layer identity,
all-masked·last-visible causal·GQA-distinct edge profile에서
모두 유지됐다.

모든 양성 scenario는 synthetic sentinel이 아니라
prepared Q/K/V부터 Headwise capture와 TensorCube Stage10·11·12를 거쳐
W8 comparator까지 이어지는 전체 경로를 실행했다.

반복 대상 profile은 서로 다른 execution epoch와 source generation을 사용하면서도
동일한 compact context digest와 semantic replay digest를 생성했고,
각 scenario 뒤 Headwise·TensorCube·row-class·Texture-06·W6 자원은
다음 scenario admission 전에 terminal owner-zero로 회수됐다.

matrix 동안 full context readback, context materialization,
Decode route mutation, TensorCube output commit,
HeadwiseFullActive production writer promotion은 없었다.
```

---

# 31. 다음 패치 경계

W8A PASS 뒤 다음 패치는 `ASH-ATTN-DECODE-W9A`다.

```text
Immutable Decode Attention Route SSOT /
TensorCube Context Shadow Adoption /
Headwise Production Context Preservation /
Output Projection Dual Observation /
Logits Shadow Parity /
Token Candidate Parity /
No Sampler Input Mutation /
No Selected Token Mutation Seal
```

W8A PASS 전에는 W9A Decode shadow route를 시작하지 않는다.

W8A에서 production writer를 이동하지 않는다.
W8A의 최종 산출물은 writer 권한이 아니라 matrix qualification evidence다.
