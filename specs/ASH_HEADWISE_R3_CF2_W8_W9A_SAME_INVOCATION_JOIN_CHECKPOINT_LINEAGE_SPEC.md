# HEADWISE-R3-CF2
## W8/W9A SAME-NATIVE-INVOCATION RECEIPT JOIN + CHECKPOINT LINEAGE QUALIFICATION

**Revision:** `HEADWISE-R3-CF2`  
**Parent:** `HEADWISE-R3-CF1 SELECTED PRODUCTION OUTPUT + W8/W9A INVOCATION CLOSURE`  
**Successor:** `HEADWISE-R3-CF3` selected-output canonical reference qualification, or the subsequent Headwise/TensorCube capacity-strided consumer revision after independent physical gates  
**Class:** native invocation provenance, measured parity evidence, strict checkpoint/source lineage  
**Status (2026-10-09): PARTIAL SOURCE BAKE / STATIC 41/41 PASS / NEGATIVE STATIC 26/26 REJECTED.** W8 original comparator receipt is typed-joined to the same native W9A layer receipt in SOURCE, without a second comparator call. One of the 19 original head-training source inputs (`native_wgpu.rs`) changed. New checkpoint lineage creation/qualification, Rust COMPILE, real GPU PHYSICAL and independent W8 Queue-completion evidence remain **HOLD / NOT_RUN**. Legacy W9A route policy and original W9A receipt format are preserved. Details in source-bake annex.

```text
HEADWISE-R3-CF2

W8/W9A SAME-NATIVE-INVOCATION RECEIPT JOIN
+ CF1 ORIGINAL W8 RECEIPT VALIDATOR PRESERVATION
+ SAME-CALL W8 COMPARATOR OWNERSHIP
+ W9A LAYER RECEIPT EXACT SHA BINDING
+ REAL CANDIDATE INVOCATION DIGEST MATCH
+ MODEL / SESSION / STEP / LAYER / NONCE CURRENTNESS
+ SAME DEVICE / SAME QUEUE PHYSICAL AUTHORITY
+ W8 NUMERICAL RESULT != W9A ROUTING DECISION
+ NON-SAMPLED != MEASURED
+ COMPARATOR FAILURE != ZERO MISMATCH
+ ACTUAL QUEUE CALLBACK != MAP CALLBACK
+ BOUNDED IN-MEMORY JOIN LEDGER
+ ONCE-ONLY JOIN PUBLICATION / RETIREMENT
+ STRICT 19-INPUT HEAD CHECKPOINT SOURCE LINEAGE
+ NO NATIVE_WGPU HASH EXEMPTION OR DIGEST RESEAL
+ NO UNSOURCED LEGACY CHECKPOINT ADOPTION
+ ORIGINAL W9A PRE-SAMPLER POLICY PRESERVATION
+ NO FULL CONTEXT HOST READBACK
+ NO ADDITIONAL W8 COMPARATOR DISPATCH
+ NO PACKED / HEADWISE / CF5-D ACTIVE PROMOTION
+ NO PHYSICAL PASS WITHOUT REAL WGPU EXECUTION
```

---

## 0. Evidence baseline, exact parent

Source inspected: `ASH_PASS3_HEADWISE_R3_CF1_SELECTED_PRODUCTION_OUTPUT_W8_W9A_INVOCATION_CLOSURE_CODE_ONLY.zip`.

```text
parent_zip_sha256:
f335e0f9a6b7df4d16cc8ce66c8f6b3098172095203fbc7ba4ecf4cd75c0cb5b

parent_entries: 8747
parent_cf1: SOURCE PARTIAL / STATIC 42/42
parent_cf1_negative_static: 21/21 rejected
parent_compile: NOT_RUN
parent_naga: NOT_RUN
parent_gpu_physical: NOT_RUN
parent_w8_w9a_same_invocation: HOLD
```

The parent also has an independent selected-production fixture whose caller-supplied reference digest is **not** proof of canonical reference provenance. That admission remains HOLD and is **outside** the CF2 join implementation.

## 1. Concrete source callsites and facts

**CONFIRMED / SOURCE:**

1. `crates/model_core/src/native_wgpu.rs:17107–17143`: `compare_attention_decode_w9a_contexts()` constructs and returns an actual `AttentionInterconnectW8BackendParityReceipt` from the current native runtime Device/Queue.
2. `native_wgpu.rs:18126–18143`: in the `w9a_sampled_audit` branch, the W8 receipt is stored in the local `parity` variable; only `parity.pass` is copied into `context_parity_pass` (plus fault policy). The receipt identity and SHA are not carried to the W9A layer receipt.
3. `native_wgpu.rs:18157–18217`: TensorCube-selected or rollback `AttentionDecodeW9ALayerRouteReceipt` is sealed and recorded without the W8 invocation digest. Unsampled `HeadwiseDefault` also records `context_parity_pass: true` without comparison (`18123–18245`).
4. `crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs:96–146,267–300,449–493`: W8 receipt carries `invocation_identity_digest`, pipeline identity/digest, geometry, compact status, failure counters, `comparison_completion_observed`, numerical verdict and receipt digest.
5. `...attention_interconnect_w8_context_parity.rs:408–430`: current W8 comparator submits one command buffer and waits for a **map_async callback** via `PollType::Wait`; `comparison_completion_observed` is derived from GPU status words 25 and 26. An independent `Queue::on_submitted_work_done` callback is **not** shown at this boundary. Those kinds of completion evidence must not be relabeled.
6. `crates/model_core/src/attention_decode_w9a_production_runtime.rs:78–109`: W9A layer route receipt has no comparator invocation or W8 receipt SHA. Its `context_parity_pass` is an existing routing/compatibility gate, not a measured evidence enum.
7. `crates/model_core/src/headwise_r3_cf1_w8_join_evidence.rs:33–103`: the CF1 verifier authenticates a standalone W8 receipt but intentionally emits `w9a_same_invocation_proven=false` and `MeasurementUnavailable`. Joining JSONs after the fact by session/step strings is not acceptable.
8. `crates/model_core/src/aof_r1_shared_lm_head_math.rs:77–108`: `shared_lm_training_source_digest()` includes 19 byte inputs, **including `native_wgpu.rs` and `Cargo.lock`**. Recomputed exact current digest:

