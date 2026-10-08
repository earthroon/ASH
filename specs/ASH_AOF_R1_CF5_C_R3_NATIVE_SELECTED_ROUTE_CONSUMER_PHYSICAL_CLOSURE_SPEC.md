# AOF-R1-CF5-C-R3

## NATIVE SELECTED-ROUTE CONSUMER BINDING + PHYSICAL QUALIFICATION CLOSURE

**Patch ID:** `AOF-R1-CF5-C-R3`  
**Parent:** `AOF-R1-CF5-C-R2`  
**Successor:** `AOF-R1-CF5-D` only after actual whole-consumer PHYSICAL qualification  
**Class:** Selected-route native observation, WGPU context parity, owner and checkpoint lineage closure  
**Status (2026-10-09): PARTIAL SOURCE BAKE, STATIC PASS / COMPILE NOT_RUN / NAGA NOT_RUN / GPU PHYSICAL NOT_RUN / FULL R3 HOLD.** R3-A Jacobi/Linear scoped OBSERVE and selected native route-evidence inventory added; Headwise/TensorCube native capacity-strided parity and full-route admission remain unimplemented. See source bake annex.

**Exact parent ZIP:** `ASH_PASS3_AOF_R1_CF5_C_R2_VERIFIER_NATIVE_SEAM_CHECKPOINT_LINEAGE_QUALIFICATION_CODE_ONLY.zip`  
**Parent SHA-256:** `461e7509db39278bf1a1d05f7673d0fda8a0a3d17abdca63b84ca77b0d8038cb`  
**Parent files:** 8,734

```text
AOF-R1-CF5-C-R3

+ CF5-A/B/C / R1 / R2 SOURCE SEMANTICS PRESERVATION
+ EXACT PARENT CARGO / NAGA / NATIVE TREE REQUALIFICATION
+ REAL LINEAR JACOBI BACKEND ATTENTION SCOPE
+ REAL HEADWISE INCREMENTAL SELECTED CONSUMER
+ REAL HEADWISE CHUNKED SELECTED CONSUMER
+ REAL TENSORCUBE ACTUAL INCREMENTAL CONSUMER
+ NO HEADWISE / TENSORCUBE AS BURN FALLBACK
+ NO SYNTHETIC TENSORCUBE CHUNKED ROUTE
+ GPU-NATIVE CONTEXT BITWISE / FIRST-MISMATCH OBSERVATION
+ FULL K/V VISIBLE-TAIL + PHYSICAL-STRIDE CURRENTNESS
+ ROUTE-LOCAL SESSION / GENERATION / OWNER BINDING
+ D1 / D2 / D4 FRESH PHYSICAL COVERAGE MATRIX
+ REAL COMPLETION / RETIREMENT AND NEGATIVE MATRIX
+ R2 RECEIPT TRUTH REPAIR WITHOUT FABRICATED PASS
+ TRAINING CHECKPOINT SOURCE DIGEST PRESERVATION
+ NO CANONICAL KV PUBLICATION OR TOKEN RESULT CHANGE
+ NO FULL QKV HOST READBACK OR HIDDEN MATERIALIZATION
+ NO CF5-D ACTIVE OR FUSED PRODUCTION PROMOTION
```

---

## 0. Evidence baseline and stop law

R2 code contains a backend verifier Tree OBSERVE hook and a 16-byte GPU comparison status path, but its supplied receipt records **COMPILE, Naga, RUNTIME and PHYSICAL as NOT_RUN**. This is not yet a GPU-qualified Tree baseline.

| Evidence layer | Parent status |
|---|---|
| R2 SOURCE/STATIC | 44/44 PASS; 12/12 negative-source perturbations rejected |
| R1 SOURCE/STATIC | 66/66 PASS |
| CF5-C SOURCE/STATIC | 62/62 PASS |
| CF5-A/B, CF4, CF3 STATIC | preserved per parent report |
| Older CF1/CF2/VH6 byte-only gate | 51/52, one CF4 superseded `aof_r1_prefix_commit.rs` byte assertion |
| Training checkpoint 19-input digest | `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283` |
| Rust compile / native Naga | NOT_RUN |
| Tree or Linear actual GPU proof | NOT_RUN |
| Whole CF5-C / CF5-D ACTIVE | HOLD / FORBIDDEN |

Do not silently convert the older 51/52 into a PASS. Preserve the exact supersession attribution while keeping the remaining gates effective.

## 1. Exact SOURCE owners

