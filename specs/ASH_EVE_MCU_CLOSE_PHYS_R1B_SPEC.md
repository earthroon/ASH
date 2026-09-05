# ASH-EVE-MCU-CLOSE-PHYS-R1B

## MCU PERSISTENT-CHILD PHYSICAL IDENTITY + SUCCESSOR SOURCE-LOAD WITNESS

### 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-PHYS-R1B
Direct parent: ASH-EVE-MCU-CLOSE-PHYS-R1A
Class: PHYSICAL CONTINUATION IDENTITY + SOURCE AUTHORITY NO-RELOAD CLOSURE
Source release: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Native / WGPU physical qualification: HOLD
```

기준 본체:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1A_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: c1b136df5866b2d1fbf9e3be20085aead87ceb23caad1be3468621750187a207
```

조항 1~66은 요구 계약과 명시된 구현 선택이다. 실제 베이크·검사 결과는 부록 A에 분리한다. SOURCE / STATIC를 NATIVE / PHYSICAL 결과로 읽지 않는다.

예약 토큰:

```text
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_STATIC
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_NATIVE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_CHILD_CONSTRUCTION
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_CHILD_CONTINUITY
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_SOURCE_BOOTSTRAP
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_SUCCESSOR_NO_RELOAD
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B_CHECKPOINT_NO_REHYDRATE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1B
HOLD_ASH_EVE_MCU_CLOSE_PHYS_R1B_PENDING
```

이번 코드 베이크에서 native/physical PASS 토큰을 발행하지 않는다.

### 1. 목적

11개 persistent MCU child의 실제 production constructor 성공을 각각 기록하고 같은 R4 세션의 invocation 경계에서 같은 authority instance가 유지되는지 검사한다. 기존 durable source loader의 실제 진입을 기록하며, successor와 checkpoint-keep 이후에는 살아 있는 SourceState를 복원하고 durable source 재읽기로 대체하지 않는다.

같은 설정으로 만든 새 child와 같은 bytes를 다시 읽은 source는 continuation 증거가 아니다.

### 2. Source-derived parent state

기존 `McuPersistentChildAuthoritiesR7B`의 정확한 11개 child:

```text
McuGlobalTensorCubeJobQueueR6
McuMixedPrecisionExecutionExpertAuthorityR7
McuDeterministicPrecisionExpertRouterR8
McuGpuResidentExpertBucketAuthorityR8A
McuExactAtlasSlotLeaseGenerationRuntimeR1
McuSubmissionEpochDependencyRuntimeR1
ProductionMuonPendingQueueCutoverRuntimeR1
ProductionMuonPendingWaveQueueCoreR2
MuonDeviceCandidateRuntime
AsyncRetirementRuntime
McuRealProductionWaveShadowRuntimeR1
```

기존 `physical_child_construction_count = 1`은 wrapper-set telemetry다. 이것만으로 11개 각각의 생성 횟수를 주장하지 않는다. 기존 `load_source`를 authoritative durable source loader로 유지한다.

### 3. Non-goals

child 알고리즘, expert routing, arena, SubmissionEpoch, pending wave, device candidate, retirement, Adam/HiMuon 수학, R3C/R3C1 commit, R7B generation, R1A F2, durability, invocation 계획, producer cache 정책을 변경하지 않는다. 새 loader, checkpoint fallback, 두 번째 MCU owner, Python/PowerShell 실행기를 만들지 않는다.

### 4. Identity boundary

identity는 동일 프로세스의 instrumented Rust authority instance에 대한 증거다. mutable state digest, stack address, GPU buffer identity와 다르다. child 내부 상태는 진행할 수 있다. 이 revision은 내부 GPU allocation 전체가 같다는 주장까지 하지 않는다.

### 5. Child kind ABI

`McuPersistentChildKindR1B`의 canonical ordinal 0~10은 조항 2의 순서를 따른다. exact typed kind를 사용하고 문자열 정렬이나 mutable telemetry로 identity를 정하지 않는다.

### 6. Instance identity

`McuPersistentChildIdentityR1B`는 kind, construction ordinal, session digest, process instance ordinal, construction scope ordinal, optional intrinsic digest, instance digest를 포함한다. schema와 길이 framing을 넣어 SHA-256으로 결합한다. ordinal은 checked atomic allocation으로 발급하며 overflow는 오류다. process 재시작을 넘는 identity가 아니다.

