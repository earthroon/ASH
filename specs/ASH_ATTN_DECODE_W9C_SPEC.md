# ASH-ATTN-DECODE-W9C

## TensorCube Global Default Writer Promotion /
## Atomic Authority Pointer Switch /
## Headwise Rollback-Only Oracle /
## Default Route Artifact Adoption /
## Instant Demotion /
## Cross-Session Authority Consistency /
## No Dual Production Writer Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-DECODE-W9C`  
> Proposed build revision: `W9C-w9b-global-default-authority-switch-r1`  
> Parent: `ASH-ATTN-DECODE-W9B`  
> Parent state: `PHYSICAL PASS`  
> Parent TensorCube authority: qualified-domain actual writer  
> Parent global default writer: `HeadwiseFullActive`  
> W9C target global default writer: `TensorCube`  
> W9C rollback-only oracle: `HeadwiseFullActive`  
> W9C token commit authority: `W9A Pre-Sampler Commit Gate`  
> Global switch scope: exact adopted authority domain only  
> Dual production writer: forbidden  
> Silent fallback: forbidden  
> Next authority patch: `ASH-ATTN-DECODE-W9D`

---

# 0. 상태 구분

## 확정

사용자 로컬 물리 실행에서 다음 W9B PASS 토큰이 관측됐다.

```text
PASS_ASH_ATTN_DECODE_W9B_ACTUAL_CANARY_EXPANSION_FULL_LAYER_QUALIFICATION_CANARY_RATIO_PROMOTION_LONG_SESSION_TOKEN_SOAK_LATENCY_VRAM_BUDGET_CROSS_DEVICE_ALLOWLIST_ROLLBACK_DRILL_MATRIX_THREE_WINDOW_STABILITY_DETERMINISTIC_ROUTE_PINNING_HEADWISE_GLOBAL_DEFAULT_PRESERVATION_NO_FULL_CONTEXT_READBACK_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_TENSORCUBE_ACTUAL_ROUTE_STABILITY_SEALED
```

따라서 W9C는 다음을 부모 물리 권위로 채택한다.

```text
TensorCube full-layer qualification
TensorCube qualified-domain actual writer
canary ratio promotion completion
long-session token soak PASS
latency budget PASS
VRAM budget PASS
cross-device allowlist binding
rollback drill matrix PASS
three-window stability PASS
deterministic route pinning
Headwise global default preservation
no full context readback
no full logits readback
no silent fallback
no unrecoverable token commit
```

## 제안

이 문서의 authority artifact schema, atomic pointer protocol, generation epoch, startup adoption, demotion barrier, cross-session consistency receipt, rollback-only oracle contract는 W9C 구현 계약 제안이다.

## 판단 불가

현재 대화 로그만으로 다음은 확정할 수 없다.

```text
global default 전환 뒤 실제 production session 수
권한 포인터 교체 중 동시 decode-step 경쟁 상태
process restart 뒤 artifact 재채택 안정성
demotion fault injection의 실제 latency
global TensorCube default에서의 장기 fleet 안정성
```

W9C physical gate가 위 항목을 판정한다.

---

# 1. 목적

W9B까지 TensorCube는 다음 권한을 획득했다.

```text
qualified-domain actual writer
full-layer qualified
canary ratio promoted
long-session stable
latency budget bound
VRAM budget bound
device allowlist bound
rollback drill bound
```

그러나 global default writer는 여전히 Headwise였다.

W9C의 목적은 다음 단일 권한 전환을 물리적으로 닫는 것이다.

```text
Headwise global default writer
→
TensorCube global default writer
```

이 전환은 단순 Boolean 변경이 아니다.

다음이 동시에 성립해야 한다.

```text
1. default route artifact가 정확한 parent evidence를 가진다.
2. authority pointer가 torn state 없이 원자적으로 교체된다.
3. 모든 신규 decode-step이 하나의 authority generation만 관측한다.
4. Headwise는 production writer가 아니라 rollback-only oracle로 내려간다.
5. fault가 발생하면 token commit 전에 즉시 Headwise로 demotion한다.
6. process·thread·session 경계에서 같은 default authority를 재현한다.
7. 어떤 invocation에서도 production writer가 둘이 되지 않는다.
```

W9C PASS 후 다음 문장이 사실이어야 한다.

```text
정확히 채택된 W9C default-route artifact의 authority domain 안에서
TensorCube가 global default attention writer로 동작했다.

Headwise는 일반 production route에 참여하지 않았고,
audit 또는 rollback이 필요한 경우에만 oracle writer로 실행됐다.

authority switch와 demotion은 generation-bound atomic snapshot으로 수행됐으며,
어떤 token commit에서도 두 production writer가 동시에 권한을 갖지 않았다.
```

---

# 2. 핵심 비목표

W9C는 다음을 수행하지 않는다.

```text
Headwise 구현 삭제
Headwise weight 제거
Headwise rollback 경로 제거
TensorCube 계산 수식 변경
새 sampler 수식 도입
새 LM-head 수식 도입
device allowlist 자동 확장
driver allowlist 자동 확장
authority artifact 없는 환경변수 강제 승격
token commit 이후 rollback
full context host readback
full logits host readback
dual production writer warm standby
오류를 무시한 자동 재승격
fleet-wide remote control plane
```

