# ASH-ATTN-INTERCONNECT-W3-C0 명세

## Headwise Route Coverage Inventory /
## Prefill·Incremental·Chunked Callsite Census /
## All-Layer Route Matrix /
## GPU·CPU Materialize Branch Census /
## Host Reupload Branch Census /
## Greedy·Sampled Decode Coverage /
## Unclassified Route Zero /
## Coverage Authority Snapshot Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C0`  
> Build revision: `W3-C0-headwise-route-coverage-inventory-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W0-R2` PASS + `W1-R1` PASS + `W2-R1` PASS  
> 현재 Headwise 상태: production prefill·incremental admission 표면 존재, 전체 generation 경로 coverage 미봉인  
> 현재 TensorCube 상태: `ShadowObserverOnly`, live Q/K/V dispatch 0  
> 이 커밋의 성격: **inventory-only / behavior-preserving / route-mutation-zero**  
> 후속 커밋: `W3-C1 Headwise Full-Route Admission Policy`

---

# 0. 목적

W0~W2는 다음을 확정했다.

```text
W0  Headwise·TensorCube authority binding
W1  model/runtime shape authority
W2  lease provenance / model·layer·decode-step identity
```

그러나 현재 “Headwise가 켜져 있다”는 문장은 production generation 전체를 뜻하지 않는다.

현재 소스에는 서로 다른 attention 실행 표면이 공존한다.

```text
1. decode_state prefill
   try_grouped_query_attention_via_atlas()
   -> production device-guarded Headwise 가능
   -> None이면 Burn grouped_query_attention fallback

2. decode_state incremental decode
   try_grouped_query_attention_via_atlas()
   -> production device-guarded Headwise 가능
   -> None이면 Burn grouped_query_attention fallback

3. generic generation forward fast path
   AshDecoderBlock::forward_prepared_set()
   -> grouped_query_attention 직접 호출
   -> Headwise router 우회

4. module trace / diagnostic / repair smoke
   Headwise 시도 또는 Burn GQA 또는 CPU reference attention 혼재

5. non-production Headwise atlas branch
   dispatch_native_qkv_to_cpu_f32()
   -> CPU Vec<f32>
   -> Tensor::from_data()
   -> GPU tensor 재생성
```

W3-C0의 목적은 기능을 켜는 것이 아니다.

```text
현재 attention route를 production·generic·trace·diagnostic·reference로 분류하고,
각 callsite의 phase·layer scope·GPU/CPU movement·fallback·authority 의미를
하나의 immutable Coverage Authority Snapshot으로 봉인한다.
```

W3-C0 PASS가 확정하는 것:

```text
모든 scoped attention primitive callsite가 식별되었다.
production prefill과 incremental의 실제 call chain이 식별되었다.
greedy와 sampled가 공유하는 attention forward chain이 식별되었다.
chunked decode의 contract 존재와 production callsite 부재가 구분되었다.
Headwise를 우회하는 generic forward가 식별되었다.
CPU materialize와 host reupload branch가 식별되었다.
미분류 attention route가 0이다.
```

W3-C0 PASS가 확정하지 않는 것:

```text
Headwise가 전 경로에서 실행된다.
Headwise가 모든 layer에서 production dispatch된다.
CPU materialize branch가 제거되었다.
chunked decode가 구현되었다.
TensorCube가 shadow에서 승격되었다.
TensorCube가 live Q/K/V를 소비한다.
```

---

# 1. 현재 소스에서 확인된 사실

본 절은 W2-R1 코드 기준 source-derived inventory seed다.

## 1.1 Production prefill

`crates/model_core/src/decode_state.rs`

```text
forward_prefill
  -> decode_layers().iter().enumerate()
  -> forward_block_prefill(layer_idx, ...)
  -> try_grouped_query_attention_via_atlas(... FullPrefill ...)
  -> Some(ctx): Headwise result
  -> None: grouped_query_attention fallback
```

확정:

```text
phase                  full_prefill
layer scope            all decode_layers
Headwise attempt       있음
Burn fallback          있음
production eligibility operator policy에 의존
```

## 1.2 Production incremental decode

`crates/model_core/src/decode_state.rs`

```text
forward_last_logits_single_token
  -> decode_layers().iter().enumerate()
  -> forward_block_decode(layer_idx, ...)
  -> cached K/V + new K/V cat
  -> try_grouped_query_attention_via_atlas(... IncrementalDecode ...)
  -> Some(ctx): Headwise result
  -> None: grouped_query_attention fallback
```

확정:

```text
phase                  incremental_decode
q_seq                  1
layer scope            all decode_layers
Headwise attempt       있음
Burn fallback          있음
persistent K/V         Burn Tensor cache concat
```

## 1.3 Greedy·sampled forward convergence

현재 greedy와 sampled는 token selection 이후 로직은 다르지만 attention forward는 공유한다.

