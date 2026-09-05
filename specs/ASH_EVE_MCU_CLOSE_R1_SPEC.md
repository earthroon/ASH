# ASH-EVE-MCU-CLOSE-R1

## Production Continuation + Terminal Lifecycle Closure

> 문서 구분: §0부터 부록 A까지는 합의된 구현 계약이다. 해당 부분의 SPECIFICATION ONLY 상태는 명세 작성 시점을 뜻한다. 실제 코드 베이크, 구현 방식의 명시적 변경, 검사 결과와 미검증 범위는 부록 B에 별도로 기록한다. 계약 요구사항을 실행 결과로 읽지 않는다.

### 0. Revision / 상태

```text
Patch ID: ASH-EVE-MCU-CLOSE-R1
Short name: EVE-MCU-CLOSE-R1
Status: SPECIFICATION ONLY / PROPOSED IMPLEMENTATION CONTRACT

Source materialization: NOT PERFORMED BY THIS SPECIFICATION
Static validation: NOT RUN FOR THIS REVISION
Rust compilation / native tests: NOT RUN FOR THIS REVISION
GPU physical qualification: HOLD
Repository commit: NOT PERFORMED
```

이 문서의 타입·필드·상태 전이·검사·산출물은 구현 요구사항이다. 기존 소스에 적용된 변경이나 검증 결과가 아니다. MIRASASH를 넣기 전에 기존 Eve / MCU 생산 세션의 수명 경계를 완결한다.

예약 토큰:

```text
PASS_ASH_EVE_MCU_CLOSE_R1_STATIC
PASS_ASH_EVE_MCU_CLOSE_R1_NATIVE
HOLD_ASH_EVE_MCU_CLOSE_R1_PHYSICAL_PENDING
```

앞의 두 토큰은 해당 검사 실행을 통과한 경우에만 생성한다. 종합 물리 승격은 후속 `EVE-MCU-CLOSE-PHYS-R1`의 실제 campaign 결과로만 가능하다.

### 1. 기준 소스와 근거

```text
Artifact:
ASH_PASS3_DK_SYN_R2A_CLOSED_LOOP_STABILITY_STATIC_SOURCE_BAKE_CODE_ONLY(1).zip

SHA-256:
2a5174cde27615aeb47f1e4df860de432f683025116b2451096ace4618db8935

Archive entries: 8,583
Non-directory files: 8,460
```

8,460개 전체를 전수 검증했다는 의미가 아니다. 기준은 첨부 본체와 `ASH_EVE_MCU_REVIEW_EVIDENCE.md`, `ASH_EVE_MCU_REVIEW_LOGS.zip`이다. 이전 리뷰의 GitHub 비교 커밋은 `d28ed995760dc6b5d7d444bed1870199ee48e5ed`이며, 이 문서 작성 시점의 최신 HEAD라는 주장은 하지 않는다.

이전 로그의 관련 정적 검사 결과는 13 PASS / 3 FAIL이다. 본 revision의 테스트 결과로 재사용하지 않는다. 기존 명세와 실제 소스가 다를 때 차이를 명시하고, 미구현 경로를 구현된 것으로 간주하지 않는다.

### 2. 완료할 주장

> 하나의 생산 `TrainableSessionRuntimeR4`가 승인된 실행 계획을 여러 invocation으로 나누어 실행한다. 동일한 Adam 본체, Eve authority, HiMuon runtime, MCU children을 유지하며, 마지막 승인 source와 cursor를 정확히 계승한다. 저장·commit·abort·retirement·해제가 끝난 실제 상태와 세션의 terminal 상태가 일치한다.

이 revision은 기존 R4B/R4C, MCU terminal closure, EVE 관측 연결 과제를 하나의 국소 구현 범위로 묶는다. 새 optimizer owner나 범용 scheduler를 만들지 않는다.

### 3. 유지할 parent / authority

```text
Eve mutable RAM M/V R3 + persistent authority R3G
R3G root guard + exact lease sequencer
Trainable Session R4 + sealed admission R4A
R3C / R3C1 full TrainableGeneration commit
R3B Adam target-to-RAM handoff
R3D / R3E / R3F durability and recovery, admitted R8A momentum references
MCU R7 / R7A / R7B / admitted R7A1
HiMuon R8 / R8A
EVE-PHYS-R1 observation surfaces
Existing generation recovery fence and restart policy
```

| 객체 / 결정 | 유지할 authority |
| --- | --- |
| Adam M/V, geometry, Adam 갱신 | 기존 Eve / RAM Adam owner |
| HiMuon momentum과 그 durability | 기존 HiMuon owner |
| physical submit, completion, arena, target, retirement | 기존 MCU owner |
| 전체 generation 승인과 rotation | 기존 R3C / R3C1 coordinator |
| invocation 계획, continuation, 세션 종료 | 기존 R4 owner |
| durability 완료 | 실제 기존 저장 경로의 완료 증거 |
| 관측과 종합 판정 | 읽기 전용 observer / 검증기 |

관측기는 commit·writeback·producer 생성·runtime 재구성 권한을 갖지 않는다.

### 4. 직접 닫을 결함

| ID | 기준 소스에서 확인한 상태 | 요구사항 |
| --- | --- | --- |
| C01 | `pipeline.rs`는 R4를 한 번 호출하고 final close한다. | 같은 production entry에서 봉인한 여러 invocation을 실행한다. |
| C02 | scheduler가 매 호출 `load_source(cfg)`를 실행한다. | 최초 bootstrap 이후에는 마지막 승인 `SourceState`를 move-restore한다. |
| C03 | 매 호출 output / `training_state` 신규 생성, 고정 이름 보고서 생성을 전제한다. | session canonical root와 invocation 보고서 범위를 분리한다. |
| C04 | resident 누적 실행량을 invocation budget과 직접 비교한다. | 세션 누적값과 invocation delta를 분리한다. |
| C05 | 마지막 invocation step이 곧 `final_writeback`이다. | invocation 경계, checkpoint, final close의 의도를 분리한다. |
| C06 | `mark_final_writeback()`이 계수를 1로 대입한다. | 실제 완료 receipt와 단일 finalization 전이로 증명한다. |
| C07 | MCU runtime 해제 후 final snapshot을 만든다. | live witness를 먼저 확보하고 실제 해제 후 종료를 확정한다. |
| C08 | production abort가 parent R7만 종료한다. | 안전한 정리 후 R7B와 parent R7을 함께 종료한다. |
| C09 | R7A cache 생성과 legacy producer 계수의 의미가 다르다. | 실제 acquisition 결과, session adoption, instance continuity를 분리한다. |
| C10 | N8의 고정 8-step 조건 / 최종 보고서를 invocation 단위로 평가한다. | 원래 workload 조건을 유지하며 세션 집계에서 평가한다. |

