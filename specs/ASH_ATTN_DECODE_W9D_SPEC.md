# ASH-ATTN-DECODE-W9D

## Post-Promotion Sustained Fleet Soak /
## Remote Artifact Rollout /
## Authority Revocation /
## Driver Update Requalification /
## Device-Loss Recovery Re-Adoption /
## Fleet-Wide Instant Demotion /
## No Stale Global Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-DECODE-W9D`  
> Proposed build revision: `W9D-w9c-fleet-authority-rollout-revocation-r1`  
> Parent: `ASH-ATTN-DECODE-W9C-R1D`  
> Parent state: `PHYSICAL PASS`  
> Parent default writer: `TensorCube`  
> Parent rollback-only oracle: `HeadwiseFullActive`  
> Parent authority owner: `W9C Default Route Manager`  
> W9D target scope: multi-installation fleet authority lifecycle  
> W9D rollout mode: signed artifact wave adoption  
> W9D revocation mode: generation-bound fleet revocation  
> W9D stale authority tolerance: zero  
> W9D global default writer after PASS: `TensorCube` within active fleet authority epoch  
> Headwise after PASS: rollback-only oracle and fleet-safe demoted default  
> Next authority patch: `ASH-ATTN-DECODE-W9E`

---

# 0. 상태 구분

## 확정

사용자 로컬 물리 실행에서 다음 W9C PASS 토큰이 관측됐다.

```text
PASS_ASH_ATTN_DECODE_W9C_TENSORCUBE_GLOBAL_DEFAULT_WRITER_PROMOTION_ATOMIC_AUTHORITY_POINTER_SWITCH_HEADWISE_ROLLBACK_ONLY_ORACLE_DEFAULT_ROUTE_ARTIFACT_ADOPTION_INSTANT_DEMOTION_CROSS_SESSION_AUTHORITY_CONSISTENCY_PROCESS_RESTART_REPLAY_WRITER_LEASE_EXCLUSIVITY_SINGLE_SAMPLER_ATOMIC_TOKEN_COMMIT_NO_DUAL_PRODUCTION_WRITER_NO_FULL_CONTEXT_READBACK_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_POST_COMMIT_ROLLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

따라서 W9D는 다음을 부모 물리 권위로 채택한다.

```text
TensorCube global default writer
atomic authority pointer switch
Headwise rollback-only oracle
default route artifact adoption
instant demotion
cross-session authority consistency
process restart replay
writer lease exclusivity
single sampler invocation
atomic token commit
no dual production writer
no full context readback
no full logits readback
no silent fallback
no post-commit rollback
no unrecoverable token commit
```

## 제안

이 문서의 fleet epoch, rollout wave, revocation journal, remote artifact transport, driver requalification, device-loss re-adoption, fleet demotion, stale authority exclusion 구조는 W9D 구현 계약 제안이다.

## 판단 불가

현재 대화 로그만으로 다음은 확정할 수 없다.

```text
실제 설치본 수
실제 원격 배포 서버 구성
실제 서명 키 보관 방식
실제 driver update 빈도
실제 device-loss 재발 빈도
실제 fleet latency·VRAM 분포
실제 원격 revocation 전달 지연
```

W9D physical gate와 fleet simulation gate가 위 항목을 판정한다.

---

# 1. 목적

W9C는 단일 process authority domain 안에서 TensorCube를 global default writer로 승격했다.

W9D의 목적은 이 권위를 여러 설치본과 여러 runtime epoch에 안전하게 배포하고, 필요할 때 빠르게 회수하며, device·driver 변화 후 다시 검증된 경우에만 재채택하는 것이다.

W9D가 답해야 하는 질문:

```text
1. W9C authority artifact를 여러 설치본에 단계적으로 배포할 수 있는가?
2. rollout 중 일부 설치본만 새 epoch를 채택해도 authority가 혼재되지 않는가?
3. revocation이 발생하면 모든 active installation이 stale TensorCube authority를 버리는가?
4. driver update 뒤 기존 qualification을 자동 재사용하지 않는가?
5. device loss 뒤 recovery된 device가 이전 authority를 무조건 재채택하지 않는가?
6. fleet-wide demotion이 신규 token commit보다 먼저 전파되는가?
7. offline·delayed·restarted installation이 stale global authority를 재생하지 않는가?
```

W9D PASS 후 다음 문장이 사실이어야 한다.

```text
W9C에서 승격된 TensorCube global default authority가
signed rollout wave와 exact fleet epoch를 통해 설치본 집합에 배포됐다.

각 installation은 동일한 authority lineage와 revocation state를 검증한 뒤에만
TensorCube global default를 채택했다.

