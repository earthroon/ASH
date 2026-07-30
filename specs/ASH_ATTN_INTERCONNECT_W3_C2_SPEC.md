# ASH-ATTN-INTERCONNECT-W3-C2 명세

## Headwise Prefill Full Activation /
## Full-Route Policy Live Enforcement /
## All-Layer Production Admission /
## Full-Prefill Shape Coverage /
## Zero CPU QKV Materialization /
## Zero Host Reupload /
## Burn Fallback Attribution /
## Prefill Output Authority Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C2`  
> Build revision: `W3-C2-headwise-prefill-full-activation-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C1-R3` PASS  
> Parent policy authority: `full_route_admission`  
> Parent enforcement mode: `compatibility_projection`  
> 대상 surface: `ProductionPrefill` only  
> Incremental·Chunked·Generic Forward: behavior-preserving nonmutation  
> TensorCube role: `ShadowObserverOnly` 유지  
> attention output authority: Headwise 유지  
> 후속 커밋: `W3-C3 Headwise Incremental Full Activation`

---

# 0. 목적

W3-C0는 현재 attention 경로를 전수 조사했다.

```text
prefill          attempted_but_fallback_possible
incremental      attempted_but_fallback_possible
chunked          contract_present_live_absent
generic forward  bypassed_direct_burn
CPU materialize  1 branch
host reupload     2 branches
```

W3-C1은 route admission의 정책 권위를 하나로 통합했다.

```text
operator intent          immutable bind-time snapshot
policy authority         HeadwiseFullRouteAdmissionPolicySnapshot
legacy projection        exact
prefill decision         unified compatibility projection
incremental decision     unified compatibility projection
chunked                   DenyLiveCallsiteAbsent
generic forward           reconciliation blocker
```

그러나 production prefill hot path는 아직 W3-C1 decision을 직접 집행하지 않는다.

현재 실제 경로는 다음과 같다.

```text
forward_prefill
  -> for every decode layer
  -> forward_block_prefill
  -> Q/K/V projection
  -> try_grouped_query_attention_via_atlas(...)
       Some(ctx)  -> Headwise result
       None       -> caller Burn grouped_query_attention
```

`try_grouped_query_attention_via_atlas` 내부에는 서로 의미가 다른 결과가 `Option` 하나에 겹쳐 있다.

```text
router disabled
policy not admitted
dispatcher absent
geometry invalid
production dispatch failure
production quarantine
non-production CPU roundtrip failure
```

또한 production admission이 아니면 다음 경로가 존재한다.

```text
GPU Headwise dispatch
  -> dispatch_native_qkv_to_cpu_f32
  -> Vec<f32>
  -> Tensor::from_data
  -> GPU tensor reupload
```

W3-C2의 목적은 production prefill에 한해 이 모호성을 제거하고 다음 상태를 만드는 것이다.

```text
모든 prefill layer가 W3-C1 policy SSOT에서 실제 admission decision을 받는다.
모든 admitted layer가 same-device Headwise production dispatch를 실행한다.
production prefill에서 CPU QKV materialize와 host reupload는 0이다.
Burn fallback은 typed outcome과 명시 receipt 없이 실행될 수 없다.
positive production prefill matrix에서 모든 layer output authority는 Headwise다.
```

W3-C2 PASS가 확정하는 것:

```text
prefill live policy enforcement
all-layer admission exact
full-prefill runtime shape reconciliation
same-device Q/K/V raw-borrow admission
Headwise output commit on every positive layer
production prefill CPU materialize 0
production prefill host reupload 0
silent Burn fallback 0
fallback attribution exact
```

W3-C2 PASS가 확정하지 않는 것:

```text
incremental decode full activation
chunked decode implementation
generic forward reconciliation
TensorCube shadow exit
TensorCube live Q/K/V consumption
Headwise resource plateau
Headwise device-loss recovery
```

---

# 1. 현재 코드에서 직접 확인된 상태

## 1.1 Prefill layer loop

`crates/model_core/src/decode_state.rs`

```text
forward_prefill
  -> decode_layers().iter().enumerate()
  -> forward_block_prefill(layer_idx, layer, ...)
```

따라서 static intended layer coverage는:

```text
[0, decode_layers().len())
```

W3-C2는 이 intended range와 runtime receipt range가 exact한지 검증한다.

## 1.2 Q/K/V shape

`forward_block_prefill`은 projection 후 다음 shape를 만든다.

```text
Q [batch, query_heads, seq, head_dim]
K [batch, kv_heads,    seq, head_dim]
V [batch, kv_heads,    seq, head_dim]
```

Full prefill 조건:

```text
seq_q == seq_kv
q_position_base == kv_position_base
prefill_invocation_ordinal == 0
decode_step_ordinal == None
```

## 1.3 Current production Headwise path

`NativeWgpuModel::try_grouped_query_attention_via_atlas`는 production policy가 route를 admit하면:

```text
runtime handles exact
same-device dispatcher exact
RawBorrowed Q/K/V
candidate output ring
downstream output ring
dispatch_native_qkv_into_output_device_guarded
output readback 0
output host upload 0
```

성공 시 `Some(downstream_output)`을 반환한다.

실패 시:

```text
headwise_production_quarantined = true
rollback count += 1
return Ok(None)
```

caller는 `None`을 Burn GQA fallback으로 처리한다.

## 1.4 Current non-production branch

Production policy가 route를 admit하지 않으면:

```text
dispatch_native_qkv_to_cpu_f32
Tensor::<NativeInferenceBackend,4>::from_data
```

W3-C2 production prefill은 이 branch에 진입할 수 없다.

## 1.5 Current W3-C1 policy mode

W3-C1 PASS 시:

```text
enforcement_mode = CompatibilityProjection
execution_mutation_allowed = false
route_pointer_write_allowed = false
output_authority_change_allowed = false
```