C01~C09는 이전 리뷰 E1~E5와 연결된다. C10은 기준 scheduler의 budget 검사, N8 finalization, step receipt 집계에서 추가 확인한 직접 연관 범위다. 새로운 성능 기능을 뜻하지 않는다.

### 5. Admission / 실행 계획

제안하는 설정 필드는 기존 `BaseTrainingRuntimeConfig`에만 추가한다.

```text
admit_eve_mcu_close_r1: bool                 default false
eve_mcu_close_r1_invocations: Vec<...>       default empty
```

계획 항목은 기존 exit enum을 재사용한다. 아래는 추가할 타입의 계약이며 적용된 코드가 아니다.

```rust
pub struct TrainableInvocationPlanEntryCloseR1 {
    pub optimizer_steps: u32,
    pub exit: TrainableInvocationExitR4,
}
```

Active admission에는 기존 R4 active owner / cross-invocation, R4A sealed profile / hotpath retirement, Eve R3G, resident Adam / Weight, ProductionMuon, MCU R7 및 R7B child extraction / generation ownership, R3C / R3C1과 그 필수 parent가 필요하다. R7A / R7A1 / R8A 및 durability 조합은 실제 선택된 admission을 유지한다. 새 flag 때문에 parent를 자동으로 켜거나 끄지 않는다.

계획 검사는 세션 bootstrap 전에 수행한다.

```text
admission false + nonempty plan            => REJECT
admission true  + empty plan               => REJECT
각 invocation.optimizer_steps >= 2         => REQUIRED
checked_sum(invocation.optimizer_steps)
    == cfg.training.production_loop_optimizer_steps
마지막 항목.exit == CloseAfterDurableWriteback
그 외 항목.exit == KeepResident 또는 DurableCheckpointKeepResident
final-close 항목 수 == 1
```

원래 R6의 invocation 최소 2-step 조건을 유지한다. 1-step 호출이나 partial accumulation park를 새로 지원하지 않는다. 단일 항목 계획도 구현상 허용하지만 cross-invocation 물리 증명은 아니다.

**의미 변경 S1:** `production_loop_optimizer_steps`는 기존 전체 실행량을 유지한다. Active 계획에서는 이를 각 invocation에 반복 적용하지 않고 합계 예산으로 소비한다. cfg를 4, 4 등으로 수정하거나 R4A를 재봉인하지 않는다.

제안 설정 예:

```toml
[training]
admit_eve_mcu_close_r1 = true
production_loop_optimizer_steps = 8

[[training.eve_mcu_close_r1_invocations]]
optimizer_steps = 4
exit = "KEEP_RESIDENT"

[[training.eve_mcu_close_r1_invocations]]
optimizer_steps = 4
exit = "CLOSE_AFTER_DURABLE_WRITEBACK"
```

이 예에는 기존 필수 parent 설정을 생략했다. 단독 실행 가능한 전체 config라는 뜻이 아니다.

### 6. R4A 봉인과 bootstrap

R4A의 기존 `training / optimizer / backend` raw config digest를 유지한다. 추가 계획과 admission은 그 봉인에 포함한다. 별도 mutable config 사본을 실행 authority로 만들지 않는다.

세션 owner는 확정된 계획, 다음 invocation ordinal, session output identity, 초기 source identity와 scheduler profile identity를 보관한다. `checkpoints.output_dir`는 기존 raw digest의 대상이 아니므로 session output identity로 별도 고정한다. 기존 raw digest의 의미를 몰래 바꾸지 않는다.

최초 bootstrap에서만 authoritative source load, scheduler profile load / 승인된 horizon extension, dataset 준비와 최초 resident materialization을 수행한다. 기존 초기 source preflight는 유지한다. `r6_required_batch_count`가 읽는 초기 cursor도 같은 검증된 bootstrap identity에 연결하며, 후속 invocation에서는 초기 source preflight를 다시 실행하지 않는다.

다음 값은 호출 중 변경할 수 없다.

```text
execution plan / policy seal
model / tokenizer / dataset lineage
scheduler profile / admitted horizon
Device / Queue authority
session root / initial durable parent identity
optimizer routing and admitted execution modes
```

후속 호출에 새 RAM inventory seed를 공급하거나 dataset owner를 다시 만들면 거부한다. 같은 pipeline이 준비한 batch owner와 reservation을 유지한다.

같은 invocation API를 사용하되 실제 budget과 ordinal은 R4가 봉인된 계획에서 발급한다. caller의 exit와 현재 계획 항목이 다르면 실행 전에 거부한다. 반복 호출용 별도 optimizer executor를 만들지 않는다.

### 7. SourceState와 continuation 소유권

기존 `SourceState`는 이름과 필드를 유지한다. scheduler 밖으로 이동 소유할 수 있도록 필요한 최소 crate visibility 또는 접근자만 추가한다. 독립적인 두 번째 source record를 도입하지 않는다.

```text
TrainableSessionRuntimeR4
  └─ parked / active continuation
       ├─ 기존 SourceState
       ├─ 봉인된 scheduler profile / 초기 parent binding
       ├─ invocation 시작 계수 / 세션 집계
       ├─ 기존 RAM budget / reservation / Weight / Adam
       ├─ 기존 ProductionMuonRuntime / MCU / HiMuon
       └─ 기존 Eve root guard / lease sequencer
```

`SourceState`의 generation·optimizer step·cursor만 복사해서 계승하지 않는다. records, parent training-state digest, candidate manifest, packed slot / source kind, scheduler state, durability descriptor binding을 포함한 전체 승인 source를 move한다.

```text
첫 invocation:
    initial durable source -> bootstrap -> 실행 -> 승인된 successor source

KeepResident / checkpoint-keep:
    승인 source + live runtime을 함께 park

후속 invocation:
    함께 restore -> identity 대조 -> 다음 승인 generation 실행
```

**의미 변경 S2:** in-process continuation의 source authority는 살아 있는 R4 세션이다. 새 프로세스 durable resume는 기존 loader / recovery 경로다. 둘을 하나의 fallback으로 취급하지 않는다.

ordinal이 2 이상인데 continuation이 없으면 오류다. body만 있고 source가 없거나 그 반대여도 오류다. 초기 source를 다시 읽어 상태를 맞추지 않는다.

successor source는 기존 전체 commit 성공에만 연결한다. commit 후 `build_source_after_commit`이나 evidence 작성이 실패하면 commit 이전 상태로 돌아간 것으로 표시하지 않고 기존 recovery fence를 적용한다. 기존 no-fail tail 안에 새로운 fallible source 작업을 넣지 않는다.

