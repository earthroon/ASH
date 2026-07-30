# ASH-ATTN-INTERCONNECT-W2 명세

## Lease Provenance /
## Model·Layer·Decode-Step Identity /
## Buffer Identity·Offset·Length /
## Device·Queue Lineage /
## Generation Domain Separation /
## Freshness Epoch /
## Stale·Cross-Layer·Cross-Model Rejection Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W2`  
> Build revision: `W2-lease-provenance-generation-domain-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W0-R2` PASS + `ASH-ATTN-INTERCONNECT-W1-R1` PASS  
> Parent W1 summary: shape authority `model_spec_plus_runtime_dims`, q_seq=1 admitted, dynamic KV admitted  
> production attention output authority: `Headwise` 유지  
> TensorCube role: `ShadowObserverOnly` 유지  
> TensorCube live Q/K dispatch: 아직 금지  
> 후속 패치: `W3 Reusable Stage10 Runtime Executor`, `W4 Headwise Live Q/K Shadow Tap`

---

# 0. 목적

W0는 Headwise와 TensorCube Stage10의 권위를 동일 모델 인스턴스에 결속했다.

W1은 다음 shape authority를 확정했다.

```text
static geometry            bound ModelSpec.dimensions
dynamic geometry           actual Q/K/V dimensions
position geometry          causal position snapshot
kernel profile             16x16 / subgroup32 / head_dim64
dynamic KV blocks          ceil_div(kv_seq, 16)
q_seq=1                    active row 1 + inactive row 15
```

그러나 현재 `RawWgpuBufferLease`와 `ActiveTensorRawHandle`은 다음만 보유한다.

```text
label
shape
len_elements
len_bytes
bytes_per_element
Arc<BackendBuffer>
BridgeMode
ActiveTensorRawHandle
buffer_offset
buffer_size
primitive_id, optional
stream_id, optional
seam_id
vendor_access_path
```

현재 lease 자체에는 다음이 없다.

```text
model_instance_id
model_instance_binding_digest
decode_session_id
decode_session_contract_digest
layer_index
decode_step_ordinal
attention phase
causal position snapshot digest
shape reconciliation digest
dispatch plan digest
runtime device identity
runtime queue identity
KV cache generation
attention invocation generation
lease capture generation
freshness state
consumer lifetime
```

따라서 현재 lease는 메모리 수명은 `Arc<BackendBuffer>`로 유지할 수 있어도, 의미상 최신 Q/K인지, 같은 모델·레이어·스텝인지, 같은 runtime device·queue에서 생성된 것인지 증명하지 못한다.

W2의 목적은 다음과 같다.

```text
1. attention invocation의 identity를 모델·세션·레이어·스텝 단위로 확정한다.
2. Q/K raw lease를 기존 RawWgpuBufferLease와 분리된 provenance wrapper에 결속한다.
3. buffer identity·offset·size·logical length를 정확히 봉인한다.
4. device·queue lineage는 live Arc pointer equality를 최종 권위로 사용한다.
5. 서로 다른 generation domain을 이름과 타입으로 분리한다.
6. lease freshness를 attention invocation lifetime에 제한한다.
7. stale·cross-model·cross-session·cross-layer·cross-step lease를 fail-closed로 거부한다.
```

---

# 1. W2 패치 경계

W2는 provenance 계약과 검증기를 만든다.

W2에서 허용되는 것:

```text
AttentionInvocationIdentity 생성
ModelSpec / model binding / decode session binding 검증
layer_index / layer_count 검증
decode_step_ordinal 명시적 전달
RawWgpuBufferLease metadata 관찰
ActiveTensorRawHandle consistency 검증
process-local buffer identity 계산
runtime device/queue lineage snapshot 생성
provenance wrapper 생성
synthetic / validation fixture provenance gate
stale / cross-domain negative control
```

W2에서 금지되는 것:

```text
Headwise hot path에서 실제 Q/K lease capture
TensorCube Stage9/10 live dispatch
TensorCube output commit
TensorCube KV read/write
Headwise output 변경
Headwise route mutation
TensorCube stage pointer mutation
blocking map_async
device.poll(Wait)
payload readback
host upload fallback admission
```

W2 PASS는 W4 live tap의 입장권이다. W2 자체가 live tap은 아니다.

---

# 2. 현재 구현에서 확인된 사실

## 2.1 RawWgpuBufferLease

현재 구조:

```rust
pub struct RawWgpuBufferLease {
    pub label: String,
    pub shape: Vec<usize>,
    pub len_elements: usize,
    pub len_bytes: u64,
    pub bytes_per_element: usize,
    pub buffer: Arc<BackendBuffer>,
    pub mode: BridgeMode,
    pub active_handle: ActiveTensorRawHandle,
    pub buffer_offset: u64,
    pub buffer_size: u64,
}
```

판단:

```text
memory ownership           있음, Arc<BackendBuffer>
shape/range metadata       있음
primitive/stream metadata  active_handle에 optional
model/layer/step identity   없음
device/queue identity       없음
generation/freshness        없음
```

## 2.2 ActiveTensorRawHandle

현재 live raw path는 다음을 제공할 수 있다.

```text
mode = RawBorrowed
state = BorrowedBuffer
primitive_id = Some(...)
stream_id = Some(...)
buffer = Some(Arc<BackendBuffer>)
buffer_offset
buffer_size
vendor_access_path
seam_id
```

Host upload path는 다음이다.

```text
mode = UploadedFromHost
state = MetadataOnly
primitive_id = None
stream_id = None
buffer = None
vendor_access_path = host_upload:fallback
```

W2 attention lease admission은 host upload path를 허용하지 않는다.

## 2.3 NativeWgpuRuntimeHandles

현재 구조:

```rust
pub struct NativeWgpuRuntimeHandles {
    pub device: Arc<RuntimeWgpuDevice>,
    pub queue: Arc<RuntimeWgpuQueue>,
    pub source: &'static str,
}
```

현재 Headwise dispatcher의 same runtime 검증은 다음이 SSOT다.

```rust
Arc::ptr_eq(dispatcher_device, runtime_handles.device)
Arc::ptr_eq(dispatcher_queue, runtime_handles.queue)
```

