# AOF-R1-CF5-C-R2
## VERIFIER NATIVE SEAM + CHECKPOINT LINEAGE QUALIFICATION

**Patch ID:** `AOF-R1-CF5-C-R2`  
**Parent:** `AOF-R1-CF5-C-R1` (Native Consumer Callsite Binding + Completed Observe-Backing Handoff)  
**Successor:** `AOF-R1-CF5-C-R3` only for remaining unqualified native routes / full C closure; `AOF-R1-CF5-D` remains gated on whole-consumer physical qualification.  
**Class:** Actual verifier attention seam, session-scoped GPU observation, strict checkpoint lineage qualification  
**Status (2026-10-09): PARTIAL SOURCE/STATIC BAKE.** Backend-native Tree verifier OBSERVE seam candidate applied; SOURCE/STATIC 44/44 PASS and 12/12 negative-source rejections. Rust COMPILE, native Naga, RUNTIME, GPU PHYSICAL and numerical parity NOT_RUN. Full CF5-C-R2, Linear qualification, all-consumer closure and CF5-D ACTIVE remain HOLD. See exact source-bake annex.

```text
AOF-R1-CF5-C-R2

+ CF5-A/B/C / R1 PARENT SEMANTIC PRESERVATION
+ ACTUAL NATIVE VERIFIER ATTENTION BUFFER SEAM
+ EXACT Q / SUFFIX K / SUFFIX V / CANONICAL CONTEXT CAPTURE
+ TREE / LINEAR ROUTE IDENTITY PRESERVATION
+ PER-INVOCATION / PER-SESSION READ-ONLY OBSERVER SCOPE
+ SESSION-PARKED CAPACITY BACKING OWNER / GENERATION BINDING
+ PROPOSAL ROUND CHANGE WITHOUT ORIGIN REWRITE
+ MATCHING DEVICE / QUEUE / TREE / LAYER ORDINAL
+ NO UNBOUNDED GLOBAL / TLS OBSERVER STATE
+ NO CROSS-SESSION OBSERVER CONSUMPTION
+ OBSERVE GPU SUBMISSION / COMPLETION / RETIREMENT
+ GPU-RESIDENT CONTEXT PARITY, COMPACT RECEIPT
+ NO FULL Q/K/V / FUTURE-TREE HOST READBACK
+
+ PREFERRED: TRAINING SOURCE-DIGEST PRESERVATION VIA BACKEND SEAM
+ ALTERNATIVE: EXPLICIT NEW CHECKPOINT LINEAGE ONLY IF REQUIRED
+ NO EXISTING CHECKPOINT MANIFEST REWRITE
+ NO TRAINING SOURCE-DIGEST BYPASS OR ALLOWLIST
+ NO AUTOMATIC MIGRATION / PROMOTION
+
+ OLD CANONICAL VERIFIER OUTPUT REMAINS AUTHORITATIVE
+ NO ORDINARY / CHUNKED / HEADWISE / TENSORCUBE ROUTE RECLASSIFICATION
+ NO KV PUBLICATION / KV STORAGE / FUSED PRODUCTION CHANGE
+ NO NEW WORK OR WAIT OUTSIDE OPT-IN OBSERVE
+ FULL CF5-C / CF5-D ACTIVE REMAIN HOLD
```

---

## 0. Exact parent and evidence boundary

Parent code-only archive:

`ASH_PASS3_AOF_R1_CF5_C_R1_NATIVE_CONSUMER_CALLSITE_HANDOFF_CODE_ONLY.zip`

SHA-256:

`d568bc6a3f9a9d75b9d5b9b684c8e180c83578330f9262eecafdef0d063363fd`

The archive contains **8,731 entries**, ZIP CRC valid. Source review only; this specification does not imply successful Cargo/Naga/runtime/physical execution.

Previous R1 status:

- R1-A completed OBSERVE backing handoff: SOURCE applied.
- R1-B ordinary selected Burn route and R1-C selected chunked Burn route: SOURCE applied, not physically promoted.
- R1-D private verifier connection: HOLD.
- R1-E actual WGPU physical campaign: NOT_RUN.
- Canonical KV remains Legacy; CF5 `ACTIVE` is unavailable.

**R2 addresses the verifier seam specifically, not all remaining native consumers.**

---

## 1. Verified callsite facts

The actual model-core verifier is in:

`crates/model_core/src/aof_r1_verification.rs`

- `NativeWgpuModel::aof_forward()` is private, approximately lines 708–814 of the parent.
- `layer.canonical_qkv_prepared(hidden, &prepared)` produces actual per-layer Q/K/V.
- `owner.programs.attention(params, tree, q, k, v, pk, pv, ctx, linear)` is called with actual raw WGPU leases for Q, suffix K/V, compact prefix K/V and canonical context output.
- Tree verification enters through `verify_aof_r1_tree_depth()`; linear verification is also called from existing native qualification/Jacobi callsites. These must not be conflated.
- `aof_forward()` currently flattens compact prefix `[1,H,T,W]` into `[T * H * W]` after validating real shape and canonical KV generation.

