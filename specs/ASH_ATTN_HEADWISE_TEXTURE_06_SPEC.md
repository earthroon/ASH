# ASH-ATTN-HEADWISE-TEXTURE-06

## Existing Dynamic Tensor Policy Adoption /
## LoRATrain VRAM Microbatch Scheduler Reuse /
## FFN Power-of-Two Capacity Candidate Search /
## Active Span Compaction Reuse /
## DeltaK·QWave Capacity Hint Binding /
## Committed KV Hard-Floor Preservation /
## Texture Capacity Generation Migration /
## Submission-Fenced Old Generation Retirement /
## No Causal KV Pruning Authority Expansion /
## Access-History Accumulated Heatmap /
## RawWgpuBufferLease Slice Authority /
## Adaptive Bitstream Slice Chunking /
## Chunk Slot Submission State Machine /
## Selective Owner-Zero Retirement /
## QWave Temporal Boundary Trajectory /
## DeltaK-to-Phase Projection Adoption /
## Cairo-Inspired Tube-Concentration Overshoot Regularizer /
## Release-Impulse Boundary Damping /
## Phase-Coherent Path-Integral Partition /
## Intermediate-Tier Transition Enforcement /
## No Direct Mathematical-Theorem Claim Seal

> 상태: 갱신 명세 rev.2  
> 패치 ID: `ASH-ATTN-HEADWISE-TEXTURE-06`  
> 부모: `ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01-R2` 계열  
> 생산 권위: `BufferAtlasV1` 유지  
> 후보 권위: Texture dynamic-slice shadow-only  
> 금지: causal KV 삭제, production route mutation, hidden fallback, theorem-derived correction 주장

---

# 0. 목표

Texture-05의 `physical_page_capacity=16`, `maxSeqKv=1792` 고정 residency를 canonical DecodeState K/V 기반의 동적 slice cache로 교체한다.

```text
Canonical DecodeState K/V
→ RawWgpuBufferLease range authority
→ 32-token access-history bins
→ DeltaK-to-phase projection
→ QWave temporal boundary trajectory
→ Cairo-inspired overshoot regularization
→ phase-coherent path-integral partition
→ bounded texture chunk ring
→ canonical logical merge
→ submission-fenced selective retirement
```

동적화 대상은 물리 texture cache의 경계·크기·prefetch·retirement이며, committed KV 범위와 attention 의미는 바꾸지 않는다.

# 1. Authority boundary

Correctness SSOT:

```text
DecodeState K/V backing buffers
committed_token_count
causal snapshot
production generation
```

TEXTURE-06 소유:

```text
access-history snapshot
QWave boundary trajectory
partition candidate graph
chunk boundaries and tiers
chunk slot assignment
submission completion tickets
selective retirement receipts
```

필수 all-zero counters:

```text
causal_kv_prune_count
committed_range_hole_count
committed_range_overlap_count
logical_merge_order_mutation_count
production_route_mutation_count
candidate_output_commit_count
candidate_downstream_consumer_count
silent_capacity_fallback_count
```

# 2. Existing policy adoption

## 2.1 LoRATrain scheduler

기존 `build_gpu_microbatch_packing_plan_and_receipt`를 adapter에서 직접 호출한다.

```text
VRAM budget
→ max active tokens
→ unsafe tier 0.5 shrink
→ GPU-only/order-preserving receipt
```

OOM·dispatch-timeout retry 계약을 유지하며, receipt 없는 shrink를 금지한다.

## 2.2 FFN capacity ladder

기본 chunk tiers:

```text
32, 64, 128, 256, 512 tokens
```

경계 quantum은 32 tokens다. 32는 subgroup width가 아니라 history·boundary 정렬 단위다.

## 2.3 Active span compaction

Compaction은 KV 삭제가 아니다. 현재 invocation에서 처리할 committed chunk descriptor를 압축할 뿐이며 전체 committed range coverage를 유지한다.

# 3. RawWgpuBufferLease slice authority

Canonical BHSD K/V lease에서 head별 token slice를 파생한다.

필수 검사:

```text
same_backing_buffer
byte_ranges_overlap
RawBorrowed mode
BorrowedBuffer handle state
shape/offset/size bounds
```

Read/read overlap은 허용하지만 read/write와 write/write overlap은 금지한다. Submitted 또는 retirement-pending slot은 새 destination으로 재사용할 수 없다.

# 4. Access-history heatmap

각 32-token bin은 다음 이력을 보존한다.

```text
read count and EMA
bytes read
last/previous submission serial
reuse distance
neighbor affinity
DeltaK activity
QWave amplitude/phase/coherence
pressure/closure/resonance
history generation
```

미완료·실패·취소 submission은 확정 history에 반영하지 않는다.

# 5. QWave temporal boundary trajectory

DeltaK는 기존 sigmoid projection으로 circular phase에 투영한다.

```text
DeltaK activity
→ phase
→ phase mismatch
→ coherence
→ trajectory penalty
```

QWave가 boundary 이동 방향과 temporal persistence를 담당한다. Heatmap 단독으로 boundary를 변경할 수 없다.

Trajectory spike는 curvature·phase·pressure·closure 초과분 제곱 penalty로 억제한다.

# 6. Cairo-inspired overshoot regularizer

기존 ASH의 tube concentration·release impulse·curvature stress 구조를 공학적 regularizer로 재사용한다.

```text
tube_concentration = pressure × closure × resonance
cairo_overshoot = ln(1 + gamma × concentration × curvature)
```

Cairo 항은 edge cost를 증가시킬 수 있지만 boundary를 직접 mutation할 수 없다.

허용 표현:

```text
Cairo-Inspired Tube-Concentration Overshoot Regularizer
```

금지 표현:

```text
Mizohata-Takeuchi theorem-derived correction
mathematically proven overshoot bound
exact Cairo counterexample implementation
```

# 7. Release-impulse damping

Closure drop과 pressure delta로 shrink·retirement의 급격한 이동을 지연한다.

```text
release_impulse = |closure_release| + |pressure_delta|
```

고 release impulse에서는 즉시 shrink를 금지하고 중간 tier hold generation을 요구한다.

# 8. Phase-coherent path-integral partition

Node는 32-token 정렬 boundary, edge는 하나의 chunk candidate다.

Edge cost:

```text
memory bytes
dispatch count
heat variance
hot-range large-chunk penalty
migration cost
phase mismatch
trajectory overshoot
Cairo concentration stress
release impulse
boundary churn
```

선택된 path는 `[0, committed_token_count)`를 정확히 한 번 덮어야 한다.

# 9. Intermediate-tier transition

기본 tier graph:

```text
32 ↔ 64 ↔ 128 ↔ 256 ↔ 512
```

Generation당 최대 1 tier 이동을 허용한다.

```text
32 → 256 금지
64 → 256 금지
32 → 64 → 128 → 256 허용
```

Correctness floor가 필요한 emergency grow만 typed receipt와 함께 예외로 허용한다.

# 10. Frozen partition generation

Invocation 시작 시 partition generation을 pin한다. 실행 중 history가 변해도 해당 invocation의 chunk boundary와 logical merge order는 바뀌지 않는다.

```text
physical prefetch order  adaptive
logical accumulation     token_start ascending
streaming merge order    canonical fixed
```

# 11. Bounded chunk ring

기본 slot count는 3, 허용치는 3 또는 4다.

```text
Free
→ Encoding
→ Submitted
→ Completed
→ RetirementSelected
→ OwnerZero
→ Free
```

Submitted 상태에서 Encoding으로 직접 돌아갈 수 없다.

# 12. Submission-fenced retirement

각 chunk ticket은 monotonic `submission_serial`과 submit identity digest를 함께 기록한다.

한 reclaim pass는 최대 32 ticket만 검사한다.

```text
non-blocking progress poll
→ completed ticket selection
→ matching transient owner drop
→ owner-zero receipt
→ slot Free
```

전체 queue `poll(Wait)`는 session final retirement 또는 emergency ceiling drain에만 허용한다.