| Source file | Required authority |
|---|---|
| `crates/model_core/src/aof_r1_runtime.rs` | Session parked backing and current completed FuturePool Tree scope |
| `crates/model_core/src/aof_r1_lookahead.rs` | Natural `ArkLookahead::prepare()` → `aof_r1_jacobi_choices()` call |
| `crates/model_core/src/aof_r1_verification.rs` | Private `aof_forward(..., true/false)`; unchanged if preserving checkpoint digest |
| `crates/burn_webgpu_backend/src/aof_r1_verification.rs` | Real canonical `attention()` with Q, K, V, prefix K/V, output and linear flag |
| `crates/burn_webgpu_backend/src/aof_r1_cf5_c_r2_verifier_observe.rs` | Existing scoped backend observer and Tree/Linear shader candidates |
| `crates/model_core/src/decode_state.rs` | Actual ordinary/chunked QKV, selected route, canonical context |
| `crates/model_core/src/headwise_incremental_full_activation.rs` | `HeadwiseCommitted`, `TensorCubeActualCommitted`, `BurnFallbackRequired` |
| `crates/model_core/src/headwise_chunked_decode_activation.rs` | `HeadwiseCommitted` / `BurnFallbackRequired` |
| `crates/model_core/src/attention_runtime_shape_authority.rs` | `HeadwiseCausalPositionSnapshot` |
| `crates/model_core/src/aof_r1_kv_consumer_bridge.rs` | Existing Burn/Verifier read-only consumer candidates |
| `crates/burn_webgpu_backend/src/aof_r1_kv_capacity_consumer.rs` | Physical capacity-strided native WGPU kernel ABI |
| `crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs` | Physical case and route receipt aggregation |
| `crates/model_core/src/aof_r1_admission.rs` | Runtime source digest |
| `crates/model_core/src/aof_r1_shared_lm_head_math.rs` | 19-file training source digest SSOT |

## 2. R3-P0: native compile + shader + Tree physical control

This phase MUST precede any full R3 physical approval.

1. Resolve the existing exact `vendor/sherpa-rs-main/crates/sherpa-rs` workspace path dependency. Do not create a dummy crate, change the dependency version, delete the workspace member or silently fall back.
2. Run real `cargo metadata --locked`, backend/model_core/orchestrator native release checks and the exact native binaries used by the campaign.
3. Run Naga parsing and WGPU shader/pipeline validation for the Tree/Linear, incremental, chunked and bitwise-compare WGSL actually invoked.
4. Exercise the **already written R2 Tree scope** using a real model, a completed session-parked prefix, a real FuturePool Tree, actual same-Queue completion and full expected layer cardinality.
5. Exercise scope conflicts, wrong Tree identity, generation mismatch, dropped/failed completion, device loss and stale reentry. The `Mutex<Option<...>>` ownership and trait requirements are not proven by source inspection.
6. Seal original source digest, Cargo.lock digest, binary SHA-256, GPU/Queue physical binding and actual receipt lineage.

If Tree fails during compile/physical qualification, repair the exact failure locally and hold any claim that the R3 route matrix is qualified. No CPU simulation or static shader inclusion substitutes for native execution.

## 3. R3-A: natural Linear/Jacobi verifier

**CONFIRMED / SOURCE:** `ArkLookahead::prepare()` naturally calls `model.aof_r1_jacobi_choices()` within an iteration loop, and that method enters `aof_forward(..., true)`. Standalone qualification also has real Linear invocation sites. R2's currently installed Tree scope explicitly sets `linear_oracle:false`; it cannot qualify those Linear paths.

R3 SHALL install a new **per-selected-iteration** scope surrounding the natural Linear/Jacobi call, ideally at the `ArkLookahead::prepare()` / `aof_r1_jacobi_choices()` boundary. The exact current `self.gpu.tree()?`, width, iteration ordinal, current source/session/proposal identity, and parked backing must be bound together.

Required before scope:

```text
same ArkVerificationDevice instance that actually receives attention()
same native Device and Queue instance and physical binding
same model/checkpoint/tokenizer and request/session epoch
same canonical KV visible length/content generation
parked origin proposal round immutable
consumer proposal round current
same actual Jacobi tree buffer and iteration
exact linear flag = true
```

A lookahead-owned shader/program object with merely the same schema is not interchangeable with the actual receiver. If the owner instances differ, record `FAIL_CF5_C_R3_WRONG_VERIFIER_INSTANCE` and HOLD. Every Jacobi iteration can have new tree content even when the WGPU buffer handle stays stable; record iteration identity and window epoch, not just buffer pointer. No global/TLS observer permission and no copied `aof_forward()` surrogate.

Distinguish `QUALIFICATION_FIXTURE_LINEAR` from `SAME_SESSION_PARKED_LINEAR`: an OFF-mode standalone fixture with independent fresh prefill is not proof of handoff into a current AOF production session.

Exit is actual `linear_oracle=true` backend invocation, correct per-iteration scope, all-layer GPU completion and route-local numerical status. Any training-digest input change requires an explicit new checkpoint lineage decision, not silent digest rewriting.

## 4. R3-B: actual Headwise incremental selected route

`forward_block_decode()` already receives actual `canonical_qkv_prepared()` outputs, then selects `HeadwiseCommitted`, `TensorCubeActualCommitted` or `BurnFallbackRequired`.

