# ASH-ATTN-INTERCONNECT-W3-C3 명세

## Headwise Incremental Full Activation /
## q_seq=1 Live Policy Enforcement /
## All-Layer Decode-Step Admission /
## Persistent KV Generation Binding /
## Dynamic KV Boundary Coverage /
## Zero CPU QKV Materialization /
## Zero Host Reupload /
## Greedy·Sampled Decode Parity /
## Incremental Output Authority Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C3`  
> Build revision: `W3-C3-headwise-incremental-full-activation-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C2-R1` PASS  
> Parent prefill state: `ProductionPrefill = LiveEnforced / 22 of 22 Headwise`  
> 대상 surface: `ProductionIncrementalDecode` only  
> q_seq authority: `1`  
> KV sequence authority: staged persistent KV transaction의 actual post-append length  
> Prefill·Chunked·Generic Forward: behavior-preserving nonmutation  
> TensorCube role: `ShadowObserverOnly` 유지  
> attention output authority: `Headwise` 유지  
> Full canonical source SHA-256: `e32d675da5d5e82c0f234c10001c9af9906a274753c64a1eb5fb72d4dd4c7603`

---

# 0. 목적

W3-C2는 production prefill을 다음 상태로 승격했다.

```text
prefill activation        live_enforced
all layers                22 / 22
shape coverage            full_prefill
CPU QKV materialize       0
host reupload             0
silent fallback           0
output authority          Headwise
```

W3-C3은 production incremental decode에 한해 다음을 확정한다.

```text
state.generated.len() before forward가 canonical decode_step_ordinal이다.
KvPositionLifecycle은 stage_for_decode_step / commit_for_decode_step을 사용한다.
모든 layer의 persistent K/V prefix generation이 exact하다.
new K/V append는 staged generation에 귀속된다.
attention-visible K/V는 staged generation으로 봉인된다.
모든 layer가 같은 decode step과 같은 staged KV generation을 사용한다.
모든 next K/V는 별도 step transaction에 보관된다.
전 레이어 성공 후에만 authoritative KvLayerCache에 publish한다.
production incremental은 typed Headwise outcome을 사용한다.
CPU QKV materialize와 host reupload는 0이다.
greedy와 sampled decode가 동일 incremental attention authority를 사용한다.
```

W3-C3 PASS가 확정하지 않는 것:

```text
chunked decode live activation
generic forward bypass 제거
TensorCube shadow exit
TensorCube live Q/K/V consumption
Headwise resource plateau
TensorCube final attention context
```

---

# 1. Parent closure

필수 parent chain:

```text
W0-R2
W1-R1
W2-R1
W3-C0
W3-C1-R3
W3-C2-R1
```

필수 parent state:

```text
W3-C1
  policy_authority        full_route_admission
  operator_intent         immutable_bind_time_snapshot
  incremental             unified_compatibility_projection
  legacy_projection       exact

W3-C2
  prefill_activation      live_enforced
  all_layers              exact
  zero_cpu_materialize    true
  zero_host_reupload      true
  output_authority        headwise
```

Parent mismatch 시 incremental dispatch를 실행하지 않는다.

---

# 2. Authority chain and state ownership

```text
VerifiedModelInstanceBinding
  -> W0 authority
  -> W1 model/runtime shape authority
  -> W2 invocation identity and generation domains
  -> W3-C0 coverage authority
  -> W3-C1 full-route admission policy
  -> W3-C2 prefill activation authority
  -> BoundDecodeSessionContract
  -> IncrementalDecodeStepOrdinalAuthority
  -> IncrementalKvStepTransaction
  -> HeadwiseIncrementalExecutionOutcome
  -> HeadwiseIncrementalStepActivationReceipt
```

상태 귀속:

```text
model-level immutable
  model binding / shape authority / full-route policy
  device / queue / dispatcher / Headwise output rings / quarantine

session-level mutable
  DecodeState / generated token count / bound session / KV lifecycle

step-level mutable
  decode_step_ordinal / staged generation / staged layer tensors / receipts

layer-level ephemeral
  actual Q/K/V shape / invocation identity / admission / output authority
```

