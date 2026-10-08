# AOF-R1-CF5

## BLOCK PREFIX COMMIT + KV CAPACITY AUTHORITY

**Current implementation/evidence: PARTIAL SOURCE BAKE (A/B OBSERVE only). Full CF5 approval: HOLD.**

**Revision:** AOF-R1-CF5  
**Parent:** AOF-R1-CF4 PREFIX COMMIT TRANSFER ATTRIBUTION  
**Successor:** AOF-R1-CF6 PACKED/FUSED PRODUCTION PROMOTION (separate approval)  
**Class:** Canonical KV backing / logical-view / transactional publication optimization  
**Status:** Full A/B/C/D/E contract remains a target. **A/B OBSERVE source/static implemented (73/73 PASS); C/D/E ACTIVE not implemented (HOLD). Rust COMPILE/RUNTIME/PHYSICAL/PERFORMANCE: NOT_RUN / NOT_MEASURED.**  
**Reference package:** `ASH_PASS3_AOF_R1_CF4_PREFIX_COMMIT_TRANSFER_ATTRIBUTION_CODE_ONLY.zip` (SHA-256 `0b0904f845755d96b96f7a7da4605d1ae6da82bbf88ae93ef311b46c9434a231`).

```text
AOF-R1-CF5
BLOCK PREFIX COMMIT / KV CAPACITY AUTHORITY

+ CF1 / CF2 / VH6 / CF3 / CF4 PRESERVATION
+ EXACT VERIFIED-PREFIX BLOCK OWNERSHIP
+ PHYSICAL CAPACITY / LOGICAL COMMITTED LENGTH SEPARATION
+ CAPACITY-STRIDED K/V BACKING WITH EXPLICIT VIEW AUTHORITY
+ BOUNDED BLOCK PREPARE: COPY OLD PREFIX AT MOST ONCE
+ VERIFIED-SUFFIX BATCH SCATTER WITHOUT PER-TOKEN PREFIX REWRITE
+ REAL QUEUE COMPLETION BEFORE CANONICAL VISIBILITY
+ TOKEN-BY-TOKEN CANONICAL PUBLICATION PRESERVATION
+ EACH-TOKEN CURRENTNESS / ADMISSION / CANCEL REVALIDATION
+ INCOMPLETE / EOS / STOP / EMIT-ERROR TAIL ISOLATION
+ ORDINARY DECODE / AOF VERIFIER CONSUMER COMPATIBILITY
+ CF4 MEASURED COPYING / WAIT / ALLOCATION ATTRIBUTION PRESERVATION
+ LEGACY / OBSERVE / ACTIVE SAME-SOURCE COMPARISON
+ NO UNOBSERVED SPEEDUP OR VRAM CLAIM
+ NO SILENT COMPACT MATERIALIZATION OR CPU FALLBACK
+ NO FUSED PRODUCTION PROMOTION
```

---

## 0. Admission prerequisites and epistemic boundary

1. The CF4 ZIP contains **code and static instrumentation**, not an actual compiled/physical cost receipt. Its report explicitly records COMPILE, RUNTIME and PHYSICAL as `NOT_RUN`.
2. It is legitimate to develop the CF5 SOURCE branch without a performance result. **Do not promote `ACTIVE` or claim COPY_DOMINANT** before actual CF1/CF2/VH6/CF3/CF4 validation and a same-source benchmark.
3. The physical capacity / logical-view bridge is not proven available in the current Burn/RawWGPU stack. **Its feasibility is UNKNOWN** until a compiled native bridge and a real GPU parity probe demonstrate stride-aware consumers without a hidden full-buffer copy.
4. Source/static success cannot be promoted to real WGPU completion, canonical parity or speedup.

## 1. Exact existing call graph

The present selected AOF commit flow is:

```text
model_core::aof_r1_runtime::aof_r1_adopted_step()
  -> ArkPendingPrefix::commit_next()
     -> commit_next_inner()
        -> aof_r1_select_verified_hidden() (per token)
        -> stage_kv()
           -> clone KvCache metadata
           -> Tensor::zeros([1, heads, past+1, width]) x K,V per layer
           -> ArkVerificationDevice::stage_prefix_append()
              -> old KV [0,past) read + one suffix slot write
              -> queue.submit + wait_for_queue (per-layer)
        -> ArkVerificationDevice::complete_publication()
        -> require_boundary/current_structure/admission/cancel
        -> state.kv = next
        -> publish token/hidden/receipt; cursor.advance_prevalidated()
```

Source paths (relative to `ash_pass3/`):