W3-C2는 `ProductionPrefill`에 한해서 live enforcement를 추가한다.

정책 SSOT를 교체하지 않는다.

---

# 2. 상태 귀속과 SSOT

## 2.1 Model-owned immutable authority

`NativeWgpuModel` 소유:

```text
VerifiedModelInstanceBinding
AttentionModelShapeAuthoritySnapshot
HeadwiseOperatorIntentSnapshot
HeadwiseFullRouteAdmissionPolicySnapshot
runtime process epoch
runtime handle generation
device / queue / dispatcher
Headwise production quarantine
Headwise output rings
```

## 2.2 Session-owned authority

`DecodeState` 소유:

```text
BoundDecodeSessionContract
KV lifecycle
prefill invocation ordinal
per-layer invocation identity
prefill activation receipt
```

현재 `DecodeState`는 `BoundRuntimeObjectIdentity`와 KV lifecycle만 보존한다.

W2의 canonical `AttentionInvocationIdentity`는 full `BoundDecodeSessionContract`를 요구한다.

따라서 W3-C2는 다음을 추가한다.

```rust
pub struct DecodeState {
    // existing fields
    pub bound_decode_session_contract: Option<BoundDecodeSessionContract>,
    pub last_headwise_prefill_activation_receipt:
        Option<HeadwisePrefillActivationReceipt>,
}
```

`bind_runtime_identity()`에서 session contract를 clone하여 1회 결속한다.

금지:

```text
KV lifecycle의 decode_session_id만으로 session contract 재구성
request_id 추론
sampling policy digest 추론
prompt token digest 재계산 후 기존 contract 대체
```

## 2.3 Layer-owned ephemeral state

각 prefill layer invocation이 소유:

```text
runtime Q/K/V tensors
runtime shape observation
causal bridge receipt
shape reconciliation receipt
attention invocation identity
full-route admission context
full-route admission decision
production dispatch receipt
output authority receipt
fallback attribution receipt, if any
```

layer 종료 후 Tensor 자체를 global policy state에 저장하지 않는다.

---

# 3. Parent closure

필수 parent chain:

```text
W0-R2  dual authority binding
W1-R1  model/runtime shape authority
W2-R1  invocation identity and provenance
W3-C0  route coverage inventory
W3-C1-R3 full-route admission policy
```

필수 digest:

```text
w0_binding_digest
w1_shape_authority_digest
w2_provenance_authority_digest
w3_c0_coverage_authority_digest
w3_c1_policy_authority_digest
w3_c1_operator_intent_digest
w3_c1_legacy_projection_digest
```

필수 W3-C1 state:

```text
policy_authority == full_route_admission
operator_intent == immutable_bind_time_snapshot
legacy_projection == exact
prefill == unified_compatibility_projection
route_behavior_mutation == 0
tensorcube_role == shadow_observer_only
output_authority == headwise
```

Parent drift가 있으면 production prefill을 실행하지 않는다.

---

# 4. W3-C2 live enforcement boundary

W3-C2는 W3-C1 policy 전체를 `FullRouteEnforced`로 바꾸지 않는다.

Surface별 effective mode:

```text
ProductionPrefill            LiveEnforced
ProductionIncrementalDecode  CompatibilityProjection
ProductionChunkedDecode      ExplicitDeniedLiveCallsiteAbsent
GenericGenerationForward     ReconciliationRequired
ModuleTrace                  DiagnosticOnly
DiagnosticSmoke              DiagnosticOnly
```

새 타입:

```rust
pub enum HeadwiseSurfaceEnforcementMode {
    CompatibilityProjection,
    LiveEnforced,
    ExplicitDenied,
    ReconciliationRequired,
    DiagnosticOnly,
}
```

새 immutable activation authority:

```rust
pub struct HeadwisePrefillActivationPolicySnapshot {
    pub schema: String,
    pub patch_id: String,
    pub build_revision: String,
    pub model_instance_id: String,
    pub full_route_policy_digest: String,
    pub operator_intent_digest: String,
    pub shape_authority_digest: String,
    pub surface: HeadwiseRuntimeSurfaceId,
    pub enforcement_mode: HeadwiseSurfaceEnforcementMode,
    pub require_all_layers: bool,
    pub require_zero_cpu_materialize: bool,
    pub require_zero_host_reupload: bool,
    pub allow_attributed_burn_fallback_after_dispatch_failure: bool,
    pub forbid_nonproduction_cpu_roundtrip: bool,
    pub activation_digest: String,
}
```

Canonical 값:

```text
surface                                           ProductionPrefill
enforcement_mode                                  LiveEnforced
require_all_layers                                true
require_zero_cpu_materialize                      true
require_zero_host_reupload                        true
allow_attributed_burn_fallback_after_dispatch_failure true
forbid_nonproduction_cpu_roundtrip                true
```

이 snapshot은 W3-C1 policy에서 파생되며 역으로 W3-C1 policy를 수정하지 않는다.

---

# 5. Causal authority bridge

현재 production dispatch는 backend의 `HeadwiseCausalPositionSnapshot`을 사용한다.

W1/W2 identity는 model_core의 `AttentionRuntimeCausalPositionSnapshot`을 사용한다.

두 타입은 필드 의미가 같지만 schema와 digest domain이 다르다.

조용한 digest 대체는 금지한다.

새 receipt:

```rust
pub struct HeadwisePrefillCausalAuthorityBridgeReceipt {
    pub schema: String,
    pub backend_snapshot_digest: String,
    pub runtime_snapshot_digest: String,
    pub route_exact: bool,
    pub session_exact: bool,
    pub position_epoch_exact: bool,
    pub q_position_base_exact: bool,
    pub kv_position_base_exact: bool,
    pub seq_q_exact: bool,
    pub seq_kv_exact: bool,
    pub suffix_alignment_exact: bool,
    pub bridge_digest: String,
    pub pass: bool,
}
```