The backend callee is in:

`crates/burn_webgpu_backend/src/aof_r1_verification.rs`

- `ArkVerificationDevice::attention()` accepts the actual `RawWgpuBufferLease` values for Q, suffix K/V, compact prefix K/V and output, plus `tree`, `params[8]`, and `linear_oracle`.
- Its canonical tree/linear dispatch and resulting `output` remain the same selected verifier authority.
- The backend file is **not one of the 19 direct inputs** to `shared_lm_training_source_digest()` in this parent.

**Revision of prior assumption:** Direct exposure from private `aof_forward()` would change its hashed source file. That does **not** establish that all real verifier observation seams require changing it. A backend-owned scoped observer is a plausible alternative, not yet a compiled/physical capability.

---

## 2. Source-digest truths are two separate authorities

`crates/model_core/src/aof_r1_shared_lm_head_math.rs::shared_lm_training_source_digest()` hashes 19 exact path+byte inputs (including `aof_r1_verification.rs`, `model_layers.rs`, `native_wgpu.rs` and `Cargo.lock`).

Exact parent training-source digest:

`e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`

`ArkSharedLmCheckpoint::read()` in `crates/model_core/src/aof_r1_shared_lm_heads.rs` rejects the manifest if `training.source_digest != shared_lm_training_source_digest()` with `AOFSharedLmTrainingSourceMismatch`.

`crates/model_core/src/aof_r1_admission.rs::ark_runtime_source_digest()` is different. It already includes model-core verifier, backend verifier, CF5 consumer helpers and the runtime campaign, plus `Cargo.lock`.

**Required:** `training_source_digest` may remain identical while `ark_runtime_source_digest` changes due to R2 implementation. A new runtime-source receipt does not justify reusing an older runtime admission receipt. Conversely, runtime digest drift alone does not imply old head-checkpoint weight incompatibility.

---

## 3. Decision A: prefer an existing real backend Q/K/V seam

Implement an **opt-in backend-local verifier observer** at the actual `ArkVerificationDevice::attention()` callsite, without editing the 19 training-hash input files, if and only if an explicit synchronous scope can be safely bound to the correct invocation.

Candidate touch points:

- `crates/burn_webgpu_backend/src/aof_r1_verification.rs` (actual attention callee)
- **new** `crates/burn_webgpu_backend/src/aof_r1_cf5_c_r2_verifier_observe.rs` (scoped permit, owner/queue validation, GPU compare and receipt)
- `crates/model_core/src/aof_r1_runtime.rs` (qualifying session, pool invocation and scoped permit)
- `crates/model_core/src/aof_r1_kv_block_authority.rs` (borrowed session-parking views, only if needed)
- `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs` (qualified scenario and aggregate evidence)
- `crates/model_core/src/aof_r1_admission.rs` (new module / shader exact bytes in runtime digest)
- Native Naga shader-list registration and exact static/negative validator.

**Forbidden in path A:** editing `crates/model_core/src/aof_r1_verification.rs`, the training digest implementation, its 18 other path inputs, or `Cargo.lock` merely to attach a probe.

If path A cannot safely bind, classify `HOLD_CF5_C_R2_BACKEND_SCOPE_UNPROVEN` and follow §17. Do not silently change source lineage.

---

## 4. Invocation-scope SSOT

Create a strictly invocation-local, non-serialized capability equivalent to:

```rust
// Conceptual contract; not existing source or a proven compiling type.
struct ArkCf5VerifierObservePermit {
    session_identity_digest: String,
    request_identity_digest: String,
    canonical_content_generation: u64,
    session_epoch: u64,
    origin_proposal_round: u64,
    consumer_proposal_round: u64,
    physical_device_authority_id: u64,
    physical_queue_authority_id: u64,
    runtime_generation: u64,
    expected_layer_count: usize,
    expected_tree_or_linear: ArkCf5VerifierRoute,
    expected_past_len: usize,
    next_layer_ordinal: usize,
    completion: ArkCf5VerifierScopeCompletion,
}

enum ArkCf5VerifierScopeCompletion {
    NotSubmitted,
    InFlight,
    Completed,
    Failed,
    Unproven,
}
```

Exact field types and ownership are chosen from existing repository identities; the names above are conceptual.

- One scope corresponds to **one real verifier invocation**, not a process-wide mode flag.
- The owner must be the same `ArkVerificationDevice`/live model/device/queue that performs the canonical attention calls.
- No global static or unqualified thread-local mutable observer is an admission authority.
- Another concurrent invocation must not consume or append events to this scope.
- It must remain possible to run canonical `attention()` with zero additional allocations/submissions/waits when OBSERVE is disabled.

