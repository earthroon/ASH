# ASH-ATTN-DECODE-W9B

## Actual Canary Expansion /
## Full-Layer Qualification /
## Canary Ratio Promotion /
## Long-Session Token Soak /
## Latency·VRAM Budget /
## Cross-Device Allowlist /
## Rollback Drill Matrix /
## TensorCube Actual Route Stability Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-DECODE-W9B`  
> Proposed build revision: `W9B-w9a-actual-route-expansion-stability-r1`  
> Parent: `ASH-ATTN-DECODE-W9A-R1E`  
> Parent state: `PHYSICAL PASS`  
> Parent authority: TensorCube actual-canary token commit with Headwise same-invocation rollback  
> Global default writer before W9B: `HeadwiseFullActive`  
> Global default writer after W9B: `HeadwiseFullActive`  
> TensorCube authority after W9B: qualified-domain actual writer  
> Global TensorCube default promotion: forbidden in W9B  
> Next authority patch: `ASH-ATTN-DECODE-W9C`

---

# 0. 상태 구분

## 확정

사용자 로컬 물리 실행에서 다음 W9A PASS 토큰이 관측됐다.

```text
PASS_ASH_ATTN_DECODE_W9A_TENSORCUBE_ACTUAL_CONTEXT_SELECTION_PRE_OUTPUT_PROJECTION_ROUTE_SSOT_PRODUCTION_OUTPUT_PROJECTION_ADOPTION_PRODUCTION_LOGITS_CONTINUATION_PRE_SAMPLER_COMMIT_GATE_DETERMINISTIC_CANARY_ELIGIBILITY_HEADWISE_SAME_INVOCATION_ROLLBACK_SAMPLED_DUAL_PATH_AUDIT_REAL_SAMPLER_SINGLE_INVOCATION_ATOMIC_TOKEN_COMMIT_SESSION_QUARANTINE_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

따라서 W9B는 다음을 부모 물리 권위로 채택한다.

```text
TensorCube actual context selection
production output projection adoption
production logits continuation
real sampler single invocation
actual token commit
same-invocation Headwise rollback
sampled dual-path audit
session quarantine
no full logits readback
no silent fallback
no unrecoverable token commit
```

## 제안

이 문서의 canary ratio ladder, soak band, latency·VRAM threshold schema, cross-device qualification schema는 W9B의 구현 계약 제안이다.

실제 수치 threshold는 W9A와 Headwise baseline을 Rust가 측정해 생성한 calibration artifact에서 봉인한다.

## 판단 불가

현재 대화 로그만으로 다음은 확정할 수 없다.

```text
전체 layer가 W9A qualified인지
장시간 token soak의 실제 p95·p99
TensorCube 경로의 실제 latency 우위
device별 driver 안정성
global default writer 승격 가능 여부
```

W9B physical gate가 위 항목을 판정한다.

---

# 1. 목적

W9A는 deterministic canary domain에서 TensorCube가 실제 production token을 생성할 수 있음을 증명했다.

W9B의 목적은 그 권한을 무조건 확대하는 것이 아니다.

W9B는 다음 질문에 답한다.

```text
1. 모델의 모든 attention layer가 TensorCube actual route를 사용할 수 있는가?
2. canary 비율을 높여도 token commit 안정성이 유지되는가?
3. 긴 session과 긴 KV 상태에서도 latency·VRAM이 안정적인가?
4. device·driver가 달라도 같은 qualification을 주장할 수 있는가?
5. 의도적 실패를 주입해도 Headwise rollback이 항상 같은 step에서 복구하는가?
6. TensorCube actual route가 반복 실행과 재시작 후에도 같은 authority contract를 유지하는가?
```

W9B가 완료되면 다음 문장이 사실이어야 한다.

```text
W9A에서 단일 deterministic canary로 검증된 TensorCube actual route가
전체 qualified layer, 승격된 canary ratio, 장시간 token session,
승인된 device·driver allowlist에서 안정적으로 token을 생성했다.