Canonical bridge:

```text
backend FullPrefill     -> runtime FullPrefill
backend digest          preserved
runtime digest          independently computed
field equality          all true
```

Digest equality 자체를 요구하지 않는다.

필드 equality와 각 타입의 self-validation을 요구한다.

---

# 6. Full-prefill runtime shape authority

## 6.1 Runtime observation

실제 Q/K/V dims에서 `RuntimeAttentionShapeObservation`을 생성한다.

금지:

```text
ModelSpec dims를 actual tensor dims로 복사하여 observation 위조
K shape로 V shape 대체
prompt token count를 seq_q로 간주하고 tensor dims 검증 생략
```

## 6.2 Shape reconciliation

필수 검증:

```text
Q batch == K batch == V batch
Q heads == model query_heads
K heads == V heads == model kv_heads
Q/K/V head_dim == model head_dim
Q seq == K seq == V seq
causal seq_q == runtime Q seq
causal seq_kv == runtime K/V seq
q_position_base == kv_position_base
seq <= max_position_embeddings
sliding window contract exact
```

## 6.3 Headwise prefill kernel profile

W1의 model shape authority는 유지한다.

TensorCube profile ID를 Headwise execution authority로 재사용하지 않는다.

W3-C2는 Headwise 전용 profile receipt를 추가한다.

```rust
pub struct HeadwisePrefillKernelProfileSnapshot {
    pub schema: String,
    pub profile_id: String,
    pub head_dim_required: u32,
    pub subgroup_size_required: u32,
    pub query_heads_per_kv_required: Option<u32>,
    pub full_prefill_supported: bool,
    pub minimum_seq: u32,
    pub maximum_seq_from_model: u64,
    pub raw_borrow_required: bool,
    pub profile_digest: String,
}
```

Current source-derived constraints:

```text
head_dim_required        64
subgroup_size_required   32
full_prefill_supported   true
minimum_seq              1
maximum_seq              ModelSpec.max_position_embeddings
raw_borrow_required      true
```

GQA group size는 model authority와 dispatcher plan이 exact해야 한다.

## 6.4 Required boundary matrix

모델 max position이 충분한 경우 최소 검사:

```text
1
2
3
15
16
17
31
32
33
63
64
65
127
128
129
255
256
257
511
512
513
1023
1024
1025
max_position - 1
max_position
```

`max_position`보다 큰 fixture는 생성하지 않는다.

동일 값은 deduplicate하고 오름차순으로 실행한다.

---

# 7. Prefill invocation identity

각 layer는 W2 `AttentionInvocationIdentity`를 실제로 생성한다.

Canonical fields:

```text
phase                       Prefill
route_id                    full_prefill
layer_index                 actual loop index
layer_count                 decode_layers().len()
decode_step_ordinal         None
prefill_invocation_ordinal  Some(0)
q_position_base             causal q base
kv_position_base            causal KV base
seq_q                       runtime Q seq
seq_kv                      runtime K/V seq
shape_reconciliation_digest actual layer receipt
dispatch_plan_digest        actual Headwise plan digest
attention_invocation_generation unique monotonic generation
```

`dispatch_plan_digest`는 dispatch 전에 결정된 Headwise plan authority에서 온다.

임의 문자열 placeholder는 금지한다.

모든 layer invocation generation은 서로 달라야 한다.

동일 prefill의 model/session/position epoch/prompt domain은 같아야 한다.

---

# 8. Live admission context

각 layer의 actual runtime facts로 `HeadwiseFullRouteAdmissionContext`를 생성한다.

Canonical context:

```text
surface_id                  ProductionPrefill
route_id                    FullPrefill
route_readiness             LiveCallsitePresent
layer_index                 actual layer index
layer_count                 actual decode layer count
decode_step_ordinal         None
prefill_invocation_ordinal  Some(0)
model_binding_digest        VerifiedModelInstanceBinding.instance_binding_digest
shape_authority_digest      W1 snapshot digest
shape_reconciliation_digest actual reconciliation digest
invocation_identity_digest  actual W2 invocation digest
causal_position_digest      backend or bridged runtime digest, field identified
q_shape/k_shape/v_shape     actual tensor dims
```

Boolean eligibility fields는 실제 상태에서 생성한다.

```text
parent_authority_valid
surface_route_exact
model_geometry_valid
shape_valid
causal_position_valid
invocation_identity_present
dispatcher_present
runtime_handles_present
dispatcher_device_exact
dispatcher_queue_exact
raw_borrow_available
quarantined
runtime_profile_supported
```

모두 `true`로 채우는 convenience constructor는 production hot path에서 금지한다.

W3-C1 fixture constructor는 gate fixture에만 허용한다.

---

# 9. Typed prefill execution outcome

Production prefill은 `Option<Tensor>`를 사용하지 않는다.

신규 outcome:

```rust
pub enum HeadwisePrefillExecutionOutcome {
    HeadwiseCommitted {
        output: Tensor<NativeInferenceBackend, 4>,
        admission: HeadwiseFullRouteAdmissionDecision,
        dispatch: HeadwiseAtlasProductionDispatchReceipt,
        authority: HeadwisePrefillLayerOutputAuthorityReceipt,
    },
    BurnFallbackRequired {
        admission: HeadwiseFullRouteAdmissionDecision,
        failure: HeadwisePrefillDispatchFailureReceipt,
        fallback: HeadwisePrefillFallbackAttributionReceipt,
    },
}
```

Canonical dedicated method:

```rust
execute_prefill_attention_via_headwise(
    q,
    k,
    v,
    heads,
    kv_heads,
    head_dim,
    causal_position,
    activation_policy,
    admission_bundle,
) -> Result<HeadwisePrefillExecutionOutcome>
```

금지:

```text
ProductionPrefill에서 기존 generic try 함수의 non-production branch 사용
None으로 policy denial 표현
None으로 dispatch failure 표현
caller가 reason 없이 Burn fallback 선택
```

Incremental은 W3-C3 전까지 기존 generic method를 유지한다.

---

# 10. Production prefill admission semantics

Positive production prefill layer는 다음 disposition만 허용한다.

```text
AdmitProductionDeviceGuarded
```

다음 disposition은 required production domain에서 hard denial이다.

```text
DenyParentAuthorityInvalid
DenyOperatorProductionDisabled
DenyOperatorRouteDisabled
DenyRouterDisabled
DenyQkvBridgeDisabled
DenyModelIdentityMismatch
DenyModelGeometryMismatch
DenyShapeAuthorityMismatch
DenyCausalPositionMismatch
DenyInvocationIdentityMissing
DenyLayerIdentityMismatch
DenyDispatcherMissing
DenyRuntimeHandlesMissing
DenyDeviceLineageMismatch
DenyQueueLineageMismatch
DenyRawBorrowUnavailable
DenyQuarantined
DenyUnsupportedRuntimeProfile
```

Hard denial은 silent Burn fallback으로 바꾸지 않는다.

Canonical behavior:

```text
before dispatch admission denial
  -> fail closed
  -> no Headwise dispatch
  -> no Burn fallback
  -> no partial prefill commit
```

단, 이미 admission된 production dispatch가 output commit 전에 실패하면 explicit attributed Burn fallback을 허용한다.

---

# 11. All-layer production admission

새 forward-level receipt:

```rust
pub struct HeadwisePrefillActivationReceipt {
    pub schema: String,
    pub patch_id: String,
    pub build_revision: String,
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub prompt_token_digest: String,
    pub prompt_len: usize,
    pub expected_layer_count: usize,
    pub observed_layer_count: usize,
    pub admitted_layer_count: usize,
    pub headwise_committed_layer_count: usize,
    pub burn_fallback_layer_count: usize,
    pub burn_remainder_layer_count: usize,
    pub cpu_materialize_count: u64,
    pub host_reupload_count: u64,
    pub silent_fallback_count: u64,
    pub layer_receipt_digests: Vec<String>,
    pub first_failure: Option<HeadwisePrefillFirstFailure>,
    pub final_output_authority: HeadwisePrefillFinalOutputAuthority,
    pub activation_digest: String,
    pub pass: bool,
    pub failures: Vec<String>,
}
```

Positive PASS:

```text
observed_layer_count         == expected_layer_count
admitted_layer_count         == expected_layer_count
headwise_committed_layer_count == expected_layer_count
burn_fallback_layer_count    == 0
burn_remainder_layer_count   == 0
cpu_materialize_count        == 0
host_reupload_count          == 0
silent_fallback_count        == 0
final_output_authority       HeadwiseAllLayers
```

Layer receipt ordering은 layer index ascending이다.

중복, 누락, 역순은 실패다.

---

# 12. Zero CPU QKV materialization

Production prefill source scope에서 금지되는 호출:

```text
dispatch_native_qkv_to_cpu_f32
attention output into_data().to_vec::<f32>()
CPU Vec<f32> context authority
```

허용되지 않는 우회:

```text
helper function으로 이름만 변경
trace path를 production path에서 호출
output guard를 핑계로 full payload readback
```

Production prefill counters:

```text
q_cpu_materialize_count
k_cpu_materialize_count
v_cpu_materialize_count
context_cpu_materialize_count
```

PASS 시 모두 0이다.

Compact telemetry readback은 현재 Headwise guard contract에 따라 별도 분류한다.

Full output payload readback은 0이어야 한다.

---

# 13. Zero host reupload

Production prefill attention payload에서 금지:

```text
Tensor::<NativeInferenceBackend,4>::from_data(flat, device)
Raw bridge UploadedFromHost
CPU context upload
CPU Q/K/V upload fallback
```

입력 token ID tensor 생성은 attention payload host reupload counter에 포함하지 않는다.

분류를 혼합하지 않는다.

PASS:

```text
q_host_upload_count        0
k_host_upload_count        0
v_host_upload_count        0
context_host_upload_count  0
output_host_upload_count   0
```

---

# 14. Same-device Q/K/V and output authority

각 positive layer dispatch receipt는 다음을 만족한다.

```text
same_device_dispatcher             true
q_zero_copy                         true
k_zero_copy                         true
v_zero_copy                         true
output_zero_copy                    true
output_buffer_identity_match        true
output_cpu_readback_count           0
output_host_upload_count            0
decision.authority_source           DeviceGuardDecisionToken
hot_path_map_async_count            0
hot_path_blocking_poll_count         0
hot_path_host_guard_decision_count   0
output_value_readback_count          0
```

Layer output authority receipt:

```rust
pub enum HeadwisePrefillLayerOutputAuthority {
    HeadwiseDeviceGuarded,
    BurnGpuAttributedFallback,
    BurnGpuQuarantinedRemainder,
}
```

한 layer 안에서 authority는 하나만 존재해야 한다.

금지:

```text
Headwise output 일부 + Burn output 일부 혼합
candidate output과 downstream output alias overlap
Headwise 성공 후 Burn 재실행
Burn 성공 후 Headwise output commit
```

---

# 15. Burn fallback attribution

## 15.1 허용 시점

Burn fallback은 다음 조건에서만 허용한다.

```text
admission disposition == AdmitProductionDeviceGuarded
Headwise dispatch attempted == true
failure before output commit == true
candidate output committed == false
downstream output committed == false
```

## 15.2 Fallback receipt

