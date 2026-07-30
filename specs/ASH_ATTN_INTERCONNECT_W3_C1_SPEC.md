# ASH-ATTN-INTERCONNECT-W3-C1 명세

## Headwise Full-Route Admission Policy /
## Model·Shape·Device Eligibility /
## Prefill·Incremental·Chunked Unified Decision /
## Generic Forward Bypass Reconciliation /
## Fail-Closed Fallback Classification /
## Route Decision SSOT Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C1`  
> Build revision: `W3-C1-headwise-full-route-admission-policy-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C0` PASS  
> Full canonical source SHA-256: `abeabb733fa0aa784b695d4c59e1772577ecd51a95032805377634ad36ffffd0`  
> production attention output authority: `Headwise` 유지  
> TensorCube role: `ShadowObserverOnly` 유지  
> 이 커밋의 성격: policy authority migration / compatibility projection / execution behavior preservation  
> 후속 커밋: `W3-C2 Headwise Prefill Full Activation`

---

# 0. 목적

W3-C0는 현재 route를 다음과 같이 봉인했다.

```text
production prefill       attempted_but_fallback_possible
production incremental   attempted_but_fallback_possible
production chunked       contract_present_live_absent
generic forward          bypassed_direct_burn
CPU materialize          1 branch
host reupload             2 branches
unclassified             0
```

W3-C1은 분산된 operator env, legacy route bool, model/shape/device 조건, quarantine, fallback 분류를 하나의 immutable policy authority와 deterministic decision 함수로 통합한다.

W3-C1 PASS가 뜻하는 것:

```text
operator intent가 model bind 시 1회 캡처된다.
HeadwiseFullRouteAdmissionPolicySnapshot이 단일 policy SSOT다.
prefill·incremental·chunked·generic forward가 같은 decision taxonomy를 사용한다.
chunked live callsite 부재가 explicit denial로 표현된다.
generic forward direct Burn 경로가 reconciliation blocker로 표현된다.
legacy promotion policy는 full-route policy의 exact compatibility projection이다.
현재 production 실행 결과와 authority는 변경되지 않는다.
```

W3-C1 PASS가 뜻하지 않는 것:

```text
Headwise prefill 또는 incremental이 완전 활성화됐다.
chunked live callsite가 구현됐다.
generic forward가 Headwise로 전환됐다.
Burn fallback 또는 CPU roundtrip이 제거됐다.
TensorCube가 shadow에서 벗어났다.
```

---

# 1. Parent closure

필수 부모:

```text
W0-R2
  output_authority=headwise
  tensorcube_role=shadow_observer_only
  route_mutation=0
  stage_mutation=0

W1-R1
  shape_authority=model_spec_plus_runtime_dims
  q_seq=1 admitted
  dynamic KV geometry admitted

W2-R1
  explicit model·layer·decode-step identity
  device·queue lineage exact
  generation domains separated
  freshness attention-invocation-scoped

W3-C0
  coverage_authority=source_inventory
  prefill=attempted_but_fallback_possible
  incremental=attempted_but_fallback_possible
  chunked=contract_present_live_absent
  generic_forward=bypassed_direct_burn
  unclassified primitives=0
  unclassified callsites=0
```

필수 parent digest:

```text
w0_binding_digest
w1_shape_authority_digest
w2_provenance_authority_digest
w3_c0_coverage_authority_snapshot_digest
w3_c0_source_scope_digest
```

Coverage drift가 감지되면 W3-C0 재실행을 요구하고 W3-C1을 중단한다.

---

# 2. Authority chain

```text
VerifiedModelInstanceBinding
  -> W0 authority
  -> W1 shape authority
  -> W2 identity/provenance
  -> W3-C0 coverage authority
  -> HeadwiseOperatorIntentSnapshot
  -> HeadwiseFullRouteAdmissionPolicySnapshot
  -> HeadwiseFullRouteAdmissionContext
  -> HeadwiseFullRouteAdmissionDecision
  -> HeadwiseLegacyPromotionProjection
```

규칙:

```text
legacy projection이 full-route policy를 역생성하지 않는다.
per-call decision은 policy와 context의 순수 함수다.
decision은 route pointer, output authority, TensorCube role을 수정하지 않는다.
```