따라서 W2에서 live same-device / same-queue의 최종 판정 권위는 digest 문자열이 아니라 `Arc::ptr_eq`다.

## 2.4 Attention callsite

현재 `try_grouped_query_attention_via_atlas`는 다음을 받는다.

```text
Q tensor
K tensor
V tensor
heads
kv_heads
head_dim
causal_position
```

현재 인자에 없는 것:

```text
layer_index
decode_step_ordinal
model_instance_id
decode_session_contract_digest
KV cache generation
attention invocation generation
```

그러나 호출부에는 다음 정보가 존재한다.

```text
forward_block_prefill(layer_idx, ...)
forward_block_decode(layer_idx, ...)
DecodeState.generated.len()
KvPositionLifecycle.decode_session_id
KvPositionLifecycle.position_epoch
KvPositionLifecycle.committed_past_len
```

W2는 이 정보를 암묵적으로 추론하지 않고 명시적 invocation identity로 전달한다.

---

# 3. SSOT 구조

W2의 권위 순서:

```text
VerifiedModelInstanceBinding
  -> BoundDecodeSessionContract
  -> AttentionModelShapeAuthoritySnapshot
  -> AttentionRuntimeShapeReconciliationReceipt
  -> AttentionInvocationIdentity
  -> RuntimeDeviceQueueLineageSnapshot
  -> RawWgpuBufferLease metadata
  -> AttentionLeaseProvenance
  -> ProvenancedAttentionLease
  -> AttentionLeasePairReceipt
```

후단이 전단을 덮어쓸 수 없다.

다음은 금지한다.

```text
lease label에서 layer index 추출
q_position_base에서 decode step 추론
kv_seq에서 KV generation 추론
buffer pointer에서 model instance 추론
stream_id에서 decode session 추론
TensorCube stage generation과 decode generation 숫자 비교
candidate nonce와 lease capture generation 숫자 비교
```

---

# 4. 신규 타입

## 4.1 AttentionInvocationPhase

```rust
pub enum AttentionInvocationPhase {
    Prefill,
    IncrementalDecode,
    ChunkedDecode,
}
```

Canonical 문자열:

```text
prefill
incremental_decode
chunked_decode
```

## 4.2 AttentionInvocationIdentity

Schema:

```text
ash.attn.interconnect.w2.invocation-identity.v1
```

필드:

```text
schema
patch_id
build_revision
model_instance_id
model_instance_binding_digest
effective_runtime_binding_digest
decode_session_id
decode_session_contract_digest
request_id
session_epoch
position_epoch
phase
route_id
layer_index
layer_count
decode_step_ordinal, optional for prefill
prefill_invocation_ordinal, optional for decode
q_position_base
kv_position_base
seq_q
seq_kv
causal_position_snapshot_digest
shape_reconciliation_digest
dispatch_plan_digest
attention_invocation_generation
invocation_open
invocation_digest
```

Canonical rules:

```text
model identity exact
decode session identity exact
0 <= layer_index < layer_count
layer_count == bound ModelSpec.num_layers
phase and route_id exact
causal position fields exact
shape reconciliation model_instance exact
dispatch plan model_instance exact
attention_invocation_generation > 0
invocation_open == true during capture and validation
```

### Prefill

```text
phase                     prefill
route_id                  full_prefill
decode_step_ordinal       None
prefill_invocation_ordinal Some(0)
seq_q == seq_kv
q_position_base == kv_position_base
```

### Incremental decode

```text
phase                     incremental_decode
route_id                  incremental_decode
decode_step_ordinal       Some(explicit value)
prefill_invocation_ordinal None
seq_q == 1
q_position_base == kv_position_base + seq_kv - 1
```

### Chunked decode

```text
phase                     chunked_decode
route_id                  chunked_decode
decode_step_ordinal       Some(explicit value)
2 <= seq_q < seq_kv
```

`decode_step_ordinal`은 `q_position_base`, `past_len`, `kv_seq`에서 역추론하지 않는다.

권위 값은 `DecodeState`가 forward 호출 직전에 가진 explicit step ordinal이다.

현재 greedy / sampled decode 경로에서 사용 가능한 값:

```text
state.generated.len()
live_generated_count_before_forward
```

구현 시 하나의 명명으로 정규화한다.

```text
decode_step_ordinal = generated_count_before_forward
```

이 값이 prompt absolute position과 같다고 가정하지 않는다.

## 4.3 AttentionTensorRole

```rust
pub enum AttentionTensorRole {
    Query,
    Key,
}
```

W2에서는 V provenance를 정의할 수 있지만 admission 대상은 Q/K만이다.

```text
Query role -> Q shape authority
Key role   -> K shape authority
Value role -> W2 admission 금지, W4 이후 별도 확장
```

## 4.4 RuntimeDeviceQueueLineageSnapshot

Schema:

```text
ash.attn.interconnect.w2.runtime-device-queue-lineage.v1
```

필드:

```text
schema
runtime_source
runtime_process_epoch
runtime_handle_generation
device_identity_opaque
queue_identity_opaque
device_arc_strong_count_observed
queue_arc_strong_count_observed
same_dispatcher_device
same_dispatcher_queue
same_bridge_device
same_bridge_queue
lineage_digest
```

권위 규칙:

```text
same_dispatcher_device = Arc::ptr_eq(dispatcher.device, runtime_handles.device)
same_dispatcher_queue  = Arc::ptr_eq(dispatcher.queue, runtime_handles.queue)
same_bridge_device     = bridge가 같은 handles에서 생성됨
same_bridge_queue      = bridge가 같은 handles에서 생성됨
```

`device_identity_opaque`와 `queue_identity_opaque`는 process-local debug identity다.

구현 권장:

```text
opaque = sha256(runtime_process_epoch || pointer_address || role)
```

다음 주장은 금지한다.

```text
opaque identity가 프로세스 재시작 후에도 동일하다.
opaque identity가 adapter PCI identity다.
queue identity가 물리 GPU identity다.
R15 physical_device_digest와 live Arc identity가 동일 의미다.
```

R15 `physical_device_digest`는 선행 audit artifact 증거다. W2 live pointer equality의 대체물이 아니다.

## 4.5 AttentionBufferRangeIdentity

Schema:

```text
ash.attn.interconnect.w2.buffer-range-identity.v1
```

필드:

```text
buffer_identity_opaque
buffer_offset
buffer_size
logical_len_elements
logical_len_bytes
bytes_per_element
range_end_exclusive
shape
shape_element_product
range_digest
```

Canonical 검증:

```text
logical_len_elements == product(shape)
logical_len_bytes == logical_len_elements * bytes_per_element
bytes_per_element == 4
buffer_size >= logical_len_bytes
range_end_exclusive == buffer_offset + buffer_size, checked
buffer_size > 0
logical_len_bytes > 0
```

`buffer_identity_opaque`는 `Arc::as_ptr(&lease.buffer)`에서 process-local opaque identity를 만든다.

## 4.6 ActiveHandleConsistencyReceipt

Schema:

```text
ash.attn.interconnect.w2.active-handle-consistency.v1
```

검증:

```text
lease.mode == RawBorrowed
active_handle.mode == RawBorrowed
active_handle.state == BorrowedBuffer
active_handle.buffer.is_some
Arc::ptr_eq(lease.buffer, active_handle.buffer)
lease.shape == active_handle.shape
lease.len_elements == active_handle.len_elements
lease.len_bytes == active_handle.len_bytes
lease.bytes_per_element == active_handle.bytes_per_element
lease.buffer_offset == active_handle.buffer_offset
lease.buffer_size == active_handle.buffer_size
primitive_id non-empty
stream_id non-empty
vendor_access_path not host_upload:fallback
seam_id non-empty
```

## 4.7 AttentionLeaseGenerationDomains

Schema:

```text
ash.attn.interconnect.w2.generation-domains.v1
```

필드:

```text
model_instance_epoch
decode_session_epoch
position_epoch
kv_cache_generation
attention_invocation_generation
lease_capture_generation
headwise_candidate_nonce, optional
tensorcube_stage_generation
headwise_route_authority_digest
tensorcube_stage_authority_digest
generation_domain_digest
```

각 필드의 의미:

```text
model_instance_epoch
  source: VerifiedModelInstanceBinding.model_instance_epoch
  scope: model construction

decode_session_epoch
  source: BoundDecodeSessionContract.session_epoch
  scope: decode session

position_epoch
  source: HeadwiseCausalPositionSnapshot.position_epoch
  scope: absolute position domain

kv_cache_generation
  source: new KvPositionLifecycle.content_generation
  scope: successful KV cache commit count

attention_invocation_generation
  source: NativeWgpuModel-owned monotonic counter
  scope: one attention invocation

lease_capture_generation
  source: invocation-local monotonic counter
  scope: Q/K lease capture order

headwise_candidate_nonce
  source: existing headwise_candidate_nonce
  scope: production candidate only
  W2 planner-only path: None

tensorcube_stage_generation
  source: W0 TensorCube authority generation_after
  current exact: 44

headwise_route_authority_digest
  source: W0 Headwise authority snapshot digest
  type: digest, not numeric generation

tensorcube_stage_authority_digest
  source: W0 TensorCube authority snapshot digest
  type: digest
```

중요:

```text
서로 다른 generation domain의 숫자 equality를 요구하지 않는다.
```

금지 예:

```text
model_instance_epoch == session_epoch
session_epoch == position_epoch
kv_cache_generation == decode_step_ordinal
attention_invocation_generation == candidate_nonce
lease_capture_generation == tensorcube_stage_generation
```

현재 Headwise route에는 canonical numeric generation counter가 없다.

따라서 W2는 `headwise_route_generation` 숫자를 꾸며내지 않는다.

Headwise route revision authority는 digest로 표현한다.

```text
headwise_route_authority_digest
```

현재 Burn raw resource에도 allocator storage generation이 노출되지 않는다.

따라서 W2는 물리 storage generation을 주장하지 않는다.

재사용 방지는 다음으로 봉인한다.

```text
buffer identity + range
attention invocation generation
lease capture generation
freshness epoch
```

## 4.8 AttentionLeaseFreshnessEpoch

Schema:

```text
ash.attn.interconnect.w2.freshness-epoch.v1
```

필드:

```text
model_instance_id
decode_session_id
layer_index
decode_step_ordinal
position_epoch
kv_cache_generation
attention_invocation_generation
lease_capture_generation
opened_at_invocation_generation
valid_through_invocation_generation
invocation_open
consumed
freshness_digest
```

Canonical lifetime:

```text
opened_at_invocation_generation == attention_invocation_generation
valid_through_invocation_generation == attention_invocation_generation
invocation_open == true at admission
consumed == false before first consumer
```

한 lease는 다음 scope를 벗어날 수 없다.

```text
owner_scope                 attention_invocation
maximum_consumer_scope      tensorcube_shadow_dispatch
maximum_input_lease_scope   attention_invocation
may_escape_decode_step      false
may_escape_attention_call   false
may_be_stored_in_route_snapshot false
may_be_stored_in_registry   false
may_be_sent_to_background_task false
```

`Arc<BackendBuffer>`가 살아 있어도 freshness가 만료되면 stale이다.

메모리 생존과 의미상 최신성은 다른 계약이다.

## 4.9 AttentionLeaseProvenance

Schema:

```text
ash.attn.interconnect.w2.lease-provenance.v1
```

필드:

```text
schema
patch_id
build_revision
role
model_instance_id
model_instance_binding_digest
effective_runtime_binding_digest
decode_session_id
decode_session_contract_digest
request_id
layer_index
layer_count
decode_step_ordinal
phase
route_id
causal_position_snapshot_digest
shape_reconciliation_digest
dispatch_plan_digest
primitive_id
stream_id
seam_id
vendor_access_path
buffer_range_identity
runtime_lineage
lease_generations
freshness_epoch
active_handle_consistency_digest
provenance_digest
pass
failures
```

## 4.10 ProvenancedAttentionLease

Rust wrapper:

```rust
pub struct ProvenancedAttentionLease {
    pub lease: RawWgpuBufferLease,
    pub provenance: AttentionLeaseProvenance,
}
```

기존 `RawWgpuBufferLease` 구조를 직접 확장하지 않는다.

이유:

```text
기존 생성자 수가 많음
scratch/output lease까지 동일 provenance를 강제하면 의미 오염
W2 Q/K attention seam에만 엄격 계약 필요
기존 API binary/source churn 최소화
```

Wrapper 생성은 validation을 통과한 뒤에만 가능하다.

```text
ProvenancedAttentionLease::try_new(...)
```

unchecked constructor는 금지한다.

## 4.11 AttentionLeasePairReceipt

Schema:

```text
ash.attn.interconnect.w2.qk-lease-pair.v1
```

필드:

```text
model_instance_id
decode_session_id
layer_index
decode_step_ordinal
attention_invocation_generation
q_provenance_digest
k_provenance_digest
same_model
same_session
same_layer
same_step
same_position_epoch
same_kv_generation
same_invocation_generation
same_device
same_queue
same_stream
roles_exact
shapes_match_w1
ranges_non_overlapping_or_distinct
pair_digest
pass
failures
```

---

# 5. Invocation identity 전달

## 5.1 Prefill path

현재 call chain:

```text
forward_prefill
  -> for layer_idx
  -> forward_block_prefill(layer_idx, ...)
  -> try_grouped_query_attention_via_atlas(...)
```

W2 변경:

```text
forward_prefill
  -> build AttentionInvocationIdentity per layer
  -> forward_block_prefill(..., &invocation_identity)
  -> try_grouped_query_attention_via_atlas(..., &invocation_identity)
```

Prefill identity:

```text
layer_index                 loop layer_idx
layer_count                 spec.dimensions.num_layers
phase                       prefill
decode_step_ordinal         None
prefill_invocation_ordinal  Some(0)
position epoch              KV lifecycle position_epoch
KV generation               prefill stage-before-commit generation
```

## 5.2 Decode path

현재 call chain:

```text
DecodeState::decode_step*
  -> forward_last_logits_single_token
  -> for layer_idx
  -> forward_block_decode(layer_idx, ...)
  -> try_grouped_query_attention_via_atlas(...)
```

W2 변경:

```text
DecodeState::decode_step*
  -> capture explicit decode_step_ordinal
  -> forward_last_logits_single_token(..., decode_step_ordinal)
  -> build AttentionInvocationIdentity per layer
  -> forward_block_decode(..., &invocation_identity)
  -> try_grouped_query_attention_via_atlas(..., &invocation_identity)
```

Canonical source:

```text
decode_step_ordinal = state.generated.len() before forward
```

모든 greedy / sampled / legacy decode callsite는 같은 source를 사용해야 한다.

다음은 금지한다.

```text
한 callsite만 ordinal 전달
sampled path에서 past_len 사용
greedy path에서 generated.len 사용
position base로 ordinal 대체
누락 시 0 fallback
```

## 5.3 Layer identity

```text
layer_index = enumerate index
layer_count = bound ModelSpec.dimensions.num_layers
```

검증:

```text
layer_index < layer_count
actual decode_layers().len() == layer_count
invocation layer_index == callsite layer_idx
Q/K provenance layer_index == invocation layer_index
```

label의 `layer_12` 문자열은 증거가 아니다.

---

# 6. KV cache generation

현재 `KvPositionLifecycle`은 다음을 가진다.

```text
decode_session_id
model_instance_id
position_epoch
absolute_position_base
committed_past_len
staged_append_len
next_write_position
```

W2는 다음 메타데이터를 추가한다.

```text
content_generation: u64
staged_generation: Option<u64>
last_committed_decode_step: Option<usize>
```

초기화:

```text
content_generation = 0
staged_generation = None
last_committed_decode_step = None
```

Stage:

```text
staged_generation = Some(content_generation + 1)
```

Commit 성공:

```text
content_generation = staged_generation
staged_generation = None
last_committed_decode_step = explicit step ordinal, decode only
```

Commit 실패:

```text
content_generation unchanged
staged_generation cleared or transaction rolled back
partial generation publish 0
```

Prefill의 모든 layer Q/K provenance는 동일 prefill transaction KV generation을 사용한다.

Incremental decode의 모든 layer Q/K provenance는 동일 decode-step transaction KV generation을 사용한다.

레이어마다 KV generation을 증가시키지 않는다.

```text
1 decode transaction = 1 KV cache generation
```

---

# 7. Attention invocation generation

`NativeWgpuModel`에 다음 owner를 둔다.

```text
attention_invocation_generation: AtomicU64
```

증가 시점:

```text
각 layer attention invocation 직전 fetch_add(1)
```

특성:

```text
process-local
model-instance-local
monotonic
0 reserved
wraparound fail-closed
```

Invocation generation은 다음과 다르다.

```text
decode step
layer index
candidate nonce
KV generation
TensorCube stage generation
```

한 decode step에 N layer가 있으면 invocation generation은 N번 증가한다.

---

# 8. Lease capture generation

한 invocation 안에서 lease capture 순서를 명시한다.

Canonical W4 예정 순서:

```text
Query capture generation = 1
Key capture generation   = 2
```

W2 validator는 다음을 요구한다.

```text
q.lease_capture_generation == 1
k.lease_capture_generation == 2
same attention_invocation_generation
```

capture generation은 buffer allocation generation이 아니다.

---

# 9. Buffer identity와 range

## 9.1 Buffer identity

Live process에서 authoritative comparison:

```rust
Arc::ptr_eq(&q.lease.buffer, &k.lease.buffer)
```

Receipt에는 raw address 대신 opaque digest를 기록한다.

같은 underlying buffer가 허용되는 경우:

```text
ranges do not overlap
primitive IDs differ
roles differ
logical lengths exact
```

다른 underlying buffer도 허용한다.

## 9.2 Range overlap

```text
q_start = q.buffer_offset
q_end   = q.buffer_offset + q.buffer_size
k_start = k.buffer_offset
k_end   = k.buffer_offset + k.buffer_size
```

같은 buffer identity일 때:

```text
non_overlap = q_end <= k_start || k_end <= q_start
```

Q/K는 서로 다른 logical tensor이므로 overlap은 reject한다.

Exact alias도 reject한다.

## 9.3 Logical length

```text
len_elements = product(shape)
len_bytes = len_elements * bytes_per_element
buffer_size >= len_bytes
```