성능·메모리·수치·lifetime·rollback budget을 벗어난 profile은
즉시 Headwise authority로 되돌아갔으며,
silent fallback이나 commit 이후 rollback은 발생하지 않았다.
```

---

# 2. 핵심 비목표

W9B는 다음을 수행하지 않는다.

```text
TensorCube를 global default writer로 승격
Headwise rollback route 삭제
모든 device를 자동 허용
새 attention 수식 도입
새 sampler 수식 도입
새 LM-head 수식 도입
full logits host readback
full context host readback
CPU sampler fallback
환경변수만으로 force promotion
실패 threshold 완화
receipt 없는 비율 변경
```

다음은 W9C 이후 범위다.

```text
TensorCube global default writer
Headwise rollback-only oracle
atomic global authority pointer switch
fleet-wide default route
```

---

# 3. Authority Map

## 3.1 Global authority

```text
Global default attention writer
  HeadwiseFullActive

Qualified W9B domain actual writer
  TensorCube

Rollback writer
  HeadwiseFullActive

Canary ratio authority
  W9B Promotion Controller

Device admission authority
  W9B Device Allowlist Artifact

Token commit authority
  W9A Pre-Sampler Commit Gate

Global default promotion authority
  denied
```

## 3.2 SSOT hierarchy

```text
W9A physical artifact
  ↓
W9B calibration artifact
  ↓
W9B full-layer qualification artifact
  ↓
W9B device allowlist artifact
  ↓
W9B canary promotion artifact
  ↓
per-session immutable route snapshot
```

하위 단계는 상위 artifact digest를 정확히 바인딩해야 한다.

상위 digest가 바뀌면 하위 authority는 자동 무효화한다.

## 3.3 단일 writer 규칙

한 layer invocation에는 actual writer가 정확히 하나만 존재한다.

```text
TensorCube actual
xor
Headwise actual
```

sampled dual-path audit에서 Headwise oracle이 실행될 수 있지만 production selected context는 하나다.

```text
production context writer count = 1
audit oracle count              = 0 or 1
```

---

# 4. W9B Promotion State Machine

```rust
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum AttentionDecodeW9BPromotionState {
    HeadwiseDefault,
    TensorCubeCanaryTier0,
    TensorCubeCanaryTier1,
    TensorCubeCanaryTier2,
    TensorCubeCanaryTier3,
    TensorCubeCanaryTier4,
    Hold,
    Quarantined,
}
```

권장 ratio ladder:

```text
Tier0 = 1 / 64
Tier1 = 1 / 16
Tier2 = 1 / 4
Tier3 = 1 / 2
Tier4 = qualified sessions 100%
```

주의:

```text
Tier4 != global default writer
```

Tier4는 W9B-qualified session 집합 안에서만 TensorCube actual route를 100% 선택한다.

allowlist 밖의 session·device·geometry는 여전히 Headwise다.

## 4.1 허용 전이

```text
HeadwiseDefault
→ TensorCubeCanaryTier0

Tier0 → Tier1
Tier1 → Tier2
Tier2 → Tier3
Tier3 → Tier4

TierN → Hold
TierN → Quarantined
Hold → Tier0
Quarantined → HeadwiseDefault
```

## 4.2 금지 전이

```text
HeadwiseDefault → Tier2 이상
Tier0 → Tier3 이상
Tier1 → Tier4
Quarantined → TierN
Hold → Tier1 이상
Tier4 → GlobalDefault
```

## 4.3 승격 조건

각 tier는 바로 이전 tier의 physical receipt를 부모로 가져야 한다.

```text
promotion candidate tier N
requires
tier N-1 artifact PASS
and
tier N-1 soak receipt PASS
and
tier N-1 budget receipt PASS
and
tier N-1 rollback drill PASS
and
tier N-1 owner-zero PASS
```

---

# 5. Deterministic Canary Selection

## 5.1 Selection key

```text
selection_key = SHA-256(
    patch_id
 || build_revision
 || model_instance_digest
 || checkpoint_digest
 || tokenizer_digest
 || device_allowlist_entry_digest
 || session_id
 || session_epoch
 || promotion_tier
 || route_policy_digest
)
```

```text
bucket = first_u64(selection_key) % denominator
selected = bucket < numerator
```

## 5.2 금지 입력

다음은 bucket derivation에 사용할 수 없다.

```text
wall-clock time
thread scheduling order
GPU timestamp
random OS entropy
unordered map iteration order
process ID
memory address
```

## 5.3 Session pinning

한 session이 시작된 뒤 promotion tier와 selected route는 session 종료까지 고정한다.

중간 tier 변경은 다음 session부터 적용한다.

예외:

```text
rollback 또는 quarantine 발생
→ 현재 session 즉시 Headwise pin
```

## 5.4 Replay parity

같은 입력 artifact와 같은 session identity에서:

```text
selected route
promotion tier
audit bucket
device allowlist entry
```

가 bit-exact하게 재현돼야 한다.

---

# 6. Full-Layer Qualification

## 6.1 목표

W9A에서 일부 layer만 qualified됐을 가능성을 제거한다.

W9B는 모델의 attention layer 전체를 inventory하고 각 layer를 독립적으로 qualification한다.

## 6.2 Layer inventory SSOT

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AttentionDecodeW9BLayerInventoryEntry {
    pub layer_index: u32,
    pub layer_identity_digest: String,
    pub q_projection_digest: String,
    pub k_projection_digest: String,
    pub v_projection_digest: String,
    pub output_projection_digest: String,
    pub q_head_count: u32,
    pub kv_head_count: u32,
    pub head_dim: u32,
    pub supported_geometry_digest: String,
    pub inventory_entry_digest: String,
}
```