R3-B SHALL observe **only the naturally selected `HeadwiseCommitted`** via an independent read-only capacity-strided candidate. Inputs are the actual canonical Q/new K/new V, the bound parked KV backing, selected `HeadwiseIncrementalLayerOutputAuthorityReceipt`, `HeadwiseCausalPositionSnapshot`, actual stage/position generation, selected output Tensor and Device/Queue. Never reclassify that output as `IncrementalBurn`.

The shadow reader must reproduce the selected Headwise route's real RoPE, scale, causal visibility, grouping and numerical reduction policy. Using Burn `grouped_query_attention()` merely because its input shape matches is not native Headwise parity. The returned selected Headwise context remains canonical and unmodified.

Exit requires a real selected Headwise invocation, valid currentness and head-major stride, real GPU context comparison and completion. If the actual Headwise ABI is not accessible without host materialization, record `HOLD_CF5_C_R3_HEADWISE_NATIVE_ABI_UNAVAILABLE`.

## 5. R3-C: actual Headwise chunked selected route

The current chunked enum has `HeadwiseCommitted` and `BurnFallbackRequired`; no `TensorCubeActualCommitted` branch is established in this exact source.

Observe selected `HeadwiseCommitted` using the actual `DecodeStepSpan`, `HeadwiseCausalPositionSnapshot`, selected chunk output authority, per-query native visibility, stage generation and completed parked backing. The R1 **Burn-full-stage** assumption is **not** transferred to Headwise.

Never infer chunk causal masking from a generic formula. Derive the visibility from the selected native route; absent authority is HOLD. The candidate may not commit KV or modify the existing chunk transaction. Preserve EOS, cancel, emit failure and already published canonical state.

## 6. R3-D: actual TensorCube incremental selected route

Only the natural `HeadwiseIncrementalExecutionOutcome::TensorCubeActualCommitted` is eligible, with its `w9a_receipt`, `headwise_authority` and actual selected output. Record W9A receipt digest, layout, matching Q/K/V, current KV generation, model/session owner, same Queue, capacity/visible contract, GPU numerical comparison and physical completion.

Do not fabricate a TensorCube chunked branch or use Burn/Headwise results as evidence of TensorCube success. If the TensorCube selected storage representation cannot be borrowed as a valid raw device lease without extra CPU materialization, explicitly HOLD rather than converting to host or making up an ABI.

## 7. Typed route status and exact selection

Proposed new types, not existing source:

```rust
enum ArkCf5SelectedNativeRoute {
    VerifierTree,
    VerifierLinearJacobi,
    IncrementalBurn,
    IncrementalHeadwise,
    IncrementalTensorCubeActual,
    ChunkedBurn,
    ChunkedHeadwise,
}

enum ArkCf5RouteStatus {
    NotSelected,
    NotApplicable,
    SourceOnly,
    GpuObserved,
    NumericQualified,
    PhysicalQualified,
    Hold { reason: String },
    Failed { reason: String },
}
```

`NotSelected` is NOT a PASS; `NotApplicable` is permitted only with an exact source/feature/policy proof of structural inapplicability. Preserve typed route identity from the actual selected outcome and use `match`/tuple patterns to prevent relabeling between unrelated paths.

---

## 8. Route coverage SSOT

Before running the campaign, freeze a route manifest containing:

```text
runtime source digest
model/checkpoint/tokenizer identity
selected feature and native execution policy
required route kinds
expected layer cardinality
expected head/GQA/dtype and Q/K/V layout
applicable D1/D2/D4 combinations
precise route selection producer/receipt type
per-route numerical comparison policy source
actual session Device/Queue identity
```

Every selected invocation must provide proof of its actual route, layer and owner. Absence of telemetry is `NOT_OBSERVED`, not zero failures. `NOT_APPLICABLE` requires proof that the route is structurally unavailable in the exact selected configuration. Headwise/TensorCube paths must not be silently removed from the manifest just because the current CPU/GPUs did not select them.

## 9. Capacity-backed KV indexing and visibility

For head-major prefix K/V backing with physical capacity `C`, visible committed length `V`, head width `W`:

```text
physical_element_offset = (kv_head * C + token_position) * W + component
readable token_position < V
0 < V <= C
```

The suffix Q/K/V layout is controlled by the actual native producer. Do not construct a full contiguous KV buffer, hidden head-major transpose or duplicated full QKV projection merely to feed OBSERVE.

Enforce physical buffer byte sizes, alignment, WGPU maximum storage binding limits, checked integer arithmetic, GQA head mapping, correct dtype and no input/output alias overlap. Test K and V tail isolation **independently**: if either permits `[V,C)` reads, reject. Never pass capacity `C` to a native attention mask as the logical KV length.

## 10. Numerical comparison authority

