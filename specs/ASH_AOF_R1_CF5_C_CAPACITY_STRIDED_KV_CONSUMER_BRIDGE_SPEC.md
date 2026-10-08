# AOF-R1-CF5-C

## CAPACITY-STRIDED KV CONSUMER BRIDGE

**Revision:** `AOF-R1-CF5-C`  
**Parent:** `AOF-R1-CF5-A/B` OBSERVE candidate from `ASH_PASS3_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY_CODE_ONLY.zip`  
**Successor:** `AOF-R1-CF5-D` Canonical Block Publication, then `CF5-E` Physical/Performance Admission  
**Class:** Native WGPU KV-reader ABI, attention input routing, physical parity qualification  
**Status (2026-10-08):** **PARTIAL SOURCE BAKE.** C1 borrower/view and C2/C3/C4 candidate shader APIs were baked; genuine canonical verifier/ordinary decode/chunked selected-route invocation is **NOT INSTRUMENTED**. Rust COMPILE, native Naga, RUNTIME, PHYSICAL, PERFORMANCE are **NOT_RUN / NOT_MEASURED**. Full CF5-C PASS and ACTIVE remain HOLD.

```text
AOF-R1-CF5-C

CAPACITY-STRIDED KV CONSUMER BRIDGE

+ CF5-A/B CAPACITY BACKING / GPU STAGE / PARITY SOURCE PRESERVATION
+ PHYSICAL CAPACITY C / LOGICAL VISIBLE LENGTH V SEPARATION
+ BACKING-OWNED STRIDED READ DESCRIPTOR
+ EXACT OWNER / SESSION / EPOCH / GENERATION BINDING
+ RAW WGSL CAPACITY-STRIDED KV READ (NO COMPACT MATERIALIZATION)

+ AOF VERIFIER TREE / LINEAR PREFIX READ COMPATIBILITY
+ ORDINARY INCREMENTAL DECODE PREFIX + CURRENT TOKEN READ
+ CHUNKED DECODE PREFIX + STAGED CHUNK READ
+ GQA HEAD ROUTING / EXISTING VISIBILITY RULE PRESERVATION
+ HEADWISE / TENSORCUBE / BURN ROUTE ATTRIBUTION

+ NON-PUBLISHING LEGACY-VS-STRIDED OBSERVE
+ FIRST-MISMATCH PER LAYER / ROUTE / QUERY / POSITION
+ D1 / D2 / D4 AND PARTIAL PREFIX MATRIX
+ NO UNPUBLISHED SUFFIX READ
+ NO HIDDEN KV REPACK / FULL-PREFIX ALLOCATION
+ NO NEW PRODUCTION READBACK OR QUEUE BARRIER

+ 19-FILE HEAD TRAINING SOURCE DIGEST EXACT PRESERVATION
+ AOF RUNTIME SOURCE / WGSL BYTES IDENTITY EXTENSION
+ PARENT CF1 / CF2 / VH6 / CF3 / CF4 / CF5-A/B PRESERVATION

+ DEFAULT LEGACY
+ OBSERVE IS NON-PUBLISHING
+ ACTIVE REMAINS HOLD UNTIL CF5-D
+ NO SPURIOUS PASS / NO PERFORMANCE PROMOTION
```

---

## 0. Source-derived facts and limits

The following are **SOURCE-observed in the supplied CF5 full ZIP**, not compile or physical results.

| Current source | Observed contract / obstruction |
|---|---|
| `crates/model_core/src/aof_r1_kv_block_authority.rs` | `ArkKvBlockLayout` defines `past`, `accepted`, `capacity`, `heads`, `width`, `visible_at()` and `capacity_index()`. `ArkCf5ObserveBlock` holds `[1,H,C,W]` GPU shadow tensors. `ACTIVE` currently returns `HOLD_CF5_LOGICAL_VIEW_UNAVAILABLE`. |
| `crates/burn_webgpu_backend/src/shaders/aof_r1_block_prefix_stage.wgsl` | Capacity-strided shadow `[H,C,W]` preparation and accepted suffix scatter; no canonical publication. |
| `crates/burn_webgpu_backend/src/shaders/aof_r1_block_prefix_compare.wgsl` | Raw `u32` K/V comparison of visible `[0,V)` against compact canonical staging. |
| `crates/model_core/src/aof_r1_prefix_commit.rs` | Canonical `stage_kv()` builds actual compact `[1,H,past+1,W]` tensors; legacy publication still authoritative. |
| `crates/model_core/src/aof_r1_verification.rs` | Verifier requires compact `[1,kv_heads,past,head_dim]` and calls `reshape([past * kv_hidden])`; its tree/linear attention consumes flat compact prefix. |
| `crates/model_core/src/decode_state.rs` | Incremental and chunked forward create `cat_seq_dim_4(cached, new)` and feed resulting compact K/V into GQA, headwise, or TensorCube routes. |
| `crates/model_core/src/native_wgpu.rs` | `cat_seq_dim_4()` is `Tensor::cat(..., 2)`. Existing consumers compare actual `dims()[2]` with committed/visible length. |
| `crates/burn_webgpu_backend/src/raw_bridge.rs` | `RawWgpuBufferLease` binds a contiguous physical buffer segment; it carries no separately enforced KV logical-length/physical-stride attention ABI. |
| `crates/model_core/src/aof_r1_shared_lm_head_math.rs` | `shared_lm_training_source_digest()` includes 19 exact source files, including model-core `aof_r1_verification.rs`, `native_wgpu.rs`, and `model_layers.rs`. |