### 8. Invocation delta / scheduler / N8 집계

세션 누적 계수는 호출 사이에 유지한다. invocation 시작 시 해당 계수의 기준값을 읽고 종료 시 checked subtraction으로 delta를 만든다.

```text
invocation_optimizer_steps = end_steps.checked_sub(begin_steps)
invocation_optimizer_steps == admitted_invocation_budget

final_training_generation == opened_training_generation + budget
final_optimizer_generation == opened_optimizer_generation + budget
final_cursor.next_batch_ordinal == opened_cursor.next_batch_ordinal + budget * 8
```

곱셈·덧셈·차감은 overflow / underflow를 오류로 처리한다. identity / count 오류를 `saturating_*`, 0 초기화, `unwrap_or(0)`로 정상값처럼 만들지 않는다. 기존 보조 통계 전체를 무관하게 리팩터하는 것은 범위 밖이다.

learning-rate scheduler는 기존 optimizer commit clock을 유지한다. invocation ordinal을 scheduler step으로 사용하지 않는다. invocation 마지막 step이라는 이유로 warmup이나 schedule phase를 다시 시작하지 않는다.

**의미 변경 S3:** N8의 총 8-step 조건과 source / horizon parent 조건은 session workload에 적용한다. 4+4의 각 호출을 별도 N8 8-step 실행으로 평가하지 않는다. N8·R6 fixed-name 최종 보고서는 누적 step ledger를 이용해 세션 종료에서 한 번 작성한다. 반복 호출마다 전체 실험의 PASS / HOLD를 출력하지 않는다.

`r6a_disk_steps`, sync 관측, R14 lane records, phase timing 등 최종 집계에 필요한 기존 metadata를 계획의 전체 step 수 이내로 유지한다. GPU tensor나 gradient 사본을 집계용으로 보관하지 않는다. invocation snapshot으로 세션 budget을 finalize하지 않는다.

`N8RamResumeCutRole::CutLeg1 / CutLeg2`의 fresh-process 계약은 변경하지 않는다. 이 revision의 same-process plan과 해당 cut-leg 조합은 명시적으로 거부하며 legacy 실행은 유지한다. Continuous 조건을 사용할 때는 동일한 parent와 전체 예산을 검사한다.

### 9. 출력 경로와 staging

Active 계획의 논리적 배치는 다음과 같다.

```text
session output root                        최초 1회 create-new
  training_state/                          기존 canonical state / slot / head
  production_step_<global_step>_receipt.json
  invocations/
    000001/                                호출별 고정 이름 진단 보고서
    000002/
  trainable_session_invocation_r4_<ordinal>.json
  eve_phys_r1_invocation_<ordinal>_open.json
  eve_phys_r1_invocation_<ordinal>_close.json
  eve_phys_r1_invocation_<ordinal>.json
  <기존 session-final 보고서 파일명>
```

canonical run root, recovery root, root guard는 invocation 보고서 디렉터리로 이동하지 않는다. 기존 `output`이 뜻하던 canonical 경로와 보고서 경로를 필요한 callsite에서 구분한다. 경로를 일괄 치환하지 않는다.

후속 호출은 이미 존재하는 자신의 root를 검증해서 재사용한다. 신규 session은 기존 root를 무조건 수용하지 않는다. invocation 디렉터리의 충돌, 외부 session의 root, active state binding 불일치는 거부한다.

generation slot과 active head의 기존 원자적 갱신은 허용한다. 허용된 canonical head rotation과 보고서 덮어쓰기를 구분한다. committed / recovery-preserved 경로는 invocation 오류의 staging cleanup 대상이 아니다.

기존 단일 invocation legacy 모드의 파일명과 출력 규칙은 유지한다. `_patch` 등 별도 소스 파일명을 만들지 않는다.

### 10. 저장 의도와 기존 durability 경로

step마다 다음 결정을 별개로 구한다.

```text
is_invocation_last_step
is_session_final_step
explicit_checkpoint_boundary
scheduled_recovery_cadence_due
```

| exit / 원인 | 최종 step에서 요구하는 동작 | 최종 종료 증거 |
| --- | --- | --- |
| KeepResident | 종료 때문에 강제 저장하지 않는다. 기존 cadence는 유지한다. | 없음 |
| DurableCheckpointKeepResident | 해당 committed generation을 복구할 수 있는 명시적 checkpoint를 완료한다. | 중간 checkpoint 증거만 |
| CloseAfterDurableWriteback | 해당 final committed generation의 durability를 완료한다. | FinalClose 완료 증거 |
| ScheduledCadence | 원래 cadence clock / 규칙대로 기록한다. | 그 자체로 session final-close 아님 |

**의미 변경 S4:** invocation 마지막 step과 final writeback을 분리한다. `KeepResident`를 모든 I/O 금지로 확대하지 않는다.

R3D의 `ScheduledCadence / ExplicitCheckpoint / FinalWriteback` 등 기존 reason을 재사용한다. 같은 target generation에서 cadence와 명시적 경계가 겹치면 준비·기록을 중복 수행하지 않고 실제 하나의 완료에 원인들을 귀속시킨다. final-close 원인을 cadence만으로 대체하지 않는다.

legacy packed writeback, R3D Adam anchor, R3E Weight journal / keyframe, R3F / R8A momentum durability는 기존 구현을 사용한다. 활성 경로에 필요한 컴포넌트가 빠진 checkpoint는 완료가 아니다. R3D를 꺼서 legacy 계수를 맞추거나, 기존 anchor를 dummy writeback으로 대체하지 않는다.

기존 candidate 데이터의 durable preparation이 commit 이전에 일어나는 것은 허용한다. 그러나 그 target이 전체 commit으로 승인되고 정확한 head / descriptor publication이 완료되기 전에는 checkpoint / final-close 완료로 채택하지 않는다. 관측기를 위해 optimizer update를 추가로 수행하지 않는다.

### 11. Final durability 완료 계약

final completion은 파일 개수나 I/O syscall 개수가 아니라 session finalization의 단일 완료 사건이다. 실제 파일 bytes / sync / component write 횟수는 기존 I/O 증거에 계속 별도로 기록한다.

제안 상태:

```text
NotRequested
    -> Requested(session, invocation, exact target)
    -> Prepared(existing durability path)
    -> PublishedAndVerified(existing receipts, committed target)
    -> ConsumedByClose
```

실패는 완료로 전이하지 않는다. 이미 완료한 finalization을 다시 실행하려는 요청은 명시적으로 거부한다. 중간 checkpoint는 이 상태의 final 완료 횟수를 소비하지 않는다.