- `crates/model_core/src/aof_r1_prefix_commit.rs`: `commit_next` ~109, `state.kv = next` ~350, `stage_kv` ~381, existing shape check ~429.
- `crates/model_core/src/aof_r1_runtime.rs`: `aof_r1_adopted_step` ~720; per-token call ~769; pending suffix retirement ~708.
- `crates/model_core/src/decode_state.rs`: `KvCache` ~143; `KvLayerCache` ~178; ordinary incremental KV update ~956–1017 and ~1630–1754; chunked path ~2475 onward.
- `crates/model_core/src/aof_r1_verification.rs`: prefix `Tensor` shape/reshape gate ~749–805; `ArkVerifiedTree` source & gathered suffix.
- `crates/burn_webgpu_backend/src/aof_r1_verification.rs`: `stage_prefix_append` ~427; completion ~460.
- `crates/burn_webgpu_backend/src/shaders/aof_r1_prefix_append.wgsl`: canonical bitwise head-major prefix/suffix copy.
- `crates/burn_webgpu_backend/src/raw_bridge.rs`: `RawWgpuBufferLease` & buffer offset/size; **not** a proven dynamic-stride logical tensor view.
- `crates/ash_core/src/aof_r1_prefix_commit.rs`: `ArkPrefixCursor` `tokens.len() <= 5`, `matched <= 4`, one-step generation progression.

**Existing ABI:** per-layer canonical K and V each have logical shape `[1, kv_heads, past_len, head_dim]`. Current verifier uses these shapes and flattens the cache before GPU attention; ordinary incremental decode uses `cat_seq_dim_4` and uses shape as a proof of logical sequence length. Merely allocating `[1,kv_heads,capacity,head_dim]` and setting `past_len` to a smaller value violates this ABI.

## 2. Goals and non-goals

**Goal:** For an accepted verified block of length `L`, do not reconstruct its full old KV prefix `L` times. Stage a single capacity-safe backing, append the verified suffix once, and keep **L separate canonical token/receipt/generation publications**, each guarded exactly as in the parent.

**Not a goal:** eliminate normal greedy-decode concatenation globally, fuse verifier logits with KV writes, change acceptance thresholds, batch multiple canonical tokens into one logical commit, remove valid completion barriers, or replace native model/GPU execution with a CPU path.

## 3. Distinct lengths, generations and SSOT

Define independently:

```text
T       = initial canonical past_len at block creation
L       = accepted tokens in ArkVerifiedTree (1 <= L <= 5)
C       = actual per-layer physical sequence capacity (C >= T+L)
k       = number of newly *published* tokens (0 <= k <= L)
V       = visible canonical length = T+k
B       = immutable physical backing identity, until it is retired
G_0     = pre-block logical KV content generation
G_k     = G_0+k (same per-token lineage as ArkPrefixCursor)
```

`KvCache.max_seq_capacity` is the **session/model logical maximum**, not a request to allocate that full capacity. Physical `C` is a separate bounded reservation chosen under device limits and current budget. Never confuse `C`, `V`, and `max_seq_capacity`.

When stopped at `k`, bytes in physical slots `[T+k,T+L)` exist only as **unpublished candidate storage** and MUST be invisible to canonical attention, logical tensor views, serialization, hash, checkpoint, oracle and next-round verifier.

## 4. The required two-layer representation

Introduce equivalent types (names are proposals, not claims of current implementation):

```rust
struct ArkKvBlockBacking {
    owner_generation: u64,
    physical_backing_identity: String,
    device_queue_binding: String,
    physical_capacity: usize,
    layer_backings: Vec<ArkLayerKvBacking>,
    submission_generation: u64,
    completion_proven: bool,
}

struct ArkLayerKvLogicalView {
    layer_index: usize,
    kv_heads: usize,
    head_width: usize,
    physical_stride_tokens: usize,
    committed_tokens: usize,
    backing_generation: u64,
    logical_content_generation: u64,
}

enum ArkKvStorageAuthority {
    CompactCanonical,
    CapacityBackedCanonical,
}
```

Do **not** fabricate a `Tensor<[1,H,V,W]>` shape while it physically contains `[1,H,C,W]`, unless the concrete backend provides a tested, ownership-preserving logical view with correct stride handling.

`KvCache.past_len`, `KvPositionLifecycle.committed_past_len`, `KvLayerCache.used_tokens`, `committed_token_count` and per-layer `key_content_generation` / `value_content_generation` remain **logical committed** authorities. Physical owner metadata stays separate and is never substituted for an `ArkAttemptIdentity`.