The **actually selected** canonical context is always the reference and remains unchanged. The read-only candidate executes on the same native Device/Queue. No full-context, full-QKV, or whole FuturePool-tree D2H is allowed for normal qualification.

Minimum GPU reduction receipt:

```text
expected_elements
compared_elements
canonical_nonfinite_count
candidate_nonfinite_count
raw_u32_mismatch_count
first_mismatch_flat_index
first_mismatch_layer / query / head / component
completed_gpu_submission_identity
comparison_policy_source
```

Only a real completed GPU bitwise comparison with all elements observed, zero mismatches and no nonfinite values supports a bitwise equality claim for **that exact measured route/layer**. For Headwise or TensorCube, differing floating-point reduction order may produce legitimate non-bitwise values. Do not invent or relax a numerical threshold. If existing authoritative tolerance is not identified, classify `HOLD_CF5_C_R3_NUMERICAL_POLICY_UNBOUND`, report observed error sizes and withhold numerical PASS.

The R1 Burn scalar `max(abs(reference-candidate)) == 0` is not raw f32 bitwise equality; no conversion to `BITWISE_PARITY_EXACT` without a real bitwise comparator.

## 11. Scoped submission / lifetime contract

An R3 observer must stay tied to one exact `ArkVerificationDevice` or selected native headwise/TensorCube execution owner. No process-wide or TLS global scope. Pseudostate:

```text
Inactive
→ Acquired(owner, session, route, proposal, tree/step, layer count)
→ CanonicalSubmitted
→ ObserverSubmitted
→ GPUCompletionProven
→ CompactComparisonReadback
→ Retired
→ Inactive
```

At every state use explicit owner digest, source/runtime generation, GPU queue identity and event ordinals. Rust `Drop` of a guard does **not** prove GPU completion. Submitted buffers remain pinned until real same-Queue completion or terminal device-loss retention. Reject parallel scopes on a single exclusive owner, cross-thread/cross-session use, wrong layer sequence, stale completion, double retirement and reuse before completion.

## 12. R2 legacy receipt truth repair

The parent CF5 qualification CLI reads `aof_r1_cf5_c_r2_observations` but the aggregate `cf5_c_consumer_bridge.native_verifier_tree` and `.native_verifier_linear` still contain inherited literal `HOLD_CF5_C_VERIFIER_ENTRY_UNREACHABLE` classifications. In R3, preserve historical receipts as audit history, and derive **new R3 route-local status** from actual observed events:

```text
No matching complete layer events → HOLD_NOT_OBSERVED
Real Tree events, own route, source/owner current → TREE_OBSERVED
Real Linear events, own route, source/owner current → LINEAR_OBSERVED
GPU bitwise/numeric qualifier satisfied → NUMERIC_QUALIFIED
Real same-Queue completion, no lifetime errors → PHYSICAL_QUALIFIED
Nonzero mismatch without qualified tolerance → NUMERICAL_HOLD
Missing expected layer, stale/duplicate/failed completion → FAIL
```

Never transform a literal `0` into 'measured zero'; physical metrics with no observation source must be `None` or `UNKNOWN`. A route-local sample cannot qualify all D1/D2/D4 rows. A Tree record cannot count as Linear even when the WGSL source includes both entrypoints.

## 13. No CF4 cost accounting contamination

Keep separate:

```text
CF4 canonical stage_kv / prefix-copy / submit / completion
CF5-A/B extra OBSERVE stage and comparison
R1 Burn incremental / Burn chunked shadow
R2 Tree verifier scoped shadow
R3 Linear verifier scoped shadow
R3 selected Headwise incremental and chunked shadow
R3 selected TensorCube actual incremental shadow
```

CF5 OBSERVE adds GPU work and may be slower. Do not count that work as reduced canonical copy cost or claim that the canonical per-token copy is gone. **Only CF5-D** is authorized to change physical canonical KV storage, and only after full C qualification.

## 14. Actual physical campaign matrix

Freeze a campaign identity over:

```text
model / tokenizer / trained head checkpoint SHA-256
prompt/evaluation data and generation config
Cargo.lock / runtime source / binary digests
GPU adapter / Device / Queue / runtime authority
sampling policy / EOS / banned tokens
rank A/B and D1/D2/D4
route inventory and selected-route policy digest
CF1, CF2, VH6, CF3, CF4, CF5-A/B, C-R1, C-R2 parent receipts
```

Required actual legs where applicable:

1. D1/D2/D4 Tree verifier with a genuine completed parked backing and matching FuturePool Tree.
2. Linear/Jacobi oracle with the **real current iteration tree**, same verifier instance, and same-session parked backing.
3. Headwise incremental selected route.
4. Headwise chunked selected route.
5. TensorCube actual incremental selected route when that mode is enabled and selectable.
6. Existing Burn incremental/chunked as controls, without reclassifying their output.