`buffer_size`가 allocator slice size이고 `len_bytes`가 logical payload length일 수 있으므로 exact equality는 요구하지 않는다.

다만 logical payload가 slice를 초과하면 reject한다.

## 9.4 Offset alignment

현재 f32 storage path 최소 요구:

```text
buffer_offset % 4 == 0
buffer_size % 4 == 0
```

W4 bind group의 device storage offset alignment 요구는 W3/W4 runtime executor에서 추가 검증한다.

W2가 device limit을 추측해 하드코딩하지 않는다.

---

# 10. Device·Queue lineage

## 10.1 Authority

Live admission의 최종 authority:

```text
runtime_handles.device Arc pointer identity
runtime_handles.queue Arc pointer identity
HeadwiseAtlasDispatcher::uses_runtime_handles
BurnToRawWgpuBridge created from same runtime handles
```

Receipt digest는 증거 직렬화다. pointer equality를 대체하지 않는다.

## 10.2 Cross-device rejection

다음 중 하나면 reject한다.

```text
dispatcher device pointer mismatch
bridge device pointer mismatch
lease provenance device opaque identity mismatch
runtime process epoch mismatch
runtime handle generation mismatch
```

## 10.3 Cross-queue rejection

다음 중 하나면 reject한다.

```text
dispatcher queue pointer mismatch
bridge queue pointer mismatch
Q/K queue identity mismatch
consumer queue identity mismatch
```

Q/K buffer는 device-owned resource지만, W2 pair receipt는 intended submit queue lineage도 동일해야 한다.

## 10.4 Runtime restart

프로세스 재시작 후 이전 provenance artifact를 live admission에 재사용하지 않는다.

```text
runtime_process_epoch mismatch -> stale
```

Artifact는 audit 증거이며 live capability token이 아니다.

---

# 11. Stream과 primitive identity

Q/K live raw path admission:

```text
primitive_id present and non-empty
stream_id present and non-empty
Q primitive_id != K primitive_id
Q stream_id == K stream_id
stream_id == invocation expected stream, available when bound
```

현재 `primitive_id`와 `stream_id`는 Burn/Fusion handle-map seam에서 얻는다.

이 값만으로 model/layer/step을 추론하지 않는다.

W2 provenance가 명시 identity와 결속한다.

---

# 12. Freshness 판정

Lease는 다음을 모두 만족할 때만 fresh다.

```text
model_instance_id exact
decode_session_id exact
layer_index exact
decode_step_ordinal exact
position_epoch exact
kv_cache_generation exact
attention_invocation_generation exact
runtime_process_epoch exact
invocation_open true
consumed false
```

Stale 조건:

```text
이전 invocation generation
이전 KV generation
이전 decode step
이전 layer
이전 session epoch
이전 position epoch
이전 runtime process epoch
이미 consumed
invocation closed
```

Consumer가 성공적으로 lease pair를 받으면:

```text
consumed = true
```

W4에서 dispatch submit 전 오류가 발생하면 lease를 재사용하지 않는다.

새 invocation에서 다시 capture한다.

---

# 13. Rejection matrix

## 13.1 Cross-model

Reject:

```text
model_instance_id mismatch
model_instance_binding_digest mismatch
effective_runtime_binding_digest mismatch
model_instance_epoch mismatch
```

## 13.2 Cross-session

Reject:

```text
decode_session_id mismatch
decode_session_contract_digest mismatch
request_id mismatch
decode_session_epoch mismatch
```

## 13.3 Cross-layer

Reject:

```text
Q layer != invocation layer
K layer != invocation layer
Q layer != K layer
layer index out of range
```

## 13.4 Cross-step

Reject:

```text
Q step != invocation step
K step != invocation step
Q step != K step
prefill has decode step Some
decode has decode step None
```

## 13.5 Cross-position

Reject:

```text
position_epoch mismatch
causal snapshot digest mismatch
q_position_base mismatch
kv_position_base mismatch
seq_q mismatch
seq_kv mismatch
```

## 13.6 Cross-generation

Reject:

```text
KV generation mismatch
attention invocation generation mismatch
runtime handle generation mismatch
TensorCube stage authority digest mismatch
```

TensorCube stage numeric generation과 KV generation의 equality는 검사하지 않는다.

## 13.7 Cross-device / queue

Reject:

```text
Arc pointer mismatch
process epoch mismatch
lineage digest mismatch
```

## 13.8 Role swap

Reject:

```text
Q lease tagged Key
K lease tagged Query
Q shape applied to K role
K shape applied to Q role
```

## 13.9 Host upload

Reject:

```text
lease.mode == UploadedFromHost
active_handle.state == MetadataOnly
active_handle.buffer == None
vendor_access_path starts with host_upload
BridgeStats.host_uploads > 0
```

---

# 14. W1 shape binding

W2 provenance는 W1 shape reconciliation을 다시 계산하지 않는다.

다음 digest를 참조한다.

```text
model_shape_authority_digest
shape_reconciliation_digest
dispatch_plan_digest
kernel_profile_digest
```

Q role shape:

```text
[batch, query_heads, q_seq, head_dim]
```

K role shape:

```text
[batch, kv_heads, kv_seq, head_dim]
```

W2 pair receipt는 W1 plan의 각 dispatch spec과 다음을 결속한다.

```text
model_instance_id
selected_batch
q_seq
kv_seq
query_heads
kv_heads
head_dim
q_token_base
active_query_rows
kv_block_count
```

W2는 shape를 조용히 보정하지 않는다.

---

# 15. Provenance builder

권장 API:

```rust
pub struct AttentionLeaseProvenanceBuilder<'a> {
    pub invocation: &'a AttentionInvocationIdentity,
    pub shape_receipt: &'a AttentionRuntimeShapeReconciliationReceipt,
    pub dispatch_plan: &'a TensorCubeStage10DispatchPlan,
    pub runtime_handles: &'a NativeWgpuRuntimeHandles,
    pub dispatcher: &'a HeadwiseAtlasDispatcher,
    pub generations: AttentionLeaseGenerationDomains,
}
```

Q capture:

```rust
builder.bind_query_lease(raw_q_lease)
```

K capture:

```rust
builder.bind_key_lease(raw_k_lease)
```

Pair:

```rust
builder.seal_pair(q, k)
```

