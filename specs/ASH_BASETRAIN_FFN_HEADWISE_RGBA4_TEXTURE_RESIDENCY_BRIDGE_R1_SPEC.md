# `ASH-BASETRAIN-FFN-HEADWISE-RGBA4-TEXTURE-RESIDENCY-BRIDGE-R1`

## 1. Status and parent

```text
Patch ID
ASH-BASETRAIN-FFN-HEADWISE-RGBA4-TEXTURE-RESIDENCY-BRIDGE-R1

Code parent
Pass159
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-X-PAD17-WORKGROUP-BANK-CONFLICT-REDUCTION-R1

Design donor
ASH-ATTN-HEADWISE-TEXTURE-01
ASH-ATTN-HEADWISE-TEXTURE-02
ASH-ATTN-HEADWISE-TEXTURE-03
```

This revision adopts the proven Headwise texture-residency pattern for BaseTrain FFN Gate/Up weights and connects it to the **actual BaseTrain production FFN path**.

It is not a shadow observer revision.

```text
production Gate writer = RGBA4 texture projection
production Up writer   = RGBA4 texture projection
legacy Burn Gate matmul in BaseTrain production path = retired
legacy Burn Up matmul in BaseTrain production path   = retired
```

The generic/reference decoder continuation remains available outside the BaseTrain production callsites.

---

## 2. Core authority rule

> The texture is a derived GPU read projection of the current weight. It never becomes weight authority.

Authority remains:

```text
durable checkpoint / active weight source
        -> actual decoder block Gate/Up weight tensors
        -> strict same-device raw leases
        -> derived RGBA32F Gate/Up textures
```

Forbidden inversion:

```text
texture -> checkpoint authority
texture -> optimizer authority
texture -> RAM ResidentWeightPack authority
texture -> weight reconstruction authority
```

Texture failure therefore fails the FFN production invocation closed. It does not relabel or repair weight state.

---

## 3. Headwise pattern reused

The revision reuses these Headwise principles:

```text
same existing WGPU device and queue
strict raw borrowed source leases
GPU-native population
Rgba32Float D2Array texture views
integer textureLoad
mip level 0
non-filtering numeric texture reads
no sampler
no normalized UV
no payload host round-trip
explicit device-limit/capability validation
```

The revision does **not** reuse Headwise KV/session/page-table authority.

```text
Headwise DecodeState KV lifecycle != BaseTrain FFN weight lifecycle
```

---

## 4. Production route closure

The authoritative BaseTrain callsites are rebound from:

```text
continue_from_external_preoproj_context_prepared_set(...)
```

to:

```text
continue_from_external_preoproj_context_prepared_set_texture_production(...)
```

The production rebinding applies to:

```text
Atlas runtime forward wave execution
Atlas runtime real-loss backward recomputation
Wave-resident lane forward execution
Wave-resident lane backward recomputation
```

Required source closure:

```text
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/atlas_runtime_real_loss_backward.rs
```

BaseTrain production must contain zero calls to the legacy continuation entrypoint after this revision.

---

## 5. FFN mathematical boundary

Only the base Gate and Up linear projections change physical implementation.

Unchanged:

```text
post-attention RMSNorm
exact SiLU
SwiGLU multiply
Down projection
FFN residual add
training tape field semantics
SwiGLU backward
Gate linear backward
Up linear backward
Down linear backward
```

The forward tape remains:

```text
gate_linear_pre_activation
silu_gate
up_linear
ffn_product
```

The existing analytic backward consumes those same tensors.

No LUT SiLU is admitted in R1.

---

## 6. Current LoRA boundary

The current R6R6 BaseTrain decoder-block bundle explicitly carries:

```text
PreparedRuntimeLoraSet::empty()
trainable_loras = []
```

R1 therefore fail-closes if Gate/Up texture production is invoked with runtime or trainable LoRA state.

Forbidden:

```text
ignore non-empty LoRA
silently drop LoRA delta
fallback to legacy Burn Gate/Up matmul
```

LoRA-effective texture projection requires a separate explicit revision.

---

## 7. Source layout

Gate and Up are F32 row-major matrices:

```text
Gate [d_ff, d_model]
Up   [d_ff, d_model]
```

Logical scalar:

```text
W[out, k]
```

Source index:

```text
out * d_model + k
```

Current model target:

```text
d_model = 2048
d_ff    = 5632
```

---

## 8. Texture packing

Packing revision:

```text
FFN_OUTPUT_LANE_RGBA4_R1
```

Texture geometry:

```text
width  = d_ff / 4
height = d_model
array layers = 1
format = Rgba32Float
view   = D2Array
```

For the current target:

```text
width  = 1408
height = 2048
```

One texel stores four adjacent output weights for one K coordinate:

```text
RGBA =
W[out + 0, k]
W[out + 1, k]
W[out + 2, k]
W[out + 3, k]
```

The alpha channel is the fourth numeric weight lane.

It is not a checksum channel.

---

## 9. Legacy SFT texture-atlas isolation

The old SFT FFN atlas has different packing semantics, including a parity/checksum-oriented texture layout.

R1 forbids silent reinterpretation of that layout.