---

## 5. Scope binding and same-callsite attribution

Before `pool.with_completed_tree(...)` calls the native verifier, the session obtains a borrowed view of its parked completed OBSERVE backing using the existing exact currentness check:

`ArkCf5CompletedObserveLease::read_views(kv, bound_session, model)`

Require exact:

- request/model/tokenizer/session contract and epoch identity;
- `position_epoch`, `content_generation`, `past_len`, and zero staged append;
- backing/physical device+queue+runtime-generation identity;
- `view.visible == state.kv.past_len` and `capacity >= visible` for **every** layer;
- old `origin_proposal_round` preserved and new `consumer_proposal_round` recorded separately.

Acquire real, strictly borrowed or appropriately pinned `RawWgpuBufferLease` values for the parked capacity-backed K/V; **never fabricate a RawLease or change shape fields to fake compactness**.

Actual verifier scope must bind to the specific live `tree` and expected `linear_oracle` value. If exact tree resource identity cannot be proven with supported WGPU APIs, scope admission is **HOLD**, not a guessed buffer-label comparison.

---

## 6. Concurrency and Rust lifetime safety

The backend `ArkVerificationDevice` is shared through `Arc`; a mutable `Option<Observer>` without synchronization is forbidden.

A feasible scoped implementation must guarantee:

1. Exclusive scoped registration for that verifier-owner invocation, with explicit BUSY on overlap.
2. No `Mutex` held across the entire `aof_forward()` or GPU callback path if its own `attention()` must reenter the same lock.
3. Short, non-recursive state acquisitions at attention boundaries, or a proven equivalent design.
4. No `unsafe` fabricated lifetimes, process-global mutable captures, `transmute`, or reflexive `Send/Sync` assertions.
5. No parked K/V owner destruction until all submitted shadow commands complete.
6. No previous scope receipt or observation permit reused in another session or device generation.
7. A scope cannot be marked PASS if it sees fewer/more attention calls than the bound model's exact layer count.

If Rust's actual trait/lifetime graph does not support safe scoped ownership, **HOLD path A**. Do not relax the binding policy to make it compile.

---

## 7. Per-layer real Q/K/V witness

`ArkVerificationDevice::attention()` must derive the observation from the exact arguments passed to the selected canonical dispatch:

```text
layer N actual canonical Q/K/V leases
          ↓
canonical attention dispatch (unchanged)
          ↓
CF5 capacity-strided shadow attention (opt-in)
          ↓
GPU compare: canonical context vs shadow context
          ↓
real completion witness
          ↓
compact layer receipt
```

`params` from the parent encode:

```text
[0] count
[1] past_len
[2] query_heads
[3] kv_heads
[4] head_dim
[5] anchor
[6] origin
[7] reserved
```

The current scope provides `capacity` and validated `visible_len`, not a substituted fake Tensor shape.

For each layer, require:

```text
observed_layer_ordinal == next_layer_ordinal
params.past_len == scope.expected_past_len == shadow.visible_len
query_heads % kv_heads == 0
shadow K/V shape == [1, kv_heads, capacity, head_dim]
Q / suffix K / suffix V are identical input leases to canonical verifier
canonical output is the actual output lease from that callsite
source and output buffers cannot alias improperly
```

Neither Q/K/V projection nor full-model forward is recomputed solely for observation.

---

## 8. Tree versus linear identity

The actual backend `linear_oracle` flag determines the route:

```text
false → VerifierTree
true  → VerifierLinear
```

The observation permit must bind a concrete expected route before the dispatch and reject route drift.

- A tree result may not qualify linear coverage.
- A linear fixture with no eligible live completed backing may be recorded as `NOT_APPLICABLE` or `HOLD`, not `PASS`.
- Existing tree rows, parent/index topology, anchor/origin and suffix visibility remain unchanged.
- Do not create a second independent `aof_forward()` replay and label it the current canonical verifier.
- Do not infer actual execution from shader existence or from an isolated diagnostic crate.

---

## 9. Backend-only candidate GPU comparison

The existing `ArkCapacityConsumerPrograms::verifier()` accepts real `RawWgpuBufferLease` inputs but currently expects a `RawWgpuBufferLease` output.

Preferred implementation: add a **backend-owned candidate output buffer path**, with an explicitly validated `wgpu::Buffer` (or a safely constructed existing owned-output abstraction), rather than fabricating `RawWgpuBufferLease` metadata merely to satisfy the old signature.

The GPU comparison must:

- use the same real device/queue and preserve their submission order;
- compare candidate context with the canonical `attention()` output;
- emit `u32` bitwise mismatch count, first mismatch and finite-status counters, plus actual max-absolute-error source if implemented;
- use a small bounded status readback only after the real queue-completion authority;
- perform **no full Q/K/V, full context, or full FuturePool tree D2H**;
- count all observation-only submits, readbacks, waits and scratch separately from CF4 canonical accounting.

