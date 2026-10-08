# HEADWISE-R2
## CHUNKED CAUSAL BURN FALLBACK SEMANTIC PARITY

**Patch ID:** `HEADWISE-R2`  
**Class:** Chunked decode fallback correctness / selected-route causal visibility  
**Parent:** `HEADWISE-R1` Canonical Score Scale + TextDensity Policy Qualification  
**Reference source:** `ASH_PASS3_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_CODE_ONLY.zip` plus qualified HEADWISE-R1 source  
**Successor:** CF5-C Headwise/TensorCube capacity-strided consumer work, separately gated  
**Status (2026-10-09): SOURCE BAKED / STATIC 22/22 PASS; 10/10 negative static mutations rejected.** Rust COMPILE, Naga, real GPU causal context parity, PERFORMANCE: NOT_RUN/NOT_MEASURED. No physical or production PASS; global chunked fallback default stays LegacyFullStaged. Source and exact acceptance details are in the source-bake annex.

```text
+ SELECTED CHUNKED BURN FALLBACK CAUSAL POLICY
+ HEADWISE CAUSAL POSITION SNAPSHOT AS VISIBILITY SSOT
+ ABSOLUTE QUERY / KV POSITION AND EPOCH ADMISSION
+ PER-QUERY MASK BEFORE SOFTMAX
+ BOTH QUARANTINED REMAINDER AND EXPLICIT BURN FALLBACK
+ LEGACY FULL-STAGED COMPATIBILITY AS EXPLICIT SEMANTIC MODE
+ SAME SCORE SCALE POLICY AS QUALIFIED HEADWISE-R1
+ NO FUTURE TOKEN CONTRIBUTION TO ATTENTION OUTPUT
+ SAME-INPUT SELECTED HEADWISE / BURN NUMERIC PARITY
+ CF5-C SELECTED-ROUTE OBSERVATION TRUTH UPDATE
+ NO TRAINING GQA MATH REWRITE
+ NO OTHER KV / CANONICAL PUBLICATION CHANGE
+ NO UNSOURCED LOSS OR SPEEDUP CLAIM
```

---

## 0. Verified parent source and precise defect

| File | Actual owner / observation |
|---|---|
| `crates/model_core/src/decode_state.rs` | `forward_block_chunked()` 1275 onward; quarantined `burn_remainder` path calls unmasked `grouped_query_attention` at 1352–1359; `BurnFallbackRequired` branch also calls it at 1419–1426 |
| `crates/model_core/src/model_layers.rs` | Generic/training `grouped_query_attention()` 296–325 computes score matmul / sqrt and softmax with **no causal mask** |
| `crates/burn_webgpu_backend/src/headwise_causal.rs` | `HeadwiseCausalPositionSnapshot` contains `q_position_base`, `kv_position_base`, `position_epoch`, `seq_q`, `seq_kv`, `suffix_aligned` and digest; `visible_count_for_query(q_local)` 173–196 provides constrained visible counts |
| `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_production_rw.wgsl` | `visible_kv_count(q_local)` lines 87–97 bounds Headwise loop; selected long-KV v2 also contains equivalent policy |
| `crates/model_core/src/decode_state.rs` | Source of the real chunked causal snapshot: line 2794 constructs `HeadwiseCausalPositionSnapshot::new(ChunkedDecode, ... position_authority.query_position_start, position_authority.kv_position_start, chunk.token_count, post_append_len, true)` |
| `crates/model_core/src/decode_state.rs` | Existing CF5-C-R1 OBSERVE chunked Burn path records `vec![qcount; seq]` because historical fallback sees all staged K/V. This must become policy-qualified evidence, not fabricated causal parity |

**CONFLICT / SOURCE:** Headwise calculates a per-query causal visible count; both ordinary Burn fallback branches currently see complete staged `[0, seq_kv)` domain. When `seq_q > 1`, these are different attention functions.

**SEMANTIC CHANGE:** Correcting the selected chunked fallback to causal attention may change hidden states, token probabilities and text relative to historical unmasked fallback. Do not promise exact legacy OFF/ON output parity. The proper reference is an independent **causal oracle** and qualified Headwise canonical score policy, with a separate legacy drift report.

---

## 1. Explicit visibility policy SSOT

Proposed selected-fallback enum (not an existing Rust API):