다음은 W9D 이후 범위다.

```text
post-promotion sustained fleet soak
remote authority artifact rollout
multi-device fleet promotion
authority artifact revocation propagation
recovery-aware device-loss re-adoption
```

---

# 3. Authority Domain

## 3.1 Global의 의미

W9C에서 `global default writer`는 모든 가능한 하드웨어와 모든 모델을 뜻하지 않는다.

다음 exact authority domain 안에서의 process-global default를 뜻한다.

```text
model instance digest
checkpoint digest
tokenizer digest
runtime build revision
device allowlist entry digest
driver identity digest
runtime feature digest
limits digest
layer qualification digest
geometry qualification digest
latency budget digest
VRAM budget digest
rollback matrix digest
W9B stability seal digest
```

authority domain 밖에서는 TensorCube global default를 주장할 수 없다.

## 3.2 Domain mismatch 동작

다음 중 하나라도 불일치하면:

```text
artifact adoption denied
TensorCube global default denied
Headwise safe default retained
W9C global promotion receipt not emitted
```

단, 이것은 silent fallback이 아니다.

반드시 명시적 startup decision receipt를 남긴다.

```text
DefaultRouteArtifactRejected
HeadwiseSafeDefaultRetained
```

## 3.3 Domain immutability

process lifetime 중 authority domain digest는 immutable하다.

다음 변경은 process restart 또는 명시적 re-adoption이 필요하다.

```text
checkpoint 변경
tokenizer 변경
driver 변경
device 변경
runtime feature 변경
layer graph 변경
projection weight 변경
W9B artifact 변경
```

---

# 4. Authority Roles

## 4.1 W9C PASS 전

```text
Global default writer
  HeadwiseFullActive

Qualified canary writer
  TensorCube

Rollback writer
  HeadwiseFullActive

Audit oracle
  HeadwiseFullActive
```

## 4.2 W9C PASS 후

```text
Global default writer
  TensorCube

Rollback-only oracle
  HeadwiseFullActive

Audit oracle
  HeadwiseFullActive

Token commit authority
  W9A Pre-Sampler Commit Gate

Authority pointer owner
  W9C Default Route Manager
```

## 4.3 금지 역할

```text
Headwise production default
and
TensorCube production default
```

가 동시에 활성일 수 없다.

## 4.4 Oracle의 정의

Headwise oracle은 다음 상황에만 실행 가능하다.

```text
sampled audit
pre-commit rollback
fault injection drill
authority demotion verification
```

일반 성공 경로에서 Headwise를 병렬 production writer로 실행하면 안 된다.

---

# 5. Default Authority State Machine

```rust
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum AttentionDecodeW9CDefaultAuthorityState {
    HeadwiseSafeDefault,
    TensorCubePromotionPending,
    TensorCubeGlobalDefault,
    DemotionPending,
    HeadwiseDemotedSafeDefault,
    Quarantined,
}
```

## 5.1 허용 전이

```text
HeadwiseSafeDefault
→ TensorCubePromotionPending
→ TensorCubeGlobalDefault

TensorCubeGlobalDefault
→ DemotionPending
→ HeadwiseDemotedSafeDefault

HeadwiseDemotedSafeDefault
→ TensorCubePromotionPending
```

재승격은 새 physical stability receipt가 있어야 한다.

## 5.2 금지 전이

```text
HeadwiseSafeDefault → TensorCubeGlobalDefault
TensorCubeGlobalDefault → HeadwiseSafeDefault
Quarantined → TensorCubeGlobalDefault
DemotionPending → TensorCubeGlobalDefault
```

중간 state를 건너뛰는 전이는 금지한다.

## 5.3 Quarantine

다음 fault는 profile을 quarantined 상태로 만든다.

```text
dual production writer observation
authority generation drift
artifact digest mismatch
post-commit rollback attempt
unrecoverable token commit
owner leak after demotion
repeated demotion barrier failure
```

Quarantined 상태에서는 process restart만으로 자동 재승격하지 않는다.

---

# 6. Default Route Artifact

## 6.1 Artifact schema

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AttentionDecodeW9CDefaultRouteArtifact {
    pub patch_id: String,
    pub build_revision: String,

    pub parent_w9b_artifact_digest: String,
    pub parent_w9b_manifest_digest: String,
    pub parent_w9b_stability_seal_digest: String,

    pub model_instance_digest: String,
    pub checkpoint_digest: String,
    pub tokenizer_digest: String,

    pub device_allowlist_entry_digest: String,
    pub driver_identity_digest: String,
    pub runtime_feature_digest: String,
    pub limits_digest: String,

    pub layer_qualification_digest: String,
    pub geometry_qualification_digest: String,
    pub latency_budget_digest: String,
    pub vram_budget_digest: String,
    pub rollback_matrix_digest: String,

    pub promoted_writer: String,
    pub rollback_oracle: String,
    pub token_commit_authority: String,

    pub initial_authority_generation: u64,
    pub artifact_created_unix_ms: u64,

    pub artifact_payload_digest: String,
    pub artifact_digest: String,
}
```

## 6.2 Required values

```text
promoted_writer
  TensorCube

rollback_oracle
  HeadwiseFullActive

token_commit_authority
  W9A_PreSamplerCommitGate
