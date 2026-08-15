# ASH-BASETRAIN-QK-RMSNORM-ATTENTION-STABILITY-R1

## Status

Implementation-aligned attention-stability authority layered on top of the current Pass146 BaseTrain source tree.

This R1 changes the Q/K activation path only. It does not change AdamW mathematics, TensorCube Local-Muon routing, V projection semantics, O projection semantics, attention temperature/scale, or persistent optimizer-state ownership.

## Patch identity

```text
ASH-BASETRAIN-QK-RMSNORM-ATTENTION-STABILITY-R1
```

## Core contract

```text
Per-Head Q RMSNorm /
Per-KV-Head K RMSNorm /

Head-Dim-64 Normalization Authority /
No Whole-Hidden QK Normalization /

Q/K Projection Output Normalization /
Attention-Logit Scale Stabilization /

Existing RMSNorm Kernel Reuse /
Explicit QK RMSNorm Backward /

No V Normalization /
No O-Projection Normalization /

No Weight-Space QK Clipping /
No MuonClip Equivalence Claim /

AdamW / Local-Muon Optimizer Independence /

Per-Layer Max Attention Logit Receipt /
Per-Layer Mean·RMS Attention Logit Receipt /
Q RMS / K RMS Health Ledger /

No Silent Epsilon Substitution /
No Silent F32/BF16 Precision Change /

KL Correlation Observability /
No KL-Causality Claim
```

## 1. Graph authority

When admitted, the forward graph is exactly:

```text
Q projection → Q per-head RMS64 ─┐
                                 ├→ RoPE → existing attention
K projection → K per-KV RMS64 ──┘
V projection ─────────────────────→ existing attention
```

The normalization occurs after Q/K projection and before RoPE.

The backward graph is the exact reverse dependency order:

```text
attention backward
→ RoPE backward
→ Q/K RMSNorm backward
→ q_proj / k_proj backward
```

`dQ` or `dK` from the post-RoPE attention path must never bypass the QK-RMSNorm backward stage when this authority is admitted.

## 2. Geometry authority

Current model binding:

```text
hidden_size = 2048
Q heads     = 32
KV heads    = 4
head_dim    = 64
```

R1 normalizes only the 64-element head dimension.

Q domain:

```text
Q[b, token, q_head, 0..63]
```

K domain:

```text
K[b, token, kv_head, 0..63]
```

Whole-hidden Q normalization and whole-KV-width K normalization are forbidden.

A `head_dim` other than 64 fails closed in this R1.

## 3. Non-affine RMSNorm

QK-RMSNorm introduces no trainable gamma or beta.

Forward mathematics per 64-element head vector:

```text
mean_square = sum(x_i^2) / 64
inv_rms     = 1 / sqrt(mean_square + epsilon)
y_i         = x_i * inv_rms
```

Therefore:

```text
new trainable QK tensor count = 0
new QK optimizer-state count  = 0
```

## 4. Explicit epsilon authority

R1 binds QK-RMSNorm epsilon explicitly to the canonical model RMSNorm epsilon:

```text
epsilonSource = MODEL_RMSNORM_EPSILON
```

The exact F32 epsilon bits are receipt- and checkpoint-bound.

R1 does not silently invent a second epsilon and does not silently change epsilon on resume.

## 5. Precision authority

The current implementation is F32-only for this QK-RMSNorm path.

No BF16/F16 path is silently selected for normalization, reduction, backward, or logit telemetry.

A later reduced-precision QK-RMSNorm path requires separate admission and physical evidence.

## 6. Q/K forward implementation

The backend provides a dedicated 64-wide Q/K forward primitive:

```text
rmsnorm64_forward
```

with one 64-invocation workgroup per Q or K head vector.

It computes:

- normalized output;
- inverse RMS;
- raw RMS health;
- finite status.

The Q and K forward dispatches are submitted without an unnecessary host wait between them.

## 7. Existing RMSNorm backward reuse

R1 does not add a second bespoke QK backward formula in WGSL.

Instead, the Q/K backward path reuses the existing R14 RMSNorm backward authority through:

```text
r14_rmsnorm_backward(...)
```

with an explicit non-trainable 64-element all-ones gamma lease.

This preserves the existing RMSNorm backward mathematics and nonfinite diagnostics while keeping QK-RMSNorm non-affine.

The resulting dgamma is not promoted to trainable state.

## 8. No V/O normalization

R1 requires:

```text
Q normalized = true
K normalized = true
V normalized = false
O normalized = false
```

V remains the existing attention value input.

The attention output and O projection remain unchanged.

## 9. Existing attention scale preservation

QK-RMSNorm does not remove or rewrite the existing attention scaling authority.

Attention remains:

```text
logit = dot(Q_normalized_after_RoPE, K_normalized_after_RoPE)
        × existing_attention_scale
```