```text
e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283
```

**SUPPORTED:** The two receipts coexist within the lexical W9A sampled branch. A narrow, typed in-call join is the appropriate construction point. **UNKNOWN:** whether the required change can be implemented without modifying a checkpoint-hashed input; the observed current code provides no already-verified external same-call join seam. Do not claim compatibility with old checkpoints by assumption.

## 2. Patch scope and non-goals

**In scope:** capture the original W8 receipt once, bind it to the exact W9A layer decision from the same native invocation, preserve proof after the candidate resources are retired, and record source/checkpoint compatibility accurately.

**Out of scope:** changing the W8 numerical shader, W9A canary sampling or routing percentages, W9A pre-sampler admit/rollback decisions, `HEADWISE-R1/R2` default policies, canonical KV/selected token/stop/emit, `HEADWISE-R3-CF1` canonical reference qualification, CF5 capacity-strided ACTIVE, token/s performance tuning.

No source/STATIC-only outcome qualifies these physical claims.

## 3. Mandatory same-call join authority

A valid join requires **both original sealed receipts** to be reachable inside the same native invocation before its layer authority is forgotten.

```text
native Headwise incremental invocation
  ├─ actual candidate + Headwise preprojection handles
  ├─ existing W8 comparator (only when sampled)
  │    └─ original W8 receipt (owned, sealed, completion status)
  ├─ existing W9A route decision / fault handling
  │    └─ original W9A layer receipt (sealed)
  └─ join in the same lexical ownership scope
       ├─ both receipt digests
       ├─ candidate invocation identity
       ├─ native session / layer / device / queue binding
       └─ one bounded audit ledger append
```

**Forbidden:** filesystem post-hoc timestamp matching, joining by session/step only, a process-global unscoped observer, TLS guesswork, reading JSON receipts back as live authority, matching a W8 receipt to a later layer of the same step, or executing a second W8 comparator merely to obtain its receipt.

## 4. New explicit identity binding (proposed types)

The following are **proposals**, not existing source declarations. Reuse existing canonical native identifiers instead of inventing a new source of truth.

```rust
struct HeadwiseR3Cf2InvocationIdentity {
    model_instance_id: String,
    model_instance_epoch: u64,
    checkpoint_digest: String,
    tokenizer_digest: String,
    decode_session_id: String,
    decode_session_epoch: u64,
    decode_step: u64,
    layer_index: u32,
    attention_invocation_generation: u64,
    candidate_nonce: u64,
    candidate_invocation_digest: String,
    runtime_device_identity: String,
    runtime_queue_identity: String,
    source_digest: String,
}

struct HeadwiseR3Cf2JoinedLayerEvidence {
    identity: HeadwiseR3Cf2InvocationIdentity,
    w8_receipt_sha256: Option<String>,
    w8_pipeline_identity_sha256: Option<String>,
    w9a_layer_receipt_sha256: String,
    measured_parity: W9AContextParityEvidence,
    w8_numerical_pass: Option<bool>,
    legacy_route_gate_pass: bool,
    route: AttentionDecodeW9ARouteId,
    completion: HeadwiseR3Cf2CompletionEvidence,
    lineage: HeadwiseR3Cf2LineageAuthority,
    join_state: HeadwiseR3Cf2JoinState,
    receipt_sha256: String,
}
```

Actual names may follow established naming rules. The join key MUST be derived from canonical typed invocation fields plus candidate identity, not merely a timestamp, sequence number or guessed string.

## 5. Currentness and equality gates

Before joining, require:

```text
W8.invocation_identity_digest
  == actual bundle.context_candidate_handle.invocation_identity_digest

W8 Headwise and TensorCube geometry
  == W9A actual invocation shape / selected layer geometry

W9A receipt session/epoch/step/layer/seq_kv
  == natural native invocation snapshot

model/tokenizer/checkpoint identity current
attention invocation generation current
candidate nonce / route source current
same actual Device/Queue handles used by selected Headwise and W8
W8 receipt and pipeline identity digests valid
W9A original seal valid
```

The W8 receipt does not itself contain every session/step/layer field. The missing binding must come from the **same native call's captured canonical state**, not from the W8 digest string interpreted as a decoded structure. Store both the candidate digest and exact typed scope fields.

