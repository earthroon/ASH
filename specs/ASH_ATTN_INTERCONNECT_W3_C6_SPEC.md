# ASH-ATTN-INTERCONNECT-W3-C6

## Headwise FullActive Promotion /
## Canonical Route Census Closure /
## Production Output Authority Pointer CAS /
## Promotion Eligibility Snapshot /
## Rollback Drill /
## Post-Promotion Route Revalidation /
## Diagnostic Isolation Recheck /
## TensorCube Shadow Noninterference /
## Headwise FullActive Authority Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-INTERCONNECT-W3-C6`  
> Build revision: `W3-C6-headwise-fullactive-promotion-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C5-R1` PASS  
> Canonical local source SHA-256: `c4fa78696083984e006880f7b9e3cb0d20b16ebfc2dd796f89ee4ff1cdefb571`  
> Canonical local source lines: `1499`  
> 대상: model-scoped production attention output authority  
> 신규 attention kernel: 없음  
> 신규 canonical route: 없음  
> TensorCube role: `ShadowObserverOnly` 유지  
> 최종 authority state: `HeadwiseFullActive`

---

# 0. 목적

W3-C0부터 W3-C5까지 route reality, full-route admission, prefill, incremental, chunked, generic forward closure가 완료됐다.

```text
Prefill                         LiveEnforced
Incremental                     LiveEnforced
Chunked                         LiveEnforced
GenericGenerationForward        CanonicalDelegationReady
Production direct Burn          0
Production generic bypass       0
Production CPU materialize      0
Production host reupload        0
Unclassified callsites          0
TensorCube                      ShadowObserverOnly
Output authority                Headwise
```

W3-C6는 C0-C5 parent closure를 immutable promotion eligibility snapshot으로 축약하고, model-scoped output authority pointer를 logical CAS로 `HeadwiseCanonicalRoutesSealed`에서 `HeadwiseFullActive`로 승격한다.

C6는 새 attention 계산을 만들지 않는다. C2/C3/C4 executor와 C5 canonical delegation을 재사용한다.

---

# 1. Legacy authority preservation

기존 `HeadwiseAttentionPromotionPolicySnapshot`은 01B compatibility authority다. 해당 validator의 `allow_chunked_decode == false` 제약을 완화하지 않는다.

```text
legacy promotion policy         historical compatibility authority
W3-C1 full-route policy         route admission SSOT
W3-C6 FullActive pointer        final model-scoped output authority SSOT
```

Legacy policy와 final output authority pointer를 별도 저장소와 별도 digest domain으로 유지한다.

---

# 2. Canonical route census

```text
01 ProductionPrefill
   executor       W3-C2
   readiness      LiveEnforced
   output         Headwise

02 ProductionIncrementalDecode
   executor       W3-C3
   readiness      LiveEnforced
   q_seq          1
   output         Headwise

03 ProductionChunkedDecode
   executor       W3-C4
   readiness      LiveEnforced
   q_seq          >= 2
   output         Headwise

04 GenericGenerationForward
   executor       W3-C5 classifier/delegator
   readiness      CanonicalDelegationReady
   destinations   C2 / C3 / C4 exactly
   output         Headwise
```

Closure:

```text
record count                     4
canonical attention routes       3
canonical generic destinations   3 / 3
unclassified records             0
duplicate records                0
missing records                  0
all-layer coverage               ModelSpec.num_layers exact
```

Generic forward는 네 번째 attention kernel이 아니다.

---

# 3. Promotion eligibility snapshot

```rust
pub struct HeadwiseFullActivePromotionEligibilitySnapshot {
    pub model_instance_id: String,
    pub model_instance_binding_digest: String,
    pub effective_runtime_binding_digest: String,
    pub parent_digests: BTreeMap<String, String>,
    pub route_census_digest: String,
    pub callsite_registry_digest: String,
    pub diagnostic_isolation_digest: String,
    pub tensorcube_noninterference_digest: String,
    pub production_direct_burn_count: u64,
    pub production_generic_bypass_count: u64,
    pub production_cpu_materialize_count: u64,
    pub production_host_reupload_count: u64,
    pub production_hidden_roundtrip_count: u64,
    pub production_silent_fallback_count: u64,
    pub unclassified_callsite_count: u64,
    pub headwise_quarantined: bool,
    pub active_production_attention_invocations: u64,
    pub eligible: bool,
    pub eligibility_digest: String,
    pub failures: Vec<String>,
}
```

Eligibility PASS:

```text
C0-C5 parent artifact and manifest exact
model and runtime binding exact
route census exact
all route output authority Headwise
movement, bypass and silent fallback counters 0
diagnostic isolation exact
TensorCube noninterference exact
headwise quarantine false
active production invocation count 0
```

Snapshot은 CAS 전에 생성하고 이후 immutable이다.

---

# 4. Production output authority pointer

```rust
pub enum ProductionAttentionOutputAuthorityState {
    Unbound,
    HeadwiseCanonicalRoutesSealed,
    HeadwiseFullActive,
}
```