**UNKNOWN / 판단불가:** Rust compile outcome, numerical equivalence of a new attention kernel, physical resource currentness, performance, and whether every native consumer can be reached without changing a checkpoint-hashed source file.

CF5-C does **not** assume that a contiguous `[H,C,W]` buffer can be reinterpreted as a compact `[H,V,W]` Tensor for `V < C`.

---

## 1. Patch boundary and authority

CF5-C creates a **reader** for existing CF5-A/B GPU shadow backing. It does not change what is canonical.

```text
Existing verified prefix
  → CF5-A/B prepare [H,C,W] once
  → Queue completion and owner pin
  → CF5-C capacity-strided attention reader (shadow only)
       ├─ tree/linear verifier comparison
       ├─ ordinary incremental comparison
       └─ chunked comparison
  → bounded parity receipt

Production still:
  Legacy compact KV → existing verification / decode → existing commit
```

In this revision the original compact Tensor remains the canonical producer and storage. `ArkKvBlockCommitMode::Active` must stay HOLD. `CF5-C` does not add `KvCache` capacity-backed publication or adjust EOS, stop, cancellation, emit, receipt or sampling.

---

## 2. Read-only KV descriptor SSOT

Introduce a narrowly owned concept, naming subject to current conventions:

```rust
// Specification type sketch, not existing compiled code.
struct ArkKvStridedReadView<'a> {
    key: &'a RawWgpuBufferLease,
    value: &'a RawWgpuBufferLease,
    layout: &'a ArkKvBlockLayout,
    visible_tokens: u32,         // V, never C
    backing_generation: u64,
    logical_content_generation: u64,
    source_session_epoch: u64,
    owner_identity_digest: &'a str,
}

enum ArkKvReadSource<'a> {
    CompactLegacy { /* existing tensor/lease authority */ },
    CapacityStrided(ArkKvStridedReadView<'a>),
}
```

This is **not** a generic Burn `Tensor` view and not a `#[repr(transparent)]` cast. `CapacityStrided` can only be created from a live, correct-session CF5 `ArkCf5ObserveBlock` and valid GPU leases. It may borrow the entire physical backing but can expose only `[0,V)` to consumers.

Required checks before any dispatch:

```text
0 < V <= C <= max_seq_capacity
H > 0, W > 0, element_size = 4 for this f32 contract
K/V physical region: exactly H*C*W*4 bytes per tensor
backing owner and active handle generation current
same device / same Queue as actual runtime
session ID / position epoch / model instance current
logical content generation matches selected V
buffer_offset + buffer_size checked / binding-limit admitted
no K/V output-input alias creating a write/read hazard
```

Lifetime: the descriptor cannot outlive its shadow backing, GPU submission, or pinned runtime owner. Proven completion is required before destruction/reuse; elapsed time is not a completion authority.

---

## 3. Physical index law

For batch size 1, head-major backing and logical visible prefix:

```text
P(h,t,d) = ((h * C + t) * W + d)
L(h,t,d) = ((h * V + t) * W + d)

h in [0,H)
t in [0,V)
d in [0,W)
```

`P` uses **physical capacity** and `L` is only a legacy-comparison index. Neither `V` nor `T` may substitute for `C` in physical indexing. Use checked host arithmetic and correctly guarded `u32` WGSL arithmetic, including the maximum addressable storage binding range.

Reject:

```text
physical-stride overflow
buffer binding length mismatch
K/V layout mismatch
attempted t >= V
attempted t >= C
incorrect GQA head remapping
read from future, rejected, or discarded suffix
```

`used_tokens`, `committed_token_count`, `KvCache.past_len`, and `KvPositionLifecycle.committed_past_len` remain **logical** counts, never reserved capacity.

---

## 4. GPU consumer contract, no hidden compaction

A new WGPU reader may bind the existing physical K/V buffers directly and produce a **small attention result Tensor** that is compatible with the rest of the native projection/MLP path.

Allowed:

```text
borrow existing K/V [H,C,W]
pass V and C in explicit GPU parameter block
compute attention directly using P(h,t,d)
write context [batch,query_len,q_heads,head_dim]
```