최종 증거는 최소한 다음을 연결한다.

```text
session / invocation identity
final TrainableGeneration seal and cursor digest
training generation / optimizer generation
actual durability path and reason
actual component receipt / manifest / descriptor digests
published recovery head or canonical durable binding
existing verification result
finalization ordinal / completion count
```

현재 target과 동일한 generation을 복구할 수 있어야 한다. 이전 anchor만 있고 target까지의 검증된 replay 경로도 없는 상태는 final 완료가 아니다. 기존 descriptor의 `exact_target_restart_eligible` 등 필드를 증거 없이 true로 바꾸지 않는다.

**의미 변경 S5:** 기존 `final_m_writeback_count / final_v_writeback_count = 1`을 모든 경로의 완료 authority로 사용하지 않는다. legacy 실제 계수는 원래 의미대로 유지하고, 새로운 finalization 완료 의미는 새 evidence schema에 표시한다. M만 완료되었거나 V만 완료된 상태를 부분 성공으로 승격하지 않는다.

정상적인 하나의 세션에서 final completion은 한 번이다. 프로세스 crash를 가로지르는 전역 exactly-once 저장을 새로 보장한다는 뜻은 아니다.

I/O는 실제 phase와 reason을 함께 기록한다. step 중 발생한 cadence write를 명목상 checkpoint로 분류한 것만으로 “per-step I/O 0”이라고 주장하지 않는다. 기존 수치와 의미가 달라지는 통계는 schema 차이를 명시한다.

### 12. R7B commit / retirement 종료

성공 commit은 기존 R3C1 authority와 no-fail tail을 유지한다.

```text
prepare에서 fallible 검사 완료
    -> 기존 전체 commit permit
    -> 기존 Adam / Muon / Weight rotation
    -> 이전 device source를 bounded retirement slot에 보관
    -> 기존 completion / reader 조건 확인
    -> post-commit retirement
    -> generation-local identity / handoff / union 정리
```

no-fail tail에 새 GPU wait, 파일 I/O, pipeline 생성, buffer allocation, 실패 가능한 cleanup을 넣지 않는다. 필요 계수 overflow 검사도 가능하면 prepare에서 완료하고 no-fail 단계는 준비된 값을 설치한다.

R7B의 outer phase가 Open이라는 이유만으로 다음 generation을 허용하지 않는다. physical generation과 retirement slot도 완료 조건을 만족해야 한다.

KeepResident / checkpoint-keep 경계의 필수 조건:

```text
R7 parent active generation: none
R7B physical generation identity: none
Muon target / Adam scheduler / Adam target / full target: none
live generation handoff / exact submission union: none
post-commit retired source slots: empty
pending admitted work / source-reader dependency: terminal-safe
R7B session phase: Open
```

committed device source, persistent children, admitted cache handles, HiMuon momentum, Eve 본체는 유지한다. target을 비웠다는 이유로 committed source까지 지우지 않는다.

### 13. R7B abort 종료

abort는 기존 실패 stage와 commit 경계를 먼저 판별한다.

```text
commit 전 실패
    -> 기존 pending queue / scheduler terminal drain
    -> 정확한 completion과 reader / consumer lease 확인
    -> 안전한 uncommitted target 해제
    -> R7B generation terminal 정리
    -> parent R7 generation terminal 정리
    -> 기존 abort / recovery receipt 기록
```

기존 `mark_abort_no_fail()`을 production abort에 연결하되, 준비 검사가 성공한 이후에만 호출한다. identity를 먼저 지워 남은 작업이 없는 것처럼 만들지 않는다. 이미 인계한 자원이 해제 실패로 소유권 추적에서 사라지는 `take`-후-오류 경로도 막는다.

R7A1 exact multi-consumer 계약을 유지한다. generation 숫자 일치나 임의 wait 하나가 아니라 실제 필요한 SubmissionEpoch 집합과 마지막 consumer 완료로 재사용을 허용한다.

**의미 변경 S6:** abort 성공 시 R7B와 parent R7의 terminal state를 함께 정리한다. 이것이 상위 recovery policy의 변경을 뜻하지 않는다. 기존 fence가 `FreshRestartFromPreviousSource` 등을 요구하면 outer R4는 재실행을 거부한다. R7B 내부 Open만 보고 다음 invocation을 시작하지 않는다.

commit 이후의 실패에는 pre-commit abort를 적용하지 않는다. 이미 승인된 source를 되돌리거나 old source를 다시 current로 표시하지 않는다. 이전 generation으로의 resume 여부는 기존 last-durable seal / recovery fence가 결정한다.

### 14. 오류 시 소유권 / 세션 상태

| 실패 시점 | 필수 동작 |
| --- | --- |
| begin 이전 admission 오류 | 실행·materialization 없이 요청 거부 |
| begin 이후, commit 이전 | 기존 abort / recovery 계약 수행, 재실행 가능 여부는 fence에 따름 |
| pending drain / target release 실패 | 자원 추적을 유지하고 Poisoned, 정상 park / 재사용 금지 |
| commit 이후 source binding / retirement 실패 | committed 상태를 보존하고 기존 recovery fence 적용 |
| final durability 준비 / publication 실패 | normal Closed 금지, final completion 없음 |
| durability 완료 후 release 실패 | 완료된 저장을 재실행하지 않고 release 미완료 / Poisoned를 기록 |
| release와 Closed 확정 후 관측 파일 기록 실패 | Closed는 유지, evidence publication failure를 반환하고 물리 승격은 HOLD |

모든 일반 `Result` 오류 경로가 terminal 처리를 거치도록 invocation 경계에서 수렴시킨다. local variable의 우연한 drop이나 `?` 반환만으로 cleanup 완료라고 기록하지 않는다.

미해제 자원은 기존 R4 / MCU 또는 그 scope guard의 단일 owner가 안전한 종료까지 유지한다. mutable owner를 이중으로 만들거나 참조 계수만 추가해 누락을 숨기지 않는다. 파괴자에서는 새 GPU campaign이나 실패 가능한 저장을 시작하지 않는다.

panic, OOM, process kill, device loss 이후의 정상 same-process continuation은 이 revision의 보장 대상이 아니다. 해당 실패를 정상 close receipt로 표시하지 않는다.

### 15. 최종 close 순서

최종 invocation의 정상 종료 순서를 다음으로 고정한다.