```text
greedy prefill
sampled prefill
  -> forward_prefill

greedy decode
sampled decode
  -> forward_last_logits_single_token
```

W3-C0은 다음을 구분한다.

```text
attention route convergence     shared
selector authority              separate
logit postprocessor             separate 가능
```

“sampled route가 별도 Headwise callsite를 가진다”고 기록하면 실패다.

## 1.4 Generic generation forward bypass

`crates/model_core/src/native_wgpu.rs`

```text
forward_hidden_for_generation_input
  fast path:
    for layer in model.layers
      layer.forward_prepared_set(...)
```

`crates/model_core/src/model_layers.rs`

```text
AshDecoderBlock::forward
  -> grouped_query_attention 직접 호출

AshDecoderBlock::forward_prepared_set
  -> grouped_query_attention 직접 호출
```

확정:

```text
Headwise router attempt     0
direct Burn GQA             있음
route classification        GenericModelForwardBypass
```

이 표면을 production generation과 조용히 동일시하지 않는다.

## 1.5 Headwise router gates

`NativeWgpuModel::try_grouped_query_attention_via_atlas`의 선행 gate:

```text
disable_native_headwise_atlas
disable_native_qkv_bridge
ASH_EXPERIMENTAL_NATIVE_HEADWISE_ATLAS
dispatcher presence
heads / kv_heads / head_dim geometry
causal snapshot validation
HeadwiseAttentionPromotionPolicySnapshot
headwise_production_quarantined
```

Production policy는 operator env 결속에 의존한다.

```text
ASH_HEADWISE_ATLAS_PRODUCTION
ASH_HEADWISE_ATLAS_PARENT_ARTIFACT_SHA256
ASH_HEADWISE_ATLAS_PARENT_MANIFEST_SHA256
ASH_HEADWISE_ATLAS_PROMOTE_PREFILL
ASH_HEADWISE_ATLAS_PROMOTE_INCREMENTAL
```

현재 policy validator는 다음을 강제한다.

```text
allow_chunked_decode == false
```

## 1.6 Production Headwise branch

Production route admission 시:

```text
dispatch_native_qkv_into_output_device_guarded
same-device Q/K/V
candidate output ring
downstream output ring
no output CPU readback
no output host upload
DeviceGuardDecisionToken authority
```

실패 시:

```text
headwise_production_quarantined = true
rollback counter increment
return Ok(None)
caller grouped_query_attention fallback
```

따라서 production Headwise branch는 “항상 실행”이 아니라 “admitted attempt + explicit fallback”이다.

## 1.7 Non-production Headwise branch

Production policy에 admission되지 않은 Headwise router path:

```text
dispatch_native_qkv_to_cpu_f32
  -> Vec<f32>
  -> Tensor::<NativeInferenceBackend,4>::from_data
```

분류:

```text
GPU candidate execution
GPU-to-CPU payload materialization
CPU Vec authority
CPU-to-GPU tensor reupload
```

이 경로는 zero-copy production path로 분류하면 안 된다.

## 1.8 Chunked decode

현재 source에는 다음 contract 표면이 존재한다.

```text
HeadwiseCausalRouteId::ChunkedDecode
AttentionInvocationPhase::ChunkedDecode
AttentionCausalRouteId::ChunkedDecode
promotion policy field allow_chunked_decode
```

그러나 scoped production code에서 다음은 발견되지 않는다.

```text
HeadwiseCausalPositionSnapshot::new(ChunkedDecode, ...)
production forward_chunked_decode callsite
chunked decode KV transaction
```

W3-C0 canonical verdict:

```text
contract_surface_present       true
production_callsite_present    false
production_coverage            AbsentNotImplemented
```

이를 `HeadwiseUnsupported`, `HeadwiseDisabled`, `Unclassified` 중 하나로 뭉개지 않는다.

---

# 2. 패치 경계

W3-C0에서 허용:

```text
source inventory module 추가
coverage schema 추가
source scanner / classifier 추가
Rust gate binary 추가
CLI response file 추가
source digest 계산
parent artifact revalidation
inventory artifact 작성
```

W3-C0에서 금지:

```text
try_grouped_query_attention_via_atlas의 실행 동작 변경
Headwise promotion policy 변경
allow_chunked_decode 변경
CPU materialize branch 제거
Burn fallback 제거
generic forward route 변경
route pointer write
Headwise authority state 변경
TensorCube role 변경
TensorCube live dispatch
Q/K/V capture
KV cache layout 변경
WGSL 변경
```

허용되는 production source 수정:

```text
없음
```

inventory code를 export하기 위한 `lib.rs`, gate 등록을 위한 `Cargo.toml` 수정만 허용한다.

---

# 3. Source scope

Canonical Rust source scope:

```text
crates/model_core/src/decode_state.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/model_layers.rs
crates/model_core/src/headwise_attention_promotion.rs
crates/model_core/src/attention_invocation_identity.rs
crates/model_core/src/attention_runtime_shape_authority.rs
crates/burn_webgpu_backend/src/headwise_causal.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
```

