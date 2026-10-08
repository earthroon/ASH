# AOF-R1-CF5-C-R1

## NATIVE CONSUMER CALLSITE BINDING + COMPLETED OBSERVE-BACKING HANDOFF

```text
AOF-R1-CF5-C-R1

+ CF5-A/B OBSERVE BACKING PRESERVATION
+ CF5-C READ-ONLY CANDIDATE READER PRESERVATION
+ ACTUAL NATIVE Q/K/V CALLOUT AUTHORITY
+ PENDING-PREFIX → SESSION-LOCAL SHADOW HANDOFF
+ ORIGIN / SUCCESSOR CONSUMER IDENTITY SEPARATION
+ CURRENT CANONICAL LENGTH / GENERATION REBIND WITNESS
+ OBSERVE-ONLY ORDINARY INCREMENTAL ROUTE ADOPTION
+ OBSERVE-ONLY SELECTED CHUNKED ROUTE ADOPTION
+ VERIFIER PRIVATE Q/K/V SEAM FEASIBILITY ADMISSION
+ ROUTE-LOCAL PARITY / FIRST-MISMATCH RECEIPTS
+ SAME-QUEUE COMPLETION / RETIREMENT CLOSURE
+ SOURCE / COMPILE / PHYSICAL EVIDENCE SEPARATION

+ NO TRAINING CHECKPOINT SOURCE-DIGEST DRIFT
+ NO DUPLICATED AOF_FORWARD IMPLEMENTATION
+ NO SILENT HEADWISE / TENSORCUBE RELABEL
+ NO TAIL VISIBILITY
+ NO EXTRA CANONICAL KV MATERIALIZATION
+ NO CANONICAL TOKEN / KV PUBLICATION CHANGE
+ NO CF5 ACTIVE PROMOTION
+ NO EARLY CF5-C FULL PASS
```

**Status (2026-10-08): PARTIAL SOURCE/STATIC BAKE.** R1-A and R1-B/C OBSERVE candidates have been applied to source ZIPs. R1-D private verifier, R1-E physical acceptance and CF5-D ACTIVE remain HOLD; see actual bake annex §18 below.

---

## 0. Revision and scope

- **Patch ID:** `AOF-R1-CF5-C-R1`
- **Parent implementation:** `ASH_PASS3_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE_CODE_ONLY.zip`
- **Parent source archive SHA-256:** `944ba80b9e08e1615180021db1216dc31ca0c001000a619260ad137cc3823b9d`
- **Parent GitHub SSOT spec:** `ASH_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE_SPEC.md`, final commit `5985ce81f6069421c11c4eb7ce208249fede27b9`
- **Class:** Native read-only OBSERVE callsite integration and observer lifetime ownership.
- **Successor (conditional):** CF5-C-R2 verifier seam / checkpoint-lineage qualification if an unmodified valid private-verifier seam cannot be established. Only after all required C routes close may CF5-D canonical block publication begin.

**Allowed:** expose actual read-only native Q/K/V values at a selected route, hand off a completed shadow to a bounded session owner, compare GPU context and capture physical receipts.

**Forbidden:** make `[1,H,C,W]` act as canonical `[1,H,V,W]` using a false shape, change `state.kv`, infer completion from a numerical verdict, or activate speculative storage in production.

---

## 1. Source-confirmed initial conditions

### 1.1 Existing CF5-C code is not a wired consumer

- `crates/model_core/src/aof_r1_kv_consumer_bridge.rs` provides `observe_verifier_candidate()` and `observe_decode_candidate()`, but the parent bake report marks natural native verifier/decode invocation **NOT_INSTRUMENTED**.
- `crates/burn_webgpu_backend/src/aof_r1_kv_capacity_consumer.rs` provides read-only tree, incremental and chunked programs. They are opt-in candidate APIs, not proof of genuine selected-route consumption.
- Existing independent shaders do **not** establish their own actual-model Q/K/V provenance.

### 1.2 The OBSERVE backing is shorter lived than the next consumer

`crates/model_core/src/aof_r1_prefix_commit.rs` currently owns `cf5_shadow: Option<ArkCf5ObserveBlock>` inside `ArkPendingPrefix`.

`crates/model_core/src/aof_r1_runtime.rs::aof_r1_adopted_step()` consumes `pending` and does not restore it when `pending.remaining() == 0`; its `cf5_shadow` is therefore not accessible to subsequent ordinary decode or a new verifier attempt.

