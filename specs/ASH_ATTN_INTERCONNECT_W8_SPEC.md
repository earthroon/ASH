# ASH-ATTN-INTERCONNECT-W8

## W7 TensorCube Context Candidate Adoption / Headwise Pre-Output-Projection Context Capture / Exact Invocation Identity Transaction / Q·K·V·Partition Generation Lineage / Causal·Mask Snapshot Binding / Canonical Pre-Projection Context ABI / Device-Local Candidate·Oracle Comparison / Compact First-Mismatch Receipt / All-Masked Exact-Zero Preservation / Causal Boundary Preservation / GQA Head Mapping Preservation / Submission-Fenced Dual Handle Lifetime / No Full Context Readback / No Decode Route Mutation / No Production Writer Promotion Seal

- Patch ID: `ASH-ATTN-INTERCONNECT-W8`
- Proposed build revision: `W8-w7-context-headwise-preprojection-live-parity-r1`
- Parent code baseline: `ASH-ATTN-INTERCONNECT-W7-R1A`
- Parent physical authority: `W7 Physical PASS`
- Scope class: physical parity closure / shadow-only / no production authority transfer
- Production writer before W8: `HeadwiseFullActive`
- Production writer after W8: `HeadwiseFullActive`
- TensorCube role after W8: device-local context candidate
- W8 role after W8: exact-invocation parity authority

---

# 0. 명세 목적

W7은 실제 Headwise Q/K/V source, Texture-06 dynamic K/V residency, TensorCube Stage10·11·12를 연결하여 normalized attention context candidate까지 생성했다.

그러나 W7의 PASS는 다음을 아직 증명하지 않았다.

```text
TensorCube Stage12 context candidate
==
동일 Headwise invocation이 실제 downstream에 전달한
pre-output-projection attention context
```

W8은 이 미폐쇄 경계를 닫는다.

W8의 질문은 단순한 두 버퍼의 수치 유사성이 아니다.

```text
같은 모델 인스턴스인가?
같은 authority pointer 세대인가?
같은 route와 layer인가?
같은 session과 decode step인가?
같은 Q·K·V source generation과 exact logical range인가?
같은 frozen partition generation인가?
같은 causal·mask snapshot인가?
같은 semantic context ABI인가?
```

위 조건이 하나의 immutable transaction으로 봉인된 뒤에만 Headwise context와 TensorCube context를 device-local에서 비교한다.

W8은 TensorCube 결과를 DecodeState에 채택하지 않는다. W8은 production writer를 이동하지 않는다. W8은 W9의 권한 이동에 필요한 비교 증거만 만든다.

---

# 1. 현재 기준선과 증명 경계

## 1.1 W7에서 이미 닫힌 것

```text
Headwise live prepared Q/K/V
→ Texture-06 dynamic K/V chunk residency
→ Stage10 chunk-local score statistics
→ Stage11 global online-softmax max·denominator
→ 동일 frozen K/V partition replay
→ Stage12 score recomputation
→ weighted V numerator
→ global denominator normalization
→ TensorCube context candidate
```

W7에서 유지된 금지선:

```text
full score matrix allocation           0
full probability matrix allocation     0
texture-to-buffer K/V rehydration       0
TensorCube output commit                0
attention output mutation               0
production route mutation               0
```

## 1.2 W8이 새로 닫아야 하는 것

```text
동일 실제 invocation의 Headwise pre-output-projection context
vs
W7 TensorCube Stage12 normalized context candidate
```

W8은 두 결과가 다음 의미에서 동일함을 증명한다.

```text
same model/session/layer/step
same Q/K/V generation and logical ranges
same frozen partition generation and digest
same causal and additional-mask snapshot
same semantic BQHD context coordinates
same GQA query-head → KV-head lineage
same all-masked exact-zero behavior
```

---

# 2. Authority Contract

## 2.1 W8 authority map

| Surface | Authority |
|---|---|
| Headwise downstream context | production oracle / writer |
| TensorCube Stage12 context | device-local candidate |
| W8 comparator | parity authority only |
| DecodeState route | unchanged |
| output projection | unchanged |
| logits/sampler | unchanged |

