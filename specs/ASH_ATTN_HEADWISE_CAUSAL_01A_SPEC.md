# ASH-ATTN-HEADWISE-CAUSAL-01A

## Absolute Query Position SSOT /
## KV Visibility Upper-Bound Contract /
## Prefill Incremental Chunked Route Matrix /
## Headwise Atlas Causal Parity Seal

---

# 0. Patch identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A
patch_class=headwise_atlas_causal_position_and_visibility_contract
parent_evidence=ash_pass3_ASH-TRUTH-AUDIT-01-R3-R2_snapshot
runtime_schema=ash.attn.headwise.causal.01a.runtime_artifact.v1
primary_artifact=workspace/runtime/attention/ash_attn_headwise_causal_01a_runtime_artifact.json
local_manifest=workspace/runtime/attention/ash_attn_headwise_causal_01a_local_manifest.json
promotion_scope=shadow_parity_readiness_only
production_replacement_default=false
```

This specification is based on the headwise atlas causal-mask audit record dated 2026-07-22. The audit establishes that the authoritative reference attention is causal, the headwise atlas path is shadow/unpromoted, and the active shader family does not expose an explicit query-position/KV-visibility boundary. It does not establish that every observed headwise dispatch consumes future KV entries. This patch closes that uncertainty by making absolute query position and KV visibility explicit runtime truth.

---

# 1. Parent truth

## 1.1 Confirmed by audit

The following are treated as confirmed parent facts:

```text
authoritative attention owner=causal_attention / causal_attention_batched
reference causal loop bound=j<=t
headwise atlas replacement_enabled=false
headwise atlas role=shadow/parity candidate
active base shader has no explicit k_pos vs absolute query position contract
nine inspected shader variants have no verified causal position comparison
GQA query-head to KV-head mapping exists
softmax uses max-pass followed by exp(score-max)
text_density and qwave-adjacent scales may modify attention score
```

## 1.2 Not yet confirmed

The following may not be promoted from inference to fact without runtime evidence:

```text
all headwise atlas dispatches are non-causal
seq_q always equals seq_kv
q_pos is always absolute
q_pos is always local
Q always corresponds to the KV suffix
incremental decode always uses seq_q=1
chunked decode is currently authoritative
training forward never used headwise atlas authority
text_density scale is neutral at runtime
causal-boundary omission is the sole parity failure source
```

## 1.3 Scope consequence

This patch does not claim to fix model quality or word salad. It fixes causal-position truth and parity eligibility for the unpromoted headwise atlas path.

---

# 2. Problem statement

The headwise atlas shader currently receives sequence lengths but no explicit absolute query-position owner.

A shader that loops over:

```text
k_pos=0..seq_kv-1
```

is only known to be causal when the runtime proves that every visited KV position is visible to the current query.

The presence or absence of a textual `mask` token is not authoritative because existing identifiers such as:

```text
seq_mask
head_dim_mask
group_heads_mask
```

are bit masks used for power-of-two arithmetic, not causal visibility controls.

The patch therefore defines causal safety through explicit absolute positions and a derived exclusive KV upper bound:

```text
q_abs=q_position_base+q_local
k_visible_end_exclusive=min(seq_kv, q_abs-kv_position_base+1)
```

subject to validated coordinate-domain contracts.

---

# 3. Goals

R1 requires all of the following:

```text
one absolute-query-position SSOT
one KV absolute-position SSOT
one visibility upper-bound derivation
no seq_kv-seq_q suffix inference in the shader
prefill, incremental, and chunked routes represented explicitly
invalid route shapes rejected before dispatch
both softmax passes use the same visibility bound
GQA mapping unchanged
stable softmax unchanged
text_density behavior frozen and separately receipted
reference vs headwise causal parity matrix
future-key poisoning negative controls
symbol-scoped static checks
shadow-only promotion state retained
```

---

# 4. Non-goals

This patch does not:

```text
promote headwise atlas to production authority
replace causal_attention
change model weights
change training
change sampling
change greedy/top-p policy
change KV cache ownership
change GQA topology
change softmax formulation
change text_density score semantics
change qwave/cairo/coda/curvature factors
prove translation quality
prove language quality
prove performance improvement
prove every attention shader variant production-ready
```

Any production promotion requires a later patch after parity and performance evidence.

---

# 5. Position coordinate model

## 5.1 Canonical coordinate domain

All attention positions are expressed in one monotonically increasing absolute token-position domain owned by the decode session.

Add:

```rust
pub struct AttentionPositionDomain {
    pub decode_session_id: String,
    pub position_epoch: u64,
    pub absolute_origin: u64,
}
```

Required:

```text
position epoch is immutable during one dispatch
query and KV positions use the same domain
position overflow is rejected
position underflow is rejected
session mismatch is rejected
```

## 5.2 Query position range

Add:

```rust
pub struct AbsoluteQueryPositionRange {
    pub q_position_base: u64,
    pub seq_q: u32,
}
```

For local query row `q_local`:

```text
q_abs=q_position_base+q_local
0<=q_local<seq_q
```

The runtime must not infer `q_position_base` from `seq_kv-seq_q` after the route snapshot has been finalized.

## 5.3 KV position range

Add:

```rust
pub struct AbsoluteKvPositionRange {
    pub kv_position_base: u64,
    pub seq_kv: u32,
}
```

For local KV row `k_local`:

```text
k_abs=kv_position_base+k_local
0<=k_local<seq_kv
```

## 5.4 Shared-domain validation

Before dispatch:

```text
query position epoch == KV position epoch
query decode_session_id == KV decode_session_id
q_position_base+seq_q does not overflow
kv_position_base+seq_kv does not overflow
```

---

# 6. KV visibility upper-bound contract

## 6.1 Canonical causal rule

A key is visible when:

```text
k_abs<=q_abs
```

For contiguous KV storage with one absolute base:

```text
visible_count_for_query=
  clamp(q_abs-kv_position_base+1, 0, seq_kv)
