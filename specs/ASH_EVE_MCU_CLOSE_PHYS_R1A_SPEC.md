# ASH-EVE-MCU-CLOSE-PHYS-R1A

## EXACT-CONSUMER-DELAY + ARENA-REUSE PHYSICAL NEGATIVE CLOSURE

### 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-PHYS-R1A
Direct parent: ASH-EVE-MCU-CLOSE-PHYS-R1
Class: R7A1 EXACT MULTI-CONSUMER PHYSICAL NEGATIVE QUALIFICATION
Source status: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Native / WGPU physical qualification: HOLD
```

기준 본체:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: ccfe4ff69c7812c86ba5003c8d90f841141943eff943707f57b01a0b916845ae
```

아래 조항은 실행 계약이다. 실제 베이크와 검사 결과는 부록 A에 구분한다. 정적 검사를 GPU 실행 결과로 읽지 않는다.

예약 토큰:

```text
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_STATIC
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_NATIVE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_RELEASED_AWAITING_COMPLETION_REJECT
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_LIVE_LEASE_REJECT
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_EXACT_RETIREMENT
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_ARENA_RECLAIM
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A_ARENA_REUSE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A
HOLD_ASH_EVE_MCU_CLOSE_PHYS_R1A_PENDING
```

### 1. 목적

R7A1 packed-gradient allocation의 exact consumer 하나라도 `RetiredComplete`가 아니면 arena reclaim을 거부한다. 모든 consumer의 completion과 logical release가 완료되면 기존 reclaim으로 page를 반환하고, 같은 page의 재사용은 더 큰 incarnation으로만 허용한다.

실제 WGPU consumer submission, SubmissionEpoch, logical lease, physical allocation, arena page를 하나의 증거로 결합한다.

### 2. 비목표

Adam/HiMuon 수학, gradient packing 계산, DeltaK, R3C/R3C1 commit, R7B ownership, R4 continuation, durability, producer cache, 정상 allocation 정책과 production consumer 순서는 바꾸지 않는다.

새 Python/PowerShell 로더, mock completion, CPU 대체 consumer, 별도 arena, 두 번째 reclaim 알고리즘을 만들지 않는다.

### 3. 기존 authority

```text
PackedGradientProducerOutputR7A1 / PackedGradientReadBindingR7A1
McuPackedGradientRuntimeR7A1 / McuPackedGradientIdentityR7A1
SubmissionEpoch / TrackedSubmission
LogicalLeaseId / PhysicalAllocationId
CompletionCoverage::ExactTracked / LeaseRetirementDisposition
ArenaLease / McuArenaDomainIdR7A / page ordinal / incarnation
```

정상 종료는 기존 `verify_and_reclaim_packed_gradient_multi_consumer_r7a1`과 `reclaim_arena_lease_in_domain_r7a`를 사용한다.

### 4. 닫을 경로

```text
actual consumer outstanding
  -> same reclaim admission rejects
  -> same page remains active
  -> exact completion AND logical release
  -> existing final reclaim
  -> stale incarnation rejected
  -> same page reused with new incarnation
```

조건문이 존재한다는 사실만으로 이 경로의 물리 PASS를 주장하지 않는다.

### 5. Core law

```text
Reusable = producer.RetiredComplete
        AND every exact consumer.RetiredComplete
```

`Live`, `PendingQueueWrite`, `InFlight`, `HostMapped`, `ReleasedAwaitingCompletion`, `ConservativeHold`는 거부한다. GPU completion과 logical release는 서로 대체할 수 없다. generation 진행은 completion 증거가 아니다.

### 6. Qualification consumer

기존 `PackedGradientConsumerKindR7A1::QualificationShadow`를 사용한다. 동일 packed-gradient를 read-only로 읽고 qualification scratch에만 쓴다. Weight, momentum, candidate, Adam M/V와 commit authority를 갖지 않는다.

### 7. 실제 WGPU operation