```

## 6.3 Artifact authority

artifact는 사람이 직접 편집한 JSON이 authority가 아니다.

```text
Rust builder
→ canonical payload
→ SHA-256
→ atomic write
→ readback parse
→ digest verify
→ adoption candidate
```

## 6.4 Artifact rejection

다음은 adoption을 거부한다.

```text
unknown field
missing field
duplicate semantic field
parent digest mismatch
build revision mismatch
model digest mismatch
device identity mismatch
driver identity mismatch
feature digest mismatch
budget receipt not PASS
rollback matrix not PASS
W9B stability seal not PASS
promoted writer not TensorCube
rollback oracle not Headwise
token commit authority mismatch
```

---

# 7. Atomic Authority Pointer

## 7.1 목표

다음 torn state를 금지한다.

```text
writer = TensorCube
rollback = unavailable

writer = Headwise
artifact = TensorCube

generation = new
route snapshot = old
```

## 7.2 Snapshot

```rust
#[derive(Debug, Clone)]
pub struct AttentionDecodeW9CAuthoritySnapshot {
    pub state: AttentionDecodeW9CDefaultAuthorityState,
    pub generation: u64,
    pub authority_domain_digest: String,
    pub default_route_artifact_digest: String,
    pub production_writer: AttentionDecodeProductionWriter,
    pub rollback_oracle: AttentionDecodeRollbackOracle,
    pub token_commit_authority: AttentionDecodeTokenCommitAuthority,
    pub snapshot_digest: String,
}
```

## 7.3 Pointer holder

권장 구현:

```rust
pub struct AttentionDecodeW9CAuthorityHolder {
    current: ArcSwap<AttentionDecodeW9CAuthoritySnapshot>,
    transition_lock: Mutex<()>,
    next_generation: AtomicU64,
}
```

동등한 lock-free 또는 lock-assisted 구현도 허용한다.

필수 조건:

```text
read snapshot is atomic
publish snapshot is atomic
generation strictly increases
old snapshot remains alive while readers hold Arc
```

## 7.4 Read boundary

decode-step은 시작 시 snapshot을 정확히 한 번 읽는다.

```text
step begin
→ authority snapshot acquire
→ route execution
→ pre-sampler gate
→ token commit or rollback
→ step end
```

step 중간에 pointer가 바뀌어도 해당 step은 pinned snapshot으로 끝낸다.

예외:

```text
demotion barrier fault
```

이 경우 token commit 전에 current step을 abort하고 Headwise replay한다.

## 7.5 Publish protocol

```text
transition lock acquire
→ current snapshot verify
→ candidate snapshot build
→ candidate digest verify
→ generation increment
→ atomic pointer swap
→ publication receipt write
→ transition lock release
```

publication receipt write가 실패하면 새 pointer를 authority로 인정하지 않는다.

권장:

```text
receipt prepare
→ fsync
→ pointer publish
→ publication finalize
```

또는 동등한 recoverable two-phase protocol을 사용한다.

---

# 8. Promotion Transaction

## 8.1 Prepare phase

```text
W9B parent artifact readback
default route artifact validation
authority domain validation
Headwise rollback oracle reachability
TensorCube full-layer route reachability
pre-sampler commit gate reachability
stream emission barrier reachability
owner-zero baseline
```

## 8.2 Candidate phase

```text
TensorCube candidate snapshot build
candidate generation = current + 1
candidate artifact digest bind
candidate snapshot digest compute
```

## 8.3 Commit phase

```text
atomic pointer swap
publication receipt commit
global default observation probe
```

## 8.4 Post-commit probe

promotion 직후 실제 decode-step을 최소 세 번 실행한다.

```text
session A
session B
session C
```

각 session은 TensorCube global default를 관측해야 한다.

## 8.5 Rollback of promotion transaction

pointer publication 전에 실패:

```text
HeadwiseSafeDefault 유지
generation 증가 없음
promotion receipt FAIL
```

pointer publication 뒤 post-commit probe 실패:

```text
instant demotion
new demotion generation publication
HeadwiseDemotedSafeDefault
promotion artifact quarantined
```

---

# 9. Per-Step Writer Selection

## 9.1 Production route

```rust
pub enum AttentionDecodeProductionWriter {
    TensorCube,
    Headwise,
}
```

W9C promoted state에서 정상 값:

```text
TensorCube
```

## 9.2 Rollback route

```rust
pub enum AttentionDecodeRollbackOracle {
    HeadwiseFullActive,
}
```

## 9.3 No dual writer invariant

```text
production_writer_count = 1
```

audit가 활성일 때:

```text
production_writer_count = 1
oracle_writer_count     = 1
```

audit가 비활성일 때:

```text
production_writer_count = 1
oracle_writer_count     = 0
```

## 9.4 Forbidden behavior

다음은 FAIL이다.

```text
TensorCube와 Headwise 결과를 둘 다 production candidate로 append
먼저 끝난 writer를 선택
두 writer가 sampler를 각각 호출
두 writer가 token ledger에 접근
두 writer가 stream emitter에 접근
```

---

# 10. Headwise Rollback-Only Oracle

## 10.1 Normal path prohibition

TensorCube global default 상태에서 정상 성공 step은 Headwise production projection을 실행하지 않는다.

sampled audit를 제외하면:

```text
headwise_execution_count = 0
```

## 10.2 Rollback trigger

```text
TensorCube context guard mismatch
TensorCube projection failure
non-finite candidate logits
compact logits parity failure
sampler preview mismatch
authority snapshot drift
owner leak suspicion
submission failure before commit
device loss before commit
demotion barrier activation
```

## 10.3 Same-step replay

```text
candidate step snapshot
→ TensorCube attempt
→ fault before commit
→ candidate state discard
→ Headwise replay from same step snapshot
→ real sampler exactly once
→ token commit exactly once
```

## 10.4 Oracle isolation

Headwise oracle 결과는 rollback이 승인되기 전까지 다음에 접근할 수 없다.

```text
token ledger
stream emitter
conversation state
persistent KV authority
sampler mutable state
```

## 10.5 Oracle owner-zero

rollback 또는 audit 종료 후:

```text
Headwise oracle temporary owner count = 0
TensorCube failed candidate owner count = 0
```

---

# 11. Instant Demotion

## 11.1 정의

instant demotion은 fault 관측 뒤 다음 신규 token commit보다 먼저 global default authority를 Headwise로 전환하는 것이다.

wall-clock 0ms를 의미하지 않는다.

## 11.2 Demotion trigger classes

### Numerical

```text
non-finite context
non-finite logits
parity threshold breach
top-k identity breach
sampler preview mismatch
```

### Lifetime

```text
candidate owner leak
stale partition generation
VRAM plateau breach
post-drain residue breach
```

### Authority

```text
generation drift
artifact digest drift
route snapshot drift
dual production writer observation
writer role mismatch
```

### Runtime

```text
submission failure
device loss before commit
timestamp-query integrity failure
feature identity drift
```

## 11.3 Demotion barrier

```rust
pub struct AttentionDecodeW9CDemotionBarrier {
    pub fault_epoch: u64,
    pub observed_generation: u64,
    pub fault_code: String,
    pub commit_blocked: bool,
    pub replay_required: bool,
    pub demotion_snapshot_published: bool,
    pub barrier_digest: String,
}
```

## 11.4 Barrier behavior

fault가 감지되면:

```text
pre-sampler commit blocked
stream emission blocked
token ledger append blocked
new TensorCube step admission blocked
demotion transaction started
current step Headwise replay required
```

## 11.5 Demotion publication

```text
TensorCubeGlobalDefault generation N
→ DemotionPending generation N+1
→ HeadwiseDemotedSafeDefault generation N+2
```

각 generation은 receipt를 가진다.

## 11.6 Demotion completion

다음 모두 만족해야 demotion complete다.

```text
Headwise default pointer active
TensorCube new-step admission zero
current faulted step resolved
candidate owners zero
stream emission count correct
token commit count correct
demotion receipt durable
```

---

# 12. Cross-Session Authority Consistency

## 12.1 목표

동시에 시작되는 여러 session이 서로 다른 global default를 관측하는 문제를 방지한다.

## 12.2 Session authority receipt

```rust
pub struct AttentionDecodeW9CSessionAuthorityReceipt {
    pub session_id: String,
    pub session_epoch: u64,
    pub process_epoch: u64,
    pub authority_generation: u64,
    pub authority_domain_digest: String,
    pub default_route_artifact_digest: String,
    pub observed_production_writer: String,
    pub rollback_oracle: String,
    pub first_step_invocation_digest: String,
    pub receipt_digest: String,
}
```

## 12.3 Promotion consistency

promotion 뒤 시작한 모든 session은:

```text
same authority generation
same artifact digest
same production writer = TensorCube
```

를 관측해야 한다.

## 12.4 Existing session behavior

promotion 이전에 시작된 session은 두 정책 중 하나를 명시적으로 선택해야 한다.

권장 W9C 정책:

```text
existing sessions remain pinned to old generation
new sessions use new generation
```

old-generation session 종료 후 old snapshot owner count가 0이 되어야 한다.

## 12.5 Demotion consistency

demotion barrier 이후:

```text
new sessions
  Headwise generation only