```rust
pub struct HeadwisePrefillFallbackAttributionReceipt {
    pub schema: String,
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub layer_index: usize,
    pub invocation_identity_digest: String,
    pub admission_decision_digest: String,
    pub dispatch_attempted: bool,
    pub failure_stage: String,
    pub failure_code: String,
    pub failure_before_output_commit: bool,
    pub headwise_output_committed: bool,
    pub burn_fallback_authorized: bool,
    pub burn_fallback_execution_count: u32,
    pub fallback_output_authority: String,
    pub quarantine_after_failure: bool,
    pub receipt_digest: String,
}
```

## 15.3 Single transition rule

첫 production dispatch failure 후:

```text
failed layer
  -> Burn GQA exactly once
  -> Headwise quarantine set

remaining layers
  -> no repeated Headwise attempt
  -> BurnGpuQuarantinedRemainder
  -> explicit per-layer receipt
```

이 상태는 output continuity를 위한 비상 동작이다.

W3-C2 activation PASS로 인정하지 않는다.

Forward receipt:

```text
pass = false
final_output_authority = BurnFallbackAttributed
first_failure = exact
```

## 15.4 Silent fallback zero

다음은 금지한다.

```text
None -> Burn without receipt
policy denial -> Burn
dispatcher missing -> Burn
raw borrow unavailable -> CPU roundtrip
shape mismatch -> Burn
quarantine already active -> unlabelled Burn
```

---

# 16. Legacy projection retirement for prefill

W3-C1 legacy projection은 compatibility bridge다.

W3-C2에서 production prefill live decision은 다음을 사용한다.

```text
HeadwiseFullRouteAdmissionPolicySnapshot
HeadwisePrefillActivationPolicySnapshot
HeadwiseFullRouteAdmissionContext
HeadwiseFullRouteAdmissionDecision
```

`headwise_atlas_production_requested(FullPrefill)`은 prefill live authority가 아니다.

허용:

```text
incremental compatibility path에서 legacy projection 유지
static equivalence audit에서 legacy value 비교
```

금지:

```text
prefill admission을 legacy bool 하나로 결정
legacy bool true를 full-route context 없이 production dispatch로 연결
legacy bool false를 CPU roundtrip으로 연결
```

W3-C2 artifact는 다음을 기록한다.

```text
prefill_legacy_decision_read_count = 0
prefill_full_route_decision_read_count = expected_layer_count
```

---

# 17. Greedy·sampled prefill parity

Greedy와 sampled prefill은 동일 `forward_prefill`을 사용한다.

W3-C2는 다음을 봉인한다.

```text
greedy prefill activation policy digest
sampled prefill activation policy digest
layer decision digest sequence shape
Headwise dispatch count
CPU materialize count
host reupload count
```

동일 prompt와 동일 session-bound fixture에서 attention route semantics는 같아야 한다.

Sampling selector 이후의 차이는 scope 밖이다.

---

# 18. KV lifecycle and commit boundary

현재 prefill:

```text
kv.lifecycle.stage(prompt_len)
per-layer K/V cache write
kv.past_len = prompt_len
kv.lifecycle.commit()
```

W3-C2 규칙:

```text
all layer attention outputs complete before KV lifecycle commit
admission denial before first dispatch -> no KV commit
mid-layer dispatch failure + attributed Burn success -> KV commit allowed, activation pass false
Burn fallback failure -> no KV commit
partial layer cache publication without forward completion -> reject
```

KV content generation과 position epoch는 W2 domain을 유지한다.

Headwise candidate nonce와 KV generation을 숫자 equality로 비교하지 않는다.

---

# 19. Production source changes

신설 권장:

```text
crates/model_core/src/headwise_prefill_full_activation.rs
crates/orchestrator_local/src/attention_interconnect_w3_c2_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w3_c2_gate.rs
specs/cli/ash_attn_interconnect_w3_c2.args
```

수정 예상:

```text
crates/model_core/src/lib.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/Cargo.toml
```

수정 금지:

```text
incremental attention behavior
chunked route constructor
generic model forward route
TensorCube role and dispatch
TensorCube WGSL
Headwise attention WGSL, unless compile-only ABI correction is separately named
W0/W1/W2 authority schemas
```

---

# 20. Required runtime interfaces

권장 public contracts:

```rust
pub struct HeadwisePrefillAdmissionBundle {
    pub causal_bridge: HeadwisePrefillCausalAuthorityBridgeReceipt,
    pub shape_observation: RuntimeAttentionShapeObservation,
    pub shape_reconciliation: AttentionRuntimeShapeReconciliationReceipt,
    pub invocation_identity: AttentionInvocationIdentity,
    pub admission_context: HeadwiseFullRouteAdmissionContext,
    pub admission_decision: HeadwiseFullRouteAdmissionDecision,
    pub bundle_digest: String,
}
```

```rust
pub struct HeadwisePrefillLayerExecutionReceipt {
    pub layer_index: usize,
    pub invocation_generation: u64,
    pub admission_bundle_digest: String,
    pub dispatch_receipt_digest: Option<String>,
    pub fallback_receipt_digest: Option<String>,
    pub output_authority: HeadwisePrefillLayerOutputAuthority,
    pub cpu_materialize_count: u64,
    pub host_reupload_count: u64,
    pub receipt_digest: String,
    pub pass: bool,
}
```

```rust
pub fn execute_prefill_attention_via_headwise(
    &self,
    q: Tensor<NativeInferenceBackend, 4>,
    k: Tensor<NativeInferenceBackend, 4>,
    v: Tensor<NativeInferenceBackend, 4>,
    heads: usize,
    kv_heads: usize,
    head_dim: usize,
    causal_position: HeadwiseCausalPositionSnapshot,
    bundle: &HeadwisePrefillAdmissionBundle,
) -> Result<HeadwisePrefillExecutionOutcome>
```

`execute_prefill_attention_via_headwise`는 non-production CPU roundtrip branch를 가지지 않는다.

---

# 21. Static enforcement checks