Reject stale session, model epoch, candidate generation, layer reorder, duplicate invocation ID and cross-device/queue evidence.

## 6. Independent measurement and routing policy

Do not change the meaning of the existing W9A `context_parity_pass: bool` during this patch. This field is used by existing route/pre-sampler admission logic.

Introduce independent evidence from the real W8 comparator:

```rust
enum W9AContextParityEvidence {
    NotMeasured,
    MeasuredPass,
    MeasuredFail,
    MeasurementUnavailable,
}
```

Reuse the enum already present in `headwise_r3_w9a_parity_evidence.rs`; do not create a second incompatible enum.

| Native condition | Evidence | Existing route policy |
|---|---|---|
| `HeadwiseDefault`, no W8 | `NotMeasured` | unchanged |
| TensorCube canary, unsampled | `NotMeasured` | unchanged |
| Sampled W8 completed, `w8.pass=true` | `MeasuredPass` | unchanged; still checks fault policy |
| Sampled W8 completed, `w8.pass=false` | `MeasuredFail` | existing rollback/quarantine policy |
| Sample requested but comparator never returned a valid receipt | `MeasurementUnavailable` or explicit failure | existing error/failure policy preserved |
| Valid W8 numerical PASS plus forced `ContextMismatch` | `MeasuredPass` **for W8 only** | forced route rejection is separately recorded |

A fault-injected route rejection is not retroactively a W8 numerical failure. Conversely, `context_parity_pass=true` on unsampled W9A is not evidence of measured W8 parity.

## 7. Original receipt ownership and resource lifetime

The W8 original receipt (small owned CPU object) must remain in the current stack until both W9A route decision and sealed layer receipt are available. No re-dispatch, full Q/K/V readback or additional staging tensor is permitted.

When candidate/row-classification handles call `terminal_drain()`, the original W8 receipt and exact candidate invocation digest are retained as small copied metadata. Physical handle retirement remains governed by the prior W9A code.

If comparison or owner retirement fails before any valid W9A layer receipt exists, record a **failed/unavailable observation**, not a fabricated joined PASS. A pending submission is never freed early just to complete the audit.

## 8. Distinguish completion authorities

The existing W8 receipt's `comparison_completion_observed` is derived from GPU status words. Current `map_async + PollType::Wait` is a real mapped status readback, but **does not itself identify a separate Queue completion callback**.

Evidence MUST distinguish:

```text
w8_compare_dispatch_observed
w8_finalize_dispatch_observed
w8_queue_submit_observed
w8_map_callback_observed
w8_status_copy_readback_observed
w8_gpu_status_terminal_observed
w8_queue_completion_callback_observed: Option<bool>
```

An explicit `Queue::on_submitted_work_done` observation may be introduced **only on the existing sampled W8 work**, with bounded pending ownership and no new submission or full buffer readback. If no distinct callback is registered, `w8_queue_completion_callback_observed=None`, not `true`.

Full physical qualification requires proven completion with the precise declared authority. Do not count one callback under two names.

## 9. Bounded session-local join ledger

Prefer the existing `attention_decode_w9a_runtime` owner (or a narrowly owned equivalent) for a bounded record of joined layer observations:

```text
key = (session_id, session_epoch, decode_step, layer_index,
       attention_invocation_generation, candidate_nonce)

value = original W8 digest + original W9A digest + exact source binding
```

Requirements:

- no unbounded `Vec` growth per token across sessions;
- one join per native selected layer invocation;
- duplicate publish returns an explicit error/receipt;
- stale candidates cannot overwrite a current join;
- joined observations retire/compact with session/step terminal closure;
- no query of a global mutable ledger to *guess* the comparator after the invocation;
- audit disk receipts cannot be deserialized to create live approval.

A bounded ledger may remain disabled in default/unsampled routing. Any new memory/serialization cost must be separately measured.

## 10. Publication/commit ordering

**Source design goal:** extend the natural W9A branch with a local `Option<AttentionInterconnectW8BackendParityReceipt>` (or borrowed reference), not a duplicated verifier run.

Conceptual order:

```text
capture native invocation identity
→ original Headwise/TensorCube candidate
→ existing conditional W8 comparison
→ preserve original sealed W8 receipt when measured
→ original W9A route decision and candidate retirement
→ construct original sealed W9A layer receipt
→ validate/build same-call join BEFORE audit commit
→ record original W9A and optional join atomically or under one scoped transaction
→ return unchanged canonical output/route
```

Avoid creating a new failure *after* canonical token publication because an optional audit write failed. `QUALIFY_REQUIRED` may fail closed **before** committing a selected layer if join authority is missing; `OBSERVE` must preserve the original W9A decision and separately report audit failure/unavailability. No silent successful audit receipt.

## 11. Explicit runtime admission modes

Suggested qualification-only mode (reuse existing project mode types where possible):

```rust
enum HeadwiseR3Cf2JoinMode {
    Disabled,
    Observe,
    RequireMeasuredJoin,
}
```