### 7. Pointer prohibition

Rust owner 이동 때문에 `&child as *const _`는 authority가 아니다. stack address에 의존하지 않는다. metadata가 같다는 사실만으로 임의의 다른 객체를 채택하지 않는다.

### 8. Intrinsic identity

기존 stable intrinsic identity가 제공될 때만 결합할 수 있다. 이번 구현의 intrinsic 값은 `None`이며 없는 child API나 GPU identity를 만들어 넣지 않는다. process-local construction identity가 이번 관측의 기준이다.

### 9. Construction ledger

`McuPersistentChildConstructionLedgerR1B`는 최초 child 생성 이전에 열고, 실제 `new(...)?`가 성공한 직후 해당 객체를 `adopt(kind, child)`로 이동한다. constructor 실패는 success record를 만들지 않는다. 중복 kind와 ordinal overflow를 거부한다.

**구현 선택 S1:** 원래 R7 session identity는 일부 child 생성보다 늦게 확정된다. 생성 순서를 바꾸지 않고 unbound successful-construction ticket을 먼저 발급한 뒤 실제 R7 identity에 한 번만 결합한다.

### 10. Constructor callsite binding

원래 production construction 순서를 유지한다.

```text
device candidate -> async retirement -> wave shadow -> atlas lease
-> R7 parent
-> global queue -> dependency -> pending core -> pending cutover
-> mixed expert -> precision router -> GPU bucket
```

11개 성공 지점 각각에 하나의 ticket을 발급한다. wrapper 생성 시 11이라는 값을 대입하는 방식은 금지한다.

### 11. Exact completeness

seal 시 정확히 11 kinds, kind별 1회, unique instance, 동일 construction scope, 원래 성공 순서의 ordinal을 요구한다. 누락·중복·다른 scope의 record를 거부한다. 일부 child만 관측한 set은 완성된 R1B가 아니다.

### 12. Typed identity set

`McuPersistentChildIdentitySetR1B`는 기존 owning field 이름을 유지한 11개 명시적 필드를 갖는다. canonical ordered view로 digest를 계산한다. unordered map을 최종 identity authority로 사용하지 않는다.

### 13. Physical owner binding

**구현 선택 S2:** `ConstructedMcuChildR1B<T>`가 실제 child와 private construction record를 같이 소유한다. live wrapper에는 Clone/Deserialize/into_inner/record setter가 없다. R7B는 이 wrapper 11개와 consumed sealed ledger를 함께 소유하고 witness마다 실제 field ticket을 seal과 비교한다.

기존 child 알고리즘 호출을 유지하기 위해 Deref/DerefMut을 제공한다. 이것은 관측된 production source의 객체 연속성 계약이며, 임의 Rust 코드가 mutable reference로 내부 객체를 바꾸는 행위까지 언어 수준에서 차단한다는 주장은 아니다. production replacement 경로를 추가하지 않는다.

### 14. Replacement prohibition

동일 세션에서 child rebuild/set/replace/fallback API를 추가하지 않는다. actual ticket과 seal이 다르거나 경계 identity가 달라지면 오류다. 새 child가 필요하면 새 runtime/session이며 continuation으로 세지 않는다.

### 15. Legacy telemetry

기존 wrapper count의 의미와 값 1은 유지한다. R1B construction count는 실제 성공 record 길이로 계산하고 per-kind uniqueness를 확인한다. replacement count는 실제 field ticket 비교로 산출하며 mismatch는 거부한다.

### 16. Child boundary witness

기존 R4 live boundary에서 MCU session, typed set, set digest, wrapper count, actual-record count, replacement 결과를 읽는다. witness는 metadata만 복제한다. mutable child나 GPU 자원을 복제하지 않는다.

### 17. Close/Open continuity

모든 Close(N)/Open(N+1)에 session, kind, construction ordinal, instance ordinal, scope, instance digest, set digest가 동일해야 한다. construction count는 증가하지 않고 replacement는 0이어야 한다.

### 18. State progression

queue/submission/lease/pending/retirement/candidate telemetry와 내부 mutable state는 바뀔 수 있다. serialized child 전체 bytes의 equality는 요구하지 않는다. identity와 state를 분리한다.

### 19. Construction delta

