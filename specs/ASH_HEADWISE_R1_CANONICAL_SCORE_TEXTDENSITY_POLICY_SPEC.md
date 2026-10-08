# HEADWISE-R1
## CANONICAL SCORE SCALE / TEXTDENSITY SEMANTIC SEPARATION

**Patch ID:** `HEADWISE-R1`  
**Class:** Headwise attention score-semantics repair / dual-mode numerical qualification  
**Parent:** `ASH_PASS3_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_CODE_ONLY.zip`  
**Successor:** `HEADWISE-R2` Chunked Causal Fallback Qualification  
**Status (2026-10-09): SOURCE BAKED / STATIC 38/38 PASS; 9/9 negative static mutations rejected.** Rust COMPILE, Naga, real GPU score/context parity, PERFORMANCE: NOT_RUN/NOT_MEASURED. No physical or production PASS; no global score-policy default change. Source and exact acceptance details are in the source-bake annex.

```text
+ EXACT CANONICAL GQA SCORE SCALE
+ EXPLICIT LEGACY TEXTDENSITY-ADJUSTED COMPATIBILITY
+ SEPARATE MATHEMATICAL POLICY FROM TEXTDENSITY METADATA
+ SHORT-KV / LONG-KV V2 PRODUCTION SHADER PARITY
+ EXPLICIT SCORE POLICY ABI / PIPELINE IDENTITY
+ EXISTING 96-BYTE CAUSAL POSITION PARAM CONTRACT PRESERVATION
+ SAME Q/K/V + SAME CAUSAL POSITION NUMERICAL MATRIX
+ NO UNQUALIFIED DEFAULT CHANGE
+ HEAD-TRAINING SOURCE-DIGEST BYTE PRESERVATION
+ NO HEADWISE-R2 MASK CHANGE
+ NO CF5-D ACTIVE / FUSED PRODUCTION PROMOTION
```

---

## 0. Exact SOURCE baseline

Current implementation, verified from the R3 parent archive:

| File | Relevant source |
|---|---|
| `crates/burn_webgpu_backend/src/headwise_atlas.rs` | `AtlasTextDensityUniform::default` lines 83–106; `HeadwiseAtlasRuntimeSpec` lines 142–157; `HeadwiseAtlasGpuParams` lines 217–242; host `scale = 1/sqrt(head_dim)` at 1294 and 2610; selected short/long production pipeline at 845–875, 2546–2565 |
| `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_production_rw.wgsl` | `atlas_score_scale` lines 73–80, `visible_kv_count` lines 87–97, score use 131–143 |
| `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_production_long_kv_optimized_v2.wgsl` | selected long-KV v2 `atlas_score_scale` lines 78–85 |
| `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_production_long_kv_tiled_v1.wgsl` | maintained legacy v1 with the same formula; classify as reachable/qualification-only before modification |
| `crates/model_core/src/model_layers.rs` | canonical `grouped_query_attention()` lines 296–325: `(Q·K^T)/sqrt(d)` with no TextDensity multiplier |
| `crates/model_core/src/native_wgpu.rs` | `atlas_text_density_uniform()` lines 16715–16729: returns `None` if not configured; that maps to `unwrap_or_default()` downstream |

Existing score formula:

```wgsl
let gate = max(text_density.density_gate, 0.25);
// ... lane/packed/cairo/coda/curvature/zero_copy multipliers ...
return params.scale * max(text_density.shader_weight_scale, 0.5)
       * gate * lane_multiplier() * packed_path_multiplier()
       * cairo * coda * curvature * zero_copy;
```

The default `shader_weight_scale=1`, `density_gate=0`, other signal inputs zero. For a raw zero-copy candidate with `active_tensor_zero_copy=1`, the effective additional multiplier is `0.25`; where zero-copy is false, it is `0.25 × 0.985 = 0.24625`. This is **SOURCE arithmetic**, not a measured default distribution of all production calls: configured TextDensity can change these values.

**CONFLICT / SOURCE:** This score law is not mathematically the same as canonical `grouped_query_attention` unless the total multiplier happens to equal 1. That alone does not prove a user-visible model-quality regression.

