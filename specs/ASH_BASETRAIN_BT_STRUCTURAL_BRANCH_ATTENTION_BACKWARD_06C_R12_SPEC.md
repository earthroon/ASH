# ASH-BASETRAIN-BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12

## R11 G204D Live Physical Parent / Canonical Base + H1·H2·H3·H4 Attention Backward / Five-Lane G204D Reuse / Shared Canonical K·V Single Authority / Branch-Local Q+δQ Adoption / Gate-Weighted dContext Split / Base dContext Residual Coefficient / Per-Horizon dQ Publication / Per-Lane dK·dV Partial Publication / Deterministic Shared-dK Reduction / Deterministic Shared-dV Reduction / Canonical dQ Base-plus-Branch Accumulation / Gate Gradient Carrier Publication / Zero Branch-Local K Authority / Zero Branch-Local V Authority / Zero K·V Payload Duplication / Zero Gradient Payload Readback / No RoPE Backward / No QKV Projection Backward / No δQ Projector Backward / No Gate Projector Backward / No RMSNorm·OProj·FFN Backward / Gradient Atlas Accumulation Deferred / Optimizer = 0 / Weight Mutation = 0 / Proof Ledger HOLD Seal

> Patch ID: `ASH-BASETRAIN-BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12`
>
> Build revision: `bt-structural-branch-attention-backward-06c-r12`
>
> Physical parent: `BT-WGSL-BACKPROP-G204D-LIVE-PROMOTION-06C-R11`
>
> Proof ledger: `HOLD`

---

## 1. Purpose

R12 promotes the R11 live G204D base-attention backward path into the complete five-lane structural attention backward surface:

```text
BASE
H1
H2
H3
H4
```

The five lanes share one canonical K and one canonical V. Structural branches differ only by the additive query delta and their own exact forward softmax/context state.

R12 publishes:

```text
dQbase_post_rope

dDeltaQ_H1
dDeltaQ_H2
dDeltaQ_H3
dDeltaQ_H4

dK_shared_post_rope
dV_shared

dGate_H1
dGate_H2
dGate_H3
dGate_H4
```

R12 does not run RoPE backward, QKV projection backward, δQ/gate projector backward, gradient-atlas accumulation, optimizer, or weight mutation.

---

## 2. R11 physical parent

R12 requires the R11 physical contract that already admitted:

```text
R10 live-tape parent bound
Q32 live geometry
post-RoPE Q direct lease
post-RoPE K direct lease
canonical V direct lease
Stage11 global-state direct adoption
Stage12 lineage binding
G204D live dispatch
dQ/dK/dV GPU publication
finite + nonzero base gradient
zero gradient payload readback
double-run reproducibility
```

The R11 G204D live executor remains the only attention-backward kernel authority.

R12 does not create a parallel attention-backward implementation.

---

## 3. Structural forward equation

For each selected decoder layer:

```text
Q0 = Qbase
Q1 = Qbase + δQ1
Q2 = Qbase + δQ2
Q3 = Qbase + δQ3
Q4 = Qbase + δQ4
```

All lanes share:

```text
K = Kcanonical
V = Vcanonical
```

Contexts:

```text
C0 = Attention(Q0,K,V)
C1 = Attention(Q1,K,V)
C2 = Attention(Q2,K,V)
C3 = Attention(Q3,K,V)
C4 = Attention(Q4,K,V)
```

Structural output semantics:

```text
Cfinal = C0
       + G1 * (C1 - C0)
       + G2 * (C2 - C0)
       + G3 * (C3 - C0)
       + G4 * (C4 - C0)
```

The current gate projectors are zero-start. R12 retains that exact initialization contract.

---

## 4. Branch forward-tape extension

R10/R11 retained only the base attention tape. R12 may not reuse the base Stage11 state for `Qbase + δQh` because that would differentiate a different softmax surface.

R12 therefore extends the selected live C9 forward tape with four exact branch records:

```text
horizon index
δQ post-RoPE additive surface
gate output
Qbase + δQ branch query
branch Stage11 global softmax state
branch Stage12 context
```

Each H1-H4 branch executes the actual Stage10/Stage11/Stage12 forward attention path during the selected-layer live forward capture.

Required:

```text
branchStage11Count = 4
branchContextCount = 4
baseStage11ReusedForBranch = false
forwardAttentionRecomputeCount = 0
```

The branch forward is part of the original selected-layer capture, not a backward-time recomputation.