## 2.2 절대 금지

```text
TensorCube context를 DecodeState에 commit
Headwise production context 교체
output projection 입력 교체
CPU context fallback
full context host roundtrip
새 partition 선택
다른 invocation 결과 비교
비교 실패를 성공으로 완화
silent fallback
```

---

# 3. Canonical Pre-Projection Context ABI

## 3.1 Semantic ABI

W8의 비교 의미 좌표는 다음으로 고정한다.

```text
semantic coordinate = [batch, query_token, query_head, head_dimension]
canonical semantic layout name = BQHD
scalar type = f32
```

## 3.2 물리 ABI 차이

현재 Headwise와 TensorCube의 물리 flatten 순서는 다르다.

```text
Headwise physical context
[B, H, Q, D]

TensorCube Stage12 physical context
[B, Q, H, D]
```

`q_seq = 1`에서는 두 flatten 순서가 우연히 동일해 보일 수 있다. 따라서 W8은 raw linear index parity를 금지한다.

## 3.3 semantic-to-physical mapping

Comparator는 각 semantic coordinate에 대해 물리 인덱스를 직접 계산한다.

```text
headwise_index = (((b * H + h) * Q + q) * D + d)
tensorcube_index = (((b * Q + q) * H + h) * D + d)
```

금지:

```text
full transpose buffer
context copy for canonicalization
host-side canonicalization
q_seq=1 전용 우연 일치 의존
```

---

# 4. Exact Invocation Identity Transaction

## 4.1 목적

수치 비교 전에 두 context가 같은 attention invocation에서 생성됐다는 사실을 증명한다.

Identity mismatch는 numerical mismatch가 아니다. Identity mismatch가 발생하면 comparator dispatch 자체를 금지한다.

## 4.2 필수 identity fields

```text
patch_id
build_revision
model_instance_id
model_instance_epoch
decode_session_id
decode_session_epoch
layer_index
invocation_ordinal
decode_step
route_id
authority_pointer_generation
authority_pointer_digest

Q generation
Q exact element offset
Q exact element count
Q range fingerprint

K generation
K exact element offset
K exact element count
K range fingerprint

V generation
V exact element offset
V exact element count
V range fingerprint

partition_generation
partition_digest
canonical_chunk_order_digest

causal_enabled
causal_snapshot_digest
additional_mask_kind
additional_mask_digest
combined_mask_snapshot_digest

batch
q_seq
seq_kv
query_head_count
kv_head_count
gqa_group_size
head_dim
context_element_count

semantic_context_abi
headwise_physical_context_abi
tensorcube_physical_context_abi

device_identity_digest
queue_lineage_digest
production_authority_snapshot_digest
```

## 4.3 Transaction gate

다음 중 하나라도 불일치하면 FAIL하고 GPU numerical compare를 실행하지 않는다.

```text
model/session/layer/step
route/authority generation
Q/K/V generation or range
partition generation/digest/order
causal or additional-mask snapshot
geometry
semantic ABI
physical ABI declaration
device/queue lineage
production authority snapshot
```

---

# 5. Headwise Pre-Output-Projection Context Capture

## 5.1 authoritative capture point

Headwise oracle은 계산 중간 candidate가 아니다.

다음 조건을 통과해 실제 downstream으로 전달되는 context handle을 캡처한다.

```text
Headwise kernel completion
→ finite guard approval
→ production authority validation
→ downstream_output selection
→ output projection 직전
```

즉 W8 oracle은 `candidate_output`이 아니라 guard와 authority 검사를 통과한 `downstream_output`이다.

## 5.2 capture handle

```text
HeadwisePreOutputProjectionContextHandle
```

필수 보유 정보:

```text
Arc<BackendBuffer>
logical byte offset
logical byte length
batch/q_seq/query_heads/head_dim
physical ABI id
invocation identity digest
authority snapshot digest
submission serial
completion ticket
owner token
capture digest
```

## 5.3 금지

```text
context 전체 readback
새 context buffer 복사
production output mutation
Headwise writer lifetime 단축
비교 완료 전 owner release
```

---

# 6. W7 TensorCube Context Candidate Adoption