## 6.3 Layer qualification matrix

각 layer는 최소 다음 profile을 통과해야 한다.

```text
decode q_seq=1
short KV
middle KV
long KV
chunk boundary -1
chunk boundary exact
chunk boundary +1
causal active
all-masked
GQA mapping
repeat execution
rollback injection
```

## 6.4 Exact layer admission

다음 모두 일치해야 해당 layer를 allowlist에 넣는다.

```text
layer index
projection weight digests
head geometry
W8A context parity receipt
W9A actual token receipt
W9B layer matrix receipt
```

## 6.5 Full-layer completion

```text
qualified_layer_count
==
model_attention_layer_count
```

가 아니면 `FullLayerQualification`을 주장할 수 없다.

부분 qualification은 허용하되 상태를 명확히 기록한다.

```text
PartialLayerQualified
```

부분 qualification 상태에서는 Tier4 진입을 금지한다.

---

# 7. Geometry Qualification

## 7.1 Geometry key

```rust
pub struct AttentionDecodeW9BGeometryKey {
    pub q_seq: u32,
    pub seq_kv: u32,
    pub batch: u32,
    pub q_heads: u32,
    pub kv_heads: u32,
    pub head_dim: u32,
    pub mask_profile: String,
    pub causal: bool,
    pub chunk_policy_digest: String,
}
```

## 7.2 Range expansion 금지

다음 식의 추정 admission은 금지한다.

```text
q_seq <= tested_max
seq_kv <= tested_max
```

실제 qualified geometry key 또는 artifact가 승인한 canonical band에 포함돼야 한다.

## 7.3 Boundary matrix

각 policy-derived chunk boundary `B`마다:

```text
B - 1
B
B + 1
```

을 실행한다.

첫 chunk, middle chunk, final partial chunk를 모두 포함한다.

---

# 8. Long-Session Token Soak

## 8.1 목적

짧은 gate 통과만으로는 다음 문제를 발견할 수 없다.

```text
KV lifetime leak
owner count 누적
ring slot 고갈
partition generation drift
sampler state divergence
token ledger double append
latency tail 증가
VRAM staircase
quarantine 이후 재활성화
```

## 8.2 Soak bands

token band는 CLI와 calibration artifact에서 결정한다.

권장 기본 profile:

```text
S0  64 committed tokens
S1  256 committed tokens
S2  1024 committed tokens
S3  max admitted context까지
```

모델 context limit이 S2보다 작으면:

```text
S2 = max admitted context
S3 = omitted with explicit reason
```

## 8.3 Prompt classes

```text
short instruction
long subtitle-like input
repetition-heavy input
mixed punctuation
EOS-near input
high-entropy token stream
```

특정 문장 내용은 authority가 아니다.

prompt class와 tokenized input digest가 authority다.

## 8.4 Per-step invariant

모든 committed step에서:

```text
real_sampler_invocation_count = 1
token_commit_count            = 1
candidate_byte_leak_count     = 0
double_commit_count           = 0
early_stream_emit_count       = 0
stale_handle_count            = 0
```

## 8.5 Soak-level invariant

```text
committed_token_count == requested_token_count or valid EOS stop
owner_count returns to baseline after session
VRAM returns within release tolerance after terminal drain
partition generation strictly monotonic
session route remains pinned
```

## 8.6 EOS 처리

EOS는 soak 실패가 아니다.

다음 receipt가 있어야 한다.

```text
stop_reason = EOS
selected_token_id = canonical EOS
sampler invocation count exact
token commit count exact
terminal drain observed
```

---

# 9. Latency Budget