`ArkCf5ObserveBlock::read_view()` currently checks **the original `proposal_round` and attempt identity**, together with current canonical length/generation. A later proposal is not automatically authorized to borrow it.

**Required dependency order:** lifetime handoff **before** next-consumer invocation. Merely adding an `observe_decode_candidate()` call without a valid backing owner is not an implementation of this revision.

### 1.3 Native source boundaries

- `crates/model_core/src/aof_r1_verification.rs::NativeWgpuModel::aof_forward()` is private, and its `q/k/v`, `pk/pv`, tree descriptors and original attention context are local to its layer loop.
- `crates/model_core/src/decode_state.rs::forward_block_decode()` computes `canonical_qkv_prepared()` and then chooses `HeadwiseCommitted`, `TensorCubeActualCommitted` or `BurnFallbackRequired`, with a separate `burn_remainder` branch.
- `forward_block_chunked()` computes the same canonical Q/K/V and selects headwise versus Burn, with `DecodeStepSpan` and chunk-route readiness.
- `crates/model_core/src/model_layers.rs::grouped_query_attention()` has no built-in chunk-causal mask. It is not a substitute for independently observed headwise route masking.

The first three files `aof_r1_verification.rs`, `native_wgpu.rs`, `model_layers.rs` are included in `shared_lm_training_source_digest()`. Direct modification would change the existing head checkpoint's exact training-source identity.

**Baseline classification:** SOURCE-CONFIRMED. Actual Rust compile and GPU execution of these candidate modules remain UNKNOWN.

---

## 2. Implementation partition

| Substep | Owner | Deliverable | Admission |
|---|---|---|---|
| **R1-A** | `aof_r1_prefix_commit.rs`, `aof_r1_runtime.rs`, `aof_r1_kv_block_authority.rs` | Bounded session-local completed-OBSERVE backing handoff | Exact old/new identity + completion + no tail exposure |
| **R1-B** | `decode_state.rs`, existing `aof_r1_kv_consumer_bridge.rs` | Genuine Q/K/V hook in selected incremental branch | Natural selected route observed, same-source context parity |
| **R1-C** | `decode_state.rs`, route receipt | Genuine Q/K/V hook in supported chunked branch | Actual `DecodeStepSpan`/visibility authority, no inferred mask |
| **R1-D** | `aof_r1_runtime.rs`, verifier callsite discovery | Private-verifier seam proof or explicit HOLD | No duplicate verifier / training digest drift |
| **R1-E** | `aof_r1_cf5_qualification_cli.rs`, new validator | Physical matrix, fail-closed receipts and lineage | Real WGPU + no fabricated full-C PASS |

R1-A must precede R1-B/R1-C. R1-D can proceed independently as an evidence-gated discovery, but may not claim FULL CF5-C closure solely through a separate GPU shader.

---

## 3. R1-A: session-local completed shadow ownership

### 3.1 Owner

Extend the existing `ArkDecodeSession` / explicit decode session handoff, not a global cache, static singleton, process-wide device registry, or detached host tensor list.

A conceptual type, **not an assertion that it exists**:

```rust
struct ArkCf5CompletedObserveLease {
    shadow: ArkCf5ObserveBlock,
    origin: ArkAttemptIdentity,
    published_prefix: usize,
    canonical_past_at_handoff: usize,
    canonical_generation_at_handoff: u64,
    session_epoch: u64,
    physical_owner_digest: String,
    terminal_observation: ArkCf5HandoffStatus,
}

enum ArkCf5HandoffStatus {
    ParkedForReadOnlyObservation,
    Consuming,
    RetirementPending,
    Retired,
    QuarantinedTerminal,
}
```

The real code may use existing owner structs instead of introducing redundant layers. `ArkDecodeSession` is already present as `DecodeState::aof_r1_session` and is the preferred authority anchor. Observe the current take/replace mechanics before adding borrows, so `self`/`state` borrowing does not manufacture a new alias.

### 3.2 Move/retire boundary

```text
one or more successful CF5 OBSERVE `compare_next()`
    ↓
canonical publication of exactly k tokens (0 <= k <= accepted)
    ↓
no in-flight GPU work using shadow OR completion tracked by owning lease
    ↓
ArkPendingPrefix terminal/cancel/partial suffix boundary
    ↓
validate: every published KV position has compared parity
    ↓
MOVE shadow into bounded session-local observe owner
    ↓
next selected native reader obtains borrow-scoped read capability
    ↓
real Queue completion / observer retirement
```