The typed `KvLayerCache.key_cache` / `value_cache` fields cannot silently hold capacity-sized tensors while old consumers still expect compact shape. Either introduce an explicit capacity-backed KV variant at the consumer seam or demonstrate a safe zero-copy view that presents the same **logical** representation. If neither is available: **HOLD_CF5_LOGICAL_VIEW_UNAVAILABLE**; `ACTIVE` is forbidden.

## 5. Physical layout and index mapping

Canonical compact source layout is head-major:

```text
source_offset(h,pos,c) = ((h*T) + pos)*head_width + c
```

The capacity-backed target MUST use its own physical stride:

```text
target_offset(h,pos,c) = ((h*C) + pos)*head_width + c
```

The pre-gathered verified suffix in `ArkVerifiedTree.gathered` uses row-major suffix slots:

```text
suffix_offset(j,h,c) = j*kv_heads*head_width + h*head_width + c
```

For each layer and both K/V, copy source prefix `[0,T)` once into the new backing and scatter suffix `j in [0,L)` to physical position `T+j`, preserving original **u32 bit patterns of f32** and original token order. Never use a raw byte append for multi-head tensors: head-major physical row stride would be wrong.

Check every index/size product with `checked_mul`/`checked_add`, respect `max_storage_buffer_binding_size`, per-device workgroup limits, alignment, correct K/V cardinality, exact source/target binding range, offset/size and absence of unintended aliasing.

The parent `aof_r1_prefix_append.wgsl` and `stage_prefix_append` remain available for `LEGACY`. Add a separate named CF5 block-projection shader and driver. No undeclared mutation of the parent shader or relaxed lease validation.

## 6. Once-per-block preparation

A single `ArkPreparedKvBlock` is bound to:

```text
session_id / model / tokenizer / request
proposal_round / root token / position_epoch
parent KV generation G_0 and exact past_len T
ArkVerifiedTree original identity and accepted-token digest
current structure / admission snapshot identity
CF2/CF4 actual queue/device owner
per-layer K/V backing identity and actual physical range
```

Prepare requirements:

1. A valid `ArkVerifiedTree` with `L` accepted canonical tokens; no guessed/unverified positions, no new verifier decision.
2. Sufficient room for `T+L`, or an explicit **rejected-capacity/HOLD** before any canonical publication. No synthetic extension of max tokens.
3. All layers allocate/borrow a safe bounded destination in the same owner; only one prefix migration (if any) and one suffix scatter per layer. No accidental `O(L)` full-prefix copy caused by convenience `slice`, `reshape`, `cat` or `clone` materialization.
4. Submit the existing-queue work and retain all source/suffix/destination handles through proven completion; no mapping/readback/fence added merely to observe correctness.
5. On any layer stage failure, leave `state.kv`, generated tokens, receipt cursor, lifecycle and current structure unchanged; release/retire staged GPU resources only after actual completion.
6. Physical backing enters the **PreparedCompleted** state only after bound-queue completion and error-scope validation, not after `submit()` alone.

A proposal with `L=1` is still a valid one-slot block but may have no structural advantage. No optimization success based solely on this case.

## 7. Publish per token, never per block

Keep the parent `ArkPrefixCursor` as the sole token-consumption authority. For each pending index `k`, execute the same `aof_r1_select_verified_hidden`, structure/currentness, admission, sampling bans/EOS, cancel checks and `try_reserve` behavior at the same prepublication boundary.

Conceptual state machine:

```rust
enum ArkKvBlockPhase {
    Unprepared,
    Staging,
    PreparedInFlight,
    PreparedCompleted,
    PartiallyPublished,
    FullyPublished,
    Retiring,
    Retired,
    TerminalHold,
}

match (phase, per_token_guard, completion_proven) {
    (ArkKvBlockPhase::PreparedCompleted | ArkKvBlockPhase::PartiallyPublished, Ok(()), true)
        => { /* update V=T+k+1, one generation, one token/receipt */ }
    (_, Err(_), _) => { /* preserve published prefix, retire tail */ }
    (_, _, false) => { /* never publish or reuse */ }
    _ => { /* explicit invalid-state classification */ }
}
```

**Meaning change:** `state.kv` may now refer to stable capacity backing plus a moving logical visible length, instead of an allocated compact `Tensor` per token. The externally observable sequence is unchanged:

```text
V: T -> T+1 -> T+2 -> ... -> T+L
G: G0 -> G0+1 -> G0+2 -> ... -> G0+L
one token + one KV logical append + one receipt per successful step
```