Any mutation of the existing attention scale belongs to a separate patch authority.

## 10. GQA semantics preservation

The existing 32-Q-head / 4-KV-head mapping is unchanged.

QK-RMSNorm normalizes each Q head and each KV K head independently and does not alter replication/grouping semantics.

## 11. No weight-space clipping

This R1 is activation-side Q/K normalization only.

Forbidden:

```text
Wq *= clip_scale
Wk *= clip_scale
```

The implementation records zero Q/K weight-clip authority.

## 12. No MuonClip equivalence claim

QK-RMSNorm and weight-space QK clipping are different mechanisms.

R1 explicitly does not claim equivalence to MuonClip or another QK-Clip method.

## 13. Optimizer independence

QK-RMSNorm is a model forward/backward graph authority, not an optimizer routing authority.

It is independent from:

- all-AdamW BaseTrain;
- RAM-resident Adam M/V;
- PCIe-overlapped Adam M/V transfer;
- TensorCube Local-Muon eligibility;
- future Local-Muon/AdamW hybrid materialization.

No Adam M/V or Muon momentum ownership changes in this patch.

## 14. Attention-logit observability

Per layer, R1 computes compact post-RoPE attention-logit health using the same causal/GQA addressing and existing attention scale as the real attention path.

The compact ledger includes:

```text
min
max
absolute max
mean
RMS
count
nonfinite status
```

The full attention matrix is never read back to the host for this receipt.

## 15. Q/K RMS health

Per layer, R1 records compact Q and K health including raw RMS and normalized-state finite evidence.

The receipt surface is intended to expose whether Q/K vector magnitude pressure is reduced before it reaches attention logits.

## 16. Compact readback authority

R1 does not map compute STORAGE buffers directly.

Compute/storage buffers use GPU-compatible STORAGE/COPY usage.

Dedicated readback staging uses:

```text
MAP_READ | COPY_DST
```

Q and K norm health/status are combined into one staging readback.

Attention-logit summary/status are combined into one staging readback.

Therefore the current forward health path uses two compact map-read operations per layer rather than mapping raw Q/K or attention payloads.

Raw attention payload readback remains zero.

## 17. Per-layer receipt binding

QK-RMSNorm health is attached to the existing per-layer forward-wave receipt stream.

The layer receipt carries:

```text
qk_rmsnorm_admitted
qk_rmsnorm_health
```

The health object includes geometry, epsilon identity, normalization flags, attention-scale identity, Q/K health, logit health, nonfinite evidence, compact-readback accounting, and KL-correlation claim boundaries.

## 18. Backward receipt binding

Backward layer receipts include:

```text
qk_rmsnorm_backward_count
qk_rmsnorm_backward_nonfinite_count
```

The count is explicit evidence that Q/K RMSNorm backward was not bypassed.

## 19. KL correlation boundary

The current BaseTrain source tree does not expose a canonical KL metric in this execution path.

R1 therefore explicitly records the distinction:

```text
klCorrelationObservable = true
klValuePresent          = false
klValueSynthesized      = false
klCausalityClaimed      = false
```

This means the QK health ledger is designed to be joined with a canonical KL authority if/when such a metric is available at the same training epoch.

R1 never invents a KL value and never claims that prior KL instability was caused by Q/K magnitude.

## 20. No diagnostic synthesis

If a value or metric was not physically observed, it is not created from inference.

In particular:

- no fabricated KL value;
- no fabricated raw-attention payload;
- no inferred MuonClip event;
- no inferred weight clipping;
- no silent nonfinite repair.

## 21. Packed-state semantic binding

QK-RMSNorm changes model execution semantics even though it adds no trainable tensor.

The packed runtime state manifest therefore binds:

```text
qkRmsnormAttentionStabilityAdmitted
qkRmsnormEpsilonBits
```

Legacy packed manifests deserialize these new fields as:

```text
false
0
```

so old physical parents remain readable without silently claiming QK-RMSNorm admission.

## 22. Resume semantics

Resume rules are explicit:

```text
source QK OFF → requested QK OFF
  allowed

source QK OFF → explicit requested QK ON
  allowed as an explicit new semantic lineage transition

source QK ON → requested QK ON
  allowed only when epsilon bits match exactly

source QK ON → requested QK OFF
  forbidden
```

The forbidden downgrade fails closed rather than silently changing forward semantics.

## 23. Admission flag

Runtime admission is explicit:

```text
--admit-qk-rmsnorm-attention-stability
```

Without this flag the existing Q/K projection → RoPE → attention path remains the authority.

## 24. Route preflight

When admitted, preflight requires:

```text
head_dim == 64
model RMSNorm epsilon finite
model RMSNorm epsilon > 0
```

Failure is closed before training execution.

## 25. Structural validator

R1 adds:

```text
tools/validate_qk_rmsnorm_attention_stability_static.py
```