```

Canonical exclusive bound:

```text
k_visible_end_exclusive=visible_count_for_query
```

The shader iterates only:

```text
0<=k_local<k_visible_end_exclusive
```

## 6.2 Why the bound is authoritative

The implementation must prefer loop truncation over visiting future keys and `continue`-skipping them.

Required shape:

```wgsl
let q_abs = params.q_position_base + q_local;
let visible_count = visible_kv_count(q_abs, params.kv_position_base, params.seq_kv);
var k_local = 0u;
loop {
    if (k_local >= visible_count) { break; }
    // score work
    k_local = k_local + 1u;
}
```

Both max-pass and sum-pass must use the identical `visible_count` value.

## 6.3 Empty visibility

A query with zero visible keys is invalid for decoder self-attention.

```text
visible_count=0 -> fail closed before dispatch
```

No silent zero vector or NaN softmax fallback is allowed.

## 6.4 Upper-bound invariants

For every query row:

```text
visible_count>=1
visible_count<=seq_kv
max_visited_k_abs<=q_abs
future_key_visit_count=0
max_pass_visible_count==sum_pass_visible_count
```

---

# 7. Route taxonomy

Add:

```rust
pub enum HeadwiseCausalRouteId {
    FullPrefill,
    IncrementalDecode,
    ChunkedDecode,
}
```

Each route is an explicit runtime identity. Route selection is finalized before dispatch and may not be reconstructed from tensor shapes after execution.

## 7.1 Full prefill

Canonical shape:

```text
route=FullPrefill
q_position_base=kv_position_base
seq_q=seq_kv
```

For each query row:

```text
visible_count=q_local+1
```

Negative control:

```text
all-K traversal must differ from causal reference when future keys are poisoned
```

## 7.2 Incremental decode

Canonical shape:

```text
route=IncrementalDecode
seq_q=1
q_position_base=kv_position_base+seq_kv-1
```

For the only query row:

```text
visible_count=seq_kv
```

No explicit future-key rows exist in the current KV range, but the route still carries explicit absolute position truth.

Invalid incremental cases:

```text
seq_q!=1
q_position_base != kv_position_base+seq_kv-1
seq_kv=0
```

## 7.3 Chunked decode

Canonical shape:

```text
route=ChunkedDecode
seq_q>=2
q_position_base >= kv_position_base
q_position_base+seq_q <= kv_position_base+seq_kv
```

The query chunk corresponds to an explicit absolute interval. It is not assumed to be the KV suffix unless the route snapshot says so.

For query row `q_local`:

```text
visible_count=q_position_base+q_local-kv_position_base+1
```

If chunked decode is suffix-aligned, that condition must be separately receipted:

```text
q_position_base+seq_q == kv_position_base+seq_kv
```

Suffix alignment is not inferred from lengths alone.

---

# 8. Route matrix

Minimum positive matrix:

| Case | Route | seq_q | seq_kv | q_base | kv_base | Expected visible counts |
|---|---:|---:|---:|---:|---:|---|
| P01 | FullPrefill | 1 | 1 | 0 | 0 | [1] |
| P02 | FullPrefill | 4 | 4 | 0 | 0 | [1,2,3,4] |
| P03 | FullPrefill | 8 | 8 | 128 | 128 | [1..8] |
| I01 | IncrementalDecode | 1 | 1 | 0 | 0 | [1] |
| I02 | IncrementalDecode | 1 | 8 | 7 | 0 | [8] |
| I03 | IncrementalDecode | 1 | 8 | 135 | 128 | [8] |
| C01 | ChunkedDecode | 2 | 8 | 6 | 0 | [7,8] |
| C02 | ChunkedDecode | 4 | 12 | 8 | 0 | [9,10,11,12] |
| C03 | ChunkedDecode | 3 | 10 | 104 | 100 | [5,6,7] |
| C04 | ChunkedDecode | 4 | 16 | 108 | 100 | [9,10,11,12] |

Minimum negative matrix:

```text
seq_q=0
seq_kv=0
query/KV session mismatch
position epoch mismatch
q base overflow
KV base overflow
query interval outside KV domain
incremental seq_q>1
incremental q base not at final KV position
full prefill unequal sequence lengths
full prefill unequal bases
chunk start before KV base
chunk end after KV end
visible_count=0
max-pass/sum-pass bound mismatch
suffix inference used without route receipt
```

---

# 9. Dispatch parameter ABI

Extend the headwise shader parameter ABI with explicit position fields.

Canonical logical fields:

```text
seq_q: u32
seq_kv: u32
q_position_base_lo: u32
q_position_base_hi: u32
kv_position_base_lo: u32
kv_position_base_hi: u32
position_epoch_lo: u32
position_epoch_hi: u32
route_id: u32
```

If the current WGSL environment does not support native u64 operations, use a verified two-u32 representation with checked addition/subtraction helpers.

Required ABI receipt:

```text
struct byte size
field offsets
field widths
Rust layout digest
WGSL layout digest
layout parity=true
```

No implicit padding may remain unverified.

---

# 10. Rust-side owner contract

## 10.1 SSOT owner

Absolute position truth is owned by the decode session/KV lifecycle, not by the shader and not by a source-code heuristic.

Recommended ownership:

```text
DecodeSession
  -> AttentionPositionSnapshot
  -> HeadwiseAtlasDispatchRequest
  -> WGSL params
  -> dispatch receipt