---

## 5. Structural parameter identity

The branch forward extension reconstructs the existing 06C structural parameter bank using the exact deterministic R9 initialization contract rather than inventing a second parameter identity.

### Horizon head seed

```text
SHA256(
  headManifestDigest
  + "\0h{horizon}\0fused_weight\0xavier_uniform_sha256_splitmix64_v1"
)
```

### Factor projector seed

```text
domain = ash.06c.tensorcube.factor
parts  = [headManifestDigest, factorFamily]
```

### δQ projector seed

```text
domain = ash.06c.deltaq
parts  = [layerIndex, horizonIndex, headManifestDigest]
```

### Gate projector

```text
weights = exact zero
bias = none
G = sigmoid(rawGate) * 2 - 1
```

The Xavier/SplitMix64 arithmetic is preserved bit-contractually from the previous 06C structural implementation.

---

## 6. Runtime structural manifest prepublication

The structural head manifest is required before C9 executes the selected decoder layer.

R12 therefore lets R06B derive the same tokenizer-capacity manifest, factor slices, fused output width, and structural head manifest before the decoder parent executes, and writes:

```text
--bt-structural-branch-runtime-config
```

The later normal R06B head-manifest construction must match the prepublished manifest and capacity exactly.

Fail closed on drift:

```text
BTMedusaHeadsR12HeadManifestDrift
BTMedusaHeadsR12CapacityManifestDrift
```

This avoids a second structural SSOT.

---

## 7. Exact dContext split

Given upstream `dCfinal`:

```text
dC_H1 = dCfinal * G1
dC_H2 = dCfinal * G2
dC_H3 = dCfinal * G3
dC_H4 = dCfinal * G4
```

Base lane:

```text
dC_BASE = dCfinal * (1 - G1 - G2 - G3 - G4)
```

R12 performs this split on GPU.

Current gate geometry is the exact `[B,Q,1]` output of the existing gate projector. The current physical fixture is B1, so the gate is one scalar per query token and broadcast across all Q-head/feature elements.

---

## 8. Gate-output gradient carrier

For each structural branch:

```text
dGate_h = reduce_hidden(
  dCfinal * (C_h - C0)
)
```

R12 computes this deterministic reduction in WGSL using one 64-lane workgroup per query and a fixed tree reduction.

No floating-point atomic accumulation is used.

The resulting surface is an output-coordinate gradient:

```text
gradientCoordinate = GATE_OUTPUT
```

It is not yet a gate-projector parameter gradient.

---

## 9. Gate-zero semantics

Because the gate projector is zero-start, H1-H4 upstream branch dContext may be exactly zero during initial admission.

R12 therefore distinguishes:

```text
BASE aggregate zero  → hard failure
STRUCTURAL lane zero → ROLE_LOCAL_ZERO allowed
```

A zero structural-lane gradient is evidence of zero current gate-mediated backward pressure, not evidence that the branch is false or invalid.

R11 base nonzero admission remains hard.

---

## 10. Five-lane G204D reuse

R12 uses the R11 live G204D executor for all five lanes.

```text
BASE: Qbase          + canonical K/V + base Stage11 state
H1:   Qbase + δQ1    + canonical K/V + H1 Stage11 state
H2:   Qbase + δQ2    + canonical K/V + H2 Stage11 state
H3:   Qbase + δQ3    + canonical K/V + H3 Stage11 state
H4:   Qbase + δQ4    + canonical K/V + H4 Stage11 state
```

No branch-local K or V forward authority is created.

Required:

```text
canonicalKForwardAuthorityCount = selectedLayerCount
canonicalVForwardAuthorityCount = selectedLayerCount
branchLocalKAuthorityCount = 0
branchLocalVAuthorityCount = 0
```

---

## 11. Per-lane gradient partials

Each G204D lane initially publishes temporary partials:

```text
dQ0, dK0, dV0
dQ1, dK1, dV1
dQ2, dK2, dV2
dQ3, dK3, dV3
dQ4, dK4, dV4
```

The K/V lane partials are workspace only:

```text
role = LANE_LOCAL_PARTIAL
```

They are not externally canonical K/V gradient authorities.

---

## 12. Canonical Qbase gradient

Because all five branch queries contain Qbase:

```text
dQbase_total = dQ0 + dQ1 + dQ2 + dQ3 + dQ4
```

R12 performs this with the fixed merge order:

```text
BASE → H1 → H2 → H3 → H4
```

