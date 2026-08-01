# ASH-ATTN-INTERCONNECT-W4

## Live Headwise Q·K·V Execution Envelope /
## Production RawWgpuBufferLease Adoption /
## Texture06 Dynamic Slice Source Binding /
## Model·Layer·Session·Step Provenance /
## Q Buffer·K/V Texture Ownership Split /
## Frozen Invocation Partition Generation /
## Canonical KV Exact Coverage /
## Zero Persistent Source Duplication /
## Submission-Fenced Chunk Lifetime /
## Headwise FullActive Output Authority Preservation /
## No TensorCube Dispatch Yet /
## No Attention Output Mutation Seal

> 상태: 구현 명세 rev.1
> 부모 authority: `ASH-ATTN-INTERCONNECT-W3-C6`
> 부모 residency runtime: `ASH-ATTN-HEADWISE-TEXTURE-06`
> production output authority: `HeadwiseFullActive`

## 0. 목적

W4는 Texture-06의 gate-owned fixture source를 실제 Headwise production invocation의 `PreparedAtlasInputs` Q/K/V raw lease로 교체한다.

```text
Headwise live Q/K/V
→ production RawWgpuBufferLease
→ Texture-06 read-only dynamic slices
→ bounded K/V texture chunk ring
→ submission-fenced retirement
```

W4는 attention 계산기나 output writer를 교체하지 않는다. Headwise가 기존 계산과 output commit을 계속 담당하고 Texture-06은 동일 invocation의 K/V residency sidecar만 담당한다.

## 1. Authority SSOT

| 상태 | SSOT |
|---|---|
| model instance | `VerifiedModelInstanceBinding` |
| output authority | `ProductionAttentionOutputAuthorityPointer` |
| invocation lifetime | `ProductionAttentionAuthorityLease` |
| live Q/K/V backing | `PreparedAtlasInputs` raw leases |
| committed KV range | causal snapshot / DecodeState |
| dynamic boundaries | frozen `KvDynamicPartitionPlan` |
| K/V texture cache | Texture-06 chunk ring |
| completion | submission ticket + callback |
| slot reuse | owner-zero receipt |
| attention output | Headwise FullActive writer |

W4는 pointer CAS, route promotion, rollback, output commit 권한을 갖지 않는다.

## 2. Live invocation provenance

각 invocation은 다음을 digest에 포함한다.

```text
model_instance_id / epoch
authority_pointer_generation / digest
route_closure_digest / route_id
layer_index / invocation_ordinal
decode_session_id / epoch / step
q_position_base / kv_position_base / position_epoch
source_kv_generation / committed_token_count
q_seq / source_seq_len / q_heads / kv_heads / head_dim
device_identity_digest / queue_lineage_digest
causal_snapshot_digest
```

서로 다른 model, layer, session, step, KV generation의 lease를 하나의 partition에 섞으면 FAIL이다.

## 3. Production lease admission

Q/K/V는 모두 다음을 만족해야 한다.

```text
bridge mode             RawBorrowed
active buffer           present
bytes per element       4
same device             true
same queue lineage      true
host upload             0
metadata-only source    0
```

Canonical shapes:

```text
Q [batch, q_heads, q_seq, head_dim]
K [batch, kv_heads, source_seq_len, head_dim]
V [batch, kv_heads, source_seq_len, head_dim]
```

W4는 hidden reshape, host materialization, host reupload, source readback을 허용하지 않는다.

## 4. Ownership split

```text
Q backing               Headwise invocation owned
Q representation        RawWgpuBufferLease
Q texture upload        0

K/V canonical backing   Headwise / DecodeState owned
K/V slice lease         read-only range view
K/V texture slots       Texture-06 owned bounded cache
```

Per-head slice는 같은 backing buffer의 byte-range view이며 byte copy가 아니다.

기존 `same_backing_buffer`, `byte_ranges_overlap`, `admit_slice_alias` 검사를 재사용한다. read/read overlap은 허용할 수 있으나 read/write, write/write, retirement-pending slot reuse는 금지한다.

## 5. Dynamic partition freeze

```text
Authority lease acquire
→ Q/K/V admission
→ access-history snapshot
→ Q-wave partition planning
→ partition generation seal
→ first slot Encoding
```

첫 Encoding 이후 동일 invocation 안의 repartition count는 반드시 0이다. 다음 invocation에서만 새 history에 따라 새 generation을 선택할 수 있다.

기본 정책:

```text
boundary quantum       32 tokens
chunk tiers            32, 64, 128, 256, 512
texture slots          3 or 4
completion scan width  32 tickets
max tier transition    1
causal KV pruning      forbidden
```

## 6. Canonical KV exact coverage

Partition은 `[0, committed_token_count)`를 정확히 한 번 덮는다.

```text
first start             0
last end                committed_token_count
hole count              0
overlap count           0
out-of-range count      0
coverage multiplicity   exactly 1
logical order           token_start ascending
```

미커밋 capacity tail은 partition에 포함하지 않는다. 마지막 32-token 미만 tail은 부분 bin과 부분 chunk로 허용하되 coverage는 exact여야 한다.

## 7. Zero persistent source duplication

필수 all-zero:

```text
persistent_source_buffer_create_count
persistent_source_duplicate_bytes
host_materialization_count
host_upload_count
source_readback_count
source_staging_copy_count
```

허용되는 것은 raw lease handle clone, range view, bounded K/V texture slot, small uniform, bind group, command encoder, submission ticket뿐이다.

## 8. Chunk lifetime

상태 머신:

```text
Free
→ Encoding
→ Submitted
→ Completed
→ RetirementSelected
→ OwnerZero
→ Free
```

`submission_serial`은 로컬 순서이고 실제 완료 evidence는 queue completion callback이다. 정상 진행은 non-blocking `Poll`과 최대 32-ticket selective scan을 사용한다. steady-state per-chunk 전체 `Wait`는 금지하고 final drain 또는 명시적 ring-saturation emergency에서만 `Wait`를 허용한다.

```text
completion observed
→ transient handles drop
→ owner IDs retire
→ remaining owners == 0
→ OwnerZero
→ slot Free
```

Source lease는 관련 submission 완료 전 drop할 수 없다.

## 9. Headwise FullActive preservation

W4 before/after:

```text
pointer state                 HeadwiseFullActive
pointer generation            unchanged
pointer digest                unchanged
Headwise output writer        exactly 1
Texture-06 output writer      0
TensorCube output writer      0
production route mutation     0
```

동일 Q/K/V를 sidecar disabled/enabled로 A/B replay하고 Headwise output digest, causal receipt, route receipt가 동일해야 한다.

## 10. No TensorCube Dispatch Yet

필수 all-zero:

```text
tensorcube_pipeline_acquire_count
tensorcube_stage10_dispatch_count
tensorcube_stage11_dispatch_count
tensorcube_stage12_dispatch_count
tensorcube_output_commit_count
tensorcube_authority_lease_count
```

W4 live binding은 TensorCube dispatch symbol을 import하거나 호출하지 않는다.

## 11. No Attention Output Mutation

Texture uploader binding은 K source, V source, K destination texture, V destination texture, params uniform만 가진다.

필수 all-zero:

```text
q_mutation_count
k_source_mutation_count
v_source_mutation_count
attention_output_mutation_count
logit_mutation_count
sampler_mutation_count
decode_state_mutation_count
texture06_output_commit_count
```

## 12. Runtime failure policy

`PhysicalGateStrict`에서는 모든 W4 오류가 gate FAIL이다.

`RuntimeShadowObserve`에서는 sidecar만 HOLD하고 기존 Headwise production은 계속할 수 있다. 단 다음 failure receipt를 남긴다.

```text
failure_stage / failure_code
candidate_outcome = hold
production_continued = true
production_route_unchanged = true
silent_fallback_count = 0
TensorCube dispatch = 0
attention output mutation = 0
```

Model identity mismatch, authority pointer mismatch, production lease corruption, committed KV inconsistency, causal snapshot inconsistency, source lifetime violation은 production-fatal이다.

## 13. 구현 표면

### `burn_webgpu_backend`

`headwise_atlas.rs`에 prepared-input hook을 추가한다. 기존 dispatch wrapper와 WGSL 수치는 보존한다.

### `model_core`

`headwise_texture_06_live_binding.rs`를 추가하고 `native_wgpu.rs`의 production Headwise dispatch callsite에서 sidecar hook을 호출한다. 기존 authority enum, pointer CAS 의미, `RawWgpuBufferLease` layout은 변경하지 않는다.

### `ash_core`

Texture-06 dynamic partition, DeltaK-to-phase, Q-wave temporal trajectory, Cairo-inspired regularizer를 재사용한다. 부분 tail coverage를 허용하되 hard floor와 exact coverage는 보존한다.

### `orchestrator_local`