```

## 10.2 Required snapshot

Add:

```rust
pub struct HeadwiseCausalPositionSnapshot {
    pub route_id: HeadwiseCausalRouteId,
    pub decode_session_id: String,
    pub position_epoch: u64,
    pub q_position_base: u64,
    pub kv_position_base: u64,
    pub seq_q: u32,
    pub seq_kv: u32,
    pub suffix_aligned: bool,
    pub digest: String,
}
```

The digest binds every field.

## 10.3 No reconstruction

Forbidden:

```text
q_position_base=seq_kv-seq_q
q_position_base inferred after dispatch
route inferred from seq_q alone
route inferred from source function name
position receipt rebuilt from output tensor shape
```

Allowed only as a negative-control fixture:

```text
legacy suffix inference
```

---

# 11. Shader family scope

The audit identified one active base shader and multiple variants. R1 must classify every variant into exactly one state:

```text
PatchedAndParityCovered
DisabledPendingPatch
NotReachableInParentRoute
```

No variant may remain reachable with state unknown.

Minimum inspected family:

```text
headwise_atlas_attention
headwise_atlas_attention_f16_pow2
headwise_atlas_attention_subgroup_exp
headwise_atlas_attention_texture_lut_alpha_scale
headwise_atlas_attention_texture_lut_alpha_scale_sparse
headwise_atlas_attention_texture_lut_alpha_scale_gpu
headwise_atlas_attention_texture_lut_exp
headwise_atlas_attention_vec4_f16_packed
plus every additional discovered variant in the active tree
```

The active base shader must be patched first. Other variants may be disabled if parity coverage is unavailable.

---

# 12. Two-pass softmax lock

The patch must preserve:

```text
max-pass
sum/weighted-value pass
exp(score-max_score)
```

Both passes must consume the same:

```text
q_abs
visible_count
GQA head mapping
score scale
```

Required receipt fields:

```text
max_pass_bound_digest
sum_pass_bound_digest
bounds_match=true
max_pass_future_visit_count=0
sum_pass_future_visit_count=0
```

Changing softmax reduction order beyond what is required for the visibility bound is out of scope.

---

# 13. GQA preservation

The following must remain unchanged:

```text
q_heads
kv_heads
query_heads_per_kv
kv_head_for_query_head mapping
```

Parity matrix must cover:

```text
first query head in each KV group
last query head in each KV group
first KV head
last KV head
non-divisible defensive rejection if unsupported
```

Any GQA mapping drift is a separate failure from causal-boundary failure.

---

# 14. text_density and score-scale freeze

The parent shader may multiply attention scores by text_density/qwave-adjacent scale components.

R1 policy:

```text
causal patch may not alter text_density logic
causal patch may not alter gate/lane/packed/cairo/coda/curvature/zero-copy factors
causal parity fixtures must record the effective score scale
```

Two parity modes are required:

```text
Mode A: neutral score-scale fixture
Mode B: parent-runtime score-scale fixture
```

The purpose is causal attribution, not validation of text_density semantics.

Required:

```text
text_density_changed=false
score_scale_code_digest_before==after
```

A later patch must separately audit whether the score-scale modification is valid.

---

# 15. Future-key poisoning tests

Simple random parity may miss a causal leak. Add deterministic future-key poisoning fixtures.

For each prefill/chunked case:

```text
past/current K,V values remain fixed
future K,V values receive large deterministic poison values
reference causal output must remain unchanged
patched atlas output must remain unchanged within tolerance
legacy all-K atlas output must change materially
```

Required metrics:

```text
reference_future_poison_delta
patched_atlas_future_poison_delta
legacy_atlas_future_poison_delta
```

PASS:

```text
reference_future_poison_delta<=tolerance
patched_atlas_future_poison_delta<=tolerance
legacy_atlas_future_poison_delta>poison_detection_floor
```

The legacy delta proves the fixture can detect the leak.

---

# 16. Numerical parity

## 16.1 Oracle

Oracle:

```text
causal_attention / causal_attention_batched
```

The oracle must use identical:

```text
Q/K/V values
GQA mapping
head_dim scale
score-scale configuration
position domain
visibility rule
```

## 16.2 Required shapes

At minimum:

```text
batch=1
q_heads=32
kv_heads=4
head_dim=64
seq lengths=1,2,4,8,16,32
absolute bases=0,1,127,128,2047
routes=FullPrefill,IncrementalDecode,ChunkedDecode
```

Additional reduced fixtures may be used for exhaustive element inspection.

## 16.3 Error metrics

```text
max_abs_error
mean_abs_error
max_rel_error
non_finite_count
mismatch_element_count
```

Relative error denominator:

```text
max(abs(reference), relative_floor)
relative_floor=1e-6 unless parent contract requires stricter
```

Initial promotion thresholds:

```text
max_abs_error<=1e-3
max_rel_error<=1e-3
hard_abs_ceiling<=1e-2
non_finite_count=0
```

Thresholds do not override exact causal visibility checks.

---

# 17. Position and visibility receipts

## 17.1 Per-dispatch receipt

Add:

```rust
pub struct HeadwiseCausalDispatchReceipt {
    pub dispatch_ordinal: u64,
    pub route_id: HeadwiseCausalRouteId,
    pub decode_session_id: String,
    pub position_epoch: u64,
    pub q_position_base: u64,
    pub kv_position_base: u64,
    pub seq_q: u32,
    pub seq_kv: u32,
    pub suffix_aligned: bool,
    pub min_visible_count: u32,
    pub max_visible_count: u32,
    pub zero_visible_query_count: u32,
    pub future_key_visit_count: u64,
    pub max_pass_sum_pass_bound_mismatch_count: u32,
    pub suffix_inference_used: bool,
    pub position_snapshot_digest: String,
    pub receipt_digest: String,
}
```

## 17.2 Per-query sampled receipt

For the complete small fixtures and sampled rows of large fixtures:

```text
q_local
q_abs
visible_count
first_visible_k_abs
last_visible_k_abs
max_visited_k_abs
future_key_visit_count
max_pass_visible_count
sum_pass_visible_count
```

## 17.3 Route summary

Add:

```rust
pub struct HeadwiseCausalRouteMatrixSummary {
    pub positive_case_count: u32,
    pub negative_case_count: u32,
    pub prefill_case_count: u32,
    pub incremental_case_count: u32,
    pub chunked_case_count: u32,
    pub future_poison_case_count: u32,
    pub failed_case_count: u32,
    pub unknown_route_count: u32,
    pub suffix_inference_count: u32,
    pub future_key_visit_count: u64,
    pub digest: String,
}
```

---

# 18. Parity verdict model

Each case receives one of:

```text
PASS
EXPECTED_REJECT
NUMERIC_FAIL
CAUSAL_VISIBILITY_FAIL
POSITION_CONTRACT_FAIL
ABI_FAIL
UNSTABLE_HOLD
```

A case may not be flattened into generic false without reason.

Required top-level counts:

```text
pass_case_count
expected_reject_case_count
numeric_fail_count
causal_visibility_fail_count
position_contract_fail_count
abi_fail_count
unstable_hold_count
```

---

# 19. Negative controls

Minimum 96 negative/positive controls grouped as:

```text
16 position-domain controls
16 route-shape controls
16 visibility-bound controls
16 two-pass consistency controls
16 future-key poisoning controls
16 receipt/static controls
```

Required controls include:

```text
q_position_base omitted
kv_position_base omitted
position epoch mismatch
session mismatch
u64 addition overflow
seq_q=0
seq_kv=0
full-prefill unequal bases
full-prefill unequal lengths
incremental seq_q=2
incremental query not at last KV position
chunk interval before KV start
chunk interval after KV end
zero visible keys
visible count greater than seq_kv
future key included by one
max-pass causal, sum-pass all-K
sum-pass causal, max-pass all-K
legacy seq_kv-seq_q inference
q_pos local treated as absolute
absolute q_pos treated as local
future K poison
future V poison
GQA mapping altered
text_density code altered
shader variant reachable but unclassified
receipt digest field omitted
receipt reconstructed after dispatch
broad substring static-check false positive
```

Every expected rejection must show:

```text
rejected=true
dispatch_executed=false
fallback_used=false
```

except shader-level poison controls that intentionally execute a legacy comparison kernel.

---

# 20. Static checks

Static checks must be symbol-scoped or control-flow scoped. Broad substring search may not determine PASS/HOLD.

Forbidden static method:

```text
source.contains("mask")
```

Required checks:

```text
active shader parameter ABI contains q and KV absolute bases
active shader computes one visible bound per query
max-pass loop upper bound uses visible bound
sum-pass loop upper bound uses same visible bound
active shader has no seq_kv-only all-K traversal after patch
Rust dispatcher binds absolute position fields
route validation occurs before dispatch
no production path infers q base from seq_kv-seq_q
GQA mapping symbol digest unchanged
text_density scale function digest unchanged
replacement_enabled default remains false
unknown reachable shader variant count=0
```

Comment text, log strings, receipt field names, fixtures, and documentation are excluded from executable-code counts.

---

# 21. Runtime gate

Add:

```text
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01a_gate.rs
```

The gate must:

```text
load parent snapshot and source tree
classify shader variants
validate Rust/WGSL ABI layout
run route matrix
run future-poison fixtures
run reference parity
run negative controls
emit receipts and verdict
perform no production promotion
perform no model-quality claim
```

Canonical CLI:

```text
--repo-root
--parent-snapshot
--runtime-profile
--route-matrix full
--include-prefill true
--include-incremental true
--include-chunked true
--future-poison true
--verify-gqa true
--freeze-text-density true
--require-shadow-only true
--full-source-hash true
--out-dir workspace/runtime/attention
```

---

# 22. Required artifacts

```text
workspace/runtime/attention/
  ash_attn_headwise_causal_01a_runtime_artifact.json
  ash_attn_headwise_causal_01a_local_manifest.json
  ash_attn_headwise_causal_01a_parent_binding_receipt.json
  ash_attn_headwise_causal_01a_shader_family_inventory.json
  ash_attn_headwise_causal_01a_position_abi_receipt.json
  ash_attn_headwise_causal_01a_route_matrix.json
  ash_attn_headwise_causal_01a_dispatch_receipts.json
  ash_attn_headwise_causal_01a_future_poison_receipts.json
  ash_attn_headwise_causal_01a_gqa_preservation_receipt.json
  ash_attn_headwise_causal_01a_softmax_two_pass_receipt.json
  ash_attn_headwise_causal_01a_text_density_freeze_receipt.json
  ash_attn_headwise_causal_01a_parity_summary.json
  ash_attn_headwise_causal_01a_negative_control_matrix.json
  ash_attn_headwise_causal_01a_static_checks.json
  ash_attn_headwise_causal_01a_no_promotion_guard.json
  ash_attn_headwise_causal_01a_model_quality_claim_guard.json
  ash_attn_headwise_causal_01a_verdict.json