**Numerical rule:** zero bitwise mismatches may establish exact context parity for an actually executed identical input. A nonzero difference is `HOLD_UNQUALIFIED_NUMERICAL_PARITY` unless a separately predeclared, parent-authorized tolerance exists. `max_abs == 0` alone cannot substitute for bitwise identity (including signed zero / non-finite cases).

---

## 10. Real GPU completion and retirement

For each scoped attention observation:

```text
Canonical submit
  → same-queue shadow submit
  → same-queue comparison submit
  → actual Queue completion callback / proven equivalent
  → status readback
  → scoped receipt finalization
  → temporary GPU resources retired
```

The exact number of submissions may be optimized if the *actual implementation* and receipt show them; do not invent one-submit counts.

`completion=InFlight | Unproven` forbids release/reuse of resources still used by the queue. If any layer fails, retain/retire through the existing completion authority; no automatic `mem::forget` leak of proven completed work.

Source-level zero-wait assumptions are not physical evidence. `OBSERVE` overhead is additional and **must never be reported as canonical execution cost**.

---

## 11. Scope teardown on all exits

Provide explicit closure for:

```text
normal verifier completion
candidate numerical mismatch
invalid/missing parked backing
stale currentness
GPU validation failure
device lost / queue failure
cancel / EOS / stop
panic/unwind where Rust cleanup applies
repeated session / concurrent scope conflict
```

A scope guard's Drop may revoke the admission permit, but may not fabricate GPU completion or prematurely release in-flight backing. A previous generation's callback must not retire a successor scope.

In ordinary production LEGACY/OFF, the absence of a scope must not generate a new GPU allocation, dispatch, readback, or wait.

---

## 12. Actual session-to-verifier callsite

The latest parent has:

- `ArkDecodeSession.parked_cf5` as the single completed session-local OBSERVE backing.
- `ArkDecodeSession::cf5_parked()` for immutable access.
- `aof_r1_runtime.rs`: the actual verification call is inside the `pool.with_completed_tree(...)` closure that calls `model.verify_aof_r1_tree_depth(...)`.

R2 shall bind the scoped permit immediately around that **specific real verifier call**, using disjoint borrows of `pool` and `parked_cf5` where Rust permits.

Required:

- actual session's parked owner; not a deserialized JSON receipt;
- exact current completed `ArkPoolTicket` and fresh proposal identity;
- model target-resource `ArkVerificationDevice` matches the verifier call;
- bound session and current canonical KV `state.kv` do not mutate between admission and completion;
- acquisition / teardown on every `Result` path, no stale observer mode surviving the closure.

When there is no parked backing (e.g. first proposal), normal canonical verifier behavior continues. An explicitly requested R2 physical test records **`HOLD_CF5_C_R2_NO_COMPLETED_BACKING`** rather than claiming full route coverage.

---

## 13. Minimal shape and policy preservation

No changes permitted to:

```text
canonical Q/K/V projection and rotation
original tree/linear attention WGSL math
root, anchor, origin, parent/index semantics
actual selected logits/target choices
FuturePool dedupe/compact and completion
sampling, EOS, cancel, emit, STOP and ACK
KV committed length / content generation
head-only optimizer and training tensors
Vocab tiles or numerical acceptance thresholds
existing CF5-C-R1 Burn route observations
```

The actual canonical verifier output remains authoritative; the capacity consumer output is nonpublishing.

---

## 14. Explicit lineage fork only if backend scope is impossible

Path B is **conditional**, never silently combined with Path A:

`AOF-R1-CF5-C-R2B-EXPLICIT-VERIFIER-SEAM-NEW-TRAINING-LINEAGE`

Only initiate it after a recorded blocker demonstrates that Path A cannot safely bind per-session Q/K/V to a real verifier invocation.

Possible Path B implementation:

- modify the exact private `aof_forward()` owner with a narrow opt-in typed callback at the actual per-layer attention callsite;
- preserve normal OFF/LEGACY execution as an equivalent branch with the original canonical dispatch;
- do not change head math, training VJP, cache values, root logits, KV shape, or output order;
- register the observer implementation and shader bytes in `ark_runtime_source_digest()`;
- recompute the 19-input `shared_lm_training_source_digest()` and bind a **new** head-checkpoint training lineage.

**Source admission warning:** a modification to `aof_r1_verification.rs` changes the current `shared_lm_training_source_digest()` even when its training math is nominally preserved. Existing manifests will be rejected by the unchanged strict reader. This is expected; it is **not a reason to disable that validation**.

---

## 15. Checkpoint and manifest handling in Path B

Forbidden:

```text
old manifest.training.source_digest rewritten in place
old checkpoint weights/manifest silently resealed
'previous digest' allowlist grafted into ArkSharedLmCheckpoint::read()
checkpoint shape/binding validators relaxed
training.source_digest derived from a claimed equivalence instead of exact bytes
source-only equivalence promoted to real training/quality parity
```