```text
legacy input-column packing
!=
FFN_OUTPUT_LANE_RGBA4_R1
```

Forbidden:

```text
RGB3 + alpha checksum -> RGBA4 weights reinterpretation
legacy atlas manifest rewrite
legacy tile coordinates reused under new semantic name
```

---

## 10. Same-device raw lease contract

The production method bridges exactly five live tensors as strict raw borrowed WGPU leases:

```text
normalized FFN input
Gate weight
Up weight
Gate output tensor
Up output tensor
```

Required:

```text
BridgeMode = RawBorrowed
ActiveTensorHandleState = BorrowedBuffer
bytesPerElement = 4
binding window covers exact payload
host upload = 0
```

The Gate/Up output tensors are allocated as Burn tensors first and their GPU buffers are passed directly as writable storage destinations.

Therefore no output adoption copy is required.

---

## 11. GPU population pass

Shader:

```text
crates/burn_webgpu_backend/src/shaders/
base_train_ffn_gate_up_texture_population_output_lane_rgba4.wgsl
```

One invocation owns:

```text
(out_vec4, k)
```

and writes one Gate texel plus one Up texel.

Canonical workgroup:

```text
8 x 8 x 1
```

This population pass is not the later 16x16x16 TensorCube FFN kernel.

---

## 12. Production projection pass

Shader:

```text
crates/burn_webgpu_backend/src/shaders/
base_train_ffn_gate_up_texture_projection_output_lane_rgba4.wgsl
```

One invocation owns:

```text
(token, out_vec4)
```

and accumulates four Gate outputs plus four Up outputs.

For each K:

```text
x = input[token, k]
GateWeights = textureLoad(GateTexture, (out_vec4, k), layer=0, mip=0)
UpWeights   = textureLoad(UpTexture,   (out_vec4, k), layer=0, mip=0)

GateAcc = fma(vec4(x), GateWeights, GateAcc)
UpAcc   = fma(vec4(x), UpWeights,   UpAcc)
```

The pass writes directly to the authoritative production Gate/Up Burn tensor buffers.

---

## 13. Numeric texture policy

Required:

```text
textureLoad = true
integer coordinates = true
mip = 0
Rgba32Float = true
```

Forbidden:

```text
textureSample
textureSampleLevel
sampler binding
normalized UV
linear filtering
sRGB texture format
```

R1 makes no claim that cache hit rate is universally 100%.

R1 makes no guaranteed speedup claim without physical timing receipts.

---

## 14. Direct production output authority

This revision is not shadow.

The texture projection pass is the actual BaseTrain Gate/Up writer.

Receipt truth:

```text
productionGateProjectionCount = 1
productionUpProjectionCount   = 1

legacyBurnGateProjectionCount = 0
legacyBurnUpProjectionCount   = 0
```

A texture capability, population, or projection failure aborts the production continuation.

No legacy Gate/Up fallback is allowed.

---

## 15. Exact SiLU preservation

After texture Gate/Up completion:

```text
gate_pre
   -> existing silu_tensor(gate_pre)
   -> silu_gate

silu_gate * up_linear
   -> ffn_product
```

Thus R1 does not create a forward/backward derivative mismatch.

SiLU LUT remains deferred.

---

## 16. Backward closure

Real-loss backward recomputation uses the same texture production continuation.

Therefore the tensors entering:

```text
r13_swiglu_backward
r13_linear_backward(GATE)
r13_linear_backward(UP)
```

come from the same production Gate/Up implementation used by forward.

No shadow/reference Gate/Up tensor is substituted into the training tape.

---

## 17. Texture capability gate

Before submission the implementation validates:

```text
texture width <= max_texture_dimension_2d
texture height <= max_texture_dimension_2d
array layers >= 1
Rgba32Float storage texture creation
Rgba32Float non-filterable sampled binding creation
population pipeline validation
projection pipeline validation
```

Validation uses WGPU error scopes.

Failure is fail-closed.

---

## 18. Current texture footprint

For d_model 2048 and d_ff 5632:

```text
one texture
1408 * 2048 * 16 bytes
= 46,137,344 bytes
= 44 MiB

Gate + Up
= 92,274,688 bytes
= 88 MiB
```

R1 holds the pair for the live production invocation and does not promote all-layer permanent residency.

All-layer blind residency remains forbidden.

---

## 19. Resource-lifetime boundary

R1 prioritizes route correctness and physical adoption over persistent allocation reuse.

Current implementation creates the Gate/Up texture pair and the associated production pipelines/bind groups inside the production invocation.

This is intentionally visible as remaining resource churn.

It must not be misreported as persistent slab reuse.

A later FFN resource-slab revision may lift:

```text
texture objects
views
pipeline layouts
pipelines
bind groups
uniform slabs
```

into an executor-owned reusable generation.

---

## 20. Relation to Pass160

Pass160 remains the Local Muon executor resource-slab revision and is not silently repurposed.

FFN resource reuse receives its own later revision.

This prevents Muon optimizer-state work and FFN forward execution from sharing accidental resource authority.

---

## 21. Production receipt

Backend receipt:

```rust
BaseTrainFfnRgba4TextureProductionReceipt
```