existing TensorCube sessions
  next step admission blocked
  Headwise replay or safe termination
```

## 12.6 Cross-thread replay

동일한 session corpus를 thread scheduling 순서만 바꿔 최소 세 번 실행한다.

다음은 같아야 한다.

```text
authority generation
writer selection
token sequence
demotion decision
receipt semantics
```

---

# 13. Process Restart Adoption

## 13.1 Startup sequence

```text
runtime build identity
→ device identity
→ driver identity
→ W9B parent artifact
→ W9C default route artifact
→ authority domain reconstruction
→ artifact digest verification
→ Headwise oracle reachability
→ TensorCube route reachability
→ atomic holder initialization
```

## 13.2 Startup state

artifact adoption PASS:

```text
TensorCubeGlobalDefault
```

artifact adoption FAIL:

```text
HeadwiseSafeDefault
```

## 13.3 Three-cycle replay

최소 세 번:

```text
process start
→ artifact adoption
→ three sessions
→ terminal drain
→ process exit
```

세 cycle에서 다음이 같아야 한다.

```text
default route artifact digest
authority domain digest
initial generation semantics
production writer
token output digest
owner-zero result
```

## 13.4 Corrupted artifact drill

다음 corruption을 각각 주입한다.

```text
single-byte payload mutation
parent digest mutation
writer role mutation
device digest mutation
build revision mutation
```

모두 startup adoption을 거부해야 한다.

---

# 14. Authority Generation

## 14.1 Generation rules

```text
strictly monotonic
never reused within process epoch
promotion increments
demotion-pending increments
demotion-complete increments
```

## 14.2 Process epoch

```rust
pub struct AttentionDecodeW9CProcessEpoch {
    pub process_epoch_id: String,
    pub boot_artifact_digest: String,
    pub initial_generation: u64,
    pub epoch_digest: String,
}
```

process restart 시 generation 숫자가 다시 시작될 수 있지만 process epoch digest가 달라야 한다.

## 14.3 ABA 방지

snapshot identity는 generation 숫자만으로 비교하지 않는다.

```text
process_epoch_digest
+
generation
+
snapshot_digest
```

를 사용한다.

---

# 15. Token Commit Barrier Preservation

## 15.1 Authority

W9C는 W9A Pre-Sampler Commit Gate의 권한을 변경하지 않는다.

```text
attention writer
→ logits
→ sampler preview
→ commit gate
→ real sampler
→ atomic token commit
```

## 15.2 Fault timing

### Before commit

```text
rollback allowed
demotion allowed
Headwise replay allowed
```

### After commit

```text
rollback forbidden
token rewrite forbidden
alternate writer replay forbidden
```

## 15.3 Commit receipt extension

```rust
pub struct AttentionDecodeW9CTokenCommitAuthorityExtension {
    pub authority_generation: u64,
    pub authority_snapshot_digest: String,
    pub production_writer: String,
    pub rollback_used: bool,
    pub demotion_barrier_observed: bool,
    pub commit_authority_digest: String,
}
```

---

# 16. Default Route Manager

## 16.1 Responsibilities

```text
artifact validation
authority holder initialization
promotion transaction
demotion transaction
session snapshot issuance
generation tracking
publication receipts
quarantine
```

## 16.2 Non-responsibilities

```text
attention math
sampler math
token ledger mutation
stream transport
KV tensor mutation
```

## 16.3 Suggested interface

```rust
pub trait AttentionDecodeW9CDefaultRouteManager {
    fn current_snapshot(&self) -> Arc<AttentionDecodeW9CAuthoritySnapshot>;