---

# 3. Decode-step ordinal authority

Schema:

```text
ash.attn.interconnect.w3.c3.decode-step-ordinal.v1
```

Canonical source:

```text
decode_step_ordinal = state.generated.len() before forward
```

금지:

```text
kv.past_len에서 decode step 추론
causal position에서 decode step 추론
last_committed_decode_step + 1을 유일 source로 사용
selector 이후 generated.len() 사용
```

Greedy, sampled, legacy direct decode의 세 callsite가 모두 explicit ordinal을 전달해야 한다.

---

# 4. Persistent KV generation binding

Step 시작 전:

```text
committed_past_len = P
content_generation = G
staged_generation = None
staged_decode_step = None
```

Stage:

```text
stage_for_decode_step(1, S)
staged_generation = G + 1
staged_decode_step = S
q_seq = 1
kv_seq = P + 1
```

Commit:

```text
commit_for_decode_step(S)
content_generation = G + 1
last_committed_decode_step = S
committed_past_len = P + 1
staged fields clear
```

`KvLayerCache` metadata:

```rust
pub key_content_generation: u64,
pub value_content_generation: u64,
pub last_committed_decode_step: Option<u64>,
pub committed_token_count: usize,
```

각 layer에서 prefix generation G와 staged generation G+1을 분리하여 기록한다.

---

# 5. Atomic incremental KV transaction

```rust
pub enum IncrementalKvTransactionState {
    Open,
    AllLayersStaged,
    Published,
    Aborted,
}
```

Canonical publish order:

```text
1. 모든 layer attention과 MLP 완료
2. staged layer count·order·generation exact
3. logits projection 완료
4. authoritative KvLayerCache에 next K/V publish
5. kv.past_len = P + 1
6. commit_for_decode_step(S)
7. activation receipt finalize
```

실패 시:

```text
abort_staged_decode_step(S)
staged tensors drop
authoritative cache 보존
content_generation 보존
past_len 보존
```

Partial layer publish 후 rollback은 금지한다.

---

# 6. Incremental live policy enforcement

Surface modes after W3-C3:

```text
ProductionPrefill            LiveEnforced
ProductionIncrementalDecode  LiveEnforced
ProductionChunkedDecode      ExplicitDenied
GenericGenerationForward     ReconciliationRequired
ModuleTrace                  DiagnosticOnly
DiagnosticSmoke              DiagnosticOnly
```

Positive layer disposition:

```text
AdmitProductionDeviceGuarded
```

Admission denial before dispatch:

```text
no Headwise dispatch
no Burn fallback
no KV slot mutation
abort staged lifecycle
step returns error
```

Admitted dispatch failure before output commit만 explicit Burn fallback 대상으로 분류한다.

---

# 7. Runtime shape and causal authority

Actual tensors:

```text
Q [batch, query_heads, 1, head_dim]
K [batch, kv_heads, P + 1, head_dim]
V [batch, kv_heads, P + 1, head_dim]
```

필수 검증:

```text
Q batch == K batch == V batch
Q heads == ModelSpec query_heads
K heads == V heads == ModelSpec kv_heads
Q/K/V head_dim == ModelSpec head_dim
Q seq == 1
K seq == V seq == staged visible token count
causal seq_q == 1
causal seq_kv == P + 1
q_position_base == absolute_position_base + P
```

Backend causal snapshot과 model-core runtime snapshot은 각 schema를 유지하고 field-exact bridge receipt로 연결한다.

---

# 8. Dynamic KV boundary coverage

Contract matrix:

```text
1 / 2 / 3
15 / 16 / 17
31 / 32 / 33
63 / 64 / 65
127 / 128 / 129
255 / 256 / 257
511 / 512 / 513
1023 / 1024 / 1025
max_position - 1
max_position
```

Live production entrypoint는 persistent prefix가 필요하므로 post-append `kv_seq >= 2`다.

각 target `N`:

```text
past_len_before = N - 1
append_len = 1
q_seq = 1
kv_seq = N
```