---

## 1. Scope and unmodified authorities

R1 changes **only Headwise score-policy selection and corresponding shader score scale**, plus strictly necessary source identity / qualification / receipt plumbing.

R1 must not change:

- Q/K/V projections, tensor shapes, head-to-KV-head mapping, normalization, softmax algorithm, online max/denominator update, or output projection.
- `HeadwiseCausalPositionSnapshot`, `visible_kv_count`, query positions, `route_id`, EOS, stop/cancel, FuturePool, canonical KV publication, W9A selection policy, or AOF speculative admission.
- Existing head training recipe, optimizer/VJP, stored checkpoint bytes, or source-digest admission checks.
- Headwise/CF5 GPU lease submission or completion ownership.

**Semantic change:** switching to `CanonicalGqa` changes attention logits and possibly output. It must not be concealed as a performance-only or byte-neutral patch.

---

## 2. Explicit policy SSOT

Proposed backend-owned enum, not claimed to exist:

```rust
#[repr(u32)]
pub enum HeadwiseScorePolicy {
    LegacyTextDensityAdjusted = 0,
    CanonicalGqa = 1,
}
```

Selection must be tied to exact runtime/campaign configuration and recorded in every Headwise production/qualification receipt. Do not infer it from the mere presence of a TextDensity object. `TextDensity` remains useful observation/routing metadata in either mode; only `LegacyTextDensityAdjusted` may apply it to mathematical score scale.

Policy laws:

| Selected policy | Score scale authority | Meaning |
|---|---|---|
| `LegacyTextDensityAdjusted` | Exact pre-R1 formula, including default floor and zero-copy factor | Historical behavior, **not** canonical-GQA parity |
| `CanonicalGqa` | `params.scale = 1/sqrt(head_dim)` | Canonical mathematical score independent of density/lane/path/zero-copy diagnostics |
| Unknown / corrupt policy ID | Explicit error | Neither implicit legacy nor canonical fallback |

**Default-preservation:** Existing production configurations continue the historical policy until a separate, receipt-backed default cutover is approved. A freshly selected **canonical qualification** configuration must use CanonicalGqa even when the TextDensity object is otherwise default. Changing the process-wide default is a separately declared semantic change, not a hidden part of this source bake.

No environment variable may silently override a committed `HeadwiseScorePolicy` selected by the session authority.

---

## 3. GPU parameter / shader ABI contract

Current `HeadwiseAtlasGpuParams` is 96 bytes, with `_pad_align0: [f32; 3]` and `_pad0: [f32; 4]`; `_pad0[0]` holds the existing input-layout flag. **Do not repurpose `_pad0[0]` or change the meaning of `scale`.**

Recommended narrow representation: add explicit `score_policy: u32` in the existing post-`scale` alignment space and resize `_pad_align0` accordingly, while preserving total 96-byte size, `_pad0` offset, `HEADWISE_CAUSAL_GPU_PARAM_SIZE_BYTES`, and existing layout selection. Alternatively, a policy-specialized, versioned pipeline may be used if exact ABI equivalence is demonstrated. Do not silently steal an unrelated float flag.

- Version policy ABI as `ash.attn.headwise.score_policy.v1` and bind to shader source digest / production receipt.
- Assert exact Rust/WGSL field offsets and 96-byte struct size, not only `size_of` equality.
- Update **both actual selected** short-KV production shader and long-KV optimized v2 shader. Audit tiled-v1/forced-probe paths; either update or explicitly exclude them from canonical qualification.
- Pipeline cache key and route receipt must distinguish score policy whenever a separate shader/pipeline variant is involved.
- CPU dispatch admission rejects unknown policy before resource binding/submission. GPU guard may diagnose corruption but must not silently substitute a policy.

Proposed WGSL contract:

```wgsl
fn canonical_score_scale() -> f32 {
    return params.scale;
}
fn legacy_adjusted_score_scale() -> f32 {
    // Exact historical atlas_score_scale expression (unchanged).
    return params.scale * max(text_density.shader_weight_scale, 0.5)
        * max(text_density.density_gate, 0.25)
        * lane_multiplier() * packed_path_multiplier()
        * cairo_factor() * coda_factor() * curvature_factor()
        * zero_copy_factor();
}
```

The helper names are proposed; actual legacy expression must be byte-equivalent in its arithmetic order, not rewritten freely for style. WGSL select/switch dispatches `CanonicalGqa` vs legacy using the exact policy identifier.

---

## 4. TextDensity isolation

In `CanonicalGqa` the following must **not affect score scale**:

```text
density_lane, packed_path_id, shader_weight_scale, density_gate,
cairo_risk_proxy, coda_weight_mean, curvature_mean,
active_tensor_zero_copy
```

They may remain in telemetry, route-policy selection, or a separately defined *non-score* mechanism, but those other uses must not be recast as mathematical equivalence. Test the same Q/K/V and causal snapshot while varying each TextDensity field individually: canonical score identity must remain unchanged.

For `LegacyTextDensityAdjusted`, preserve all multipliers and their existing default/floor semantics exactly.

---

## 5. Parity oracle and isolation of R2

R1 parity must isolate scaling from the existing chunked causal discrepancy. Primary baseline: **incremental `seq_q=1`** with actual `HeadwiseCausalRouteId::IncrementalDecode`, the same visible K/V range and `head_dim=64`, GQA head mapping and physical Q/K/V buffers.

Compare:

```text
reference: current canonical Burn GQA score/context
candidate: Headwise CanonicalGqa, short/long production route
control: historical Headwise LegacyTextDensityAdjusted
```

- First compare math invariants: scale bits, shapes, `q_head -> kv_head` mapping, visible key count, finite score/context, and route identity.
- Compare actual context with the **existing project numeric tolerance** where an appropriate authority exists. If none is bound, report per-row absolute/relative error and `HOLD_NUMERICAL_TOLERANCE_UNBOUND`; do not invent a threshold.
- Floating-point subgroup reduction and online softmax may differ in operation order. Exact bitwise context parity is desirable evidence, **not assumed** merely because scales match.
- Score parity may use bounded deterministic GPU fixtures; production must not perform full Q/K/V host readback to diagnose every step.
- Record first mismatching head / query / key (if score observed) or context component; classify error source separately from TextDensity and mask policy.
- Chunked R1 score-only fixtures may use the **same explicit Headwise visibility** on both arms, not the pre-R2 unmasked Burn fallback. Full chunked parity is an R2 acceptance obligation.

At least test default and non-default TextDensity, `seq_q=1`, different valid head mapping, near-tie/nonfinite fixtures, and short/long route selection around the existing router boundary; do not assume route solely from length.

---

## 6. Error and negative matrix

Required fail-closed cases:

```text
unknown score-policy ID
missing policy receipt / stale policy identity
canonical mode influenced by density_lane or density_gate
canonical mode influenced by active_tensor_zero_copy
legacy expression altered, multiplication order changed
short-KV updated while selected long-KV v2 remains historical
pipeline reuse with mismatched policy
head_dim / GQA mapping unsupported
score/context nonfinite
context mismatch outside admitted numerical contract
historical default changed without explicit cutover
CF5/Causal position or canonical KV semantics modified
```

Proposed failure codes:

```text
FAIL_HEADWISE_R1_SCORE_POLICY_UNBOUND
FAIL_HEADWISE_R1_SCORE_POLICY_ID_UNKNOWN
FAIL_HEADWISE_R1_CANONICAL_SCALE_DRIFT
FAIL_HEADWISE_R1_TEXTDENSITY_LEAK_IN_CANONICAL
FAIL_HEADWISE_R1_LEGACY_ADJUSTED_FORMULA_DRIFT
FAIL_HEADWISE_R1_SHORT_LONG_ROUTE_POLICY_DRIFT
FAIL_HEADWISE_R1_GPU_PARAMS_ABI_DRIFT
FAIL_HEADWISE_R1_NUMERIC_PARITY
FAIL_HEADWISE_R1_TRAINING_DIGEST_DRIFT
FAIL_HEADWISE_R1_PREMATURE_DEFAULT_PROMOTION
```