```rust
#[repr(u32)]
pub enum HeadwiseChunkedFallbackVisibility {
    LegacyFullStaged = 0,
    CausalSnapshotBound = 1,
}
```

- `LegacyFullStaged`: current Burn behavior, retained only as explicitly identified compatibility/reference policy; **not** causal.
- `CausalSnapshotBound`: only keys permitted by `HeadwiseCausalPositionSnapshot::visible_count_for_query` contribute to output.
- Missing/unknown policy, unavailable exact position authority or inconsistent snapshot => explicit error/HOLD; no silent substitution.

Selected policy must be bound to route choice, layer receipt, CF5 OBSERVE receipt and campaign identity. No guessed causal mask from sequence length alone may override snapshot authority.

Existing production remains unchanged until a separate physically qualified and user-approved semantic cutover. After authorized cutover, the selected chunked fallback is causal; any legacy compatibility arm remains labeled legacy, not a silent fallback from failed causal admission.

---

## 2. Exact mask law

For a session-bound snapshot:

```text
Q_base = q_position_base: u64
K_base = kv_position_base: u64
Q = seq_q: u32 (>= 2 for normal chunked route)
K = seq_kv: u32 (current staged compact KV length)
q_abs(i) = checked(Q_base + i)
k_abs(j) = checked(K_base + j)
```

Key j is allowed to contribute to query i **iff** `k_abs(j) <= q_abs(i)` and `j < seq_kv`. A useful display formula for valid domains is:

\[
\operatorname{visible}(i) = \min\bigl(K,\,Q_{base}+i-K_{base}+1\bigr)
\]

**Rust authority:** `snapshot.visible_count_for_query(i)`, `snapshot.validate_for_shape(seq_q, seq_kv)`, `snapshot.validate_contract()` and `snapshot.validate_digest()`, not unchecked arithmetic from this formula.

For normal suffix-aligned L-token chunk appended to previous visible T tokens:

```text
Q=L, K=T+L
visible(0)=T+1
visible(1)=T+2
...
visible(L-1)=T+L
```

Use original absolute base/position epoch for nonzero-origin domains. A zero-visible normal production query is a hard failure, **not** all-masked softmax. Preserve the existing W8A all-masked fixture as a separate, explicitly nonproduction diagnostic exception.

**Crucial distinction:** Burn matmul + subsequent mask may **physically load** future K values before softmax. R2 requires zero *attention weight/contribution* from future positions, not an unmeasured claim that physical future-key memory loads are zero. Eliminating reads requires a separate fused masked-dot kernel and physical evidence.

---

## 3. Decode-only causal GQA operation

Do **not** change `model_layers.rs::grouped_query_attention()`; it is generic/training math, and `model_layers.rs` belongs to the 19-file checkpoint training-source digest. Build a new decode-only operation and use it **only** at selected chunked Burn fallback callsites.

Proposed new file:

`crates/model_core/src/headwise_chunked_causal_fallback.rs`

Conceptual API (Burn tensor masking methods require compile verification):

```rust
fn grouped_query_attention_chunked_causal<B: Backend>(
    q: Tensor<B, 4>,
    k: Tensor<B, 4>,
    v: Tensor<B, 4>,
    num_heads: usize,
    num_kv_heads: usize,
    head_dim: usize,
    snapshot: &HeadwiseCausalPositionSnapshot,
) -> Result<Tensor<B, 4>>;
```

1. Validate `snapshot.route_id == ChunkedDecode`, session/epoch identity, checked positions, `validate_for_shape()`, and digest before context production.
2. Preserve canonical GQA head grouping, `QK^T/sqrt(head_dim)`, score dtype, original K/V grouping and softmax reduction axis.
3. Build a per-query GPU mask or bounded control descriptor; apply it **to score logits before softmax** with broadcasting over score shape `[batch, kv_heads, group_size, seq_q, seq_kv]`.
4. Mask disallowed logits with effective negative infinity or independently proven zero-weight equivalent. Avoid arbitrary finite negative biases. Guarantee masked probabilities/contributions are zero even under large finite future logits.
5. Reject a fully masked production row (no fabricated zero or uniform context).
6. Keep physical buffers on GPU, no full Q/K/V host readback, no Python preprocessing. Account additional score/mask allocation separately, without claiming speedup.
7. R1 canonical score scale and R2 causal mask are **independent axes**. If selected Headwise uses `LegacyTextDensityAdjusted`, require matched explicit score policy for comparison or report `SCORE_POLICY_NOT_COMPARABLE`.