- `Disabled` (default): original W9A canary/audit policy and output exactly preserved; no extra comparator.
- `Observe`: original W8 sampled comparison reused; join and audit result recorded; W9A route authority stays unchanged.
- `RequireMeasuredJoin`: selected sampled route requires exact valid joined receipt before qualification. This is **not** automatic W9A production default or AOF promotion.

Unsupported source/lineage or Device/Queue identity yields explicit HOLD. No implicit fallback to `NotMeasured` when measured evidence was required.

## 12. Checkpoint lineage: source change cannot be concealed

`shared_lm_training_source_digest()` includes `native_wgpu.rs` and `Cargo.lock`; source byte drift in either changes the training source identity. The parent 19-input digest is:

```text
e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283
```

**Path A: old checkpoint remains valid** only if an exact callsite join is implemented **without modifying any of those 19 byte inputs**, and this is proven by recomputing each byte digest. The inspected source does not yet establish such a verified seam; this is a conditional possibility, not an available implementation.

**Path B: explicit new lineage (expected if `native_wgpu.rs` is edited)**:

1. Declare a deliberate training source-digest change; record all 19 exact before/after SHA256 values and the first changed input.
2. Keep the parent checkpoint + manifest immutable. Do not edit its `training.source_digest`, disable its validator, or whitelist the new digest as equivalent without proof.
3. Create or qualify a new head checkpoint under the new **real** source lineage, using an authorized training/migration route and new manifest. Reusing old weights under a new digest requires its own equivalence and provenance authority, not a JSON reseal.
4. Verify real model/tokenizer/dataset/head rank lineage, checkpoint content digest, evaluator compatibility and actual native loading.
5. Keep the old source/checkpoint executable as a separately labeled reference arm for A/B; never mix old and new receipts in the same authority chain.

If legitimate Path B is not complete, `HOLD_HEADWISE_R3_CF2_HEAD_CHECKPOINT_NEW_LINEAGE_REQUIRED`. Do not postpone the digest problem until after a GPU run and then silently downgrade the gate.

## 13. Minimal source touch points

**Likely required (meaning-changing):**

- `crates/model_core/src/native_wgpu.rs`: narrow same-branch capture and original W8/W9A joined recording. **Checkpoint-hashed input; triggers Path B unless exact non-edit seam proven.**

**Supporting modules (new modules preferred):**

- `crates/model_core/src/headwise_r3_cf1_w8_join_evidence.rs`: retain original standalone receipt validation, extend with a strictly separate same-call join builder; do not convert its current `report_w8_w9a_unjoined()` into a generic post-hoc “join by strings”.
- `crates/model_core/src/headwise_r3_w9a_parity_evidence.rs`: evidence classification and measured/unmeasured aggregates.
- `crates/model_core/src/attention_decode_w9a_production_runtime.rs`: bounded session/local join audit store and terminal compaction, without changing legacy route gate semantics.
- `crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs`: only if a genuine Queue completion callback is required; no new compare dispatch or relaxed threshold.
- `crates/model_core/src/aof_r1_admission.rs`: runtime source-digest binding for new helper/shader bytes; **do not** fake or exclude training lineage.
- `tools/validate_ash_headwise_r3_cf2_w8_w9a_native_join_static.py`: exact source/lineage/negative gate.

Avoid adding a second Rust W9A route receipt schema merely to smuggle proof into legacy `context_parity_pass`. Prefer a new separately sealed joined receipt referencing the original layer receipt SHA.

## 14. Receipt schema (required)

File/audit concept:

```text
headwise_r3_cf2_w8_w9a_same_invocation_join_receipt.json
schema = ash.headwise.r3.cf2.native_w8_w9a_join.v1
```

Required fields:

```text
source_tree_sha256
runtime_binary_sha256
Cargo.lock_sha256
head_training_source_digest_parent
head_training_source_digest_current
head_checkpoint_lineage_mode
head_checkpoint_digest
head_manifest_digest
model_digest / tokenizer_digest
model_instance_epoch
session_id / session_epoch
decode_step / layer_index
attention_invocation_generation / candidate_nonce
candidate_invocation_digest
W8 original receipt_sha256 / pipeline_identity_digest
W9A original layer receipt_sha256
W8 actual numerical pass / finite / mismatch count / first mismatch
W8 map callback / GPU status / queue callback distinct witnesses
W9A legacy route gate result / original selected route
sampling state + fault-injection classification
join identity exact / layer duplication count
owner completion / retirement state
not_measured / measurement_unavailable / measured_pass / measured_fail
first_failure_code
source / static / compile / runtime / physical states
pass_token (nullable)
receipt_sha256
```

Receipt must carry explicitly `UNKNOWN`/`None` for unavailable physical values. Literal zero is not a substitute for unobserved counters.

## 15. Required negative matrix

At minimum reject or classify distinctly:

| Negative | Required disposition |
|---|---|
| W8 belongs to earlier `decode_step` | STALE_JOIN_FAIL |
| W8 candidate from other model/session/epoch | CROSS_OWNER_FAIL |
| Same step but wrong layer | LAYER_IDENTITY_FAIL |
| Same layer but next invocation generation / nonce | CROSS_INVOCATION_FAIL |
| Valid W8 receipt SHA but W9A SHA mismatch | RECEIPT_BINDING_FAIL |
| Correct strings, different candidate invocation digest | CANDIDATE_IDENTITY_FAIL |
| Same candidate, wrong Device/Queue generation | DEVICE_QUEUE_FAIL |
| Duplicate join record | DUPLICATE_JOIN_FAIL |
| Unsampled TensorCube/Headwise receipt with legacy `context_parity_pass=true` | NOT_MEASURED, never MeasuredPass |
| Sampled W8 complete but numerical mismatch | MeasuredFail; original rollback unchanged |
| Sample requested but W8 callback/comparison fails | MeasurementUnavailable/error; no invented zero |
| Valid W8 PASS plus injected W9A context mismatch | W8 MeasuredPass + W9A route rejection recorded separately |
| W8 map observed but claimed Queue callback absent | PHYSICAL_COMPLETION_HOLD |
| New `native_wgpu.rs` + old checkpoint digest | LINEAGE_HOLD |
| W8 original comparator executed twice to obtain a join | DUPLICATE_DISPATCH_FAIL |
| Audit write/receipt failure after token already committed | POSTCOMMIT_SEMANTIC_DRIFT_FAIL |
| Cross-leg A/B/C prior disk receipt as live authority | CROSS_LEG_IDENTITY_FAIL |

Preserve the first failure and the exact source stage. Do not collapse numerical mismatch and missing completion into one generic error.

## 16. SOURCE/STATIC gates

The static validator SHALL check:

```text
1 canonical W8 sampled comparison call retained
original W8 receipt is preserved through the same native branch
joined receipt consumes original sealed W8 and W9A references
candidate invocation digest, step, layer, generation, nonce checked
Device/Queue currentness checked
legacy context_parity_pass route policy unchanged
unsampled fields cannot be MeasuredPass
fault-injected route rejection distinct from numerical result
original receipt SHA and pipeline identity digest validated
no fallback using disk/timestamp/TLS/global unscoped registry
no extra W8 comparison / full context readback
queue callback evidence distinct from map/status evidence
bounded join ledger + exactly-once retire/compaction present
checkpoint 19-input source differences calculated honestly
no training digest bypass, forged migration or hidden source exclusion
R3-CF1 selected-output fixture still explicitly HOLD
no CF5-D ACTIVE / production performance PASS
```

Static PASS must be labeled `SOURCE/STATIC` only; this is not native comparator execution.

## 17. Compile and native execution gates

Run only after exact workspace dependency input is restored (the code-only parent lacks the external `vendor/sherpa-rs-main/crates/sherpa-rs` path). No dummy package or dependency-version substitution.

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo test -p model_core --lib headwise_r3_cf2 --release --locked -j 1
cargo test -p burn_webgpu_backend --lib attention_interconnect_w8 --release --locked -j 1
```

Use exact test names discovered from `Cargo.toml`/test discovery. The above filters are **proposed**, not confirmed available tests. Compile the actual W9A native route; diagnostic-only compilation is insufficient.

Run native Naga only for WGSL paths changed by this revision (or the established full Naga suite as a regression), and report it separately from Rust compilation.

## 18. Real WGPU physical matrix

Use real same-source Device/Queue, model/checkpoint/tokenizer, with fresh session and bounded output roots. Required route cases:

1. `HeadwiseDefault` with no W8 comparator: `NotMeasured`.
2. `TensorCubeActualCanary`, unsampled: `NotMeasured`, old route policy preserved.
3. `TensorCubeSampledAudit` with W8 PASS: `MeasuredPass`, exact same-call W8/W9A digest join.
4. Sampled W8 mismatch: `MeasuredFail`, original rollback/quarantine path.
5. W8 numerical PASS + fault-injection reject: W8 measured PASS, effective W9A route rejected; no conflation.
6. W8 comparator failure before valid receipt: `MeasurementUnavailable` or explicit terminal failure, no invented joined record.
7. Cross-session, stale step, duplicate layer, wrong invocation nonce, wrong queue, swapped SHA inputs: fail closed.
8. Repeated fresh sessions and selected eligible layers to prove join uniqueness, terminal retirement and no cross-case reuse.

Use the same physical W8 comparator and W9A layer route call; do not substitute a standalone fixture generated afterward. Check `full_context_readback_count=0`, and no per-token comparator added in default unsampled mode. The W8 sampled path's existing `PollType::Wait` must be reported as a real host wait; there is no structural evidence of zero-wait operation.

## 19. Performance and meaning-change accounting

CF2 is **not** a speedup revision.

- New join/serialization and optional sampled-path Queue callback have measurable costs; record CPU wall, callback wait, allocation/bytes and compact status D2H separately.
- Do not claim no new CPU wait unless physically observed; do not introduce extra default per-token polling or readback.
- Preserve `LegacyTextDensityAdjusted` and `LegacyFullStaged` defaults, existing W9A admission and rollback, token/KV/stop/emit, no new FuturePool promotion.
- An observed W8 comparator mismatch is a numerical fact; a candidate rollback is a routing fact; selected-output fixture parity is a separate independent fact.
- A source-digest change is a **checkpoint lineage change**, not just diagnostic metadata.

## 20. Failure classes

```text
FAIL_HEADWISE_R3_CF2_W8_RECEIPT_INVALID
FAIL_HEADWISE_R3_CF2_W9A_RECEIPT_INVALID
FAIL_HEADWISE_R3_CF2_SAME_INVOCATION_UNPROVEN
FAIL_HEADWISE_R3_CF2_CANDIDATE_DIGEST_DRIFT
FAIL_HEADWISE_R3_CF2_CROSS_SESSION_OR_LAYER
FAIL_HEADWISE_R3_CF2_ATTENTION_GENERATION_DRIFT
FAIL_HEADWISE_R3_CF2_QUEUE_IDENTITY_DRIFT
FAIL_HEADWISE_R3_CF2_DUPLICATE_JOIN
FAIL_HEADWISE_R3_CF2_SAMPLED_W8_MISSING
FAIL_HEADWISE_R3_CF2_UNSAMPLED_FAKE_MEASURED
FAIL_HEADWISE_R3_CF2_ROUTE_NUMERIC_CONFLATION
FAIL_HEADWISE_R3_CF2_CALLBACK_SOURCE_MISLABEL
FAIL_HEADWISE_R3_CF2_UNBOUNDED_JOIN_LEDGER
FAIL_HEADWISE_R3_CF2_CHECKPOINT_LINEAGE_DRIFT
HOLD_HEADWISE_R3_CF2_HEAD_CHECKPOINT_NEW_LINEAGE_REQUIRED
HOLD_HEADWISE_R3_CF2_PHYSICAL_COMPARATOR_NOT_RUN
HOLD_HEADWISE_R3_CF2_SELECTED_OUTPUT_REFERENCE_NOT_QUALIFIED
```

## 21. Independent terminal PASS boundaries

Do not issue a single undifferentiated PASS for three different claims.

```text
SOURCE_JOIN_IMPLEMENTED
  - typed same-call join exists, source/static/compile gates pass