---

## 7. Existing checkpoint + runtime source identity

`shared_lm_training_source_digest()` contains 19 exact input files including `model_layers.rs`, `native_wgpu.rs`, `aof_r1_verification.rs` and the Cargo lock. Avoid direct edits to those files in R1; all included training bytes and the digest must remain exact, or use a separately authorized new checkpoint lineage. Never relax `AOFSharedLmTrainingSourceMismatch` or overwrite existing manifests.

The current `ark_runtime_source_digest()` enumerates AOF integration files but does **not** inherently cover the selected Headwise production shader strings. R1 therefore needs a versioned **Headwise score-policy source digest** binding:

```text
Headwise backend implementation + actual short/long WGSL bytes
+ score ABI/policy revision + selected route + TextDensity source
```

If R1 integrates into AOF receipts, extend the existing runtime digest domain explicitly and invalidate stale receipts by source identity. Do not claim that unchanged generic AOF source hash proves updated Headwise shader identity.

---

## 8. Execution modes and receipts

Modes: `LEGACY`, `OBSERVE_CANONICAL`, and `CANONICAL_QUALIFIED`. These are **score qualification modes**, not CF5-D KV `ACTIVE` or AOF packed production cutover.

- `LEGACY`: historical adjusted score stays authoritative.
- `OBSERVE_CANONICAL`: legacy source remains output authority; canonical score context is compared on exact same input / position; extra GPU work is accounted separately.
- `CANONICAL_QUALIFIED`: only after exact physical parity and source/route/owner seal, canonical score output may become authoritative **within explicitly admitted Headwise route/session**. The global process default remains historical unless separately promoted.

Suggested receipt: `headwise_r1_score_policy_numerical_receipt.json` containing schema, binary/source digests, Device/Queue/session/owner identity, route ID, source/shader digest, score policy, TextDensity values/digest, `scale` f32 bits, score/context comparison coverage, max/first mismatch, completion/retirement, old-output unchanged observation, and `global_default_changed=false`.

Counters whose measurement authority does not exist remain `UNKNOWN`/`NOT_MEASURED`, not literal success-shaped zero.

---

## 9. Validation ladder

**SOURCE/STATIC:** both selected shader variants, policy ID, 96-byte ABI and layout offset gates, legacy formula preservation, training source digest, route receipts, negative source mutations.

**COMPILE:** real `burn_webgpu_backend` and `model_core` release builds; actual Naga validation for selected WGSL variants (not merely shader registration).

**RUNTIME:** deterministic score policy and one-query reference tests, checked session/route/pipeline identity. GPU mock simulation is not PHYSICAL.

**PHYSICAL:** real native WGPU short/long Q/K/V numerical/semantic matrix, actual queue completion, same-source receipt, no hidden QKV host readback, no early resource reuse.

**PERFORMANCE:** not a gate for R1 correctness and no speedup implied.