Required fields include:

```text
patchId
packingRevision
layerIndex
weightGeneration
batch
seqLen
tokenCount
hidden
intermediate
textureWidth
textureHeight
textureArrayLayers
Gate texture bytes
Up texture bytes
pair texture bytes
same-device raw source
two-pass dispatch counts
sampler binding count
host weight repack count
weight payload D2H count
production Gate/Up counts
legacy Burn Gate/Up counts
receipt digest
```

---

## 22. BaseTrain layer receipt binding

`AtlasRuntimeForwardLayerReceipt` records:

```text
ffnTextureProductionBound = true
ffnTextureReceiptDigest
ffnTexturePairBytes
```

This makes the production route observable in normal forward receipts rather than only in a standalone diagnostic harness.

---

## 23. Host movement prohibition

PASS requires:

```text
hostWeightRepackCount = 0
weightPayloadD2HCount = 0
```

The implementation may create tiny uniform parameter buffers on the host.

That does not constitute weight payload movement.

---

## 24. Forbidden fallback

Forbidden:

```text
texture validation failure -> Burn Gate/Up matmul
raw lease failure -> CPU materialization
shape mismatch -> generic matmul
unsupported format -> host-packed texture upload
LoRA present -> ignore LoRA and continue
```

Every case fails closed.

---

## 25. Static validation

New validator:

```text
tools/validate_basetrain_ffn_headwise_rgba4_texture_residency_bridge_r1_static.py
```

It verifies at minimum:

```text
patch identity
RGBA32F D2Array contract
output-lane RGBA4 packing
alpha-as-weight semantics
integer textureLoad
no sampler
no textureSample
production method presence
BaseTrain forward production rebinding
BaseTrain backward recompute rebinding
legacy BaseTrain continuation retirement
exact SiLU retention
training tape retention
LoRA fail-closed guards
backend module export
no SiLU LUT
zero host repack/D2H declarations
legacy Gate/Up projection counts zero
```

Current baked static result:

```text
25 / 25 PASS
```

---

## 26. Parent regression gate

Pass159 Local Muon static validator must remain green because the FFN production bridge does not alter Local Muon geometry or optimizer semantics.

Current baked result:

```text
Pass159 static
52 / 52 PASS
```

---

## 27. Compile authority

The bake environment used to produce this revision does not contain `cargo` or `rustc`.

Therefore:

```text
Rust compile = not established by bake environment
physical WGPU execution = not established by bake environment
```

The user's local ASH checkout remains compile and physical execution authority.

No compile PASS is claimed without that evidence.

---

## 28. Validation order on the user machine

```powershell
cd D:\1111113232\DUST\1\ash_pass3

cargo fmt --all -- --check
cargo check -p burn_webgpu_backend --release
cargo check -p model_core --release
cargo check -p base_train --release

python tools\validate_basetrain_ffn_headwise_rgba4_texture_residency_bridge_r1_static.py
python tools\validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

N8 is not required for this patch's first validation.

---

## 29. Required first physical evidence

The first physical BaseTrain run must establish:

```text
ffnTextureProductionBound = true
Gate/Up texture receipt digest present
productionGateProjectionCount = 1
productionUpProjectionCount = 1
legacyBurnGateProjectionCount = 0
legacyBurnUpProjectionCount = 0
hostWeightRepackCount = 0
weightPayloadD2HCount = 0
final hidden finite
real-loss backward receives Gate/Up tape without error
```

No speedup percentage is claimed before GPU timing is measured.

---

## 30. Non-goals

R1 does not implement:

```text
16x16x16 fused Gate+Up+SwiGLU kernel
SiLU LUT
Down texture projection
persistent FFN texture slot ring
multi-layer texture residency
async overlap
GPU timestamp attribution
LoRA effective texture composition
```

These remain separate revisions.

---

## 31. Next natural revision

```text
ASH-BASETRAIN-FFN-TENSORCUBE-16X16X16-GATE-UP-SWIGLU-FUSED-PRODUCTION-R1
```

Because R1 already makes texture Gate/Up production-active, the next revision does not need a shadow detour unless physical parity exposes a correctness problem.

Its job is to collapse:

```text
texture Gate/Up projection
exact SiLU
SwiGLU multiply
```

into the 16x16x16 specialized production kernel while preserving the same training tape semantics.

---

## 32. Final seal

```text
This revision does not ask whether the FFN texture path could work.

It makes the BaseTrain production Gate and Up projections use it.

The current Gate and Up tensors remain the source authority.
Their strict same-device raw buffers populate two Rgba32Float D2Array textures.
Each RGBA texel contains four adjacent output weights at one K coordinate.
The production projection kernel reads those textures with integer textureLoad and writes directly into the Burn Gate/Up output tensor buffers.

There is no sampler.
There is no normalized UV.
There is no host repack.
There is no weight payload readback.
There is no legacy Burn Gate/Up fallback inside BaseTrain production.

Exact SiLU remains exact.
The existing SwiGLU training tape remains intact.
The existing backward consumes the texture-produced Gate/Up values.

The texture is a window onto the current weight, not a second weight authority.
```