driver update, device loss, artifact revocation, fleet demotion이 발생하면
기존 authority는 즉시 무효화되며,
stale TensorCube global authority로 신규 decode-step을 시작할 수 없었다.
```

---

# 2. 핵심 비목표

W9D는 다음을 수행하지 않는다.

```text
TensorCube attention 수식 변경
Headwise 구현 삭제
sampler 수식 변경
LM-head 수식 변경
remote server를 token 생성 경로에 직접 삽입
remote control plane 없이는 실행 불가하게 만들기
unsigned artifact 허용
revoked artifact 재활성화
driver family 이름만으로 재승인
device family 이름만으로 재승인
offline 설치본의 영구 stale authority 허용
token commit 이후 rollback
full context readback
full logits readback
fleet-wide dual production writer
```

다음은 W9E 이후 범위다.

```text
multi-model fleet authority
heterogeneous TensorCube profile routing
remote telemetry compaction
federated artifact transparency
fleet-wide signed release channels
automatic staged recovery orchestration
```

---

# 3. W9D Authority Hierarchy

```text
W9C Default Route Artifact
  ↓
W9D Fleet Authority Artifact
  ↓
W9D Rollout Wave Artifact
  ↓
Installation Adoption Receipt
  ↓
Session Authority Snapshot
  ↓
Decode-Step Writer Lease
```

revocation hierarchy:

```text
Fleet Revocation Artifact
  ↓
Installation Revocation Receipt
  ↓
Local Demotion Barrier
  ↓
Headwise Safe Default
```

하위 authority는 모든 상위 digest를 정확히 바인딩해야 한다.

---

# 4. Fleet Terminology

## 4.1 Fleet

W9D에서 fleet은 다음 설치본 집합이다.

```text
같은 ASH runtime product lineage
같은 W9D patch contract
같은 model family
같은 authority server namespace
각자 독립 process·device·driver identity 보유
```

단일 PC에서 여러 독립 runtime directory를 실행하는 simulation도 fleet로 간주할 수 있다.

## 4.2 Installation

```rust
pub struct AttentionDecodeW9DInstallationIdentity {
    pub installation_id: String,
    pub installation_epoch: u64,
    pub machine_identity_digest: String,
    pub runtime_build_digest: String,
    pub model_instance_digest: String,
    pub checkpoint_digest: String,
    pub tokenizer_digest: String,
    pub device_identity_digest: String,
    pub driver_identity_digest: String,
    pub feature_digest: String,
    pub limits_digest: String,
    pub identity_digest: String,
}
```

## 4.3 Fleet epoch

```rust
pub struct AttentionDecodeW9DFleetEpoch {
    pub fleet_id: String,
    pub authority_epoch: u64,
    pub rollout_epoch: u64,
    pub revocation_epoch: u64,
    pub parent_w9c_artifact_digest: String,
    pub fleet_policy_digest: String,
    pub epoch_digest: String,
}
```

## 4.4 Rollout wave

```text
Wave0
  verification-only shadow installations

Wave1
  1 installation or 1%

Wave2
  5%

Wave3
  25%

Wave4
  50%

Wave5
  100%
```

실제 ratio는 policy artifact에 봉인한다.

---

# 5. Fleet Authority State Machine

```rust
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum AttentionDecodeW9DFleetAuthorityState {
    Unenrolled,
    EnrolledHeadwiseSafe,
    RolloutCandidate,
    TensorCubeFleetActive,
    RevocationPending,
    HeadwiseFleetDemoted,
    RequalificationPending,
    RecoveryReadoptionPending,
    Quarantined,
}
```

## 5.1 허용 전이

```text
Unenrolled
→ EnrolledHeadwiseSafe

EnrolledHeadwiseSafe
→ RolloutCandidate
→ TensorCubeFleetActive

TensorCubeFleetActive
→ RevocationPending
→ HeadwiseFleetDemoted

HeadwiseFleetDemoted
→ RequalificationPending
→ RolloutCandidate

HeadwiseFleetDemoted
→ RecoveryReadoptionPending
→ RolloutCandidate
```

## 5.2 금지 전이

```text
Unenrolled → TensorCubeFleetActive
RevocationPending → TensorCubeFleetActive
Quarantined → TensorCubeFleetActive
RequalificationPending → TensorCubeFleetActive
RecoveryReadoptionPending → TensorCubeFleetActive
```

---

# 6. Fleet Authority Artifact

## 6.1 Schema

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AttentionDecodeW9DFleetAuthorityArtifact {
    pub patch_id: String,
    pub build_revision: String,

    pub fleet_id: String,
    pub authority_epoch: u64,
    pub rollout_epoch: u64,
    pub revocation_epoch: u64,

    pub parent_w9c_artifact_digest: String,
    pub parent_w9c_manifest_digest: String,
    pub parent_w9c_global_default_seal_digest: String,

    pub model_family_digest: String,
    pub checkpoint_allowlist_digest: String,
    pub tokenizer_allowlist_digest: String,

    pub device_allowlist_digest: String,
    pub driver_allowlist_digest: String,
    pub runtime_feature_allowlist_digest: String,
    pub limits_allowlist_digest: String,

    pub rollout_policy_digest: String,
    pub soak_policy_digest: String,
    pub demotion_policy_digest: String,
    pub revocation_policy_digest: String,
    pub requalification_policy_digest: String,

    pub promoted_writer: String,
    pub rollback_oracle: String,

    pub issued_at_unix_ms: u64,
    pub not_before_unix_ms: u64,
    pub expires_at_unix_ms: u64,

    pub issuer_key_id: String,
    pub payload_digest: String,
    pub signature_algorithm: String,
    pub signature: String,
    pub artifact_digest: String,
}
```