## 6.1 W7 handoff 확장

W8은 W7의 다음 device-local handle을 채택한다.

```text
TensorCubeStage12ContextCandidateHandle
TensorCubeStage12ContextRowClassificationHandle
```

Context candidate handle 필수 정보:

```text
Arc<BackendBuffer>
logical byte offset/length
context element count
BQHD physical ABI
partition generation/digest
canonical chunk order digest
W7 invocation identity digest
submission completion ticket
owner token
handoff digest
```

Row classification handle 필수 정보:

```text
row count
active/all-masked flags
GQA mapping evidence
causal boundary evidence
submission completion ticket
owner token
```

## 6.2 W7 authority 유지

```text
output_commit_authorized = false
production_writer = HeadwiseFullActive
```

W8 adoption은 계산 결과를 비교 대상으로 채택하는 것이며 production adoption이 아니다.

---

# 7. Device-Local Candidate·Oracle Comparison

## 7.1 GPU inputs

```text
binding 0  Headwise downstream context buffer
binding 1  TensorCube Stage12 context buffer
binding 2  Stage12 row classification buffer
binding 3  compare params uniform
binding 4  compact status buffer
```

## 7.2 compare pass

각 semantic scalar에 대해:

```text
semantic [b,q,h,d]
→ headwise physical index BHQD
→ tensorcube physical index BQHD
→ mapped KV head = h / gqa_group_size
→ row flags read
→ finite check
→ all-masked exact-zero check
→ abs/relative error check
→ atomic counters
→ atomicMin(first_mismatch_semantic_index)
```

## 7.3 tolerance

기본값:

```text
absolute_tolerance = 2.0e-4
relative_tolerance = 2.0e-3
relative_floor     = 1.0e-4
```

판정:

```text
abs_error <= abs_tol
or
abs_error / max(abs(headwise), abs(tensorcube), relative_floor) <= rel_tol
```

All-masked row는 tolerance가 아니라 exact zero를 요구한다.

## 7.4 first mismatch determinism

Compare pass는 detail payload를 여러 thread가 직접 덮어쓰지 않는다.

```text
pass 1
atomicMin(first semantic scalar index)

pass 2
single finalize dispatch
→ semantic coordinate
→ physical indices
→ mapped KV head
→ row flags
→ value bits
```

이 구조로 first mismatch receipt의 결정성을 봉인한다.

---

# 8. Compact Status ABI

## 8.1 ABI

```text
32 words
128 bytes
```

## 8.2 필수 필드

```text
compared_scalar_count
mismatch_count
headwise_non_finite_count
tensorcube_non_finite_count
headwise_all_masked_nonzero_count
tensorcube_all_masked_nonzero_count
max_absolute_error_bits
max_relative_error_bits
first_mismatch_semantic_index
first_mismatch_batch
first_mismatch_query_token
first_mismatch_query_head
first_mismatch_dimension
first_mismatch_mapped_kv_head
first_mismatch_row_flags
first_mismatch_headwise_physical_index
first_mismatch_tensorcube_physical_index
first_mismatch_headwise_value_bits
first_mismatch_tensorcube_value_bits
layout_guard_violation_count
buffer_bounds_violation_count
gqa_mapping_violation_count
causal_snapshot_violation_count
mask_snapshot_violation_count
compare_dispatch_count
finalize_dispatch_count
queue_submit_count
compact_status_readback_count
full_context_readback_count
context_materialization_copy_count
completion_observed
pass_flag
```

## 8.3 Readback seal

```text
Headwise context payload readback      0
TensorCube context payload readback    0
full context materialization copy      0
compact status readback                1
compact status readback bytes          128
```

---

# 9. All-Masked Exact-Zero Preservation

## 9.1 row classification

Stage12 row classification은 다음을 구분한다.

```text
ACTIVE
ALL_MASKED
```

ALL_MASKED row의 조건:

```text
global max = -inf
denominator = 0
weighted numerator = 0
normalized context = exact +0.0
```

## 9.2 W8 gate

ALL_MASKED row에서 어느 쪽이든 nonzero, NaN, ±inf이면 FAIL한다.