Builder는 다음을 수행하지 않는다.

```text
raw lease 자체 생성
host upload fallback
TensorCube dispatch
output buffer allocation
route decision
stage pointer write
```

W4가 live raw bridge로 lease를 생성한 뒤 W2 builder를 호출한다.

---

# 16. State ownership

## 16.1 NativeWgpuModel-owned

```text
attention_invocation_generation AtomicU64
runtime_handle_generation u64
runtime_process_epoch u64
```

## 16.2 DecodeState / KV lifecycle-owned

```text
decode_session identity
session epoch
position epoch
KV cache generation
explicit decode step ordinal
```

## 16.3 Invocation-local

```text
AttentionInvocationIdentity
lease capture generation
Q/K provenance
pair receipt
consumed state
```

## 16.4 W0-owned

```text
Headwise route authority digest
TensorCube stage authority digest
TensorCube stage generation 44
output authority
```

## 16.5 W1-owned

```text
model shape authority digest
shape reconciliation digest
dispatch plan digest
kernel profile digest
```

한 owner의 값을 다른 owner가 재계산하거나 덮어쓰지 않는다.

---

# 17. Runtime process epoch

W2는 process-local identity domain을 만든다.

권장:

```text
RuntimeProcessEpoch
  initialized once per process
  nonzero u64
  immutable
```

생성 방식은 구현에서 결정할 수 있으나 다음을 만족해야 한다.

```text
같은 process에서 안정적
다른 process에서 재사용하지 않음
artifact replay capability로 사용하지 않음
```

보안 토큰이라고 주장하지 않는다.

---

# 18. Positive validation matrix

W2 gate는 live model Q/K를 tap하지 않는다.

대신 deterministic provenance fixture와 standalone same-runtime lease fixture를 사용한다.

Minimum positive cases: 48

## 18.1 Phase matrix

```text
prefill
incremental_decode
chunked_decode
```

## 18.2 Layer matrix

```text
layer 0
middle layer
last layer
```

`middle`과 `last`는 W1 model shape authority의 `num_layers`에서 유도한다.

## 18.3 Shape matrix

```text
q_seq 1 / kv_seq 1
q_seq 1 / kv_seq 17
q_seq 1 / kv_seq 65
q_seq 16 / kv_seq 16
q_seq 16 / kv_seq 17
q_seq 17 / kv_seq 32
```

## 18.4 Buffer layout matrix

```text
distinct Q/K buffers
same backing buffer, non-overlapping ranges
nonzero aligned offsets
buffer_size > logical_len_bytes
exact buffer_size == logical_len_bytes
```

## 18.5 Generation matrix

```text
KV generation 1
KV generation 2
attention invocation generation 1
attention invocation generation > layer_count
runtime handle generation 1
TensorCube stage generation 44
```

모든 positive case:

```text
same model/session/layer/step
same device/queue/stream
roles exact
ranges valid
freshness valid
pair pass
live TensorCube dispatch 0
```

---

# 19. Decision counters

Schema:

```text
ash.attn.interconnect.w2.decision-counters.v1
```

Canonical 44 counters:

```text
parent_w0_binding_mismatch
parent_w1_shape_authority_mismatch
model_instance_id_mismatch
model_binding_digest_mismatch
effective_runtime_binding_mismatch
model_instance_epoch_mismatch
decode_session_id_mismatch
decode_session_contract_mismatch
request_id_mismatch
decode_session_epoch_mismatch
position_epoch_mismatch
layer_index_mismatch
layer_count_mismatch
decode_step_missing
decode_step_mismatch
phase_route_mismatch
causal_snapshot_digest_mismatch
shape_reconciliation_digest_mismatch
dispatch_plan_digest_mismatch
lease_role_mismatch
lease_mode_mismatch
active_handle_state_mismatch
active_handle_buffer_mismatch
primitive_id_missing
stream_id_missing
stream_id_mismatch
buffer_identity_mismatch
buffer_offset_mismatch
buffer_size_mismatch
logical_length_mismatch
buffer_range_overflow
buffer_range_overlap
runtime_process_epoch_mismatch
runtime_handle_generation_mismatch
device_lineage_mismatch
queue_lineage_mismatch
kv_cache_generation_mismatch
attention_invocation_generation_mismatch
lease_capture_generation_mismatch
freshness_expired
lease_already_consumed
host_upload_detected
route_mutation_detected
stage_mutation_detected
```

PASS 조건은 전부 0이다.

첫 nonzero counter와 다음 context를 출력한다.

```text
case_id
role
model_instance_id
decode_session_id
layer_index
decode_step_ordinal
buffer identity/range
generation domain tuple
```

---

# 20. Negative controls

Minimum 64건을 실제 실행한다.

## 20.1 Parent authority

```text
01 W0 binding digest flip
02 W0 output authority tensorcube
03 W1 model shape digest flip
04 W1 dispatch plan digest flip
```

## 20.2 Model identity

```text
05 model_instance_id mismatch
06 model binding digest mismatch
07 effective runtime binding mismatch
08 model instance epoch mismatch
```

## 20.3 Session identity

```text
09 decode_session_id mismatch
10 decode session contract digest mismatch
11 request_id mismatch
12 session epoch mismatch
13 position epoch mismatch
```

## 20.4 Layer and step

```text
14 layer index below domain, represented invalid
15 layer index == layer_count
16 Q layer mismatch
17 K layer mismatch
18 Q/K cross-layer pair
19 decode step missing in incremental
20 decode step present in prefill
21 Q decode step stale
22 K decode step stale
23 Q/K cross-step pair
24 phase/route mismatch
```

## 20.5 Causal and shape

```text
25 causal snapshot digest flip
26 q_position_base mismatch
27 kv_position_base mismatch
28 seq_q mismatch
29 seq_kv mismatch
30 shape reconciliation digest flip
31 dispatch plan digest flip
32 Query role with K shape
33 Key role with Q shape
```

## 20.6 Raw lease mode / handle

```text
34 UploadedFromHost mode
35 MetadataOnly state
36 active handle buffer None
37 active handle buffer different Arc
38 primitive_id None
39 primitive_id empty
40 stream_id None
41 stream_id empty
42 vendor_access_path host_upload fallback
43 seam_id empty
```