입력은 실제 R7A1 owned-existing binding이다. 출력은 별도 scratch다. WGSL은 bounded gradient element를 읽고 scratch에 atomic side effect를 남긴다. shader/pipeline/bind-group validation 오류는 명시적 오류로 반환한다.

빈 submission, shader 없이 작성한 lease, external borrowed 대체를 consumer 증거로 받지 않는다.

### 8. 봉인된 work budget

```text
shadow_dispatch_count default 256, admitted 1..=4096
shadow_elements_per_dispatch default 256, admitted 1..=256
maximum_shadow_read_elements default 65536, upper bound 1048576
actual elements = min(packed logical elements, configured element count)
```

설정의 dispatch*element 상한은 실행 전에 검사한다. sleep, host spin, 가짜 completion, 실행 중 workload 증가는 금지한다. 실제 incomplete observation window를 못 잡으면 HOLD다.

`reuse_policy`는 `NaturalOnly` 또는 `NaturalThenSameDomainReacquire`이며 campaign 시작 전에 봉인한다.

### 9. 대상 선정

exact multi-consumer 및 arena reuse admission이 모두 활성이고 실제 owned packed binding이 존재해야 한다. 이번 구현은 봉인된 production traversal에서 처음 생성한 R7A1 runtime 하나를 선택한다.

model/optimizer generation, canonical parameter, binding digest, physical allocation, domain, page, incarnation을 선택 시 기록한다. 실패 후 다른 target으로 다시 시도하지 않는다.

### 10. F2-A: ReleasedAwaitingCompletion

```text
A1 real shadow A submission
A2 actual nonblocking incomplete observation
A3 logical gradient lease release
A4 ReleasedAwaitingCompletion observed
A5 same reclaim classifier rejects
A6 arena still active and unchanged
A7 exact completion
A8 RetiredComplete
```

A2 이후 completion이 먼저 도착해 A4가 관측되지 않으면 `RELEASED_AWAITING_COMPLETION_NOT_OBSERVED`다. 정상 completion을 늦추거나 tracker 상태를 고쳐 window를 만들지 않는다.

### 11. F2-A attribution

producer와 원래 production consumer는 모두 exact retired여야 한다. Shadow A만 유일한 blocker여야 한다. 다른 blocker가 있거나 attribution이 불분명하면 HOLD다.

### 12. F2-B: completed but Live

```text
B1 real shadow B submission
B2 exact completion
B3 logical lease not released: Live
B4 same reclaim classifier rejects
B5 arena still active and unchanged
B6 logical release
B7 RetiredComplete
```

Shadow B는 A와 다른 actual lease 및 submission epoch를 갖는다. completion만으로 release를 대신하지 않는다.

### 13. Shared reclaim admission SSOT

`classify_packed_gradient_reclaim_r7a1`은 production reclaim과 negative probe가 공유하는 read-only classifier다.

```text
PackedGradientReclaimAdmissionR1A
  Eligible
  Blocked { exact lease/site/disposition blockers }
```

allocation, domain, queue, page, incarnation, logical range, producer, exact consumer set, coverage와 actual epoch를 검증한다. production reclaim은 Eligible일 때만 기존 mutation을 호출한다.

의미 변경 S1: eligibility 계산 위치를 하나로 모은다. 모든 exact consumer가 retired여야 한다는 안전 조건은 완화하지 않는다.

### 14. Negative probe ownership

negative classifier는 runtime을 consume하거나 arena를 반환하지 않는다. 예상된 Blocked는 qualification의 정상 관측이며 같은 runtime에서 completion/release를 마친 뒤 기존 `seal_and_reclaim`을 수행한다.

Shadow admission은 `ConsumerSetSealed` 전이다. direct reclaim과 deferred reclaim 모두 같은 runtime hook을 통과한다.

### 15. Arena non-mutation witness