필수 정적 검사:

```text
forward_block_prefill calls dedicated prefill executor exactly once
forward_block_prefill does not call generic try method
prefill executor does not call dispatch_native_qkv_to_cpu_f32
prefill executor does not call Tensor::<NativeInferenceBackend,4>::from_data
prefill executor reads full-route policy
prefill executor evaluates full-route admission decision
prefill executor requires ProductionPrefill surface
prefill executor requires FullPrefill route
prefill executor returns typed outcome, not Option
Burn fallback callsite has attribution receipt
all layer loop unchanged
incremental callsite unchanged
generic forward callsite unchanged
TensorCube live dispatch added count 0
WGSL changed count 0
```

---

# 22. Positive validation matrix

최소 64 positive cases.

## 22.1 Policy and binding

```text
01 W0 exact
02 W1 exact
03 W2 exact
04 W3-C0 exact
05 W3-C1-R3 exact
06 model binding exact
07 session binding exact
08 activation policy bind exact
```

## 22.2 Shape boundaries

최소 26 prompt lengths from section 6.4.

## 22.3 Layer coverage

```text
first layer
middle layer
last layer
all-layer ordered closure
no duplicate invocation generation
```

## 22.4 Device and movement

```text
same-device dispatcher
same queue lineage
Q RawBorrowed
K RawBorrowed
V RawBorrowed
output RawBorrowed
CPU materialize zero
host reupload zero
```

## 22.5 Selector parity

```text
greedy prefill
sampled prefill
shared attention chain
```

## 22.6 Output authority

```text
Headwise every layer
no Burn fallback
no mixed authority
KV commit after complete layer closure
```

Canonical implementation target:

```text
positive_cases = 72
minimum = 64
```

---

# 23. Negative controls

최소 72 negative controls.

## 23.1 Parent closure

```text
01 W0 digest flip
02 W1 digest flip
03 W2 digest flip
04 W3-C0 digest flip
05 W3-C1 policy digest flip
06 operator intent digest flip
07 legacy projection mismatch
```

## 23.2 Session and invocation

```text
08 missing bound session contract
09 session model mismatch
10 request ID reconstruction attempt
11 prefill ordinal missing
12 prefill ordinal nonzero
13 decode step present on prefill
14 invocation generation duplicate
15 invocation digest flip
16 layer index mismatch
17 layer count mismatch
```

## 23.3 Causal bridge

```text
18 route mismatch
19 session mismatch
20 position epoch mismatch
21 q base mismatch
22 KV base mismatch
23 seq_q mismatch
24 seq_kv mismatch
25 suffix alignment mismatch
26 backend digest mismatch
27 runtime digest mismatch
```

## 23.4 Shape

```text
28 batch mismatch
29 Q head mismatch
30 K head mismatch
31 V head mismatch
32 head_dim mismatch
33 K/V seq mismatch
34 q_seq != kv_seq
35 empty prompt
36 max position overflow
37 sliding window violation
38 actual tensor observation replaced with ModelSpec dimensions
```

## 23.5 Admission

```text
39 parent authority false
40 production operator disabled
41 prefill route disabled
42 router disabled
43 QKV bridge disabled
44 dispatcher missing
45 runtime handles missing
46 device mismatch
47 queue mismatch
48 raw borrow unavailable
49 quarantined
50 unsupported runtime profile
51 legacy bool only admission
52 convenience context booleans all true without evidence
```

## 23.6 Execution and movement

```text
53 generic try function called from prefill
54 CPU f32 dispatcher called
55 Tensor::from_data context reupload
56 Q host upload fallback
57 K host upload fallback
58 V host upload fallback
59 output full payload readback
60 blocking poll
61 map_async on hot path
62 candidate/downstream overlap
63 output identity mismatch
```

## 23.7 Fallback

```text
64 policy denial silently converted to Burn
65 dispatcher absent converted to Burn
66 raw borrow unavailable converted to CPU roundtrip
67 dispatch failure without attribution receipt
68 fallback execution count > 1 on failed layer
69 repeated Headwise attempts after quarantine
70 mixed Headwise and Burn authority in one layer
71 Burn remainder without per-layer receipt
72 fallback output committed before Headwise failure classification
```

## 23.8 Isolation

```text
73 incremental behavior mutation
74 chunked live callsite addition
75 generic forward route mutation
76 TensorCube role mutation
77 TensorCube live dispatch
78 output authority pointer mutation
79 WGSL mutation
80 KV commit before layer closure
```

Canonical implementation target:

```text
negative_controls = 80
minimum = 72
```

---

# 24. Decision counters

Schema:

```text
ash.attn.interconnect.w3.c2.decision-counters.v1
```

Canonical 52 counters:

```text
parent_w0_mismatch
parent_w1_mismatch
parent_w2_mismatch
parent_w3_c0_mismatch
parent_w3_c1_mismatch
model_binding_mismatch
session_binding_missing
session_binding_mismatch
activation_policy_mismatch
causal_bridge_mismatch
shape_observation_mismatch
shape_reconciliation_mismatch
invocation_identity_missing
invocation_identity_mismatch
invocation_generation_duplicate
prefill_ordinal_mismatch
layer_index_mismatch
layer_count_mismatch
layer_order_mismatch
layer_missing
layer_duplicate
full_route_policy_missing
full_route_decision_missing
full_route_decision_denied
legacy_prefill_decision_read
prefill_generic_try_call
prefill_nonproduction_cpu_branch
q_cpu_materialize
k_cpu_materialize
v_cpu_materialize
context_cpu_materialize
q_host_reupload
k_host_reupload
v_host_reupload
context_host_reupload
output_host_reupload
output_value_readback
hot_path_map_async
hot_path_blocking_poll
raw_borrow_missing
device_lineage_mismatch
queue_lineage_mismatch
output_buffer_identity_mismatch
input_output_overlap
silent_burn_fallback
unattributed_burn_fallback
fallback_retry_overflow
repeated_headwise_after_quarantine
mixed_layer_output_authority
kv_commit_before_layer_closure
incremental_route_mutation
tensorcube_live_dispatch_detected
```