Reference classification scope:

```text
crates/model_core/src/reference_math.rs
```

Orchestrator evidence scope:

```text
current W0/W1/W2 gate binaries
current Headwise promotion gate binary
```

다음은 기본 inventory scope에서 제외한다.

```text
tests fixture source, 별도 ValidationFixture 분류가 없는 경우
archived generated source
target/
workspace/runtime/
code bake manifests
Markdown specs
PowerShell/CMD wrappers
```

Source scope 자체가 artifact에 기록되며, 파일 추가·삭제는 후속 gate에서 drift로 감지된다.

---

# 4. Stable callsite identity

라인 번호는 callsite identity가 아니다.

Schema:

```text
ash.attn.interconnect.w3.c0.callsite.v1
```

Stable ID 형식:

```text
<crate>::<module>::<enclosing_fn>::<primitive>::<ordinal_within_fn>
```

예:

```text
model_core::decode_state::forward_block_prefill::try_headwise::0
model_core::decode_state::forward_block_prefill::burn_gqa_fallback::0
model_core::decode_state::forward_block_decode::try_headwise::0
model_core::decode_state::forward_block_decode::burn_gqa_fallback::0
model_core::native_wgpu::try_grouped_query_attention_via_atlas::device_guarded_dispatch::0
model_core::native_wgpu::try_grouped_query_attention_via_atlas::cpu_f32_materialize::0
model_core::native_wgpu::try_grouped_query_attention_via_atlas::tensor_from_cpu_reupload::0
model_core::model_layers::AshDecoderBlock_forward::burn_gqa_direct::0
model_core::model_layers::AshDecoderBlock_forward_prepared_set::burn_gqa_direct::0
```

Callsite digest 입력:

```text
stable_id
source_relative_path
enclosing_item_kind
enclosing_item_name
primitive_kind
normalized_argument_shape
branch_ancestor_signature
classification
```

라인·컬럼은 관측값으로 기록하지만 digest authority에 넣지 않는다.

---

# 5. Attention primitive registry

W3-C0 scanner가 반드시 식별할 primitive:

```text
try_grouped_query_attention_via_atlas
dispatch_native_qkv_into_output_device_guarded
dispatch_native_qkv_to_cpu_f32
grouped_query_attention
causal_attention
causal_attention_batched
Tensor::<NativeInferenceBackend,4>::from_data
into_data().to_vec::<f32>() within attention route
```

보조 primitive:

```text
HeadwiseCausalPositionSnapshot::new
HeadwiseAttentionPromotionPolicySnapshot::new
headwise_atlas_production_requested
headwise_production_quarantined
```

새 attention primitive가 scope에 등장했는데 registry에 없으면 `UnclassifiedPrimitive`로 실패한다.

---

# 6. Classification taxonomy

## 6.1 Surface class

```rust
pub enum AttentionSurfaceClass {
    ProductionPrefill,
    ProductionIncrementalDecode,
    ProductionChunkedDecode,
    GenericGenerationForward,
    ModuleTrace,
    DiagnosticSmoke,
    ValidationGate,
    CpuReference,
}
```

## 6.2 Route class

```rust
pub enum AttentionRouteClass {
    HeadwiseProductionDeviceGuarded,
    HeadwiseNonProductionCpuRoundtrip,
    BurnGroupedQueryAttentionFallback,
    BurnGroupedQueryAttentionDirect,
    CpuReferenceAttention,
    ContractOnlyNoLiveCallsite,
}
```

## 6.3 Movement class

```rust
pub enum AttentionDataMovementClass {
    SameDeviceZeroCopy,
    GpuResidentBurnTensor,
    GpuToCpuMaterialize,
    CpuToGpuReupload,
    CpuOnlyReference,
    NoPayloadMovement,
}
```

## 6.4 Authority class

```rust
pub enum AttentionAuthorityClass {
    HeadwiseOutputAuthorityCandidate,
    BurnFallbackOutputAuthority,
    DiagnosticOnly,
    TraceOnly,
    ReferenceOnly,
    ContractOnly,
}
```

## 6.5 Coverage status

```rust
pub enum HeadwiseCoverageStatus {
    ProductionAdmittedPossible,
    AttemptedButFallbackPossible,
    BypassedDirectBurn,
    CpuRoundtripOnly,
    AbsentNotImplemented,
    DiagnosticOnly,
    ReferenceOnly,
}
```

`Disabled`, `Unsupported`, `AbsentNotImplemented`를 같은 값으로 쓰지 않는다.

---

# 7. Call chain inventory

Schema:

```text
ash.attn.interconnect.w3.c0.call-chain.v1
```

필드:

```text
chain_id
entrypoint
selector_mode
generation_phase
route_id
functions
attention_callsites
layer_loop_owner
layer_count_source
kv_owner
fallback_edges
cpu_materialize_edges
host_reupload_edges
terminal_output_authority
chain_digest
```