```text
attention_interconnect_w4_cli_registry.rs
ash_attn_interconnect_w4_verification_gate.rs
ash_attn_interconnect_w4_physical_gate.rs
```

두 bin은 `orchestrator_tcu_audit_bins` feature 아래 등록한다.

## 14. Verification gate

검증 matrix:

```text
committed KV    32, 64, 192, 384, 768, 1280, 1792
q_seq           1, 8, 32
layer           0, 10, 21
slot count      3, 4
chunk tier      32, 64, 128, 256, 512
```

검증 항목:

```text
raw lease admission
partial tail coverage
partition freeze
alias policy
ownership split
slot state machine
32-ticket scan ceiling
owner-zero before reuse
authority before/after equality
TensorCube zero counters
output mutation zero counters
negative controls
```

## 15. Physical gate

Physical gate는 Headwise dispatcher의 `prepare_native_qkv_strict`와 prepared hook을 통과한 raw lease를 Texture-06 sidecar에 전달한다.

관측 항목:

```text
same-device raw borrow count
source backing identity
per-head slice offsets
partition generation
chunk upload dispatch count
submission / completion count
peak live slot count
owner-zero receipts
persistent source duplicate bytes
host upload/readback count
Headwise output A/B digest
output authority before/after
TensorCube zero counters
```

표준 geometry에서 512-token K/V slot pair는 약 1 MiB이며 3-slot ring은 약 3 MiB다. 실제 판정은 texture descriptor requested bytes를 기준으로 한다. W4는 Texture-05의 고정 95.9MB floor를 할당하지 않아야 한다.

## 16. Negative controls

최소 다음을 독립적으로 FAIL시킨다.

```text
wrong model instance / epoch
stale authority generation / digest
authority state not HeadwiseFullActive
wrong layer / session / decode step
mixed source KV generation
UploadedFromHost or MetadataOnly source
missing active buffer
wrong Q/K/V shape
source shorter than committed range
coverage hole / overlap / out-of-range
repartition after Encoding
direct multi-tier transition
read-write alias overlap
slot reuse before owner-zero
completion before submission
duplicate completion
source drop before completion
persistent source allocation
host materialization / reupload / readback
TensorCube dispatch nonzero
Texture-06 output commit nonzero
production route mutation
Headwise output digest change
```

## 17. 완료 게이트

```text
workspace cargo check                    PASS
W4 verification bin check                PASS
W4-introduced warning                    0
actual Headwise prepared Q/K/V binding   PASS
same-device raw borrow                   PASS
K/V chunk physical upload                PASS
exact committed KV coverage              PASS
completion and owner-zero                PASS
persistent source duplicate bytes        0
host upload/readback                      0
Headwise output A/B parity                PASS
TensorCube dispatch                       0
production route mutation                 0
```

W4 완료 후에도 production authority는 `HeadwiseFullActive`, Texture-06 역할은 live residency sidecar, TensorCube는 미결선 상태다.

## 18. W5 handoff

W4는 다음 readiness evidence만 W5에 넘긴다.

```text
invocation_identity_digest
partition_generation
slice_id / token_start / token_count
q_lease_digest
K/V texture slot IDs
destination texture digest
submission serial / completion observed
exact coverage digest
```

W5에서 처음으로 다음을 연다.

```text
Q buffer + K texture
→ TensorCube Stage10 live shadow dispatch
```

## PASS token

```text
PASS_ASH_ATTN_INTERCONNECT_W4_LIVE_HEADWISE_QKV_EXECUTION_ENVELOPE_PRODUCTION_RAW_WGPU_BUFFER_LEASE_TEXTURE06_DYNAMIC_SLICE_MODEL_LAYER_SESSION_STEP_PROVENANCE_Q_BUFFER_KV_TEXTURE_OWNERSHIP_FROZEN_PARTITION_CANONICAL_EXACT_COVERAGE_ZERO_PERSISTENT_SOURCE_DUPLICATION_SUBMISSION_FENCED_CHUNK_LIFETIME_HEADWISE_FULLACTIVE_OUTPUT_AUTHORITY_NO_TENSORCUBE_NO_OUTPUT_MUTATION_SEALED
```

## 최종 봉인

> 실제 Headwise FullActive invocation의 Q/K/V가 동일 model·layer·session·step provenance 아래 Texture-06의 동적 K/V chunk ring에 물리적으로 적재되고 안전하게 회수되지만, attention 계산과 output authority는 한 비트도 바뀌지 않는다.