Use fresh bounded native session identities for independent legs. Disk JSON receipts are audit-only, not live permits. Required route depth combinations that cannot be selected must be classified `NOT_SELECTED` or source-proven `NOT_APPLICABLE`, never fabricated runtime records. Current `ArkPrefixCursor` supports at most five accepted tokens. Do not invent accepted-prefix length 8.

## 15. Negative and semantic matrix

| Negative / semantic case | Expected result |
|---|---|
| Wrong model/tokenizer/request or session epoch | stale backing rejected |
| Origin round rewritten into successor round | reject source identity drift |
| Wrong device, queue or verifier instance | reject scope/lease |
| Jacobi tree changes between iterations | rebind iteration or reject stale tree |
| Tree observation relabelled Linear | reject |
| Headwise/TensorCube output relabelled Burn | reject |
| Physical `C` used instead of visible `V` | reject hidden tail read |
| K valid but V tail invalid, or reverse | reject independently |
| Skipped, repeated or unordered layer | reject |
| Context comparison count incorrect | reject |
| One-bit error introduced into GPU comparison | real mismatch/first index recorded |
| Failed GPU completion or device loss | no retired/reusable false success |
| Double/late completion for old generation | reject |
| Terminal observer failure | retain canonical history, no fake PASS |
| EOS, StopSequence, MaxNewTokens | preserve existing stop result |
| Cancel before publication | zero new canonical token/KV |
| Cancel after partial publication | prior canonical token/KV retained |
| Emit failure | failed ACK, already-published canonical KV retained |
| Duplicate commit/consume | no duplicate append |
| Stale FuturePool identity | candidate rejected |
| Missing required rank/depth/route | aggregate HOLD |
| Old receipt from another binary/source | lineage mismatch |
| One of 19 training digest inputs changed | old checkpoint admission HOLD |

Negative source mutations prove that a static checker detects a pattern. They are not GPU execution proofs.

---

## 16. Source and checkpoint lineage

The 19 input files in `shared_lm_training_source_digest()` MUST remain byte-identical if the existing trained head checkpoint is consumed. Parent digest:

```text
e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283
```

`aof_r1_verification.rs`, `model_layers.rs` and `native_wgpu.rs` are in that set. Prefer new evaluation/reader modules and non-hashed `aof_r1_runtime.rs`, `aof_r1_lookahead.rs`, `decode_state.rs` boundaries. If source ownership makes a hashed-file change unavoidable, stop and define a distinct checkpoint-lineage migration, including new real training/checkpoint evidence. Do **not** edit old training digest/manifest or weaken source admission.

Update `aof_r1_admission.rs::ark_runtime_source_digest()` with every new/changed OBSERVE module, WGSL byte input and qualifier. The runtime digest must use actual file content, not a path-only recipe. The qualified GPU receipt shall bind that runtime digest and the exact executed binary hash.

## 17. Implementation delta boundaries

Preferred narrow touchpoints (exact revisions may require fewer files):

```text
crates/model_core/src/aof_r1_runtime.rs
crates/model_core/src/aof_r1_lookahead.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/aof_r1_kv_consumer_bridge.rs
crates/model_core/src/aof_r1_admission.rs
crates/burn_webgpu_backend/src/aof_r1_cf5_c_r2_verifier_observe.rs
crates/burn_webgpu_backend/src/aof_r1_kv_capacity_consumer.rs
crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs
```

New modules, if required:

```text
crates/model_core/src/aof_r1_cf5_c_r3_selected_route_observe.rs
crates/burn_webgpu_backend/src/aof_r1_cf5_c_r3_route_compare.rs
crates/burn_webgpu_backend/src/shaders/aof_r1_cf5_c_r3_*.wgsl
tools/validate_ash_aof_r1_cf5_c_r3_selected_route_static.py
```

Those new path names are **proposals**, not preexisting files. Add them only when the relevant native source path can be reached without changing unrelated attention/training code. No `_patch` filenames, no changes to checkpoint training math, FuturePool proposal rules, prefix commit storage or packed production promotion.

## 18. Terminal receipt schema

Proposed file:

```text
aof_r1_cf5_c_r3_native_selected_route_physical_qualification_receipt.json
schema = ash.aof_r1.cf5.c.r3.native_selected_route_qualification.v1
```

Per route/layer case:

```text
source tree and runtime binary SHA256
model, tokenizer, head checkpoint and manifest SHA256
session, owner, source/runtime/position generations
origin / consumer proposal round (not conflated)
selected native route and authority receipt digest
Q/K/V native producer and selected canonical output identity
Tree/Linear type and actual tree identity, or selected step/chunk identity
Jacobi iteration/width when present
expected/observed layer ordinal and count
KV C, V, head width, dtype and visibility source
submission / completion / retirement event identifiers
comparison size, bitwise mismatch, first mismatch, nonfinite
optional authoritative tolerance and its exact source
canonical output/commit/stop parity status
CF4 canonical work and R3 extra OBSERVE work
explicit `SOURCE_ONLY | GPU_OBSERVED | NUMERIC_QUALIFIED | PHYSICAL_QUALIFIED | HOLD | FAIL`
receipt hash
```