## 9.1 Baseline

같은 device·driver·model·prompt·seed에서 Headwise baseline을 먼저 측정한다.

```text
Headwise baseline
TensorCube candidate
```

는 같은 workload plan을 사용한다.

## 9.2 측정 축

```text
attention stage GPU ns
output projection GPU ns
full decode step GPU ns
host-visible step latency ns
p50
p95
p99
max
first-token latency
steady-state token latency
rollback latency
```

## 9.3 Budget artifact

```rust
pub struct AttentionDecodeW9BLatencyBudget {
    pub headwise_p50_ns: u64,
    pub headwise_p95_ns: u64,
    pub headwise_p99_ns: u64,
    pub tensorcube_p50_ns: u64,
    pub tensorcube_p95_ns: u64,
    pub tensorcube_p99_ns: u64,
    pub maximum_regression_basis_points: u32,
    pub maximum_absolute_tail_delta_ns: u64,
    pub rollback_p99_budget_ns: u64,
    pub pass: bool,
    pub receipt_digest: String,
}
```

## 9.4 승격 규칙

threshold는 CLI literal이 아니라 calibration artifact digest로 봉인한다.

승격 시 최소 다음이 필요하다.

```text
TensorCube p95 within budget
TensorCube p99 within budget
rollback p99 within budget
no monotonic tail growth across soak windows
timestamp-query evidence present
```

## 9.5 Timing source

허용:

```text
GPU timestamp query
monotonic host clock around exact step boundary
```

금지:

```text
console log timestamp
wall-clock date
unordered trace merge
```

---

# 10. VRAM Budget

## 10.1 측정 축

```text
baseline resident bytes
candidate resident bytes
peak resident bytes
per-token delta
per-layer delta
post-drain residual bytes
rollback scratch peak
audit dual-path peak
```

## 10.2 VRAM receipt

```rust
pub struct AttentionDecodeW9BVramBudgetReceipt {
    pub baseline_bytes: u64,
    pub steady_state_bytes: u64,
    pub peak_bytes: u64,
    pub post_drain_bytes: u64,
    pub maximum_allowed_peak_bytes: u64,
    pub maximum_allowed_post_drain_delta_bytes: u64,
    pub monotonic_growth_detected: bool,
    pub plateau_observed: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

## 10.3 Plateau requirement

최소 세 개의 동일 길이 observation window에서:

```text
window_n_peak
window_n+1_peak
window_n+2_peak
```

이 budget tolerance 안에서 plateau를 형성해야 한다.

## 10.4 금지 완화

다음 방식으로 PASS를 만들면 안 된다.

```text
measurement window 단축
첫 warmup 제외 규칙 변경
peak 대신 average만 기록
rollback scratch 제외
audit scratch 제외
terminal drain 전 측정 종료
```

---

# 11. Cross-Device Allowlist

## 11.1 Device identity

```rust
pub struct AttentionDecodeW9BDeviceIdentity {
    pub backend: String,
    pub vendor_id: u32,
    pub device_id: u32,
    pub adapter_name: String,
    pub driver_name: String,
    pub driver_info: String,
    pub subgroup_size: u32,
    pub enabled_feature_digest: String,
    pub limits_digest: String,
    pub runtime_version_digest: String,
    pub identity_digest: String,
}
```

## 11.2 Exact allowlist

allowlist entry는 family 이름만으로 만들 수 없다.

금지:

```text
RTX 30 series 전체
NVIDIA 전체
subgroup 32이면 전체
shader-int64 지원이면 전체
```

허용:

```text
정확한 adapter identity
정확한 driver range
정확한 runtime feature digest
정확한 limits digest
정확한 W9B physical receipt
```

## 11.3 Driver range

driver range admission은 명시적 lower/upper bound와 검증 receipt가 있어야 한다.

검증되지 않은 신규 driver는 Headwise default로 간다.

## 11.4 Device qualification matrix

각 device entry에서 최소 다음을 실행한다.

```text
verification gate
full-layer matrix
long-session soak
latency budget
VRAM budget
rollback drill
device-loss pre-commit drill
three-cycle process restart replay
```

## 11.5 Allowlist publication

```text
workspace/runtime/attention/decode/w9b/
  device_allowlist_candidate.json
  device_allowlist_manifest.json
