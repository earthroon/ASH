# ASH-EVE-MCU-CLOSE-PHYS-R1C

## REAL WGPU PRODUCER INSTANCE REPLACEMENT REJECTION
## + COLD / WARM / REUSE PHYSICAL AUTHORITY CLOSURE

### 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-PHYS-R1C
Direct parent: ASH-EVE-MCU-CLOSE-PHYS-R1B
Class: R7A PRODUCER PHYSICAL AUTHORITY CLOSURE
Source release: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Native / WGPU qualification: HOLD
```

Parent artifact:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1B_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: 214f69a8654649ef12aad16afdd78a290ade1d20a3b76662d5470280eb46fc15
```

예약 토큰:

```text
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_STATIC
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_NATIVE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_COLD
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_WARM
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_REUSE
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C_REPLACEMENT_REJECT
PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C
HOLD_ASH_EVE_MCU_CLOSE_PHYS_R1C_PENDING
```

이 문서의 구조 계약과 실제 source bake 결과를 구분한다. 실제 실행 결과는 부록 A에 기록하며 source/static evidence를 native/WGPU physical PASS로 승격하지 않는다.

### 1. 목적

R1C는 Cold 실제 생성, Warm 실제 채택, same-session reuse, same-key/different-instance replacement rejection 네 축을 물리적으로 닫는다.

> 같은 cache key는 같은 producer authority의 충분조건이 아니다.
>
> 세션이 채택한 실제 producer instance identity가 authority다.

### 2. 유지할 authority

R7A DeviceAuthority-lifetime cache, McuSessionRuntimeR7, ProductionMuon/AdamW scheduler, Eve R3G lease/submission, R4 continuation, R7B child ownership, R1A arena law, R1B source/child witness, R3C/R3C1 commit authority를 유지한다.

Adam/HiMuon 수학, optimizer routing, WGPU shader equations, cache key 계산은 변경하지 않는다.

### 3. 세 사건 분리

```text
Physical Build
Session Adoption
Session Reuse
```

Warm cache에서는 physical build delta 0이 정상이다.

### 4. Stable Producer Identity

실제 R7A AdamW producer construction 성공 시 process-local immutable `McuAdamwProducerInstanceIdentityR1C`를 발급한다.

```text
schema
class = CACHE_AUTHORITY | QUALIFICATION_CANDIDATE
device_authority_id
canonical_cache_key_digest
physical_build_ordinal
process_instance_ordinal
instance_identity_digest
```

stack address는 authority identity가 아니다.

### 5. Cache Entry Binding

AdamW cache entry는 actual `Arc<AdamWActiveDeviceCandidateProducerR1>`와 stable identity를 함께 소유한다. 기존 cached API는 유지하고 R1C acquisition API가 `producer / identity / built_now / lookup_hit`를 반환한다.

### 6. Cold Contract

```text
first lookup_hit = false
first built_now = true
session adoption = 1
successor invocation same identity reuse > 0
```

### 7. Warm Contract

같은 process / DeviceAuthority에서 Cold가 만든 cache를 유지한다.

```text
first lookup_hit = true
first built_now = false
warm identity == cold cached identity
session adoption = 1
successor reuse > 0
```

### 8. Same-Session Reuse

R1C Cold/Warm/Replacement leg는 모두 `4 KeepResident + 4 FinalClose`다. actual acquisition에 invocation ordinal을 결합하고 invocation 1과 2에서 같은 instance identity를 요구한다.

### 9. Shared Admission Classifier

정상 reuse와 qualification candidate는 같은 classifier를 사용한다.

```text
InitialAdoption
ReuseSameInstance
RejectReplacement
```

key/device drift는 replacement 시험이 아니라 오류다.

### 10. Actual WGPU Replacement Candidate

Replacement leg invocation 2의 첫 same-instance reuse에서 cache 밖 qualification candidate P1을 만든다.

```text
P0 = current cached session producer
P1 = same DeviceAuthority
     same canonical key
     actual AdamWActiveDeviceCandidateProducerR1 constructor
     different stable instance identity
     not inserted into cache/session
```

P1은 metadata fixture가 아니다.

### 11. Candidate Non-Escape

qualification candidate는 producer를 private field로 소유하고 producer getter, optimizer submit API, cache insertion API, session replacement API를 노출하지 않는다. 따라서 candidate optimizer submission은 0이어야 한다.

### 12. Replacement Rejection

```text
key(P0) == key(P1)
Device(P0) == Device(P1)
instance(P0) != instance(P1)
```

에서 shared classifier는 `RejectReplacement`를 반환해야 한다.

### 13. Original Producer Survives