PHYSICAL_JOIN_QUALIFIED
  - real sampled W8/W9A same-call join + completion + retirement
    with a legitimately admitted checkpoint lineage

SELECTED_OUTPUT_QUALIFIED
  - independent CF1 selected production output + canonical reference
    and matched-numeric GPU parity physically established
```

A narrow CF2 physical join receipt may emit:

```text
PASS_HEADWISE_R3_CF2_W8_W9A_SAME_INVOCATION_PHYSICAL_JOIN
```

only when SOURCE/STATIC/COMPILE, correct checkpoint lineage, actual same-call physical comparison, identity, numerical provenance, bounded resource retirement and applicable negative matrix all pass. This token **does not** mean selected production output qualified.

`PASS_HEADWISE_R3_CF1_SELECTED_OUTPUT_W8_W9A_CLOSURE` remains gated on the **independent** CF1 selected-output canonical-reference provenance and physical result; do not issue it merely because the CF2 join passes. `CF5-D ACTIVE` remains forbidden.

## 22. Next development handoff

1. Implement typed same-invocation W8 result retention + W9A joined audit in the natural native branch; keep default route behavior.
2. Immediately resolve the `native_wgpu.rs` byte-change consequence: either prove a truly digest-preserving seam, or create the explicit new head checkpoint lineage authority. No partial compile result may override this.
3. Run exact release compilation and existing sampled W8 actual GPU comparator, session/step/layer negative matrix, real completion/retirement and source-bound receipt aggregation.
4. Independently complete the CF1 selected-output *canonical reference provenance*, then return to Headwise/TensorCube capacity-strided consumer parity before CF5-D.

---

## Final invariant

```text
ORIGINAL W8 COMPARATOR RECEIPT
+
ORIGINAL W9A LAYER RECEIPT
+
SAME NATIVE INVOCATION / OWNER / GENERATION / DEVICE / QUEUE
+
MEASURED RESULT DISTINCT FROM ROUTING GATE
+
PHYSICAL COMPARATOR COMPLETION AND RESOURCE RETIREMENT
+
VALID HEAD CHECKPOINT SOURCE LINEAGE
=
W8/W9A SAME-INVOCATION PHYSICAL JOIN QUALIFIED