```text
headwise_all_masked_nonzero_count = 0
tensorcube_all_masked_nonzero_count = 0
```

---

# 10. Causal Boundary Preservation

W8 identity는 causal snapshot digest를 W7 identity와 Headwise capture 양쪽에 결합한다.

검증 대상:

```text
last valid key boundary
future-key exclusion
all-masked synthetic row
q_seq > 1 query-token별 causal boundary
```

Causal snapshot digest가 다르면 comparator를 실행하지 않는다.

---

# 11. GQA Head Mapping Preservation

현재 profile:

```text
query_head_count = 32
kv_head_count    = 4
gqa_group_size   = 8
mapped_kv_head   = query_head / 8
```

W8은 first mismatch receipt에 mapped KV head를 기록한다.

P3 sentinel은 KV head별로 구분되는 V band를 사용하여 잘못된 query-head→KV-head mapping을 검출한다.

```text
GQA mapping violation count = 0
```

---

# 12. Submission-Fenced Dual Handle Lifetime

## 12.1 owner graph

```text
Headwise production owner
TensorCube W7 owner
W8 compare owner
```

W8 compare submission 완료 전에는 Headwise와 TensorCube handle을 해제할 수 없다.

## 12.2 terminal drain

```text
compare completion observed
→ compact status readback 완료
→ Headwise W8 owner release
→ TensorCube row-classification owner release
→ TensorCube context owner release
```

필수 receipt:

```text
dual_handle_terminal_drain_observed = true
stale_handle_passage_count = 0
premature_release_count = 0
```

---

# 13. Physical Scenarios

W8 자체 완료에 필요한 최소 scenario는 다음 네 개다.

## P0 Live continuity

```text
q_seq = 1
seq_kv = 384
실제 W4→W7 live path
Headwise downstream context vs W7 Stage12 context
```

## P1 Layout sentinel

```text
q_seq = 2
seq_kv = 16
BHQD와 BQHD flatten 순서 차이를 강제
semantic-coordinate compare 검증
```

## P2 All-masked sentinel

```text
synthetic all-masked row
Headwise exact zero
TensorCube exact zero
```

## P3 GQA sentinel

```text
KV-head-distinct V bands
32 query heads / 4 KV heads
query_head / 8 mapping 검증
```

## N0 Negative control

```text
known semantic scalar 하나를 의도적으로 변형
mismatch_count = 1
first_mismatch_semantic_index = expected
```

Comparator가 무조건 PASS하는 죽은 기관이 아님을 증명한다.

넓은 shape/length/layer matrix는 W8A로 분리한다.

---

# 14. Rust Runtime Surface

## 14.1 backend

```text
crates/burn_webgpu_backend/src/
  attention_interconnect_w8_context_parity.rs
  headwise_atlas.rs
  tensorcube_stage12_weighted_value_accumulation.rs

crates/burn_webgpu_backend/src/shaders/
  attention_interconnect_w8_context_compare.wgsl
  attention_interconnect_w8_first_mismatch_finalize.wgsl
```

## 14.2 model core

```text
crates/model_core/src/
  attention_interconnect_w8.rs
  attention_interconnect_w7.rs
```

## 14.3 orchestrator

```text
crates/orchestrator_local/src/
  attention_interconnect_w8_cli_registry.rs
  attention_interconnect_w8_artifact_wave_map.rs

crates/orchestrator_local/src/bin/
  ash_attn_interconnect_w8_verification_gate.rs
  ash_attn_interconnect_w8_physical_gate.rs
```

## 14.4 CLI

```text
specs/cli/
  ash_attn_interconnect_w8_verification.args
  ash_attn_interconnect_w8_physical.args
```

---

# 15. Verification Gate

Verification gate는 다음을 검사한다.

```text
source path 존재
W7 parent artifact digest
W8 source digest map
WGSL reserved identifier admission
WGSL binding contract
status ABI 32 words / 128 bytes
BHQD↔BQHD semantic mapping marker
identity mismatch fail-closed marker
no full context readback marker
no context materialization marker
no output commit marker
no Decode route mutation marker
no writer promotion marker
P0/P1/P2/P3 scenario declaration
N0 negative control declaration
```

