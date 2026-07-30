# ASH-ATTN-INTERCONNECT-W3-C4

## Headwise Chunked Decode Live Activation /
## Chunk Boundary Authority /
## Chunk-Local q_seq Geometry /
## Persistent KV Multi-Token Append Transaction /
## All-Layer Chunk Admission /
## Cross-Chunk Position Continuity /
## Zero CPU QKV Materialization /
## Zero Host Reupload /
## Chunk Output Authority Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C4`  
> Build revision: `W3-C4-headwise-chunked-decode-live-activation-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C3-R1` PASS  
> Full canonical source SHA-256: `e354fb0564e303c5171b74775883255ec2cc6ce76bf2d0eb299e26940ae4d362`  
> Full canonical source lines: `2451`  
> 대상 surface: `ProductionChunkedDecode` only  
> TensorCube role: `ShadowObserverOnly` 유지

---

# 0. 목적

W3-C3 종료 상태:

```text
ProductionPrefill            LiveEnforced
ProductionIncrementalDecode  LiveEnforced
ProductionChunkedDecode      ContractPresentLiveCallsiteAbsent
GenericGenerationForward     ReconciliationRequired
TensorCube                    ShadowObserverOnly
```

W3-C4는 historical W3-C1 policy를 변조하지 않고 child live-callsite authority를 추가하여 chunked route의 effective readiness를 다음과 같이 승격한다.

```text
historical parent readiness  ContractPresentLiveCallsiteAbsent
live registration            production callable
child effective readiness    LiveCallsitePresent
historical parent preserved  true
```

W3-C4 PASS가 확정하는 것:

```text
production-callable committed chunk adapter
bound committed chunk authority
chunk decode-step span authority
chunk position span authority
q_seq >= 2 and q_seq < kv_seq
persistent prefix required
multi-token staged KV append
all-layer atomic KV publication
joint KV and token-history rollback
cross-chunk step and position continuity
same-device RawBorrowed Q/K/V
CPU QKV materialize 0
host reupload 0
silent fallback 0
Headwise chunk output authority
```

W3-C4 PASS가 확정하지 않는 것:

```text
generic forward bypass reconciliation
TensorCube shadow exit
TensorCube live Q/K/V consumption
TensorCube final context authority
Headwise final FullActive promotion
```

---

# 1. Parent closure

Required parent chain:

```text
W0-R2
W1-R1
W2-R1
W3-C0
W3-C1-R3
W3-C2-R1
W3-C3-R1
```

Required parent state:

```text
prefill activation       live_enforced
incremental activation   live_enforced
incremental q_seq        1
incremental all layers   exact
persistent KV binding    prefix_plus_staged_exact
atomic KV publish        true
CPU materialize          0
host reupload            0
output authority         headwise
```

Any parent mismatch fails closed before chunk dispatch.

---

# 2. Live callsite registration and readiness authority

Historical W3-C1 policy remains immutable.

```rust
pub struct ChunkedLiveCallsiteRegistrationReceipt {
    pub model_instance_id: String,
    pub surface: HeadwiseRuntimeSurfaceId,
    pub route: HeadwiseCausalRouteId,
    pub adapter_type: String,
    pub entrypoint_symbol: String,
    pub production_callable: bool,
    pub gate_only: bool,
    pub diagnostic_only: bool,
    pub requires_bound_session: bool,
    pub requires_committed_chunk_authority: bool,
    pub parent_policy_digest: String,
    pub registration_digest: String,
    pub pass: bool,
}
```

Canonical entrypoint:

```text
decode_committed_chunk_with_sampling_choice
```

Effective readiness:

```rust
pub struct HeadwiseEffectiveRouteReadinessAuthority {
    pub parent_readiness: HeadwiseRouteReadiness,
    pub effective_readiness: HeadwiseRouteReadiness,
    pub live_callsite_registration_digest: String,
    pub historical_parent_preserved: bool,
    pub authority_digest: String,
    pub pass: bool,
}
```

The readiness override is valid only for `ProductionChunkedDecode`. It cannot mutate prefill, incremental, generic forward, diagnostic or trace surfaces.

---

# 3. Bound committed chunk authority

W3-C4 does not invent proposals or acceptance decisions.

```rust
pub struct BoundCommittedDecodeChunk {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub request_id: String,
    pub chunk_id: String,
    pub source_kind: ChunkCommitSourceKind,
    pub token_ids: Vec<u32>,
    pub token_count: u32,
    pub generated_len_before_forward: u64,
    pub chunk_start_decode_step_ordinal: u64,
    pub chunk_end_decode_step_ordinal: u64,
    pub upstream_commit_authority_digest: String,
    pub token_sequence_digest: String,
    pub chunk_authority_digest: String,
}
```

Runtime requirements:

```text
token_count >= 2
chunk.token_ids[0] == state.last_token
chunk start ordinal == state.generated.len() before forward
chunk end ordinal == start + token_count - 1
model/session/request identity exact
upstream commit authority digest valid
```

Automatic conversion of ordinary greedy or sampled single-token decoding into chunk mode is forbidden.

---

# 4. Decode-step span authority