## 7.1 Greedy prefill

Expected chain:

```text
prefill
  -> forward_prefill
  -> forward_block_prefill per layer
  -> try_headwise
  -> Headwise production OR Burn fallback
```

## 7.2 Sampled prefill

Expected chain:

```text
prefill_with_sampling_choice
  -> forward_prefill
  -> same attention chain as greedy prefill
```

## 7.3 Greedy incremental

Expected chain:

```text
decode_step
  -> forward_last_logits_single_token
  -> forward_block_decode per layer
  -> try_headwise
  -> Headwise production OR Burn fallback
```

## 7.4 Sampled incremental

Expected chain:

```text
decode_step_with_sampling_choice
  -> forward_last_logits_single_token
  -> same attention chain as greedy incremental
```

## 7.5 Chunked

Expected current inventory:

```text
entrypoint            absent
position constructor  absent
layer loop            absent
live attention call   absent
contract enum         present
policy field          present but validator-forbidden
```

---

# 8. Layer coverage matrix

Schema:

```text
ash.attn.interconnect.w3.c0.layer-coverage-matrix.v1
```

필드:

```text
model_instance_id
model_layer_count
layer_count_source
surface_class
phase
entrypoint
layer_loop_kind
layer_index_source
expected_layers
headwise_attempt_layers
burn_fallback_layers
direct_burn_layers
unreachable_layers
coverage_status
matrix_digest
```

W3-C0은 runtime dispatch 횟수를 주장하지 않는다.

Static layer-loop coverage를 다음처럼 표현한다.

```text
forward_prefill
  layer loop = decode_layers().iter().enumerate()
  static intended coverage = [0, num_layers)

forward_last_logits_single_token
  layer loop = decode_layers().iter().enumerate()
  static intended coverage = [0, num_layers)

generic forward
  layer loop = model.layers
  Headwise attempt = 0
```

`static intended coverage`와 `runtime observed coverage`를 분리한다.

W3-C0에는 runtime observed coverage가 없다.

---

# 9. Phase coverage matrix

Canonical matrix columns:

```text
surface
phase
position route
entrypoint exists
Headwise attempt exists
production policy can admit
Headwise failure fallback exists
Burn direct bypass exists
CPU materialize exists
host reupload exists
all-layer loop exists
selector modes sharing chain
coverage verdict
```

Expected current rows:

```text
ProductionPrefill
  route FullPrefill
  Headwise attempt yes
  production admission configurable
  Burn fallback yes
  all-layer loop yes

ProductionIncrementalDecode
  route IncrementalDecode
  Headwise attempt yes
  production admission configurable
  Burn fallback yes
  all-layer loop yes

ProductionChunkedDecode
  route contract present
  live entrypoint no
  production policy forbidden
  verdict AbsentNotImplemented

GenericGenerationForward
  Headwise attempt no
  Burn direct yes
  verdict BypassedDirectBurn
```

---

# 10. CPU materialize census

Schema:

```text
ash.attn.interconnect.w3.c0.cpu-materialize-inventory.v1
```

필드:

```text
callsite_id
source_surface
source_function
trigger_branch
input_storage
gpu_dispatch_before_materialize
materialized_type
materialize_api
output_consumer
production_reachable
classification
```

Canonical known attention materialize branch:

```text
try_grouped_query_attention_via_atlas
  non-production path
  dispatch_native_qkv_to_cpu_f32
  returns Vec<f32>
```

다음은 별도 분류한다.

```text
attention output materialize
logits materialize
weight diagnostic materialize
module trace materialize
```

W3-C0은 attention route inventory에서 logits·weight materialization을 수치에 섞지 않는다.

---

# 11. Host reupload census

Schema:

```text
ash.attn.interconnect.w3.c0.host-reupload-inventory.v1
```

Canonical known branch:

```text
CPU Vec<f32>
  -> Tensor::<NativeInferenceBackend,4>::from_data
  -> device = self.device
```

분류:

```text
source route        HeadwiseNonProductionCpuRoundtrip
movement            CpuToGpuReupload
production zero-copy false
```

Raw bridge의 `UploadedFromHost` fallback도 inventory 대상이다.

다음은 서로 다른 항목이다.

```text
Headwise output Vec 재업로드
Raw bridge Q/K/V host-upload fallback
input token tensor creation
```

input token ID의 `Tensor::from_data`는 Q/K/V attention payload reupload가 아니다.

---

# 12. Headwise policy inventory

Schema:

```text
ash.attn.interconnect.w3.c0.headwise-policy-inventory.v1
```

필드:

```text
policy_schema
binding_source
operator_env_keys
allow_full_prefill
allow_incremental_decode
allow_chunked_decode
chunked_validator_constraint
quarantine_state_owner
policy_digest_owner
```

W3-C0은 실제 env 값을 production 기본값으로 간주하지 않는다.