Forbidden inside the capacity reader:

```text
copy all [0,V) K/V to [H,V,W]
Tensor::cat of full old-prefix K/V merely for consumer convenience
copy-on-CPU / readback full K/V
reshape([H*V*W]) on a physical [H*C*W] backing
materialize compact staging under a different helper name
new per-token prefix-sized scratch allocation
```

**Important:** Producing the compact attention **output** is allowed. Producing a compact copy of the entire prefix K/V is not. Count both separately.

The new shader must keep the source values unrotated unless the specific existing route's canonical recipe proves a different transform. Do not introduce a new RoPE or softmax/masking convention as an unsolicited correction.

---

## 5. AOF tree/linear verifier consumer

Source: `model_core/src/aof_r1_verification.rs::aof_forward` → `burn_webgpu_backend::aof_r1_verification::ArkVerificationDevice::attention`.

Current prefix addressing is compact:

```wgsl
pk[(head * past + key) * dim + d]
```

CF5-C proposed strided qualifier:

```wgsl
pk[(head * capacity + key) * dim + d]
```

Only the **prefix read address** changes. Preserve the existing tree-attention visibility: root row, parent/ancestor traversal, depths, origin/anchor, tree-vs-linear case, suffix-node K/V indexing, GQA quotient, two-pass softmax, winner and near-tie contract. A verifier prefix with `V` visible tokens must pass `past = V`, not `past = C`.

Required outputs for the same real tree/root/owner:

```text
legacy logits/winners/near-tie classification
capacity-strided shadow logits/winners/near-tie classification
root and verified candidate identity
first mismatch: layer, row, head, output component, source position (if attributed)
```

Numerical error must be measured using the **existing** absolute/relative tolerance, without silently introducing a looser comparison. Same-operation bitwise comparison can be additionally reported, but is not an unproven blanket requirement for changed GPU reduction order.

**Entry-point warning:** model-core `aof_forward()` and its helper `aof_embed()` are private in the training-digest-covered file. An independent shadow kernel is not evidence that the **real verifier production entrypoint** can consume it. CF5-C must either establish a legitimate separate native seam using the existing canonical projections, or explicitly report `HOLD_CF5_C_VERIFIER_ENTRY_UNREACHABLE`. Never copy/paste a second entire verifier and claim it as the same canonical authority.

---

## 6. Ordinary incremental decode consumer

Source: `decode_state.rs::forward_block_decode`.

Current flow:

```text
q, k_new, v_new = canonical_qkv_prepared
k_cache = cat_seq_dim_4(cached_k, k_new)
v_cache = cat_seq_dim_4(cached_v, v_new)
attention(q, k_cache, v_cache)
```

CF5-C must evaluate attention from two typed sources without concatenating old-prefix K/V:

```text
prefix: capacity-backed [0,V), physical stride C
current single-token K/V: separate stage at logical position V
query: current q, q_len = 1
```

For key index `t`:

```text
0 <= t < V : read capacity backing using P(h,t,d)
t == V     : read current k_new/v_new using their canonical layout
t > V      : inaccessible
```

No CF5-C direct write into the canonical cache. The newly computed `context` is a non-publishing comparison result against the legacy ordinary-decode context for the same `q`, K/V, head mapping, currentness and feature-route identity.

Existing branches such as `HeadwiseCommitted`, `TensorCubeActualCommitted`, and `BurnFallbackRequired` must be observed separately. Do not silently substitute a direct raw shader for a selected production attention route or count a Burn fallback as a strided-reader success.

---

## 7. Chunked decode consumer

Source: `decode_state.rs::forward_block_chunked` and the existing chunk-generation receipt.

The new read contract must support:

```text
prefix [0,V) from [H,C,W]
staged chunk [V,V+Q) from existing qkv output
Q >= 2 for the chunked route
chunk ID and DecodeStepSpan authoritative
per-query visibility from the selected canonical route
```

CF5-C **must not invent a universal chunk-causal mask**. In the inspected source the generic Burn `grouped_query_attention()` path uses matmul+softmax, while the native headwise chunk route maintains separate causal/generation bindings. Each route's exact visibility law must be inventoried and preserved. If two production branches have different semantics, classify a `CONFLICT` and qualify them separately instead of silently reconciling.

For a proven causal chunk route only, query index `i` may read staged positions permitted by its existing causal-position authority, never a future staged position. For noncausal/legacy fallback, follow the actual selected source semantics, even if unusual; do not call a changed mask a parity fix.

Required identity:

```text
chunk_id
DecodeStepSpan
position/absolute_position_base
prefix generation
staged generation
committed token count
layer index
native route admission identity
```

Do not alter the existing `ChunkedKvAppendTransaction` or publish its shadow K/V. Headwise texture/persistent-KV routes that cannot consume a strided backing are explicit `UNSUPPORTED_ROUTE`, not silently successful.