PASS 시 전부 0이다.

Failure injection run은 별도 expected counter receipt를 사용하며 production PASS counters에 합산하지 않는다.

---

# 25. Runtime artifact closure

Output directory:

```text
workspace/runtime/attention/interconnect/w3/c2
```

Rust gate가 다음 48개 child artifact를 순서대로 산출한다.

```text
identity.json
parent_w0_binding.json
parent_w1_shape_authority.json
parent_w2_provenance.json
parent_w3_c0_coverage.json
parent_w3_c1_policy.json
source_scope.json
prefill_session_binding.json
prefill_causal_authority_bridge.json
prefill_kernel_profile.json
prefill_shape_observation_matrix.json
prefill_shape_reconciliation_matrix.json
prefill_invocation_identity_matrix.json
prefill_admission_context_matrix.json
prefill_admission_decision_matrix.json
prefill_all_layer_coverage.json
prefill_layer_order.json
prefill_device_lineage.json
prefill_raw_borrow_receipts.json
prefill_zero_copy_inputs.json
prefill_output_ring.json
prefill_dispatch_receipts.json
prefill_output_commit.json
prefill_burn_fallback_registry.json
prefill_fallback_attribution.json
prefill_cpu_materialize_zero.json
prefill_host_reupload_zero.json
prefill_silent_fallback_zero.json
prefill_policy_live_enforcement.json
prefill_legacy_projection_retirement.json
incremental_nonmutation.json
chunked_nonmutation.json
generic_forward_nonmutation.json
tensorcube_nonmutation.json
output_authority.json
greedy_sampled_prefill_parity.json
shape_boundary_matrix.json
layer_failure_injection.json
device_mismatch_injection.json
dispatch_failure_rollback.json
negative_control_outcomes.json
decision_counters.json
static_checks.json
runtime_observations.json
prefill_activation_authority_snapshot.json
verdict.json
runtime_artifact.json
handoff_receipt.json
```

Canonical ordered-list digest:

```text
child_artifact_expected       48
child_artifact_list_sha256     756e800f2e0dca5e98fd4ec33a5dc731ea526c1f4174eb67a8e2874ed9f8cd68
serialization                  UTF-8, one filename per line, trailing LF included
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w3_c2_runtime_artifact.json

schema = ash.attn.interconnect.w3.c2.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w3_c2_local_manifest.json

schema = ash.attn.interconnect.w3.c2.local_manifest.v1
manifest self excluded from hash graph
```

코드 ZIP 제외:

```text
명세 Markdown
W3-C2 runtime artifact
W3-C2 local manifest
W3-C2 child artifacts
SHA sidecar
PowerShell/CMD helper
```

---

# 26. CLI contract

Binary:

```text
ash_attn_interconnect_w3_c2_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c2.args
```

Canonical keys:

```text
--repo-root
--parent-w0-runtime-artifact
--parent-w0-local-manifest
--parent-w1-runtime-artifact
--parent-w1-local-manifest
--parent-w2-runtime-artifact
--parent-w2-local-manifest
--parent-w3-c0-runtime-artifact
--parent-w3-c0-local-manifest
--parent-w3-c1-runtime-artifact
--parent-w3-c1-local-manifest
--verified-model-instance-binding
--model-spec
--bound-decode-session-contract
--expected-model-instance-id
--expected-full-route-policy-digest
--expected-prefill-activation-mode
--require-live-prefill-policy-enforcement
--require-all-layer-production-admission
--require-actual-runtime-shape-observation
--require-causal-authority-bridge
--require-w2-prefill-invocation-identity
--require-same-device-qkv
--require-raw-borrow-qkv
--require-zero-cpu-materialize
--require-zero-host-reupload
--require-typed-prefill-outcome
--require-explicit-burn-fallback-attribution
--require-silent-fallback-zero
--require-greedy-sampled-prefill-parity
--require-kv-commit-after-layer-closure
--forbid-prefill-legacy-bool-authority
--forbid-prefill-generic-try-path
--forbid-incremental-route-mutation
--forbid-chunked-route-mutation
--forbid-generic-forward-mutation
--forbid-tensorcube-role-mutation
--forbid-tensorcube-live-dispatch
--minimum-positive-cases
--minimum-negative-controls
--validation-mode
--negative-control-mode
--out-dir
--binding-epoch
```

Canonical count:

```text
44 key/value pairs
88 non-empty lines
```

Validation mode:

```text
fixture
physical
both
```

Promotion canonical mode:

```text
both
```

Fixture-only PASS는 implementation closure이며 production promotion receipt가 아니다.

---

# 27. Physical GPU receipt

W3-C2는 live activation이므로 promotion PASS에는 physical GPU evidence가 필요하다.

최소 physical matrix:

```text
prompt length 1
prompt length 16
prompt length 17
prompt length 64
prompt length 65
prompt length 128
prompt length 512
prompt length min(1024, max_position)
prompt length max_position, memory permitting
```

각 run:

```text
all model layers observed
all model layers admitted
all model layers Headwise committed
Q/K/V zero-copy
output zero-copy
CPU materialize 0
host reupload 0
Burn fallback 0
KV commit exact
```

메모리 한계로 max-position run을 생략하면 artifact에 `skipped`가 아니라 FAIL을 기록한다.

Profile maximum을 낮추려면 별도 명세가 필요하다.

---

# 28. PASS gate

필수 PASS:

```text
W0/W1/W2/W3-C0/W3-C1 parent exact
model instance exact
bound session contract exact
prefill activation policy exact
ProductionPrefill live enforcement active
legacy prefill decision read count 0
actual runtime shape observation exact
causal bridge exact
W2 invocation identity per layer exact
all layer count exact
all layer order exact
all layer admission disposition AdmitProductionDeviceGuarded
all layer Headwise dispatch success
same-device Q/K/V exact
RawBorrowed Q/K/V exact
output zero-copy exact
CPU QKV materialize 0
context CPU materialize 0
host reupload 0
silent fallback 0
Burn fallback 0 in positive matrix
mixed authority 0
KV commit after all-layer closure
greedy sampled prefill parity exact
incremental behavior mutation 0
chunked behavior mutation 0
generic forward mutation 0
TensorCube role mutation 0
TensorCube live dispatch 0
positive cases >= 64
negative controls >= 72
child artifacts 48/48
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
model_instance=<id>
surface=production_prefill
enforcement_mode=live_enforced
policy_authority=full_route_admission
expected_layers=<model layers>
admitted_layers=<model layers>
headwise_committed_layers=<model layers>
burn_fallback_layers=0
cpu_materialize_count=0
host_reupload_count=0
silent_fallback_count=0
raw_borrow_qkv=true
same_device_dispatch=true
full_prefill_shape_coverage=true
greedy_sampled_prefill_chain=shared
incremental_mutation=0
chunked_mutation=0
generic_forward_mutation=0
tensorcube_live_dispatch=0
output_authority=headwise
child_artifacts=48/48
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C2_HEADWISE_PREFILL_FULL_ACTIVATION_FULL_ROUTE_POLICY_LIVE_ENFORCEMENT_ALL_LAYER_PRODUCTION_ADMISSION_FULL_PREFILL_SHAPE_COVERAGE_ZERO_CPU_QKV_MATERIALIZATION_ZERO_HOST_REUPLOAD_BURN_FALLBACK_ATTRIBUTION_PREFILL_OUTPUT_AUTHORITY_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W3_C2_PREFILL_LIVE_ADMISSION_LAYER_COVERAGE_ZERO_COPY_MOVEMENT_FALLBACK_ATTRIBUTION_OR_OUTPUT_AUTHORITY_NOT_PROVEN
```

---

# 29. Direct Cargo execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c2_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c2.args"
```

Expected revision:

```text
W3-C2-headwise-prefill-full-activation-v1
```

Expected first log:

```text
[ash-attn-interconnect-w3-c2][build] revision=W3-C2-headwise-prefill-full-activation-v1 child_artifact_expected=48 child_artifact_list_sha256=756e800f2e0dca5e98fd4ec33a5dc731ea526c1f4174eb67a8e2874ed9f8cd68
```

---

# 30. Failure handling

First mismatch priority:

```text
parent closure
model/session binding
activation policy
causal bridge
runtime shape observation
shape reconciliation
invocation identity
admission context
decision disposition
layer coverage
raw-borrow/device lineage
dispatch receipt
output authority
movement counters
fallback attribution
KV commit
artifact closure
```

금지되는 보정:

```text
missing session contract reconstruction
actual Q/K/V shape 대신 ModelSpec shape 사용
policy denial을 Burn fallback으로 변경
raw borrow 실패를 UploadedFromHost로 변경
Headwise dispatch 실패를 None으로 축약
fallback receipt 없이 grouped_query_attention 실행
quarantine 후 Headwise 재시도
CPU roundtrip을 diagnostic으로 재분류
output readback을 guard telemetry로 재분류
missing layer receipt를 synthetic PASS로 채움
```

---

# 31. W3-C3 handoff

W3-C3가 입력으로 받는 것:

```text
prefill activation policy digest
prefill live enforcement receipt digest
all-layer coverage digest
causal bridge schema
runtime shape observation schema
W2 invocation identity plumbing
same-device Q/K/V receipt schema
typed execution outcome schema
fallback attribution schema
zero CPU materialize receipt
zero host reupload receipt
output authority receipt
```

W3-C3에서 재사용 가능한 구조:

```text
bound session contract ownership
actual runtime shape observation
causal bridge
invocation generation
full-route admission context
same-device dispatch outcome
fallback attribution
```

W3-C3에서 달라지는 것:

```text
surface                  ProductionIncrementalDecode
route                    IncrementalDecode
q_seq                    1
seq_kv                   dynamic
prefill ordinal          None
decode step ordinal      Some(step)
persistent KV generation exact
```

---

# 32. 최종 봉인 문장

W3-C2 PASS 시 다음을 확정한다.

```text
ASH production prefill의 모든 attention layer는 W3-C1 full-route admission policy를
실제 runtime Q/K/V shape, model/session identity, causal position, device/queue lineage와 함께 평가한다.

모든 positive production prefill layer는 AdmitProductionDeviceGuarded 결정을 받고,
same-device RawBorrowed Q/K/V를 Headwise production dispatcher에 제출하며,
Headwise downstream output을 해당 layer의 단일 output authority로 사용한다.

Production prefill에서는 CPU Q/K/V materialization, CPU context materialization,
attention payload host reupload, silent Burn fallback이 모두 0이다.

Headwise dispatch가 output commit 전에 실패하는 negative path는 typed failure와
explicit Burn fallback attribution receipt를 남기며, 같은 layer에서 fallback은 한 번만 실행되고
남은 layer는 quarantine remainder receipt를 갖는다. 이 경로는 output continuity를 제공하지만
W3-C2 activation PASS로 인정되지 않는다.

Incremental, chunked, generic forward와 TensorCube role은 이 커밋에서 변경되지 않는다.
```

아직 금지되는 주장:

```text
Headwise incremental decode가 완전 활성화됐다.
Headwise chunked decode가 구현됐다.
Generic forward bypass가 제거됐다.
TensorCube가 shadow에서 벗어났다.
Headwise resource allocation이 plateau에 도달했다.
```