```

Generated runtime artifacts are excluded from the source bake archive.

---

# 23. Primary artifact ABI

Required top-level flat fields:

```text
schema
patch_id
parent_patch_id
pass
status
verdict
primary_artifact
manifest
parent_snapshot_digest
source_tree_digest
active_shader_variant_id
active_shader_digest
position_abi_digest
route_matrix_digest
positive_case_count
negative_case_count
prefill_case_count
incremental_case_count
chunked_case_count
future_poison_case_count
failed_case_count
future_key_visit_count
zero_visible_query_count
max_pass_sum_pass_bound_mismatch_count
suffix_inference_count
unknown_shader_variant_count
gqa_mapping_changed
text_density_changed
replacement_enabled
production_authority_claim_count
model_quality_claim_count
```

No nested object may replace these public fields.

---

# 24. Failure codes

```text
ParentSnapshotMissing
ParentSnapshotDigestMismatch
AuthoritativeReferenceAttentionMissing
HeadwiseShaderInventoryIncomplete
HeadwiseActiveShaderUnknown
HeadwiseReachableVariantUnclassified
AbsoluteQueryPositionMissing
AbsoluteKvPositionMissing
AttentionPositionEpochMismatch
AttentionPositionSessionMismatch
AttentionPositionOverflow
AttentionQueryIntervalOutsideKvDomain
HeadwiseRouteUnknown
HeadwiseFullPrefillShapeInvalid
HeadwiseIncrementalShapeInvalid
HeadwiseChunkedShapeInvalid
HeadwiseSuffixInferenceObserved
HeadwiseZeroVisibleKeys
HeadwiseVisibilityUpperBoundOverflow
HeadwiseFutureKeyVisited
HeadwiseMaxSumVisibilityMismatch
HeadwiseRustWgslAbiMismatch
HeadwiseGqaMappingChanged
HeadwiseSoftmaxStructureChanged
HeadwiseTextDensityChanged
HeadwiseReferenceParityFailed
HeadwiseFuturePoisonReferenceChanged
HeadwiseFuturePoisonAtlasChanged
HeadwiseFuturePoisonFixtureIneffective
HeadwiseReceiptMissing
HeadwiseReceiptDigestMismatch
HeadwiseReceiptReconstructed
HeadwiseStaticCheckBroadSubstringUsed
HeadwiseUnexpectedProductionPromotion
ModelQualityOverclaimObserved
CompileTruthMissing
```

---

# 25. PASS formula

```text
PASS =
  parent snapshot bound
  && active authoritative reference attention found
  && active headwise shader classified
  && every reachable shader variant classified
  && Rust/WGSL position ABI parity
  && absolute query position present for every case
  && absolute KV position present for every case
  && route identity explicit for every case
  && all positive route cases pass
  && all invalid route cases reject before dispatch
  && zero visible query count==0
  && future key visit count==0
  && max-pass/sum-pass bound mismatch count==0
  && suffix inference count==0
  && GQA mapping changed==false
  && softmax structure changed==false
  && text_density changed==false
  && reference parity within threshold
  && future poison reference delta within threshold
  && future poison patched-atlas delta within threshold
  && future poison legacy-atlas delta above detection floor
  && negative control count>=96
  && negative control fail count==0
  && unknown shader variant count==0
  && replacement_enabled==false
  && production authority claim count==0
  && model quality claim count==0