---

## 8. GQA and attention math

For each relevant route verify:

```text
q_heads > 0, kv_heads > 0, q_heads % kv_heads == 0
kv_head = q_head / (q_heads / kv_heads)
head_dim exactly the model's dimension
prefix and staged-token Q/K/V values are same-source
scale / reduction / finite rules inherited from actual route
```

The CF5-A/B shadow stage is raw `u32` bit preserving. Consumer arithmetic is f32 and can differ with reduction order; classify numerical differences honestly. Measure finite logits/context, maximum absolute error, tolerance-qualified difference, winner equality where applicable, and first failing route/row/head/layer. Do not convert an unexplained mismatch into an automatic tolerance adjustment.

---

## 9. Session, generation and visibility admission

A capacity view is valid only for its own:

```text
model / tokenizer / checkpoint lineage
native owner and backing identity
same actual device / queue
AOF attempt and proposal round
DecodeState decode_session_id
position_epoch / absolute_position_base
expected committed content generation
verified accepted length
```

If `T` is the original canonical length and `k` tokens have been published by the legacy authority, the shadow logical view is `V = T + k`, `0 <= k <= L`, where `L <= min(5, depth+1)`.

Never use the prepared `T+L` length as `V` until those tokens are actually canonical. Test partial publication followed by another AOF verification, one ordinary incremental decode, and one chunked decode. A stale/aborted/restarted generation must invalidate all old view capabilities.

---

## 10. Failure and completion lifetime

If an OBSERVE consumer dispatch fails or reports mismatch:

```text
legacy canonical state remains unchanged by CF5-C
shadow work stops or reports failed route
shadow buffers retained until actual same-Queue completion
lease becomes eligible for retirement only after completion/currentness checks
```

A rejected numerical result does not prove GPU completion. A completion callback does not prove numerical parity. Preserve CF2 retirement contract, and never release/reacquire a capacity backing while a reader still uses it.

No host timeout, `Drop`, `mem::forget` or elapsed wall-clock interval may fabricate a successful retirement.

---

## 11. Modes and promotion boundary

```rust
// Conceptual, not yet a change to existing enum.
match mode {
    ArkKvBlockCommitMode::Legacy => legacy_canonical,
    ArkKvBlockCommitMode::Observe => legacy_canonical_plus_strided_shadow,
    ArkKvBlockCommitMode::Active => Err(HOLD_CF5_C_ACTIVE_REQUIRES_CF5_D),
}
```

The existing `HOLD_CF5_LOGICAL_VIEW_UNAVAILABLE` may remain the outer admission refusal until CF5-D implements real canonical ownership. Avoid adding a second silent Active flag. Any override must be explicitly classified as a **future semantics change**.

CF5-C `OBSERVE` can be functionally tested with extra GPU work. Extra observation submissions/readbacks belong to the **shadow** ledger and must not be mistaken for canonical CF4 traffic or throughput.

---

## 12. Source touch points: proposal, not applied changes

| File | Proposed scope |
|---|---|
| `crates/model_core/src/aof_r1_kv_block_authority.rs` | Expose a borrow-scoped `ArkKvStridedReadView` from the existing `ArkCf5ObserveBlock`; require current generation/visibility. |
| **New** `crates/model_core/src/aof_r1_kv_consumer_bridge.rs` | Read-route descriptor, genuine native shadow dispatch/reduction, parity/first-failure accounting. |
| `crates/model_core/src/decode_state.rs` | OBSERVE-only hooks around existing incremental/chunked consumer boundary; canonical path untouched. |
| `crates/model_core/src/aof_r1_runtime.rs` | Safe qualifier seam for the next real AOF verification where reachable without altering training-source identity. |
| `crates/burn_webgpu_backend/src/aof_r1_verification.rs` | Dedicated capacity-aware raw consumer program / bind validation; preserve old entrypoints. |
| **New WGSL** `aof_r1_tree_attention_capacity.wgsl` | Existing tree/linear attention, strided prefix indexing, same visibility. |
| **New WGSL** `aof_r1_incremental_attention_capacity.wgsl` | Prefix `[0,V)` + staged current token, GQA. |
| **New WGSL** `aof_r1_chunked_attention_capacity.wgsl` | Explicit per-route chunk visibility and generation binding. |
| `crates/model_core/src/aof_r1_admission.rs` | Add **actual bytes** of every new Rust consumer/WGSL and orchestrator qualifier file to `ark_runtime_source_digest()`. |
| `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs` | Extend current CF5 qualification with route/matrix and physical proof, default OFF. |
| **New** `tools/validate_ash_aof_r1_cf5_c_capacity_strided_consumer_static.py` | Positive/negative source checks, parent invariants and Naga registration. |