Never clone a full `[H,C,W]` backing just to keep it alive. Existing `Tensor` handles may be moved or shared only under their legitimate WGPU owner/lifetime contract.

**Partial publication:** `published_prefix=k` may be less than `accepted`. Only `[0,T+k)` can be read. The physically prepared tail stays noncanonical and hidden.

**Lifetime bound:** at most one parked completed OBSERVE backing per decode session unless a separately budgeted bounded ring is explicitly justified. Replacing a parked backing requires completing/retiring its read work first. No silently accumulating old backing across proposal rounds.

### 3.3 No implicit fresh authority

The origin `ArkAttemptIdentity` remains immutable. A subsequent proposal may have a different `proposal_round`; it must never be made to pass the old `read_view()` simply by rewriting that field or weakening generation validation.

Introduce a distinct **handoff/rebind receipt**, conceptually:

```rust
struct ArkCf5ConsumerReadPermit<'a> {
    backing: &'a ArkCf5CompletedObserveLease,
    consumer_session: &'a BoundDecodeSessionContract,
    visible: usize,
    canonical_generation: u64,
    owner_generation: u64,
    consumer_route: ArkCf5ConsumerRoute,
}
```

Its constructor SHALL compare: model/checkpoint/tokenizer source; decode session ID and epoch; original physical device/queue owner; old completed publication state; current canonical K/V content generation and `[0,V)` logical bytes; source hash; and the new consumer's exact route identity. A new proposal round is allowed **only through this explicit proven handoff**, not by pretending to be the old proposal.

### 3.4 Invalidation

On cancellation, EOS/stop finalization, session restart, model reload, adapter/runtime binding change, new KV generation, or a new canonical append that changes the readable prefix, the old capability must become stale. Await or defer retirement of any submitted read-only GPU work under the existing queue completion authority. Do not release before completion.

If handoff is not legal, record `HOLD_CF5_C_R1_SHADOW_HANDOFF_UNAVAILABLE` and do not run a substitute shadow against a differently prepared KV source.

---

## 4. R1-B: actual ordinary incremental Q/K/V callsite

**Target:** `crates/model_core/src/decode_state.rs::forward_block_decode()` only, within the actual selected native path.

Capture borrow/handle references immediately after:

```rust
let (q, k, v) = layer.canonical_qkv_prepared(x, &prepared_runtime_loras);
```

Before `reshape/swap_dims`, these have contiguous layouts:

```text
q: [1,1,Hq*D]
k: [1,1,Hkv*D]
v: [1,1,Hkv*D]
```

Keep canonical `q/k/v` processing and `cat_seq_dim_4()` unchanged. Any extra tensors belong only to opt-in `OBSERVE` and must not be treated as an optimization of canonical decode.

**Selected route qualification:**

```text
burn_remainder=true
    -> selected explicit quarantined-remainder Burn branch

execute_incremental_attention_via_headwise(...)
    -> HeadwiseCommitted          : UNSUPPORTED_FOR_R1_B
    -> TensorCubeActualCommitted  : UNSUPPORTED_FOR_R1_B
    -> BurnFallbackRequired      : eligible Burn shadow comparison
```

Do not claim `OrdinaryIncrementalBurn` merely because a Burn expression can be run alongside a real headwise/TensorCube winner.

At the original selected-route boundary, compare the real context against the newly dispatched shadow. The shadow's `[1,1,Hq*D]` output and the native context heads `[1,Hq,1,D]` must be compared under explicit equivalent-layout indexing; **do not use a CPU materialization as the comparison authority**.

Required physical proof:

```text
same true q/k/v projection tensor owners
same actual old prefix (via completed CF5 handoff)
same D/Hq/Hkv and q_head -> kv_head mapping
same canonical visible T
same selected fallback route and layer
same adapter/prepared-LoRA binding
same real Queue completion
finite numeric context + existing tolerance / first mismatch
```

**Failure precedence:** an observer mismatch or observer dispatch error after the selected canonical computation cannot rewind already published canonical KV/token state. Record a nonpromoting qualification failure and retire the shadow safely. Never turn diagnostic failure into a fabricated canonical decode failure after publication.

---

## 5. R1-C: selected chunked Q/K/V callsite

**Target:** `crates/model_core/src/decode_state.rs::forward_block_chunked()`.

Capture actual pre-reshape `canonical_qkv_prepared()` tensors with `Q >= 2` and the corresponding `DecodeStepSpan`, `chunk_id`, `HeadwiseCausalPositionSnapshot`, generation binding, readiness receipt, and selected execution outcome.

