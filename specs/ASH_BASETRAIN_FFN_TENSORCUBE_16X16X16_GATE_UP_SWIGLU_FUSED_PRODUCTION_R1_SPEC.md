# `ASH-BASETRAIN-FFN-TENSORCUBE-16X16X16-GATE-UP-SWIGLU-FUSED-PRODUCTION-R1`

## Status

```text
Patch ID
ASH-BASETRAIN-FFN-TENSORCUBE-16X16X16-GATE-UP-SWIGLU-FUSED-PRODUCTION-R1

Parent
ASH-BASETRAIN-FFN-HEADWISE-RGBA4-TEXTURE-RESIDENCY-BRIDGE-R1

Parent packing
FFN_OUTPUT_LANE_RGBA4_R1

Execution role
BaseTrain production

Shadow role
none
```

This revision replaces the Pass160 BaseTrain Gate/Up texture projection plus host-side exact SiLU and SwiGLU multiply sequence with one physical fused Gate/Up/SiLU/SwiGLU compute dispatch. The existing Gate/Up RGBA32F texture population remains the source-preparation pass.

---

## 1. Production authority

BaseTrain forward and real-loss backward recomputation use:

```text
continue_from_external_preoproj_context_prepared_set_tensorcube_fused_production(...)
```

The authoritative BaseTrain callsites are:

```text
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
  2 production callsites

crates/base_train/src/atlas_runtime_real_loss_backward.rs
  2 backward-recompute callsites
```

The Pass160 production method:

```text
continue_from_external_preoproj_context_prepared_set_texture_production(...)
```

is retained as parent/reference code but is no longer called by BaseTrain production.

No legacy Burn Gate/Up fallback is admitted by the fused production method.

---

## 2. Physical execution topology

Canonical runtime topology:

```text
current Gate/Up F32 weight buffers
        |
        v
Pass160 RGBA4 GPU texture population
        |
        +--> Gate Rgba32Float D2Array
        +--> Up   Rgba32Float D2Array
        |
        v
16x16x16 fused production dispatch
        |
        +--> gate_pre
        +--> silu_gate
        +--> up_linear
        +--> ffn_product
        |
        v
existing Down projection
        |
        v
existing residual path
```

The Gate/Up texture population and fused projection are separate compute passes in one WGPU command encoder because the textures transition from storage-write use to sampled `textureLoad` use.

Therefore:

```text
texture population dispatch = 1
Gate+Up+SiLU+SwiGLU fused dispatch = 1
```

The phrase "one fused production dispatch" refers to the Gate/Up projection, exact SiLU and SwiGLU stage, not to weight texture population.

---

## 3. TensorCube geometry

Canonical constants:

```text
M = 16 tokens
N = 16 FFN output scalars
K = 16 hidden scalars
workgroup invocations = 64
```

WGSL:

```text
@workgroup_size(64, 1, 1)
```

Invocation mapping:

```text
row_in_tile      = local_invocation_index / 4
col_vec4_in_tile = local_invocation_index % 4

token    = workgroup_id.y * 16 + row_in_tile
out_vec4 = workgroup_id.x * 4 + col_vec4_in_tile
```

One invocation owns one output `vec4<f32>`, so one workgroup owns:

```text
16 token rows x 4 vec4 columns
= 16 x 16 scalar output tile
```

Dispatch:

```text
workgroups_x = intermediate / 16
workgroups_y = ceil(token_count / 16)
workgroups_z = 1
```

---

## 4. Geometry admission

R1 requires:

```text
hidden > 0
intermediate > 0
hidden % 16 == 0
intermediate % 16 == 0
```

The current target profile satisfies:

```text
d_model = 2048
d_ff    = 5632
```

Sequence length is not assumed to be divisible by sixteen.

The shader performs one entry guard:

```text
if token >= token_count
    return
```

and does not depend on WebGPU OOB robustness for logical tail ownership.

---

## 5. Weight texture authority

The parent texture contract remains unchanged:

```text
format = Rgba32Float
dimension = D2
view = D2Array
array layers = 1
mip level = 0
packing = FFN_OUTPUT_LANE_RGBA4_R1
```

For one K coordinate:

```text
RGBA =
W[out + 0, k]
W[out + 1, k]
W[out + 2, k]
W[out + 3, k]
```

All four channels are numeric weight payload.

No alpha checksum interpretation is admitted.

---

## 6. Numeric texture policy

Required:

```text
textureLoad
integer coordinates
mip 0
non-filterable Rgba32Float
```

Forbidden:

```text
sampler binding
textureSample
textureSampleLevel
normalized UV
linear filtering
sRGB interpretation
```

No hardware texture-cache hit-rate or speedup percentage is claimed by this revision.

---

## 7. K traversal

The fused shader traverses K in blocks of sixteen:

```text
k_block += 16
```

The source contains four explicit groups:

```text
k + 0..3
k + 4..7
k + 8..11
k + 12..15
```