**Checkpoint freeze:** Do not touch the 19 `shared_lm_training_source_digest()` inputs solely to wire the qualifier; in particular do not edit model-core `aof_r1_verification.rs`, `native_wgpu.rs` or `model_layers.rs` without declaring a *different* checkpoint-lineage revision. If the real verifier cannot be instrumented via a safe independent seam, record HOLD. A byte-hash bypass/forged training digest is not allowed.

The file names above are proposed target paths, not a report of already-created files.

---

## 13. Exact source-digest preservation

Compute before/after SHA-256 for all 19 training-hashed files from `aof_r1_shared_lm_head_math::shared_lm_training_source_digest()` and preserve exact bytes. Independently extend `ark_runtime_source_digest()` over all new consumer code and WGSL **content**, not only shader paths/labels.

If the training-hashed source must change, CF5-C's legacy-checkpoint-preservation contract fails closed; stop and issue an explicit lineage-change proposal rather than silently widening scope.

Receipt fields:

```text
training_source_digest_before
training_source_digest_after
training_source_19_file_byte_identity_pass
runtime_source_digest_before
runtime_source_digest_after
new_shader_byte_coverage_pass
```

---

## 14. Static / compilation preconditions

Static validator must establish:

```text
capacity index always uses C
visible checks always use V
no implicit reshape/compact Tensor alias
no full-prefix K/V materialization in CapacityStrided path
negative out-of-range, overflow, stale-owner and future-tail checks
GQA divisor and group mapping unchanged
verifier tree/linear predicate inheritance
incremental/chunk route-specific visibility contracts
backend/consumer source and WGSL bytes added to runtime digest
19 checkpoint-hashed sources byte-identical
no default-mode / publication-order change
no claim of CF5-D Active
```

WGSL checks require both parsing and validation with the actual target features. A successful textual search for `@compute` is not shader validation. CPU unit tests for descriptors prove only metadata logic. Actual Rust WGPU type-checking and pipeline construction require native execution.

---

## 15. Bounded GPU physical test matrix

Required depths and maximum lengths from the **current actual layout**:

| Verification depth | Supported accepted block length |
|---|---|
| D1 | 1, 2 |
| D2 | 1, 2, 3 |
| D4 | 1, 2, 3, 4, 5 |

Accepted length `8` is **NOT_APPLICABLE**, never an inferred pass.

Required cases include:

- Verifier real tree path + linear oracle; root/parent/ancestor variation, near-tie and multiple layer/head arrangements.
- Ordinary incremental q_len=1 immediately after `k=0`, `k=1`, `0<k<L`, and `k=L` visible tokens.
- Chunked q_len>=2 with exact existing headwise, TensorCube and fallback route attribution; changed visibility semantics must fail.
- `T=1`, usual prompt length, and near maximum allowed capacity; unequal `C` vs `V` is essential.
- Tail poisoning in a **noncanonical shadow-only fixture**, verifying no read of `[V,C)` even when it contains conspicuous sentinel bit patterns.
- GQA many-query-heads / fewer-KV-heads; K/V same shape but different numerical values to catch swaps.
- Stale session, different generation/epoch, wrong backing digest, duplicate reuse, completion pending.
- EOS, stop, cancel before/after partial commit, failed emit, stale candidate, rejected suffix and repeated fresh session, with Legacy canonical tokens/KV/stop unchanged.
- Negative byte accounting: attempted hidden recompact, extra copy/MapRead, corrupted stride, wrong query visible length, forced cross-route fallback.

Shadow-only tail poisoning must never mutate the actual canonical cache or published checkpoint. Zero-length valid-prefix fixtures are `NOT_APPLICABLE` where existing AOF policy requires positive prefix.

---

## 16. Exact parity hierarchy

Prove separately:

```text
A. SOURCE: descriptor and kernel source correctly references physical stride
B. STATIC: ABI, bounds, identities, parent semantics checked
C. COMPILE: real Rust and Naga/WGSL compile
D. RUNTIME: same-path native source/route execution with controlled inputs
E. PHYSICAL: WGPU dispatch + completion + bounded readout parity
F. PERFORMANCE: same-source A/B with observation overhead removed or accounted
```

**Bitwise KV data parity from CF5-A/B does not prove attention output parity.** F32 attention may differ with reduction order and route. Report numerical tolerance/finite/winner/near-tie separately. Do not silently replace `FLOAT_TOLERANCE` with an arbitrary larger threshold; use the exact parent value(s) after source inspection.

Physical consumer acceptance requires genuine real-model Q/K/V from the native selected route, not a synthetic fixture alone. Synthetic negative fixtures can accompany it, never substitute for it.

---

## 17. Counters and provenance

Record at least:

```text
consumer_route: VerifierTree | VerifierLinear | IncrementalHeadwise |
                IncrementalTensorCube | IncrementalBurn |
                ChunkedHeadwise | ChunkedBurn | ExplicitlyUnsupported
read_view_owner_digest, session_epoch, backing_generation
capacity_tokens, visible_tokens, q_len, q_heads, kv_heads, head_dim
actual_consumer_dispatch_count, actual_completion_count
strided_prefix_read_elements, query_stage_read_elements
hidden_prefix_repack_count, hidden_prefix_repack_bytes
shadow_only_readback_bytes, shadow_queue_submission_count
compare_max_abs_error, near_tie_count, winner_parity
first_mismatch_layer, first_mismatch_query, first_mismatch_component
first_mismatch_key_position_if_available
consumer_support_status, physical_execution_status
```

Use counters at the actual dispatch/allocator sites; no fabricated literal zero presented as a measured zero. Distinguish OBSERVE overhead from canonical CF4 counters. `physical_vram_bytes` and `gpu_execution_ns` remain `UNKNOWN` unless measured by their corresponding physical instruments.

---

## 18. Receipt structure

File proposal:

```text
aof_r1_cf5_c_capacity_strided_consumer_bridge_receipt.json
```

Schema proposal: `ash.aof_r1.cf5_c.capacity_strided_consumer_bridge.v1`.

Bind:

```text
source_tree_digest
Cargo.lock digest
runtime_binary_sha256
training_source_digest_before/after
model/tokenizer/head-checkpoint/split identity
CF1/CF2/VH6/CF3/CF4 exact parent identifiers
CF5-A/B observe staging and parity receipt identity
GPU adapter, same-device and same-queue identity if actually observed
per-route × per-depth coverage matrix
real attention-source identity and visibility authority
strided key/value readouts and context/logit parity
owner-pinned completion and post-completion retirement
KV recompact and readback counters
first failing route/position
source/static/compile/runtime/physical/performance status
production_admission=false
promoted=false
receipt_hash
```

The aggregate receipt must not call a route PASS merely because the shader exists. Explicitly distinguish **UNSUPPORTED**, **NOT_RUN**, **HOLD**, **FAIL**, and **PASS**. Lack of an observed numerical-rejection physical path in CF2 remains a parent HOLD, not a newly fabricated success.

---

## 19. Negative failure classes

```text
FAIL_CF5_C_VIEW_SHAPE_REINTERPRETATION
FAIL_CF5_C_PHYSICAL_STRIDE_DRIFT
FAIL_CF5_C_LOGICAL_VISIBLE_TAIL_READ
FAIL_CF5_C_GQA_KV_HEAD_MAPPING
FAIL_CF5_C_VERIFIER_ANCESTRY_DRIFT
FAIL_CF5_C_VERIFIER_ORIGIN_DEPTH_DRIFT
FAIL_CF5_C_INCREMENTAL_CURRENT_TOKEN_MISSING
FAIL_CF5_C_CHUNK_VISIBILITY_SEMANTIC_DRIFT
FAIL_CF5_C_ROUTE_FALLBACK_MISCLASSIFIED
FAIL_CF5_C_HIDDEN_PREFIX_COMPACTION
FAIL_CF5_C_NEW_CANONICAL_READBACK_OR_WAIT
FAIL_CF5_C_STALE_OWNER_EPOCH
FAIL_CF5_C_BUFFER_BINDING_RANGE_OVERFLOW
FAIL_CF5_C_PRECOMPLETION_VIEW_RELEASE
FAIL_CF5_C_GPU_ATTENTION_PARITY
FAIL_CF5_C_TRAINING_SOURCE_DIGEST_DRIFT
FAIL_CF5_C_RUNTIME_SHADER_DIGEST_GAP
FAIL_CF5_C_PUBLISHED_STATE_DRIFT
FAIL_CF5_C_EARLY_ACTIVE_PROMOTION
HOLD_CF5_C_VERIFIER_ENTRY_UNREACHABLE
HOLD_CF5_C_UNSUPPORTED_NATIVE_CONSUMER_ROUTE
HOLD_CF5_C_CF1_OR_CF2_OR_VH6_PARENT_PHYSICAL_MISSING
HOLD_CF5_C_NATIVE_COMPILATION_NOT_RUN
```

No fail-open path classifies unknown/unsupported as pass.

---

## 20. Concrete verification commands (after implementation)

Use exact target features determined from the parent Cargo manifests; do not invent target names. Expected baseline commands:

```powershell
cargo metadata --format-version 1 --locked

cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1

cargo test -p model_core --lib aof_r1_kv_block --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_consumer_bridge --release --locked -j 1

# Once the new test tool is actually added:
python .\tools\validate_ash_aof_r1_cf5_c_capacity_strided_consumer_static.py
```

Then run the **existing CF5 native qualification CLI** with a new explicitly specified `consumer_probe` section, preserving its exact argument names from the implementation. The consumer probe is proposed here and **does not yet exist**. Execute on a real WGPU device with genuine selected model/tree/Q/K/V; record actual completion. An absent optional vendor path required by Cargo is a separate exact-input HOLD, never repaired with dummy dependency.