Do not infer a universal causal window from `i <= query_index`. The source-visible generic Burn fallback calls `grouped_query_attention()` over the concatenated cache without applying an explicit chunk mask **inside that primitive**. However, a route-specific visibility vector must be derived from its **actual selected route contract** and bound to a receipt; a different headwise causal policy must not be silently reconciled.

Required route matrix:

| Selected physical route | R1-C behavior |
|---|---|
| `burn_remainder` explicit Burn | OBSERVE only with exact original visibility contract |
| `BurnFallbackRequired` | OBSERVE only after receipt-proven visibility |
| `HeadwiseCommitted` | `UNSUPPORTED_ROUTE`; do not substitute Burn or claim parity |
| Route identity unknown | `HOLD_CF5_C_R1_CHUNK_VISIBILITY_UNRESOLVED` |

The candidate backend already requires caller-supplied `per_query_staged_visible: &[u32]`. This vector must be derived from the actual selected route, checked once per query (length, bounds, generation), and hashed into the physical receipt.

If no route-local visibility proof exists, classify `HOLD`, not zero mismatch and not full chunked parity.

Keep `ChunkedKvAppendTransaction`, returned cache tensors, and canonical outputs unchanged.

---

## 6. R1-D: real verifier seam admission

**Target:** the actual verifier `NativeWgpuModel::aof_forward()` loop in `crates/model_core/src/aof_r1_verification.rs`, without changing its training-digest-covered bytes.

The current source **does not expose** its local `q/k/v`, `tree`, `pk/pv` and `ctx` to a sibling module. A second implementation re-running projections is at best an independent fixture, not the natural production verifier callsite.

R1-D SHALL perform an exact demand-site/seam audit:

1. Identify whether any existing production-owned callable hook already exposes the **same layer/row/Q/K/V/context tensors** without cloning the whole verifier or changing any of the 19 training-hashed files.
2. If such a hook is proven, attach the existing `ArkKvStridedReadView`/capacity shader and compare against **the actual verifier-selected output** without altering canonical results.
3. Otherwise emit **`HOLD_CF5_C_R1_VERIFIER_PRIVATE_ENTRY_UNREACHABLE`** and a source-path/line/evidence manifest. Do not invent a visibility override or pretend a parallel verifier is the same authority.
4. If training-hashed code must change, open an explicit **separate checkpoint-lineage revision**. Old head checkpoints keep their original training-source digest; migration or requalification must be verifiable, never accomplished by editing manifests/hashes to pass a gate.

**Exit boundary:** real tree/linear callsite qualification is an independent physical condition. Successful standalone tree WGSL dispatch alone does not clear it.

---

## 7. Actual prefix layout and visibility law

For each matched layer:

```text
T = canonical prefix at shadow creation
L = verified accepted length (1..=min(depth+1,5))
C = T+L             // physical capacity
k = canonically published tokens, 0<=k<=L
V = T+k             // strictly visible prefix

physical(h,t,d) = (h*C+t)*D+d,       0<=t<V
compact(h,t,d)  = (h*V+t)*D+d,       0<=t<V
```

For ordinary decode the current staged token is stored separately at logical position `V`. For chunked decode, staged K/V `[V,V+Q)` are separate and may be read only according to proven selected-route visibility.

Every reader must check K and V **independently**; poisoning one side alone must fail. No shader may read `[V,C)` simply because the physical binding has that capacity.

Exact GQA requirement: `Hq % Hkv == 0`, mapped KV head `h / (Hq/Hkv)`, same selected head_dim and scale as canonical route.

---

## 8. Comparison authority and GPU cost attribution

A read-only consumer may add OBSERVE-only GPU dispatches and bounded parity readback; it may not introduce an unconditional extra GPU synchronization or additional full prefix host readback into normal `LEGACY` generation.

**Required distinction:**

```text
canonical CF4 submit / D2H / wait
    != CF5-C-R1 OBSERVE-only submit / D2H / wait
```

Prefer bounded GPU comparison/reduction (first failing layer, head, row, component, max numerical error) with explicit finite flags; no `Vec<f32>` containing full context or full prefix readback as the ordinary proof route. Existing numeric tolerance is inherited exactly; do not invent an `atol/rtol` promotion threshold.

The currently implemented independent consumer shaders perform their own softmax reduction order. Bitwise equality of floating context is not automatically required; exact Q/K/V raw bit parity, numeric context tolerance, winner parity where applicable, and no near-tie rule relaxation are separate metrics.