NOT YET = SELECTED HEADWISE PRODUCTION OUTPUT QUALIFIED
NOT YET = CF5-D ACTIVE
NOT YET = PERFORMANCE PROMOTION
```

**Source-bake status supersession:** CF2 source has been packaged and STATIC-checked, but NO Rust compile, native WGPU same-invocation physical join, new head checkpoint admission, selected-production-output qualification or performance measurement has been completed.

---

## 24. Exact source-bake evidence annex, 2026-10-09

This annex documents code-only SOURCE modifications and honest evidence status. The original FULL PHYSICAL acceptance contract in sections 0–23 remains binding. **No full CF2 PASS token has been emitted.**

# HEADWISE-R3-CF2 W8/W9A SAME-INVOCATION JOIN + CHECKPOINT LINEAGE

**SOURCE bake report, 2026-10-09.** This records source/STATIC tests, **not** Rust COMPILE or actual WGPU PHYSICAL execution.

## 1. Exact parent and output

| Artifact | SHA-256 |
|---|---|
| Parent (8,747 files) | `f335e0f9a6b7df4d16cc8ce66c8f6b3098172095203fbc7ba4ecf4cd75c0cb5b` |
| Full code-only (8,749 files) | `bffd52091a9e5cace4a34009ab427413fb36d87517131aad6354ef1746b01f3c` |
| Overlay (6 files) | `b6ca0141eb8d49f2f1f791c268e88170b59410e206152c34ca19ba1c92c39e41` |

- Full ZIP: `ASH_PASS3_HEADWISE_R3_CF2_W8_W9A_SAME_INVOCATION_JOIN_CHECKPOINT_LINEAGE_CODE_ONLY.zip`
- Overlay ZIP: `ASH_HEADWISE_R3_CF2_W8_W9A_SAME_INVOCATION_JOIN_CHECKPOINT_LINEAGE_OVERLAY_CODE_ONLY.zip`
- Delta **ADD 2 / MOD 4 / DEL 0**; archive CRC and extracted byte identity PASS; 8,743 parent entries byte-identical.

### Added source

- `crates/model_core/src/headwise_r3_cf2_native_join.rs`: exact typed same-call W8/W9A receipt builder, identity/geometry/receipt hash validation, numerical W8 evidence distinct from W9A routing, explicit callback provenance, bounded audit summary, 8 source-only Rust unit tests (not executed).
- `tools/validate_ash_headwise_r3_cf2_same_invocation_static.py`: static/negative gates and 19-input training digest evaluation. It is **not** a native Rust runtime dependency.

### Modified source

- `crates/model_core/src/native_wgpu.rs`: retain **original** W8 sampled comparator receipt in the same native stack, pair it with the sealed TensorCube/rollback W9A layer receipt; default Disabled; opt-in Observe with explicit source training digest check; RequireMeasuredJoin returns lineage HOLD; no additional W8 call, no change to W9A compatibility gate and no full context readback. Separate audit errors preserve original route selection. Public bounded audit summary and drain method.
- `crates/model_core/src/attention_decode_w9a_production_runtime.rs`: 128-record bounded session-local `VecDeque`, exact duplicate key check, failure count, first-failure attribution, step-local drain and evidence summary.
- `crates/model_core/src/attention_decode_w9a_model_registry.rs`: module registration/export.
- `crates/model_core/src/aof_r1_admission.rs`: new join helper included in runtime source-digest SSOT.

### Evidence semantics

- Original W8: receipt hash/pipeline hash, candidate invocation digest, GPU result words, shape, error count and first mismatch validated/bound. No re-dispatch.
- Original W9A: sealed `receipt_digest`, current `session_id/epoch`, `decode_step`, `layer_index`, physical `seq_kv`, actual route and existing `context_parity_pass` preserved.
- `NotMeasured` for unsampled; `MeasuredPass`/`MeasuredFail` from *W8 receipt's checked GPU result*, not W9A boolean; `MeasurementUnavailable` when a sampled route has no valid completed comparator.
- W8 compact GPU status/readback recorded separately from Queue completion callback. **No distinct Queue callback existed at this W8 site**, so `w8_queue_completion_callback_observed=None`. Never true by inference from map/status.
- CF2 join records carry `checkpoint_lineage_qualified=false`, `physical_join_qualified=false`. Audit summary also forbids pass and selected-production qualification. This SOURCE code is not a physical promotion.

## 2. Checkpoint lineage: intentional breaking source change

**Explicit meaning change:** `native_wgpu.rs` is in the existing **19-input** `shared_lm_training_source_digest()` domain. CF2 changes its bytes. The old checkpoint is not automatically compatible with the new source.

| Checkpoint training source authority | SHA-256 |
|---|---|
| Parent 19-input digest | `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283` |
| Current 19-input digest | `0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094` |

Only the `native_wgpu.rs` entry changed; 18/19 inputs including `Cargo.lock` are identical. No old head checkpoint/manifest has been modified, re-sealed, transplanted or admitted as compatible.

**HOLD_HEADWISE_R3_CF2_HEAD_CHECKPOINT_NEW_LINEAGE_REQUIRED.** An actual new checkpoint or explicitly qualified migration plus model/tokenizer/dataset/rank/provenance loading evidence is required. The opt-in Observe API only checks a supplied source-digest string; that string alone is *not* checkpoint authenticity. No CLI campaign claims a new physical checkpoint.

## 3. Verification performed

| Layer | Result |
|---|---|
| New CF2 SOURCE/STATIC | **41/41 PASS** |
| CF2 negative source perturbations | **26/26 rejected** |
| Parent ZIP CRC/byte match | **PASS** |
| Current full/overlay CRC & exact byte match | **PASS** |
| Rust COMPILE | **NOT_RUN** (cargo/rustc unavailable) |
| Rust CPU unit tests | **NOT_RUN** |
| Native Naga | **NOT_RUN** (no modified WGSL in CF2) |
| Native WGPU physical join/completion | **NOT_RUN** |
| Real new checkpoint/migration | **NOT_CREATED / HOLD** |
| Performance | **NOT_MEASURED** |

**Parent static truth:** Legacy source-byte/digest gates fail because this revision intentionally modifies `native_wgpu.rs`. They have not been changed, suppressed or called PASS:

- `validate_ash_headwise_r1_score_policy_static.py`: exit `1`; HEADWISE-R1 STATIC 37 / 38 FAIL ['no_training_source_edit']
- `validate_ash_headwise_r2_chunked_causal_static.py`: exit `1`; HEADWISE-R2 STATIC 21 / 22 FAIL ['training_primitive_byte_unchanged']
- `validate_ash_headwise_r3_subgroup_w9a_evidence_static.py`: exit `1`; HEADWISE-R3 STATIC 33 / 37 FAIL ['pre_dispatch_gate', 'strict_rejects_proxy_only', 'proxy_mismatch_fails_closed', 'training_digest_byte_identical']
- `validate_ash_headwise_r3_cf1_selected_output_w8_w9a_static.py`: exit `1`; HEADWISE-R3-CF1 SOURCE/STATIC 41 / 42 FAIL ['checkpoint_digest_unchanged']
- `validate_ash_aof_r1_cf5_c_r3_selected_route_static.py`: exit `1`; R3 STATIC 59/60 FAIL ['checkpoint_training_19_source_exact'] TRAINING_SOURCE_DIGEST 0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094 INPUTS 19
- `validate_ash_aof_r1_cf5_c_r2_verifier_scope_static.py`: exit `1`; CF5-C-R2 STATIC FAIL: ['training_hash_preserved'] TRAINING_SOURCE_DIGEST=0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094 COUNT=19
- `validate_ash_aof_r1_cf5_c_r1_native_consumer_handoff_static.py`: exit `1`; PASS single_session_parked_slot PASS session_parked_initialized PASS session_parked_borrow_method PASS move_from_terminal_pending PASS terminal_pending_not_reused PASS park_requires_not_finished PASS park_storage_transaction PASS no_new_can
- `validate_ash_aof_r1_cf5_c_capacity_strided_consumer_static.py`: exit `1`; PASS cf5_c_model_module_registered PASS cf5_c_backend_module_registered PASS borrow_scoped_view PASS view_not_fabricated_burn_tensor PASS view_explicit_visible PASS view_published_limit PASS view_canonical_generation PASS view_layer_generat
- `validate_ash_aof_r1_cf5_block_prefix_commit_static.py`: exit `1`; {   "schema": "ash.aof_r1.cf5.block_prefix_commit_kv_capacity.source_static.v1",   "status": "FAIL",   "checks": 73,   "passed": 72,   "failed": [     "training_checkpoint_digest_byte_preserved"   ],   "implemented": "A_B_OBSERVE_ONLY",   "
- `validate_ash_aof_r1_cf4_prefix_commit_transfer_static.py`: exit `1`; {   "schema": "ash.aof_r1.cf4.prefix_commit_transfer.source_static.v1",   "status": "FAIL",   "checks": 65,   "passed": 64,   "failed": [     "training_source_digest_exact_parent"   ],   "parent_old_byte_invariant": "SUPERSEDED_EXPLICITLY_O
- `validate_ash_aof_r1_cf3_quality_evaluator_compaction_static.py`: exit `1`; {   "schema": "ash.aof_r1.cf3.quality_evaluator_compute_compaction.source_static.v1",   "status": "FAIL",   "checks": 51,   "passed": 50,   "failed": [     "checkpoint_training_source_byte_preserved:crates/model_core/src/native_wgpu.rs"   ]


The HEADWISE-R3 historical proxy/strict signature gates were already superseded by CF1, independent of the new CF2 training digest failure. Current CF2 source/static passing **cannot supersede physical admission**.

## 4. Failure/negative conditions

The new validator rejects loss of W8/W9A receipt SHA, candidate digest, session/layer/nonce/generation, runtime Device/Queue binding, numeric raw-status comparison, independent callback evidence, original W8 result retention, bounded ledger/duplicate rejection, source digest binding, artificial `MeasuredPass`, modified legacy route gate and forged physical/checkpoint PASS. These are source mutations, not GPU executions.

## 5. Windows native qualification commands (NOT EXECUTED)

```powershell
python .\tools\validate_ash_headwise_r3_cf2_same_invocation_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo test -p model_core --lib headwise_r3_cf2 --release --locked -j 1
```

The exact external `vendor/sherpa-rs-main/crates/sherpa-rs` workspace path dependency must be restored on the native machine before Cargo metadata; never fabricate a stub. Then run real sampled/un-sampled W9A and force mismatch cases with legitimate newly qualified head checkpoint lineage, same bound Device/Queue, selected layer receipt/currentness, original W8 receipt and explicit GPU/map/retirement evidence. Test stale step, wrong candidate, duplicate append, session swap and callback-source separation.

**No physical or checkpoint-lineage PASS token issued.** Parent CF1 selected-output reference producer remains independently HOLD, as do CF5-D ACTIVE and performance promotion.

### Additional exact in-flight policy-generation fence

`configure_headwise_r3_cf2_join_mode()` increments an explicit `cf2_join_policy_generation` with checked overflow. The natural selected W9A attention invocation captures that policy generation, and receipt publication rejects a mismatch against the current runtime with `FAIL_HEADWISE_R3_CF2_JOIN_POLICY_CHANGED_IN_FLIGHT`. The strengthened static validator checks this fence, with two specific negative mutations removing the guard or its generation increment. Those checks are included in the final **41/41** and **26/26** results. This is SOURCE evidence, not proof of real concurrent WGPU behavior.