    fn prepare_promotion(
        &self,
        artifact: &AttentionDecodeW9CDefaultRouteArtifact,
    ) -> Result<AttentionDecodeW9CPromotionCandidate>;

    fn commit_promotion(
        &self,
        candidate: AttentionDecodeW9CPromotionCandidate,
    ) -> Result<AttentionDecodeW9CPromotionReceipt>;

    fn begin_demotion(
        &self,
        fault: AttentionDecodeW9CFault,
    ) -> Result<AttentionDecodeW9CDemotionBarrier>;

    fn complete_demotion(
        &self,
        barrier: AttentionDecodeW9CDemotionBarrier,
    ) -> Result<AttentionDecodeW9CDemotionReceipt>;
}
```

---

# 17. Audit Policy After Promotion

## 17.1 Audit remains sampled

Headwise oracle은 완전히 제거하지 않는다.

권장 post-promotion audit ratio:

```text
1 / 64 sessions
```

실제 값은 artifact에 봉인한다.

## 17.2 Audit comparison surface

```text
attention context compact digest
post-output-projection hidden compact digest
final logits compact parity
top-k identity
pure sampler preview token
```

## 17.3 Audit failure

```text
current step rollback
instant demotion
current artifact quarantine
new session TensorCube admission zero
```

audit failure 뒤 계속 TensorCube global default를 유지하면 FAIL이다.

---

# 18. No Dual Production Writer Seal

## 18.1 Runtime counters

```rust
pub struct AttentionDecodeW9CWriterExclusivityCounters {
    pub tensorcube_production_entries: u64,
    pub headwise_production_entries: u64,
    pub headwise_oracle_entries: u64,
    pub dual_production_observations: u64,
    pub sampler_invocations: u64,
    pub token_commits: u64,
    pub stream_emissions: u64,
}
```

## 18.2 Per-step invariant

TensorCube default success:

```text
tensorcube_production_entries = 1
headwise_production_entries   = 0
headwise_oracle_entries       = 0 or 1
sampler_invocations           = 1
token_commits                 = 1
stream_emissions              = 0 or 1
```

rollback success:

```text
tensorcube_production_attempt = 1
headwise_production_entries   = 1
headwise_oracle_entries       = 1
sampler_invocations           = 1
token_commits                 = 1
stream_emissions              = 0 or 1
```

여기서 Headwise는 rollback 승인 뒤 production writer가 된다.

같은 순간 두 production writer가 활성인 것은 아니다.

## 18.3 Temporal exclusivity

```text
TensorCube production lease release
before
Headwise rollback production lease acquire
```

lease overlap은 FAIL이다.

## 18.4 Writer lease

```rust
pub struct AttentionDecodeW9CWriterLease {
    pub invocation_id: String,
    pub authority_generation: u64,
    pub writer: AttentionDecodeProductionWriter,
    pub acquired: bool,
    pub released: bool,
    pub lease_digest: String,
}
```

---

# 19. Fault Injection Matrix

## Promotion transaction

```text
artifact validation failure
candidate snapshot digest failure
publication receipt write failure
pointer swap interruption
post-promotion probe failure
```

## Runtime authority

```text
generation drift
snapshot digest drift
dual writer lease overlap
stale session snapshot
route manager unavailable
```

## TensorCube path

```text
context guard mismatch
projection binding mismatch
non-finite logits
sampler preview mismatch
owner leak
```

## Demotion

```text
demotion-pending publication failure
Headwise route unavailable
current step replay failure
owner-zero timeout
demotion receipt durability failure
```

## Restart

```text
corrupted default artifact
stale parent W9B artifact
new driver identity
new device identity
feature digest drift
```

각 fault는 최소 세 번 반복한다.

---

# 20. Failure Codes

## Parent and artifact

```text
AttentionDecodeW9CParentW9BArtifactMissing
AttentionDecodeW9CParentW9BArtifactNotPass
AttentionDecodeW9CParentW9BDigestMismatch
AttentionDecodeW9CParentStabilitySealMismatch
AttentionDecodeW9CDefaultRouteArtifactMissing
AttentionDecodeW9CDefaultRouteArtifactDigestMismatch
AttentionDecodeW9CDefaultRouteArtifactRoleMismatch
AttentionDecodeW9CBuildRevisionMismatch
```

## Domain

```text
AttentionDecodeW9CAuthorityDomainMismatch
AttentionDecodeW9CModelDigestMismatch
AttentionDecodeW9CCheckpointDigestMismatch
AttentionDecodeW9CTokenizerDigestMismatch
AttentionDecodeW9CDeviceIdentityMismatch
AttentionDecodeW9CDriverIdentityMismatch
AttentionDecodeW9CRuntimeFeatureDigestMismatch
AttentionDecodeW9CLimitsDigestMismatch
```

## Promotion

```text
AttentionDecodeW9CPromotionPrepareFailed
AttentionDecodeW9CPromotionCandidateDigestMismatch
AttentionDecodeW9CPromotionPublicationFailed
AttentionDecodeW9CPromotionPostProbeFailed
AttentionDecodeW9CIllegalStateTransition
```

## Pointer and generation

```text
AttentionDecodeW9CAuthorityPointerUnavailable
AttentionDecodeW9CAuthorityGenerationNonMonotonic
AttentionDecodeW9CAuthoritySnapshotDigestMismatch
AttentionDecodeW9CAuthorityABADetected
AttentionDecodeW9CAuthorityReadTornState
```

## Writer exclusivity

```text
AttentionDecodeW9CDualProductionWriterDetected
AttentionDecodeW9CWriterLeaseOverlap
AttentionDecodeW9CHeadwiseProductionRouteUnexpected
AttentionDecodeW9CTensorCubeProductionRouteMissing
AttentionDecodeW9CWriterRoleMismatch
```

## Demotion

```text
AttentionDecodeW9CDemotionBarrierFailed
AttentionDecodeW9CDemotionPublicationFailed
AttentionDecodeW9CDemotionHeadwiseUnavailable
AttentionDecodeW9CDemotionReplayFailed
AttentionDecodeW9CDemotionOwnerLeak
AttentionDecodeW9CDemotionReceiptNotDurable
```

## Session

```text
AttentionDecodeW9CSessionAuthorityGenerationMismatch
AttentionDecodeW9CSessionArtifactDigestMismatch
AttentionDecodeW9CCrossSessionWriterMismatch
AttentionDecodeW9CStaleSessionAdmission
AttentionDecodeW9CExistingSessionPolicyViolation
```

## Token commit

```text
AttentionDecodeW9CSamplerDoubleInvocation
AttentionDecodeW9CTokenDoubleCommit
AttentionDecodeW9CEarlyStreamEmission
AttentionDecodeW9CPostCommitRollbackAttempt
AttentionDecodeW9CUnrecoverableTokenCommit
AttentionDecodeW9CSilentFallbackDetected
```

## Restart

```text
AttentionDecodeW9CStartupArtifactAdoptionFailed
AttentionDecodeW9CStartupDefaultWriterMismatch
AttentionDecodeW9CProcessReplayMismatch
AttentionDecodeW9CCorruptedArtifactAccepted
```

---

# 21. Implementation File Plan

## model_core

```text
crates/model_core/src/
  attention_decode_w9c.rs
  attention_decode_w9c_authority_snapshot.rs
  attention_decode_w9c_authority_holder.rs
  attention_decode_w9c_default_route_artifact.rs
  attention_decode_w9c_default_route_manager.rs
  attention_decode_w9c_promotion_transaction.rs
  attention_decode_w9c_demotion_barrier.rs
  attention_decode_w9c_writer_lease.rs
  attention_decode_w9c_session_authority.rs
  attention_decode_w9c_writer_exclusivity.rs