```text
1. final committed source / generation 확인
2. 그 generation의 final durability 완료 검증
3. pending work / generation-local target / retirement 정리 완료 확인
4. 살아 있는 Adam / Eve / HiMuon / MCU에서 close witness 확보
5. 필요하면 pre-release witness를 기록, 아직 final PASS는 아님
6. session-owned runtime / reservations / root guard 해제
7. 해제 결과와 finalization consumption 확인
8. R4 Closed 확정
9. final closure evidence publication
```

**의미 변경 S7:** live witness는 release보다 먼저, terminal receipt는 release와 Closed보다 나중이다.

witness에는 Adam M/V allocation 집합, Eve identity, guard identity, lease sequence, MCU session / 실제 child lineage, 실제 producer binding, current generation, R7B terminal 상태와 durability binding을 포함한다. witness는 metadata만 가진다. 큰 tensor 복제나 observer 전용 producer 생성은 금지한다.

`complete_invocation(..., None)`만으로 Closed가 되지 않도록 final durability와 release 완료를 소비하는 gate를 추가한다. `close_already_durable()`도 같은 완료 근거가 없는 active closure에서 검사를 생략하지 못하게 한다. 이미 Closed인 객체에 대한 읽기 전용 상태 확인은 허용하지만 writeback을 재실행하지 않는다.

keep 경계는 terminal-safe 확인 -> live boundary snapshot -> continuation park -> Open 순서다. budget authority의 finalize / reservation release / final-writeback 출력은 수행하지 않고 필요한 snapshot만 만든다.

### 16. Producer / cache 관측

R7A cache는 DeviceAuthority 수명이고 legacy producer는 세션 수명이다. 서로 다른 생성 계수를 하나로 취급하지 않는다.

실제 `KernelBuildCellR7A::get_or_build()`에는 `built_now`가 이미 존재한다. 그 실제 acquisition 결과를 읽기 전용 증거로 전달한다. 공유 cache의 전역 계수 차이만으로 특정 세션의 생성을 추정하지 않는다.

필수 관측 구분:

```text
physical build: 이번 정확한 key acquisition에서 실제 생성했는가
session adoption: 이 세션이 해당 producer를 최초 채택했는가
session reuse: 후속 사용이 같은 live producer instance인가
```

| 조건 | 판정 |
| --- | --- |
| Cold R7A key, 실제 build | build 증거와 session adoption 기록 |
| 이미 준비된 동일 device / key | built_now=false 허용, session adoption은 실제 기록 |
| 같은 세션의 후속 invocation | 동일 key / DeviceAuthority / producer instance 유지 |
| 유효성 실패 또는 cache 취득 실패 | 오류, legacy 재생성으로 대체 금지 |
| 최초 open이며 producer 미사용 | NotAcquired 허용 |
| 최종 evidence인데 producer 미사용 | 해당 Adam submission / persistence 물리 주장 불가 |

**의미 변경 S8:** 모든 세션에 `physical build count == 1`을 요구하지 않는다. 실제 사용한 producer의 adoption 1회, 이후 replacement 0회와 기존 lease / submission 증거를 요구한다. 정상적인 warm cache를 실패로 처리하지 않는다.

같은 cache key만으로 같은 instance라고 단정하지 않는다. 실제 Arc 대상 identity 또는 생성 시 부여된 살아 있는 instance identity를 사용한다. park / restore는 Rust struct의 주소를 바꿀 수 있으므로 MCU struct 주소 자체를 persistence 조건으로 쓰지 않는다.

session close는 session 참조를 해제한다. 다른 세션도 사용할 수 있는 device-lifetime cache 전체를 retire하거나 `Arc::strong_count == 0`을 요구하지 않는다. 수명 주체가 다른 자원을 같은 release 계수에 섞지 않는다.

### 17. 관측 schema / 토큰 호환성

기존 observer 파일과 boundary 파일명을 유지한다. 새 판정은 다음 schema로 식별한다.

```text
closure_schema: ash.eve_mcu.close.r1
closure_revision: ASH-EVE-MCU-CLOSE-R1
```

Active 경로의 final receipt는 기존 `eve_phys_r1_cross_invocation_physical_receipt.json` 파일명을 사용할 수 있지만, 새 closure schema / producer / durability 판정을 포함해야 한다. 구 reader가 이를 옛 R1 판정으로 해석하도록 예전 PASS 토큰을 넣지 않는다. Legacy mode의 기존 schema와 token 의미는 유지한다.

최소 evidence 범위:

| 범위 | 필요한 정보 |
| --- | --- |
| Session | plan digest, admission seal, initial source / output identity, 실제 사용 mode |
| Invocation | ordinal, budget, exit, opened / final generation, cursor / scheduler digest, delta |
| Continuation | close -> successor-open source / body / guard / lease / MCU identity 연결 |
| Durability | 실제 완료 binding, reason, component coverage, finalization state |
| MCU terminal | commit 또는 abort, exact completion, target / union / retirement 상태 |
| Producer | key / device / instance, 실제 build outcome, adoption / reuse |
| Close | live witness, release 완료, terminal phase, publication 결과 |

현재 pipeline의 의도적인 parent HOLD 출력 / 반환을 일반 실행 오류와 구분한다. 기존 physical gate를 삭제하지 않고 실제 workload / close 완료 evidence와 qualification 상태를 별도로 기록한다. 알려진 HOLD라는 이유만으로 다른 오류까지 성공으로 처리하지 않는다.

`physical_pass_claimed`는 static bake에서 false다. synthetic JSON, 단위 테스트의 가짜 counters, 정적 문자열 검사만으로 physical PASS를 만들지 않는다. 실제 constructor / hydration / publication / acquire / release 지점에서 계수를 기록하며 cfg의 true를 횟수 1의 근거로 쓰지 않는다.

source tree / executable hashing 같은 provenance 준비는 기존 bootstrap 또는 외부 검사 경계에 둔다. 매 invocation observer에서 전체 tree·Adam tensor를 스캔하지 않는다. 기존 필요한 durability 검증 I/O와 observer의 metadata 관측을 구분한다.

### 18. 오류 코드 계약

새 경계에서 최소한 다음 오류를 구별한다. 기존 더 구체적인 오류는 cause로 보존한다.