구분:

```text
policy capability       source contract
operator selection      runtime environment
runtime dispatch        actual execution evidence
```

---

# 13. Generic forward inventory

Generic forward는 다음 이유로 반드시 별도 surface다.

```text
NativeWgpuModel::forward_hidden_for_generation_input fast path
  -> AshDecoderBlock::forward_prepared_set
  -> grouped_query_attention
```

Inventory 필드:

```text
entrypoint
caller set
production reachability
layer loop
attention primitive
Headwise attempt count
fallback semantics
```

W3-C0 PASS 조건:

```text
generic forward bypass가 명시적으로 기록됨
production decode_state chain과 병합되지 않음
Headwise full coverage로 오인되지 않음
```

---

# 14. Trace·diagnostic·reference 분리

## 14.1 Module trace

`trace_module_native_hidden_pair`는 Headwise router를 시도하지만 production generation evidence가 아니다.

```text
surface = ModuleTrace
authority = TraceOnly
```

## 14.2 Diagnostic smoke

TensorCube decode repair·overlay·parity smoke에서 사용하는 direct Burn GQA는 production Headwise bypass 증거로 합산하지 않는다.

```text
surface = DiagnosticSmoke
authority = DiagnosticOnly
```

## 14.3 CPU reference

```text
causal_attention
causal_attention_batched
```

분류:

```text
surface = CpuReference
authority = ReferenceOnly
```

Production fallback이라고 추정하지 않는다.

---

# 15. Coverage Authority Snapshot

Schema:

```text
ash.attn.interconnect.w3.c0.coverage-authority.v1
```

필드:

```text
schema
patch_id
build_revision
model_instance_id
parent_w0_digest
parent_w1_digest
parent_w2_digest
source_scope_digest
source_file_digests
attention_primitive_registry_digest
callsite_inventory_digest
call_chain_inventory_digest
layer_coverage_matrix_digest
phase_coverage_matrix_digest
cpu_materialize_inventory_digest
host_reupload_inventory_digest
production_prefill_status
production_incremental_status
production_chunked_status
generic_forward_status
greedy_sampled_attention_chain_shared
unclassified_primitive_count
unclassified_callsite_count
route_mutation_count
tensorcube_live_dispatch_count
snapshot_digest
pass
failures
```

Expected status:

```text
production_prefill_status
  AttemptedButFallbackPossible

production_incremental_status
  AttemptedButFallbackPossible

production_chunked_status
  AbsentNotImplemented

generic_forward_status
  BypassedDirectBurn
```

W3-C0은 이 결과를 “실패”로 보지 않는다.

현재 상태를 정확히 분류했는지가 PASS 기준이다.

---

# 16. Source scanner 계약

권장 구현:

```text
Rust source를 UTF-8로 읽음
주석·문자열 literal을 구분 가능한 tokenizer 사용
item/function boundary 식별
primitive call token 식별
branch ancestor signature 계산
manual classification registry와 join
```

정규식만으로 문자열 안의 함수 이름을 callsite로 계산하면 안 된다.

권장 선택:

```text
syn parser + visit feature
```

새 dependency가 부담되면 최소 tokenizer를 구현할 수 있으나 다음을 통과해야 한다.

```text
line comment exclusion
block comment exclusion
string literal exclusion
raw string exclusion
macro token distinction
method call vs free function distinction
```

Scanner output은 stable callsite ID로 정렬한다.

정렬:

```text
surface rank
source path
item name
primitive rank
ordinal
```

---

# 17. Source anchor receipt

각 registered callsite에는 다음 anchor를 둔다.

```text
source_relative_path
enclosing_item_name
primitive_name
expected_ordinal
normalized_context_digest
```

금지:

```text
absolute Windows path
line number only identity
전체 repository hash 하나만 사용
substring 한 개만으로 callsite 인정
```

Source drift가 발생하면:

```text
anchor missing
anchor duplicate
context digest mismatch
new unclassified primitive
```

중 첫 항목으로 실패한다.

---

# 18. Required current callsite classes

최소 다음 callsite class가 inventory에 있어야 한다.

```text
01 prefill try_headwise
02 prefill burn fallback
03 incremental try_headwise
04 incremental burn fallback
05 module trace try_headwise
06 module trace burn fallback
07 production device-guarded dispatch
08 production rollback-to-None
09 non-production CPU f32 materialize
10 non-production Tensor::from_data reupload
11 generic forward layer.forward_prepared_set bypass
12 AshDecoderBlock::forward direct Burn GQA
13 AshDecoderBlock::forward_prepared_set direct Burn GQA
14 traced generation loop direct Burn GQA
15 diagnostic repair smoke direct Burn GQA
16 diagnostic overlay parity direct Burn GQA
17 CPU causal_attention
18 CPU causal_attention_batched
19 promotion policy full-prefill field
20 promotion policy incremental field
21 promotion policy chunked-forbidden rule
22 operator env production gate
23 router env disable gate
24 production quarantine gate
25 Raw bridge host-upload fallback surface
26 chunked route contract-only surface
```