---

## 4. Modify exactly the two selected chunked branches

In `decode_state.rs::forward_block_chunked()`:

**A. Quarantined remainder (`burn_remainder`)** must consume new causal GQA only with the admitted `CausalSnapshotBound` policy.

**B. `HeadwiseChunkedExecutionOutcome::BurnFallbackRequired`** must consume the identical snapshot-bound causal primitive, retaining independent fallback attribution.

Forbidden scope creep:

```text
forward_block_decode() incremental (seq_q=1): unchanged
full_prefill and training GQA: unchanged
HeadwiseCommitted native output: unchanged
TensorCube W9A (incremental only): not relabeled Burn
checkpoint training/VJP/optimizer: unchanged
canonical KV transaction / generation / EOS/cancel/emit: unchanged
```

Headwise stays authoritative when its selected layer succeeds. The fallback and remainder are modified **only** on their genuine selected route. Do not apply a mask retroactively to already-computed Headwise contexts or reclassify a native route.

---

## 5. CF5-C OBSERVE compatibility and evidence truth

CF5-C-R1's existing full-stage Burn visibility vector must become policy-specific:

```text
LegacyFullStaged  => vec![seq_kv; seq_q], receipt LEGACY_FULL_STAGE
CausalSnapshotBound => snapshot.visible_counts(), receipt CAUSAL_SNAPSHOT_BOUND
```

The capacity-strided shadow reader receives the actual per-query allowed range; `physical_capacity C` and `logical visible V` remain separate. It never becomes canonical KV or replaces canonical context. Bind selected visibility policy, position snapshot digest, owner and generation to receipt.

An absent OBSERVE sample is `UNOBSERVED_SELECTION_UNKNOWN` unless an exact route manifest proves `NOT_SELECTED`. Update any CF5-C-R3 static rule that assumes full-stage Burn literal **only under an explicit versioned supersession**; do not silence unrelated regressions.

---

## 6. Ownership/currentness and stop law

Bind actual model/checkpoint and tokenizer, decode session ID, position epoch/snapshot digest, chunk ID, DecodeStepSpan, layer/selected route, prefix/staged generation, Q/K/V shapes/owner device, and WGPU completion identity where present. Stale identity or mask error must terminate before canonical context/transaction publication.

Preserve EOS, stop sequences, max-token, cancel before/after publish, emit failure and ACK distinction, duplicate consume and partial suffix disposal semantics. Existing canonical transaction remains the only publisher.

---

## 7. Parity and negative matrix

**A. Structural oracle:** valid chunks L=2/3/4 with previous KV T=0/1/long; absolute origins including `u32` lower-word carry; position epoch and session changes; exact first/middle/last query visible range. Invalid cases: stale digest/session, wrong route, mismatched q/k shape, checked overflow, `seq_q=1` chunked misuse, zero-visible normal row, W8A exceptional probe outside production.

**B. Deterministic numerics:** identical f32 Q/K/V/head grouping on causal Burn, independent masked oracle and R1 canonical Headwise short/long paths. Include exact/near ties, extreme finite logits, future-key sentinel changes, and per-query mask contribution. Do not infer `bitwise_exact=true` from a scalar max absolute error of 0 without bitwise comparison authority.

**C. Selected native routes:** actual `HeadwiseCommitted`, explicit `BurnFallbackRequired`, `burn_remainder` and original incremental control. Same-source D1/D2/D4 AOF campaigns may supply separate coverage but are **not satisfied by an unrun label**. Compare real GPU contexts and completion/retirement.

**D. Semantic migration:** separately compare `LegacyFullStaged` vs `CausalSnapshotBound` to record intentional output drift. Do not reject causal repair simply because historical full-stage output differs. No unexplained numerical threshold is added: when an existing authoritative tolerance is unavailable report `HOLD_HEADWISE_R2_NUMERIC_TOLERANCE_UNBOUND`.

Negative gates must catch both fallback callsites missing mask, `seq_q` used as `seq_kv`, a first-query overbroad visibility, unqualified W8A all-masked production, stale snapshot digest, Headwise→Burn relabeling, and incorrect CF5-C `NOT_SELECTED` conclusions.