```

연결 대상:

```text
attention_decode_w9b.rs
attention_decode_w9b_promotion_controller.rs
attention_decode_w9b_route_snapshot.rs
attention_decode_w9b_stability_window.rs
attention_decode_w9a_pre_sampler_commit.rs
attention_decode_w9a_step_transaction.rs
decode_state.rs
native_wgpu.rs
generation_sampling.rs
kv_rollback01_forked_replay.rs
```

## burn_webgpu_backend

```text
crates/burn_webgpu_backend/src/
  attention_decode_w9c_authority_probe.rs
  attention_decode_w9c_writer_lease_probe.rs
  attention_decode_w9c_demotion_fault_injection.rs
```

새 attention kernel은 추가하지 않는다.

## orchestrator_local

```text
crates/orchestrator_local/src/
  attention_decode_w9c_cli_registry.rs
  attention_decode_w9c_artifact_wave_map.rs
  attention_decode_w9c_scenario_plan.rs
  attention_decode_w9c_fault_matrix.rs
  attention_decode_w9c_process_replay.rs

crates/orchestrator_local/src/bin/
  ash_attn_decode_w9c_verification_gate.rs
  ash_attn_decode_w9c_physical_gate.rs
```

## CLI

```text
specs/cli/
  ash_attn_decode_w9c_verification.args
  ash_attn_decode_w9c_physical.args