Report physical GPU execution time only if timestamp queries actually measured it. Host callback wait is host wall time, not kernel duration. Source/STATIC counters are not measured VRAM or bandwidth.

---

## 9. Failure ordering / observer side effects

Observation mode must preserve terminal behavior for:

```text
normal complete block
partial accepted prefix
EOS / StopSequence / MaxNewTokens
cancel before publication / after partial publication
emit failure and ACK distinction
stale owner / renewed proposal
ordinary decode after completed prefix
chunked decode after completed prefix
partial layer failure
Queue callback failed / completion unavailable
repeated fresh session / device or queue drift
```

Legacy publishes independently; the shadow may be retired/discarded but never promoted into the canonical cache. A failed OBSERVE comparison must not manufacture token/KV/receipt publication or erase already-published history.

No ordinary mutable `Arc<Mutex<...>>` registry is justified by merely needing a one-time session-local read-only probe. Keep owner scope narrow.

---

## 10. Explicit mode/route states

Prefer match-based states, not success-shaped booleans:

```rust
// Conceptual, not an existing public enum.
enum ArkCf5ConsumerProbeOutcome {
    ObservedPhysicalParity,
    ObservedPhysicalMismatch,
    BlockedMissingHandoff,
    BlockedStaleOwner,
    BlockedUnqualifiedRoute,
    BlockedPrivateVerifierEntry,
    BlockedMissingChunkVisibility,
    NotRun,
}
```

Every case must record actual selected route, not merely requested route. A numeric rejection is not proof of resource lifetime failure; a completion callback is not proof of numerical equality.

Global `ArkKvBlockCommitMode::Active` remains **HOLD**, irrespective of R1 outcomes.

---

## 11. Source files to touch (proposal, not applied)

| Existing path | Surgical change |
|---|---|
| `crates/model_core/src/aof_r1_prefix_commit.rs` | Expose one terminal, moved OBSERVE backing at the exact pending retirement boundary; no new canonical staging/publish ordering. |
| `crates/model_core/src/aof_r1_runtime.rs` | Own bounded parked shadow in `ArkDecodeSession` with explicit later-consumer handoff and retirement. |
| `crates/model_core/src/aof_r1_kv_block_authority.rs` | Split origin attempt identity from subsequent read permit; leave original same-attempt checks intact for the existing caller. |
| `crates/model_core/src/aof_r1_kv_consumer_bridge.rs` | Route-bound context comparison and typed permit consumer; do not relabel headwise/TensorCube as Burn. |
| `crates/model_core/src/decode_state.rs` | OBSERVE-only true Q/K/V hooks in incremental/chunked chosen branches, after obtaining correct session-local backing. |
| `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs` | Bind parent CF5-C identity, per-route execution coverage and first failure; no forged terminal token. |
| `crates/model_core/src/aof_r1_admission.rs` | Extend actual-byte `ark_runtime_source_digest()` to all new Rust/receipt/WGSL paths. |
| `tools/validate_ash_aof_r1_cf5_c_capacity_strided_consumer_static.py` or new R1 validator | Source-path, negative mutation and training-digest preservation. |

**Frozen input set:** the 19 exact `shared_lm_training_source_digest()` files, especially `aof_r1_verification.rs`, `model_layers.rs`, `native_wgpu.rs`, and `Cargo.lock`. No changed-byte exception in this revision. If scope forces one, stop and authorize a separate lineage revision.

Keep existing WGSL filenames, crate names, and public API conventions. Add new WGSL only when source-proven semantics require it; no speculative shader proliferation.

---

## 12. Static and negative gates

The R1 static validator SHALL establish:

```text
real callsite uses canonical_qkv_prepared-produced Q/K/V
no independently regenerated Q/K/V passed as "canonical"
selected route is observed and recorded
finished pending backing moved to session owner, not dropped
at most one parked owned backing per session
old proposal id not rewritten for a new consumer
explicit consumer-generation rebind with exact canonical state
K/V tail checks independently present
no global map / host full-prefix readback
no type shape disguise
no new canonical submit / mutation introduced
no Observer success promotes Active
training source hash inputs byte-preserved
all new paths covered by runtime source digest
CF4 counters exclude shadow GPU operations
```

Mandatory negative fixtures:

1. Shadow dropped at pending termination: reject.
2. Rebind into different session/epoch/owner/proposal without handoff evidence: reject.
3. Rebind after an intervening canonical KV append: reject.
4. Accept physically prepared unpublished tail as visible: reject.
5. K-only hidden-tail read, then V-only: both rejected.
6. Headwise/TensorCube selected path relabeled as Burn: reject.
7. Chunk visibility vector inferred rather than bound to selected route: reject.
8. Shadow context substituted into canonical output: reject.
9. Training-hashed source byte changed: reject.
10. New shader/callsite source absent from runtime digest: reject.
11. Fake numerical/completion or unobserved dispatch count: reject.
12. Full-C PASS token emitted with verifier `NOT_INSTRUMENTED`: reject.

**Gate independence:** legacy CF1/CF2/VH6 static exact-byte checks which were superseded by the existing CF4 `aof_r1_prefix_commit.rs` instrumentation remain historical conflict evidence; do not mark them full PASS by modifying expected SHA silently.

---

## 13. Compile qualification

First restore exact external workspace inputs; a missing `vendor/sherpa-rs-main/crates/sherpa-rs` package is a dependency-input HOLD, not proof the CF5-C-R1 Rust source is wrong.

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_consumer_bridge --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_block --release --locked -j 1
```

Target/feature presence must be confirmed from the source manifest. The above commands are **instructions, not execution results**. Register and physically parse/validate any changed WGSL through the project's existing Naga path; a static filename list alone is not native validation.

---

## 14. Runtime and physical matrix

Bind **one exact source/tree, model/tokenizer/checkpoint pair, same WGPU Device/Queue and held-out/qualifying prompt identity** to the campaign. Each leg requires a fresh state/receipt; do not reuse another run's physical completion proof.

| Axis | Cases | Qualification |
|---|---|---|
| Depth | D1 / D2 / D4 | Actual AOF executed, supported prefix length only |
| Published prefix | `0, 1, 2, 3, 4, 5` where legal | Exact visible length; 8 = NOT_APPLICABLE |
| Shadow lifetime | full commit, partial stop, cancel, session restart | bounded parked owner, tail invisible, safe retirement |
| Incremental | true BurnFallbackRequired; explicit burn remainder | actual same-source q/k/v and context parity |
| Incremental non-Burn | HeadwiseCommitted / TensorCubeActualCommitted | explicit UNSUPPORTED, not numeric PASS |
| Chunked | selected proven Burn route Q>=2 | per-query visibility and context parity |
| Chunked non-Burn | HeadwiseCommitted | explicit UNSUPPORTED |
| Verifier | real tree/linear native entry with same q/k/v | PASS only when legitimate native seam observed; else HOLD |
| Failure | stale owner, changed epoch, callback missing, duplicate retire, K/V tail | no publication or false completion |

Commit matrix inherits EOS / stop / max / cancel / emit-failure / duplicate consume / stale identity / suffix-discard from VH6/CF5. A leg failing before actual GPU submission must show `NOT_SUBMITTED`, not `observed_submit_count=0` interpreted as physical PASS.

---

## 15. Receipt schema and first-failure attribution

Suggested audit-only output:

```text
aof_r1_cf5_c_r1_native_consumer_callsite_handoff_receipt.json
schema = ash.aof_r1.cf5.c.r1.native_consumer_handoff.v1
```

Required fields:

```text
source_tree_sha256
training_source_digest_before
training_source_digest_after
runtime_source_digest
binary_sha256
model_digest, tokenizer_digest, checkpoint_digest
physical_device_id, physical_queue_id, session_epoch
origin_proposal_round, original_kv_generation
handoff_sequence, handoff_visible_len, backing_capacity
producer_compare_count, published_prefix_count
parked_lease_count, retired_lease_count, pending_completion_count
post_handoff_consumer_generation, consumer_route_selected
native_qkv_actual_callsite_observed  // Some(true) only if actually executed
actual_submit_count                 // Option or explicitly unobserved
actual_completion_count             // Option or explicitly unobserved
per_route_context_parity
verifier_tree_status, verifier_linear_status
ordinary_burn_status, ordinary_headwise_status, ordinary_tensorcube_status
chunked_burn_status, chunked_headwise_status
first_mismatch: layer, row/query, head, component, generation, selected_route
canonical_token_text_stop_parity
canonical_kv_generation_parity
CF4_canonical_counters_unchanged
production_admission = false
active_block_commit = false
performance_status = NOT_MEASURED
status, explicit_blockers, receipt_hash
```

Any missing proof remains `UNKNOWN`, `NOT_RUN`, `NOT_APPLICABLE` or a named `HOLD`, **never a literal zero or boolean false masquerading as a measurement**.

---

## 16. Failure classes

```text
HOLD_CF5_C_R1_SHADOW_HANDOFF_UNAVAILABLE
HOLD_CF5_C_R1_VERIFIER_PRIVATE_ENTRY_UNREACHABLE
HOLD_CF5_C_R1_CHUNK_VISIBILITY_UNRESOLVED
HOLD_CF5_C_R1_ROUTE_UNSUPPORTED
FAIL_CF5_C_R1_ORIGIN_IDENTITY_DRIFT
FAIL_CF5_C_R1_CROSS_SESSION_REBIND
FAIL_CF5_C_R1_STALE_GENERATION_REBIND
FAIL_CF5_C_R1_UNPUBLISHED_TAIL_VISIBLE
FAIL_CF5_C_R1_KV_LAYOUT_OR_GQA_DRIFT
FAIL_CF5_C_R1_NUMERIC_CONTEXT_MISMATCH
FAIL_CF5_C_R1_CROSS_ROUTE_FALSE_PARITY
FAIL_CF5_C_R1_PRECOMPLETION_SHADOW_RETIREMENT
FAIL_CF5_C_R1_DUPLICATE_REBIND_OR_RETIRE
FAIL_CF5_C_R1_TRAINING_DIGEST_DRIFT
FAIL_CF5_C_R1_RUNTIME_SOURCE_DIGEST_GAP
FAIL_CF5_C_R1_CANONICAL_PUBLICATION_DRIFT
FAIL_CF5_C_R1_FAKE_GPU_COMPLETION
FAIL_CF5_C_R1_EARLY_ACTIVE_PROMOTION
```

---

## 17. Completion law and successor

There are **separate** admissible achievements:

```text
A. SHADOW HANDOFF QUALIFIED
  bounded move from terminal prefix -> session owner
  origin and later consumer identities proven
  no stale/tail read
  completion/retirement closed