정상 B/C 세션은 최초 11개 successful construction, wrapper 1개를 유지한다. 후속 invocation에 추가 constructor event가 있거나 다른 scope의 set이 나타나면 실패다. R4/ProductionMuon의 기존 reconstruction 검사도 유지한다.

### 20. Loader SSOT

기존 `load_source` 하나의 시그니처만 확장한다. `load_source_r1b`, continuation용 별도 loader, checkpoint-reload fallback을 만들지 않는다. 기존 source 해석·복구 로직은 유지한다.

### 21. Load context

```text
SourceLoadReasonR1B:
  InitialBootstrap
  FreshProcessResume
  SameSessionSuccessor
  CheckpointRehydrate

SourceLoadContextR1B:
  session_identity_digest
  invocation_ordinal
  reason
```

live ledger는 R4가 단독 소유한다. 이번 runtime 활성화는 기존 native PHYS request를 사용하며 별도 config flag를 추가하지 않는다. PHYS 없는 legacy context는 Disabled다.

### 22. Actual entry witness

실제 loader 입구에서 attempt를 기록하고 context/scope를 검사한다. 첫 source-authority read 전에 read-start phase를 기록한다. 성공은 반환되는 실제 SourceIdentity와 함께, 실패는 원래 cause와 함께 기록한다. attempt/success/failure/read-start를 혼동하지 않는다.

### 23. Fail before I/O

SameSessionSuccessor와 CheckpointRehydrate는 첫 durable read 전에 거부한다. ordinal 2 이상을 InitialBootstrap으로 표시해도 거부한다. Disabled context로 active PHYS source를 여는 것도 거부한다. cfg의 campaign/output binding이 owning ledger와 다르면 read 이전에 실패한다.

### 24. Initial bootstrap

각 B/C leg는 별도 세션이며 하나의 authoritative bootstrap load가 성공해야 한다. 이번 same-process campaign은 첫 load를 InitialBootstrap으로 분류한다. 그 입력이 기존 resume parent일 수 있음은 실제 path/source에 기록한다. FreshProcessResume reason은 새 프로세스 진입 계약과 별도로 구별하며 continuation reload로 사용하지 않는다.

### 25. Same-session successor

B의 4+4에서 bootstrap 1, actual in-memory restore 1, successor loader attempt/read-start/success 모두 0을 요구한다. SourceState를 실제 parked body에서 꺼내는 begin 경계에서 restore를 기록한다.

### 26. Checkpoint keep

C의 2+2+4에서 bootstrap 1, restore 2, successor 및 checkpoint rehydrate attempt/read-start/success 모두 0이다. 중간 checkpoint 완료는 기존 durability 증거가 담당한다. checkpoint write를 수행했다는 이유로 본체를 다시 읽지 않는다.

### 27. Allowed I/O

checkpoint write, recovery-head/reopen 검증, receipt publication과 기존 초기 N8 cursor preflight는 허용한다. source reload 금지는 live SourceState를 durable loader 결과로 대체하는 행위에 대한 것이다. 모든 invocation 간 I/O가 0이라는 주장은 하지 않는다.

### 28. Source event ledger

actual event 종류:

```text
InvocationEntered / LoadAttempt / DurableSourceReadStarted
DurableBootstrapLoad / LoadFailed
DurableReloadAttemptRejected / CheckpointRehydrateAttemptRejected
BootstrapSourcePrepared / InMemoryInvocationRestore
InvocationSuccessorAdopted / BoundaryOpen / BoundaryClose
```

ordinal, invocation, reason, optional source/path/error를 기록한다. event 수는 봉인된 step/invocation 수로 제한한다. snapshot digest를 재계산하고 상태 전이 전체를 replay해 검사한다.

### 29. Causal order

**구현 선택 S3:** 기존 R4의 InvocationEntered는 bootstrap보다 먼저다. 실제 실행 Open witness는 bootstrap/materialization 이후다. 이 둘을 같은 사건으로 취급하지 않는다.

```text
InvocationEntered(1) -> loader attempt/read/success
-> BootstrapSourcePrepared -> BoundaryOpen(1)
-> committed successor events -> BoundaryClose(1)
-> InvocationEntered(2) -> actual InMemoryInvocationRestore
-> BoundaryOpen(2)
```

최초 packing/recovery metadata로 raw loaded source와 prepared source digest가 달라질 수 있다. 동일 generation/optimizer/cursor progression을 확인하고 두 시점의 identity를 구분해서 남긴다. 후속 close/open equality를 완화하지 않는다.