rejection 이후 authoritative identity는 P0이며 P0의 subsequent acquisition/execution이 계속되어야 한다. P1을 거부한 뒤 P0를 재구성하는 rollback은 허용하지 않는다.

### 14. Candidate Cleanup

P1 identity를 기록한 뒤 qualification Arc를 drop한다. P0 cache entry, DeviceAuthority, global cache, session P0 reference는 변경하지 않는다.

### 15. Existing Session Binding

기존 `McuAdamProducerBindingCloseR1`에 `first_lookup_hit_r1c`와 `producer_instance_identity_r1c`를 추가한다. legacy non-cache path는 R1C promotion 대상이 아니다.

### 16. Cache / Session Lifetime Separation

```text
R7A cache lifetime = DeviceAuthority lifetime
session adoption lifetime = TrainableSession lifetime
```

session close는 global cache destruction을 요구하지 않는다.

### 17. R1B Join

각 R1C leg는 R1B snapshot을 갖고 2 invocations, 11 persistent child continuity, bootstrap load 1, successor durable reload 0, in-memory restore 1을 요구한다.

### 18. Lease Join

각 final boundary에서 Eve source submit > 0, submit == unique lease, lease reuse == 0을 요구한다.

### 19. Numerical Non-Perturbation

Cold/Warm/Replacement는 같은 초기 조건과 parent numerical contract를 사용하며 Cold vs Warm, Cold vs Replacement를 비교한다. Weight, Adam M/V, HiMuon momentum, loss, generation, cursor, scheduler progression을 포함한다.

### 20. Campaign Mode

기존 Rust campaign에 `R1C_PRODUCER_AUTHORITY`를 추가한다.

```text
R1CCold
R1CWarm
R1CReplacement
```

세 leg는 하나의 process와 기존 bootstrap Device에서 순차 실행한다. 외부 Python/PowerShell orchestrator는 없다.

### 21. Receipts

```text
eve_mcu_close_phys_r1c_cold_producer_receipt.json
eve_mcu_close_phys_r1c_warm_producer_receipt.json
eve_mcu_close_phys_r1c_replacement_rejection_receipt.json
eve_mcu_close_phys_r1c_promotion_receipt.json
```

raw receipt는 physical_pass=false이고 combined promotion만 실제 campaign 검증 후 R1C PASS를 가질 수 있다.

### 22. Native Gate

R1C native test inventory는 stable identity uniqueness/digest, class separation, ordinal drift, initial adoption, same-instance reuse, same-key/different-instance rejection, key/device drift를 검사한다. fixture는 WGPU physical PASS가 아니다.

### 23. WGPU Acceptance

```text
P01 cold actual miss
P02 cold built_now true
P03 cold adoption 1
P04 cold invocation2 same instance
P05 warm actual hit
P06 warm built_now false
P07 warm identity == cold
P08 warm invocation2 same instance
P09 replacement first acquisition warm
P10 invocation2 actual P1 WGPU object
P11 same key
P12 different instance
P13 shared classifier rejects
P14 P1 optimizer submit 0
P15 P1 not installed
P16 P0 remains authoritative
P17 P0 later reuse
P18 R1B continuity
P19 Eve source submission
P20 lease reuse 0
P21 Cold/Warm numerical parity
P22 Cold/Replacement numerical parity
P23 normal final close
P24 poison 0
P25 raw evidence bound
```

### 24. Promotion Rule

Native PASS, Cold build, Warm no-build adoption, same-session reuse, actual P1, replacement rejection, P1 execution 0, P0 continuation, R1B continuity, lease exactness, numerical parity, normal close를 모두 만족한 실제 campaign에서만 `PASS_ASH_EVE_MCU_CLOSE_PHYS_R1C`를 발행한다.

Source bake에는 final PASS를 발행하지 않는다.

### 25. Rejection Conditions

cold miss 미관측, warm rebuild, key-only reuse, stable identity drift, metadata-only candidate, candidate cache/session 설치, candidate execution, P0 변경, cache clear/eviction으로 시험 성립, R1B reload/reconstruction, lease reuse, numerical drift는 HOLD다.

### 26. Source Scope

```text
ADD Rust:
crates/base_train/src/eve_mcu_close_physical_producer_authority_r1c.rs

MOD Rust:
crates/base_train/src/eve_mcu_close_physical_campaign_r1.rs
crates/base_train/src/eve_mcu_close_physical_qualification_r1.rs
crates/base_train/src/lib.rs
crates/base_train/src/mcu_session_runtime_r7.rs
crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs

MOD existing static validator:
tools/validate_ash_mcu_device_lifetime_kernel_cache_bounded_buffer_arena_r7a_static.py
```