negative 전후 allocation, domain, page, incarnation, in-use, reclaim counter와 domain active count가 같아야 한다. 두 probe의 reclaimed-range delta는 0이다.

F2 reject 통계는 실제 causal journal에서 산출한다. read-only probe 때문에 global arena allocator의 계수를 임의로 증가시키지 않는다.

### 16. Exact completion

기존 nonblocking poll, actual completion mailbox, `wait_for_submission_exact`와 exact Device/Queue/SubmissionEpoch를 사용한다. timeout, 경과 시간, 함수 반환, generation은 completion이 아니다.

관측 실패 때도 제출된 shadow를 exact drain한 뒤 logical lease를 정리한다. drain 실패는 cleanup 미완료 오류이며 arena 재사용을 승인하지 않는다. completion publication을 의도적으로 보류하는 구현은 사용하지 않는다.

### 17. 최종 reclaim

producer, 원래 production consumers, Shadow A/B 모두 ExactTracked 및 RetiredComplete여야 한다. 기존 final reclaim을 수행하고 page가 실제 free인지 확인한다.

기존 `PackedGradientLifetimeReceiptR7A1.physical_pass_claimed`는 false를 유지한다. R1A physical promotion은 별도 campaign receipt만 담당한다.

### 18. Stale incarnation

reclaim 직후 old binding은 page-not-active로 거부된다. 재사용 후에는 old incarnation이 stale로 거부된다. 임의 오류를 stale rejection으로 인정하지 않고 해당 오류와 실제 page witness를 함께 검사한다.

### 19. Positive reuse

먼저 다음 natural production allocation에서 같은 page의 새 producer submission을 관측한다. 없으면 final live capture 전에 봉인된 정책이 허용하는 경우에만 기존 allocator로 same-domain reacquire를 수행한다.

같은 physical allocation, page, key/size class, 더 큰 incarnation이 필요하다. allocator에서 다른 page가 나오면 그것을 정리한 뒤 mismatch/HOLD다. 특정 page를 강제로 주는 allocator를 추가하지 않는다.

### 20. Reuse evidence class

```text
ProductionNaturalReuse
QualificationSameDomainReacquire
```

natural reuse가 우선이다. reacquire는 같은 budget/domain/class로 실제 buffer를 얻고, tracked initialization submission과 exact completion/release/reclaim을 수행한다. training step이나 optimizer 갱신으로 세지 않는다.

### 21. Campaign integration

기존 Rust campaign에 `F2ConsumerDelay`를 추가한다. 이 모드는 동일 조건의 Leg A reference 8 step과 F2 8 step을 실행한다.

F2는 training failure leg가 아니다. 두 예상 reject, 정상 reclaim/reuse, 정상 final close가 모두 성공해야 한다. 기존 production entry 이외의 executor를 만들지 않는다.

### 22. Numerical non-perturbation

Leg A와 F2의 initial streams, registry, generation, optimizer step, cursor, scheduler 진행을 비교한다. Weight/Adam M/V/HiMuon momentum과 8-step loss sequence는 부모의 사전 봉인 tolerance를 사용한다.

실행 후 tolerance를 넓히지 않는다. R1A가 전체 RNG/data provenance 미완결을 대신 해결했다고 주장하지 않는다.

### 23. Production consumer set

원래 consumer를 제거하거나 observer/fused route를 끄지 않는다. final exact set은 baseline production set에 actual Shadow A/B lease를 추가한 집합과 같아야 한다.

의미 변경 S2: 동일 physical page의 이전 incarnation에서 남은 lease 이력은 exact retired인지 계속 검사하지만 현재 producer의 consumer count에는 넣지 않는다. 기존 A01의 단조 증가 LogicalLeaseId를 경계로 사용한다. 과거 non-retired lease는 거부한다. 현재 집합의 누락/중복/알 수 없는 consumer는 거부한다.

### 24. No silent fallback