Current `ArkPrefixCommitObservation` schema/fields are preserved, including `kv_generation_before/after`, source `MatchedProposal | TargetCorrection | TargetBonus`, token ordinal, readback bytes and the canonical `state.kv` visibility semantics. New block/storage fields are additive and do not replace old receipt values with incompatible physical sizes. Distinguish old `staged_full_kv_bytes` **logical** accounting from new physical reservation bytes and actual observed allocations.

All fallible validation, metadata allocations, and receipt construction must complete before the irreversible publication edge. A late accounting failure cannot revoke a token already published; retain an **incomplete telemetry receipt**, not a fabricated commit rollback.

## 8. Consumer parity is a non-optional gate

The following paths must be audited, and every `ACTIVE`-reachable one either become stride-aware or be proven to obtain a truly zero-copy compact logical view:

| Consumer | Existing dependency | CF5 obligation |
|---|---|---|
| `aof_r1_verification.rs::aof_forward` | exact `[1,H,past,W]` and flatten/reshape | full stride-aware prefix attention, no hidden compact materialization |
| `decode_state.rs::forward_block_decode` | `cat_seq_dim_4(cached_k,k_new)`; logical shape | active-to-ordinary transition explicitly owned, efficient or measured |
| `decode_state.rs::forward_block_chunked` | shape check against post-append len | logical length / stride parity or explicit unsupported profile HOLD |
| `model_layers.rs::grouped_query_attention` | uses real tensor dimension for key sequence | no capacity tokens exposed as valid attention sequence |
| canonical forward/replay oracle | exact tokens and suffix slice | equivalence for visible `[0,V)` only |
| prefill/restart/session identity | compact KV lineage | new block owner creation or explicit retirement without stale alias |

**Critical:** `RawWgpuBufferLease { buffer_offset, buffer_size }` provides a contiguous binding region, **not** an automatic per-head dynamic-stride representation. The existing AOF verifier converts compact `[1,H,past,W]` into `[past*H*W]`; pointing it at `[1,H,C,W]` without revising index math can read other heads' reserved/tail bytes. A simple `Tensor::slice`/`reshape` is not assumed zero-copy. Run an actual backing-identity/physical parity test. If active reachable consumers cannot be migrated safely within scope, halt the full CF5 promotion and report the precise consumer blocker; do not silently switch per token to costly compact reconstruction.

## 9. Immutable prefix and tail isolation

A prepared block may contain uncommitted suffix data, but those bytes must have **no canonical read authority**. Every consumer must use `V` as a hard address/sequence bound, not `C`.

Forbidden:

```text
V < T+L but attention reads [V,T+L)
readback/hash/oracle includes tail
published token N with KV logical count N+2
republish already consumed suffix
new proposal borrows stale capacity owner
overwrite an in-flight backing used by another submission
```

If a next ordinary/AOF operation begins after `k<L`, it must observe exactly `[0,T+k)` with the correct per-head layout. Unpublished tail cannot be promoted just because it was physically written earlier.

## 10. Cancellation, EOS, stop, emit and failure semantics

Required matrix:

- **Cancel before first publication:** no canonical changes, `k=0`; GPU staged work retires after completion.
- **Cancel after k publications:** first `k` tokens/KV generations persist; rest non-canonical and retired.
- **EOS / stop / max tokens at k:** terminate exactly at existing boundary; no remaining speculative KV becomes visible.
- **Emit failure after publication:** `published != ACK`, already-public canonical token/KV stay. Do not roll history backward or duplicate emission. All unused tail retires.
- **Stale model/session/position/queue/owner/structure/bans:** fail closed at the same per-token guard, including changes **after** block staging.
- **GPU submit/completion failure:** zero new canonical publication for any uncompleted operation; no early reuse.
- **Partial layer prepare:** no canonical layer advances before all layers are validated and GPU completion proven.
- **Duplicate consume / callback:** zero duplicate token/KV/receipt or free; explicit failure reason.
- **Following session / new prefill / resumed ordinary decode:** no active pending shadow/tail authority leaks or stale backing reuse.

Preserve the existing CF2 pending-retirement/terminal-quarantine rules for real GPU in-flight handles.

## 11. Modes / rollout

Introduce a **commit-specific** mode separate from `ArkMode` inference admission:

```rust
enum ArkKvBlockCommitMode {
    Legacy,
    Observe,
    Active,
}
```

- `Legacy` (default): CF4 canonical path unchanged.
- `Observe`: CF4 legacy produces/publishes canonical results; shadow CF5 backing is prepared on the **same model/checkpoint/input** and compared on bounded, current, non-publishing probes. Shadow must never mutate the canonical cache. Any added GPU work/VRAM is attributed separately, not represented as normal production cost.
- `Active`: admission requires exact current source/parent physical proof and verified consumer bridge; otherwise **HOLD**. CF5 publishes canonical logical views token-by-token. No implicit fallback to Legacy after a partial block or after a mismatch.