```text
E_EVE_MCU_CLOSE_R1_PLAN_INVALID
E_EVE_MCU_CLOSE_R1_PLAN_BUDGET_DRIFT
E_EVE_MCU_CLOSE_R1_ADMISSION_DRIFT
E_EVE_MCU_CLOSE_R1_CONTINUATION_MISSING
E_EVE_MCU_CLOSE_R1_SOURCE_IDENTITY_DRIFT
E_EVE_MCU_CLOSE_R1_OUTPUT_IDENTITY_DRIFT
E_EVE_MCU_CLOSE_R1_INVOCATION_COUNTER_DRIFT
E_EVE_MCU_CLOSE_R1_PARTIAL_ACCUMULATION_AT_BOUNDARY
E_EVE_MCU_CLOSE_R1_DURABILITY_TARGET_DRIFT
E_EVE_MCU_CLOSE_R1_FINALIZATION_ALREADY_CONSUMED
E_EVE_MCU_CLOSE_R1_MCU_NOT_TERMINAL_SAFE
E_EVE_MCU_CLOSE_R1_ABORT_CLEANUP_INCOMPLETE
E_EVE_MCU_CLOSE_R1_RECOVERY_FENCE_ACTIVE
E_EVE_MCU_CLOSE_R1_PRODUCER_IDENTITY_DRIFT
E_EVE_MCU_CLOSE_R1_RELEASE_INCOMPLETE
E_EVE_MCU_CLOSE_R1_EVIDENCE_PUBLICATION_FAILED
```

반환 오류와 실제 마지막 committed / durable / released 상태를 함께 보존한다. 오류 로그를 썼다는 사실은 해당 cleanup이 성공했다는 증거가 아니다.

### 19. 변경 파일 범위

| 기존 파일 | 변경 내용 |
| --- | --- |
| `crates/base_train/src/config.rs` | default-OFF admission과 explicit invocation plan |
| `crates/base_train/src/pipeline.rs` | 한 source / batch / session에서 계획 실행, seed 최초 전달, terminal 결과 전달 |
| `crates/base_train/src/trainable_session_active_production_owner_r4.rs` | continuation, plan consumption, delta, close / failure gate |
| `crates/base_train/src/trainable_session_admission_profile_r4a.rs` | 계획 admission / 봉인 연결 |
| `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs` | source restore, root 분리, budget scope, N8 집계, 저장 의도, close 순서 |
| `crates/base_train/src/ram_resident_adam_mv.rs` | 실제 writeback 완료 연결, legacy 계수 의미 보존 |
| `crates/base_train/src/eve_persistent_adam_cross_invocation_physical_seal_r1.rs` | live witness, 새 판정 schema, terminal receipt |
| `crates/base_train/src/mcu_session_runtime_r7.rs` | 실제 producer acquisition / adoption 증거 노출 |
| `crates/base_train/src/mcu_session_runtime_r7b.rs` | abort / commit / retirement terminal 검사 및 연결 |
| `crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs` | 생산 abort와 final witness / terminal 결과 연결 |
| `crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs` | 기존 build cell의 실제 acquisition outcome 노출 |

R3D/R3F 등 기존 durability helper의 최소 signature / reason 전달 변경은 허용한다. 파일을 교체하거나 새 저장 엔진을 만들지 않는다. 필요한 기존 export / CLI / config literal callsite 보완도 적용한 실제 변경 목록에 명시한다. 무관한 전역 포맷 변경은 제외한다.

추가 산출물 제안:

```text
specs/ASH_EVE_MCU_CLOSE_R1_SPEC.md
tools/validate_ash_eve_mcu_close_r1_static.py
```

native 상태 전이 테스트는 가능하면 기존 모듈의 `#[cfg(test)]` 영역을 사용한다. 새로운 GPU 훈련 실행기는 만들지 않는다. 신규 Rust 분기는 `match`와 typed enum을 우선한다.

### 20. 정적 / native acceptance

각 행은 실행해야 할 검사 요구사항이며 PASS 결과가 아니다.

| ID | 검사 | 기대 결과 |
| --- | --- | --- |
| A01 | Disabled + empty plan | 기존 one-shot 정책 유지 |
| A02 | Active + empty / 1-step / 합계 불일치 / 비최종 Close | admission 거부 |
| A03 | plan / optimizer / device / root drift | 실행 전 거부 |
| A04 | 2회차에 source 또는 body 누락 | 재수화 없이 오류 |
| A05 | 4+4와 2+2+4의 metadata progression | source / cursor / scheduler 연속 |
| A06 | invocation 누적값 mismatch / underflow | 명시 오류, 초기화 없음 |
| A07 | 전체 N8=8, 부분 호출=4 | N8 최종 판정은 전체 집계에서 1회 |
| A08 | 후속 호출 고정 이름 보고서 생성 | 자신의 invocation 범위 사용, canonical root 유지 |
| A09 | KeepResident + cadence 미도래 / 도래 | 강제 final 없음, 실제 cadence 유지 |
| A10 | checkpoint-keep | 해당 generation durable, body와 reservation 유지 |
| A11 | final-close 중 M/V 또는 component 누락 | Closed / 완료 토큰 거부 |
| A12 | final-close 재진입 | 중복 writeback 없이 명시 오류 |
| A13 | 마지막 update의 prepared anchor, commit 실패 | final durability로 채택하지 않음 |
| A14 | 정상 generation commit / retirement | 다음 경계에서 generation-local state 없음 |
| A15 | pre-commit abort, cleanup 성공 | R7B와 R7 모두 terminal, recovery fence 유지 |
| A16 | pending consumer / drain / release 실패 | 조기 arena 재사용 없음, Poisoned |
| A17 | commit 후 실패 | pre-commit abort 금지, committed state 보존 |
| A18 | live snapshot / release / Closed 순서 | use-after-release 관측·조기 Closed 없음 |
| A19 | Cold / warm / reused producer | 실제 acquisition 판정, identity replacement 거부 |
| A20 | 초기 producer 미취득 | NotAcquired 허용, 최초 사용 이후 정확히 연결 |
| A21 | 다른 cache 사용자 존재 | 전역 계수 오염 없이 해당 acquisition 귀속 |
| A22 | final receipt 쓰기 실패 | 실제 Closed 유지, physical promotion 없음 |
| A23 | staging cleanup | 이전 committed / recovery-preserved path 보존 |
| A24 | 새 schema / 구 reader | 옛 PASS로 오인하지 않음 |
| A25 | partial accumulation / active lease park | 경계 거부 |
| A26 | 기존 source / commit / N8 / R4A 회귀 | parent 계약 변경 없음 |

새 정적 검사는 실제 owning field와 생산 호출부를 확인한다. 주석의 옛 필드 문자열만으로 통과시키지 않는다.

이전 R3A / R3B / R7A1 검사의 stale field / profile 경로는 현재 successor ownership에 맞게 고친다. 검사 완화를 기능 수정으로 보고하지 않고, 각각 production callsite 연결과 native 검사를 함께 둔다.

native compilation과 CPU 상태 전이 테스트는 GPU 물리 검증이 아니다. 정확한 실행 명령, source revision, build profile, exit code, 실행 / 제외 test inventory를 보존한다. 실제로 실행하지 않은 test를 PASS 수에 넣지 않는다.