```

PASS proves the shadow headwise atlas has explicit absolute query-position truth, an exact causal KV visibility upper bound, and parity coverage for prefill, incremental, and chunked routes. It does not promote the atlas to production or prove that previous model output quality issues are fixed.

---

# 26. Build and run

Expected checks:

```powershell
cargo fmt --all -- --check
cargo check --manifest-path crates/burn_webgpu_backend/Cargo.toml
cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01a_gate
```

Expected run:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01a_gate `
  -- `
  --repo-root . `
  --parent-snapshot workspace/runtime/truth_audit/ash_truth_audit_01_r3_r2_runtime_artifact.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --route-matrix full `
  --include-prefill true `
  --include-incremental true `
  --include-chunked true `
  --future-poison true `
  --verify-gqa true `
  --freeze-text-density true `
  --require-shadow-only true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

Expected PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01A_ABSOLUTE_QUERY_POSITION_SSOT_KV_VISIBILITY_UPPER_BOUND_PREFILL_INCREMENTAL_CHUNKED_ROUTE_MATRIX_HEADWISE_ATLAS_CAUSAL_PARITY_NO_PROMOTION_NO_MODEL_QUALITY_OVERCLAIM
```

---

# 27. Promotion boundary

R1 is shadow parity readiness only.

A later promotion patch must separately prove:

```text
runtime consumer binding
production output authority
performance non-regression
cache/KV lifecycle integration
rollback
no silent fallback
exact active shader variant selection
```

Suggested next patch:

```text
ASH-ATTN-HEADWISE-CAUSAL-01B
Shadow-to-Production Authority Promotion /
KV Lifecycle Binding /
Performance Non-Regression /
Rollback Seal
```