Allowed transition:

```text
Unbound -> HeadwiseCanonicalRoutesSealed
HeadwiseCanonicalRoutesSealed -> HeadwiseFullActive
HeadwiseFullActive -> HeadwiseCanonicalRoutesSealed   rollback only
```

Forbidden:

```text
Unbound -> HeadwiseFullActive direct
HeadwiseFullActive -> Unbound
any state -> TensorCube authority
any state -> implicit Burn authority
```

Pointer:

```rust
pub struct ProductionAttentionOutputAuthorityPointer {
    pub model_instance_id: String,
    pub state: ProductionAttentionOutputAuthorityState,
    pub generation: u64,
    pub route_closure_digest: String,
    pub promotion_eligibility_digest: Option<String>,
    pub writer_id: String,
    pub operation_id: String,
    pub previous_pointer_digest: Option<String>,
    pub pointer_digest: String,
}
```

Generation starts at 1 for `HeadwiseCanonicalRoutesSealed`. Every successful transition advances exactly once. Rollback restores semantic state but never restores an old generation.

---

# 5. Logical CAS

Compound pointer records do not claim hardware compare-exchange. Canonical implementation is mutex-guarded logical CAS.

```rust
pub struct ProductionAttentionOutputAuthoritySlot {
    inner: Mutex<Option<ProductionAttentionOutputAuthorityPointer>>,
    active_invocations: AtomicU64,
    promotion_freeze: AtomicBool,
    applied_operations: Mutex<BTreeMap<String, ProductionAttentionOutputAuthorityCasReceipt>>,
}
```

Same critical section checks:

```text
current pointer present
current generation == expected generation
current digest == expected digest
model identity exact
writer identity exact
transition allowed
proposed generation == current + 1
proposed.previous_pointer_digest == current digest
operation ID unique or exact idempotent replay
active invocation count == 0
promotion freeze acquired
```

ABA prevention:

```text
Candidate G
FullActive G+1
Rollback Candidate G+2
Re-promotion FullActive G+3
```

---

# 6. Production attention lease

When the C6 authority slot is bound, every canonical production attention invocation captures the FullActive pointer generation and digest.

```text
route start
  -> acquire production attention lease
  -> active invocation count +1
  -> capture model, generation and pointer digest

output commit boundary
  -> pointer state still HeadwiseFullActive
  -> model identity exact
  -> generation exact
  -> pointer digest exact

route finish
  -> active invocation count -1
```

C2 prefill, C3 incremental and C4 chunked output commit points all perform lease revalidation. Diagnostic Burn and TensorCube shadow paths cannot acquire this lease.

Promotion and rollback require quiescence. Active production invocations are not force-cancelled.

---

# 7. Promotion operation

```text
1. C0-C5 parent closure revalidation
2. canonical route census 4/4
3. generic destinations 3/3
4. diagnostic isolation and TensorCube shadow recheck
5. immutable eligibility snapshot creation
6. pre-pointer readback HeadwiseCanonicalRoutesSealed
7. promotion freeze acquire
8. active invocations == 0
9. logical CAS
10. post-pointer readback HeadwiseFullActive
11. post-promotion route revalidation
```

Final pointer write is performed only by the named authority writer and operation ID.

---

# 8. Post-promotion route revalidation

After actual FullActive pointer CAS:

```text
Prefill
  boundary prompt matrix
  all layers Headwise

Incremental
  q_seq=1
  at least 128 sequential steps

Chunked
  at least 32 chunks
  at least 256 appended tokens

Generic
  all three canonical destinations replayed
```

Every route proves:

```text
FullActive pointer lease exact
all layers admitted
Headwise output committed
CPU materialize 0
host reupload 0
direct Burn 0
silent fallback 0
TensorCube output 0
```

---

# 9. Rollback drill

Rollback drill uses an isolated authority slot and the same CAS implementation.

```text
Candidate
  -> FullActive
  -> failure injection
  -> Candidate rollback
  -> stale generation and digest rejection
  -> FullActive re-promotion
```

Drill proves:

```text
prior semantic state exact
monotonic generation
ABA prevention
route mutation 0
Burn authority promotion 0
TensorCube pointer write 0
re-promotion success
```

Post-promotion active validation failure causes the active pointer to rollback to `HeadwiseCanonicalRoutesSealed` and returns HOLD.

---

# 10. Diagnostic isolation recheck

```text
production_reachable       false
output_promotion_count     0
KV commit count            0
generation commit count    0
sampling handoff count     0
pointer write count        0
```

Diagnostic Burn remains explicit nonproduction-only authority.

---

# 11. TensorCube shadow noninterference

```text
role                          shadow_observer_only
owner identity drift          0
live Q/K/V dispatch           0
output commit                 0
authority pointer write       0
promotion token read          0
production lease acquisition  0
shadow observation allowed    true
```

TensorCube and Burn are not output pointer state candidates.

---

# 12. Restart and device-loss behavior

Process restart requires parent revalidation and a fresh local slot bind. In-memory pointer state is not silently trusted across process epochs.