## 6.2 Required roles

```text
promoted_writer
  TensorCube

rollback_oracle
  HeadwiseFullActive
```

## 6.3 Signature

권장:

```text
Ed25519
```

허용 조건:

```text
deterministic verification
canonical payload
key id explicit
public key allowlist explicit
signature verified before adoption
```

## 6.4 Key rotation

key rotation artifact는 다음을 포함한다.

```text
old key id
new key id
activation epoch
revocation epoch
rotation signature
```

old key가 revoke된 뒤 old key artifact는 adoption 불가다.

---

# 7. Remote Artifact Rollout

## 7.1 Remote의 의미

remote artifact는 네트워크를 통해 수신되는 fleet authority artifact다.

W9D는 특정 HTTP stack을 authority로 두지 않는다.

허용 transport 예:

```text
HTTPS
signed object storage
local mirror
air-gapped removable media
```

authority는 transport가 아니라 signature·digest·epoch 검증에 있다.

## 7.2 Fetch sequence

```text
fetch metadata
→ size limit check
→ temporary file write
→ SHA-256
→ signature verification
→ canonical parse
→ epoch verification
→ revocation verification
→ installation compatibility verification
→ atomic cache publish
→ adoption candidate
```

## 7.3 Anti-rollback

설치본은 다음보다 낮은 epoch를 채택할 수 없다.

```text
max_seen_authority_epoch
max_seen_rollout_epoch
max_seen_revocation_epoch
```

## 7.4 Cache

```text
active/
candidate/
revoked/
quarantine/
```

cache 이동은 atomic rename으로 수행한다.

## 7.5 Rollout wave admission

```rust
pub struct AttentionDecodeW9DRolloutWaveArtifact {
    pub fleet_id: String,
    pub authority_epoch: u64,
    pub wave_id: String,
    pub wave_index: u32,
    pub numerator: u32,
    pub denominator: u32,
    pub previous_wave_receipt_digest: String,
    pub required_soak_window_count: u32,
    pub required_installation_count: u32,
    pub required_token_count: u64,
    pub artifact_digest: String,
}
```

---

# 8. Deterministic Installation Selection

```text
selection_key = SHA-256(
    fleet_id
 || authority_epoch
 || rollout_epoch
 || wave_id
 || installation_id
 || installation_identity_digest
)
```

```text
selected = first_u64(selection_key) % denominator < numerator
```

금지 입력:

```text
wall-clock
process id
random entropy
thread order
memory address
GPU timestamp
```

---

# 9. Post-Promotion Sustained Fleet Soak

## 9.1 목적

W9C의 local process PASS만으로는 다음을 증명할 수 없다.

```text
installation 간 authority drift
fleet rollout 중 epoch 혼재
장시간 driver thermal drift
장기 VRAM 누적
revocation 전달 지연
restart 뒤 stale cache 재채택
device-loss 반복 후 authority corruption
```

## 9.2 Soak dimensions

```text
installation count
session count
token count
wall-clock duration
process restart count
device-loss injection count
driver identity variants
rollout wave
```

## 9.3 Required windows

각 wave는 최소 세 개의 연속 fleet PASS window가 필요하다.

```text
PASS
PASS
PASS
```

## 9.4 Fleet stability window

```rust
pub struct AttentionDecodeW9DFleetStabilityWindow {
    pub fleet_id: String,
    pub authority_epoch: u64,
    pub rollout_epoch: u64,
    pub wave_id: String,
    pub window_index: u32,

    pub active_installation_count: u64,
    pub tensorcube_installation_count: u64,
    pub headwise_installation_count: u64,

    pub session_count: u64,
    pub committed_token_count: u64,
    pub rollback_count: u64,
    pub demotion_count: u64,
    pub requalification_count: u64,
    pub device_loss_count: u64,

    pub p95_latency_ns: u64,
    pub p99_latency_ns: u64,
    pub peak_vram_bytes: u64,
    pub post_drain_residual_bytes: u64,

    pub stale_authority_observations: u64,
    pub dual_writer_observations: u64,
    pub unrecoverable_commit_count: u64,

    pub pass: bool,
    pub digest: String,
}
```