Suggested commands after restoring the existing exact missing workspace vendor path:

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo test -p burn_webgpu_backend --lib headwise_r1 --release --locked -j 1
cargo test -p model_core --lib headwise_r1 --release --locked -j 1
```

New test filters are **proposed**, not claimed as current Cargo test targets. A matching physical canary/CLI must be added and actually executed.

---

## 10. Completion law

`PASS_HEADWISE_R1_CANONICAL_SCORE_POLICY_QUALIFICATION` may be issued only if all of these are true:

```text
actual selected short and long production paths covered
canonical scale truly = params.scale = 1/sqrt(head_dim)
canonical TextDensity score coupling = 0
legacy adjusted behavior preserved under explicitly legacy policy
same input/position score/context parity admitted
owner and pipeline identity current; GPU work completed/retired
Rust COMPILE + WGSL Naga + native WGPU PHYSICAL completed
training source digest / checkpoint admission unchanged
no unqualified default switch; no CF5-D or AOF production promotion
```

If any applicable route lacks numerical evidence, return `HOLD_HEADWISE_R1_NUMERICAL_QUALIFICATION_INCOMPLETE`. Static gates never elevate themselves to physical PASS.

**Final invariant:** `CANONICAL SCORE AUTHORITY + EXPLICIT ADJUSTED LEGACY + REAL Q/K/V NUMERIC PARITY + ORIGINAL CHECKPOINT LINEAGE = HEADWISE-R1 QUALIFIED`, with global default still separately gated.

---

## HEADWISE-R1 exact SOURCE bake annex (2026-10-09)

This annex supersedes the historical "specification only" label for SOURCE/STATIC **only**, not the original numerical/physical acceptance law. Full PHYSICAL R1 qualification is **HOLD**.

- Parent: `ASH_PASS3_AOF_R1_CF5_C_R3_NATIVE_SELECTED_ROUTE_CONSUMER_PHYSICAL_CLOSURE_CODE_ONLY.zip` SHA256 `6372140b21d5eb30fbe32fa6b3474849b9b3f987487f8ea53cf2e3ec54359558`, 8,735 files.
- HEADWISE-R1 full code-only: `ASH_PASS3_HEADWISE_R1_CANONICAL_SCORE_TEXTDENSITY_POLICY_CODE_ONLY.zip` SHA256 `465db0faaa79142bdf763f9ca6d1615bcc16155705d546128df9a0bff17b06bf`, 8,737 files.
- R1 overlay: `ASH_HEADWISE_R1_CANONICAL_SCORE_TEXTDENSITY_POLICY_OVERLAY_CODE_ONLY.zip` SHA256 `0640888b2f38efa9ea255dbf5dfa49036d7a3a644f2fc2daf53e033091f3c179`. ADD 2 / MODIFY 9 / DELETE 0.
- Source touch points: backend `headwise_atlas.rs` / `lib.rs`; `headwise_atlas_attention.wgsl`; `headwise_atlas_attention_production_rw.wgsl`, selected `...long_kv_optimized_v2.wgsl`, long-KV v1/compatibility variants; `headwise_reference_attention_measurement.wgsl`; model-core runtime digest source `aof_r1_admission.rs`. New Rust ABI test and static validator.
- The selected score mode is explicitly `HeadwiseScorePolicy::{LegacyTextDensityAdjusted,CanonicalGqa}`. Four existing atlas input constructors continue to default to Legacy. Canonical mode uses `params.scale` alone; Legacy preserves the prior WGSL multiplier expression and arithmetic order. Unknown mode ID is rejected at the Rust selector boundary.
- Host `HeadwiseAtlasGpuParams` remains 96 bytes; new `score_policy:u32` at offset 68, `_pad0` existing input-layout flag begins at offset 80. Short and selected long-V2 production shader parameter structures and receipt/source-digest binding are versioned.
- Training checkpoint `shared_lm_training_source_digest()` 19-input byte-equivalent SHA256 remains `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`. No legacy checkpoint validation policy change.
- Actual SOURCE/STATIC result: **38/38 PASS**, all **9/9** negative-source perturbations rejected. ZIP CRC and per-entry byte parity PASS.
- Rust COMPILE = NOT_RUN; actual Naga WGSL validation = NOT_RUN; real Headwise↔Burn score/context parity and same-queue completion/retirement = NOT_RUN; PERFORMANCE = NOT_MEASURED.
- Actual `CanonicalGqa` mode remains **opt-in**, not the default. This static SOURCE bake **does not authorize the global production cutover or emit `PASS_HEADWISE_R1_CANONICAL_SCORE_POLICY_QUALIFICATION`**.

Native next steps (not executed):
```powershell
python .\tools\validate_ash_headwise_r1_score_policy_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo test -p burn_webgpu_backend --lib headwise_r1_score_policy --release --locked -j 1
```

Restore exact workspace vendor path dependency before Cargo metadata; do not introduce a stub package. Run existing WGPU26 Naga suite on the updated WGSL and same-source actual incremental Q/K/V short/long Headwise vs Burn parity. No numerical tolerance relaxation or hidden fallback.