---

## 21. Stepwise implementation partition

| Substep | Implementation | Completion criterion |
|---|---|---|
| **CF5-C1** | Typed read-view, owner/epoch/generation, checked `C`/`V`, no Tensor shape fabrication | CPU/static negatives and honest source digest |
| **CF5-C2** | Verifier tree/linear capacity-indexed shader and genuine source-binding seam | Native GPU verifier parity with identical tree/linear visibility; if private canonical seam unreachable, HOLD |
| **CF5-C3** | Ordinary incremental q_len=1 prefix + current-token consumer | Native GPU context parity after partial commit; no full-prefix materialization |
| **CF5-C4** | Chunked Q>=2, per-route visibility/causal/receipt integration | Every claimed supported headwise/TensorCube/Burn route qualified separately |
| **CF5-C5** | Matrix, identity/retirement, first-mismatch, per-route receipt | PHYSICAL coverage and regression, production remains LEGACY |

No step can claim entire CF5-C closure based on the C1 descriptor alone.

---

## 22. Completion law

CF5-C may emit:

```text
PASS_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE
```

**only when all**:

```text
SOURCE
  All claimed real native consumer seams implemented without hidden K/V materialization
  19-file head training digest unchanged
  New Rust/WGSL bytes bound into AOF runtime source identity

STATIC
  C/V, offset, alias, owner, generation and tail invariants validated
  Route visibility/policy and canonical publication unchanged

COMPILE
  Actual Rust release targets and WGSL native pipelines pass

RUNTIME
  Real model Q/K/V/selected route compared to canonical same-source oracle

PHYSICAL
  D1/D2/D4 matrix with supported L=1..min(5,D+1)
  Verifier tree/linear, incremental and supported chunked routes observed
  No hidden prefix K/V full materialization
  GPU completion and source/owner identity proven
  Numerical context/logit/winner/near-tie parity within existing contracts

SEMANTIC
  Legacy canonical token/text/stop/KV/receipt unaffected
  No premature reuse, no stale read, no unpublished suffix visibility

PROMOTION
  Active remains HOLD; no CF5-D ownership cutover
  No performance claim
```

If any essential consumer route cannot be reached without modifying a checkpoint-hashed source, do **not** emit the full PASS. Issue `HOLD_CF5_C_VERIFIER_ENTRY_UNREACHABLE` or the exact applicable HOLD and propose a separate, explicit training-lineage change only after determining the precise source modification.

### Final invariant

```text
CF5-A/B PHYSICAL BACKING [H,C,W]
+ CURRENT OWNER / GENERATION
+ VISIBLE LENGTH V, NOT CAPACITY C
+ REAL VERIFIER / INCREMENTAL / CHUNKED GPU READS
+ NO FULL-PREFIX COMPACT KV MATERIALIZATION
+ EXACT EXISTING ATTENTION SEMANTICS
+ REAL COMPLETION AND PARITY
= CF5-C CONSUMER COMPATIBILITY QUALIFIED

CF5-C PASS != CF5-D ACTIVE CANONICAL PUBLICATION
CF5-C PASS != CF5-E PERFORMANCE PROMOTION
```

**Implementation-state supersession:** This original target contract is now accompanied by a partial source-bake annex. No full CF5-C PASS has been achieved; only the explicit implementation subset described below has been applied to the code-only ZIP. GitHub records specification/evidence only, not runtime source.

---

## 23. Exact source-bake and evidence annex (2026-10-08)

# AOF-R1-CF5-C CAPACITY-STRIDED KV CONSUMER BRIDGE

## Bake classification

**SOURCE/STATIC partial implementation only.** Full CF5-C remains HOLD; Rust COMPILE, real Naga shader compilation, native model runtime and WGPU physical parity are NOT_RUN. No finished inference speedup, headwise/TensorCube equivalence or production promotion is claimed.

## Parent / artifacts

- Parent: `ASH_PASS3_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY_CODE_ONLY.zip`
- Parent SHA256: `29a83e889de96e863b8dae071a09216efaea7ac83eb6ee86f6643b0fdf813ea6`
- Full: `ASH_PASS3_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE_CODE_ONLY.zip` (SHA256 `944ba80b9e08e1615180021db1216dc31ca0c001000a619260ad137cc3823b9d`)
- Overlay: `ASH_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE_OVERLAY_CODE_ONLY.zip` (SHA256 `eecbb4521a418bb1a6a37935dc3e2f744b0c9e94de034dac3a9dcc44fb965204`)
- Complete archive: **8730** files; ADD 6, MOD 6, DEL 0.
- CRC PASS and extracted byte comparison PASS for both archives.

## Actual implementation, not simulated acceptance