It verifies, among other things:

- exact head-dim 64 authority;
- per-Q-head and per-KV-head normalization;
- non-affine behavior;
- existing R14 backward reuse;
- no duplicate QK backward shader;
- forward placement before RoPE;
- reverse backward placement after RoPE backward;
- V/O preservation;
- attention-scale preservation;
- no weight clipping/MuonClip equivalence;
- dedicated MAP_READ staging;
- compact logit/RMS telemetry;
- no raw attention payload readback;
- no silent reduced precision;
- KL value non-synthesis;
- packed-state semantic binding;
- QK-ON resume downgrade rejection;
- CF1 registration.

## 26. CF1 binding

The QK-RMSNorm validator is registered in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

This source-tree change invalidates older CF1 source-tree digests. A fresh local CF1 receipt is required before physical BaseTrain execution.

## 27. Bake-time static evidence

The bake environment produced the following static evidence:

```text
QK RMSNorm                    96/96 PASS
First-Candidate Registry      92/92 PASS
TensorCube Local Muon        101/101 PASS
N8 Long Horizon               70/70 PASS
Storage Root                  39/39 PASS
Scheduler Extension           23/23 PASS
Subgroup32 AdamW              36/36 PASS
R14                           52/52 PASS
```

RAM-resident Adam M/V and Adam M/V PCIe-overlap validators also remained PASS in the bake workspace.

Of the 18 Python validators registered by the full CF1 script, 12 were runnable and passed in the slim bake workspace. Six validators could not be executed because the intentionally slim parent archive does not contain the repository `specs/cli/*.args` contract fixtures required by those validators.

Those six are **not claimed as PASS** by this spec. The user's full local repository and fresh CF1 execution remain the compile/closure authority.

The bake environment did not contain a Rust/Cargo/WGPU physical toolchain, so no Rust compile, shader physical execution, or BaseTrain physical PASS is claimed here.

## 28. Structural PASS

Reserved structural token:

```text
PASS_ASH_BASETRAIN_QK_RMSNORM_ATTENTION_STABILITY_STRUCTURAL_R1
```

It means only that the Q/K RMS64 graph, explicit backward, semantic bindings, and telemetry surfaces are structurally present and statically validated.

## 29. Physical PASS boundaries

The following require physical GPU evidence and are not claimed by this bake:

```text
PASS_ASH_BASETRAIN_QK_RMSNORM_ATTENTION_FORWARD_BACKWARD_PHYSICAL_R1
PASS_ASH_BASETRAIN_QK_RMSNORM_ATTENTION_LOGIT_STABILITY_OBSERVED_R1
```

The second token additionally requires an actual baseline comparison showing reduced attention-logit pressure.

## 30. HOLD frontier

Until physical forward/backward and baseline comparison are complete:

```text
HOLD_ASH_BASETRAIN_QK_RMSNORM_PHYSICAL_BASELINE_COMPARISON_NOT_YET_ADMITTED
```

Even a successful comparison does not automatically promote QK-RMSNorm to the canonical model line.

Production promotion remains separately held.

## 31. Non-goals

R1 does not add:

- V normalization;
- O normalization;
- learned QK gamma/beta;
- weight-space Q/K clipping;
- MuonClip;
- QK-Clip equivalence;
- learned attention temperature;
- softmax replacement;
- changed attention scale;
- BF16/F16 QK normalization;
- fused projection+QK-Norm kernels;
- canonical production promotion.

## SSOT seal

```text
Q NORM DOMAIN            = one Q head × 64
K NORM DOMAIN            = one KV head × 64
WHOLE-HIDDEN QK NORM     = forbidden

FORWARD ORDER            = projection → QK RMS64 → RoPE → attention
BACKWARD ORDER           = attention backward → RoPE backward → QK RMS backward → projection backward

QK RMSNORM               = non-affine
NEW TRAINABLE PARAMETER  = none
EPSILON                  = explicit model RMSNorm epsilon, exact F32 bits
PRECISION                = current F32 authority, no silent reduced precision

V                         = unchanged
O                         = unchanged
ATTENTION SCALE           = unchanged
Q/K WEIGHT CLIP           = none
MUONCLIP EQUIVALENCE      = not claimed

OPTIMIZER DEPENDENCY      = none

HEALTH RECEIPT            = Q/K RMS + attention min/max/absMax/mean/RMS/count
RAW ATTENTION READBACK    = 0
KL VALUE                  = absent unless a canonical source exists
KL SYNTHESIS              = forbidden
KL CAUSALITY              = not claimed

CHECKPOINT SEMANTICS      = QK admission + epsilon bits bound
QK-ON → QK-OFF RESUME     = forbidden

CURRENT ADAMW/MUON ROUTING= unchanged
PHYSICAL PASS             = not yet claimed
CANONICAL PROMOTION       = not admitted
```