Cargo/WGSL 변경은 없다.

### 27. Artifact Policy

code-only ZIP에서 spec/manifest/log/physical receipts/campaign outputs를 제외한다. Rust, existing WGSL, Cargo build metadata, compile-required fixtures, existing static validators를 유지한다. 새 Python/PowerShell loader는 없다.

### 28. Remaining PHYS-R1 Work

R1C 이후 남는 축:

```text
R1D EXECUTED WORKLOAD PROVENANCE
    + RUNNING BINARY
    + COMPILED SOURCE CLOSURE
    + RNG AUTHORITY
    + DATASET BYTE BINDING

R1E AGGREGATE NATIVE/WGPU PHYSICAL PROMOTION SEAL
```

### 29. Direct Successor

```text
ASH-EVE-MCU-CLOSE-PHYS-R1D
EXECUTED WORKLOAD PROVENANCE
+ RUNNING BINARY
+ COMPILED SOURCE CLOSURE
+ RNG AUTHORITY
+ DATASET BYTE BINDING
```

### 30. Final Law

> 같은 key는 같은 producer authority를 뜻하지 않는다.
>
> Cold는 실제 생성, Warm은 실제 기존 instance 채택, continuation은 같은 instance의 실제 재사용으로 구분한다.
>
> 같은 key의 다른 실제 WGPU producer가 만들어져도 session authority 교체는 실행 전에 거부한다.
>
> rejection 이후 기존 producer가 그대로 학습을 계속해야 negative closure가 성립한다.
>
> 실제 Rust/WGPU campaign이 없으면 physical HOLD를 유지한다.

## 부록 A. 실제 Source Bake

```text
Release: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Parent files: 8408
Added: 1 Rust
Modified: 6 (Rust 5 + existing static validator 1)
Deleted: 0
Output files: 8409
New Python loader: 0
New PowerShell loader: 0
WGSL changed: 0
Cargo.toml changed: 0
Cargo.lock changed: 0
```

실제 구현:

```text
1. R7A AdamW cache entry가 actual producer Arc와 R1C stable identity를 함께 소유.
2. exact cache acquisition이 lookup_hit / built_now / stable identity를 반환.
3. McuSessionRuntimeR7 기존 binding에 stable identity를 결합.
4. R1C scope가 actual acquisition을 invocation ordinal과 함께 기록.
5. Replacement leg invocation 2 첫 same-instance reuse에서 actual uncached P1 생성.
6. P1은 private qualification wrapper로 유지되고 cache/session에 노출되지 않음.
7. 정상 reuse와 P1 negative가 같은 classifier를 사용.
8. Cold/Warm/Replacement 4+4 leg를 기존 Rust campaign에서 같은 process/device로 실행하도록 연결.
9. R1B child/source witness, Eve lease evidence, numerical comparison을 R1C promotion에 join.
```

검사 결과:

```text
Existing related static scripts: 16 / 16 PASS
R1C source-contract checks: 65 / 65 PASS
Changed/added Rust UTF-8 + lexical delimiters: 6 / 6 PASS
R1C-prefixed native tests materialized: 9, NOT RUN
Additional PHYS campaign plan test: 1, NOT RUN
Cargo / rustc / rustfmt: unavailable
Rust compile / borrow checking / linking: NOT RUN
WGPU execution: NOT RUN
Numerical parity: NOT RUN
R1C physical PASS from source bake: none
Aggregate PHYS-R1: HOLD
```

정적 검사 최초 실행에서는 R7A validator가 이전 direct cache outcome call을 기대해 72/73이었다. 실제 R1C acquisition API와 stable identity를 검사하도록 기존 항목 하나를 갱신한 뒤 73/73 및 관련 16/16을 확인했다. 테스트 삭제나 주석 witness로 통과시키지 않았다.

Cargo/Rustc가 없으므로 compile 가능 여부는 판단불가다. 부모에서 상속된 sherpa-rs path dependency 및 일부 test include 입력 누락을 dummy crate/JSON으로 채우지 않았다.

코드 전용 산출물:

```text
ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1C_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256: 91b465784337d03ad0c8960e17dfe57785a5d0214ae82c578217f84fa2fa63a1
Bytes: 21,368,328
Files: 8,409
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
Unicode paths with UTF-8 flag: 18
```

명세, audit manifest, validation logs는 코드 ZIP 밖에 둔다.

## 부록 B. Campaign Input

```json
{
  "mode": "R1C_PRODUCER_AUTHORITY"
}
```

나머지 PHYS-R1 입력을 그대로 사용한다. 별도 loader/executor는 없다.