---

# 3. Runtime surface와 readiness

```rust
pub enum HeadwiseRuntimeSurfaceId {
    ProductionPrefill,
    ProductionIncrementalDecode,
    ProductionChunkedDecode,
    GenericGenerationForward,
    ModuleTrace,
    DiagnosticSmoke,
}
```

```rust
pub enum HeadwiseRouteReadiness {
    LiveCallsitePresent,
    ContractPresentLiveCallsiteAbsent,
    BypassRequiresCanonicalInvocation,
    DiagnosticOnly,
}
```

Canonical mapping:

```text
ProductionPrefill            LiveCallsitePresent
ProductionIncrementalDecode  LiveCallsitePresent
ProductionChunkedDecode      ContractPresentLiveCallsiteAbsent
GenericGenerationForward     BypassRequiresCanonicalInvocation
ModuleTrace                  DiagnosticOnly
DiagnosticSmoke              DiagnosticOnly
```

W3-C1 enforcement mode:

```text
CompatibilityProjection
```

`FullRouteEnforced`는 W3-C2 이후 route별 activation receipt가 누적된 뒤에만 허용한다.

---

# 4. Operator intent

Schema:

```text
ash.attn.interconnect.w3.c1.operator-intent.v1
```

필드:

```text
model_instance_id
runtime_process_epoch
experimental_router_enabled
production_requested
promote_prefill_requested
promote_incremental_requested
promote_chunked_requested
reconcile_generic_forward_requested
raw_borrow_required
disable_native_headwise_atlas
disable_native_qkv_bridge
parent_artifact_digest_input
parent_manifest_digest_input
environment_capture_complete
captured_before_first_forward
intent_digest
```

환경 입력은 model bind 시 1회만 읽는다.

```text
ASH_EXPERIMENTAL_NATIVE_HEADWISE_ATLAS
ASH_HEADWISE_ATLAS_PRODUCTION
ASH_HEADWISE_ATLAS_PARENT_ARTIFACT_SHA256
ASH_HEADWISE_ATLAS_PARENT_MANIFEST_SHA256
ASH_HEADWISE_ATLAS_PROMOTE_PREFILL
ASH_HEADWISE_ATLAS_PROMOTE_INCREMENTAL
ASH_HEADWISE_ATLAS_PROMOTE_CHUNKED
ASH_HEADWISE_ATLAS_RECONCILE_GENERIC_FORWARD
ASH_EXPERIMENTAL_NATIVE_RAW_BORROW_REQUIRED
```

금지:

```text
attention call마다 env 재조회
누락 parent digest 자동 보정
runtime env 변경으로 기존 model policy 변경
```

---

# 5. Full-route policy SSOT

Schema:

```text
ash.attn.interconnect.w3.c1.full-route-policy.v1
```

필수 필드:

```text
model_instance_id
model_instance_binding_digest
effective_runtime_binding_digest
w0_binding_digest
w1_shape_authority_digest
w2_provenance_authority_digest
w3_c0_coverage_snapshot_digest
w3_c0_source_scope_digest
operator_intent_digest
enforcement_mode
required_production_surfaces
route_readiness
allow_prefill_intent
allow_incremental_intent
allow_chunked_intent
reconcile_generic_forward_intent
burn_gpu_fallback_policy
nonproduction_cpu_roundtrip_policy
emergency_cpu_fallback_policy
fail_closed
first_denial_precedence_version
legacy_projection_required
policy_digest
```

Policy slot:

```text
first exact bind          1회
same digest rebind        idempotent
different digest overwrite reject
```

---

# 6. Eligibility context

Schema:

```text
ash.attn.interconnect.w3.c1.admission-context.v1
```

입력군:

```text
surface / route / readiness
layer index / layer count
decode-step or prefill ordinal
model binding / shape / invocation / causal digests
Q/K/V dimensions
heads / KV heads / head dimension
parent authority validity
dispatcher and runtime-handle presence
device and queue exactness
raw borrow availability
quarantine state
runtime profile support
```

Model eligibility:

```text
model instance exact
model binding digest exact
heads > 0
kv_heads > 0
heads % kv_heads == 0
head_dim > 0
Q/K/V head dimensions exact
K/V sequence exact
Q sequence nonzero and <= KV sequence
```

Route shape:

```text
FullPrefill       q_seq == kv_seq
IncrementalDecode q_seq == 1
ChunkedDecode     2 <= q_seq < kv_seq
```

Device eligibility:

```text
dispatcher present
runtime handles present
device Arc lineage exact
queue Arc lineage exact
raw borrow exact when required
runtime profile supported
```

---

# 7. Admission disposition

```rust
pub enum HeadwiseAdmissionDisposition {
    AdmitProductionDeviceGuarded,
    DenyParentAuthorityInvalid,
    DenyOperatorProductionDisabled,
    DenyOperatorRouteDisabled,
    DenyRouterDisabled,
    DenyQkvBridgeDisabled,
    DenyModelIdentityMismatch,
    DenyModelGeometryMismatch,
    DenyShapeAuthorityMismatch,
    DenyCausalPositionMismatch,
    DenyInvocationIdentityMissing,
    DenyLayerIdentityMismatch,
    DenyDecodeStepIdentityMismatch,
    DenySurfaceUnknown,
    DenyLiveCallsiteAbsent,
    DenyGenericForwardCanonicalInvocationMissing,
    DenyDispatcherMissing,
    DenyRuntimeHandlesMissing,
    DenyDeviceLineageMismatch,
    DenyQueueLineageMismatch,
    DenyRawBorrowUnavailable,
    DenyQuarantined,
    DenyUnsupportedRuntimeProfile,
    DiagnosticOnly,
}
```

Current canonical surface verdict:

```text
Prefill
  unified compatibility projection

Incremental
  unified compatibility projection

Chunked
  DenyLiveCallsiteAbsent

Generic forward
  DenyGenericForwardCanonicalInvocationMissing

Trace / diagnostic
  DiagnosticOnly
```

Decision은 deterministic first-denial precedence를 사용하고 `first_denial_code`를 남긴다.

---

# 8. Fallback classification

```rust
pub enum HeadwiseFallbackClass {
    BurnGpuReferenceFallback,
    BurnGpuDirectBypass,
    NonProductionCpuRoundtrip,
    ExplicitEmergencyCpuFallback,
    NoFallbackAllowed,
}
```

구분:

```text
BurnGpuReferenceFallback
  production Headwise attempt가 비입장 또는 실패한 뒤 같은 호출에서 Burn GQA 사용

BurnGpuDirectBypass
  generic forward처럼 Headwise attempt 없이 Burn GQA 직접 실행

NonProductionCpuRoundtrip
  GPU -> CPU Vec<f32> -> GPU Tensor::from_data
  production fallback admission 금지

ExplicitEmergencyCpuFallback
  operator가 명시한 비상 경로
  W3-C1 production admission 0

NoFallbackAllowed
  authority/gate 또는 실행이 허용되지 않은 상태
```

모든 fallback은 reason code와 explicit receipt를 가져야 한다. Silent fallback은 금지한다.

---

# 9. Legacy compatibility projection

기존 `HeadwiseAttentionPromotionPolicySnapshot`은 독립 권위가 아니다.

```text
full-route policy
  -> HeadwiseLegacyPromotionProjection
  -> HeadwiseAttentionPromotionPolicySnapshot
```

Exact projection:

```text
allow_full_prefill
  production_requested
  && router enabled
  && headwise/qkv bridge not disabled
  && promote_prefill_requested

allow_incremental_decode
  production_requested
  && router enabled
  && headwise/qkv bridge not disabled
  && promote_incremental_requested

allow_chunked_decode
  false
```

Independent legacy writer와 semantic mismatch는 거부한다.

---

# 10. Behavior-preservation boundary

W3-C1에서 허용:

```text
operator intent snapshot 추가
full-route policy·context·decision 타입 추가
legacy compatibility projection 추가
policy slot 추가
per-call env read를 bind-time immutable snapshot으로 대체
policy gate와 artifact writer 추가
```

W3-C1에서 금지:

```text
prefill/incremental dispatch 결과 변경
chunked live entrypoint 생성
generic forward route 변경
Burn fallback 제거
CPU roundtrip 제거
Headwise output authority 변경
TensorCube role 변경
TensorCube live dispatch
WGSL 변경
```

---

# 11. Gate matrix

Positive cases:

```text
prefill model/shape/device matrix        12
incremental KV boundary matrix           21
legacy behavior combinations              7
chunked/generic/diagnostic classification 4
deterministic replay                      12
total                                     56
```

Negative controls:

```text
minimum 56
canonical implementation 62
```

주요 negative군:

```text
parent digest drift
operator intent captured after first forward
missing/invalid production parent digest
intent digest flip
policy overwrite
independent legacy writer
FullRouteEnforced premature use
surface/route/readiness mismatch
chunked live admission attempt
generic bypass misclassification
model/GQA/shape mismatch
causal/invocation/layer/step mismatch
dispatcher/runtime/device/queue/raw-borrow mismatch
quarantine
production CPU roundtrip admission
silent fallback
retry count overflow
route/TensorCube/output authority mutation
```

Decision counters:

```text
42, PASS 시 전부 0
```

---

# 12. Artifact closure

Output directory:

```text
workspace/runtime/attention/interconnect/w3/c1
```

Child artifacts, ordered:

```text
identity.json
parent_w0_binding.json
parent_w1_shape_authority.json
parent_w2_provenance.json
parent_w3_c0_coverage.json
source_inventory.json
operator_intent_contract.json
full_route_policy_schema.json
policy_binding_receipt.json
legacy_promotion_projection.json
model_eligibility_matrix.json
shape_eligibility_matrix.json
device_eligibility_matrix.json
runtime_surface_registry.json
phase_route_registry.json
prefill_admission_matrix.json
incremental_admission_matrix.json
chunked_admission_matrix.json
generic_forward_reconciliation.json
fallback_classification_registry.json
burn_gpu_fallback_policy.json
cpu_roundtrip_nonproduction_policy.json
emergency_cpu_fallback_policy.json
quarantine_policy.json
dispatcher_availability_policy.json
runtime_handles_policy.json
raw_bridge_policy.json
all_layer_decision_matrix.json
greedy_sampled_decision_parity.json
deterministic_decision_replay.json
legacy_behavior_equivalence.json
no_route_behavior_mutation.json
no_tensorcube_role_mutation.json
negative_control_outcomes.json
decision_counters.json
static_checks.json
policy_authority_snapshot.json
verdict.json
runtime_artifact.json
handoff_receipt.json
```

```text
child_artifact_expected       40
child_artifact_list_sha256     976b8e732ac98a8f0107df160bf09d1aae031c6fcbedca99367fa56ed69fbbab
serialization                  UTF-8, one filename per line, trailing LF included
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c1_runtime_artifact.json
schema = ash.attn.interconnect.w3.c1.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c1_local_manifest.json
schema = ash.attn.interconnect.w3.c1.local_manifest.v1
manifest self excluded from hash graph
```

Code ZIP excludes Markdown, W3-C1 runtime outputs, SHA sidecars, helper PowerShell/CMD files.

---

# 13. CLI contract

Binary:

```text
ash_attn_interconnect_w3_c1_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c1.args
```

```text
37 key/value pairs
74 non-empty lines
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
--verified-model-instance-binding
--model-spec
--expected-model-instance-id
--expected-w3-c0-coverage-digest
--expected-enforcement-mode
--require-immutable-operator-intent
--require-single-policy-authority
--require-legacy-projection
--require-prefill-unified-decision
--require-incremental-unified-decision
--require-chunked-explicit-denial
--require-generic-bypass-reconciliation
--require-model-eligibility
--require-shape-eligibility
--require-device-eligibility
--require-fallback-classification
--require-deterministic-denial-precedence
--require-greedy-sampled-decision-parity
--forbid-per-call-env-authority
--forbid-production-cpu-roundtrip
--forbid-route-behavior-mutation
--forbid-tensorcube-role-mutation
--forbid-output-authority-mutation
--minimum-positive-cases
--minimum-negative-controls
--negative-control-mode
--out-dir
--binding-epoch
```