숫자는 canonical minimum class 수이며 동일 class의 callsite가 여러 개일 수 있다.

---

# 19. Greedy·sampled coverage receipt

Schema:

```text
ash.attn.interconnect.w3.c0.selector-path-coverage.v1
```

필드:

```text
selector_mode
prefill_entrypoint
incremental_entrypoint
attention_prefill_chain_id
attention_incremental_chain_id
selector_specific_attention_callsite_count
shared_chain_exact
receipt_digest
```

PASS:

```text
greedy attention prefill chain == sampled attention prefill chain
greedy attention incremental chain == sampled attention incremental chain
selector-specific attention primitive callsite count == 0
```

단, selector 이후 logits 처리의 차이는 허용한다.

---

# 20. Unclassified route zero

Unclassified는 다음 중 하나다.

```text
registry에 없는 attention primitive
surface가 없는 callsite
route class가 없는 callsite
movement class가 없는 payload movement callsite
authority class가 없는 output path
production reachability가 판단되지 않은 callsite
```

`Unknown`을 `DiagnosticOnly`로 조용히 내리는 폴백은 금지한다.

Canonical PASS:

```text
unclassified_primitive_count = 0
unclassified_callsite_count = 0
unclassified_production_reachable_count = 0
```

---

# 21. Decision counters

Schema:

```text
ash.attn.interconnect.w3.c0.decision-counters.v1
```

Canonical 34 counters:

```text
parent_w0_binding_mismatch
parent_w1_shape_authority_mismatch
parent_w2_provenance_mismatch
source_scope_missing
source_file_missing
source_file_digest_failure
source_parse_failure
function_anchor_missing
function_anchor_duplicate
callsite_id_collision
attention_primitive_unclassified
attention_callsite_unclassified
production_entrypoint_unclassified
phase_unclassified
layer_scope_unclassified
prefill_chain_unresolved
incremental_chain_unresolved
chunked_contract_unresolved
greedy_chain_unresolved
sampled_chain_unresolved
greedy_sampled_chain_divergence
generic_forward_bypass_unclassified
headwise_gate_unclassified
production_policy_unclassified
production_dispatch_unclassified
burn_fallback_unclassified
cpu_materialize_unclassified
host_reupload_unclassified
module_trace_misclassified
diagnostic_route_misclassified
reference_route_misclassified
route_mutation_detected
tensorcube_live_dispatch_detected
output_authority_mutation_detected
```

PASS 조건은 전부 0이다.

현재 chunked production callsite 부재는 counter가 아니다.

`chunked_contract_unresolved`는 contract 존재·live 부재를 구분하지 못했을 때만 증가한다.

---

# 22. Negative controls

최소 44건을 실행한다.

## 22.1 Parent closure

```text
01 W0 digest flip
02 W1 digest flip
03 W2 digest flip
```

## 22.2 Source scope

```text
04 required source file missing
05 source file invalid UTF-8
06 source parse failure
07 duplicate source path
08 out-of-scope generated file admission
```

## 22.3 Anchor and identity

```text
09 enclosing function renamed without registry update
10 primitive removed
11 primitive duplicated in same function
12 ordinal collision
13 stable callsite ID collision
14 line-number-only identity fixture
15 absolute path identity fixture
```

## 22.4 Primitive discovery

```text
16 new try_headwise call unclassified
17 new grouped_query_attention call unclassified
18 new device-guarded dispatch unclassified
19 new CPU f32 materialize unclassified
20 new Tensor::from_data attention reupload unclassified
21 new causal_attention call unclassified
```

## 22.5 Route classification

```text
22 prefill classified as diagnostic
23 incremental classified as generic
24 chunked contract classified as live
25 generic forward classified as production Headwise
26 module trace classified as production generation
27 diagnostic smoke classified as production
28 CPU reference classified as Burn fallback
```

## 22.6 Movement classification

```text
29 CPU f32 branch classified zero-copy
30 Tensor::from_data reupload omitted
31 input token Tensor::from_data misclassified as attention reupload
32 logits readback misclassified as attention context readback
33 raw host upload fallback omitted
```

## 22.7 Chain coverage

```text
34 greedy prefill chain missing
35 sampled prefill chain missing
36 greedy incremental chain missing
37 sampled incremental chain missing
38 sampled fake separate attention callsite
39 layer loop classified single-layer
40 chunked absent classified disabled
```

## 22.8 Isolation

```text
41 route mutation attempt
42 Headwise policy mutation attempt
43 TensorCube live dispatch attempt
44 output authority mutation attempt
```

각 negative control:

```text
rejected == true
production source mutation == 0
route mutation == 0
TensorCube live dispatch == 0
partial authority snapshot publish == 0
```

---

# 23. Static checks

필수 정적 검사:

```text
scoped try_grouped_query_attention_via_atlas callsite count classified 100%
scoped grouped_query_attention callsite count classified 100%
scoped dispatch_native_qkv_to_cpu_f32 callsite count classified 100%
scoped device_guarded dispatch callsite count classified 100%
attention Tensor::from_data reupload classified 100%
chunked production constructor count 0, current baseline
chunked contract surface count > 0
generic forward Headwise attempt count 0, current baseline
greedy/sampled shared attention chain true
production source behavioral diff count 0
WGSL changed file count 0
route pointer write count 0
TensorCube dispatch added count 0
```

W3-C0 implementation 파일이 source scope에 자기 자신을 넣어 recursive inventory를 만들면 안 된다.

---

# 24. Implementation files

신설 권장:

```text
crates/model_core/src/headwise_route_coverage_inventory.rs
crates/orchestrator_local/src/attention_interconnect_w3_c0_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w3_c0_gate.rs
specs/cli/ash_attn_interconnect_w3_c0.args
```

수정 허용:

```text
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

분석 대상이지만 수정 금지:

```text
crates/model_core/src/decode_state.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/model_layers.rs
crates/model_core/src/headwise_attention_promotion.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
```

W3-C0 코드 bake에서 위 수정 금지 파일 digest가 부모 W2-R1과 달라지면 실패한다.

---

# 25. Artifact 산출

출력 디렉터리:

```text
workspace/runtime/attention/interconnect/w3/c0
```

Rust gate가 다음 36개 child artifact를 순서대로 산출한다.

```text
identity.json
parent_w0_binding.json
parent_w1_shape_authority.json
parent_w2_provenance.json
source_scope.json
source_file_digests.json
attention_primitive_registry.json
callsite_inventory.json
call_chain_inventory.json
production_generation_entrypoints.json
prefill_route_inventory.json
incremental_route_inventory.json
chunked_route_inventory.json
greedy_route_inventory.json
sampled_route_inventory.json
generic_forward_inventory.json
module_trace_inventory.json
diagnostic_route_inventory.json
reference_cpu_inventory.json
headwise_gate_inventory.json
production_policy_inventory.json
headwise_dispatch_inventory.json
burn_fallback_inventory.json
cpu_materialize_inventory.json
host_reupload_inventory.json
layer_coverage_matrix.json
phase_coverage_matrix.json
route_classification_matrix.json
unclassified_route_report.json
source_anchor_receipts.json
negative_control_outcomes.json
decision_counters.json
static_checks.json
coverage_authority_snapshot.json
verdict.json
runtime_artifact.json
```

Canonical ordered list:

```text
child_artifact_expected       36
child_artifact_list_sha256     54f7adcb85edf8e12083c525ac219886836d862cf44d01b96be5954dd34c127d
serialization                  UTF-8, one filename per line, trailing LF included
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w3_c0_runtime_artifact.json

schema = ash.attn.interconnect.w3.c0.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/
ash_attn_interconnect_w3_c0_local_manifest.json

schema = ash.attn.interconnect.w3.c0.local_manifest.v1
manifest self excluded from hash graph
```

코드 ZIP 제외:

```text
명세 Markdown
W3-C0 runtime artifact
W3-C0 local manifest
W3-C0 child artifacts
SHA-256 sidecar
helper PowerShell/CMD
```

---

# 26. CLI 계약

Binary:

```text
ash_attn_interconnect_w3_c0_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c0.args
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
--verified-model-instance-binding
--model-spec
--source-scope-file
--require-production-prefill-chain
--require-production-incremental-chain
--require-chunked-contract-surface
--require-chunked-production-callsite-absent
--require-greedy-sampled-shared-forward
--require-generic-forward-bypass-inventory
--require-headwise-policy-inventory
--require-device-guarded-dispatch-inventory
--require-burn-fallback-inventory
--require-cpu-materialize-inventory
--require-host-reupload-inventory
--require-module-trace-separation
--require-diagnostic-separation
--require-reference-separation
--require-unclassified-zero
--forbid-production-source-mutation
--forbid-route-mutation
--forbid-tensorcube-live-dispatch
--forbid-output-authority-mutation
--minimum-callsite-classes
--minimum-negative-controls
--negative-control-mode
--out-dir
--binding-epoch
```

Canonical count:

```text
34 key/value pairs
68 non-empty lines
```

`--source-scope-file`은 Rust gate가 읽는 canonical source path list다.

source scope file은 명세가 아니라 CLI fixture이며 코드 ZIP에 포함할 수 있다.

---

# 27. PASS gate

필수 PASS:

```text
W0-R2 parent exact
W1-R1 parent exact
W2-R1 parent exact
model instance exact
source scope complete
source parse complete
all registered anchors exact
all attention primitives classified
all attention callsites classified
production prefill chain resolved
production incremental chain resolved
chunked contract present
chunked production callsite absent, current baseline
Greedy·sampled shared attention chain exact
generic forward bypass explicitly inventoried
Headwise policy gates inventoried
production device-guarded branch inventoried
Burn fallback branch inventoried
CPU materialize branch inventoried
host reupload branch inventoried
module trace separated
diagnostic routes separated
CPU reference routes separated
unclassified primitive 0
unclassified callsite 0
production source behavioral mutation 0
route mutation 0
TensorCube live dispatch 0
output authority mutation 0
negative controls >= 44
child artifacts 36/36
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
model_instance=<id>
coverage_authority=source_inventory
prefill=attempted_but_fallback_possible
incremental=attempted_but_fallback_possible
chunked=contract_present_live_absent
generic_forward=bypassed_direct_burn
greedy_sampled_attention_chain=shared
cpu_materialize_branches>=1
host_reupload_branches>=1
unclassified_primitives=0
unclassified_callsites=0
route_mutation=0
tensorcube_live_dispatch=0
output_authority=headwise
child_artifacts=36/36
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C0_HEADWISE_ROUTE_COVERAGE_INVENTORY_PREFILL_INCREMENTAL_CHUNKED_CALLSITE_CENSUS_ALL_LAYER_ROUTE_MATRIX_CPU_MATERIALIZE_HOST_REUPLOAD_GREEDY_SAMPLED_SHARED_CHAIN_UNCLASSIFIED_ROUTE_ZERO_COVERAGE_AUTHORITY_SNAPSHOT_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W3_C0_ATTENTION_ROUTE_CALLSITE_FALLBACK_MOVEMENT_OR_COVERAGE_INVENTORY_INCOMPLETE
```

---

# 28. 직접 Cargo 실행

저장소 루트:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c0_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c0.args"
```

