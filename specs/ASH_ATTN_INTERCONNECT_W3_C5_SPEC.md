# ASH-ATTN-INTERCONNECT-W3-C5

## Generic Forward Attention Reconciliation /
## Direct Burn Bypass Isolation /
## Production Route Classification /
## Headwise Canonical Surface Delegation /
## CPU Materialization Boundary Retirement /
## Explicit Diagnostic-Only Burn Authority /
## Unclassified Attention Callsite Zero /
## No Hidden Host Roundtrip /
## Headwise Route Closure Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C5`  
> Build revision: `W3-C5-generic-forward-attention-reconciliation-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C4-R2` PASS  
> Full canonical source SHA-256: `c4760fc4ed87f4665def795b9665b39ba7539d051e9558bf87153c4bbadf54b1`  
> Full canonical source lines: `2155`  
> TensorCube role: `ShadowObserverOnly` 유지

---

# 0. 목적

W3-C2, C3, C4에서 production attention의 세 canonical surface는 이미 Headwise live route다.

```text
ProductionPrefill            LiveEnforced
ProductionIncrementalDecode  LiveEnforced
ProductionChunkedDecode      LiveEnforced
```

남은 문제는 `GenericGenerationForward`가 historical W3-C1 policy에서 다음 상태라는 점이다.

```text
readiness      BypassRequiresCanonicalInvocation
fallback       BurnGpuDirectBypass
```

W3-C5는 generic forward에 네 번째 attention implementation을 만들지 않는다. 모든 production generic invocation을 다음 canonical destination 중 하나로 분류하고 기존 live surface에 위임한다.

```text
PrefillDelegate
IncrementalDelegate
ChunkedDelegate
DiagnosticOnlyBurn
ExplicitUnsupported
```

PASS 목표:

```text
production generic direct Burn          0
production generic layer/model bypass   0
production CPU materialization          0
production host reupload                0
production hidden full readback         0
unclassified attention callsite         0
diagnostic output promotion             0
TensorCube live dispatch                 0
output authority                         Headwise
```

---

# 1. Parent closure

Required chain:

```text
W0-R2
W1-R1
W2-R1
W3-C0
W3-C1-R3
W3-C2-R1
W3-C3-R1
W3-C4-R2
```

Required parent state:

```text
Prefill       LiveEnforced
Incremental   LiveEnforced
Chunked       LiveEnforced
Generic       BypassRequiresCanonicalInvocation
TensorCube    ShadowObserverOnly
```

Parent artifact, manifest, model binding, policy or source digest mismatch fails closed.

---

# 2. Generic invocation authority

```rust
pub enum GenericForwardIntent {
    ProductionPrefill,
    ProductionIncrementalDecode,
    ProductionChunkedDecode,
    ModuleTrace,
    DiagnosticSmoke,
    TrainingReference,
    Unsupported,
}

pub struct GenericForwardCanonicalInvocation {
    pub model_instance_id: String,
    pub decode_session_id: Option<String>,
    pub request_id: String,
    pub invocation_id: String,
    pub intent: GenericForwardIntent,
    pub input_token_count: usize,
    pub decode_state_present: bool,
    pub committed_past_len: Option<usize>,
    pub decode_step_ordinal: Option<u64>,
    pub prefill_invocation_ordinal: Option<u64>,
    pub committed_chunk_authority_digest: Option<String>,
    pub diagnostic_authority_digest: Option<String>,
    pub invocation_digest: String,
}
```

Route intent is caller-owned SSOT. Tensor shape alone cannot infer route.

```text
seq_len >= 1  does not imply prefill
seq_len == 1  does not imply incremental
seq_len > 1   does not imply chunked
```

Missing authority is an error, not fallback.

---

# 3. Route classification

```rust
pub enum GenericForwardCanonicalDestination {
    PrefillDelegate,
    IncrementalDelegate,
    ChunkedDelegate,
    DiagnosticOnlyBurn,
    ExplicitUnsupported,
}
```

Canonical matrix:

```text
ProductionPrefill
  bound session + empty committed KV
  -> W3-C2 prefill delegate

ProductionIncrementalDecode
  bound session + DecodeState + q_seq=1 + explicit step
  -> W3-C3 incremental delegate

ProductionChunkedDecode
  bound session + DecodeState + committed chunk + q_seq>=2
  -> W3-C4 chunked delegate

ModuleTrace / DiagnosticSmoke
  explicit diagnostic token
  -> DiagnosticOnlyBurn

TrainingReference / Unsupported
  -> ExplicitUnsupported for NativeWgpu production
```

W3-C5 adds no layer loop, QKV projection loop, causal builder, KV lifecycle or attention kernel.

---

# 4. Historical parent preservation

W3-C1 policy remains immutable.

```text
parent readiness     BypassRequiresCanonicalInvocation
child readiness      CanonicalDelegationReady
parent preserved     true
```

The child readiness authority is valid only when classification policy and delegate registry digests are exact.

---

# 5. Production generic reconciliation

Legacy methods are not production callable without authority.

```text
forward_logits_for_generation
forward_hidden_for_generation_input
```

W3-C5 retirement:

```text
legacy generation caller
  -> fail closed
  -> use DecodeState canonical surface

diagnostic caller
  -> explicit DiagnosticBurnAuthorityToken
  -> forward_logits_diagnostic_only / forward_hidden_diagnostic_only
```

Canonical production entrypoints validate generic invocation before delegating:

```text
DecodeState::forward_prefill
DecodeState::decode_step_with_sampling_choice
DecodeState::decode_committed_chunk_with_sampling_choice
```