## 9.5 Soak pass

```text
stale authority observations = 0
dual writer observations = 0
unrecoverable commits = 0
latency budget PASS
VRAM budget PASS
owner-zero PASS
revocation replay PASS
restart replay PASS
```

---

# 10. Authority Revocation

## 10.1 Revocation artifact

```rust
pub struct AttentionDecodeW9DRevocationArtifact {
    pub fleet_id: String,
    pub revocation_epoch: u64,
    pub revoked_authority_epoch: u64,
    pub revoked_artifact_digests: Vec<String>,
    pub revoked_driver_digests: Vec<String>,
    pub revoked_device_digests: Vec<String>,
    pub reason_code: String,
    pub effective_at_unix_ms: u64,
    pub issuer_key_id: String,
    pub payload_digest: String,
    pub signature: String,
    pub artifact_digest: String,
}
```

## 10.2 Revocation precedence

```text
revocation artifact
>
cached fleet authority artifact
>
local W9C default route artifact
```

## 10.3 Local action

revocation 관측 즉시:

```text
new TensorCube step admission blocked
pre-sampler commit barrier armed
local W9C instant demotion invoked
Headwise safe default published
active artifact moved to revoked cache
revocation receipt committed
```

## 10.4 Offline installation

offline installation은 마지막 trusted revocation state를 사용한다.

authority artifact가 만료됐거나 revocation freshness budget을 초과하면:

```text
TensorCube global default denied
Headwise safe default
```

## 10.5 Revocation freshness budget

```rust
pub struct AttentionDecodeW9DRevocationFreshnessPolicy {
    pub maximum_offline_age_ms: u64,
    pub maximum_revocation_check_age_ms: u64,
    pub fail_closed: bool,
    pub digest: String,
}
```

W9D는 `fail_closed=true`를 요구한다.

---

# 11. Driver Update Requalification

## 11.1 Driver identity drift

다음 중 하나가 바뀌면 기존 driver qualification은 무효다.

```text
driver name
driver version
driver info
shader compiler identity
runtime backend version
enabled feature digest
limits digest
subgroup behavior
```

## 11.2 Update detection

startup과 device recreation 시 driver identity를 재계산한다.

## 11.3 Requalification state

```text
driver drift observed
→ TensorCube authority suspended
→ Headwise safe default
→ W9B qualification subset replay
→ W9C authority adoption replay
→ W9D fleet re-enrollment
```

## 11.4 Required requalification matrix

```text
subgroup probe
shader-int64 probe
timestamp query probe
full-layer qualification sample
long-session token soak sample
latency budget sample
VRAM plateau sample
rollback drill sample
authority pointer probe
```

## 11.5 Driver range authority

driver range allowlist는 exact lower/upper bound와 proof digest가 필요하다.

새 driver가 range 안에 있어도 shader compiler identity가 달라지면 재qualification한다.

---

# 12. Device-Loss Recovery Re-Adoption

## 12.1 원칙

device loss 뒤 새 device handle은 이전 authority snapshot을 자동 상속하지 않는다.

## 12.2 Recovery sequence

```text
device loss observed
→ TensorCube admission block
→ active step commit block
→ Headwise safe termination or replay
→ old device resources retire
→ new adapter/device creation
→ device identity recompute
→ driver identity recompute
→ runtime feature recompute
→ limits recompute
→ W9B recovery qualification
→ W9C artifact re-adoption
→ W9D fleet epoch revalidation
→ TensorCube re-adoption candidate
```

## 12.3 Re-adoption receipt

```rust
pub struct AttentionDecodeW9DRecoveryReadoptionReceipt {
    pub installation_id: String,
    pub device_loss_epoch: u64,
    pub old_device_identity_digest: String,
    pub new_device_identity_digest: String,
    pub old_authority_generation: u64,
    pub new_authority_generation: u64,
    pub w9b_requalification_digest: String,
    pub w9c_readoption_digest: String,
    pub w9d_fleet_epoch_digest: String,
    pub tensorcube_readopted: bool,
    pub receipt_digest: String,
}
```

## 12.4 Same-device recovery

같은 adapter name이어도 identity digest가 재계산돼야 한다.

## 12.5 Three-cycle loss replay

최소 세 번:

```text
TensorCube active
→ device loss
→ Headwise safe mode
→ device recreation
→ requalification
→ TensorCube re-adoption
```

---

# 13. Fleet-Wide Instant Demotion

## 13.1 목표

fleet demotion trigger가 발생하면 모든 active installation에서 신규 TensorCube token commit을 차단한다.

## 13.2 Trigger

```text
revocation artifact
critical audit failure
driver regression
device family regression
dual writer observation
unrecoverable token commit
stale authority observation
signature compromise
rollout wave failure
```