---

# 9. W2 invocation identity and provenance

각 layer invocation:

```text
phase                         IncrementalDecode
route_id                      incremental_decode
layer_index                   actual
layer_count                   actual
decode_step_ordinal           Some(S)
prefill_invocation_ordinal    None
seq_q                         1
seq_kv                        P + 1
attention_invocation_generation unique and nonzero
```

같아야 하는 domain:

```text
model / session / decode step / position epoch / prefix generation / staged generation
```

달라야 하는 domain:

```text
layer index / invocation generation / lease capture generation / buffer identities
```

Cross-layer·cross-step stale lease를 거부한다.

---

# 10. Typed execution outcome

```rust
pub enum HeadwiseIncrementalExecutionOutcome<T> {
    HeadwiseCommitted {
        output: T,
        admission: HeadwiseFullRouteAdmissionDecision,
        dispatch: HeadwiseAtlasProductionDispatchReceipt,
        authority: HeadwiseIncrementalLayerOutputAuthorityReceipt,
    },
    BurnFallbackRequired {
        admission: HeadwiseFullRouteAdmissionDecision,
        failure: HeadwiseIncrementalDispatchFailureReceipt,
        fallback: HeadwiseIncrementalFallbackAttributionReceipt,
    },
}
```

Production incremental에서 금지:

```text
generic Option<Tensor> outcome
non-production CPU branch
None으로 policy denial 또는 dispatch failure 표현
reason 없는 Burn 선택
```

---

# 11. Zero host movement and output authority

Positive layer:

```text
same_device_dispatcher           true
Q/K/V zero-copy                  true
output zero-copy                 true
output buffer identity exact     true
output CPU readback              0
output host upload               0
hot-path map_async               0
hot-path blocking poll           0
```

Attention payload에서 금지:

```text
dispatch_native_qkv_to_cpu_f32
Q/K/V/context full payload materialization
Tensor<4>::from_data reupload
Raw bridge UploadedFromHost
```

Layer authority:

```text
HeadwiseDeviceGuarded
BurnGpuAttributedFallback
BurnGpuQuarantinedRemainder
```

Positive step final authority:

```text
HeadwiseAllLayers
```

---

# 12. Burn fallback attribution

허용 조건:

```text
admission == AdmitProductionDeviceGuarded
dispatch attempted == true
failure before output commit == true
Headwise output committed == false
```

Failed layer는 Burn GQA를 정확히 한 번 실행하고 receipt를 남긴다. 이후 layer는 Headwise를 재시도하지 않고 `BurnGpuQuarantinedRemainder` receipt를 갖는다.

이 경로는 output continuity를 제공할 수 있으나 W3-C3 activation PASS로 인정하지 않는다. Burn 자체 실패 시 KV transaction을 abort한다.

---

# 13. Greedy·sampled parity and long decode

다음 세 callsite가 동일 authority를 사용한다.

```text
decode_step_with_sampling_choice greedy
decode_step_with_sampling_choice sampled
decode_step legacy direct
```

허용되는 차이는 `LastLogitsGpu` 이후 selector 단계뿐이다.

Long decode minimum:

```text
100 sequential decode steps
```

각 step에서 ordinal, past length, global generation, layer generation이 1씩 전진하고 staged state가 commit 후 비어 있어야 한다.

Historical activation receipts는 unbounded 보관하지 않고 latest-only 또는 bounded ring으로 제한한다.

---

# 14. Validation matrix

```text
positive cases              >= 88
canonical implementation     96
negative controls           >= 96
canonical implementation    104
decision counters           64
long decode steps           >= 100
child artifacts             59
CLI key/value pairs         55
```

Negative controls include:

```text
parent digest drift
step source mismatch / duplicate / descending
stage() or commit() legacy API use
staged generation overflow or mismatch
partial layer publish
missing/duplicate/reversed layer
causal and Q/K/V shape mismatch
cross-layer/cross-step lease
legacy bool-only admission
device/queue/raw-borrow mismatch
CPU materialize or host upload
unattributed fallback
retry after quarantine
selector-specific attention path
prefill/chunked/generic/TensorCube mutation
```