Device loss cannot carry FullActive state into a replacement device without model/runtime identity revalidation. Silent promotion carry-over is forbidden.

---

# 13. Implementation surface

New module:

```text
crates/model_core/src/headwise_fullactive_promotion.rs
```

Modified:

```text
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/src/attention_interconnect_w3_c6_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w3_c6_gate.rs
crates/orchestrator_local/Cargo.toml
specs/cli/ash_attn_interconnect_w3_c6.args
```

Forbidden modifications:

```text
Headwise WGSL
TensorCube WGSL
W3-C1 legacy validator relaxation
legacy allow_chunked_decode=true
new attention primitive
new canonical route
C2/C3/C4 numerical behavior
C5 diagnostic authority semantics
```

---

# 14. Validation and artifact contract

```text
positive cases              >= 144
implementation target       152
negative controls           >= 152
implementation target       160
decision counters           121
child artifacts             96
CLI key/value pairs         92
response file lines         184 non-empty
```

Child artifact ordered-list digest:

```text
0a410e3df9bfd9fb2f2fe51fc0457c80bef606f6a14c537e084c2fe06aad710a
```

Output:

```text
workspace/runtime/attention/interconnect/w3/c6/
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c6_runtime_artifact.json
workspace/runtime/attention/interconnect/ash_attn_interconnect_w3_c6_local_manifest.json
```

Code ZIP excludes Markdown, generated runtime artifacts, local manifests, SHA sidecars and PowerShell/CMD helpers.

---

# 15. PASS gate

```text
C0-C5 parents exact
legacy policy preserved
route census 4/4
canonical delegates 3/3
all-layer closure exact
production direct Burn 0
production generic bypass 0
production CPU materialize 0
production host reupload 0
production hidden roundtrip 0
production silent fallback 0
unclassified callsites 0
diagnostic isolation exact
TensorCube shadow noninterference exact
quarantine false
promotion eligibility true
logical CAS applied
pointer readback HeadwiseFullActive
generation incremented once
ABA guard exact
post-promotion route revalidation PASS
rollback drill PASS
rollback re-promotion PASS
restart rebind PASS
device-loss carry-over forbidden
positive cases >= 144
negative controls >= 152
decision counters 121 and all zero
child artifacts 96/96
runtime artifact pass true
local manifest pass true
```

Expected summary:

```text
promotion=fullactive
route_census=4/4
canonical_routes=3/3
generic_delegation=ready
all_layers=22/22
pre_pointer=headwise_canonical_routes_sealed
post_pointer=headwise_full_active
cas=applied
generation_advance=exact
aba_protection=true
active_invocations_at_cas=0
post_promotion_revalidation=pass
rollback_drill=pass
rollback_repromotion=pass
production_direct_burn=0
production_cpu_materialize=0
production_host_reupload=0
diagnostic_isolation=exact
tensorcube_role=shadow_observer_only
tensorcube_live_dispatch=0
tensorcube_output_commit=0
output_authority=headwise_full_active
child_artifacts=96/96
pass=true
```

PASS token:

```text
PROMOTE_ASH_ATTN_INTERCONNECT_W3_C6_HEADWISE_FULLACTIVE_PROMOTION_CANONICAL_ROUTE_CENSUS_CLOSURE_PRODUCTION_OUTPUT_AUTHORITY_POINTER_CAS_PROMOTION_ELIGIBILITY_SNAPSHOT_ROLLBACK_DRILL_POST_PROMOTION_ROUTE_REVALIDATION_DIAGNOSTIC_ISOLATION_RECHECK_TENSORCUBE_SHADOW_NONINTERFERENCE_HEADWISE_FULLACTIVE_AUTHORITY_SEALED
```

---

# 16. Direct Cargo execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_interconnect_w3_c6_gate `
  -- `
  "@specs/cli/ash_attn_interconnect_w3_c6.args"
```

Expected first log:

```text
[ash-attn-interconnect-w3-c6][build] revision=W3-C6-headwise-fullactive-promotion-v1 child_artifact_expected=96 child_artifact_list_sha256=0a410e3df9bfd9fb2f2fe51fc0457c80bef606f6a14c537e084c2fe06aad710a
```

---

# 17. W4 handoff

W3-C6 completion freezes Headwise as final production attention authority while TensorCube remains shadow-only.

W4 may consume:

```text
HeadwiseFullActive pointer digest
promotion eligibility digest
canonical route census digest
post-promotion revalidation digest
TensorCube noninterference digest
```

W4 candidate execution cannot mutate the Headwise pointer without its own explicit authority and compare/rollback contracts.

---

# 18. Final seal

W3-C6 PASS seals Headwise across Prefill, Incremental, Chunked and Generic canonical delegation. The model-scoped output authority pointer is promoted through expected-generation and expected-digest logical CAS, production output commits revalidate a FullActive lease, rollback advances generation rather than restoring it, Diagnostic Burn remains nonproduction-only, and TensorCube remains a noninterfering shadow observer.