## 13.3 Demotion broadcast

transport는 best effort일 수 있지만 authority semantics는 fail-closed다.

각 installation은 다음 중 하나를 관측해야 한다.

```text
signed demotion artifact
revocation epoch increase
authority artifact expiry
freshness budget breach
```

## 13.4 Local demotion barrier

W9C demotion barrier를 재사용한다.

```text
fleet fault
→ local fault mapping
→ W9C instant demotion
→ Headwise safe default
```

## 13.5 Fleet completion

```rust
pub struct AttentionDecodeW9DFleetDemotionSummary {
    pub fleet_id: String,
    pub revocation_epoch: u64,
    pub targeted_installation_count: u64,
    pub acknowledged_installation_count: u64,
    pub demoted_installation_count: u64,
    pub stale_installation_count: u64,
    pub failed_installation_count: u64,
    pub completion_digest: String,
}
```

PASS 조건:

```text
stale_installation_count = 0
failed_installation_count = 0
```

simulation에서는 모든 installation을 제어할 수 있어야 한다.

---

# 14. No Stale Global Authority

## 14.1 Stale 정의

다음 중 하나라도 해당하면 stale authority다.

```text
authority epoch lower than max seen
rollout epoch lower than max seen
revocation epoch lower than max seen
artifact expired
artifact revoked
driver identity changed
device identity changed
runtime build changed
parent W9C artifact changed
signature key revoked
```

## 14.2 Startup denial

stale artifact만 존재하면:

```text
HeadwiseSafeDefault
```

## 14.3 Runtime denial

active TensorCube authority가 stale로 판정되면:

```text
next step admission blocked
current step pre-commit rollback
local demotion
artifact quarantine
```

## 14.4 Monotonic journal

```rust
pub struct AttentionDecodeW9DAuthorityJournal {
    pub max_seen_authority_epoch: u64,
    pub max_seen_rollout_epoch: u64,
    pub max_seen_revocation_epoch: u64,
    pub active_artifact_digest: String,
    pub revoked_artifact_digests: Vec<String>,
    pub journal_generation: u64,
    pub journal_digest: String,
}
```

journal은 atomic write + readback verify를 사용한다.

---

# 15. Rollout Controller

## 15.1 Input

```rust
pub struct AttentionDecodeW9DRolloutControllerInput {
    pub fleet_authority_artifact_digest: String,
    pub rollout_wave_artifact_digest: String,
    pub previous_wave_summary_digest: String,
    pub fleet_stability_window_digests: Vec<String>,
    pub revocation_journal_digest: String,
    pub operator_policy_digest: String,
}
```

## 15.2 Decision

```rust
pub enum AttentionDecodeW9DRolloutDecision {
    AdvanceOneWave,
    HoldWave,
    DemoteFleet,
    QuarantineArtifact,
}
```

## 15.3 One-wave rule

한 번에 한 wave만 승격한다.

## 15.4 Hold conditions

```text
insufficient installation count
insufficient token count
latency budget breach
VRAM budget breach
restart replay mismatch
device-loss replay mismatch
revocation drill incomplete
```

---

# 16. Remote Artifact Cache SSOT

```text
workspace/runtime/attention/decode/w9d/cache/
  active/
  candidate/
  revoked/
  quarantine/
  journal.json
```

## 16.1 Active cache

exactly one active fleet artifact per fleet id.

## 16.2 Candidate cache

signature verified but not yet adopted.

## 16.3 Revoked cache

재채택 금지.

## 16.4 Quarantine cache

parse 가능하지만 policy 위반 또는 proof mismatch.

---

# 17. Installation Adoption Transaction

```text
candidate artifact read
→ signature verify
→ epoch anti-rollback
→ revocation journal check
→ installation compatibility
→ parent W9C availability
→ local W9C adoption probe
→ Headwise oracle reachability
→ atomic active cache publish
→ installation adoption receipt
```

adoption receipt 실패 시 TensorCube authority를 publish하지 않는다.

---

# 18. Cross-Installation Consistency

## 18.1 Required equality

같은 wave의 installation은 다음을 공유한다.

```text
fleet id
authority epoch
rollout epoch
revocation epoch
fleet artifact digest
rollout wave digest
promoted writer
rollback oracle
```

## 18.2 Allowed differences

```text
installation id
machine identity
device identity
driver identity
local authority generation
process epoch
```

## 18.3 Consistency receipt