This mode does **not** enable packed/fused head production. Do not modify rank selection, +2/+3/+4/+5 head math, FuturePool verdicts or policy thresholds.

## 12. Proposed source ownership

Expected modifications / new modules, all subject to actual compile-closure inspection:

```text
crates/model_core/src/aof_r1_prefix_commit.rs
crates/model_core/src/aof_r1_runtime.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/aof_r1_verification.rs
crates/burn_webgpu_backend/src/aof_r1_verification.rs
crates/burn_webgpu_backend/src/shaders/aof_r1_block_prefix_stage.wgsl      [NEW]
crates/model_core/src/aof_r1_kv_block_authority.rs                      [NEW]
crates/model_core/src/aof_r1_kv_block_authority_tests.rs                [NEW]
crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs           [NEW]
tools/validate_ash_aof_r1_cf5_block_prefix_commit_static.py           [NEW]
```

Additional ordinary/headwise consumer files may be necessary (e.g. `model_layers.rs`, WGPU headwise kernels). This is a **potential scope expansion**, not an already verified narrow edit. The full dependency-closed consumer graph must be recorded before baking. No arbitrary change to base-training, optimizer, head-training checkpoint source digest or unrelated KV paths.

The CF4 `aof_r1_commit_trace.rs`, `aof_r1_cf4_transfer_attribution.rs`, telemetry and existing receipts remain reporting SSOT. CF5 may append derived fields, not erase, zero or silently reclassify original CF4 work.

## 13. Implementation stages and gates

| Stage | Work | Exit criterion |
|---|---|---|
| **CF5-A** | Exact parent/CF4 evidence preflight; real KV consumer map; capacity/stride prototype | Native WGPU physical read/write of `[1,H,C,W]` with logical `[1,H,V,W]`, exact bitwise K/V views, backing owner identity; otherwise HOLD |
| **CF5-B** | Block prepare and physical owner, copy-prefix-once + suffix scatter, all-layer transaction | Actual completed dispatch, head-major bitwise parity, no aliases, bounded reservation, CF2 retirement |
| **CF5-C** | Verifier and ordinary/chunked consumer compatibility, strict view masking | Every active reachable path consumes exactly `[0,V)`, no hidden `O(V)` materialization or wrong-head stride |
| **CF5-D** | Per-token publication/currentness/receipt/cancel/emit integration | D1/D2/D4 canonical OFF/ON token/text/stop/KV logical parity, once-only generation/cursor progression |
| **CF5-E** | Observe/Active qualification, CF4 accounting and controlled benchmark | At most one full-prefix migration per prepared block, no unobserved reuse, physical evidence + separate speed test |

Before CF5-C passes the old `stage_kv` remains the only publication authority. CF5-A/B source implementation **may not** claim Active closure merely because the stage shader works.

## 14. Static negative gates

The new validator SHALL reject:

```text
physical capacity treated as canonical logical length
committed length derived from buffer binding size
unknown stride silently treated as contiguous
index formula missing per-head physical stride
copy the whole prefix again for each published token
canonical publication before real queue completion
single bulk receipt replacing per-token receipts
per-token boundary/admission/cancel checks removed
acceptance of depth outside D1/D2/D4 or length >5
stale/duplicate owner generation release
partial layer visibility
tail visible to forward, oracle, or resume
new H2D/D2H to read the whole KV as a convenience
unbounded reservation to max_seq_capacity
CF4 counters removed or rewritten as all zero
head-training source digest changed
numerical tolerance / winner / near-tie changed
implicit CPU / legacy fallback under ACTIVE
```

Preserve existing CF1/CF2/VH6/CF3/CF4 gates and report intentionally superseded byte-identity checks explicitly rather than rewriting their historical accepted digests to force PASS.

## 15. Runtime and physical qualification

Required cases: D1/D2/D4; accepted lengths actually allowed by the depth policy (up to D1+bonus 2, D2+bonus 3, D4+bonus 5); partial-prefix acceptance, correction, bonus, near-tie, EOS, StopSequence, MaxNewTokens, cancel before/after publish, emit failure, stale model/session/epoch, duplicate consume, failed stage/submit/completion and repeat fresh sessions.

**Accepted length 8 = NOT_APPLICABLE** under the present `ArkPrefixCursor` upper bound 5. Never generate a fake physical eight-token prefix to satisfy the former broad roadmap.