Aggregate:

```text
parent CF1/CF2/VH6/CF3/CF4/CF5-C-R2 exact receipt bindings
route manifest digest and required route-depth matrix
actual observed/qualified route-depth matrix
NOT_SELECTED / NOT_APPLICABLE / HOLD/FAIL with first precise reason
training source digest before/after
compile, native Naga, runtime and GPU physical statuses
logical prefix capacity / canonical visible length parity
precompletion reuse / duplicate retirement / stale reuse violation counts
production_admission = false
cf5_d_active = false
performance_status = NOT_PROMOTED
```

A receipt hash must bind canonical bytes of actually observed fields. No literal success-shaped `physical_pass=true`, no promotion based only on a source file's existence and no reuse of a previous binary's audit JSON as live authority.

## 19. Failure classes

```text
HOLD_CF5_C_R3_PARENT_COMPILE_UNVERIFIED
HOLD_CF5_C_R3_PARENT_TREE_PHYSICAL_UNVERIFIED
HOLD_CF5_C_R3_NATIVE_NAGA_UNVERIFIED
HOLD_CF5_C_R3_LINEAR_NATIVE_SEAM_UNBOUND
HOLD_CF5_C_R3_LINEAR_NOT_SELECTED
HOLD_CF5_C_R3_HEADWISE_NATIVE_ABI_UNAVAILABLE
HOLD_CF5_C_R3_TENSORCUBE_ABI_UNAVAILABLE
HOLD_CF5_C_R3_NUMERICAL_POLICY_UNBOUND
HOLD_CF5_C_R3_REQUIRED_ROUTE_NOT_SELECTED
HOLD_CF5_C_R3_ROUTE_COVERAGE_INCOMPLETE
FAIL_CF5_C_R3_WRONG_VERIFIER_INSTANCE
FAIL_CF5_C_R3_LINEAR_TREE_IDENTITY_DRIFT
FAIL_CF5_C_R3_JACOBI_ITERATION_DRIFT
FAIL_CF5_C_R3_TREE_AS_LINEAR_EVIDENCE
FAIL_CF5_C_R3_HEADWISE_AS_BURN_EVIDENCE
FAIL_CF5_C_R3_TENSORCUBE_AS_BURN_EVIDENCE
FAIL_CF5_C_R3_HEADWISE_CAUSAL_VISIBILITY_DRIFT
FAIL_CF5_C_R3_KV_PHYSICAL_STRIDE_DRIFT
FAIL_CF5_C_R3_KV_HIDDEN_TAIL_ACCESS
FAIL_CF5_C_R3_OWNER_OR_CONTENT_GENERATION_DRIFT
FAIL_CF5_C_R3_NUMERIC_PARITY_UNQUALIFIED
FAIL_CF5_C_R3_LAYER_COUNT_OR_ORDER_DRIFT
FAIL_CF5_C_R3_STALE_OR_DUPLICATE_COMPLETION
FAIL_CF5_C_R3_PRECOMPLETION_LEASE_REUSE
FAIL_CF5_C_R3_CHECKPOINT_TRAINING_SOURCE_DRIFT
FAIL_CF5_C_R3_RUNTIME_SOURCE_DIGEST_OMISSION
FAIL_CF5_C_R3_FULL_QKV_HOST_READBACK
FAIL_CF5_C_R3_CANONICAL_PUBLICATION_DRIFT
FAIL_CF5_C_R3_FALSE_PHYSICAL_RECEIPT
FAIL_CF5_C_R3_EARLY_CF5_D_ACTIVE
```

## 20. Validation and command authority

The R3 source validator SHALL statically require:

- Actual native Linear callsite with same program owner and per-iteration tree.
- Actual selected Headwise incremental/chunked and TensorCube incremental branches, each with typed route receipt. No Burn reclassification.
- Actual K and V stride, logical visibility, causal/position identity and separate tail guards.
- Matching completion and resource ownership for every GPU comparison.
- Training source digest intact; new R3 modules/WGSL included in runtime hash.
- No canonical `state.kv` replacement, no extra token commit, no silent fallback.
- Route matrix assembled from *observed* events rather than literal flags.

Parent preflight commands, not claims of execution:

```powershell
python .\tools\validate_ash_aof_r1_cf5_c_r2_verifier_scope_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf5_cf6_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib aof_r1_kv_consumer_bridge --release --locked -j 1
```

Once baked, invoke the R3 native validator, the existing native shader/Naga qualification command (actual arguments derived from the baked CLI), and a real model/GPU campaign. Preserve exit codes and log/binary SHA. The source package does not contain a Rust toolchain or the exact required external sherpa-rs vendor directory, so the above commands have **not** been run in this specification phase.