Verification gate는 Rust가 다음을 산출한다.

```text
runtime specification JSON
canonical verification runtime artifact JSON
canonical verification local manifest JSON
```

정적 파일로 패키지에 포함하지 않는다.

---

# 16. Physical Gate

Physical gate는 다음 순서로 실행한다.

```text
parent artifact admission
→ 실제 W4→W7 P0 재실행
→ Headwise downstream context capture
→ W7 candidate/row-classification handoff
→ exact invocation identity bind
→ device-local comparator
→ P1 layout sentinel
→ P2 all-masked sentinel
→ P3 GQA sentinel
→ N0 known mismatch negative control
→ compact receipt readback
→ dual handle terminal drain
→ source Q/K/V fingerprint recheck
→ authority snapshot recheck
```

Physical gate는 Rust가 다음을 산출한다.

```text
runtime specification JSON
scenario receipts
canonical physical runtime artifact JSON
canonical physical local manifest JSON
```

---

# 17. Runtime Artifact Required Fields

```text
schemaVersion
schema
patchId
buildRevision
parentW7ArtifactDigest
parentW7ManifestDigest
sourceDigests
shaderDigests
pipelineIdentity
invocationIdentityDigest
exactInvocationTransactionDigest
Headwise capture digest
W7 handoff digest
P0 receipt
P1 receipt
P2 receipt
P3 receipt
N0 receipt
qkv lineage bound
partition lineage bound
causal snapshot bound
mask snapshot bound
canonical ABI bound
context payload readback count
context materialization count
compact readback bytes
decode route mutation count
writer promotion count
TensorCube output commit count
dual handle terminal drain
source fingerprint before/after
production authority before/after
passToken
pass
```

---

# 18. 완료 게이트

```text
parent W7 physical artifact admission       PASS
exact invocation identity transaction       PASS
Q/K/V generation lineage                    PASS
partition lineage                           PASS
causal snapshot binding                     PASS
additional mask snapshot binding            PASS
Headwise downstream context live            PASS
TensorCube context candidate live            PASS
canonical semantic context ABI              PASS
P0 live context parity                      PASS
P1 BHQD↔BQHD layout sentinel                PASS
P2 all-masked exact-zero                    PASS
P3 GQA mapping sentinel                     PASS
N0 first-mismatch negative control          PASS
source Q/K/V mutation count                 0
full context readback count                 0
context materialization copy count          0
compact readback bytes                      128
decode route mutation count                 0
production writer promotion count           0
TensorCube output commit count               0
dual handle terminal drain                  PASS
production writer after W8                  HeadwiseFullActive
```

---

# 19. PASS Token

```text
PASS_ASH_ATTN_INTERCONNECT_W8_W7_TENSORCUBE_CONTEXT_CANDIDATE_ADOPTION_HEADWISE_PRE_OUTPUT_PROJECTION_CONTEXT_CAPTURE_EXACT_INVOCATION_IDENTITY_QKV_PARTITION_LINEAGE_CAUSAL_MASK_SNAPSHOT_CANONICAL_CONTEXT_ABI_DEVICE_LOCAL_PARITY_COMPACT_FIRST_MISMATCH_ALL_MASKED_ZERO_CAUSAL_GQA_DUAL_HANDLE_LIFETIME_NO_FULL_CONTEXT_READBACK_NO_DECODE_ROUTE_MUTATION_NO_WRITER_PROMOTION_SEALED
```

---

# 20. W8 이후 경계

W8 PASS가 의미하는 것:

```text
동일 실제 attention invocation에서
Headwise가 downstream으로 전달한 pre-output-projection context와
TensorCube Stage12 context candidate가
identity·ABI·mask·causal·GQA 의미와 수치에서 parity를 통과했다.
```

W8 PASS가 의미하지 않는 것:

```text
TensorCube가 DecodeState writer가 됐다
TensorCube가 output projection을 구동한다
logits가 TensorCube 경로를 사용한다
모든 shape/layer/device matrix가 통과했다
```

다음 패치:

```text
ASH-ATTN-INTERCONNECT-W8A
Dynamic Shape·Boundary·Multi-Layer Physical Matrix
```