---

## 8. Failure codes and receipt

```text
FAIL_HEADWISE_R2_VISIBILITY_POLICY_UNBOUND
FAIL_HEADWISE_R2_UNKNOWN_POLICY_ID
FAIL_HEADWISE_R2_SNAPSHOT_DIGEST_DRIFT
FAIL_HEADWISE_R2_POSITION_EPOCH_OR_SESSION_DRIFT
FAIL_HEADWISE_R2_CAUSAL_MASK_ROW_DRIFT
FAIL_HEADWISE_R2_FUTURE_ATTENTION_CONTRIBUTION_NONZERO
FAIL_HEADWISE_R2_ALL_MASKED_PRODUCTION_ROW
FAIL_HEADWISE_R2_FALLBACK_CALLSITE_UNMIGRATED
FAIL_HEADWISE_R2_REMAINDER_CALLSITE_UNMIGRATED
FAIL_HEADWISE_R2_HEADWISE_BURN_CONTEXT_PARITY
FAIL_HEADWISE_R2_SCORE_POLICY_MISMATCH
FAIL_HEADWISE_R2_CF5_OBSERVE_VISIBILITY_DRIFT
FAIL_HEADWISE_R2_TRAINING_DIGEST_DRIFT
FAIL_HEADWISE_R2_SILENT_LEGACY_FULL_STAGE_FALLBACK
FAIL_HEADWISE_R2_PREMATURE_DEFAULT_MIGRATION
```

Receipt: `headwise_r2_chunked_causal_fallback_receipt.json` with schema; R1 parent digest; source/binary identity; visibility/score policy; session, chunk/layer/route/generation; exact snapshot digest and q/kv bases; per-query visible counts or hashed descriptor; observed future **contribution** vs unknown future GPU **loads**; GPU context error; first mismatch; actual submission/completion/retirement; selected-route data, canonical unchanged evidence during OBSERVE, physical status and receipt hash.

No per-element CPU logs or fabricated observed zeros.

---

## 9. Acceptance commands and evidence ladder

**SOURCE/STATIC:** decode-only causal operation, both native Burn chunked branches, position SSOT, policy-specific CF5 evidence, checked negative gates, no training digest drift and no canonical publication change.

**COMPILE:** real model_core/back-end release builds with exact dependencies, Naga if any new WGSL source is added.

**RUNTIME:** exact positions and softmax/masked numeric fixtures; negative cases and observed legacy semantic drift.

**PHYSICAL:** real native WGPU Q/K/V using same Headwise-R1 canonical score, actual selected Headwise vs repaired Burn context, real GPU completion/retirement and D1/D2/D4 as applicable.

**PERFORMANCE:** independently measured if requested; no speedup inference from parity.

After restoring exact workspace dependency inputs:

```powershell
cargo metadata --format-version 1 --locked
cargo check -p model_core --lib --release --locked -j 1
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo test -p model_core --lib headwise_r2 --release --locked -j 1
```

`headwise_r2` is a **proposed** new test filter. A real native WGPU qualification runner and exact receipt still need to be implemented and executed.

---

## 10. Completion law

`PASS_HEADWISE_R2_CHUNKED_CAUSAL_FALLBACK_QUALIFICATION` requires:

```text
HEADWISE-R1 canonical score policy physically admitted for parity
both selected chunked Burn fallback branches use the same validated snapshot
per-query visible counts exactly match selected Headwise
future attention contribution = 0; physical future-load claim = UNKNOWN unless measured
actual same-input numerical context parity admitted
owner/session/generation currentness and completion/retirement proven
training/checkpoint lineage intact
Rust COMPILE, Naga where applicable, real WGPU PHYSICAL PASS
EOS/cancel/emit/stop/duplicate transaction semantics preserved
no premature global default change or CF5-D ACTIVE promotion
```

A separately authorized production cutover may then make `CausalSnapshotBound` authoritative for chunked fallback. That cutover declares **semantic drift** relative to unmasked legacy and requires a fresh generation regression campaign. Failure in the causal route yields HOLD/FAIL, never a silent legacy route deceptively called causal.