missing packed binding, ExternalBorrowed, missing arena, unknown coverage, missed delay window, unexpected eligibility, reuse mismatch는 오류/HOLD다. CPU tensor, 새 buffer, fake state, telemetry-only PASS로 대체하지 않는다.

### 25. 오류 계약

최소 구별:

```text
TARGET_PROFILE_NOT_ADMITTED / PACKED_BINDING_MISSING
SHADOW_BUILD_FAILED / SHADOW_SUBMIT_FAILED
DELAY_WINDOW_NOT_OBSERVED
RELEASED_AWAITING_COMPLETION_NOT_OBSERVED / LIVE_LEASE_NOT_OBSERVED
EARLY_REUSE_NOT_REJECTED / BLOCKER_ATTRIBUTION_AMBIGUOUS
ARENA_MUTATED_ON_REJECT / EXACT_COMPLETION_MISSING
LEASE_NOT_RETIRED / SHADOW_CLEANUP_INCOMPLETE
FINAL_RECLAIM_FAILED / OLD_INCARNATION_STILL_ACTIVE
REUSE_NOT_OBSERVED / REUSE_ALLOCATION_DRIFT
NUMERICAL_DRIFT
```

실제 기존 오류는 cause로 보존한다. qualification 오류와 production 오류를 함께 기록한다. 정상 상태를 찍은 뒤 오류를 숨기지 않는다.

### 26. Receipt

```text
file: eve_mcu_close_phys_r1a_f2_consumer_delay_receipt.json
schema: ash.eve_mcu.close.physical.r1a.consumer_delay
```

필수 binding: campaign/native identity, selected model/optimizer generation/parameter, physical allocation/device/queue/domain/page/incarnation, producer epoch/lease, baseline exact consumers, Shadow A/B actual epoch/lease, negative proofs, non-mutation witnesses, exact final disposition, final reclaim witness, reuse class/new incarnation/new submission, numerical comparison 및 receipt digest.

source snapshot은 actual `retire_after_submission`을 포함한다. stored admission 결과는 같은 classifier로 재검증한다. 이 파일은 실행 authority가 아니며 JSON을 읽어 PASS를 가져오는 경로는 없다.

### 27. Causal order

A1<A2<A3<A4<A5<A6<A7<A8, B1<B2<B3<B4<B5<B6<B7을 요구한다. A8와 B7 이후 C1(all retired), C2(final reclaim), C3(old rejected), C4(new reuse) 순서다.

wall-clock 대신 실제 operation journal의 순서를 사용한다. 중복/누락/역전은 거부한다.

### 28. Telemetry

정상 receipt의 actual journal에서 shadow submit 2, incomplete 1, ReleasedAwaitingCompletion 1, completed-Live 1, expected reject 2, exact shadow completion 2, retirement 2, selected-page final reclaim 1, stale rejection 1, positive reuse 1을 산출한다.

negative reclaim delta는 0이다. config true나 고정 대입을 실행 횟수로 쓰지 않는다. 수치 drift와 unexpected success는 최종 승격을 막는다.

### 29. Source scope

기존 파일: backend R7A1, A01 snapshot, arena witness, MCU packed runtime, 생산 pack callsite, PHYS-R1 campaign/audit, 필요한 module exports.

신규 파일:

```text
crates/burn_webgpu_backend/src/himuon_packed_gradient_consumer_delay_r1a.rs
crates/burn_webgpu_backend/src/himuon_packed_gradient_consumer_delay_r1a.wgsl
crates/base_train/src/eve_mcu_close_physical_consumer_delay_r1a.rs
```

기존 R7A1 정적 검사 1개는 바뀐 검사 위치를 따라가도록 갱신한다. 새 Python validator나 loader는 코드 ZIP에 추가하지 않는다.

### 30. Rust branching

신규 Rust admission/state branching은 typed enum과 match를 사용한다. 무관한 기존 if를 리팩터하지 않는다. WGSL의 bounded index guard는 shader 내부 조건이다.