### 30. Exact source boundary

training generation, optimizer generation, cursor/next batch, scheduler digest, training-state parent digest, complete SourceState digest를 기존 identity로 비교한다. 승인된 successor는 실제 `build_source_after_commit` 결과를 source에 설치한 지점에서 기록한다. generation/optimizer는 +1, cursor는 기존 accumulation8에 맞게 +8이어야 한다.

### 31. Equivalent reload forbidden

close와 open digest가 같아도 중간 durable reload event가 있으면 실패다. reload count를 source가 존재한다는 사실로 추정하지 않는다. final replay는 정상 campaign에 load attempt/read-start/success 각 1과 rejected/failed event 0을 요구한다.

### 32. Scope

source ledger는 process id, checked session instance ordinal, campaign digest, R4A seal, output identity로 scope를 봉인한다. 다른 세션의 이벤트와 합치지 않는다. B/C는 동일 campaign 조건을 공유하지만 서로 다른 session/child instances다.

### 33. Counters

이벤트에서 reason별 attempts/read-starts/successes/failures/rejects와 in-memory restore/successor adoption을 산출한다. cfg flag 또는 관측기가 만든 고정값을 계수로 쓰지 않는다. final event 수와 causal order를 함께 검증한다.

### 34. Read witness scope

read-start는 기존 loader가 첫 active-state read에 진입한 source-read phase 횟수다. filesystem syscall 횟수가 아니다. 내부 recovery redirect read는 같은 loader의 원래 경로다. N8의 초기 cursor preflight는 source authority loader 호출과 구별한다. successor negative test는 attempts 1 증가, read-start 증가 0을 검사한다.

### 35. Successor negative test

기존 loader에 active ordinal 2와 SameSessionSuccessor를 제시한다. `SUCCESSOR_SOURCE_RELOAD_FORBIDDEN`을 반환하고 실제 read marker에 도달하지 않아야 한다. 정상 WGPU leg에는 금지된 호출을 의도적으로 넣지 않는다.

### 36. Checkpoint negative test

CheckpointRehydrate로 실제 기존 loader를 호출하면 `CHECKPOINT_REHYDRATE_FORBIDDEN`이고 read-start는 0이다. 데이터 파일이 없어서 우연히 실패한 결과와 admission 단계의 거부를 구별한다.

### 37. Identity replacement test

native metadata에서 한 child identity를 다른 instance로 바꿔 boundary 비교가 거부하는지 검사한다. actual field ticket mismatch도 검사한다. fixture는 GPU child가 교체됐다는 physical 증거가 아니다.

### 38. Missing child test

required kind 하나라도 빠지면 seal이 실패한다. 단순 길이만 맞는 set을 허용하지 않는다. per-kind completeness와 actual wrapper ticket 대응을 함께 검사한다.

### 39. Duplicate test

kind 중복, instance 중복, construction order/scope 변형을 각각 거부한다. 다르게 부여된 ordinal이 kind 중복을 정당화하지 않는다.

### 40. Production campaign

기존 `SuccessAbc` Rust campaign을 사용한다. A는 기준, B 4+4와 C 2+2+4가 R1B 필수 leg다. 기존 native gate, numerical 비교, source recheck 이후에만 R1B publication 함수가 호출된다. 새 executor/loader/JSON PASS import를 만들지 않는다.

### 41. Leg B

actual runtime 1, wrapper 1, per-kind construction 1씩 총 11, replacement 0, boundary match 1, bootstrap1, restore1, successor/rehydrate0, 정상 final close를 요구한다.

### 42. Leg C

B와 독립된 session과 instances에서 wrapper1/children11, replacement0, boundary match2, bootstrap1, restore2, checkpoint durability 및 no-rehydrate, 정상 final close를 요구한다.

### 43. Terminal preservation

모든 park에서 기존 R7/R7B active generation 없음, target/pending/retirement terminal-safe, phase Open을 계속 요구한다. persistent child identity가 유지된다는 사실로 generation-local 작업 유출을 허용하지 않는다.

### 44. Final live witness

final release 전에 실제 11개 field ticket과 session identity를 관측한다. release 후에는 metadata snapshot만 남는다. witness가 mutable child를 소유하거나 수명을 연장하지 않는다. 기존 durability/live/release/Closed 순서를 유지한다.