## 20.7 Buffer range

```text
44 len_elements != product(shape)
45 len_bytes mismatch
46 bytes_per_element != 4
47 buffer_size zero
48 buffer_size < logical_len_bytes
49 offset + size overflow
50 unaligned offset
51 same buffer overlapping ranges
52 exact Q/K alias
```

## 20.8 Device / queue

```text
53 runtime process epoch mismatch
54 runtime handle generation mismatch
55 dispatcher device Arc mismatch
56 dispatcher queue Arc mismatch
57 bridge device lineage mismatch
58 bridge queue lineage mismatch
59 Q/K device identity mismatch
60 Q/K queue identity mismatch
```

## 20.9 Generation / freshness

```text
61 KV generation mismatch
62 attention invocation generation mismatch
63 lease capture order reversed
64 stale previous invocation
65 invocation closed
66 already consumed lease
67 TensorCube stage authority digest mismatch
68 TensorCube stage generation mismatch
```

## 20.10 Authority isolation

```text
69 Headwise output authority mutation attempt
70 TensorCube live dispatch attempt
71 route mutation attempt
72 stage pointer mutation attempt
```

각 negative control:

```text
rejected == true
Headwise output authority unchanged
TensorCube live dispatch count == 0
route mutation count == 0
stage mutation count == 0
partial provenance publish == 0
partial artifact count == 0
```

Canonical minimum은 64이며 구현 권장은 72/72다.

---

# 21. Static checks

필수 정적 검사:

```text
RawWgpuBufferLease direct model_instance field count      0
RawWgpuBufferLease direct layer field count               0
RawWgpuBufferLease direct decode_step field count         0
ProvenancedAttentionLease unchecked constructor count     0
q_position_base to decode_step inference count            0
kv_seq to generation inference count                      0
cross-generation numeric equality count                   0
Headwise route numeric generation fabrication count       0
host upload admission count                               0
TensorCube live dispatch call from W2 gate                0
map_async in W2 hot path                                  0
blocking device poll in W2 hot path                       0
route pointer write call                                  0
stage pointer write/CAS call                              0
```

Callsite checks:

```text
prefill attention invocation carries layer identity
incremental attention invocation carries explicit step identity
sampled decode uses same step source as greedy decode
all try_grouped_query_attention_via_atlas callsites updated
missing invocation identity fallback count 0
```

---

# 22. Implementation files

신설 권장:

```text
crates/burn_webgpu_backend/src/attention_lease_provenance.rs
crates/model_core/src/attention_invocation_identity.rs
crates/model_core/src/attention_generation_domains.rs
crates/orchestrator_local/src/attention_interconnect_w2_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w2_gate.rs
specs/cli/ash_attn_interconnect_w2.args
```

수정 권장:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/decode_state.rs
crates/orchestrator_local/Cargo.toml
```

`raw_bridge.rs` 수정은 provenance builder가 authoritative bridge lineage snapshot을 받을 수 있는 read-only API 추가에 한정한다.

권장 API:

```text
BurnToRawWgpuBridge::uses_runtime_handles(...)
BurnToRawWgpuBridge::runtime_lineage_snapshot(...)
```

기존 raw lease 생성 동작은 변경하지 않는다.

수정 금지:

```text
Stage9 WGSL
Stage10 WGSL
Headwise production WGSL
W0 binding semantics
W1 shape formulas
Headwise route LUT
TensorCube stage pointer
KV payload layout
V binding
weighted-V accumulation
```

---

# 23. Artifact 산출

출력 디렉터리:

```text
workspace/runtime/attention/interconnect/w2
```

Rust gate가 실행 시 다음 41개 child artifact를 순서대로 산출한다.

```text
identity.json
parent_w0_binding.json
parent_w1_shape_authority.json
source_inventory.json
existing_lease_surface.json
invocation_identity_contract.json
model_instance_identity.json
decode_session_identity.json
layer_identity.json
decode_step_identity.json
attention_phase_identity.json
runtime_handle_lineage.json
device_identity.json
queue_identity.json
buffer_identity_contract.json
active_handle_consistency.json
buffer_range_contract.json
q_lease_provenance.json
k_lease_provenance.json
qk_pair_binding.json
generation_domain_registry.json
freshness_epoch.json
lease_lifetime_contract.json
same_invocation_admission.json
stale_rejection.json
cross_model_rejection.json
cross_session_rejection.json
cross_layer_rejection.json
cross_step_rejection.json
cross_device_rejection.json
cross_queue_rejection.json
role_swap_rejection.json
overlap_rejection.json
host_upload_rejection.json
planner_binding.json
no_live_qk_dispatch.json
negative_control_outcomes.json
decision_counters.json
static_checks.json
verdict.json
runtime_artifact.json
```

Canonical ordered list:

```text
child_artifact_expected       41
child_artifact_list_sha256     89762c94d15a6d541ba7e78994d68611adf2f911517822cf5c794750af027b08
serialization                  UTF-8, one filename per line, trailing LF included
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w2_runtime_artifact.json

schema = ash.attn.interconnect.w2.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w2_local_manifest.json