### 31. Static acceptance

실제 owned binding, tracked submission, exact epoch/lease/allocation, page/incarnation, common classifier, non-consuming probe, non-mutation, 두 disposition, 기존 final reclaim, stale/new incarnation, Rust campaign 연결, 기존 수학/commit 불변을 검사한다.

정적 검사는 컴파일이나 GPU 실험을 대신하지 않는다.

### 32. Native acceptance

두 영향 crate의 실제 Cargo 검사와 테스트 실행 파일을 사용한다. test inventory를 읽고 exact test별 실행을 확인한다. 0-test/ignored-test는 PASS가 아니다.

R1A tests는 disposition, exact set, historical lease, epoch/coverage drift, duplicate/missing consumer, work bound, scope, event order, ambiguous blocker를 검증한다. 가짜 native fixture로 physical token을 발급하지 않는다.

### 33. WGPU acceptance

| ID | 검사 | 필수 결과 |
| --- | --- | --- |
| P01 | target profile | exact lease + arena active |
| P02 | packed binding | real owned existing |
| P03 | Shadow A | real WGPU epoch/lease |
| P04 | incomplete window | actually observed |
| P05 | A release | ReleasedAwaitingCompletion |
| P06 | A admission | reject |
| P07 | A attribution | only A blocks |
| P08 | A page | unchanged and active |
| P09 | A completion | exact |
| P10 | A retirement | RetiredComplete |
| P11 | Shadow B | different real epoch/lease |
| P12 | B completion | exact |
| P13 | B unreleased | Live |
| P14 | B admission | reject |
| P15 | B attribution | only B blocks |
| P16 | B release | RetiredComplete |
| P17 | full exact set | all retired |
| P18 | final reclaim | existing path succeeds |
| P19 | stale binding | rejected |
| P20 | positive reuse | same page, new incarnation |
| P21 | production consumers | preserved |
| P22 | numerical parity | sealed contract passes |
| P23 | workload | 8-step normal final close |
| P24 | unexpected success | none |
| P25 | receipt | raw observations bound |

### 34. Promotion gate

native admission, real Leg A/F2 completion, P01-P25, numerical comparison, source recheck 및 receipt publication을 모두 만족한 경우에만 `PASS_ASH_EVE_MCU_CLOSE_PHYS_R1A`를 발급한다.

이번 구현은 하위 조건을 raw proofs로 기록하고 별도 R1A 최종 receipt에서 승격한다. 예약 하위 토큰을 실행 없이 개별 생성하지 않는다. 기존 parent packed receipt의 physical flag는 false다.

### 35. Rejection / HOLD

window 부재, synthetic completion, unknown coverage, ambiguous blocker, page mutation on reject, consumer 누락, completion 없이 release만 만족, live lease 조기 reclaim, stale binding 허용, telemetry-only reuse, 수치 drift는 모두 HOLD다.

실제 completion이 A4 전에 도착한 경우도 관측 미완료다. 그것을 조기 reclaim 버그가 관측된 것으로 과장하지 않는다.

### 36. Artifact policy

코드 ZIP에서 명세, audit manifest, 검사 로그, 생성된 receipt와 campaign manifest를 제외한다. 빌드에 필요한 Cargo metadata, 기존 fixture, 소스와 WGSL은 유지한다. 새 Python/PowerShell 로더는 없다.

### 37. Parent relationship

R1A는 F2 consumer-delay/reuse 축만 닫는다. MCU child construction identity, source-load witness, real producer replacement, full workload provenance 등 다른 PHYS-R1 미완결은 남긴다.

R1A PASS가 있어도 종합 `PASS_ASH_EVE_MCU_CLOSE_PHYS_R1`은 발급하지 않는다. 기존 CLI의 종합 HOLD/exit 2를 유지하고 R1A 결과는 별도 receipt로 식별한다.

### 38. Direct successor