```rust
pub struct AttentionDecodeW9DCrossInstallationConsistencyReceipt {
    pub fleet_id: String,
    pub wave_id: String,
    pub installation_receipt_digests: Vec<String>,
    pub authority_epoch_set: Vec<u64>,
    pub rollout_epoch_set: Vec<u64>,
    pub revocation_epoch_set: Vec<u64>,
    pub stale_authority_count: u64,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 19. Fleet Audit

## 19.1 Audit sampling

```text
installation audit ratio
session audit ratio
token audit ratio
```

각 축은 독립적이다.

## 19.2 Audit surfaces

```text
authority epoch
artifact digest
writer lease
compact attention digest
compact logits parity
top-k identity
sampler preview
token commit count
```

## 19.3 Audit failure

```text
local demotion
installation quarantine
wave HOLD
fleet demotion evaluation
```

---

# 20. Network and Clock Independence

## 20.1 Network

network failure는 authority corruption이 아니다.

하지만 freshness budget을 초과하면 TensorCube authority를 유지할 수 없다.

## 20.2 Clock

artifact expiry는 monotonic secure time source 또는 signed server time receipt를 사용한다.

wall-clock rollback이 감지되면 fail-closed한다.

## 20.3 Offline simulation

네트워크 없이도 local directory transport로 rollout·revocation을 재현할 수 있어야 한다.

---

# 21. Failure Codes

## Artifact

```text
AttentionDecodeW9DFleetArtifactMissing
AttentionDecodeW9DFleetArtifactSignatureInvalid
AttentionDecodeW9DFleetArtifactDigestMismatch
AttentionDecodeW9DFleetArtifactExpired
AttentionDecodeW9DFleetArtifactNotYetValid
AttentionDecodeW9DFleetArtifactIssuerKeyRejected
```

## Epoch

```text
AttentionDecodeW9DAuthorityEpochRollback
AttentionDecodeW9DRolloutEpochRollback
AttentionDecodeW9DRevocationEpochRollback
AttentionDecodeW9DAuthorityJournalMismatch
```

## Rollout

```text
AttentionDecodeW9DRolloutWaveParentMissing
AttentionDecodeW9DRolloutWaveTierSkip
AttentionDecodeW9DRolloutWaveSoakIncomplete
AttentionDecodeW9DRolloutWaveBudgetBreach
AttentionDecodeW9DRolloutWaveConsistencyMismatch
```

## Revocation

```text
AttentionDecodeW9DRevocationArtifactInvalid
AttentionDecodeW9DRevocationNotApplied
AttentionDecodeW9DRevokedArtifactReadopted
AttentionDecodeW9DRevocationFreshnessExceeded
```

## Driver

```text
AttentionDecodeW9DDriverIdentityDrift
AttentionDecodeW9DDriverRequalificationIncomplete
AttentionDecodeW9DShaderCompilerIdentityMismatch
```

## Device loss

```text
AttentionDecodeW9DDeviceLossAuthorityReuseDetected
AttentionDecodeW9DRecoveryRequalificationIncomplete
AttentionDecodeW9DRecoveryReadoptionDenied
AttentionDecodeW9DRecoveryOwnerLeak
```

## Fleet demotion

```text
AttentionDecodeW9DFleetDemotionNotAcknowledged
AttentionDecodeW9DFleetDemotionIncomplete
AttentionDecodeW9DStaleInstallationDetected
AttentionDecodeW9DFleetDemotionCommitLeak
```

## Stale authority

```text
AttentionDecodeW9DStaleGlobalAuthorityDetected
AttentionDecodeW9DExpiredAuthorityAccepted
AttentionDecodeW9DRevokedAuthorityAccepted
AttentionDecodeW9DOldEpochAccepted
```

---

# 22. Implementation File Plan

## model_core

```text
crates/model_core/src/
  attention_decode_w9d.rs
  attention_decode_w9d_fleet_authority.rs
  attention_decode_w9d_rollout_controller.rs
  attention_decode_w9d_revocation.rs
  attention_decode_w9d_authority_journal.rs
  attention_decode_w9d_installation_identity.rs
  attention_decode_w9d_driver_requalification.rs
  attention_decode_w9d_device_loss_readoption.rs
  attention_decode_w9d_fleet_demotion.rs
  attention_decode_w9d_stale_authority.rs
```

연결 대상:

```text
attention_decode_w9c.rs
attention_decode_w9c_default_route_manager.rs
attention_decode_w9c_demotion_barrier.rs
attention_decode_w9c_authority_holder.rs
attention_decode_w9b_device_allowlist.rs
attention_decode_w9b_stability_window.rs
decode_state.rs
native_wgpu.rs
```

## burn_webgpu_backend

```text
crates/burn_webgpu_backend/src/
  attention_decode_w9d_device_identity_probe.rs
  attention_decode_w9d_driver_identity_probe.rs
  attention_decode_w9d_device_loss_probe.rs
  attention_decode_w9d_fleet_telemetry_probe.rs