B. INCREMENTAL BURN SELECTED-ROUTE PARITY QUALIFIED
  A true + actual selected Burn q/k/v + same GPU context comparison

C. CHUNKED BURN SELECTED-ROUTE PARITY QUALIFIED
  A true + selected route visibility proven + actual GPU context comparison

D. VERIFIER TREE / LINEAR QUALIFIED
  actual private-verifier production entry observed without training-lineage violation
```

A SOURCE/STATIC bake of any of A/B/C/D does not confer physical acceptance. `PASS_AOF_R1_CF5_C_R1_NATIVE_CONSUMER_HANDOFF` may be issued only when the **specified R1 matrix** has real COMPILE/RUNTIME/PHYSICAL evidence with all supported route legs either passing or explicitly classified as excluded by predeclared scope, with no false full-C claim. If the required real verifier entry remains blocked, the R1 aggregate must carry `HOLD_VERIFIER_SEAM` and must **not** be used as `PASS_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE`.

**CF5-C full closure requires the real tree/linear, ordinary decode, chunked and selected headwise/TensorCube semantics demanded by the parent CF5-C contract.** No optional-shader experiment or Burn-only matrix is a substitute.

**CF5-D `ACTIVE` remains disabled regardless of these partial statuses.**

### Final invariant

```text
REAL CANONICAL Q/K/V PRODUCER
+
ORIGIN-SEALED COMPLETED SHADOW
+
EXACT SESSION / GENERATION HANDOFF
+
SELECTED-ROUTE READ-ONLY GPU CONSUMPTION
+
NO CANONICAL PUBLICATION CHANGE
+
TRUTHFUL ROUTE-LOCAL RECEIPTS
=
CF5-C-R1 OBSERVE CALLSITE EVIDENCE