```text
EVE-MCU-CLOSE-PHYS-R1B
MCU PERSISTENT-CHILD PHYSICAL IDENTITY
+ SUCCESSOR SOURCE-LOAD WITNESS
```

R1A에서 그 instrumentation이나 MIRASASH까지 확장하지 않는다.

### 39. Final law

> GPU completion 없는 release도, release 없는 GPU completion도 reclaim 근거가 아니다.
>
> negative admission은 arena를 변경하지 않는다.
>
> 같은 page의 새 사용자는 더 큰 incarnation을 가진다.
>
> 실제 Rust/WGPU 관측과 수치 검증이 없으면 physical HOLD를 유지한다.

## 부록 A. 실제 source bake

```text
Release: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Modified existing files: 10
Added files: 3 (Rust 2, WGSL 1)
Deleted files: 0
Unchanged files: 8392
New Python / PowerShell loader: 0
```

shared classifier, 두 actual shadow submission, scoped F2 selection, direct/deferred terminal hook, exact drain/release, free/stale witness, natural reuse 및 봉인된 same-domain reacquire, Leg A/F2 numerical comparison과 별도 promotion 경로를 소스에 반영했다.

consumer-set sealing은 shadow 추가 이후로 이동했다. historical lease는 계속 검증하지만 현재 consumer count에서 제외한다. 두 사항은 위 S1/S2 및 조항 14의 명시적 의미 변경이다.

실행한 검사:

```text
Existing parent static scripts: 16 / 16 PASS
R1A source-contract checks: 62 / 62 PASS
Changed/added Rust UTF-8 + lexical delimiters: 11 / 11 PASS
New Rust native tests: 24 added, NOT RUN
Cargo/rustc compile / borrow checking / linking: NOT RUN
WGSL/WGPU execution / numerical parity: NOT RUN
Physical PASS issued by this bake: none
```

기존 정적 검사기는 처음 15/16이 통과했다. R7A1 검사 1개가 base의 과거 문자열 위치를 기대해 실패했으며, shared backend classifier와 실제 base 호출을 함께 검사하도록 갱신한 뒤 16/16을 확인했다. 테스트 삭제나 주석 토큰으로 통과시키지 않았다.

Cargo/Rustc가 베이크 환경에 없으므로 컴파일 여부는 판단불가다. 부모 ZIP부터 없는 sherpa-rs path dependency와 일부 test include 입력을 가짜 crate/JSON으로 채우지 않았다. 독립 workspace 전체 빌드를 보장하지 않는다.

코드 전용 산출물:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1A_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: c1b136df5866b2d1fbf9e3be20085aead87ceb23caad1be3468621750187a207
Bytes: 21431002
Files: 8405
CRC: PASS
Duplicate paths: 0
Unicode paths with UTF-8 flag: 18
PowerShell files: 0
```

Cargo.toml/Cargo.lock과 두 영향 crate의 Cargo.toml은 부모와 같다. 기존 WGSL 계산은 변경하지 않고 read-only qualification WGSL만 추가했다. 명세/매니페스트/로그는 위 ZIP 외부에서 제공한다.

## 부록 B. Rust campaign 입력

기존 campaign JSON의 mode와 다음 필드를 사용한다. 다른 필수 입력/경로/budget은 기존 PHYS-R1 형식 그대로다. 별도의 shell 또는 Python loader는 없다.

```json
{
  "mode": "F2_CONSUMER_DELAY",
  "consumer_delay_r1a": {
    "shadow_dispatch_count": 256,
    "shadow_elements_per_dispatch": 256,
    "maximum_shadow_read_elements": 65536,
    "reuse_policy": "NaturalThenSameDomainReacquire"
  }
}
```

이는 전체 실행 config가 아닌 추가 필드 예다. profile admission을 자동으로 변경하지 않는다. 같은 campaign에서 관측 실패를 이유로 dispatch count를 늘리거나 다른 target을 골라 재시도하지 않는다.
