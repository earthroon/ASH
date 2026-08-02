# ASH-ATTN-DECODE-W9A

## TensorCube Actual Context Selection / Pre-Output-Projection Route SSOT / Production Output Projection Adoption / Production Logits Continuation / Pre-Sampler Commit Gate / Deterministic Canary Eligibility / Headwise Same-Invocation Rollback / Sampled Dual-Path Audit / No Unrecoverable Token Commit Seal

- Patch ID: `ASH-ATTN-DECODE-W9A`
- Proposed build revision: `W9A-w8a-actual-canary-pre-sampler-rollback-r1`
- Parent code baseline: `ASH-ATTN-INTERCONNECT-W8A-R1H`
- Parent physical authority: `W8A Physical PASS`
- Scope class: actual canary adoption / step-transactional / rollback-preserving
- Global default attention writer before W9A: `HeadwiseFullActive`
- Global default attention writer after W9A: `HeadwiseFullActive`
- Eligible canary invocation writer after W9A: `TensorCube`
- Ineligible or rolled-back invocation writer: `HeadwiseFullActive`
- Token commit authority: `W9A Pre-Sampler Commit Transaction`
- Silent fallback authority: denied

---

# 0. 명세 목적

W8과 W8A는 다음을 물리적으로 증명했다.

```text
동일 실제 attention invocation

Headwise pre-output-projection context
                ≈
TensorCube Stage12 normalized context
```

W8A는 이 동등성이 다음 범위에서 유지됨을 추가로 증명했다.

```text
decode geometry
prefill geometry
policy-derived chunk boundary
multi-layer anchor
all-masked exact-zero
causal boundary
GQA mapping
repeat determinism
scenario-isolated owner-zero
```

그러나 W8A까지 TensorCube context는 production decode continuation에 채택되지 않았다.

```text
TensorCube context
→ output projection
→ downstream transformer continuation
→ final logits
→ sampler
→ selected token
```

위 경로의 실제 authority는 아직 Headwise가 보유한다.

W9A는 pure shadow 단계를 반복하지 않는다.

W9A는 deterministic eligibility를 통과한 decode step에서 TensorCube context를 실제 production context로 선택하고, 동일 production output projection과 downstream model continuation을 거쳐 실제 logits candidate를 만든다.

다만 token commit 이전까지 decode step 전체를 forked transaction으로 유지한다.

```text
eligible decode step
→ TensorCube actual attention route
→ production output projection
→ downstream continuation
→ candidate logits
→ pre-sampler commit gate
→ 실제 sampler 1회
→ actual token commit
```

검증 실패 시:

```text
candidate fork 폐기
→ 같은 immutable step snapshot에서 Headwise 재실행
→ Headwise logits
→ 실제 sampler 1회
→ rollback token commit
```

W9A의 핵심은 TensorCube를 실제로 사용하는 것이다.

동시에 다음을 금지한다.

```text
commit 이전 main KV mutation
commit 이전 real sampler RNG mutation
commit 이전 token ledger append
commit 이전 user-visible stream emission
mismatch 이후 candidate token 노출
같은 step에서 sampler 2회 소비
receipt 없는 silent Headwise fallback
```

---

# 1. 현재 기준선

## 1.1 W8A에서 확정된 것

```text
Live Headwise Q/K/V
→ Texture-06 dynamic K/V residency
→ TensorCube Stage10
→ TensorCube Stage11
→ TensorCube Stage12 context
→ Headwise context와 device-local parity
```

확정된 보호선:

```text
full context host readback                 0
context materialization copy               0
stale partition passage                    0
scenario owner leak                         0
single-profile completion                  0
synthetic sentinel substitution            0
```

## 1.2 W9A가 새로 닫아야 하는 것

```text
TensorCube context actual selection
production output projection adoption
actual downstream hidden-state continuation
production logits candidate generation
pre-sampler atomic admission
same-invocation Headwise rollback
actual token commit
```

## 1.3 W9A가 증명하지 않는 것

W9A는 다음을 증명하지 않는다.

```text
모든 세션에서 TensorCube default authority
모든 layer에서 TensorCube authority
모든 device·driver에서 admission
Headwise rollback route 제거
TensorCube-only mode
장시간 fleet soak
BaseTrain forward/backward 공유
```

위 범위는 후속 W9B·W9C·W9D에서 다룬다.

---

# 2. Authority Map

## 2.1 Global authority

```text
Global default attention writer
  HeadwiseFullActive

Global rollback writer
  HeadwiseFullActive

Canary eligibility authority
  W9A Route SSOT

Pre-sampler token commit authority
  W9A Commit Gate
```

## 2.2 Eligible invocation authority

```text
qualified layer invocation
→ TensorCube context writer
→ production output projection input
→ actual downstream continuation
```

TensorCube가 선택된 invocation에서 `production_writer_promotion_count`는 0이 아니다.

W9A는 이 변화를 숨기지 않는다.

다만 이 권한은 다음 범위에만 귀속된다.

```text
exact model instance
exact decode session
exact step transaction
exact layer invocation
exact W8A-qualified geometry
exact device·driver allowlist
```

## 2.3 Ineligible invocation authority