For each block, verify:

```text
K/V bitwise equality on all visible [0,V) positions
all-layer/head/width identity exact
logical V=T+k, generation G0+k and ordinal exact
CF4 per-token receipt, emit ACK, stop reason and token/text exact
for every k, no read of [V,C)
owner currentness and queue completion proven
KV backing transfer/copy is observed at the correct callsite
no per-token old-prefix full copy in ACTIVE
```

`OBSERVE` parity must not be inferred from equal hashes of unrelated inputs or from CPU-only tests. For physical PASS use the **real NativeWGPU** headwise/verifier route. Real lifecycle/physical tests require exact model/tokenizer/checkpoint/split identity and controlled same-source baseline.

## 16. Objective instrumentation and bounded-cost accounting

Carry forward CF4 counters and add *actual source-observed*:

```text
block_prepare_attempt_count
block_prepare_complete_count
block_source_prefix_bytes (logical)
block_source_prefix_migration_count
block_suffix_gathered_elements
block_staging_allocation_count
block_staging_logical_bytes
block_physical_capacity_tokens
block_peak_reserved_vram_bytes                 = UNKNOWN unless allocator observed
block_completion_wait_ns                     = host wait, not GPU kernel time
block_visible_commit_count
block_cancelled_unused_suffix_count
block_view_materialization_count
block_view_materialization_bytes
block_owner_terminal_leak_count
block_fallback_transition_count              (0 under ACTIVE; otherwise explicit)
block_first_mismatch {session,round,layer,head,position,component}
```

Keep logical f32 K/V bytes, actual buffer allocation bytes and real bus bytes as **three different categories**. A reduced logical copy count does not prove a higher token/s or reduced physical VRAM. Report host wait, GPU kernel duration, CPU time and full generation wall separately where actually measured. Counter overflow/absence is an invalid or UNKNOWN observation, not literal zero.

## 17. Exact receipt and failure classification

New receipt:

```text
aof_r1_cf5_block_prefix_commit_kv_capacity_authority_receipt.json
```

Required schema fields:

```text
schema = ash.aof_r1.cf5.block_prefix_commit_kv_capacity.v1
parent_cf4_receipt_sha256 / validation status
source_digest / Cargo.lock / runtime binary identity
model / tokenizer / head checkpoint / split identities
session, round, depth, accepted L, initial T, physical capacity C
backing identity / owner generation / exact queue-device binding
all-layer shape and logical stride proof
completion proof / retirement proof
per-token canonical V, G, ordinal and token/receipt sequence
EOS/stop/cancel/emit/ACK/stale/duplicate matrix
read-mask / tail invisibility witness
actual full-prefix migration count and suffix scatter count
CF4 preserved counters and materialization accounting
Legacy/Observe/Active mode and first mismatch
source_status / static_status / compile_status / runtime_status /
physical_status / performance_status / production_admission=false
pass_token only after final admission; canonical receipt hash
```

Dedicated fail reasons at minimum:

```text
FAIL_CF5_CF4_PARENT_PHYSICAL_UNVERIFIED
FAIL_CF5_LOGICAL_VIEW_UNAVAILABLE
FAIL_CF5_PHYSICAL_STRIDE_MISMATCH
FAIL_CF5_HEAD_MAJOR_LAYOUT_DRIFT
FAIL_CF5_CROSS_LAYER_PARTIAL_STAGE
FAIL_CF5_PRE_COMPLETION_PUBLICATION
FAIL_CF5_LOGICAL_LENGTH_EXPOSES_TAIL
FAIL_CF5_KV_GENERATION_DRIFT
FAIL_CF5_TOKEN_KV_RECEIPT_COUNT_DRIFT
FAIL_CF5_STALE_OWNER_OR_SESSION
FAIL_CF5_COMPLETION_OR_RETIREMENT
FAIL_CF5_DUPLICATE_CONSUME_OR_COMMIT
FAIL_CF5_CANCEL_EMIT_STOP_SEMANTIC_DRIFT
FAIL_CF5_PER_TOKEN_PREFIX_COPY_SURVIVED
FAIL_CF5_HIDDEN_COMPACT_MATERIALIZATION
FAIL_CF5_VRAM_CAPACITY_BUDGET
FAIL_CF5_SOURCE_DIGEST_DRIFT
FAIL_CF5_UNSUPPORTED_DEPTH_OR_LENGTH
FAIL_CF5_EARLY_PRODUCTION_PROMOTION
```

No missing physical evidence may be labeled PASS just because a CPU/reference test succeeded.