```

---

# 22. Registry and Cargo Contract

세 crate의 module registry에 W9C 모듈을 명시적으로 등록한다.

Cargo binary:

```toml
[[bin]]
name = "ash_attn_decode_w9c_verification_gate"
path = "src/bin/ash_attn_decode_w9c_verification_gate.rs"
required-features = ["orchestrator_tcu_audit_bins"]

[[bin]]
name = "ash_attn_decode_w9c_physical_gate"
path = "src/bin/ash_attn_decode_w9c_physical_gate.rs"
required-features = ["orchestrator_tcu_audit_bins"]
```

---

# 23. Verification Gate

## 23.1 Parent verification

```text
W9B artifact exists
W9B artifact PASS
W9B manifest digest exact
W9B stability seal exact
W9B build revision exact
```

## 23.2 Authority graph

```text
TensorCube promoted writer reachable
Headwise rollback-only oracle reachable
W9A commit gate reachable
stream emitter behind commit gate
global route manager single instance
authority holder single instance
```

## 23.3 State machine

```text
legal transitions accepted
illegal transitions denied
generation monotonic
ABA negative fixture denied
quarantine re-entry denied
```

## 23.4 Artifact

```text
canonical serialization
digest readback
unknown field denial
role mismatch denial
domain mismatch denial
corruption denial
```

## 23.5 Writer exclusivity

```text
TensorCube normal path has one production lease
Headwise normal path has zero production lease
rollback lease ordering exact
dual production lease fixture denied
double sampler fixture denied
double commit fixture denied
```

## 23.6 Session consistency

```text
new sessions observe new generation
old sessions remain pinned under declared policy
demotion blocks stale TensorCube admission
cross-thread replay deterministic
```

---

# 24. Physical Gate

## Phase A: Parent adoption

```text
read W9B physical artifact
verify W9B stability seal
reconstruct exact authority domain
```

## Phase B: Default artifact generation

Rust가 default-route artifact를 생성하고 readback 검증한다.

## Phase C: Promotion transaction

```text
HeadwiseSafeDefault
→ TensorCubePromotionPending
→ TensorCubeGlobalDefault
```

atomic pointer publication과 generation receipt를 검증한다.

## Phase D: Global default sessions

최소 다음 session corpus를 실행한다.

```text
short instruction
long subtitle-like input
repetition-heavy input
mixed punctuation
EOS-near input
high-entropy token stream
```

모든 신규 session에서 TensorCube가 default writer여야 한다.

## Phase E: Concurrency

```text
single thread
2 concurrent sessions
4 concurrent sessions
8 concurrent sessions
```

지원 가능한 범위까지 실행한다.

## Phase F: Audit oracle

sampled session에서 Headwise oracle을 실행하되 production writer exclusivity를 유지한다.

## Phase G: Instant demotion matrix

모든 demotion trigger class를 주입한다.

## Phase H: Process restart

세 process cycle에서 artifact adoption과 default writer consistency를 검증한다.

## Phase I: Corrupted artifact

다섯 corruption fixture가 모두 adoption denial을 일으켜야 한다.

---

# 25. Required Artifacts

```text
workspace/runtime/attention/decode/w9c/
  ash_attn_decode_w9c_verification_runtime_specification.json
  ash_attn_decode_w9c_verification_runtime_artifact.json
  ash_attn_decode_w9c_verification_local_manifest.json

  ash_attn_decode_w9c_physical_runtime_specification.json
  ash_attn_decode_w9c_physical_runtime_artifact.json
  ash_attn_decode_w9c_physical_local_manifest.json

  default_route_artifact.json
  default_route_artifact_manifest.json
  authority_domain.json
  authority_publication_receipt.json
  authority_generation_history.json
  session_authority_receipts.json
  writer_exclusivity_receipts.json
  audit_oracle_receipts.json
  demotion_barrier_receipts.json
  demotion_completion_receipts.json
  process_replay_receipts.json
  corrupted_artifact_matrix.json
  final_global_default_seal.json
```

모든 runtime artifact는 Rust가 생성한다.

코드 ZIP에는 포함하지 않는다.

---

# 26. CLI Contract

필수 키:

```text
--patch-id
--expected-build-revision

--parent-w9b-artifact
--parent-w9b-manifest
--parent-w9b-stability-seal

--model-instance-digest
--checkpoint-digest
--tokenizer-digest

--device-allowlist-entry
--driver-identity
--runtime-feature-digest
--limits-digest