정상 시작 revision:

```text
W3-C0-headwise-route-coverage-inventory-v1
```

W3-C0는 GPU dispatch를 실행하지 않는 source inventory gate이므로 physical GPU가 없어도 source classification은 가능해야 한다.

단, 부모 artifact와 model binding은 exact revalidation한다.

---

# 29. 실패 처리

첫 mismatch 우선순위:

```text
parent closure
source scope
source parse
anchor identity
primitive classification
callsite classification
production chain
movement classification
layer/phase matrix
unclassified zero
artifact closure
```

금지되는 보정:

```text
새 callsite를 DiagnosticOnly로 자동 분류
chunked 부재를 HeadwiseDisabled로 기록
CPU materialize를 BurnGpuResident로 기록
Tensor::from_data reupload를 생략
generic forward를 production decode_state와 합침
sampled route를 별도 attention chain으로 꾸밈
line number 변경을 새로운 callsite로 취급
missing source를 warning으로 통과
```

실패 시 production behavior는 그대로 유지한다.

---

# 30. W3-C1 handoff

W3-C0 artifact는 W3-C1의 유일한 coverage parent다.

W3-C1은 다음을 입력으로 받는다.

```text
coverage authority snapshot digest
production prefill call chain IDs
production incremental call chain IDs
chunked absent receipt
generic forward bypass callsite IDs
CPU materialize callsite IDs
host reupload callsite IDs
policy gate callsite IDs
```

W3-C1에서 처음 허용되는 것:

```text
통합 HeadwiseFullRouteAdmissionDecision 설계
callsite-local gate 제거 계획
production route policy 통합
```

W3-C1에서도 아직 production dispatch behavior를 켜지 않는다.

실제 prefill 활성화는 W3-C2다.

---

# 31. 최종 봉인 문장

W3-C0 PASS 시 다음만 확정한다.

```text
현재 ASH Native WebGPU attention 실행 표면의 모든 scoped callsite가
production prefill, production incremental decode, contract-only chunked decode,
generic generation forward, module trace, diagnostic smoke, CPU reference로 분류되었다.

Production prefill과 incremental decode는 모든 decode layer에서
Headwise router를 시도할 수 있으나 Burn grouped-query-attention fallback을 보유하며,
operator-bound promotion policy와 quarantine 상태에 따라 실제 production dispatch 여부가 달라진다.

Generic generation forward는 현재 Headwise router를 우회하여
AshDecoderBlock의 Burn grouped-query-attention을 직접 사용한다.

Chunked decode는 route·shape·policy contract는 존재하지만
production constructor와 live callsite가 없다.

Non-production Headwise atlas 경로에는 GPU output의 CPU f32 materialization과
Tensor::from_data를 통한 GPU reupload가 존재한다.

Greedy와 sampled generation은 attention forward chain을 공유하며,
selector 이후 단계만 분기한다.

미분류 attention primitive와 callsite는 0이며,
이 커밋은 route·output authority·TensorCube 역할을 변경하지 않았다.
```

아직 금지되는 주장:

```text
Headwise가 완전히 켜졌다.
CPU materialize가 제거됐다.
chunked decode가 지원된다.
TensorCube가 production candidate가 됐다.
```