and publishes:

```text
dQbase_post_rope
```

for future NeoX inverse-gradient processing.

---

## 13. δQ gradients

Because:

```text
Qh = Qbase + δQh
```

R12 publishes:

```text
dDeltaQ_H1 = dQ1
dDeltaQ_H2 = dQ2
dDeltaQ_H3 = dQ3
dDeltaQ_H4 = dQ4
```

These remain in the post-RoPE additive query coordinate used by the forward branch.

R12 does not execute the δQ projector backward.

---

## 14. Deterministic shared-K reduction

Canonical K gradient:

```text
dK_shared = dK0 + dK1 + dK2 + dK3 + dK4
```

Fixed WGSL expression:

```text
((((BASE + H1) + H2) + H3) + H4)
```

Required:

```text
mergeOrder = BASE,H1,H2,H3,H4
unorderedFloatAtomicCount = 0
CPUGradientMergeCount = 0
```

The published authority is only:

```text
dK_shared_post_rope
```

---

## 15. Deterministic shared-V reduction

Canonical V gradient:

```text
dV_shared = dV0 + dV1 + dV2 + dV3 + dV4
```

with the same fixed merge order and zero unordered floating atomic accumulation.

The published authority is only:

```text
dV_shared
```

---

## 16. GPU-only merge implementation

R12 adds four small WGSL utility kernels:

```text
base_train_r12_q_add.wgsl
base_train_r12_base_dcontext.wgsl
base_train_r12_branch_dcontext_gate.wgsl
base_train_r12_ordered_merge5.wgsl
```

They perform:

```text
Qbase + δQ
base dContext split
branch dContext split + gate carrier reduction
ordered five-input gradient merge
```

No utility kernel uses floating-point atomics.

---

## 17. dContext physical admission fixture

Actual OProj backward is deferred, so R12 continues to use the R11 GPU-resident deterministic dContext fixture as the temporary upstream context gradient source.

The fixture is generated on GPU and has:

```text
host payload upload = 0
payload readback = 0
finite = true
nonzero = true
```

R12 uses it to validate the structural split, five G204D lanes, and shared gradient merges.

It is not claimed to be the final training-loss gradient authority.

A later OProj/FFN backward patch replaces this ingress with actual `dCfinal` without changing R12's five-lane logic.

---

## 18. Double-run reproducibility

For each selected layer R12 executes the complete five-lane path twice against immutable forward tape and the same GPU dContext fixture.

Exact GPU parity checks cover 11 canonical publications:

```text
dQbase_post_rope
dK_shared_post_rope
dV_shared
4 × dDeltaQ
4 × dGate carrier
```

Required:

```text
reproducibilityRuns = 2
reproducibilityMatch = true
tensorPayloadReadbackCount = 0
```

For top1:

```text
base logical G204D runs       = 2
structural logical G204D runs = 8
total logical G204D runs      = 10
```

---

## 19. Raw GPU publication surface

Per selected layer R12 publishes 11 logical gradient surfaces:

```text
1 × dQbase_post_rope
4 × dDeltaQ
1 × dK_shared_post_rope
1 × dV_shared
4 × dGate
```

All remain GPU resident.

No gradient payload is mapped to the host.

---

## 20. Gradient readback boundary

Forbidden:

```text
dQ payload readback
dK payload readback
dV payload readback
dDeltaQ payload readback
dGate payload readback
CPU gradient merge
```

Compact status/parity receipts remain permitted.

Required:

```text
gradientPayloadReadbackCount = 0
```

---

## 21. R12 scheduling semantics

Logical dependency order:

```text
Wave A
  gate/context dContext split

Wave B
  BASE G204D

Wave C
  H1/H2/H3/H4 G204D
  branch lanes dependency-independent

Wave D
  ordered dQbase merge

Wave E
  ordered shared-dK merge
  ordered shared-dV merge
```

The final merge order is deterministic regardless of branch dispatch completion order.

---

## 22. Deferred boundaries

R12 must retain zero counts for:

```text
RoPE backward
QKV projection backward
δQ projector backward
gate projector backward
gradient atlas accumulation
optimizer
weight mutation
checkpoint mutation
```

RMSNorm, OProj, and FFN backward are also outside R12.

---

## 23. Runtime receipts

R12 writes at minimum:

```text
r12_parent_r11_receipt.json
r12_branch_tape_layer_XXXX.json
r12_five_lane_layer_XXXX.json
r12_shared_k_merge_layer_XXXX.json
r12_shared_v_merge_layer_XXXX.json
r12_gate_carrier_layer_XXXX.json
r12_reproducibility_receipt.json
bt_structural_branch_attention_backward_06c_r12_final.json
```

The selected live forward also retains the existing R10/R11 tape receipts.

---

## 24. Required CLI gates

All must be true:

```text
--require-bt-structural-branch-r12-r11-physical-parent
--require-bt-structural-branch-r12-five-lane-g204d
--require-bt-structural-branch-r12-canonical-shared-kv
--require-bt-structural-branch-r12-branch-local-q
--require-bt-structural-branch-r12-exact-dcontext-split
--require-bt-structural-branch-r12-gate-carrier
--require-bt-structural-branch-r12-branch-stage11-state
--require-bt-structural-branch-r12-branch-context-tape
--require-bt-structural-branch-r12-dqbase-deterministic-merge
--require-bt-structural-branch-r12-shared-dk-deterministic-merge
--require-bt-structural-branch-r12-shared-dv-deterministic-merge
--require-bt-structural-branch-r12-zero-branch-local-k-authority
--require-bt-structural-branch-r12-zero-branch-local-v-authority
--require-bt-structural-branch-r12-zero-forward-recompute
--require-bt-structural-branch-r12-zero-gradient-readback
--require-bt-structural-branch-r12-double-run-reproducibility
--require-bt-structural-branch-r12-zero-rope-backward
--require-bt-structural-branch-r12-zero-qkv-backward
--require-bt-structural-branch-r12-zero-deltaq-projector-backward
--require-bt-structural-branch-r12-zero-gate-projector-backward
--require-bt-structural-branch-r12-zero-gradient-atlas
--require-bt-structural-branch-r12-zero-optimizer
--require-bt-structural-branch-r12-zero-weight-mutation
```

R12 also supplies:

```text
--bt-structural-branch-runtime-config
```

for pre-C9 structural manifest publication.

---

## 25. Representative fail-closed errors

```text
BTStructuralBranchR11ParentMissing
BTStructuralBranchR11ParentNotPass
BTStructuralBranchTapeMissing
BTStructuralBranchTapeHorizonOrderMismatch
BTStructuralBranchGeometryMismatch
BTStructuralBranchBaseG204DDispatchFailed
BTStructuralBranchG204DDispatchFailed
BTStructuralBranchGradientNonFinite
BTStructuralBranchPayloadReadbackDetected
BTStructuralBranchTotalGradientZero
BTStructuralBranchReproducibilityMismatch

R6R8R12BranchRuntimeConfigReadFailed
R6R8R12BranchRuntimeConfigInvalid
R6R8R12BranchRuntimeGeometryInvalid
R6R8R12BranchRuntimeManifestInvalid
R6R8R12BranchFactorSlicesMissing
R6R8R12ProjectionWeightShapeMismatch
R6R8R12BranchTensorHostUploadObserved
R6R8R12BranchStage11TapeMissing
R6R8R12BranchRuntimeNotPass
R6R8R12BranchTapeCountMismatch

BTMedusaHeadsR12HeadManifestDrift
BTMedusaHeadsR12CapacityManifestDrift
```

---

## 26. Changed source surface

Relative to the supplied R11 parent, R12 changes exactly 12 files:

```text
crates/burn_webgpu_backend/src/base_train_g204d_attention_backward_probe.rs
crates/burn_webgpu_backend/src/base_train_r12_structural_branch_backward.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/base_train_r12_base_dcontext.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r12_branch_dcontext_gate.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r12_ordered_merge5.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r12_q_add.wgsl
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
crates/orchestrator_local/src/base_train_structural_medusa_heads_06b.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

The full source tree contains 6,935 regular files at bake time. The R12 increase from R11 is exactly five new source files: one Rust backend module plus four WGSL kernels.

No Markdown specification, `.sha256`, artifact report, or manifest sidecar is embedded into the code ZIP.

---

## 27. Physical target

For the current top1/Q32 fixture, expected terminal structure is:

```text
[bt-structural-branch-attention-backward-06c-r12]
r11_physical_parent=1
selected_layers=1
attention_lanes=5
base_lanes=1
structural_lanes=4
canonical_k_authority=1
canonical_v_authority=1
branch_local_k_authority=0
branch_local_v_authority=0
base_stage11=1
branch_stage11=4
base_context=1
branch_contexts=4
g204d_base_dispatch=2
g204d_structural_dispatch=8
dq_base_published=1
deltaq_published=4
shared_dk_published=1
shared_dv_published=1
gate_carriers_published=4
gradient_nonfinite=0
total_gradient_nonzero=1
reproducibility_runs=2
reproducibility_match=1
forward_recompute=0
checkpoint_reopen=0
training_decoder_clone=0
gradient_payload_readback=0
rope_backward=0
qkv_projection_backward=0
deltaq_projector_backward=0
gate_projector_backward=0
gradient_atlas=0
optimizer=0
weight_mutation=0
proof_ledger=HOLD
```

---

## 28. PASS seal

```text
PASS_ASH_BASETRAIN_BT_STRUCTURAL_BRANCH_ATTENTION_BACKWARD_06C_R12
R11_G204D_LIVE_EXACT_PHYSICAL_PARENT /
CANONICAL_BASE_PLUS_H1_H2_H3_H4_ATTENTION_BACKWARD /
FIVE_LANE_G204D_EXECUTOR_REUSE /
CANONICAL_SHARED_K_SINGLE_FORWARD_AUTHORITY /
CANONICAL_SHARED_V_SINGLE_FORWARD_AUTHORITY /
BRANCH_LOCAL_Q_PLUS_DELTAQ_EXACT_BINDING /
EXACT_GATE_WEIGHTED_DCONTEXT_SPLIT /
BASE_DCONTEXT_RESIDUAL_COEFFICIENT_BOUND /
BASE_AND_BRANCH_STAGE11_STATE_EXACT_BINDING /
BASE_AND_BRANCH_CONTEXT_TAPE_EXACT_BINDING /
PER_HORIZON_DQ_PUBLICATION /
CANONICAL_DQBASE_DETERMINISTIC_REDUCTION /
PER_LANE_DK_DV_PARTIALS_NONAUTHORITY /
SHARED_DK_DETERMINISTIC_ORDERED_REDUCTION /
SHARED_DV_DETERMINISTIC_ORDERED_REDUCTION /
GATE_OUTPUT_GRADIENT_CARRIER_PUBLICATION /
ZERO_BRANCH_LOCAL_K_PARAMETER_AUTHORITY /
ZERO_BRANCH_LOCAL_V_PARAMETER_AUTHORITY /
ZERO_BRANCH_LOCAL_K_FORWARD_AUTHORITY /
ZERO_BRANCH_LOCAL_V_FORWARD_AUTHORITY /
ZERO_KV_FORWARD_PAYLOAD_DUPLICATION /
ZERO_UNORDERED_FLOAT_ATOMIC_MERGE /
ZERO_FORWARD_ATTENTION_RECOMPUTATION /
ZERO_GRADIENT_PAYLOAD_READBACK /
ZERO_ROPE_BACKWARD /
ZERO_QKV_PROJECTION_BACKWARD /
ZERO_DELTAQ_PROJECTOR_BACKWARD /
ZERO_GATE_PROJECTOR_BACKWARD /
ZERO_GRADIENT_ATLAS_ACCUMULATION /
ZERO_OPTIMIZER /
ZERO_WEIGHT_MUTATION /
DOUBLE_RUN_REPRODUCIBILITY /
PROOF_LEDGER_HOLD_SEALED
```

---

## 29. R13 handoff

R12 leaves the attention-side structural backward graph with canonical outputs ready for later consumers:

```text
dQbase_post_rope → future NeoX backward
dK_shared_post_rope → future NeoX backward
dV_shared → future V projection backward
4 × dDeltaQ → future δQ projector backward
4 × dGate → future gate projector backward
```

The next roadmap patch may close OProj + FFN backward so the temporary GPU dContext fixture can be replaced by the actual decoder upstream gradient.

---

## 30. Bake-time verification status

The bake environment has no `cargo`, `rustc`, `rustfmt`, or `naga` executable.

Therefore the bake-time checks are source/static only:

```text
R11→R12 changed surface = 12 files
R12 policy keys = 23, exactly once in both response files
runtime-config key = exactly once in both response files
new R12 WGSL float-atomic usage = 0
R12 live-path gradient payload readback helpers = 0
changed Rust delimiter scan = PASS
R9→R12 structural seed/init contract comparison = PASS
```

Physical Rust compilation, wgpu WGSL validation, and GPU execution remain `HOLD` until the operator-machine Cargo run.