```

Rust가 생성하고 SHA-256 readback을 검증한다.

---

# 12. Rollback Drill Matrix

## 12.1 목적

rollback은 코드 경로 존재가 아니라 실제 실패 주입 후 복구로 증명한다.

## 12.2 Drill IDs

```rust
pub enum AttentionDecodeW9BRollbackDrillId {
    ContextGuardMismatch,
    ProjectionBindingMismatch,
    CandidateLogitsNonFinite,
    LogitsParityMismatch,
    SamplerPreviewMismatch,
    CandidateOwnerLeak,
    StalePartitionGeneration,
    RouteSnapshotDrift,
    SubmissionFailureBeforeCommit,
    DeviceLossBeforeCommit,
    AtomicStreamUnavailable,
    SessionQuarantineReentry,
}
```

## 12.3 공통 성공 조건

각 drill에서:

```text
candidate token exposure count       0
real sampler invocation count        1
token commit count                   1
Headwise same-step replay count      1
candidate owner zero                 true
main state unchanged before replay   true
session quarantined                  true
silent fallback count                0
```

## 12.4 Device-loss 경계

지원 가능한 device-loss injection은 commit 이전에만 수행한다.

commit 이후 device loss는 W9B의 rollback 범위가 아니다.

그 경우 recovery patch로 분리한다.

## 12.5 Drill replay

각 drill은 최소 세 번 반복한다.

```text
same drill input
same selected route
same failure point
same final Headwise token
same receipt semantics
distinct invocation identity
distinct partition generation
```

---

# 13. Sampled Dual-Path Audit Expansion

## 13.1 Audit ratio

canary ratio와 audit ratio는 독립적이다.

권장:

```text
Tier0 audit 100%
Tier1 audit 1/4
Tier2 audit 1/8
Tier3 audit 1/16
Tier4 audit 1/32
```

실제 값은 promotion policy artifact에서 결정한다.

## 13.2 Audit 범위

```text
attention context
post-output-projection hidden
final logits compact parity
top-k identity
pure sampler preview token
```

## 13.3 Audit failure effect

한 번의 audit failure로:

```text
현재 step rollback
현재 session quarantine
현재 device/profile promotion HOLD
상위 tier promotion 금지
```

를 수행한다.

audit failure를 단순 metric으로만 기록하고 계속 TensorCube를 쓰면 안 된다.

---

# 14. Stability Window

## 14.1 Window definition

```rust
pub struct AttentionDecodeW9BStabilityWindow {
    pub window_index: u32,
    pub promotion_tier: u32,
    pub session_count: u64,
    pub committed_token_count: u64,
    pub tensorcube_token_count: u64,
    pub headwise_token_count: u64,
    pub rollback_count: u64,
    pub audit_count: u64,
    pub audit_failure_count: u64,
    pub p95_latency_ns: u64,
    pub p99_latency_ns: u64,
    pub peak_vram_bytes: u64,
    pub post_drain_vram_bytes: u64,
    pub owner_leak_count: u64,
    pub pass: bool,
    pub digest: String,
}
```

## 14.2 최소 window

각 promotion tier는 최소 세 개의 연속 PASS window가 필요하다.

```text
PASS, PASS, PASS
```

중간에 HOLD 또는 FAIL이 있으면 streak는 0으로 초기화한다.

## 14.3 Stability seal

다음 모두 만족해야 `ActualRouteStable`을 주장한다.

```text
three consecutive PASS windows
zero audit failures
zero unrecoverable commits
zero silent fallbacks
zero owner leaks
latency within budget
VRAM plateau within budget
rollback drill complete
```

---

# 15. Promotion Controller

## 15.1 Controller input

```rust
pub struct AttentionDecodeW9BPromotionInput {
    pub parent_w9a_artifact_digest: String,
    pub current_tier: u32,
    pub requested_tier: u32,
    pub layer_qualification_digest: String,
    pub device_allowlist_entry_digest: String,
    pub stability_window_digests: Vec<String>,
    pub latency_budget_digest: String,
    pub vram_budget_digest: String,
    pub rollback_matrix_digest: String,
    pub operator_policy_digest: String,
}
```

## 15.2 Promotion decision

```rust
pub enum AttentionDecodeW9BPromotionDecision {
    PromoteOneTier,
    HoldCurrentTier,
    DemoteToTier0,
    QuarantineProfile,
}
```

## 15.3 One-step promotion

한 번에 한 tier만 승격할 수 있다.

```text
requested_tier <= current_tier + 1
```

## 15.4 Automatic demotion

다음은 즉시 demotion 또는 quarantine한다.

```text
audit failure
unrecoverable commit attempt
owner leak
VRAM monotonic growth
p99 latency budget breach
route snapshot drift
device identity drift
driver identity drift
```

---

# 16. Route Snapshot Extension

```rust
pub struct AttentionDecodeW9BRouteSnapshot {
    pub w9a_route_snapshot_digest: String,
    pub promotion_state: AttentionDecodeW9BPromotionState,
    pub promotion_tier: u32,
    pub canary_numerator: u32,
    pub canary_denominator: u32,
    pub audit_numerator: u32,
    pub audit_denominator: u32,
    pub layer_qualification_digest: String,
    pub device_allowlist_entry_digest: String,
    pub latency_budget_digest: String,
    pub vram_budget_digest: String,
    pub stability_window_parent_digest: String,
    pub snapshot_digest: String,
}
```

session 시작 후 immutable하다.

---

# 17. Failure and HOLD Codes

## Parent and revision

```text
AttentionDecodeW9BParentW9AArtifactMissing
AttentionDecodeW9BParentW9ANotPass
AttentionDecodeW9BParentDigestMismatch
AttentionDecodeW9BBuildRevisionMismatch
```

## Layer qualification

```text
AttentionDecodeW9BLayerInventoryMismatch
AttentionDecodeW9BLayerNotQualified
AttentionDecodeW9BFullLayerQualificationIncomplete
AttentionDecodeW9BProjectionDigestMismatch
AttentionDecodeW9BGeometryCoverageIncomplete
```

## Promotion

```text
AttentionDecodeW9BPromotionTierSkip
AttentionDecodeW9BPromotionParentMissing
AttentionDecodeW9BPromotionStabilityWindowIncomplete
AttentionDecodeW9BPromotionBudgetNotPass
AttentionDecodeW9BPromotionRollbackMatrixIncomplete
AttentionDecodeW9BPromotionPolicyDigestMismatch
```

## Soak

```text
AttentionDecodeW9BLongSessionTokenCountMismatch
AttentionDecodeW9BSessionRouteDrift
AttentionDecodeW9BPartitionGenerationNonMonotonic
AttentionDecodeW9BTokenLedgerDoubleAppend
AttentionDecodeW9BTerminalDrainIncomplete
```

## Latency and VRAM

```text
AttentionDecodeW9BLatencyP95BudgetExceeded
AttentionDecodeW9BLatencyP99BudgetExceeded
AttentionDecodeW9BRollbackLatencyBudgetExceeded
AttentionDecodeW9BVramPeakBudgetExceeded
AttentionDecodeW9BVramPostDrainBudgetExceeded
AttentionDecodeW9BVramPlateauNotObserved
AttentionDecodeW9BVramMonotonicGrowthDetected
```

## Device

```text
AttentionDecodeW9BDeviceIdentityNotAllowlisted
AttentionDecodeW9BDriverIdentityNotAllowlisted
AttentionDecodeW9BRuntimeFeatureDigestMismatch
AttentionDecodeW9BDeviceReceiptMissing
```

## Rollback

```text
AttentionDecodeW9BRollbackDrillNotExecuted
AttentionDecodeW9BRollbackTokenExposureDetected
AttentionDecodeW9BRollbackSamplerDoubleInvocation
AttentionDecodeW9BRollbackTokenDoubleCommit
AttentionDecodeW9BRollbackOwnerLeak
AttentionDecodeW9BQuarantineReentryDetected
```

## Stability

```text
AttentionDecodeW9BStabilityWindowNotPass
AttentionDecodeW9BStabilityStreakIncomplete
AttentionDecodeW9BActualRouteNotStable
AttentionDecodeW9BSilentFallbackDetected
AttentionDecodeW9BUnrecoverableTokenCommit
```

---

# 18. Implementation File Plan

## model_core

```text
crates/model_core/src/
  attention_decode_w9b.rs
  attention_decode_w9b_layer_qualification.rs
  attention_decode_w9b_promotion_controller.rs
  attention_decode_w9b_route_snapshot.rs
  attention_decode_w9b_long_session.rs
  attention_decode_w9b_stability_window.rs
  attention_decode_w9b_device_allowlist.rs
  attention_decode_w9b_rollback_matrix.rs