1. Added borrow-scoped `ArkKvStridedReadView` obtained from the live `ArkCf5ObserveBlock`. It checks exact model/binding/request/session/proposal/device/queue/epoch/generation, visible <= compared, K/V shape `[1,H,C,W]`, and canonical logical generation/length. The descriptor never reshapes `[H,C,W]` as `[H,V,W]`.
2. Added `aof_r1_tree_attention_capacity.wgsl`: copied parent tree/linear attention recipe with only head-major *prefix* K/V indexing from `head*past` to `head*capacity`. Private canonical verifier entry remains untouched.
3. Added incremental and chunked read-only GQA WGSL candidates accepting actual native contiguous canonical Q/current-K/V `[1,Q,H*D]` and physical prefix `[1,H,C,D]`. Chunked candidate requires caller-provided route-specific per-query staged visibility. No universal causal rule added.
4. Added `ArkCapacityConsumerPrograms` WGPU26 same-device/same-queue buffer binding, shape/alias/currentness checks, bounded dispatch and existing real Queue completion. This is an **opt-in candidate API**, not proof of execution in a production route.
5. Added model-core `aof_r1_kv_consumer_bridge.rs` for typed native reader calls; headwise/TensorCube routes fail explicitly with `HOLD_CF5_C_UNSUPPORTED_NATIVE_CONSUMER_ROUTE`.
6. Registered all three WGSL sources in the existing native Naga parse/validation list, and bound Rust/actual shader **bytes** to `ark_runtime_source_digest()`.
7. Existing CF5 OBSERVE aggregate now contains `cf5_c_consumer_bridge` with explicit `HOLD/NOT_RUN` fields, no fabricated dispatch count, and no full CF5-C pass token. Canonical state and `Active` refusal remain unchanged.

## Required unresolved consumers (NOT IMPLEMENTED)

- Actual `NativeWgpuModel::aof_forward()` is private within the 19-file training-digest-covered source. Its genuine Q/K/V and tree attention dispatch are **not** rerouted to the new candidate. A separate attention shader by itself is not full verifier parity.
- `DecodeState::forward_block_decode()`/`forward_block_chunked()` selected headwise/TensorCube/Burn route invocation has not been rebound to a CF5-C reader. New methods can accept genuine Q/K/V when a legitimate callsite is established; current status is **NOT_INSTRUMENTED**.
- No real model GPU context readout, numerical tolerance parity, same-route winner/near-tie, cancellation matrix or native reuse receipt was produced. Full C2/C3/C4/C5 and CF5-D ACTIVE remain HOLD.

## Source-level verification

| Gate | Status |
|---|---|
| CF5-C SOURCE/STATIC | **62/62 PASS** |
| CF5-A/B parent STATIC | **73/73 PASS** |
| CF4 parent STATIC | **65/65 PASS** |
| CF3 parent STATIC | **51/51 PASS** |
| CF1/CF2/VH6 older STATIC | **51/52, FAIL** (prior CF4-superseded exact `aof_r1_prefix_commit.rs` byte invariant, not silently reclassified) |
| CF5-C negative static fixtures | **7/7 rejected** |
| 19-source training checkpoint digest | **unchanged: `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`** |
| Rust COMPILE | NOT_RUN (`cargo` / `rustc` unavailable in packaging environment) |
| Native Naga | NOT_RUN (only registration/source checks) |
| Actual WGPU physical | NOT_RUN |
| PERFORMANCE | UNKNOWN |

Negative fixtures: old tree stride, incremental tail exposure, implicit chunk visibility, Active fail-open, runtime digest gap, hidden full-prefix materialization, training-hash input drift. The first version of the static gate missed one-sided K/V tail mutation; it was strengthened, retested and now rejects all 7. Only the restored post-mutation source was packaged.

## Source/manifest SSOT

`ASH_AOF_R1_CF5_C_BAKE_MANIFEST.json` enumerates all 12 exact path changes and their SHA256. `ASH_AOF_R1_CF5_C_STATIC_RECEIPT.json` retains per-gate outputs, including the older parent failure. `ASH_AOF_R1_CF5_C_NEGATIVE_STATIC_RESULTS.json` retains mutation results.

## Native execution commands (not run here)

```powershell
python .	ools
alidate_ash_aof_r1_cf5_c_capacity_strided_consumer_static.py
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_consumer_bridge --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_block --release --locked -j 1
cargo run -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -- --static-only
```

The exact `vendor/sherpa-rs-main/crates/sherpa-rs` workspace path must exist before interpreting Cargo failures as Rust source compilation results. Never use a dummy dependency.

## Next development admission

Establish one **genuine real-model Q/K/V native callsite** without modifying the training-hashed 19 files, or explicitly request a separate checkpoint-lineage revision. Only after that can the tree/linear, incremental, and selected chunked physical parity matrix be executed. No `PASS_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE` token may be emitted based on this partial SOURCE bake.