## 21. Implementation and admission stages

| Stage | Actual implementation target | Terminal evidence |
|---|---|---|
| **R3-P0** | Exact dependency restore, Cargo/Naga, parent Tree GPU control | Native compile and Tree physical control measured |
| **R3-A** | Linear/Jacobi same-instance per-iteration scope | Actual Linear GPU route-local qualification |
| **R3-B** | Headwise incremental selected output reader | Selected Headwise context qualification |
| **R3-C** | Headwise chunked selected output + route visibility | Selected Headwise chunked qualification |
| **R3-D** | TensorCube actual incremental output reader | Real W9A-selected TensorCube qualification |
| **R3-E** | Exact route manifest, per-route receipt and truth-based aggregate | No route/depth laundering or fabricated zeros |
| **R3-F** | EOS/cancel/emit/stale/duplicate and AOF-OFF parity on real GPU | Full applicable route/depth/canonical matrix closure |

A partial R3 stage can report a partial **source/physical observation** but never full R3 PASS. No stage changes CF5-D ACTIVE by implication.

## 22. Completion law

Only emit:

```text
PASS_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_PHYSICAL_QUALIFICATION
```

when:

```text
SOURCE
    all actual selected-route native callsites mapped
    strict training-checkpoint lineage preserved
    complete runtime source digest includes new shaders/modules
STATIC
    R3 and all applicable parent gates PASS
    CF4 SHA supersession honestly disclosed
COMPILE
    actual backend/model_core/orchestrator native release PASS
    referenced Naga/WGPU shaders validated
RUNTIME
    all applicable route/owner/lifetime negative tests PASS
PHYSICAL
    true Tree AND Linear current-session observations
    Headwise incremental + Headwise chunked selected observations
    TensorCube actual incremental when applicable
    Burn controls independently retained
    complete required D1/D2/D4 matrix by route and depth
    real same-Queue completion / safe resource retirement
    qualified numerical parity or explicit HOLD (no PASS when HOLD)
    stale publication, premature reuse, duplicate KV/commit = 0
    EOS/stop/cancel/emit canonical parity retained
PROMOTION
    production_admission = false
    cf5_d_active = false
    performance = NOT_PROMOTED
```

One missing applicable route, unbound comparator, unseen completion or stale identity causes HOLD/FAIL, not a blanket PASS. If the exact build proves a route is genuinely structurally unavailable, its hash-sealed route manifest may classify it `NOT_APPLICABLE` without inventing a GPU run.

---

## Final invariant

```text
REAL TREE + REAL LINEAR VERIFIER
+
SELECTED BURN / HEADWISE / TENSORCUBE OUTPUTS
+
SAME DEVICE / QUEUE / SESSION / GENERATION
+
KV CAPACITY-STRIDED READING WITH INVISIBLE TAIL
+
ACTUAL GPU CONTEXT PARITY AND RETIREMENT
+
STRICT 19-INPUT TRAINING SOURCE IDENTITY
+
FULL APPLICABLE ROUTE/DEPTH NEGATIVE MATRIX
+
UNCHANGED CANONICAL TOKEN / KV / STOP
=
CF5-C-R3 OBSERVE PHYSICAL QUALIFICATION

NOT YET = CF5-D ACTIVE CANONICAL BLOCK PUBLICATION
NOT YET = REMOVAL OF PER-TOKEN CANONICAL KV PREFIX COPY
NOT YET = FUSED PRODUCTION PROMOTION
NOT YET = PERFORMANCE SPEEDUP
```

**Updated evidence boundary:** Partial SOURCE/STATIC changes have been baked and packaged, but none of the Rust COMPILE, Naga, real GPU physical parity, canonical ACTIVE publication or measured performance completion requirements has been met.

---

## SOURCE BAKE ANNEX / 2026-10-09

This annex records the *implemented partial candidate source* and its bounded evidence. It supersedes the opening "specification only" state of the original proposal, **not** the required physical/semantic completion conditions above.

### Exact artifact lineage