## 18. Native validation commands

After exact vendor input/lock graph are present, start with the actual manifest-declared targets:

```powershell
python .\tools\validate_ash_aof_r1_cf4_prefix_commit_transfer_static.py
python .\tools\validate_ash_aof_r1_cf5_block_prefix_commit_static.py
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_block --release --locked -j 1
```

The *new CF5 test name and CLI switch do not exist yet* and are not executable until the CF5 code bake provides them. Reuse existing real `--cf4-attribution` campaign as the pre-change baseline. Execute corresponding real CF5 `OBSERVE` and `ACTIVE` campaigns only after bridge parity proof. Compare with AOF OFF / legacy AOF / CF5 Active under same model, data, GPU, fixed workload and warmup. Submit evidence without changing unrelated Cargo manifest or shader source.

## 19. Performance stop condition and next successor

CF5 may issue:

```text
PASS_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY
```

**only if**:

```text
SOURCE/STATIC: complete dependency-closed consumer bridge and parent invariants
COMPILE: real native Rust graph and test targets PASS
RUNTIME: all negative/transactional token/KV test cases PASS
PHYSICAL: real WGPU stride view + block stage + callback/retirement PASS
PARITY: all enabled depth/length/case matrices exact where required
ACCOUNTING: per accepted block <=1 observed full-prefix migration;
            no per-token hidden full copy; CF4 measurements honest
PROMOTION: packed/fused head production remains unchanged
```

**Performance** requires a separate measured A/B and may legitimately report `NO_SPEEDUP`, `REGRESSION` or `INSUFFICIENT_EVIDENCE` despite correctness closure. Do not call a data-movement optimization faster just because its operation count is lower. If the real CF4 campaign reveals WAIT_DOMINANT rather than COPY_DOMINANT, record that CF5 may not be the optimal next performance investment.

---

## Final invariant

```text
ONCE-PER-BLOCK PHYSICAL KV PREPARE
+ PROVEN BOUND-QUEUE COMPLETION
+ PHYSICAL CAPACITY != LOGICAL VISIBLE LENGTH
+ CORRECT PER-HEAD STRIDED CONSUMERS
+ ONE-TOKEN-AT-A-TIME AUTHORIZED CANONICAL PUBLICATION
+ COMPLETE PREFIX/TOKEN/KV GENERATION PARITY
+ UNPUBLISHED SUFFIX NEVER BECOMES CANONICAL
+ NO PER-TOKEN WHOLE-PREFIX RE-COPY
= AOF-R1-CF5 STRUCTURAL CLOSURE
```

**Scope note (2026-10-08):** The requested full CF5 closure remains a design target. A/B OBSERVE-only source has been baked; capacity-aware canonical consumers and ACTIVE block publication (C/D/E) are not implemented or physically proven. See the source-bake annex below.

---

## SOURCE BAKE ANNEX / EXACT 2026-10-08 IMPLEMENTATION STATUS

This annex is the **observed source delta** against the exact CF4 code-only parent. It does not replace or weaken the full CF5 target contract above. Full CF5 has **not** achieved its terminal invariant.

### Artifact identity

- Parent: `ASH_PASS3_AOF_R1_CF4_PREFIX_COMMIT_TRANSFER_ATTRIBUTION_CODE_ONLY.zip`
- Parent SHA256: `0b0904f845755d96b96f7a7da4605d1ae6da82bbf88ae93ef311b46c9434a231`
- CF5 Full code-only ZIP: `ASH_PASS3_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY_CODE_ONLY.zip`
- Full ZIP SHA256: `29a83e889de96e863b8dae071a09216efaea7ac83eb6ee86f6643b0fdf813ea6`, 8,724 files.
- CF5 Overlay ZIP: `ASH_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY_OVERLAY_CODE_ONLY.zip`
- Overlay SHA256: `e92f53da023d99e188e3bd64b6e033c539cfcf046c927235bd754c866bc1bf30`.
- Delta against parent: ADD 5 / MODIFY 10 / DELETE 0. Exact per-file SHA256 recorded in `ASH_AOF_R1_CF5_BAKE_MANIFEST.json` (delivered alongside ZIP), not committed as source.
- Archive CRC: PASS; byte-for-byte extracted file comparison: PASS.

### SOURCE implemented: CF5-A / CF5-B OBSERVE only