### 45. Cache separation

R7A DeviceAuthority cache는 다른 수명이다. R1B child release 때문에 global cache 파괴나 Arc strong count 0을 요구하지 않는다. producer replacement 실험은 R1C다.

### 46. Physical claim limit

이 코드에서 actual constructor 관측, sealed owner ticket, actual field 대조, no-reconstruction과 경계 equality를 결합한다. 임의 코드 변경, 메모리 변조, child 내부 모든 GPU allocation 동일성을 포괄하는 보장이 아니다. physical 승격은 해당 instrumented source의 실제 native/WGPU 실행으로만 가능하다.

### 47. Errors

최소 구별:

```text
CHILD_LEDGER_NOT_SEALED / CHILD_COUNT_NOT_EXACT
DUPLICATE_CHILD_KIND / DUPLICATE_CHILD_INSTANCE / CHILD_KIND_MISSING
CHILD_IDENTITY_DRIFT / CHILD_RECONSTRUCTED / CHILD_REPLACED / CHILD_SESSION_DRIFT
SOURCE_BOOTSTRAP_COUNT_DRIFT / SUCCESSOR_SOURCE_RELOAD_FORBIDDEN
CHECKPOINT_REHYDRATE_FORBIDDEN / SOURCE_LOAD_REASON_DRIFT / SOURCE_LOAD_SCOPE_DRIFT
SOURCE_RESTORE_COUNT_DRIFT / SOURCE_IDENTITY_DRIFT
SOURCE_READ_PHASE_REPEATED / SOURCE_EVENT_ORDER / EVENT_BOUND_EXCEEDED
```

실제 구현은 기존 prefix와 parent cause를 유지한다. read-start 이후 실패도 완료로 기록하지 않는다.

### 48. Child receipt

`eve_mcu_close_phys_r1b_child_identity_receipt.json`은 native/campaign identity, leg/session, 11개 typed records, 모든 close/open/final live witnesses를 담는다. 원시 child receipt 자체는 `physical_pass_claimed=false`다.

### 49. Source receipt

`eve_mcu_close_phys_r1b_source_load_receipt.json`은 scope, raw causal events, initial path/source, restore/adoption, reason별 telemetry, event digest를 담는다. 원시 source receipt 자체는 physical PASS가 아니다.

### 50. Combined receipt

`eve_mcu_close_phys_r1b_promotion_receipt.json`은 child/source receipt digest, 실제 native admission, A/B/C numerical comparison을 결합한다. 두 원시 증거와 실제 parent R4A/R7/source witness를 모두 대조한 이후에만 R1B PASS를 쓴다. 하나만 존재하거나 다른 session 자료를 섞으면 실패다.

### 51. Expected telemetry

| 필드 | B | C |
| --- | ---: | ---: |
| wrapper construction | 1 | 1 |
| successful child construction | 11 | 11 |
| per-kind construction | 1 | 1 |
| replacement | 0 | 0 |
| close/open child match | 1 | 2 |
| bootstrap attempt/read/success | 1/1/1 | 1/1/1 |
| successor reload attempt/read/success | 0/0/0 | 0/0/0 |
| checkpoint rehydrate attempt/read/success | 0/0/0 | 0/0/0 |
| in-memory restore | 1 | 2 |
| committed successor adoption | 8 | 8 |

이는 기대 조건이며 이번 베이크의 GPU 측정값이 아니다.

### 52. No fabricated counts

wrapper 존재로 children11을 대입하지 않는다. source 존재로 load1을 대입하지 않는다. restore 성공으로 reload0을 추정하지 않는다. actual record/event를 비교해 얻은 값만 판정한다.

### 53. Source scope

기존 수정: R7B owner, ProductionMuon constructor spine, R4 owner, scheduler, PHYS audit/campaign, lib exports. 새 Rust:

```text
mcu_persistent_child_physical_identity_r1b.rs
source_load_witness_r1b.rs
eve_mcu_close_physical_identity_source_r1b.rs
```

모두 `crates/base_train/src/` 아래다. backend/WGSL/Cargo 파일은 이번 베이크에서 변경하지 않는다. 기존 R7B 정적 검사 1개만 실제 wrapped owning types와 constructor 기록을 검사하도록 갱신한다.

### 54. Loader signature

```text
load_source(cfg, SourceLoadWitnessContextR1B)
context = Disabled | Active { context, live ledger borrow }
```