# 13. Owner-zero

Retirement 단위는 chunk owner ticket이다.

```text
completion observed
→ actual transient handle scope 종료
→ owner records retire
→ remaining owner IDs zero
→ OwnerZero
→ Free
```

Partition generation은 모든 소속 chunk ticket이 owner-zero가 된 뒤에만 retire한다.

# 14. Physical chunk upload

TEXTURE-06의 첫 physical gate는 production attention route를 바꾸지 않는다.

Gate-owned canonical K/V fixture buffer를 `RawWgpuBufferLease`로 slice하고 3-slot RGBA32F texture ring에 실제 WebGPU compute upload를 수행한다.

```text
physical chunk upload observed        true
full attention production execution   false
production route mutation count       0
candidate output commit count         0
```

# 15. Memory census

비교 항목:

```text
Texture-05 fixed known floor = 95,944,792 bytes
source fixture bytes
slot texture requested bytes
pending retirement bytes
partition generation overlap bytes
live/peak slot count
```

Gate-owned fixture source는 compatibility evidence이므로 source duplicate bytes를 0으로 주장하지 않는다. Production direct-lease profile은 별도 후속 결선에서 검증한다.

# 16. Verification

필수 fixtures:

```text
uniform
single hot tail
two hot islands
moving hot window
phase locked
release spike
```

필수 negative controls:

```text
scan width 33
Submitted → Encoding direct transition
32 → 256 direct tier transition
partition hole or overlap
Cairo direct mutation
causal KV prune
production route mutation
```

# 17. Runtime artifacts

Rust가 실행 시 작성한다.

```text
runtime_specification.json
verification runtime artifact
physical runtime artifact
local manifest
```

ZIP에는 Markdown 명세, runtime specification, local manifest, runtime artifact를 포함하지 않는다.

# 18. Binaries

```text
ash_attn_headwise_texture_06_verification_gate
ash_attn_headwise_texture_06_physical_gate
```

Canonical CLI:

```text
--boundary-quantum-tokens 32
--chunk-token-tiers 32,64,128,256,512
--texture-chunk-slot-count 3
--completion-scan-width 32
--max-boundary-tier-step 1
--delta-k-phase-projection sigmoid
--enable-qwave-boundary-trajectory true
--enable-cairo-overshoot-regularizer true
--enable-release-impulse-damping true
--forbid-causal-kv-pruning true
--forbid-production-route-mutation true
--require-raw-wgpu-buffer-lease true
--require-owner-zero-before-slot-reuse true
```

Unknown·duplicate·missing key는 fail-closed다.

# 19. PASS token

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_06_EXISTING_DYNAMIC_TENSOR_POLICY_LORATRAIN_BUDGET_FFN_TIER_ACTIVE_SPAN_RAW_LEASE_ACCESS_HISTORY_QWAVE_TEMPORAL_BOUNDARY_DELTAK_PHASE_CAIRO_OVERSHOOT_RELEASE_DAMPING_PHASE_COHERENT_PATH_INTEGRAL_INTERMEDIATE_TIER_COMMITTED_FLOOR_CHUNK_RING_SUBMISSION_FENCED_OWNER_ZERO_NO_KV_PRUNING_NO_THEOREM_CLAIM_SEALED
```

# 20. Completion state

```text
Texture-05 fixed full-capacity residency      parent baseline
Texture-06 dynamic partition policy           implemented
Texture-06 RawWgpuBufferLease slicing          implemented
Texture-06 QWave temporal trajectory           implemented
Texture-06 Cairo overshoot regularizer         implemented
Texture-06 bounded 3-slot upload ring          implemented
Texture-06 32-ticket selective retirement      implemented
Texture-06 full attention integration          not promoted
Texture-06 causal KV pruning authority         forbidden
Texture-06 production authority                HOLD
```

TEXTURE-06은 KV를 삭제하는 패치가 아니다. Canonical committed K/V 전체를 보존한 채, 시간축 접근 이력과 QWave phase trajectory로 물리 texture cache의 경계·크기·상주 시간을 조절한다.