**Final invariant:** `SAME SCORE POLICY + SAME POSITION SNAPSHOT + SAME PER-QUERY VISIBLE K/V + REAL NUMERIC PARITY = HEADWISE ↔ BURN CHUNKED CAUSAL QUALIFIED`.

---

## HEADWISE-R2 exact SOURCE bake annex (2026-10-09)

This annex upgrades the implementation state from *specification only* to **SOURCE/STATIC only**. The full HEADWISE-R2 causal GPU qualification remains **HOLD**.

- R1 exact direct parent: `ASH_PASS3_HEADWISE_R1_CANONICAL_SCORE_TEXTDENSITY_POLICY_CODE_ONLY.zip`, SHA256 `465db0faaa79142bdf763f9ca6d1615bcc16155705d546128df9a0bff17b06bf`.
- R1+R2 full code-only: `ASH_PASS3_HEADWISE_R1_R2_CHUNKED_CAUSAL_FALLBACK_CODE_ONLY.zip`, SHA256 `7f5ba1b7c29593a78420fc2b6da2f74f49eb41380cc537833b5da3853efe912f`, 8,739 files.
- R2 overlay: `ASH_HEADWISE_R2_CHUNKED_CAUSAL_FALLBACK_OVERLAY_CODE_ONLY.zip`, SHA256 `6057fc944687f72e66fb20b46575ad26213b505847089d1aaccddd97f19d651f`. ADD 2 / MODIFY 3 / DELETE 0. ZIP CRC/byte-parity PASS.
- New module `crates/model_core/src/headwise_chunked_causal_fallback.rs` defines opt-in `HeadwiseChunkedFallbackVisibility::{LegacyFullStaged,CausalSnapshotBound}`. `crates/model_core/src/lib.rs` exports it. `decode_state.rs` retains Legacy defaults and checks session/position epoch/staged-generation on explicit selection, then routes **both** real chunked Burn fallback branches through the policy-specific evaluation.
- The historical Legacy route performs a **direct early return to the original `grouped_query_attention`**, without executing newly added causal shape/mask validation. The causal route validates exact position snapshot/route/digest, GQA shape and nonempty visibility, then broadcasts a Bool mask over `[batch,kv_heads,group_size,seq_q,seq_kv]` and masks forbidden logits with `-∞` **before softmax**. This does **not** prove future K/V memory loads were physically skipped. GPU mask construction/host allocation overhead is unmeasured.
- In the CF5-C OBSERVE route, legacy selected visibility = full staged `seq_kv` for each query; causal selected visibility = snapshot `visible_counts()`. Causal selected-route receipt adds explicit mode and snapshot digest without recasting Headwise/TensorCube outcomes as Burn. Runtime source digest includes the new causal module. The 19-input head-training digest remains `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
- SOURCE/STATIC: HEADWISE-R2 **22/22 PASS**, **10/10** negative perturbations rejected. R1 **38/38 PASS** and all 9 negatives rejected. R3/R2/C/CF5-A-B/CF4/CF3 parent checks pass.
- **Declared parent static conflict:** prior CF5-C-R1 validator is **64/66 FAIL** because `chunked_no_invented_acceptance` and `real_chunk_burn_visibility` demand a hard-coded Legacy-only assumption. R2 supersedes only those assumptions; **no silent parent gate rewrite or automatic PASS**. Old CF1/CF2/VH6 gate remains **51/52 FAIL** from the existing CF4 exact-prefix-commit-SHA supersession.
- Rust COMPILE = NOT_RUN; native Naga = NOT_RUN; real GPU chunked causal parity, owner and completion/retirement = NOT_RUN; PERFORMANCE = NOT_MEASURED. No `PASS_HEADWISE_R2_CHUNKED_CAUSAL_FALLBACK_QUALIFICATION`, CF5-D ACTIVE or Headwise/TextDensity production mode cutover.

Next native checks:
```powershell
python .\tools\validate_ash_headwise_r2_chunked_causal_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo test -p model_core --lib headwise_r2_visibility --release --locked -j 1
```

Then demonstrate real selected Burn remainder and fallback, D1/D2/D4 (as applicable), chunks length 2/3/4, absolute-position carry, causal mask contribution 0, same score policy on Headwise/Burn and explicit Legacy-vs-Causal semantic difference. No automatic recovery to unmasked Legacy after failed causal admission.