```

## orchestrator_local

```text
crates/orchestrator_local/src/
  attention_decode_w9d_cli_registry.rs
  attention_decode_w9d_artifact_wave_map.rs
  attention_decode_w9d_scenario_plan.rs
  attention_decode_w9d_fleet_simulator.rs
  attention_decode_w9d_rollout_wave_plan.rs
  attention_decode_w9d_revocation_plan.rs
  attention_decode_w9d_driver_matrix.rs
  attention_decode_w9d_device_loss_matrix.rs

crates/orchestrator_local/src/bin/
  ash_attn_decode_w9d_verification_gate.rs
  ash_attn_decode_w9d_physical_gate.rs
```

## CLI

```text
specs/cli/
  ash_attn_decode_w9d_verification.args
  ash_attn_decode_w9d_physical.args
```

---

# 23. Verification Gate

## 23.1 Parent

```text
W9C artifact PASS
W9C manifest digest exact
W9C global default seal exact
W9C build revision exact
```

## 23.2 Signature

```text
canonical payload
signature verify
key allowlist
revoked key denial
corrupted signature denial
```

## 23.3 Epoch

```text
authority monotonic
rollout monotonic
revocation monotonic
journal generation monotonic
```

## 23.4 State machine

```text
legal transitions accepted
illegal transitions denied
revoked artifact readoption denied
quarantine reentry denied
```

## 23.5 Rollout

```text
wave skip denied
three-window requirement enforced
deterministic installation selection
cross-installation consistency
```

## 23.6 Driver

```text
driver drift detected
old qualification invalidated
requalification required
```

## 23.7 Device loss

```text
old authority reuse denied
new identity required
re-adoption requires proof
```

---

# 24. Physical Gate

## Phase A: Fleet simulation bootstrap

최소 4개의 독립 installation runtime root를 구성한다.

```text
installation-00
installation-01
installation-02
installation-03
```

각 installation은 독립 cache·journal·process epoch를 가진다.

## Phase B: W9C parent adoption

각 installation에서 W9C global default를 독립적으로 채택한다.

## Phase C: Remote rollout

```text
Wave0
Wave1
Wave2
Wave3
Wave4
Wave5
```

지원 범위 내에서 순차 실행한다.

## Phase D: Sustained soak

각 wave에서 최소 세 stability window를 실행한다.

## Phase E: Revocation

active fleet artifact를 revoke한다.

모든 installation이 Headwise로 demotion해야 한다.

## Phase F: Stale restart

revoked artifact만 가진 installation을 restart한다.

TensorCube adoption이 거부돼야 한다.

## Phase G: Driver update

한 installation의 driver identity fixture를 변경한다.

재qualification 전 TensorCube adoption이 거부돼야 한다.

## Phase H: Device loss

한 installation에서 device-loss recovery를 세 번 반복한다.

## Phase I: Fleet-wide demotion

critical fault artifact를 배포하고 모든 installation의 local W9C demotion을 확인한다.

---

# 25. Required Artifacts

```text
workspace/runtime/attention/decode/w9d/
  ash_attn_decode_w9d_verification_runtime_specification.json
  ash_attn_decode_w9d_verification_runtime_artifact.json
  ash_attn_decode_w9d_verification_local_manifest.json

  ash_attn_decode_w9d_physical_runtime_specification.json
  ash_attn_decode_w9d_physical_runtime_artifact.json
  ash_attn_decode_w9d_physical_local_manifest.json

  fleet_authority_artifact.json
  fleet_authority_manifest.json
  rollout_wave_history.json
  fleet_stability_windows.json
  installation_adoption_receipts.json
  authority_journals.json
  revocation_artifact.json
  revocation_receipts.json
  driver_requalification_receipts.json
  device_loss_readoption_receipts.json
  fleet_demotion_summary.json
  stale_authority_matrix.json
  cross_installation_consistency_receipt.json
  final_no_stale_global_authority_seal.json
```

Rust가 생성한다.

코드 ZIP에 runtime artifact를 포함하지 않는다.

---

# 26. CLI Contract

필수 키:

```text
--patch-id
--expected-build-revision

--parent-w9c-artifact
--parent-w9c-manifest
--parent-w9c-global-default-seal

--fleet-id
--fleet-authority-epoch
--fleet-rollout-epoch
--fleet-revocation-epoch

--installation-count
--installation-root
--installation-id-prefix

--rollout-wave-plan
--rollout-window-count
--rollout-session-count
--rollout-token-count

--fleet-authority-signing-key
--fleet-authority-key-id
--fleet-authority-public-key

--revocation-signing-key
--revocation-key-id
--revocation-public-key

--maximum-offline-age-ms
--maximum-revocation-check-age-ms
--require-fail-closed

--driver-fixture-matrix
--device-loss-cycle-count
--process-restart-cycle-count

--require-remote-artifact-rollout
--require-authority-revocation
--require-driver-requalification
--require-device-loss-readoption
--require-fleet-wide-demotion
--require-no-stale-global-authority