### 21. 후속 physical qualification

`EVE-MCU-CLOSE-PHYS-R1`에서 동일 production entry, 동일 모델 / 초기 상태 / dataset / optimizer schedule로 비교한다.

```text
8 step one-shot
4 step KeepResident + 4 step FinalClose
2 step KeepResident + 2 step DurableCheckpointKeepResident + 4 step FinalClose
```

이는 제안 campaign이며 실행 결과가 아니다. split은 같은 프로세스 / 같은 세션이다. 초기 source, 입력 순서, 활성 경로와 RNG 상태 등 수치 영향 조건을 맞춘다. GPU 결과에 사용할 수치 허용 오차는 현재 자료만으로 판단불가이며 실험 전에 명시한다. identity / cursor / generation은 exact 비교다.

정상 연속성 외에 target 생성 후 commit 전 실패, consumer 완료 지연, final durability 실패, final receipt publication 실패를 실제 경로에서 검증한다. mock state-machine 결과만으로 GPU release / completion을 주장하지 않는다.

최소 판정:

```text
실제 Adam hydration / Eve publication / ProductionMuon construction: 각 1
실제 최초 HiMuon load / MCU session open: 각 1
successor source reload / runtime reconstruction: 0
lease reuse: 0
source submit count == unique lease count, 실제 submit > 0
Adam live allocation 집합: 호출 경계에서 동일, 기존 A/B 역할 교환 허용
producer session adoption: 1, replacement: 0
safe boundary active generation-local state: 0
final durability completion: 1
session-owned release: 완료
normal campaign poisoned count: 0
```

실패 campaign은 정상 학습 PASS와 분리한다. R7A / R7B / R7A1 등 대상 경로를 끈 실행은 그 기능의 승격 근거가 아니다. 필요한 physical 증거가 없으면 HOLD를 유지한다.

### 22. Bake 완료 정의

다음의 상태를 따로 보고한다.

| 단계 | 완료 기준 |
| --- | --- |
| Source bake | C01~C10 구현과 실제 파일 delta 제공 |
| Static | 새 검사와 명시된 parent 회귀의 실제 실행 결과 |
| Native | 영향 crate compile / 지정 native tests의 실제 성공 |
| Physical | 후속 production campaign의 실제 결과 |

정적 검사만 통과한 ZIP은 `STATIC SOURCE MATERIALIZATION`까지만 주장한다. Cargo가 없거나 실행하지 못했으면 native 항목은 NOT RUN / 판단불가이며 성공으로 간주하지 않는다. native PASS라도 physical HOLD는 자동으로 해제되지 않는다.

권장 구현 순서는 plan / bootstrap / continuation, delta / report scope, durability 의도 / 완료 연결, MCU terminal 처리, live witness / producer evidence, 검사의 순서다. 해당 순서가 별도 여섯 개 대형 revision을 새로 만들라는 뜻은 아니다.

### 23. 명시적 비목표

MIRASASH memory tensor, ΔK memory policy, erase / tier promotion, memory 전용 MCU admission은 포함하지 않는다. workspace 전체 Adam-family / LoRA Adam 통합도 포함하지 않는다.

Adam / HiMuon 수학, optimizer routing, R3C1 semantic commit authority, WGSL / CUDA kernel 계산, vendor version / Cargo.lock, multi-device / tensor-parallel optimizer 범위를 바꾸지 않는다.

프로세스 재시작 후 live allocation 유지, 임의 실패의 same-process retry, bitwise GPU determinism, 처리량 개선을 이 명세만으로 보장하지 않는다.

### 24. 최종 법칙

> 보관한 Adam 본체와 그 본체가 승인한 source는 함께 다음 호출로 넘어간다.
>
> 호출을 나눈 사실은 학습 clock과 최종 저장의 의미를 바꾸지 않는다.
>
> commit은 기존 authority가 결정하고, MCU는 승인된 실행과 정확한 terminal cleanup을 담당한다.
>
> 살아 있을 때 관측하고, 실제로 해제한 뒤 닫는다.
>
> 완료된 저장, 완료된 해제, 완료된 증거 발행은 서로 다른 결과다. 어느 하나를 다른 하나의 성공으로 대신하지 않는다.

### 부록 A. 기준 소스 식별

아래 hash와 줄 범위는 입력 ZIP의 실제 파일 기준이다. 후속 bake의 hash가 아니다.

**`crates/base_train/src/pipeline.rs`**

```text
lines: 640–755
sha256: 90d839803a907fe944a7a16794cedad10135b63810a5723a3ee7dbaa091fede5
```

**`crates/base_train/src/config.rs`**

```text
lines: 1223–1585
sha256: e5ababba64646fb51ee9cf6d60dcddda29278edbafc390b918bd6ba93b0bdb3e
```

**`crates/base_train/src/trainable_session_active_production_owner_r4.rs`**

```text
lines: 90–155, 203–305, 400–447
sha256: f45ead7822d29d212917da09a7688455100d05c46cbbf3deec13c53f5dc44e18
```

**`crates/base_train/src/trainable_session_admission_profile_r4a.rs`**

```text
lines: 246–279, 334–342
sha256: d75a98515b5e9e3362244a8e4b5888654a5f4c32040bd0f11ed66ea353cf32a6
```

**`crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`**

```text
lines: 788–811, 7406–7455, 7550–7572, 7792–7868, 7924–8175, 9338–9342, 9943–9960, 10590–10620, 12374–12410, 12929–13088, 13420–13776
sha256: 3e80efc5c37bf9b30e33690fe3c8485e8f84f8429617ecf762f594e22ab14907
```

**`crates/base_train/src/ram_resident_adam_mv.rs`**

```text
lines: 1728–1770
sha256: 733c1c5b7e4cfd0402fbced6e21a4fbf84f2cb186f6d5186ee39ba469c431191
```

**`crates/base_train/src/adam_recovery_anchor_r3d.rs`**

```text
lines: 24–56, 113–175
sha256: 5f14530412cccdcf46282ab24d243564fbd4ccc51454e65651a33fc59d20be6f
```

**`crates/base_train/src/eve_persistent_adam_cross_invocation_physical_seal_r1.rs`**

```text
lines: 12–96, 136–214, 260–330
sha256: 6a9f35e23278833eb82a928334f48047bbc0449e56c9b42072a28e1ff9b96042
```

**`crates/base_train/src/mcu_session_runtime_r7.rs`**

```text
lines: 334–356
sha256: 8c1b42386d39d18cc1bd68f9a5db16831c0a85359261338ab5e7d89d276f0f41
```