실제 진입의 permit은 context와 cfg를 검증하고, 첫 read phase를 통과한 실제 성공 결과를 기록한다. legacy Disabled는 PHYS request가 없는 경우에만 허용한다. 읽기 본체를 두 번째 public loader로 분리하지 않는다.

### 55. Rust branching

신규 module은 typed enum/match를 사용한다. unrelated if를 정리하지 않는다. 기존 child 알고리즘이나 source 해석식의 전역 포맷 변경은 범위 밖이다.

### 56. Static acceptance

S01~S18: exact11 kind, actual constructor별 성공 기록, 성공 이후 발급, owner/ticket 결합, replacement 경로 부재, wrapper 의미 유지, boundary 포함/equality, 단일 loader, actual entry, successor/rehydrate read전 거부, 실제 parked restore, load/restore event 구분, checkpoint write 구분, Python/PowerShell loader 없음, commit/generation authority 불변을 검사한다.

### 57. Native acceptance

N01~N18: exact set, 각 missing/duplicate/instance/session/replacement 오류, mutable state progression 허용, deterministic digest, bootstrap, successor/checkpoint pre-I/O 거부, scope drift, source boundary, 동일 digest+reload 거부, restore count, 두 증거 모두 필요한 promotion을 검사한다.

실제 native gate는 test executable inventory와 exact test 실행을 확인한다. 0-test/ignored-test는 성공이 아니다. CPU fixture는 physical token 근거가 아니다.

### 58. WGPU acceptance

P01~P25는 다음을 각각 실제 생산 실행에서 요구한다.

```text
P01 B actual startup
P02 exact11 children
P03 per-kind successful constructor1
P04 no duplicate construction
P05 wrapper1
P06 B close/open exact
P07 no reconstruction
P08 no replacement
P09 bootstrap1
P10 successor attempt/read/success0
P11 source exact
P12 restore1
P13 B normal final close
P14 C independent session
P15 C children11
P16 C first boundary exact
P17 C second boundary exact
P18 intermediate durable checkpoint
P19 checkpoint rehydrate0
P20 successor load0
P21 restore2
P22 both source boundaries exact
P23 final live child witness
P24 actual session-owned release
P25 raw constructor/load records bound to receipts
```

### 59. Numerical non-change

부모의 사전에 봉인한 numerical comparison을 유지한다. R1B 때문에 tolerance를 넓히지 않는다. metadata 관측이 계산 결과의 drift를 만들면 HOLD다.

### 60. Promotion

actual native gate, 정상 B/C, P01~P25, 원래 R4/R7 witness와의 exact join, source event replay, numerical 비교, final lifecycle을 모두 만족해야 한다. production 결과와 연결되지 않은 serialized fixture나 수동 counter로 PASS하지 않는다. 실제 source recheck 이후 별도 R1B receipt가 발행된다.

### 61. Rejection

11개 미완성, constructor/instance 중복, 경계 교체, wrapper/runtime reconstruction, bootstrap 횟수 오류, 정상 campaign의 reload 시도, checkpoint rehydrate, 동일 bytes 재생성, restore mismatch, release 후 witness, pointer-only identity, 추정 계수는 HOLD다. final evidence 작성 실패도 성공 receipt로 바꾸지 않는다.

### 62. Artifact policy

code ZIP에 명세·audit manifest·검사 로그·생성된 physical/campaign receipts를 넣지 않는다. Rust/WGSL 및 기존 build-required Cargo metadata/fixtures는 유지한다. 신규 Python/PowerShell loader는 없다.

### 63. R1A relationship

R1A consumer completion/lease/arena 결과와 R1B constructor/source continuity는 독립 축이다. source가 누적됐다는 이유로 R1A 또는 R1B physical PASS가 성립하지 않는다.

### 64. Remaining parent work

R1C actual WGPU producer replacement, R1D full binary/source/RNG/dataset provenance, R1E aggregate qualification이 남는다. 종합 PHYS-R1 HOLD/exit2는 유지한다. R1B receipt에 `parent_phys_r1_promoted=false`를 명시한다.

### 65. Direct successor

```text
ASH-EVE-MCU-CLOSE-PHYS-R1C
REAL WGPU PRODUCER INSTANCE REPLACEMENT REJECTION
+ COLD / WARM / REUSE PHYSICAL AUTHORITY CLOSURE
```