Required if Path B is selected:

1. Seal parent source/weights/manifest and parent head training digest as immutable artifacts.
2. Build a new exact-source training or separately authorized fresh checkpoint-production route under the new 19-input digest. Prefer the existing **head-only training** path; do not retrain the entire base model merely due to source lineage.
3. Emit a new manifest/checkpoint with the existing canonical trainer's serialization and strict hashes. It is a **new artifact lineage**, not an overwrite of the old one.
4. Independently requalify two ranks, held-out +2/+3/+4/+5, prefix acceptance and GPU/commit matrices under the new lineage.
5. Keep old weights as historical evidence only until a separately specified migration process can justify any direct weight reuse. Do not invent an equivalence token.

If exact model/dataset/training inputs for the new lineage are unavailable, **HOLD**, do not silently use the old checkpoint.

---

## 16. Path-A training-digest freeze gate

If backend-only Path A is selected, the static validator must read the **actual exact 19 input file bytes** from the two code-only revisions and require:

```text
input_count == 19
all 19 path labels unchanged
all 19 source bytes unchanged
parent_digest == current_digest
parent_digest == e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283
```

No fake manifest digest is permitted. The normal `ArkSharedLmCheckpoint::read()` must still reject a tampered training digest, altered weights digest, changed shape/rank, wrong tokenizer/model binding and stale manifests.

Simultaneously the changed runtime-source digest must be recomputed on the new source tree and old runtime admission receipts must be rejected as stale.

---

## 17. Candidate receipt ABI

Proposed per-invocation receipt:

`aof_r1_cf5_c_r2_verifier_native_scope_<case>.json`

At least:

```text
schema = ash.aof_r1.cf5.c.r2.verifier_native_scope.v1
source_tree_digest
runtime_source_digest
training_source_digest
lineage_branch = BackendPreserved | NewTrainingLineage | HOLD
model / tokenizer / checkpoint / manifest identity
session / request / old-round / new-round identity
device / queue / runtime generation
parked backing owner and generation
canonical KV generation / visible_len / capacity
pool ticket / completed tree identity
selected route = Tree | Linear
expected layer_count / actual observed layer_count
per-layer params shape/hash, buffer identity and counts
actual qkv producer = BackendAttentionArguments
canonical result remains authoritative = true
bitwise mismatches / first mismatch / finite status
numerical tolerance source or UNKNOWN
GPU submission / completion / retirement counts and actual sources
shadow extra readback / waits (separate from CF4)
first failure and qualified coverage
head_training_digest_match
runtime_receipt_currentness
production_admission = false
promoted = false
performance = NOT_PROMOTED
receipt_hash
```

No `PASS` field may be inferred solely from literal zero initialized counters or from 'shader exists'.

---

## 18. Scope and lineage campaign matrix

Required cross-product of actually supported scenarios:

| Axis | Cases |
|---|---|
| Verifier route | Real Tree; Real Linear (where native invocation exists) |
| Depth | D1, D2, D4 (actual selected verification depth) |
| Backing | Completed correctly parked; missing; stale; wrong owner/device |
| Length | Nonempty prefix, head-major capacity greater than logical visible length; boundary at capacity |
| Concurrent use | second scope rejected, no cross-session attribution |
| Failure | numerical mismatch, GPU validation, callback failure, duplicate finish, panic-unwind |
| Checkpoint | exact old digest; changed training-file bytes; changed manifest/weights; lineage A/B switch |
| Canonical | matching token/text/stop/KV logical position; EOS/cancel/emit/duplicate preservation |

At least one real accepted-block → parked backing → **next proposal's** real verifier attention is required. An OBSERVE-only synthetic buffer with equivalent shape is insufficient.

D1/D2/D4 and Tree/Linear coverage must be recorded separately: unsupported or unexecuted combinations are `NOT_APPLICABLE` / `NOT_RUN`, never copied PASS entries.

---

## 19. Required negative gates

At minimum:

```text
FAIL_CF5_C_R2_WRONG_VERIFIER_INVOCATION
FAIL_CF5_C_R2_CROSS_SESSION_OBSERVER
FAIL_CF5_C_R2_SCOPED_OWNER_CONFLICT
FAIL_CF5_C_R2_STALE_BACKING_GENERATION
FAIL_CF5_C_R2_STALE_DEVICE_QUEUE
FAIL_CF5_C_R2_EXPECTED_LAYER_COUNT_MISMATCH
FAIL_CF5_C_R2_TREE_LINEAR_ROUTE_DRIFT
FAIL_CF5_C_R2_VISIBLE_EXCEEDS_CAPACITY
FAIL_CF5_C_R2_HIDDEN_TAIL_ACCESS
FAIL_CF5_C_R2_FAKE_RAW_BUFFER_LEASE
FAIL_CF5_C_R2_FULL_QKV_READBACK
FAIL_CF5_C_R2_CANONICAL_OUTPUT_SUBSTITUTED
FAIL_CF5_C_R2_EARLY_OWNER_RETIREMENT
FAIL_CF5_C_R2_UNPROVEN_COMPLETION_ADMITTED
FAIL_CF5_C_R2_CHECKPOINT_SOURCE_DIGEST_DRIFT
FAIL_CF5_C_R2_OLD_MANIFEST_RESEALED
FAIL_CF5_C_R2_LOSS_OF_STRICT_HEAD_ADMISSION
FAIL_CF5_C_R2_PARENT_C4_ACCOUNTING_DRIFT
FAIL_CF5_C_R2_FALSE_PHYSICAL_PASS
```

Static negative mutations MUST include: remove real backend hook; route Tree as Linear; alter prefix visibility; omit shader from runtime digest; mutate one of 19 training source bytes; disable `ArkSharedLmCheckpoint::read` mismatch check; allow duplicate scope; clear pending resources before completion; replace actual backend arguments with fabricated Tensor/lease metadata; promote zero-initialized event counters.

---

## 20. Verification commands and feature resolution

Execute on the exact new code-only source with required exact workspace path dependencies present:

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
```

Discover and use actual manifest feature names before running the new qualified observer test/binary; do not invent a command switch as a finished CLI feature.

Run existing and new exact Rust tests for scope exclusivity, owner/epoch, duplicate/drop/retirement, source-digest stability and strict checkpoint loader negative paths. Validate new WGSL with actual current Naga/WGPU shader validation.

Then run real same-GPU, same-model, same-checkpoint campaigns for D1/D2/D4, Tree and supported Linear, with a completed parked backing and natural next-proposal verifier entry. Record source-bound runtime/physical receipt and existing CF4 canonical cost counters separately from OBSERVE probe overhead.

An exact missing sherpa-rs vendor path is a **workspace input HOLD**, not permission for a dummy dependency or false compile PASS.

---

## 21. Parent and resource non-regression

All required previous validators remain meaningful:

```text
CF5-C-R1 source/static preservation
CF5-C reader and WGSL ABI
CF5-A/B stage/compare and backing identities
CF4 real canonical cost source
CF3 head-quality eval paths
CF2 packet and packed lease retirement
VH6 quality/GPU/commit proof requirements
CF1 native compile contracts
```

The historical CF1/CF2/VH6 parent validator had a known 1/52 byte-preservation mismatch for `aof_r1_prefix_commit.rs`, superseded by CF4; do not relabel it as 52/52 or erase its evidence. The R2 validator must explicitly preserve remaining predicates and record exact supersession lineage for the conflicting byte-only check.

Nothing in R2 permits new ordinary decode headwise/TensorCube claims, canonically committed capacity backing, block-commit ACTIVE, new speculative depth or head production cutover.

---

## 22. Explicit state classification

All evidence reports SHALL use non-overlapping statuses:

```text
SOURCE_IMPLEMENTED
STATIC_PASS
COMPILE_PASS
RUNTIME_PASS
PHYSICAL_PASS
HOLD_INPUT_ABSENT
HOLD_SCOPE_UNPROVEN
HOLD_NUMERIC_PARITY_UNQUALIFIED
HOLD_NEW_CHECKPOINT_LINEAGE_REQUIRED
NOT_APPLICABLE
NOT_RUN
UNKNOWN
```

One status may never be inferred from another. Especially:

- `RAW_QKV_BACKEND_ARGUMENTS_PRESENT` is not `SAFE_SCOPED_OBSERVER_PROVEN`.
- `TRAINING_DIGEST_UNCHANGED` is not `PHYSICAL_VERIFIER_PARITY_PASS`.
- `GPU_COMPLETION_OBSERVED` is not `NUMERIC_PARITY_PASS`.
- `VERIFIER_SCOPE_PASS` is not `ALL_CF5_C_CONSUMER_PASS`.

---

## 23. Completion and branch law

**Path A source/compile qualifier** may proceed when a backend-only observer compiles without changing the 19 training source inputs, scope ownership and currentness are explicit and the original canonical verifier attention semantics are preserved.

**Path A physical qualifier** additionally requires real Tree/Linear coverage as declared, GPU compare output, proven completion/retirement, zero cross-session/layer identity errors, and strict head-checkpoint admission with the old exact training digest. Numerical mismatches without a sealed admissible threshold are HOLD.

**Path B** may begin only with explicit evidence that Path A is blocked and an accepted lineage change specification. It requires a new head checkpoint under its new exact training-source digest. It may not present old head weights/manifest as already admitted.

A scope-limited token such as:

`PASS_AOF_R1_CF5_C_R2_BACKEND_VERIFIER_OBSERVE_PHYSICAL`

may be emitted **only after its specific exact real GPU campaign passes**. Its presence does not authorize:

`PASS_AOF_R1_CF5_C_CAPACITY_STRIDED_KV_CONSUMER_BRIDGE`

or:

`PASS_AOF_R1_CF5_BLOCK_PREFIX_COMMIT_KV_CAPACITY_AUTHORITY`

or CF5-D ACTIVE canonical publication.

If safe scope construction or physical same-source QKV/owner proof fails, issue:

`HOLD_AOF_R1_CF5_C_R2_VERIFIER_SEAM_UNQUALIFIED`

with the first failure/unsupported authority.

---

## Final invariant

```text
EXACT NATIVE VERIFIER Q/K/V
+
BACKEND OBSERVER SCOPE BOUND TO SAME INVOCATION
+
PARKED CAPACITY BACKING CURRENT
+
CANONICAL OUTPUT PRESERVED
+
REAL GPU COMPLETION AND NUMERIC PARITY
+
STRICT CHECKPOINT LINEAGE
=
VERIFIER OBSERVE QUALIFIED