--layer-qualification-artifact
--geometry-qualification-artifact
--latency-budget-artifact
--vram-budget-artifact
--rollback-matrix-artifact

--initial-authority-generation
--existing-session-policy
--post-promotion-probe-count
--concurrent-session-count
--process-replay-count
--audit-numerator
--audit-denominator

--require-atomic-authority-pointer
--require-generation-monotonicity
--require-cross-session-consistency
--require-headwise-rollback-oracle
--require-instant-demotion
--require-no-dual-production-writer
--require-single-sampler-invocation
--require-atomic-token-commit

--deny-global-headwise-production-route
--deny-silent-fallback
--deny-full-context-readback
--deny-full-logits-readback
--deny-post-commit-rollback
--deny-unrecoverable-token-commit

--out-runtime-specification
--out-runtime-artifact
--out-local-manifest
--out-w9c-directory
```

unknown key와 duplicate key는 FAIL한다.

---

# 27. PASS Criteria

## Parent

```text
W9B physical artifact PASS                     true
W9B stability seal PASS                        true
W9B manifest digest exact                      true
```

## Artifact

```text
default route artifact generated by Rust       true
artifact readback digest exact                 true
authority domain exact                         true
promoted writer = TensorCube                   true
rollback oracle = Headwise                     true
```

## Atomic pointer

```text
pointer publication atomic                     true
generation strictly monotonic                  true
torn state observations                        0
ABA observations                               0
```

## Global default

```text
new session TensorCube default observations    all
unexpected Headwise normal production entries  0
TensorCube production route missing            0
```

## Oracle

```text
Headwise normal-path execution                  0 except audit
Headwise rollback reachability                  true
Headwise audit reachability                     true
oracle temporary owner leak                     0
```

## Demotion

```text
all required demotion drills executed           true
commit blocked before replay                    true
new TensorCube admission blocked                true
Headwise default publication observed           true
faulted step recovered or safely terminated     true
demotion owner leak                             0
```

## Session consistency

```text
cross-session generation mismatch               0
cross-session artifact mismatch                 0
stale TensorCube session admission              0
cross-thread replay mismatch                    0
```

## Writer exclusivity

```text
dual production writer observations             0
writer lease overlap                            0
sampler double invocation                       0
token double commit                             0
early stream emission                           0
```

## Restart

```text
three process replay cycles PASS                true
corrupted artifact accepted                     0
startup writer mismatch                         0
```

## Readback and fallback

```text
full context readback                           0
full logits readback                            0
silent fallback                                 0
post-commit rollback                            0
unrecoverable token commit                      0
```

---

# 28. Proposed Verification PASS Token

```text
PASS_ASH_ATTN_DECODE_W9C_DEFAULT_ROUTE_ARTIFACT_ATOMIC_AUTHORITY_POINTER_GENERATION_STATE_MACHINE_HEADWISE_ROLLBACK_ONLY_ORACLE_INSTANT_DEMOTION_CROSS_SESSION_CONSISTENCY_NO_DUAL_PRODUCTION_WRITER_STATIC_VERIFICATION_SEALED
```

---

# 29. Proposed Physical PASS Token

```text
PASS_ASH_ATTN_DECODE_W9C_TENSORCUBE_GLOBAL_DEFAULT_WRITER_PROMOTION_ATOMIC_AUTHORITY_POINTER_SWITCH_HEADWISE_ROLLBACK_ONLY_ORACLE_DEFAULT_ROUTE_ARTIFACT_ADOPTION_INSTANT_DEMOTION_CROSS_SESSION_AUTHORITY_CONSISTENCY_PROCESS_RESTART_REPLAY_WRITER_LEASE_EXCLUSIVITY_SINGLE_SAMPLER_ATOMIC_TOKEN_COMMIT_NO_DUAL_PRODUCTION_WRITER_NO_FULL_CONTEXT_READBACK_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_POST_COMMIT_ROLLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

---

# 30. Completion State

W9C PASS 후:

```text
TensorCube
  GlobalDefaultWriter
  AuthorityArtifactBound
  AtomicPointerPublished
  CrossSessionConsistent
  InstantDemotionBound

Headwise
  RollbackOnlyOracle
  SampledAuditOracle
  SafeDemotedDefault

Default Route Manager
  ProcessGlobalAuthorityOwner
  GenerationMonotonic
  ArtifactAdoptionAuthoritative

Token Commit
  W9A PreSamplerGateAuthoritative
  SingleSamplerInvocation
  AtomicTokenCommit

Production Writer
  ExactlyOnePerInvocation
```

---

# 31. 다음 패치

```text
ASH-ATTN-DECODE-W9D

Post-Promotion Sustained Fleet Soak /
Remote Artifact Rollout /
Authority Revocation /
Driver Update Requalification /
Device-Loss Recovery Re-Adoption /
Fleet-Wide Instant Demotion /
No Stale Global Authority Seal
```

W9D 진입 조건:

```text
W9C TensorCubeGlobalDefaultWriter PASS
W9C atomic pointer PASS
W9C cross-session consistency PASS
W9C instant demotion PASS
W9C no dual production writer PASS
W9C process restart replay PASS
```

이 조건이 하나라도 빠지면 W9D를 시작하지 않는다.