```

연결 대상:

```text
attention_decode_w9a.rs
attention_decode_w9a_route_ssot.rs
attention_decode_w9a_step_transaction.rs
attention_decode_w9a_pre_sampler_commit.rs
decode_state.rs
native_wgpu.rs
generation_sampling.rs
kv_rollback01_forked_replay.rs
```

## burn_webgpu_backend

```text
crates/burn_webgpu_backend/src/
  attention_decode_w9b_latency_probe.rs
  attention_decode_w9b_vram_probe.rs
  attention_decode_w9b_device_identity.rs
  attention_decode_w9b_fault_injection.rs
```

새 attention kernel은 추가하지 않는다.

## orchestrator_local

```text
crates/orchestrator_local/src/
  attention_decode_w9b_cli_registry.rs
  attention_decode_w9b_artifact_wave_map.rs
  attention_decode_w9b_scenario_plan.rs
  attention_decode_w9b_device_matrix.rs
  attention_decode_w9b_soak_plan.rs

crates/orchestrator_local/src/bin/
  ash_attn_decode_w9b_verification_gate.rs
  ash_attn_decode_w9b_physical_gate.rs
```

## CLI

```text
specs/cli/
  ash_attn_decode_w9b_verification.args
  ash_attn_decode_w9b_physical.args