PASS 시 64 decision counters는 모두 0이다.

---

# 15. Artifact closure

Output directory:

```text
workspace/runtime/attention/interconnect/w3/c3
```

```text
child_artifact_expected       59
child_artifact_list_sha256     0e75d7cc6d18cb740767427f3e0e26d3215ea025a543464db1a317eb76d12fd3
serialization                  UTF-8, one filename per line, trailing LF included
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c3_runtime_artifact.json
schema = ash.attn.interconnect.w3.c3.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c3_local_manifest.json
schema = ash.attn.interconnect.w3.c3.local_manifest.v1
manifest self excluded from hash graph
```

Code ZIP excludes Markdown, W3-C3 runtime outputs, SHA sidecars, PowerShell/CMD helpers.

---

# 16. CLI contract

Binary:

```text
ash_attn_interconnect_w3_c3_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c3.args
```

Canonical count:

```text
55 key/value pairs
110 non-empty lines
```

Required parent inputs include W0, W1, W2, W3-C0, W3-C1 and W3-C2 runtime artifacts and manifests, verified model binding and model spec.

---

# 17. PASS gate

```text
parents exact
model/session binding exact
ProductionIncrementalDecode LiveEnforced
all three callsites use explicit state.generated.len before forward
stage_for_decode_step / commit_for_decode_step / abort exact
q_seq=1 and dynamic KV geometry exact
actual runtime shape and causal bridge exact
W2 invocation identity per layer exact
prefix and staged generation exact
all layer count, order and admission exact
all layer Headwise dispatch success
atomic KV publish exact
same-device RawBorrowed Q/K/V
CPU materialize 0
host reupload 0
silent fallback 0
Burn fallback 0 in positive matrix
greedy sampled parity exact
100+ step continuity exact
prefill/chunked/generic/TensorCube mutation 0
positive cases >= 88
negative controls >= 96
child artifacts 59/59
runtime artifact and manifest pass
```

Expected summary:

```text
surface=production_incremental_decode
enforcement_mode=live_enforced
q_seq=1
all_layers=22/22
decode_step_authority=generated_len_before_forward
kv_generation_binding=prefix_plus_staged_exact
dynamic_kv_coverage=true
atomic_kv_publish=true
kv_abort_rollback=true
cpu_materialize_count=0
host_reupload_count=0
silent_fallback_count=0
greedy_sampled_decode_parity=exact
long_decode_steps>=100
tensorcube_role=shadow_observer_only
output_authority=headwise
child_artifacts=59/59
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C3_HEADWISE_INCREMENTAL_FULL_ACTIVATION_Q_SEQ_1_LIVE_POLICY_ENFORCEMENT_ALL_LAYER_DECODE_STEP_ADMISSION_PERSISTENT_KV_GENERATION_BINDING_DYNAMIC_KV_BOUNDARY_COVERAGE_ZERO_CPU_QKV_MATERIALIZATION_ZERO_HOST_REUPLOAD_GREEDY_SAMPLED_DECODE_PARITY_INCREMENTAL_OUTPUT_AUTHORITY_SEALED
```

---

# 18. Direct Cargo execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c3_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c3.args"
```

Expected revision:

```text
W3-C3-headwise-incremental-full-activation-v1
```

Expected first log:

```text
[ash-attn-interconnect-w3-c3][build] revision=W3-C3-headwise-incremental-full-activation-v1 child_artifact_expected=59 child_artifact_list_sha256=0e75d7cc6d18cb740767427f3e0e26d3215ea025a543464db1a317eb76d12fd3
```

---

# 19. Final seal

W3-C3 PASS seals explicit decode-step authority, staged persistent-KV generation, all-layer transaction publication, same-device Headwise q_seq=1 execution, zero host movement, selector parity and incremental Headwise output authority. Prefill remains live-enforced. Chunked and generic forward remain unresolved. TensorCube remains shadow-only.