W2 invocation identity stores the chunk start ordinal as its canonical decode-step ordinal. The whole range belongs to a separate span authority.

```rust
pub struct DecodeStepSpan {
    pub start_ordinal: u64,
    pub end_ordinal: u64,
    pub token_count: u32,
}
```

```text
end = start + token_count - 1
next chunk start = previous chunk end + 1
```

Gap, overlap, overflow and descending ranges fail closed.

---

# 5. Chunk position authority

Let:

```text
P = persistent prefix length
Q = committed chunk token count
```

Canonical geometry:

```text
P >= 1
Q >= 2
q_seq = Q
kv_seq = P + Q
q_position_base = absolute_position_base + P
kv_position_base = absolute_position_base
query end exclusive = KV end exclusive
suffix_aligned = true
```

`P == 0` belongs to full prefill and is rejected from chunked decode.

Cross-chunk continuity:

```text
next step start          == previous step end + 1
next query position      == previous query end + 1
next prefix length       == previous post-append KV length
next prefix generation   == previous committed generation
```

---

# 6. Span-aware KV lifecycle

W3-C3 single-token lifecycle remains valid as a singleton span projection.

```text
single token  [S..S]
chunk         [start..end]
```

Canonical APIs:

```rust
stage_for_decode_span(append_len, span)
commit_for_decode_span(span)
abort_staged_decode_span(span)
```

Legacy `stage(append_len)` and `commit()` cannot be used as chunked production authority.

---

# 7. Persistent KV multi-token transaction

Generation model:

```text
persistent prefix K/V       generation G
chunk-local append          staged generation G+1
attention-visible K/V       staged generation G+1
committed K/V after publish generation G+1
```

Generation advances once per committed chunk, not once per token.

```rust
pub enum ChunkedKvTransactionState {
    Open,
    AllLayersStaged,
    LogitsProjected,
    SelectionCommitted,
    Published,
    Aborted,
}
```

Required publication order:

```text
1. all-layer attention completion
2. all-layer next K/V staging
3. final last-row logits projection
4. next-token selector closure
5. layer cardinality, order and shape prevalidation
6. authoritative KV slot publication
7. span lifecycle commit
8. token-history publication
9. activation receipt finalization
```

No authoritative layer slot may change before all layers are staged and selector closure succeeds.

Failure behavior:

```text
abort staged span
staged tensors drop
committed K/V preserved
content generation preserved
past length preserved
generated history preserved
last token preserved
```

---

# 8. Token-history transaction

The input chunk starts with the already committed `state.last_token`.

After successful chunk processing:

```text
state.generated append = chunk.token_ids[1..] + selected_next_token
state.last_token        = selected_next_token
KV append count         = chunk.token_count
```

The selected next token is history output for the next decode operation. It is not included in the current chunk's KV append.

KV and token history form one logical commit boundary. Any selector, layer, dispatch, shape or lifecycle failure leaves both domains unchanged.

---

# 9. Runtime shape, causal bridge and W2 identity

Actual tensors:

```text
Q [batch, query_heads, Q, head_dim]
K [batch, kv_heads, P + Q, head_dim]
V [batch, kv_heads, P + Q, head_dim]
```

Each layer creates actual runtime shape observation and reconciliation receipts. ModelSpec dimensions cannot replace observed tensor dimensions.

W2 invocation identity:

```text
phase                         ChunkedDecode
route_id                      chunked_decode
decode_step_ordinal           Some(span.start)
prefill_invocation_ordinal    None
seq_q                         Q
seq_kv                        P + Q
layer_index                   actual loop index
layer_count                   actual model layer count
attention invocation generation unique and nonzero
```

Cross-layer and cross-chunk stale leases are rejected.

---

# 10. Live full-route admission

Each layer builds a real `HeadwiseFullRouteAdmissionContext` with:

```text
surface                   ProductionChunkedDecode
route                     ChunkedDecode
route readiness           LiveCallsitePresent from child authority
model/session identity    exact
actual Q/K/V shape        exact
causal position           exact
W2 invocation identity    present
same device/queue         exact
RawBorrowed Q/K/V         available
quarantine                false
runtime profile           supported
```

Positive disposition:

```text
AdmitProductionDeviceGuarded
```

Policy denial before dispatch cannot become Burn fallback.

---

# 11. Typed execution outcome

```rust
pub enum HeadwiseChunkedExecutionOutcome<T> {
    HeadwiseCommitted {
        output: T,
        admission: HeadwiseFullRouteAdmissionDecision,
        dispatch: HeadwiseAtlasProductionDispatchReceipt,
        authority: HeadwiseChunkedLayerOutputAuthorityReceipt,
    },
    BurnFallbackRequired {
        admission: HeadwiseFullRouteAdmissionDecision,
        failure: HeadwiseChunkedDispatchFailureReceipt,
        fallback: HeadwiseChunkedFallbackAttributionReceipt,
    },
}
```

Production chunked decode forbids:

```text
generic Option<Tensor> outcome
generic try_grouped_query_attention_via_atlas path
non-production CPU roundtrip
None as policy or dispatch failure
unattributed Burn selection
```