```

---

# 19. Verification Gate

## 19.1 Static graph

```text
W9A parent module registered
W9B modules registered
promotion controller reachable
global default writer unchanged
W9C authority absent
Headwise rollback reachable
real sampler behind pre-sampler gate
stream emission behind token commit
```

## 19.2 Policy tests

```text
tier skip denied
single-tier promotion allowed
three-window requirement enforced
audit failure demotes
VRAM breach demotes
device identity drift denies
session route pinning preserved
```

## 19.3 Layer tests

```text
complete inventory
duplicate layer index denied
missing layer denied
projection digest drift denied
partial qualification cannot claim full
```

## 19.4 Soak tests

```text
valid EOS completion
requested token completion
double append negative control
route drift negative control
terminal drain negative control
```

## 19.5 Rollback tests

모든 drill enum이 scenario plan에 정확히 한 번 이상 존재해야 한다.

---

# 20. Physical Gate Plan

## Phase A: Baseline calibration

```text
Headwise-only baseline
same device
same prompt corpus
same seed corpus
same token bands
```

산출:

```text
latency baseline
VRAM baseline
device identity
driver identity
runtime feature identity
```

## Phase B: Full-layer qualification

모든 attention layer에서 W9A actual route와 sampled audit를 실행한다.

## Phase C: Tier ladder

```text
Tier0
→ three PASS windows
→ Tier1
→ three PASS windows
→ Tier2
→ three PASS windows
→ Tier3
→ three PASS windows
→ Tier4
```

실행 시간 또는 corpus 제한으로 Tier4까지 못 가면 마지막 완료 tier를 명시한다.

## Phase D: Long-session soak

```text
S0
S1
S2
S3 when supported
```

## Phase E: Rollback drill matrix

모든 drill을 세 번씩 반복한다.

## Phase F: Process replay

최소 세 번:

```text
process start
→ W9B artifact adoption
→ qualified session run
→ terminal drain
→ process exit
```

artifact와 route semantics가 재현돼야 한다.

---

# 21. Required Artifacts

```text
workspace/runtime/attention/decode/w9b/
  ash_attn_decode_w9b_verification_runtime_specification.json
  ash_attn_decode_w9b_verification_runtime_artifact.json
  ash_attn_decode_w9b_verification_local_manifest.json

  ash_attn_decode_w9b_physical_runtime_specification.json
  ash_attn_decode_w9b_physical_runtime_artifact.json
  ash_attn_decode_w9b_physical_local_manifest.json

  layer_inventory.json
  layer_qualification_matrix.json
  geometry_qualification_matrix.json
  latency_baseline.json
  latency_budget_receipt.json
  vram_budget_receipt.json
  device_identity.json
  device_allowlist_candidate.json
  rollback_drill_matrix.json
  promotion_policy.json
  promotion_history.json
  stability_windows.json
  session_soak_summary.json
  final_stability_seal.json
```

모든 artifact는 Rust가 생성한다.

코드 ZIP에 runtime artifact를 포함하지 않는다.

---

# 22. CLI Contract

필수 키:

```text
--patch-id
--expected-build-revision

--parent-w9a-artifact
--parent-w9a-manifest

--promotion-tier-start
--promotion-tier-target
--promotion-window-count

