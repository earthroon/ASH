# ASH-ATTN-HEADWISE-TEXTURE-05-R4-R1

## Dynamic Wave Topology Census / Executor-Sourced Submit·Poll Authority / Static 58-Submit Census Retirement / Per-Commit Wave·Packet·Dispatch Count / R3-R3-R1 Receipt Reconciliation / GPU·Host Counter Clock Separation / First Actual Submission Topology Seal

---

## 0. 상태

```text
Patch ID
ASH-ATTN-HEADWISE-TEXTURE-05-R4-R1

Parent
ASH-ATTN-HEADWISE-TEXTURE-05-R4
ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R1

Nature
Instrumentation Authority Correction
Runtime Topology Census Closure
No Execution Topology Mutation
No WGSL Mutation
No Promotion Authority Mutation
```

R3-R3-R1 물리 실행에서 확인된 baseline은 다음과 같다.

```text
reference receipts           1,320
candidate receipts           1,320
total bounded waves         72,864
wave queue submits          72,864
wave completion polls       72,864
maximum in-flight wave           1
queue-ahead                      0
next-before-completion           0
maximum workgroups               64
```

동일 실행의 기존 R4 로그는 `encoders=58 submits=58 polls=13`을 출력했다. 이 값은 R3-R3-R1 bounded-wave executor의 실제 반복 횟수가 아니라 부모 outer instrumentation의 고정 topology 표기였다.

R4-R1은 이를 삭제하지 않고 `outer_static_census`로 강등한다. 실제 제출 topology의 SSOT는 executor 경계에서 누적된 R4 operation census와 R3-R3-R1 admission receipt로 이전한다.

---

## 1. 목표

1. 실제 executor가 생성한 command encoder, command buffer, queue submit, completion poll을 commit별로 집계한다.
2. wave submit/poll과 capture·finalize·timestamp envelope submit/poll을 분리한다.
3. 기존 `58 submit / 13 poll`을 runtime authority에서 퇴역시킨다.
4. R3-R3-R1 scheduler summary와 executor wave topology를 대조한다.
5. GPU timestamp query와 host monotonic duration을 독립 clock domain으로 봉인한다.
6. 후속 packetization의 전후 비교에 사용할 최초 실제 submission topology baseline을 발행한다.

---

## 2. 비목표

R4-R1은 다음을 바꾸지 않는다.

```text
WGSL source
32-token tile
4 tiles per wave
64 workgroup ceiling
single in-flight wave
queue-ahead zero
partial/merge/finalize 수학
BufferAtlas production authority
Texture candidate shadow authority
promotion disposition
```

다음 최적화는 후속 패치 범위다.

```text
multi-wave packetization
multi-dispatch single encoder
poll amortization
descriptor arena
bind group reuse
shader fusion
```

---

## 3. Authority 계층

```text
R3-R3-R1 Schedule
  planned bounded-wave authority

R4 Operation Census
  actual encoder / submit / poll / compute-pass authority

R4-R1 Reconciliation
  scheduler count와 executor count의 parity authority

Outer Static Census
  source topology mutation detector only
  runtime submission authority false
```

우선순위:

```text
executor actual counter
  > scheduler receipt estimate
  > source occurrence/static constant
```

---

## 4. 구현 구조

### 4.1 Backend module

```text
crates/burn_webgpu_backend/src/
  headwise_texture_05_r4_r1_topology_census.rs
```

주요 타입:

```text
HeadwiseTexture05R4R1CommitTopologyCensus
HeadwiseTexture05R4R1OuterStaticCensusReceipt
HeadwiseTexture05R4R1ClockDomainReceipt
HeadwiseTexture05R4R1ReconciliationReceipt
HeadwiseTexture05R4R1FirstActualSubmissionTopologyReceipt
HeadwiseTexture05R4R1SessionSummary
```

주요 builder:

```rust
build_r4_r1_topology_census(
    operations,
    decompositions,
    reference_admission_receipts,
    candidate_admission_receipts,
    parent_r3_r3_r1_summary,
)
```