- `crates/model_core/src/aof_r1_kv_block_authority.rs`: checked head-major `[H,C,W]` stride, `[0,V)` visible-length limit, D1/D2/D4 up to 5 tokens, explicit shadow budget, `ArkCf5ObserveBlock` lifetime and per-token observation. Default `LEGACY`; `ACTIVE` returns `HOLD_CF5_LOGICAL_VIEW_UNAVAILABLE`, never a silent legacy fallback.
- `crates/burn_webgpu_backend/src/shaders/aof_r1_block_prefix_stage.wgsl`: real WGPU candidate shader for once-per-block old-prefix copy and accepted-suffix scatter into nonpublishing `[1,H,C,W]` shadow K/V.
- `crates/burn_webgpu_backend/src/shaders/aof_r1_block_prefix_compare.wgsl`: visible `[0,V)` raw u32 K/V bitwise parity against the **existing compact Legacy canonical staging**, GPU-side mismatch counters, 12-byte status readback per layer and step in opt-in OBSERVE.
- `crates/burn_webgpu_backend/src/aof_r1_verification.rs`: original same-Queue dispatch and completion reused; new stage/compare helper and resource bounds. `crates/burn_webgpu_backend/src/aof_r1_commit_trace.rs`: CF5 shadow operations excluded from CF4 canonical copy/submit/readback accounting.
- `crates/model_core/src/aof_r1_prefix_commit.rs`: stage shadow once on first verified-prefix commit and compare each subsequent `stage_kv` result before Legacy publication, preserving token-by-token canonical state mutation and fault behavior.
- `crates/model_core/src/generation_sampling.rs`, `generation_telemetry.rs`, `decode_state.rs`: opt-in mode/budget and per-attempt observation, no default production route change.
- `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs` and native CLI binding: `--cf5-qualification INPUT.json --out FRESH_DIRECTORY` runs the existing real native commit-stability matrix; binds **same runtime source digest AND same matrix_id** to current CF4 physical parent; checks required/observed rank × D1/D2/D4 parity coverage, ensures no early promotion.
- `crates/model_core/src/aof_r1_admission.rs`: runtime source digest now includes **actual bytes of both CF5 WGSL shaders**, the CF5 Rust owner, CLI and trace file. Existing training source digest remains unchanged.
- `tools/validate_ash_aof_r1_cf5_block_prefix_commit_static.py`: 73 SOURCE/STATIC checks. New WGSL shaders are included in the existing native Naga parsing list; actual Naga compilation has not been executed.

### Explicitly NOT implemented: CF5-C/D/E ACTIVE

`RawWgpuBufferLease` in the CF4 parent represents a contiguous range and the native AOF verifier plus ordinary decode/chunked decode consumers require actual compact Tensor `[1,H,V,W]` shape. No proven zero-copy capacity-strided logical view exists. **The OBSERVE shadow is never used as canonical KV**. Full consumer integration, partial-block ACTIVE publication, tail masking, rollback/stop/emit/cancel parity and physical benchmarks remain **HOLD**. No full `PASS_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY` token has been emitted. OBSERVE itself adds real GPU staging, completion and readback workload; no speedup is claimed.

### Evidence results (do not promote)

- CF5 source/static validator: **73/73 PASS**.
- CF5 negative static mutations: **6/6 rejected** (stride, tail, early Active, digest omission, CF4 attribution leakage, forged full PASS).
- Parent CF4 static: **65/65 PASS**; parent CF3 static: **51/51 PASS**.
- Older CF1/CF2/VH6 static: **51/52**, expected failure on CF4-superseded `aof_r1_prefix_commit.rs` exact byte check. Do not falsely mark 52/52.
- Head checkpoint 19-source training digest exact: `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
- `cargo`/`rustc`: NOT AVAILABLE; Rust COMPILE: NOT_RUN; native Naga: NOT_RUN; RUNTIME: NOT_RUN; real GPU PHYSICAL: NOT_RUN; PERFORMANCE: NOT_MEASURED.
- Missing external sherpa-rs path workspace dependency requires exact input repair before a real Cargo release build, not a dummy fallback.

### Next acceptance

```powershell
python .\tools\validate_ash_aof_r1_cf5_block_prefix_commit_static.py
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_block --release --locked -j 1
cargo run -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -- --static-only
```

Then rerun the CF4 physical receipt on the *same new source and matrix* and execute a real CF5 `OBSERVE` campaign. Claim `PASS_AOF_R1_CF5_OBSERVE_PHYSICAL_PARITY` only after actual GPU K/V parity and all rank/depth coverage. Full CF5 needs a subsequent explicit capacity-aware consumer implementation and distinct PHYSICAL/SEMANTIC/PERFORMANCE validation. This commit is a **specification and exact source-bake status record**, not a code commit or physical approval.