--deny-unsigned-artifact
--deny-revoked-artifact
--deny-old-epoch
--deny-silent-fallback
--deny-full-context-readback
--deny-full-logits-readback
--deny-post-commit-rollback
--deny-unrecoverable-token-commit

--out-runtime-specification
--out-runtime-artifact
--out-local-manifest
--out-w9d-directory
```

unknown key와 duplicate key는 FAIL한다.

---

# 27. PASS Criteria

## Parent

```text
W9C physical artifact PASS                  true
W9C global default seal exact               true
W9C manifest digest exact                   true
```

## Fleet artifact

```text
signature valid                             true
issuer key allowlisted                      true
authority epoch monotonic                   true
rollout epoch monotonic                     true
revocation epoch monotonic                  true
```

## Rollout

```text
all required waves executed                 true
wave skip count                             0
three PASS windows per wave                 true
cross-installation mismatch                 0
```

## Soak

```text
required installation count                 reached
required session count                      reached
required token count                        reached
latency budget                              PASS
VRAM budget                                 PASS
owner leak count                            0
```

## Revocation

```text
revocation artifact applied                 all installations
revoked artifact readoption                 0
stale restart TensorCube adoption           0
```

## Driver

```text
driver drift detected                       true
old qualification reused                    false
requalification PASS before re-adoption      true
```

## Device loss

```text
required loss cycles                        completed
old device authority reused                 false
new identity proof                          present
re-adoption proof                           present
owner leak                                  0
```

## Fleet demotion

```text
targeted installations                      all
acknowledged installations                  all
demoted installations                       all
stale installations                         0
failed installations                        0
```

## Stale authority

```text
old epoch accepted                          0
expired artifact accepted                   0
revoked artifact accepted                   0
revoked key artifact accepted               0
```

## Safety

```text
dual production writer                      0
sampler double invocation                   0
token double commit                         0
full context readback                       0
full logits readback                        0
silent fallback                             0
post-commit rollback                        0
unrecoverable token commit                  0
```

---

# 28. Proposed Verification PASS Token

```text
PASS_ASH_ATTN_DECODE_W9D_FLEET_ARTIFACT_SIGNATURE_EPOCH_JOURNAL_ROLLOUT_WAVE_REVOCATION_DRIVER_REQUALIFICATION_DEVICE_LOSS_READOPTION_FLEET_DEMOTION_STALE_AUTHORITY_STATIC_VERIFICATION_SEALED
```

---

# 29. Proposed Physical PASS Token

```text
PASS_ASH_ATTN_DECODE_W9D_POST_PROMOTION_SUSTAINED_FLEET_SOAK_REMOTE_ARTIFACT_ROLLOUT_AUTHORITY_REVOCATION_DRIVER_UPDATE_REQUALIFICATION_DEVICE_LOSS_RECOVERY_READOPTION_FLEET_WIDE_INSTANT_DEMOTION_SIGNED_FLEET_EPOCH_MONOTONIC_REVOCATION_JOURNAL_CROSS_INSTALLATION_CONSISTENCY_HEADWISE_SAFE_DEMOTED_DEFAULT_NO_STALE_GLOBAL_AUTHORITY_NO_DUAL_PRODUCTION_WRITER_NO_FULL_CONTEXT_READBACK_NO_FULL_LOGITS_READBACK_NO_SILENT_FALLBACK_NO_POST_COMMIT_ROLLBACK_NO_UNRECOVERABLE_TOKEN_COMMIT_SEALED
```

---

# 30. Completion State

W9D PASS 후:

```text
TensorCube
  FleetGlobalDefaultWriter
  SignedArtifactBound
  RolloutWaveBound
  RevocationBound
  DriverRequalificationBound
  DeviceLossReadoptionBound

Headwise
  RollbackOnlyOracle
  FleetSafeDemotedDefault
  RevocationFallbackWriter

Fleet Authority
  EpochMonotonic
  Signed
  Revocable
  AntiRollback
  FailClosed

Installation
  CrossInstallationConsistent
  StaleAuthorityDenied
  RecoveryReadoptionBound
```

---

# 31. 다음 패치

```text
ASH-ATTN-DECODE-W9E

Multi-Model Fleet Authority /
Heterogeneous Device Profile Routing /
Signed Release Channel /
Transparency Log /
Remote Telemetry Compaction /
Automatic Recovery Rollout /
No Cross-Model Authority Bleed Seal
```

W9E 진입 조건:

```text
W9D fleet rollout PASS
W9D revocation PASS
W9D driver requalification PASS
W9D device-loss re-adoption PASS
W9D fleet demotion PASS
W9D no stale authority PASS
```

이 조건이 하나라도 빠지면 W9E를 시작하지 않는다.