NOT YET = CF5-C FULL CLOSURE
NOT YET = CF5-D ACTIVE PUBLICATION
```

---

## 18. 2026-10-08 SOURCE bake evidence / explicit partial status

The source ZIP **partially implements this contract**. This is not the physical acceptance required by §17.

### Exact artifact lineage

- Parent full ZIP SHA256: `944ba80b9e08e1615180021db1216dc31ca0c001000a619260ad137cc3823b9d`.
- Output `ASH_PASS3_AOF_R1_CF5_C_R1_NATIVE_CONSUMER_CALLSITE_HANDOFF_CODE_ONLY.zip`, SHA256 `d568bc6a3f9a9d75b9d5b9b684c8e180c83578330f9262eecafdef0d063363fd`.
- Overlay `ASH_AOF_R1_CF5_C_R1_NATIVE_CONSUMER_CALLSITE_HANDOFF_OVERLAY_CODE_ONLY.zip`, SHA256 `e609ecf9270b98c56425ffa7066530edb9faba60cdc45827b41f5f9617415930`.
- 8,731 files; ADD 1 / MODIFY 9 / DELETE 0. ZIP CRC and exact stored-byte comparison PASS.
- Full per-file evidence: `ASH_AOF_R1_CF5_C_R1_BAKE_MANIFEST.json`. Source validation: `ASH_AOF_R1_CF5_C_R1_STATIC_RECEIPT.json`.

### R1-A SRC implemented

`ArkCf5CompletedObserveLease` moves a fully compared terminal pending shadow into one session-local `ArkDecodeSession.parked_cf5`; no global cache. `read_views` checks original model, tokenizer, request, session+position epoch, device+queue, committed visible KV length and generation. Original proposal round is never rewritten. During original decode the parked lease is lent to transient `DecodeState` then restored. Canonical KV remains legacy.

### R1-B SRC implemented

Selected real ordinary `forward_block_decode` captures actual `canonical_qkv_prepared()` Q/K/V and only observes actual Burn fallback/remainder routes through the existing read-only capacity-strided GPU consumer. Actual canonical GPU context is never replaced. Optional sampled and greedy callsites carry the permit; no parked lease means no comparison. Nonzero maximum absolute error is an explicit numerical **HOLD**, not an automatically accepted tolerance. Even zero max-error does not prove bitwise parity; `context_bitwise_exact=None`.

### R1-C SRC implemented

Actual chunked `forward_block_chunked` captures selected Q/K/V and only selected Burn fallback/remainder. For this current Burn implementation, `grouped_query_attention()` consumes the whole staged K/V without an intra-chunk causal mask, so the shadow's per-query staged visibility follows that exact selected route. It is NOT a headwise/TensorCube policy. The existing commit-stability case telemetry carries `aof_r1_cf5_c_r1_observations` and the CF5 qualification CLI reports route-local counts and blocked cases without any full-R1 PASS token. Shadow GPU work is excluded from CF4 canonical attribution.

### Actual SOURCE diff

Modified:
- `crates/model_core/src/aof_r1_admission.rs`
- `crates/model_core/src/aof_r1_kv_block_authority.rs`
- `crates/model_core/src/aof_r1_kv_consumer_bridge.rs`
- `crates/model_core/src/aof_r1_prefix_commit.rs`
- `crates/model_core/src/aof_r1_runtime.rs`
- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/generation_sampling.rs`
- `crates/model_core/src/generation_telemetry.rs`
- `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs`

Added: `tools/validate_ash_aof_r1_cf5_c_r1_native_consumer_handoff_static.py`.

### Evidence

| Class | Status |
|---|---|
| R1 SOURCE/STATIC | **66/66 PASS** |
| R1 negative mutations | **10/10 correctly rejected** |
| CF5-C / CF5-A+B / CF4 / CF3 parent static | **62/62, 73/73, 65/65, 51/51 PASS** |
| Legacy CF1/CF2/VH6 static | **51/52** due to CF4+-superseded `aof_r1_prefix_commit.rs` byte preservation check |
| 19-input training checkpoint source digest | **unchanged** `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283` |
| Rust COMPILE | NOT_RUN |
| Native Naga and physical WGPU | NOT_RUN |
| Numeric parity and performance | UNKNOWN / NOT_MEASURED |

**R1-D verifier remains `HOLD_CF5_C_R1_VERIFIER_PRIVATE_ENTRY_UNREACHABLE`.** Private `aof_forward` native Q/K/V cannot yet be reached without editing the checkpoint training-digest source or an authorized native seam. Headwise/TensorCube routes remain unsupported. **R1-E actual GPU qualification remains NOT_RUN.** `CF5-D ACTIVE` stays forbidden, and no complete CF5-C / CF5-C-R1 or performance PASS may be issued.

To advance: restore exact workspace external path input (no fake vendor crate); run Cargo metadata, backend/model_core/orchestrator release checks and native Naga; run the same-source D1/D2/D4 physical CF5-C OBSERVE campaign, check completion, native context comparison, tail visibility, canonical OFF parity and receipt lineage. Then isolate the private-verifier seam in CF5-C-R2, if required. Source-only checks cannot substitute for those steps.