Each scalar input value is shared semantically between Gate and Up accumulation in the same traversal step:

```text
GateAcc = fma(x, GateWeightVec4, GateAcc)
UpAcc   = fma(x, UpWeightVec4,   UpAcc)
```

The current implementation uses scalar input-buffer reads and vec4 weight texture loads. It does not claim an input `array<vec4<f32>>` binding.

---

## 8. Workgroup-state boundary

R1 declares no workgroup storage:

```text
var<workgroup> count = 0
workgroupBarrier count = 0
reported workgroup storage bytes = 0
```

Gate and Up accumulators are invocation-private `vec4<f32>` values.

This is a structural statement only. Register occupancy and hardware stalls remain physical-measurement questions.

---

## 9. Exact SiLU and SwiGLU

The fused shader computes:

```text
SiLU(x) = x / (1 + exp(-x))
```

then:

```text
ffn_product = SiLU(gate_pre) * up_linear
```

No LUT, sampler, interpolation or approximate activation is introduced.

---

## 10. Training tape preservation

The fused dispatch writes four existing training-tape tensors directly:

```text
gate_linear_pre_activation
silu_gate
up_linear
ffn_product
```

These Burn tensors are allocated before dispatch and bridged as strict same-device raw writable storage-buffer leases.

No GPU-to-CPU adoption path is used.

The existing Down projection and analytic backward consume the same semantic tape fields as before.

Thus:

```text
dispatch topology changes
training tape meaning does not change
```

---

## 11. Backward closure

Real-loss backward recomputation is rebound to the same fused production continuation used by forward.

The existing backward chain remains authoritative:

```text
SwiGLU backward
Gate linear backward
Up linear backward
Down linear backward
```

R1 does not change derivative formulas or gradient authority.

---

## 12. LoRA boundary

The current BaseTrain bundle uses no active FFN LoRA composition on this route.

The fused method fail-closes on:

```text
runtime_loras.total_prepared() != 0
trainable_loras not empty
```

Forbidden:

```text
silently ignore LoRA
base-only projection with LoRA present
fallback to legacy Gate/Up route
```

LoRA-effective texture fusion is a separate revision.

---

## 13. Same-device raw leases

The fused continuation requires strict raw F32 leases for:

```text
normalized FFN input
Gate weight
Up weight
gate_pre output
silu_gate output
up_linear output
ffn_product output
```

Canonical bridge evidence:

```text
host uploads = 0
raw borrows >= 7
bytes per element = 4
ActiveTensorHandleState = BorrowedBuffer
BridgeMode = RawBorrowed
```

---

## 14. Failure policy

The fused route fails closed on:

```text
unsupported geometry
wrong dtype
wrong shape
invalid binding range
WGPU validation error
non-empty LoRA state
texture capability failure
pipeline creation failure
```

Forbidden fallback:

```text
fused failure -> legacy Burn Gate/Up
fused failure -> Pass160 old production projection
fused failure -> CPU materialization
```

---

## 15. Physical dispatch receipt

New authority:

```text
BaseTrainFfnTensorCube16x16x16ProductionReceipt
```

It records:

```text
patch identity
packing revision
layer index
weight generation
batch / seq_len / token_count
hidden / intermediate
texture dimensions and bytes
64-thread workgroup identity
16x16x16 macro tile identity
workgroup counts
texture population dispatch count
fused Gate/Up/SiLU/SwiGLU dispatch count
legacy Gate/Up dispatch counts
separate SiLU/SwiGLU dispatch counts
exact SiLU flag
four-tape output count
tail-token evidence
sampler count
workgroup storage bytes
host repack count
D2H byte counts
no-legacy-fallback seal
receipt digest
```

Canonical physical-dispatch counters:

```text
texture_population_dispatch_count = 1
fused_gate_up_swiglu_dispatch_count = 1
legacy_gate_projection_dispatch_count = 0
legacy_up_projection_dispatch_count = 0
separate_silu_dispatch_count = 0
separate_swiglu_dispatch_count = 0
training_tape_output_count = 4
sampler_binding_count = 0
host_weight_repack_count = 0
weight_payload_d2h_bytes = 0
input_payload_d2h_bytes = 0
output_payload_d2h_bytes = 0
```

---

## 16. Compatibility receipt boundary

`LiveDecoderBlockContinuationReceipt` has older counters:

```text
gate_proj_dispatch_count
up_proj_dispatch_count
silu_multiply_dispatch_count
```

Several pre-existing orchestrator validators treat these as logical-stage counters and require value `1`.

R1 preserves those values for compatibility.

They are **not** the physical dispatch authority after this revision.

Physical fused-dispatch truth belongs exclusively to:

```text
BaseTrainFfnTensorCube16x16x16ProductionReceipt
```

This prevents a silent semantic rewrite of historical receipt fields.

---

## 17. BaseTrain layer receipt binding

The existing BaseTrain layer receipt fields remain:

```text
ffn_texture_production_bound = true
ffn_texture_receipt_digest
ffn_texture_pair_bytes
```

The digest now binds the fused TensorCube production receipt. The field name is retained for wire/receipt compatibility because the fused route still depends on the RGBA4 texture production surface.

---

## 18. Resource lifetime

R1 does not yet introduce persistent FFN executor slabs.

Current invocation may still create:

```text
Gate texture
Up texture
texture views
uniform buffers
bind-group layouts
pipeline layouts
shader modules
compute pipelines
bind groups
```

per invocation.

No persistent-reuse claim is made.

---

## 19. Static validator

New validator:

```text
tools/validate_basetrain_ffn_tensorcube_16x16x16_gate_up_swiglu_fused_production_r1_static.py
```

Current baked result:

```text
45 / 45 PASS
```

The validator covers:

```text
patch and packing identity
64-thread workgroup
16x16x16 mapping
all sixteen K lanes
Gate/Up textureLoad
no sampler / no textureSample
exact SiLU
same-shader SwiGLU multiply
four tape outputs
token tail guard
no workgroup storage/barrier
16-divisibility gates
parent population shader reuse
production model method
no host-side SiLU/multiply in new method
LoRA fail-closed
2 forward production callsites
2 backward recompute callsites
old Pass160 BaseTrain callsites retired
legacy generic BaseTrain continuation absent
physical dispatch counters
no D2H / no host repack
no legacy fallback
backend export
no SiLU LUT
```

---

## 20. Parent regression interpretation

Pass159 Local Muon PAD17 static remains unchanged and currently reports:

```text
52 / 52 PASS
```

The historical Pass160 FFN validator currently reports:

```text
23 / 25 PASS
```

with exactly two failed assertions:

```text
production forward callsites
production backward recompute callsites
```

This is an expected supersession result, not a low-level texture-contract regression. Those two assertions require the Pass160 production entrypoint to remain authoritative, which R1 intentionally replaces.

The Pass160 validator is not rewritten to pretend the old route still owns production.

---

## 21. Compile and physical authority

The bake environment used for this revision does not provide:

```text
cargo
rustc
rustfmt
physical WGPU execution
```

Therefore this bake does **not** claim Rust compile PASS or physical GPU parity PASS.

Those judgments remain deferred until the user's local ASH checkout runs them.

---

## 22. Local validation order

```powershell
cd D:\1111113232\DUST\1\ash_pass3

cargo fmt --all -- --check
cargo check -p burn_webgpu_backend --release
cargo check -p model_core --release
cargo check -p base_train --release

python tools\validate_basetrain_ffn_tensorcube_16x16x16_gate_up_swiglu_fused_production_r1_static.py
python tools\validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

The historical Pass160 validator is not a promotion gate for this successor because its two callsite assertions are intentionally superseded.

---

## 23. First physical evidence required

The first local GPU run should establish:

```text
fused Gate/Up/SiLU/SwiGLU dispatch executes
seq_len tails such as 1, 15, 16, 17, 31, 32, 33 remain valid
Gate/Up/SwiGLU outputs remain finite
existing Down consumes ffn_product
existing real-loss backward consumes all four tape tensors
Gate/Up/Down/input gradients remain finite
host payload readback remains zero
legacy fallback remains zero
```

Parity against the Pass160 mathematical reference should be measured in a dedicated harness, not by dual-executing both routes in production.

---

## 24. Performance claim boundary

R1 structurally removes separate production Gate/Up projection and host-side SiLU/SwiGLU stages from the BaseTrain route.

R1 does not yet prove:

```text
GPU speedup percentage
texture-cache hit rate
register occupancy
ALU utilization
stall reduction
```

These require physical timing and profiling evidence.

---

## 25. Packaging closure

The baked code package contains no:

```text
Markdown specs
*.sha256
manifest artifacts
runtime artifacts
```

The overlay contains only the seven changed/new code-validation files for this revision.

The specification is committed separately to GitHub.

---

## 26. Next natural revision

```text
ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1
```

Target:

```text
reuse texture objects where generation permits
reuse texture views
reuse pipeline layouts
reuse compute pipelines
reuse bind groups when exact resource generation matches
reuse uniform/resource slabs
invalidate once on resource-generation replacement
```

This next revision addresses resource churn without changing the fused mathematical contract.

---

## Final seal

```text
Pass160 made RGBA4 texture reads production-capable.

This revision makes one 64-invocation, 16x16x16 kernel the physical
BaseTrain writer for Gate, Up, exact SiLU and SwiGLU product.

The four training-tape tensors remain real GPU tensors and are written
inside that fused dispatch.

Down and backward keep their existing semantic contracts.

No shadow output is produced.
No legacy Gate/Up fallback is available.
No sampler exists.
No activation LUT exists.
No payload round-trip to CPU exists.

The old compatibility counters remain logical counters because changing
their meaning would corrupt historical receipt semantics.
The new fused receipt owns physical-dispatch truth.
```