---

# 6. Diagnostic Burn authority

```rust
pub struct DiagnosticBurnAuthorityToken {
    pub purpose: DiagnosticBurnPurpose,
    pub production_reachable: bool,
    pub host_materialization_allowed: bool,
    pub output_promotion_allowed: bool,
    pub kv_commit_allowed: bool,
    pub generation_output_allowed: bool,
    pub authority_digest: String,
}
```

Canonical values:

```text
production_reachable       false
output_promotion_allowed   false
kv_commit_allowed          false
generation_output_allowed  false
```

Allowed purposes:

```text
ModuleTrace
Decode04ConsumerSmoke
Decode04OverlayParity
HeadwiseReferenceSeam
NonProductionFixture
```

Diagnostic output cannot become production logits, hidden state, KV content, sampling input, generated history or model authority pointer.

---

# 7. Generic backend boundary

`AshDecoderBlock::forward`, `forward_prepared_set` and Burn `grouped_query_attention` remain available for training, reference and typed fallback execution.

```text
NativeWgpu production transitive reachability  0
production route registry membership           forbidden
production output authority                    forbidden
```

Generic backend support is not deleted merely to make a lexical primitive count zero.

---

# 8. Direct callsite registry

Source-derived baseline:

```text
raw attention primitive callsites      14
canonical typed fallback callsites      7
production generic bypass classes       4
unclassified callsites                  0 target
```

Each callsite has a stable ID, owner path, function, primitive, class, production reachability and authority owner.

Authorized classes:

```text
CanonicalTypedFallback
DiagnosticOnlyBurn
GenericBackendReference
HeadwiseReferenceSeam
```

Canonical fallback primitives remain owned by W3-C2/C3/C4 explicit fallback receipts. Diagnostic and reference primitives are nonproduction only.

---

# 9. CPU and host boundary retirement

Production transitive closure forbids:

```text
dispatch_native_qkv_to_cpu_f32
Q/K/V CPU materialization
context CPU materialization
hidden full-tensor materialization
attention Tensor::from_data reupload
hidden Tensor::from_data reupload
attention payload readback
hidden payload readback
hot-path map_async
hot-path blocking poll
```

Diagnostic materialization is allowed only with an explicit token and exact materialized-byte receipt.

---

# 10. Nonmutation boundary

W3-C5 preserves:

```text
W3-C2 prefill semantics
W3-C3 incremental semantics
W3-C4 chunked semantics
canonical fallback attribution
KV lifecycle and token-history semantics
TensorCube shadow-only role
Headwise/TensorCube WGSL
```

No Headwise FullActive pointer write occurs in C5. Final promotion is W3-C6 responsibility.

---

# 11. Validation contract

```text
positive cases                    >= 128
canonical implementation target    136
negative controls                 >= 136
canonical implementation target    144
production entrypoint cases       >= 12
diagnostic cases                  >= 8
callsite replay cases             >= 14
decision counters                  97
child artifacts                    81
CLI key/value pairs                81
```

All 97 production decision counters are zero on PASS.

Negative controls cover parent drift, missing invocation, ambiguous route, shape-only inference, missing DecodeState/chunk authority, direct Burn bypass, generic model/layer bypass, missing diagnostic token, output promotion, callsite registry drift, CPU/host movement, selector parity, route mutation and TensorCube/WGSL mutation.

---

# 12. Artifact closure

```text
child_artifact_expected       81
child_artifact_list_sha256     12caad3644f6df42bd94b93dc7af7d5b4ece0937e993415c3e668f66b9d2f634
serialization                  UTF-8, one filename per line, trailing LF included
```

Output:

```text
workspace/runtime/attention/interconnect/w3/c5/
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c5_runtime_artifact.json
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c5_local_manifest.json
```

Code ZIP excludes Markdown, PowerShell/CMD helpers, SHA sidecars and pre-generated W3-C5 runtime outputs.

---

# 13. CLI and direct execution

Binary:

```text
ash_attn_interconnect_w3_c5_gate
```

Response file:

```text
specs/cli/ash_attn_interconnect_w3_c5.args
```

Direct execution:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c5_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c5.args"
```

Expected revision:

```text
W3-C5-generic-forward-attention-reconciliation-v1
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C5_GENERIC_FORWARD_ATTENTION_RECONCILIATION_DIRECT_BURN_BYPASS_ISOLATION_PRODUCTION_ROUTE_CLASSIFICATION_HEADWISE_CANONICAL_SURFACE_DELEGATION_CPU_MATERIALIZATION_BOUNDARY_RETIREMENT_EXPLICIT_DIAGNOSTIC_ONLY_BURN_AUTHORITY_UNCLASSIFIED_ATTENTION_CALLSITE_ZERO_NO_HIDDEN_HOST_ROUNDTRIP_HEADWISE_ROUTE_CLOSURE_SEALED
```

---

# 14. Final seal

W3-C5 PASS seals explicit generic invocation authority, deterministic production route classification, delegation to W3-C2/C3/C4, direct Burn bypass isolation, diagnostic-only Burn authority, production CPU and host movement retirement, exact callsite registry closure and Headwise production route closure.

After W3-C5:

```text
Prefill       LiveEnforced
Incremental   LiveEnforced
Chunked       LiveEnforced
Generic       CanonicalDelegationReady
Diagnostic    ExplicitNonProductionOnly
TensorCube    ShadowObserverOnly
```

W3-C6 performs final census, rollback drill and `HeadwiseFullActive` promotion.