---

# 12. Zero movement and output authority

Positive layer requirements:

```text
same-device dispatcher           true
Q/K/V RawBorrowed                true
Q/K/V zero-copy                  true
output zero-copy                 true
output buffer identity exact     true
full output CPU readback         0
output host upload               0
hot-path map_async               0
hot-path blocking poll           0
```

Attention payload forbids:

```text
dispatch_native_qkv_to_cpu_f32
Q/K/V/context full payload materialization
Tensor<4>::from_data context reupload
Raw bridge UploadedFromHost
```

Positive final output authority:

```text
HeadwiseAllLayers
```

Mixed Headwise and Burn output within one layer is forbidden.

---

# 13. Burn fallback attribution

Burn fallback is permitted only when:

```text
admission == AdmitProductionDeviceGuarded
dispatch attempted == true
failure before Headwise output commit == true
Headwise output committed == false
```

Failed layer executes Burn exactly once with explicit attribution. Remaining layers receive explicit quarantined-remainder receipts and cannot retry Headwise.

This may preserve output continuity but does not count as a W3-C4 activation PASS.

---

# 14. Nonmutation boundary

W3-C4 must preserve:

```text
prefill live route
incremental q_seq=1 live route
ordinary greedy and sampled selector behavior
generic forward reconciliation blocker
TensorCube shadow-only role
TensorCube live dispatch count 0
WGSL mutation count 0
```

---

# 15. Validation contract

```text
positive cases              >= 104
canonical implementation     112
negative controls           >= 112
canonical implementation     120
decision counters           78
child artifacts             69
CLI key/value pairs         67
cross-chunk sequence        >= 32 chunks
cross-chunk appended tokens >= 256
```

Negative controls include:

```text
parent authority drift
missing or mismatched registration
invalid readiness promotion
chunk identity and upstream authority mismatch
token count below/above limits
first-token mismatch
step span gap/overlap/overflow
position gap/overlap
legacy lifecycle API use
staged/prefix/layer generation mismatch
partial layer publication
early token-history mutation
causal and Q/K/V shape mismatch
cross-layer/cross-chunk stale invocation
device/queue/raw-borrow mismatch
CPU materialization or host upload
unattributed fallback
retry after quarantine
prefill/incremental/generic/TensorCube mutation
```

All 78 decision counters are zero on PASS.

---

# 16. Artifact closure

```text
child_artifact_expected       69
child_artifact_list_sha256     9b59974b9aa086135829e3738f38a4d01adb884a3b3c18c5d435e3d35806c40b
serialization                  UTF-8, one filename per line, trailing LF included
```

Output directory:

```text
workspace/runtime/attention/interconnect/w3/c4
```

Runtime artifact:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c4_runtime_artifact.json
schema = ash.attn.interconnect.w3.c4.runtime_artifact.v1
```

Local manifest:

```text
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c4_local_manifest.json
schema = ash.attn.interconnect.w3.c4.local_manifest.v1
manifest self excluded from hash graph
```

Code ZIP excludes Markdown, PowerShell/CMD helpers, SHA sidecars and pre-generated W3-C4 runtime outputs.

---

# 17. CLI and direct execution

Binary:

```text
ash_attn_interconnect_w3_c4_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c4.args
```

Direct execution:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c4_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c4.args"
```

Expected first log:

```text
[ash-attn-interconnect-w3-c4][build] revision=W3-C4-headwise-chunked-decode-live-activation-v1 child_artifact_expected=69 child_artifact_list_sha256=9b59974b9aa086135829e3738f38a4d01adb884a3b3c18c5d435e3d35806c40b
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C4_HEADWISE_CHUNKED_DECODE_LIVE_ACTIVATION_CHUNK_BOUNDARY_AUTHORITY_CHUNK_LOCAL_Q_SEQ_GEOMETRY_PERSISTENT_KV_MULTI_TOKEN_APPEND_TRANSACTION_ALL_LAYER_CHUNK_ADMISSION_CROSS_CHUNK_POSITION_CONTINUITY_ZERO_CPU_QKV_MATERIALIZATION_ZERO_HOST_REUPLOAD_CHUNK_OUTPUT_AUTHORITY_SEALED
```

HOLD token:

```text
HOLD_ASH_ATTN_INTERCONNECT_W3_C4_CHUNK_CALLSITE_BOUNDARY_SPAN_KV_TRANSACTION_CONTINUITY_ZERO_COPY_OR_OUTPUT_AUTHORITY_NOT_PROVEN
```

---

# 18. Final seal

W3-C4 PASS seals a production-callable committed chunk adapter, child readiness promotion with historical parent preservation, q_seq greater than one Headwise admission, span-aware persistent KV multi-token transaction, joint KV and token-history rollback, cross-chunk continuity, zero host movement and Headwise chunk output authority.

After W3-C4:

```text
Prefill       LiveEnforced
Incremental   LiveEnforced
Chunked       LiveEnforced
Generic       ReconciliationRequired
TensorCube    ShadowObserverOnly
```

The next unresolved Headwise route is generic forward reconciliation. TensorCube remains outside output authority.