- Parent full code-only: \`ASH_PASS3_AOF_R1_CF5_C_R2_VERIFIER_NATIVE_SEAM_CHECKPOINT_LINEAGE_QUALIFICATION_CODE_ONLY.zip\`
- Parent SHA256: \`461e7509db39278bf1a1d05f7673d0fda8a0a3d17abdca63b84ca77b0d8038cb\`; 8,734 files
- Baked full: \`ASH_PASS3_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_CODE_ONLY.zip\`
- Baked full SHA256: \`6372140b21d5eb30fbe32fa6b3474849b9b3f987487f8ea53cf2e3ec54359558\`; **8,735 files**
- Baked overlay: \`ASH_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_OVERLAY_CODE_ONLY.zip\`
- Overlay SHA256: \`10f76d9a56db994cf2f83c1b614f9e5a768a58508d27c5a598e35bd42703514a\`
- Exact delta **ADD 1 / MOD 7 / DEL 0**. Full and overlay ZIP CRC, per-entry source-byte comparison PASS.
- Detailed digest manifest: \`ASH_AOF_R1_CF5_C_R3_BAKE_MANIFEST.json\`; test report: \`ASH_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_BAKE_REPORT.md\`.

### Modified SOURCE

- \`crates/burn_webgpu_backend/src/aof_r1_lookahead.rs\`: \`Arc::ptr_eq\` real verifier-instance currentness; reject wrong verifier owner.
- \`crates/burn_webgpu_backend/src/aof_r1_cf5_c_r2_verifier_observe.rs\`: optional actual \`jacobi_iteration\` and \`window_epoch\` fields; Tree receipts remain compatible with legacy optional values.
- \`crates/model_core/src/aof_r1_lookahead.rs\`: same natural \`aof_r1_jacobi_choices\` call wrapped in \`linear_oracle=true\` scope per real iteration, actual ping-pong Tree, original verifier Arc, session/round/physical bindings; guard lifetime closed before advance.
- \`crates/model_core/src/aof_r1_runtime.rs\`: completed parked KV read views materialized before actual Jacobi scope; existing Tree and normal canonical routes unchanged.
- \`crates/model_core/src/aof_r1_kv_consumer_bridge.rs\`: typed selection receipts \`IncrementalBurn/Headwise/TensorCubeActual\`, \`ChunkedBurn/Headwise\` with native selected output/position/generation lineage, explicitly UNKNOWN GPU candidate comparison for unimplemented routes.
- \`crates/model_core/src/decode_state.rs\`: only actual selected incremental/chunked output produces evidence; TensorCube actual requires W9A receipt digest. No Headwise/TensorCube output reclassified as Burn, no canonical result substitution.
- \`crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs\`: actual Tree/Linear backend layer rows and selected-native evidence aggregated per route; absent rows are \`UNOBSERVED_SELECTION_UNKNOWN\`, **not** proof the route was unselected. \`full_r3_pass_token=null\`, \`physical_campaign_qualified=false\`, \`active_canonical_kv=false\` and no performance promotion.

Added:
- \`tools/validate_ash_aof_r1_cf5_c_r3_selected_route_static.py\`: exact source/lineage and 15 negative mutation gates.

### Scope distinction

- **R3-A: SOURCE implemented.** Natural Jacobi/Linear backend attention scope is added; actual CUDA/WGPU execution and bitwise equality are not demonstrated.
- **R3-B/C/D: selected-native receipt SOURCE implemented, but capacity-strided Headwise/TensorCube shadow comparison is NOT_IMPLEMENTED.** Their numerical and physical admission stays HOLD. Existing Burn scalar observations are **not** bitwise proof.
- **R3-E: source-only truthful route evidence inventory implemented**; no inference from zero rows to NOT_SELECTED.
- **R3-P0/F:** exact Cargo/Naga baseline and D1/D2/D4 physical campaign NOT_RUN. Full R3 PASS cannot be emitted.
- The existing 19-input head-training checkpoint source digest is byte-identical: \`e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283\`. No training-digest input, legacy checkpoint admission, canonical KV publication or AOF production promotion was modified.

### Observed SOURCE/STATIC tests

\`\`\`text
R3 SOURCE/STATIC          60/60 PASS
R3 negative source       15/15 mutations rejected
R2 parent STATIC         44/44 PASS
R1 parent STATIC         66/66 PASS
CF5-C parent STATIC      62/62 PASS
CF5-A/B parent STATIC    73/73 PASS
CF4 parent STATIC        65/65 PASS
CF3 parent STATIC        51/51 PASS
CF1/CF2/VH6 historical   51/52 FAIL
\`\`\`

The 1 historic failure is the **CF4-superseded byte-identity requirement** for \`aof_r1_prefix_commit.rs\`; it is retained as an unresolved parent static incompatibility, not relabeled PASS.

\`cargo\` / \`rustc\` unavailable in this packaging environment. Exact external workspace \`sherpa-rs\` path input absent. **COMPILE NOT_RUN, Naga NOT_RUN, RUNTIME NOT_RUN, PHYSICAL NOT_RUN, PERFORMANCE NOT_MEASURED.** The source test success is not physical or numerical proof.

### Next binding and HOLD law

First restore exact Cargo path input and run actual backend/model_core/orchestrator release compilation, then real Naga shader qualification and same-source Tree/Linear D1/D2/D4 physical parity and retirement. Build native selected Headwise/TensorCube capacity-strided attention consumers with exact causal visibility and actual output comparison before an all-route physical matrix. The full \`PASS_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_PHYSICAL_QUALIFICATION\` and CF5-D \`ACTIVE\` must remain **HOLD** until every applicable consumer is proven.