schema = ash.attn.interconnect.w2.local_manifest.v1
manifest self excluded from hash graph
```

코드 ZIP에는 다음을 넣지 않는다.

```text
명세 Markdown
W2 runtime artifact
W2 local manifest
W2 child artifact
SHA-256 sidecar
helper PowerShell script
helper CMD script
```

artifact와 manifest는 Rust gate가 실행 시 산출한다.

---

# 24. CLI 계약

Binary:

```text
ash_attn_interconnect_w2_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w2.args
```

Canonical keys:

```text
--repo-root
--parent-w0-runtime-artifact
--parent-w0-local-manifest
--parent-w1-runtime-artifact
--parent-w1-local-manifest
--verified-model-instance-binding
--decode-session-contract
--model-spec
--expected-model-instance-id
--expected-shape-authority-digest
--expected-kernel-profile-id
--expected-tensorcube-stage-generation
--expected-headwise-output-authority
--require-explicit-layer-identity
--require-explicit-decode-step-identity
--require-raw-borrowed-mode
--require-active-handle-buffer
--require-primitive-id
--require-stream-id
--require-device-pointer-equality
--require-queue-pointer-equality
--require-generation-domain-separation
--require-freshness-epoch
--forbid-host-upload
--forbid-stale-lease
--forbid-cross-model
--forbid-cross-session
--forbid-cross-layer
--forbid-cross-step
--forbid-cross-device
--forbid-cross-queue
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
40 key/value pairs
80 non-empty lines
```

CLI 값은 expectation과 gate policy다.

다음을 CLI가 생성하거나 대체하지 않는다.

```text
model instance identity
decode session identity
layer index
decode step ordinal
buffer identity
primitive/stream identity
device/queue pointer identity
generation values
```

---

# 25. PASS gate

필수 PASS 조건:

```text
parent W0-R2 closure exact
parent W1-R1 closure exact
model identity exact
decode session identity exact
layer identity explicit
incremental decode step explicit
prefill step None exact
runtime device pointer equality exact
runtime queue pointer equality exact
RawBorrowed mode exact
active handle consistency exact
primitive/stream IDs present
buffer range arithmetic exact
Q/K overlap zero
all generation domains typed and separated
freshness epoch exact
stale/cross-domain negative controls pass
positive provenance cases >= 48
negative controls >= 64, recommended 72
all 44 decision counters zero
Headwise output authority unchanged
TensorCube live Q/K dispatch zero
route mutation zero
stage mutation zero
child artifacts 41/41
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
model_instance=<id>
lease_authority=explicit_invocation_plus_raw_handle
layer_identity=explicit
decode_step_identity=explicit
device_lineage=arc_pointer_exact
queue_lineage=arc_pointer_exact
generation_domains=separated
freshness=attention_invocation_scoped
positive_cases=48/48
negative_controls=72/64
stale_rejected=true
cross_layer_rejected=true
cross_model_rejected=true
live_qk_dispatch=0
output_authority=headwise
route_mutation=0
stage_mutation=0
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W2_LEASE_PROVENANCE_MODEL_LAYER_DECODE_STEP_IDENTITY_BUFFER_IDENTITY_OFFSET_LENGTH_DEVICE_QUEUE_LINEAGE_GENERATION_DOMAIN_SEPARATION_FRESHNESS_EPOCH_STALE_CROSS_LAYER_CROSS_MODEL_REJECTION_HEADWISE_OUTPUT_AUTHORITY_PRESERVED_NO_LIVE_DISPATCH_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W2_LEASE_PROVENANCE_IDENTITY_LINEAGE_GENERATION_FRESHNESS_OR_STALE_REJECTION_NOT_PROVEN
```

---

# 26. 직접 Cargo 실행

저장소 루트에서 직접 실행한다.

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w2_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w2.args"
```

정상 시작 revision:

```text
W2-lease-provenance-generation-domain-v1
```

W2는 WGSL을 변경하지 않으므로 `burn_webgpu_backend` clean은 원칙적으로 의무가 아니다.

raw bridge / backend Rust module을 수정하므로 Cargo가 해당 crate를 정상 재컴파일해야 한다.

---

# 27. 실패 처리

첫 mismatch를 SSOT로 삼는다.

우선순위:

```text
parent authority
model/session identity
layer/step identity
shape/causal binding
raw handle consistency
buffer range
device/queue lineage
generation domains
freshness
pair binding
```

금지되는 조용한 보정:

```text
missing decode step = 0
missing layer = label parse
missing model = current model fallback
missing session = causal snapshot session fallback
missing primitive ID = label fallback
missing stream ID = empty string
stale generation = current generation overwrite
cross-device = digest only으로 허용
host upload = RawBorrowed로 재표기
overlap = distinct role이므로 허용
```

실패 시:

```text
TensorCube shadow admission denied
Headwise path unchanged
route/stage unchanged
partial provenance publish 0
```

---

# 28. W2 이후 경계

W2 이후 확정되는 것:

```text
Q/K lease의 모델·세션·레이어·스텝 귀속 방식
buffer identity·range 검증 방식
device·queue live lineage 권위
각 generation domain의 소유자와 의미
freshness lifetime
stale/cross-domain rejection
```

W3에서 추가할 것:

```text
cached Stage9/10 pipelines
persistent scratch ring
submit-fenced reuse
runtime executor generation
no blocking map
VRAM plateau
```

W4에서 처음 허용할 것:

```text
실제 Headwise Q/K live raw capture
W2 provenance wrapper 생성
W1 dispatch plan과 결속
TensorCube Stage9/10 shadow dispatch
Headwise output authority 유지
```

W4 admission sequence:

```text
W0 authority
  -> W1 shape plan
  -> W2 invocation identity
  -> live Q/K raw lease
  -> W2 provenance bind
  -> W2 pair validation
  -> W3 executor
```

---

# 29. 최종 봉인 문장

W2 PASS 시 다음만 확정한다.

```text
결속된 NativeWgpu 모델과 decode session에서 발생한 attention invocation은
명시적인 layer index와 decode-step ordinal을 가지며,
그 invocation에 속하는 Query·Key raw buffer lease는
model·session·layer·step·position·shape identity에 결속될 수 있다.

각 lease의 underlying buffer identity, offset, slice size, logical payload length,
primitive ID, stream ID, active raw handle 상태가 fail-closed로 검증되며,
Headwise dispatcher와 raw bridge와 consumer는 동일한 live Device·Queue Arc lineage를 사용한다.

model instance epoch, decode session epoch, position epoch, KV cache generation,
attention invocation generation, lease capture generation, Headwise candidate nonce,
TensorCube stage generation은 서로 다른 domain으로 분리되며
숫자 equality로 혼동되지 않는다.

lease freshness는 단일 attention invocation에 한정되고,
stale·cross-model·cross-session·cross-layer·cross-step·cross-device·cross-queue lease는 거부된다.

Headwise는 유일한 attention output authority를 유지하며,
TensorCube live Q/K dispatch와 output commit은 발생하지 않았다.
```

아직 금지되는 주장:

```text
TensorCube가 실제 live Headwise Q/K를 소비했다.
TensorCube Stage9/10이 decode hot path에서 실행됐다.
TensorCube와 Headwise의 수치 parity가 통과했다.
TensorCube가 V 또는 attention context를 생성했다.
```