### 66. Final law

> 같은 설정의 새 child가 아니라 같은 살아 있는 authority를 넘긴다.
>
> checkpoint를 썼다는 사실은 source를 다시 읽어야 한다는 뜻이 아니다.
>
> 생성과 load의 실제 진입 증거 없이 physical PASS를 발행하지 않는다.

## 부록 A. 실제 source bake

```text
Release: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Modified existing files: 8 (Rust 7, existing Python static validator 1)
Added files: 3 (Rust)
Deleted: 0
Unchanged parent files: 8397
New Python / PowerShell loader: 0
Backend / WGSL / Cargo files modified: 0
```

constructor-ticket wrapper와 typed seal, actual 11 constructor callsite, R4-owned loader/event ledger, actual loader pre-I/O denial, close/open source-child join, 기존 SuccessAbc campaign의 별도 R1B promotion을 소스에 반영했다.

**추가 구현 선택 S4:** 최초 live MCU witness는 actual R7 identity를 요구한다. 기존 생산 코드가 job submission에서 하던 `bind_device_queue`를 PHYS profile의 초기 witness 이전에 기존 native queue로 수행한다. 기존 Device/Queue metadata/domain binding만 앞당기며 새 Device/Queue, GPU buffer 또는 optimizer job을 만들지 않는다. Eve/Device join이 없으면 identity를 추정하지 않고 거부한다.

S1의 late session binding, S2의 actual child와 ticket 공동 소유, S3의 InvocationEntered/raw load/prepared/Open 구분은 기존 구조에 맞춘 명시적 구현 선택이다. 최초 load phase와 전체 disk I/O를 구분하고, wrapper의 DerefMut을 임의 코드 변경에 대한 완전한 교체 방지 수단으로 과장하지 않는다.

실행한 검사:

```text
Existing related static scripts: 16/16 PASS
R1B source-contract checks: 75/75 PASS
Changed/added Rust UTF-8 + lexical delimiter checks: 10/10 PASS
New Rust native tests: 38 added, NOT RUN
  child identity: 12
  source ledger: 14
  combined observation: 7
  actual loader negative/error tests: 5
Cargo/rustc compile, borrow checking, link: NOT RUN
WGPU / numerical parity / physical campaign: NOT RUN
Physical PASS generated by this bake: none
```

정적 검사 최초 실행에서는 R7B 검사가 이전 raw field type을 기대해 실패했다. 기존 11개 owning-field 검사를 새 typed wrapper로 옮기고 실제 constructor-adopt/seal 연결 검사 5개를 추가했다. 업데이트 후 해당 검사 83/83, 관련 스크립트 16/16을 확인했다. 주석 문자열이나 테스트 삭제로 통과시키지 않았다.

Cargo/Rustc/Rustfmt가 환경에 없어 native test는 실행하지 못했다. lexical delimiter 검사는 Rust parser나 borrow checker가 아니다. 부모부터 없는 sherpa-rs path dependency와 일부 test include 입력을 가짜 crate/JSON으로 채우지 않았다. 독립 workspace 전체 빌드를 보장하지 않는다.

코드 전용 산출물:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1B_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: 214f69a8654649ef12aad16afdd78a290ade1d20a3b76662d5470280eb46fc15
Bytes: 21361340
Files: 8408
ZIP CRC: PASS
Duplicate paths: 0
Unicode paths with UTF-8 flag: 18
PowerShell files: 0
```

root Cargo.toml/Cargo.lock과 영향 crate의 Cargo.toml은 부모와 동일하다. 명세·변경 파일별 해시·검사 원문·소스 diff는 코드 ZIP 밖에서 제공한다.

## 부록 B. 실행 및 증거 상태

기존 native Rust PHYS campaign의 `SuccessAbc` mode를 그대로 사용한다. R1B를 위한 별도 loader/config 계획은 추가하지 않는다. A/B/C가 실제 실행되고 native gate, 전체 비교, source recheck와 final audit가 통과하면 R1B child/source/combined receipt를 출력한다.

R1A F2 mode에도 정상 source/child 경계 관측이 들어가지만 그것만으로 B/C 기반 R1B promotion을 대신하지 않는다. 새 코드를 베이크한 지금은 native와 physical 결과 모두 판단불가이며, 실제 runtime receipt가 없는 상태의 종합 HOLD를 유지한다.