--tier0-numerator
--tier0-denominator
--tier1-numerator
--tier1-denominator
--tier2-numerator
--tier2-denominator
--tier3-numerator
--tier3-denominator
--tier4-numerator
--tier4-denominator

--audit-numerator
--audit-denominator

--soak-token-bands
--soak-session-count
--soak-prompt-corpus
--soak-seed-corpus

--maximum-latency-regression-bps
--maximum-latency-tail-delta-ns
--maximum-vram-peak-bytes
--maximum-vram-post-drain-delta-bytes

--require-full-layer-qualification
--require-cross-device-identity
--require-rollback-drill-matrix
--require-three-window-stability
--deny-global-default-promotion
--deny-full-logits-readback
--deny-full-context-readback
--deny-silent-fallback

--out-runtime-specification
--out-runtime-artifact
--out-local-manifest
--out-w9b-directory
```

unknown key와 duplicate key는 FAIL한다.

---

# 23. PASS Criteria

## Parent

```text
W9A physical artifact PASS                    true
W9A manifest digest exact                     true
W9A build revision exact                      true
```

## Full-layer

```text
qualified layer count
==
model attention layer count
```

## Canary promotion

```text
target tier reached                           true
tier skip count                               0
promotion without parent PASS                 0
promotion policy drift count                  0
```

## Long-session

```text
required soak bands completed                 true
token commit mismatch count                   0
session route drift count                     0
terminal drain failure count                  0
```

## Latency

```text
p95 within budget                             true
p99 within budget                             true
rollback p99 within budget                    true
tail monotonic growth                         false
```

## VRAM

```text
peak within budget                            true
post-drain within budget                      true
plateau observed                              true
monotonic growth detected                     false
```

## Device

```text
active device identity exact                  true
driver identity exact                         true
runtime feature digest exact                  true
device physical receipt PASS                  true
```

## Rollback

```text
all required drills executed                  true
all required drills repeated >= 3             true
candidate token exposure count                0
sampler double invocation count               0
token double commit count                     0
rollback owner leak count                     0
quarantine reentry count                      0
```

## Stability

```text
consecutive PASS windows >= 3                 true
audit failure count                           0
silent fallback count                         0
unrecoverable token commit count              0
```

## Authority

```text
TensorCube actual qualified-domain writer     observed
Headwise global default writer                maintained
Headwise rollback writer                      maintained
TensorCube global default promotion           false
```

---

# 24. Proposed PASS Token

```text
PASS_ASH_ATTN_DECODE_W9B_ACTUAL_CANARY_EXPANSION_FULL_LAYER_QUALIFICATION_CANARY_RATIO_PROMOTION_LONG_SESSION_TOKEN_SOAK_LATENCY_VRAM_BUDGET_CROSS_DEVICE_ALLOWLIST_ROLLBACK_DRILL_MATRIX_THREE_WINDOW_STABILITY_DETERMINISTIC_ROUTE_PINNING_HEADWISE_GLOBAL_DEFAULT_PRESERVATION_NO_FULL_CONTEXT_READBACK_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_TENSORCUBE_ACTUAL_ROUTE_STABILITY_SEALED
```

---

# 25. Completion State

W9B PASS 후 상태:

```text
TensorCube
  ActualQualifiedDomainWriter
  FullLayerQualified
  CanaryRatioPromoted
  LongSessionSoakBound
  LatencyBudgetBound
  VramBudgetBound
  DeviceAllowlistBound
  RollbackDrillBound
  ActualRouteStable

Headwise
  GlobalDefaultWriter
  SameInvocationRollbackWriter
  AuditOracle

Token commit
  W9A PreSamplerGateAuthoritative
  SingleSamplerInvocation
  AtomicCommit
```

W9B PASS는 global default promotion을 의미하지 않는다.

---

# 26. 다음 패치

```text
ASH-ATTN-DECODE-W9C

TensorCube Global Default Writer Promotion /
Atomic Authority Pointer Switch /
Headwise Rollback-Only Oracle /
Default Route Artifact Adoption /
Instant Demotion /
Cross-Session Authority Consistency /
No Dual Production Writer Seal
```

W9C 진입 조건:

```text
W9B FullLayerQualified
W9B Tier4 reached
W9B three-window stability PASS
W9B latency budget PASS
W9B VRAM budget PASS
W9B rollback matrix PASS
W9B device allowlist PASS
```

이 조건이 하나라도 빠지면 W9C를 시작하지 않는다.