---

# 14. PASS gate

```text
W0/W1/W2/W3-C0 parent exact
coverage source scope unchanged
model instance exact
operator intent immutable and digest exact
full-route policy single bind
legacy projection exact
prefill unified decision matrix pass
incremental unified decision matrix pass
chunked explicit denial exact
generic bypass reconciliation exact
model/shape/device eligibility pass
fallback classes exhaustive
first denial precedence deterministic
greedy/sampled decision parity exact
positive cases 56/56
negative controls 62/56 minimum
all 42 decision counters zero
per-call env reads 0
production CPU roundtrip admission 0
route behavior mutation 0
TensorCube role mutation 0
output authority mutation 0
child artifacts 40/40
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
policy_authority=full_route_admission
operator_intent=immutable_bind_time_snapshot
enforcement_mode=compatibility_projection
prefill=unified_compatibility_projection
incremental=unified_compatibility_projection
chunked=denied_live_callsite_absent
generic_forward=reconciliation_required_direct_burn_compatibility
legacy_projection=exact
fallback_classes=5
positive_cases=56/56
negative_controls=62/56
per_call_env_reads=0
route_behavior_mutation=0
tensorcube_role=shadow_observer_only
output_authority=headwise
child_artifacts=40/40
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C1_HEADWISE_FULL_ROUTE_ADMISSION_POLICY_MODEL_SHAPE_DEVICE_ELIGIBILITY_PREFILL_INCREMENTAL_CHUNKED_UNIFIED_DECISION_GENERIC_FORWARD_BYPASS_RECONCILIATION_FAIL_CLOSED_FALLBACK_CLASSIFICATION_ROUTE_DECISION_SSOT_LEGACY_PROJECTION_EXACT_NO_ROUTE_BEHAVIOR_MUTATION_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W3_C1_FULL_ROUTE_POLICY_AUTHORITY_ELIGIBILITY_UNIFIED_DECISION_BYPASS_RECONCILIATION_OR_FALLBACK_CLASSIFICATION_NOT_PROVEN
```

---

# 15. Direct Cargo execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c1_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c1.args"
```

Expected revision:

```text
W3-C1-headwise-full-route-admission-policy-v1
```

W3-C1 gate runs policy fixtures and source/static validation. It does not require a live Headwise GPU dispatch.

---

# 16. Failure handling

First mismatch order:

```text
parent closure
coverage drift
operator intent capture
policy binding
legacy projection
surface readiness
model eligibility
shape/causal eligibility
invocation identity
device eligibility
health/quarantine
fallback classification
deterministic replay
artifact closure
```

Forbidden repair:

```text
missing parent digest substitution
per-call environment reread
chunked absent collapsed to operator-disabled
generic bypass classified as Headwise failure fallback
missing invocation identity inferred from shape
missing layer identity parsed from label
device mismatch accepted by digest only
production CPU roundtrip relabeled emergency fallback
legacy policy retained as independent authority
unknown surface downgraded to diagnostic
```

Failure leaves route behavior, Headwise output authority, and TensorCube role unchanged.

---

# 17. W3-C2 handoff

W3-C2 consumes:

```text
full_route_policy_digest
operator_intent_digest
legacy_projection_digest
prefill admission matrix digest
model eligibility matrix digest
shape eligibility matrix digest
device eligibility matrix digest
fallback registry digest
generic bypass blocker receipt
```

W3-C2 first allows:

```text
ProductionPrefill live admission-context plumbing
prefill all-layer decision enforcement
prefill legacy-projection dependency removal
prefill GPU coverage runtime receipt
```

W3-C2 still forbids incremental enforcement, chunked entrypoint creation, generic-forward phase inference, and TensorCube role mutation.

---

# 18. Final seal

W3-C1 PASS seals one full-route admission-policy authority derived from W0, W1, W2, W3-C0 and immutable operator intent. Prefill and incremental preserve legacy behavior through exact projection. Chunked is denied because its live callsite is absent. Generic forward remains an explicit direct-Burn reconciliation blocker. Fallback classes are separated, deterministic, and fail-closed. No route execution, Headwise output authority, or TensorCube role is changed by this commit.