**`crates/base_train/src/mcu_session_runtime_r7b.rs`**

```text
lines: 241–282, 478–517
sha256: dff8b745be63200d3c047912db59c1330ccc660dfec137887f70f5e2cc117d9f
```

**`crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`**

```text
lines: 1949–1962, 2015–2032, 13925–13964, 14051–14077
sha256: eca684258db1cb296ed5ef611d9909f3bbdd3306bebcd89066c1d6e9fea512ea
```

**`crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs`**

```text
lines: 109–139, 169–205
sha256: 7fdb4a1e7a524df81d3d17135bec14757722f74a7bd994d4d45f17fa9828fb90
```

### 부록 B. 실제 source bake 기록

```text
Release class: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Runtime implementation: Rust / existing WGPU backend
New Python loader: 0
New PowerShell loader: 0
New native Rust tests: 18, NOT RUN
Parent static scripts: 16 / 16 PASS after explicit successor-binding updates
Changed Rust files: 15
Changed existing static validators: 6
Rust delimiter / UTF-8 checks: 15 / 15 PASS, NOT a compiler check
Native compile / GPU execution: NOT RUN
Physical qualification: HOLD
```

#### B1. 실제 실행 구조 변경

**S9: native persistent production frame.** Active 계획은 `execute_r6_production_session_close_r1`에서 기존 Rust scheduler 프레임 하나로 실행한다. 최초 bootstrap, dataset borrow, scheduler profile과 N8 workload ledger를 프레임 수명으로 유지한다. 각 봉인된 경계에서는 실제 `complete_invocation -> park -> begin_invocation -> restore`를 수행하고 SourceState와 Adam / Weight / ProductionMuon / MCU / guard / lease sequencer를 R4에 move한다. 단순한 JSON 경계 흉내나 외부 Python / PowerShell 반복 실행이 아니다. 기존 single-invocation API에 Active 계획을 잘못 전달하면 명시적으로 거부한다. 이 방식은 §6의 외부 invocation API 반복 호출 표현을 구체화·변경한 구현 선택이다.

Scheduler profile과 집계 metadata는 추가 parked 사본 대신 동일 프레임이 보유한다. 최종 보고서에는 읽기 전용 SourceState metadata clone을 한 번 사용한다. 이 clone은 continuation, hydration 또는 optimizer 실행 authority가 아니다. pipeline이 빌려준 dataset allocation은 pipeline 반환 전까지 살아 있으므로 session-owned release 증거로 해제됐다고 주장하지 않는다.

R4A 기존 raw config serialization이 새 training 필드를 포함하므로 `trainable_session_admission_profile_r4a.rs` 자체는 수정하지 않았다. 새로운 실행 계획과 root 검증은 기존 R4 owner에서 추가한다.

#### B2. 실제 연결한 종료 경계

중간 명시적 checkpoint 의도는 Adam anchor와 Weight keyframe 판단에 함께 전달한다. 최종 durability는 기존 R3D/R3F head, 기존 reopen 검증 및 실제 canonical manifest / component file digest에 연결한다. R3D 경로를 legacy final M/V counter 1로 꾸미지 않는다.

Active N8은 기존 `finalize_n8_long_horizon`과 storage publication을 전체 workload에 한 번 적용한다. legacy RAM-final-pack count에 의존하는 이전 receipt / promotion 분기는 Active closure receipt로 대체하며 이전 physical PASS로 취급하지 않는다. 기존 deferred-single-checkpoint admission과 중간 명시적 checkpoint 계획은 서로 충돌하므로 거부한다.

실제 producer 취득, Eve submit > 0, unique lease 일치, reuse 0을 final witness 전에 요구한다. MCU와 Adam을 해제한 후 witness를 만들지 않는다. 완료되지 않은 target / source release는 in-place 소유권을 유지하고 오류를 반환한다. R7B abort는 pending wave, exact atlas lease 및 dependency in-flight 상태를 검사한 뒤 parent R7과 함께 종료한다. final durability, live witness, release 완료가 없는 `complete_invocation`은 Closed로 전이할 수 없다.

#### B3. 검사 의미와 남은 검증

기존 정적 검사의 이전 R3A/R3B 직접 필드, R7 legacy producer, R7A cache 함수, R7B reader-check 위치, R7A1 profile 변수를 실제 successor 호출과 소유권에 맞게 갱신했다. 16개 스크립트를 실행해 16개가 통과했다. 이는 A01~A26의 native / GPU 실행 결과가 아니다. 신규 Rust 단위 테스트 18개는 소스에 추가했지만 Cargo/Rustc가 없어 실행하지 못했다. 문서의 reserved native / physical PASS는 발행하지 않는다.

입력 ZIP의 Eve 크레이트 폴더명이 이중 인코딩 손상으로 Cargo.toml의 경로와 달랐다. 18개 파일의 내용을 바꾸지 않고 `crates/아담의_갈비뼈_이브/`로 경로를 복원했다. 출력 ZIP에는 해당 Unicode 경로의 UTF-8 flag를 확인했다.

입력 본체부터 없는 항목도 그대로 명시한다. `vendor/sherpa-rs-main/crates/sherpa-rs` path dependency가 없고, `configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json` 및 `artifacts/tokenizer_manifest_v5_final.json`에 대한 기존 테스트 include가 남아 있다. 무관한 vendor나 증거 파일을 임의 생성하지 않았다. 따라서 ZIP만으로 workspace 전체가 독립 빌드된다는 주장은 하지 않는다.

#### B4. 코드 전용 ZIP

```text
Filename:
ASH_PASS3_EVE_MCU_CLOSE_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256:
72ea2c8ccb6f9947c8667763e97c0400063743df64dfd2e4cfb931e28a255316
ZIP bytes: 21,399,947
Files: 8,399
CRC verification: PASS
Duplicate paths: 0
PowerShell files: 0
```

명세, 베이크 보고서, 검사 로그, 감사용 manifest는 ZIP 밖에서 제공한다. 기존 PowerShell helper 46개와 source backup 15개를 ZIP에서 제외했다. Cargo.toml / Cargo.lock / package build metadata, WGSL 및 컴파일에 직접 포함되는 기존 JSON fixture는 보존했다. Cargo.lock과 root Cargo.toml은 입력과 동일하다. 새로운 Python validator/loader를 추가하지 않았으며, 변경된 Python 6개는 기존 정적 검사 도구다.

이 부록은 source materialization과 실제 수행한 정적 검사만 보고한다. Rust borrow checking, linking, WGPU execution, numerical parity, failure cleanup 물리 증명은 아직 판단불가다.