### 4.2 Physical gate binding

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs
```

R4 physical measurement 이후 다음 artifact를 발행한다.

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r4_r1_runtime_artifact.json
  ash_attn_headwise_texture_05_r4_r1_local_manifest.json
```

Child artifact:

```text
workspace/runtime/attention/headwise/texture/05/r4_r1/
  commit_topology_census.json
  outer_static_census.json
  clock_domain_receipt.json
  r3_r3_r1_reconciliation_receipt.json
  first_actual_submission_topology_receipt.json
  session_summary.json
```

### 4.3 Verification gate

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_r4_r1_gate.rs
```

검증 범위:

```text
parent R4 PASS
parent R3-R3-R1 PASS
physical R4-R1 runtime PASS
executor-sourced census binding
static census authority retirement
clock-domain separation
WGSL mutation zero
execution topology mutation zero
artifact digest readback
```

---

## 5. Per-commit census

각 commit은 다음 값을 가진다.

```text
commit index
texture generation
route
seq_q
seq_kv

reference receipt count
candidate receipt count

planned packet count
completed packet count
planned wave count
encoded wave count
submitted wave count
completed wave count

reference wave count
candidate wave count
wave queue submit count
wave completion poll count

command encoder count
command buffer count
actual queue submit count
actual device poll count
map_async count
compute pass count
outer non-wave submit count

maximum in-flight wave
maximum wave workgroup count
queue-ahead count
next-before-completion count
```

현재 R3-R3-R1 baseline에서는:

```text
1 wave = 1 packet = 1 queue submit = 1 completion poll
```

후속 packetization에서는 wave count를 유지하면서 packet·submit·poll count만 감소할 수 있다.

---

## 6. Executor count source

R4-R1은 새로운 추정 counter를 만들지 않는다. 기존 실제 실행 경계에서 누적된 다음 R4 operation census를 사용한다.

```text
reference_submit_count
capture_submit_count
wave_submit_count
finalize_submit_count
envelope_submit_count
queue_submit_count
exhaustive_submission_count
command_encoder_count
command_buffer_count
device_poll_wait_count
map_async_count
compute_pass_count
```

R3-R3-R1 wave topology는 admission receipt의 다음 값을 사용한다.

```text
scheduled_wave_count
queue_submit_count
completion_poll_count
observed_max_in_flight_waves
queue_ahead_submission_count
next_wave_before_completion_count
max_observed_workgroups
```

`exhaustive_submission_count`가 실제 queue submit count이며, 기존 `legacy_dispatch_submission_count`는 exhaustive authority가 아니다.

---

## 7. Static 58-submit retirement

기존 값:

```text
encoders=58
submits=58
polls=13
maps=2
compute_passes=89
```

R4-R1 이후 표현:

```text
[r4-outer-static]
  runtime_authority=false
  retired_as_runtime_authority=true
```

이 값은 부모 source topology의 회귀 감지에만 사용한다. 실제 runtime submit/poll과 합산하거나 대체하지 않는다.

---

## 8. R3-R3-R1 reconciliation

Session gate:

```text
scheduler planned wave count
  == executor planned wave count
  == executor submitted wave count
  == executor completed wave count

scheduler wave submit count
  == executor wave submit count

scheduler wave poll count
  == executor wave completion poll count

scheduler maximum in-flight
  == executor maximum in-flight

scheduler queue-ahead
  == executor queue-ahead

scheduler next-before-completion
  == executor next-before-completion
```

현재 baseline 기대값은 실행에서 다시 수집하며 코드에 고정하지 않는다.

---

## 9. Clock-domain separation

GPU domain:

```text
wgpu timestamp query
queue span
reference GPU time
capture GPU time
candidate GPU time
normalize GPU time
compare GPU time
finalize GPU time
GPU unattributed time
```

Host domain:

```text
std::time::Instant monotonic
host wall
encode
Queue::submit call duration
completion poll wait
map poll wait
callback receive
host unattributed time
```

Counter domain:

```text
logical event/order counter
commit index
wave order
submission count
packet count
```

금지:

```text
GPU queue span + host completion-poll wait
```

completion poll wait는 동일 GPU 실행을 기다린 host 구간일 수 있으므로 GPU active time과 additive하지 않는다.

---

## 10. Runtime log

```text
[ash-attn-headwise-texture-05][r4-outer-static]
  ... runtime_authority=false