```text
eligibility FAIL
→ Headwise actual route
→ no TensorCube candidate allocation required
```

## 2.4 Rollback authority

```text
candidate guard FAIL
sampled audit mismatch
non-finite logits
sampler preview mismatch
stale lineage
resource-lifetime failure

→ candidate fork revoke
→ Headwise same-step replay
```

## 2.5 금지 권한

```text
TensorCube global default promotion
Headwise rollback route deletion
operator receipt 없는 canary ratio 변경
sampler 이후 rollback
candidate bytes user-visible emission
candidate token ledger 조기 append
```

---

# 3. Canonical Route SSOT

## 3.1 Route ID

```rust
pub enum AttentionDecodeW9ARouteId {
    HeadwiseDefault,
    TensorCubeActualCanary,
    TensorCubeSampledAudit,
    HeadwiseRollbackReplay,
}
```

## 3.2 Route snapshot

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AttentionDecodeW9ARouteSnapshot {
    pub patch_id: String,
    pub build_revision: String,

    pub model_instance_id: String,
    pub model_instance_epoch: u64,
    pub checkpoint_digest: String,
    pub tokenizer_identity_digest: String,

    pub decode_session_id: String,
    pub decode_session_epoch: u64,
    pub decode_step: u64,

    pub layer_index: u32,
    pub q_seq: u32,
    pub seq_kv: u32,

    pub selected_route: AttentionDecodeW9ARouteId,
    pub canary_bucket: u32,
    pub audit_bucket: u32,

    pub w8a_parent_artifact_digest: String,
    pub w8a_matrix_receipt_digest: String,
    pub w8a_qualified_scenario_digest: String,

    pub device_identity_digest: String,
    pub driver_identity_digest: String,
    pub runtime_feature_digest: String,

    pub route_policy_digest: String,
    pub snapshot_digest: String,
}
```

## 3.3 Immutability

한 attention invocation이 시작된 뒤 다음은 변경할 수 없다.

```text
selected route
W8A qualification binding
model/checkpoint/tokenizer identity
device/driver identity
layer geometry
canary bucket
audit bucket
```

변경 감지 시 candidate path를 실행하지 않고 fail-closed Headwise route로 진입한다.

이 경우에도 explicit denial receipt를 남긴다.

---

# 4. Deterministic Canary Eligibility

## 4.1 Eligibility inputs

```text
model instance digest
checkpoint digest
tokenizer identity digest
W8A physical artifact digest
W8A matrix receipt digest
device identity
driver identity
runtime feature digest
session identity
decode step
layer index
q_seq / seq_kv
route policy revision
session quarantine state
rollback capability state
atomic stream sink capability
```

## 4.2 Qualification source

W9A는 W8A 명세의 기대값을 다시 계산하지 않는다.

다음 Rust-generated parent evidence를 채택한다.

```text
ash_attn_interconnect_w8a_physical_runtime_artifact.json
ash_attn_interconnect_w8a_physical_local_manifest.json
w8a_physical/matrix_receipt.json
w8a_physical/scenarios/*/compact_receipt.json
```

## 4.3 Initial layer allowlist

초기 W9A는 W8A physical receipt에 실제 PASS가 기록된 layer index만 TensorCube actual route로 허용한다.

```text
qualified layer set
= unique layer_index from W8A PASS scenario receipts
```

allowlist에 없는 layer는 Headwise를 사용한다.

따라서 한 decode step 안에서 다음 혼합이 가능하다.

```text
qualified layer    → TensorCube actual
unqualified layer  → Headwise actual
```

이 혼합 route 자체가 route snapshot에 기록되어야 한다.

## 4.4 Geometry allowlist

```text
(q_seq, seq_kv, layer_index, mask profile, causal route)
```

조합이 W8A receipt의 qualified domain 안에 있어야 한다.

단순히 `q_seq <= 16` 같은 범위 비교로 넓히면 안 된다.

## 4.5 Bucket derivation

```text
canary_key = SHA-256(
  route_policy_digest ||
  model_instance_id ||
  decode_session_id ||
  layer_index ||
  W8A artifact digest
)

canary_bucket = first_u32(canary_key) % canary_denominator
```

초기 권장값:

```text
canary_numerator   = 1
canary_denominator = 16
```

audit bucket:

```text
audit_key = SHA-256(canary_key || decode_step || "audit")
audit_bucket = first_u32(audit_key) % audit_denominator
```

초기 권장값:

```text
audit_numerator   = 1
audit_denominator = 8
```

## 4.6 Environment authority

환경변수는 canary를 끌 수 있다.

환경변수만으로 admission을 강제할 수는 없다.

```text
env disable  → allowed
env force-on → denied
```

## 4.7 Eligibility PASS

```text
parent W8A PASS                         true
artifact lineage exact                  true
model/checkpoint/tokenizer exact         true
device/driver allowlisted                true
geometry qualified                       true
layer qualified                          true
rollback fork available                  true
staging capacity available               true
sampler snapshot supported               true
atomic stream commit supported           true
session not quarantined                  true
canary bucket selected                   true
```

---

# 5. Decode Step Transaction

## 5.1 목적

TensorCube actual path가 실패해도 token commit 이전으로 완전히 복구할 수 있어야 한다.

W9A는 decode step을 main state에 직접 실행하지 않는다.

```text
main DecodeState
→ immutable step snapshot
→ candidate fork
→ commit gate
→ fork commit or fork discard
```

## 5.2 Step snapshot

```rust
pub struct AttentionDecodeW9AStepSnapshot {
    pub decode_session_id: String,
    pub decode_step: u64,

    pub input_token_id: u32,
    pub input_token_ledger_digest: String,
    pub position_state_digest: String,

    pub kv_snapshot_id: String,
    pub kv_generation: u64,
    pub kv_shape_digest: String,

    pub sampler_state_digest: String,
    pub sampler_rng_digest: String,
    pub penalty_state_digest: String,
    pub banned_token_mask_digest: String,
    pub eos_authority_digest: String,

    pub stream_sink_epoch: u64,
    pub stream_commit_count_before: u64,

    pub route_snapshot_digest: String,
    pub snapshot_digest: String,
}
```

## 5.3 Snapshot timing

```text
current input token 확정
→ main KV/position/sampler/token ledger snapshot
→ route selection
→ candidate fork 생성
```

## 5.4 Candidate fork

candidate fork는 다음을 독립적으로 보유한다.

```text
forked KV state
forked position state
forked hidden-state chain
forked intermediate buffers
forked logits buffer
forked resource owner epoch
```

candidate fork는 다음을 보유하지 않는다.

```text
main token ledger write authority
main sampler RNG mutation authority
user-visible stream authority
main DecodeState commit authority
```

## 5.5 Existing rollback integration

W9A는 기존 `KVSnapshotRef + TokenLedger + PositionState + ForkedReplayReceipt` 계보를 활용한다.

다만 환경변수 기반 capability 주장만으로 admission하지 않는다.

physical backend가 실제로 다음을 제공해야 한다.

```text
fork_from_snapshot
restore_to_fork
one_step replay
fork disposal
main state unchanged proof
```

---

# 6. TensorCube Actual Context Selection

## 6.1 Invocation flow

eligible layer:

```text
live Q/K/V
→ frozen partition generation
→ Texture-06
→ TensorCube Stage10
→ TensorCube Stage11
→ TensorCube Stage12 context
→ W9A route lease validate
→ production output projection input
```

ineligible layer:

```text
live Q/K/V
→ HeadwiseFullActive context
→ production output projection input
```

## 6.2 Actual writer receipt

TensorCube selected layer에서는 다음이 1이어야 한다.

```text
tensorcube_actual_context_selection_count = 1
production_output_projection_adoption_count = 1
```

다음은 0이어야 한다.

```text
shadow_only_completion_count = 0
headwise_context_selected_for_same_layer = 0
```

sampled audit에서는 Headwise oracle 계산이 추가되지만 production selected context는 TensorCube다.

## 6.3 Context lease

production output projection 직전에 다음을 다시 검증한다.

```text
route snapshot unchanged
invocation identity exact
context ABI exact
context owner live
submission completion observed
partition generation exact
layer index exact
```

검증 실패 시 output projection dispatch 전에 rollback으로 전환한다.

---

# 7. Production Output Projection Adoption

## 7.1 Canonical projection

W9A는 TensorCube 전용 output projection 수식을 만들지 않는다.

기존 production output projection을 그대로 사용한다.

```text
same weight buffer
same bias contract
same dtype profile
same layout contract
same residual integration
same normalization order
```

변경되는 것은 context input handle의 authority뿐이다.

## 7.2 Projection identity

```rust
pub struct AttentionDecodeW9AProjectionBinding {
    pub layer_index: u32,
    pub selected_context_source: AttentionDecodeW9ARouteId,
    pub context_handle_digest: String,
    pub projection_weight_digest: String,
    pub projection_bias_digest: Option<String>,
    pub input_abi: String,
    pub output_abi: String,
    pub dispatch_digest: String,
}
```

## 7.3 Projection mutation guard

금지:

```text
candidate 전용 weight clone
candidate 전용 projection kernel
host-side projection
layout copy for convenience
TensorCube path만 다른 precision 사용
```

---

# 8. Production Logits Continuation

## 8.1 Downstream continuation

TensorCube-selected context가 output projection을 통과한 뒤 candidate fork 안에서 나머지 transformer continuation을 실제로 수행한다.

```text
attention output projection
→ residual
→ subsequent layers
→ final normalization
→ LM head
→ candidate logits
```

이는 proxy logits가 아니다.

실제 production weight와 production decode graph를 사용한다.

## 8.2 Logits handle

```rust
pub struct AttentionDecodeW9ALogitsHandle {
    pub buffer_handle_digest: String,
    pub logical_offset_bytes: u64,
    pub logical_length_bytes: u64,
    pub vocab_size: u32,
    pub dtype: String,
    pub model_instance_id: String,
    pub decode_step: u64,
    pub fork_epoch: u64,
    pub route_snapshot_digest: String,
    pub completion_ticket_digest: String,
}
```

## 8.3 Logits guards

```text
vocab size exact
logical range exact
finite logits
no unexpected NaN/Inf
no out-of-range storage alias
LM-head weight digest exact
completion observed
```

## 8.4 No full logits readback

W9A는 전체 logits를 host로 읽지 않는다.

허용:

```text
compact numerical status
compact top-k IDs and scores
compact logits digest
selected token ID
```

금지:

```text
full vocab logits host roundtrip
CPU sampler fallback
host-side logits compare
```

---

# 9. Sampled Dual-Path Audit

## 9.1 Audit scope

TensorCube actual canary 중 deterministic audit bucket에 선택된 step만 Headwise oracle fork를 추가 실행한다.

```text
candidate fork
  TensorCube actual route

oracle fork
  Headwise route
```

main state는 어느 쪽에도 아직 커밋되지 않는다.

## 9.2 Same invocation identity

두 fork는 다음을 공유한다.

```text
same step snapshot
same input token
same KV snapshot generation
same position state
same model weights
same tokenizer binding
same sampler snapshot
same logits modifiers
same device/queue lineage
```

route만 다르다.

## 9.3 Audit stages

```text
A. selected attention context parity
B. post-output-projection hidden parity
C. final logits parity
D. top-k identity parity
E. pure sampler preview token parity
```

## 9.4 Device-local logits compare

```text
candidate logits buffer
oracle logits buffer
→ GPU comparator
→ compact 128-byte status
```

필수 상태:

```text
compared_logit_count
mismatch_count
candidate_non_finite_count
oracle_non_finite_count
max_absolute_error
max_relative_error
first_mismatch_index
candidate_top1_id
oracle_top1_id
top_k_overlap
compact_digest_match
```

## 9.5 Tolerance

W8 context tolerance와 별도로 logits tolerance를 둔다.

초기 제안:

```text
absolute_tolerance = 5.0e-4
relative_tolerance = 5.0e-3
relative_floor     = 1.0e-4
```

실제 baseline 측정 후 artifact SSOT로 고정한다.

## 9.6 Audit mismatch

하나라도 실패하면 candidate는 커밋할 수 없다.

```text
context mismatch
projection mismatch
logits mismatch
top1 mismatch
sampler preview token mismatch
non-finite
```

동시에 session TensorCube route를 quarantine한다.

---

# 10. Pure Sampler Preview

## 10.1 목적

sampled audit에서 candidate와 oracle이 같은 token candidate를 만드는지 확인하되 실제 sampler 상태를 소비하지 않는다.

## 10.2 Snapshot

```rust
pub struct AttentionDecodeW9ASamplerSnapshot {
    pub temperature_bits: u32,
    pub top_k: u32,
    pub top_p_bits: u32,
    pub min_p_bits: u32,
    pub repetition_penalty_bits: u32,
    pub repetition_window_digest: String,
    pub banned_token_mask_digest: String,
    pub eos_contract_digest: String,
    pub rng_state_digest: String,
    pub snapshot_digest: String,
}
```

## 10.3 Preview contract

```text
sampler preview
→ cloned immutable snapshot 사용
→ actual RNG state mutation 0
→ token ledger mutation 0
→ stream emission 0
```

## 10.4 Real sampler invocation

실제 sampler는 pre-sampler commit gate가 최종 logits source를 결정한 뒤 정확히 한 번 실행한다.

```text
candidate commit
→ candidate logits로 real sampler 1회

rollback commit
→ Headwise logits로 real sampler 1회
```

금지:

```text
candidate real sample 후 rollback
candidate와 oracle 각각 real sample
RNG state 두 번 advance
```

---

# 11. Pre-Sampler Commit Gate

## 11.1 Gate position

```text
candidate logits completion
→ optional dual-path audit
→ Pre-Sampler Commit Gate
→ final logits source selection
→ real sampler
→ token commit
```

## 11.2 Gate input

```rust
pub struct AttentionDecodeW9APreSamplerCommitInput {
    pub step_snapshot_digest: String,
    pub route_snapshot_digest: String,
    pub candidate_fork_digest: String,
    pub candidate_logits_digest: String,
    pub candidate_guard_digest: String,
    pub audit_required: bool,
    pub audit_receipt_digest: Option<String>,
    pub rollback_capability_digest: String,
    pub owner_state_digest: String,
}
```

## 11.3 Candidate admission

```text
route still eligible                     true
candidate fork complete                  true
candidate logits finite                  true
all owner leases valid                   true
main state unchanged                     true
sampler state unchanged                  true
stream commit count unchanged            true
W8A lineage exact                        true
audit result PASS when required          true
```

## 11.4 Gate result

```rust
pub enum AttentionDecodeW9ACommitDecision {
    CommitTensorCubeCandidate,
    ReplayHeadwiseThenCommit,
    AbortDecodeStep,
}
```

## 11.5 Candidate commit

```text
candidate fork becomes main decode state
candidate logits become sampler input
real sampler executes once
token ledger appends once
stream emits after atomic token commit
```

## 11.6 Rollback decision

```text
candidate fork revoked
candidate buffers drained
main state restored from same snapshot
Headwise replay fork created
same step rerun
Headwise logits admitted
real sampler executes once
Headwise fork committed
```

---

# 12. Headwise Same-Invocation Rollback

## 12.1 Same-invocation definition

```text
same model instance
same decode session
same decode step
same input token
same KV snapshot
same position state
same sampler snapshot
same logits modifiers
same tokenizer binding
```

## 12.2 Rollback trigger classes

```text
eligibility lineage drift after dispatch
TensorCube context guard fail
projection guard fail
candidate logits non-finite
sampled audit mismatch
sampler preview mismatch
candidate owner leak
submission failure
device error before commit
```

## 12.3 Rollback receipt

```rust
pub struct AttentionDecodeW9ARollbackReceipt {
    pub trigger_code: String,
    pub candidate_route_digest: String,
    pub step_snapshot_digest: String,

    pub candidate_fork_revoked: bool,
    pub candidate_owner_zero: bool,
    pub main_state_unchanged_before_replay: bool,

    pub headwise_replay_started: bool,
    pub headwise_replay_completed: bool,
    pub headwise_logits_digest: String,

    pub real_sampler_invocation_count: u32,
    pub token_commit_count: u32,
    pub stream_emit_count: u32,

    pub session_quarantined: bool,
    pub receipt_digest: String,
}
```

## 12.4 Session quarantine

rollback이 발생한 session은 남은 step에서 TensorCube actual route를 재활성화하지 않는다.

```text
candidate re-enable count = 0
```

다음 session은 policy와 artifact가 여전히 유효하면 새로 eligibility를 평가할 수 있다.

---

# 13. Atomic Token Commit

## 13.1 Commit order

```text
1. final logits source 확정
2. real sampler 1회
3. selected token ID 확정
4. forked KV/position state commit
5. sampler RNG state commit
6. token ledger append
7. decode state step increment
8. user-visible piece emission
9. final receipt publication
```

## 13.2 Atomicity

4부터 8까지 중간 실패가 발생하면 user-visible piece를 내보내면 안 된다.

stream sink는 atomic token fragment commit을 지원해야 한다.

지원하지 않으면 TensorCube canary eligibility를 거부한다.

## 13.3 Commit counters

성공한 step마다:

```text
real_sampler_invocation_count = 1
token_commit_count            = 1
stream_emit_count             = 0 or 1
candidate_byte_leak_count      = 0
double_commit_count            = 0
```

---

# 14. State Machine

```rust
pub enum AttentionDecodeW9AState {
    SnapshotSealed,
    RouteResolved,
    HeadwiseDefaultRunning,
    TensorCubeCandidateRunning,
    AuditOracleRunning,
    PreSamplerGatePending,
    CandidateCommitReady,
    RollbackPending,
    HeadwiseReplayRunning,
    HeadwiseCommitReady,
    TokenCommitted,
    SessionQuarantined,
    Aborted,
}
```

허용 전이:

```text
SnapshotSealed
→ RouteResolved

RouteResolved
→ HeadwiseDefaultRunning
→ TensorCubeCandidateRunning

TensorCubeCandidateRunning
→ AuditOracleRunning
→ PreSamplerGatePending
→ RollbackPending

AuditOracleRunning
→ PreSamplerGatePending
→ RollbackPending

PreSamplerGatePending
→ CandidateCommitReady
→ RollbackPending
→ Aborted

RollbackPending
→ HeadwiseReplayRunning
→ Aborted

HeadwiseReplayRunning
→ HeadwiseCommitReady
→ Aborted

CandidateCommitReady
→ TokenCommitted

HeadwiseCommitReady
→ TokenCommitted
```

금지 전이:

```text
TensorCubeCandidateRunning → TokenCommitted
AuditOracleRunning → TokenCommitted
RollbackPending → CandidateCommitReady
TokenCommitted → RollbackPending
SessionQuarantined → TensorCubeCandidateRunning
```

---

# 15. Sampled Audit and Non-Audit Actual Paths

W9A physical gate는 둘 다 증명해야 한다.

## 15.1 Actual non-audit

```text
TensorCube actual route
Headwise oracle 미실행
candidate logits commit
actual token commit
```

필수:

```text
tensorcube_actual_commit_count > 0
audit_dispatch_count = 0
headwise_replay_count = 0
```

## 15.2 Actual sampled audit

```text
TensorCube actual route
Headwise audit oracle 실행
audit PASS
candidate logits commit
actual token commit
```

필수:

```text
audit_dispatch_count > 0
audit_pass_count == audit_dispatch_count
candidate commit source 유지
```

## 15.3 Forced rollback

```text
TensorCube actual route
고의 mismatch 주입
audit 또는 guard FAIL
candidate revoke
Headwise same-step replay
Headwise token commit
```

필수:

```text
rollback_count > 0
candidate token exposure = 0
real sampler invocation = 1
token commit = 1
session quarantine = true
```

## 15.4 Headwise default

```text
ineligible bucket
→ Headwise direct actual route
```

TensorCube allocation과 dispatch가 없어야 한다.

---

# 16. Compact Receipts

## 16.1 Eligibility receipt

```rust
pub struct AttentionDecodeW9AEligibilityReceipt {
    pub selected: bool,
    pub denial_reasons: Vec<String>,
    pub canary_bucket: u32,
    pub audit_bucket: u32,
    pub qualified_layer: bool,
    pub qualified_geometry: bool,
    pub artifact_lineage_valid: bool,
    pub rollback_capability_valid: bool,
    pub atomic_stream_valid: bool,
    pub receipt_digest: String,
}
```

## 16.2 Step receipt

```rust
pub struct AttentionDecodeW9AStepReceipt {
    pub decode_session_id: String,
    pub decode_step: u64,
    pub route_snapshot_digest: String,
    pub step_snapshot_digest: String,

    pub selected_route: AttentionDecodeW9ARouteId,
    pub tensorcube_actual_layer_count: u32,
    pub headwise_actual_layer_count: u32,

    pub production_projection_adoption_count: u32,
    pub production_logits_continuation_count: u32,

    pub audit_required: bool,
    pub audit_pass: Option<bool>,
    pub rollback_triggered: bool,
    pub rollback_receipt_digest: Option<String>,

    pub final_logits_source: String,
    pub selected_token_id: u32,

    pub real_sampler_invocation_count: u32,
    pub token_commit_count: u32,
    pub stream_emit_count: u32,

    pub candidate_byte_leak_count: u32,
    pub full_logits_readback_count: u32,
    pub full_context_readback_count: u32,
    pub double_commit_count: u32,

    pub candidate_owner_zero: bool,
    pub oracle_owner_zero: bool,
    pub fork_disposed: bool,

    pub pass: bool,
    pub receipt_digest: String,
}
```

## 16.3 Session summary

```rust
pub struct AttentionDecodeW9ASessionSummary {
    pub total_steps: u64,
    pub headwise_default_steps: u64,
    pub tensorcube_actual_steps: u64,
    pub sampled_audit_steps: u64,
    pub rollback_steps: u64,
    pub committed_tensorcube_tokens: u64,
    pub committed_headwise_tokens: u64,
    pub quarantine_count: u64,
    pub candidate_byte_leak_count: u64,
    pub double_commit_count: u64,
    pub session_pass: bool,
    pub summary_digest: String,
}
```

---

# 17. Resource Lifetime

## 17.1 Candidate resources

```text
TensorCube context handles
Texture-06 owner leases
Stage10/11/12 buffers
projection output
intermediate hidden buffers
candidate logits
sampler preview scratch
```

candidate commit 또는 revoke 전까지 살아 있어야 한다.

## 17.2 Audit resources

```text
Headwise oracle context
oracle hidden chain
oracle logits
logits comparator scratch
```

pre-sampler gate 후 terminal drain한다.

## 17.3 Rollback resources

candidate revoke 후 owner-zero를 확인한 뒤 Headwise replay를 시작한다.

리소스 epoch가 겹치더라도 alias registry에서 main state와 충돌하면 안 된다.

## 17.4 Completion gate

```text
candidate commit path
  uncommitted scratch owner zero
  committed fork ownership transfer exact

rollback path
  candidate owner zero before Headwise replay commit

sampled audit path
  oracle owner zero before final receipt
```

---

# 18. Implementation File Plan

## 18.1 Backend

신규 권장 파일:

```text
crates/burn_webgpu_backend/src/
  attention_decode_w9a_logits_parity.rs
  attention_decode_w9a_topk_digest.rs

crates/burn_webgpu_backend/src/shaders/
  attention_decode_w9a_logits_compare.wgsl
  attention_decode_w9a_topk_digest.wgsl
```

기존 production projection과 LM-head 커널을 재사용한다.

## 18.2 Model core

```text
crates/model_core/src/
  attention_decode_w9a.rs
  attention_decode_w9a_route_ssot.rs
  attention_decode_w9a_step_transaction.rs
  attention_decode_w9a_pre_sampler_commit.rs
```

연결 대상:

```text
decode_runtime_binding.rs
generation_sampling.rs
headwise_fullactive_promotion.rs
attention_runtime_shape_authority.rs
kv_rollback01_forked_replay.rs
```

기존 FT14·FT15·FT16의 비교 개념은 참고할 수 있다.

그러나 해당 synthetic/shadow artifact를 W9A production authority로 직접 채택하면 안 된다.

## 18.3 Orchestrator

```text
crates/orchestrator_local/src/
  attention_decode_w9a_artifact_wave_map.rs
  attention_decode_w9a_cli_registry.rs
  attention_decode_w9a_scenario_plan.rs

crates/orchestrator_local/src/bin/
  ash_attn_decode_w9a_verification_gate.rs
  ash_attn_decode_w9a_physical_gate.rs
```

## 18.4 CLI

```text
specs/cli/
  ash_attn_decode_w9a_verification.args
  ash_attn_decode_w9a_physical.args
```

---

# 19. Verification Gate

## 19.1 Static checks

```text
W8A parent revision exact
W8A artifact paths canonical
route SSOT module registered
step transaction module registered
pre-sampler gate registered
sampler real invocation behind gate only
user-visible stream behind token commit only
Headwise rollback route reachable
silent fallback string absent
```

## 19.2 State machine checks

모든 허용 전이와 금지 전이를 unit test한다.

## 19.3 Eligibility checks

```text
qualified layer select
unqualified layer deny
qualified geometry select
unqualified geometry deny
stale W8A artifact deny
unsupported device deny
quarantined session deny
rollback unavailable deny
atomic stream unavailable deny
```

## 19.4 Sampler checks

```text
preview does not mutate RNG
preview does not append token
real sampler exactly once
rollback real sampler exactly once
```

## 19.5 Commit checks

```text
candidate commit path
rollback commit path
abort path
forced double commit denial
forced early stream emission denial
```

---

# 20. Physical Gate Scenarios

최소 권장 시나리오:

## P0 Headwise default control

```text
canary bucket ineligible
→ Headwise actual token commit
```

## P1 TensorCube actual non-audit

```text
qualified session
qualified layer set
no audit
→ TensorCube-influenced actual token commit
```

## P2 TensorCube sampled audit PASS

```text
candidate + oracle fork
context/projection/logits/token preview parity
→ candidate token commit
```

## P3 Forced context mismatch rollback

```text
candidate context mismatch
→ no candidate commit
→ Headwise replay
→ Headwise token commit
```

## P4 Forced logits mismatch rollback

```text
context gate PASS
logits audit mismatch
→ Headwise replay
```

## P5 Forced sampler preview mismatch rollback

```text
logits parity tolerance PASS
preview token mismatch
→ Headwise replay
```

## P6 Stale W8A lineage denial

```text
stale parent digest
→ TensorCube dispatch count 0
→ Headwise default
```

## P7 Session quarantine

```text
step N rollback
step N+1 candidate eligibility denied
```

## P8 Multi-token continuation

```text
actual canary session
minimum 8 committed tokens
TensorCube actual token count > 0
no double commit
```

---

# 21. CLI Contract

필수 키:

```text
--patch-id
--expected-build-revision
--parent-w8a-artifact
--parent-w8a-manifest
--parent-w8a-matrix-receipt

--canary-numerator
--canary-denominator
--audit-numerator
--audit-denominator

--require-actual-tensorcube-commit
--require-sampled-audit
--require-forced-rollback
--require-headwise-default-control

--require-atomic-stream
--require-forked-kv-state
--require-sampler-snapshot
--deny-full-logits-readback
--deny-full-context-readback
--deny-silent-fallback

--max-new-tokens
--fixture-prompt
--fixture-seed

--out-runtime-specification
--out-runtime-artifact
--out-local-manifest
--out-scenario-directory
```

CLI는 key/value pair 형식으로 유지한다.

unknown key와 duplicate key는 FAIL한다.

---

# 22. Rust-Generated Artifacts

```text
workspace/runtime/attention/decode/
  ash_attn_decode_w9a_verification_runtime_specification.json
  ash_attn_decode_w9a_verification_runtime_artifact.json
  ash_attn_decode_w9a_verification_local_manifest.json

  ash_attn_decode_w9a_physical_runtime_specification.json
  ash_attn_decode_w9a_physical_runtime_artifact.json
  ash_attn_decode_w9a_physical_local_manifest.json
```

scenario lanes:

```text
workspace/runtime/attention/decode/w9a_physical/
  route_policy.json
  scenario_plan.json
  eligibility/*.json
  steps/*.json
  audits/*.json
  rollbacks/*.json
  session_summary.json
```

매니페스트와 아티팩트는 ZIP에 포함하지 않는다.

실행 중 Rust가 생성한다.

---

# 23. PASS Criteria

## 23.1 Parent evidence

```text
W8A physical artifact PASS                    true
W8A manifest digest exact                     true
W8A matrix receipt PASS                       true
```

## 23.2 Actual adoption

```text
tensorcube_actual_step_count                  > 0
tensorcube_actual_layer_count                 > 0
production_projection_adoption_count          > 0
production_logits_continuation_count          > 0
committed_tensorcube_token_count              > 0
shadow_only_completion_count                  0
```

## 23.3 Sampled audit

```text
sampled_audit_count                           > 0
audit_context_mismatch_count                  0
audit_projection_mismatch_count               0
audit_logits_mismatch_count                   0
audit_sampler_preview_mismatch_count           0
```

## 23.4 Rollback

```text
forced_rollback_count                         > 0
headwise_same_invocation_replay_count         > 0
rollback_token_commit_count                   > 0
candidate_token_exposure_count                0
candidate_byte_leak_count                     0
session_quarantine_count                      > 0
candidate_reenable_after_quarantine_count      0
```

## 23.5 Sampler and commit

```text
real_sampler_invocation_count
== committed_token_count

double_sampler_invocation_count               0
double_token_commit_count                     0
early_stream_emit_count                       0
```

## 23.6 Resource lifetime

```text
candidate_fork_disposed_or_committed           100%
audit_oracle_owner_zero                       100%
rollback_candidate_owner_zero                 100%
stale_handle_passage                          0
```

## 23.7 Readback and fallback

```text
full_context_readback_count                   0
full_logits_readback_count                    0
CPU sampler fallback count                    0
silent fallback count                         0
```

## 23.8 Global authority preservation

```text
Headwise global default authority             maintained
TensorCube eligible step authority            observed
Headwise rollback authority                   maintained
TensorCube-only global mode                    false
```

---

# 24. FAIL/HOLD Codes

## Parent and identity

```text
AttentionDecodeW9AParentW8AArtifactMissing
AttentionDecodeW9AParentW8ANotPass
AttentionDecodeW9AParentDigestMismatch
AttentionDecodeW9ABuildRevisionMismatch
AttentionDecodeW9ARouteSnapshotDrift
AttentionDecodeW9AStepSnapshotMismatch
```

## Eligibility

```text
AttentionDecodeW9AModelNotQualified
AttentionDecodeW9ADeviceNotQualified
AttentionDecodeW9ADriverNotQualified
AttentionDecodeW9ALayerNotQualified
AttentionDecodeW9AGeometryNotQualified
AttentionDecodeW9ARollbackUnavailable
AttentionDecodeW9AAtomicStreamUnavailable
AttentionDecodeW9ASessionQuarantined
```

## Candidate path

```text
AttentionDecodeW9ATensorCubeContextUnavailable
AttentionDecodeW9AProjectionBindingMismatch
AttentionDecodeW9ACandidateLogitsNonFinite
AttentionDecodeW9ACandidateOwnerLeak
AttentionDecodeW9ACandidateMainStateMutation
```

## Audit

```text
AttentionDecodeW9AAuditContextMismatch
AttentionDecodeW9AAuditProjectionMismatch
AttentionDecodeW9AAuditLogitsMismatch
AttentionDecodeW9AAuditTopKParityMismatch
AttentionDecodeW9AAuditSamplerPreviewMismatch
```

## Rollback

```text
AttentionDecodeW9ACandidateRevokeFailed
AttentionDecodeW9AMainStateChangedBeforeReplay
AttentionDecodeW9AHeadwiseReplayFailed
AttentionDecodeW9ARollbackForkLeak
AttentionDecodeW9AQuarantineReenableDetected
```

## Commit

```text
AttentionDecodeW9ARealSamplerInvokedBeforeGate
AttentionDecodeW9ARealSamplerDoubleInvocation
AttentionDecodeW9ATokenDoubleCommit
AttentionDecodeW9AEarlyStreamEmission
AttentionDecodeW9AUnrecoverableTokenCommit
AttentionDecodeW9ASilentFallbackDetected
```

---

# 25. 금지 구현

```text
W8A artifact 없이 route enable
shape 범위 추정으로 qualification 확대
모든 layer를 자동 allowlist
candidate path에서 main KV 직접 mutation
candidate path에서 real RNG 직접 mutation
sampler 실행 후 rollback
candidate와 oracle 각각 real sampler 실행
full logits CPU compare
full context CPU compare
Headwise replay 없는 candidate failure 완화
rollback receipt 없는 Headwise fallback
candidate token piece 선출력
TensorCube global default promotion
```

---

# 26. Required Static Assertions

```text
size_of::<AttentionDecodeW9ARouteSnapshot>() bounded
route policy digest non-empty
canary denominator > 0
audit denominator > 0
canary numerator <= denominator
audit numerator <= denominator

real sampler call site
  reachable only after Pre-Sampler Commit Gate

stream emit call site
  reachable only after token commit

candidate path
  no main DecodeState mutable lease

rollback path
  same step snapshot digest required
```

---

# 27. Proposed PASS Token

```text
PASS_ASH_ATTN_DECODE_W9A_TENSORCUBE_ACTUAL_CONTEXT_SELECTION_PRE_OUTPUT_PROJECTION_ROUTE_SSOT_PRODUCTION_OUTPUT_PROJECTION_ADOPTION_PRODUCTION_LOGITS_CONTINUATION_PRE_SAMPLER_COMMIT_GATE_DETERMINISTIC_CANARY_ELIGIBILITY_HEADWISE_SAME_INVOCATION_ROLLBACK_SAMPLED_DUAL_PATH_AUDIT_REAL_SAMPLER_SINGLE_INVOCATION_ATOMIC_TOKEN_COMMIT_SESSION_QUARANTINE_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

---

# 28. Completion Statement

W9A 완료 시 다음 문장이 사실이어야 한다.

```text
W8A-qualified decode session과 layer invocation에서
TensorCube context가 실제 production output projection 입력으로 선택되고,
실제 downstream model graph를 통해 logits까지 이어지며,
pre-sampler commit gate를 통과한 candidate logits가
실제 sampler와 token commit에 사용됐다.

sampled audit mismatch 또는 guard failure 시
candidate fork는 token 노출 없이 폐기되고,
동일 immutable decode-step snapshot에서 Headwise가 재실행되어
sampler는 정확히 한 번만 실행되고 token은 정확히 한 번만 커밋됐다.
```

---

# 29. 다음 패치 경계

W9A PASS 후 권장 순서:

```text
ASH-ATTN-DECODE-W9B
  Actual Canary Expansion /
  Full-Layer Qualification /
  Canary Ratio Promotion /
  Long-Session Soak /
  Performance Budget /
  Cross-Device Allowlist /
  Rollback Drill Matrix

ASH-ATTN-DECODE-W9C
  TensorCube Global Default Writer Promotion /
  Headwise Rollback Oracle /
  Atomic Authority Pointer Switch

ASH-ATTN-DECODE-W9D
  Long-Context Residency Plateau /
  Device-Loss Recovery /
  Three-Cycle Replay /
  Production Hardening
```

W9A는 shadow가 아니다.

W9A는 제한된 deterministic domain에서 TensorCube가 실제 token 생성 경로에 들어가는 첫 actual authority patch다.