NOT YET = COMPLETE CF5-C CONSUMER QUALIFICATION
NOT YET = CF5-D ACTIVE CANONICAL KV
NOT YET = PERFORMANCE PROMOTION
```

**Implementation-state supersession:** The source ZIP includes the Tree verifier OBSERVE integration candidate. This is not a Rust compile receipt, real GPU physical PASS, complete R2 closure or checkpoint lineage promotion.

---

## Source bake annex / exact implementation status (2026-10-09)

The report below records the current code-only SOURCE implementation, physical validation gaps, and exact SHA lineage. These observations do **not** replace the target completion contract above.

# AOF-R1-CF5-C-R2 / VERIFIER NATIVE SEAM + CHECKPOINT LINEAGE QUALIFICATION

**Source bake report, 2026-10-09 (Asia/Seoul)**

## Exact parent

- Parent code-only: `ASH_PASS3_AOF_R1_CF5_C_R1_NATIVE_CONSUMER_CALLSITE_HANDOFF_CODE_ONLY.zip`
- Parent SHA-256: `d568bc6a3f9a9d75b9d5b9b684c8e180c83578330f9262eecafdef0d063363fd`
- Parent file count: 8,731

## Baked outputs

- Full: `ASH_PASS3_AOF_R1_CF5_C_R2_VERIFIER_NATIVE_SEAM_CHECKPOINT_LINEAGE_QUALIFICATION_CODE_ONLY.zip`
  - SHA-256: `461e7509db39278bf1a1d05f7673d0fda8a0a3d17abdca63b84ca77b0d8038cb`
  - Files: 8734
- Overlay: `ASH_AOF_R1_CF5_C_R2_VERIFIER_NATIVE_SEAM_CHECKPOINT_LINEAGE_QUALIFICATION_OVERLAY_CODE_ONLY.zip`
  - SHA-256: `743859d538b1daf70951c0a71acf550dd295ce24d9ca0221f64abbe9cf15c909`
  - Delta: ADD 3 / MOD 10 / DEL 0
- ZIP CRC: **PASS**; exact member byte comparison with parent and working source: **PASS**
- Actual SHA manifest: `ASH_AOF_R1_CF5_C_R2_BAKE_MANIFEST.json`.

## SOURCE implementation

### R2-A Actual backend attention scope, no private verifier edit

- `crates/burn_webgpu_backend/src/aof_r1_cf5_c_r2_verifier_observe.rs`: exclusive one-slot `Mutex<Option<...>>` scoped by actual `ArkVerificationDevice`, same exact wgpu Buffer/tree, expected Tree/Linear route, actual layer ordinal, bound thread and same physical runtime authority.
- `crates/burn_webgpu_backend/src/aof_r1_verification.rs`: inserts hook **after** the existing canonical `self.dispatch(...)?`, preserving exactly the canonical Q/suffix K/suffix V and context output raw leases. In Legacy/Off, the new scope is `None`: no shadow GPU allocation/submission/readback/wait.
- Scope guard Drop revokes permission on every Rust error path. Completion remains required before publishing a layer witness. Missing scope or observed layer-count mismatch cannot emit R2 PASS.

### R2-B Completed session backing → real FuturePool tree

- `crates/model_core/src/aof_r1_runtime.rs`: opted in only for `ArkKvBlockCommitMode::Observe` when parked completed shadow exists. `parked.read_views()` validates canonical session/KV currentness. Same original proposal round is maintained separately from current `receipt.identity.proposal_round`; no source identity is rewritten.
- Leases are strictly derived through `model.aof_lease()` of the actual parked capacity-backed K/V tensors. Scope begins **inside** the real `pool.with_completed_tree` closure, immediately around the real `model.verify_aof_r1_tree_depth` call. Failure and success paths both terminate the scope.
- Both verification-only and adopted-step callsites move real observed events into `DecodeState` and then `GenerationTelemetry`, without publishing shadow KV.

### R2-C Read-only GPU context bitwise parity candidate

- WGSL `shaders/aof_r1_verifier_context_bitwise_compare.wgsl` compares raw `u32` bits of actual canonical vs capacity-strided shadow attention contexts; status is `{bitwise_mismatch_count,first_mismatch,nonfinite_count,compared_count}` (4×u32).
- Actual native shader work is scheduled on the same WGPU Queue with completion/poll verification and an existing bounded readback helper. Entire context / entire QKV / FuturePool tree is never copied to CPU.
- Nonzero bitwise difference or any nonfinite observation is **HOLD_NUMERIC_PARITY_UNQUALIFIED**, not a tolerance-based PASS; true GPU bitwise zero is eligible to be called exact for that covered layer only.
- All CF5 shadow costs are excluded from CF4 canonical attribution using its existing shadow trace guard.
- Actual Tree verifier callsite is integrated. Linear program exists but is **not** integrated into a qualified live linear invocation/campaign; Tree≠Linear and no inferred D1/D2/D4 physical coverage.

### R2-D Strict checkpoint-source lineage

- The 19 byte-identical `shared_lm_training_source_digest()` inputs, including private `model_core/src/aof_r1_verification.rs`, were preserved: `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
- Only backend verifier, model-core AOF runtime/admission, telemetry, native qualification reader, shader and static validator changed. New backend observer+shader bytes are registered in `ark_runtime_source_digest()`; the **runtime digest changes**.
- No old checkpoint manifest was rewritten, no digest allowlist was introduced, and a new training-checkpoint lineage was **not** created. Path B remains a conditional later revision only after Path A is proven blocked.