[ash-attn-headwise-texture-05][r4-r1-runtime-topology]
  commits=...
  packets=...
  waves=...
  compute_passes=...
  encoders=...
  command_buffers=...
  submits=...
  polls=...
  maps=...
  wave_submits=...
  wave_polls=...
  max_in_flight=...
  max_workgroups=...
  queue_ahead=...
  next_before_completion=...
  pass=true

[ash-attn-headwise-texture-05][r4-r1-reconciliation]
  scheduler_waves=...
  executor_waves=...
  scheduler_submits=...
  executor_wave_submits=...
  scheduler_polls=...
  executor_wave_polls=...
  wave_match=true
  submit_match=true
  poll_match=true
  in_flight_match=true
  pass=true

[ash-attn-headwise-texture-05][r4-r1-clocks]
  gpu_domain=wgpu_timestamp_query
  host_domain=std_time_instant_monotonic
  counter_domain=logical_event_order
  gpu_host_additive=false
  mixed_domain_count=0
  pass=true
```

Final token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R4_R1_FIRST_ACTUAL_SUBMISSION_TOPOLOGY_SEALED
```

---

## 11. 완료 게이트

```text
operation census commit count                         60
reference admission receipt count                 1,320
candidate admission receipt count                 1,320

planned wave == submitted wave                     PASS
submitted wave == completed wave                   PASS
scheduler/executor wave reconciliation             PASS
scheduler/executor submit reconciliation           PASS
scheduler/executor poll reconciliation             PASS

maximum in-flight wave <= 1                        PASS
maximum wave workgroup <= 64                       PASS
queue-ahead == 0                                   PASS
next-before-completion == 0                        PASS

outer static runtime authority == false            PASS
outer static retirement == true                    PASS

GPU/host mixed clock count == 0                    PASS
GPU+host additive claim == false                   PASS

execution topology mutation == 0                   PASS
WGSL mutation == 0                                 PASS
production authority mutation == 0                 PASS
candidate authority mutation == 0                  PASS

physical runtime artifact                           PASS
verification artifact                               PASS
packetization comparison baseline eligible          PASS
```

---

## 12. Cargo execution order

### 12.1 Physical census generation

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

### 12.2 R4-R1 artifact verification

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_r4_r1_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_r4_r1.args"
```

R4-R1 verification gate는 physical gate가 생성한 runtime artifact를 읽으므로 이 순서를 authority로 한다.

---

## 13. 후속 handoff

다음 패치:

```text
ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R2

Sequential Wave Packetization /
Multi-Dispatch Single Encoder /
Single In-Flight Packet Authority /
Packet-Scoped Completion Fence /
Bounded Workgroup Sum /
Queue-Ahead Packet Zero /
Per-Wave Numeric Order Preservation Seal
```

R4-R1 baseline과 R3-R3-R2 결과를 비교할 때:

```text
wave count
  유지

compute dispatch count
  수학적 순서 유지 범위에서 유지 또는 명시 변화

packet count
  감소

queue submit count
  감소

completion poll count
  감소

maximum in-flight packet
  1 유지

queue-ahead
  0 유지
```

---

## 14. 최종 봉인

R4-R1은 부모 R4의 고정 `58-submit / 13-poll` 표기를 actual runtime authority에서 퇴역시킨다.

실제 BufferAtlas reference와 Texture candidate executor가 발생시킨 bounded-wave submit/poll을 R3-R3-R1 admission receipt와 R4 operation census에서 집계하고, commit·session 단위로 reconciliation한다.

GPU timestamp query, host monotonic duration, logical counter를 독립 clock domain으로 봉인하며 중복 합산을 금지한다.

본 패치는 실행 topology, WGSL, production authority, candidate shadow authority를 변경하지 않는다.

결과 artifact는 후속 Sequential Wave Packetization의 최초 실제 submission topology baseline으로 사용한다.