## Evidence and non-admission

| Level | Result |
|---|---|
| R2 SOURCE | Implemented candidate, not yet compiled |
| R2 STATIC | 44/44 PASS |
| Negative source mutations | 12/12 detected/rejected |
| Parent CF5-C-R1 | 66/66 PASS |
| Parent CF5-C | 62/62 PASS |
| Parent CF5-A/B | PASS (existing validator) |
| Parent CF4 | PASS (existing validator) |
| Parent CF3 | PASS (existing validator) |
| Legacy CF1/CF2/VH6 byte-only gate | 51/52; known CF4 supersession of aof_r1_prefix_commit.rs |
| Training source digest | Exact unchanged, 19 inputs |
| Cargo / Rust COMPILE | NOT_RUN (cargo/rustc unavailable) |
| Native Naga shader validation | NOT_RUN |
| Actual Tree WGPU PHYSICAL | NOT_RUN |
| Actual Linear WGPU PHYSICAL | NOT_RUN |
| Numeric parity / completion / retirement | NOT_MEASURED |
| Performance / full CF5-C / CF5-D ACTIVE | UNKNOWN / HOLD / FORBIDDEN |

**Package input blocker:** root workspace manifest includes `crates/asr_sidecar` with external `vendor/sherpa-rs-main/crates/sherpa-rs`, missing from this code-only ZIP. Do not invent a dummy crate, change workspace membership or silently substitute a registry package.

### Actual required execution

```powershell
python .\tools\validate_ash_aof_r1_cf5_c_r2_verifier_scope_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_consumer_bridge --release --locked -j 1
```

Actual GPU campaign must exercise a **completed accepted block → parked shadow → next-proposal same bound FuturePool Tree** and actual D1/D2/D4 layer parity in supported routes. Linear requires its own selected native qualification call with an actual completed parked backing. No `PASS_AOF_R1_CF5_C_R2_BACKEND_VERIFIER_OBSERVE_PHYSICAL` may be emitted based on SOURCE/STATIC alone.

## First risks to verify during COMPILE / PHYSICAL

1. The backend owner `Mutex<Option<...>>` introduces trait/monomorphization obligations and must be proven with real `cargo check` in the full workspace.
2. Exact raw WGPU lease and Tree Buffer owner currentness must be observed from the real session, including repeated sessions, concurrent scopes and GPU errors.
3. The two new shader pipelines need actual Naga/WGPU validation and numeric parity on the device. Merely listing the shader is not an execution result.
4. The backend scope guard must never drop a resource still in GPU flight after device loss; explicit physical retirement and failure campaigns are outstanding.
5. The source emits layer-local events but **does not** materialize an R2 physical campaign-level PASS receipt. Output stays per-case audit/telemetry and full R2 remains HOLD.

## Final state

`SOURCE APPLIED / STATIC PASS / COMPILE NOT_RUN / PHYSICAL NOT_RUN / PERFORMANCE NOT_MEASURED / FULL CF5-C-R2 HOLD / CF5-D ACTIVE FORBIDDEN`.
