# `ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1`

## Status

```text
Patch ID
ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1

Parent
ASH-BASETRAIN-FFN-TENSORCUBE-16X16X16-GATE-UP-SWIGLU-FUSED-PRODUCTION-R1

Execution role
BaseTrain production resource lifetime authority

Mathematical contract
unchanged from fused production parent
```

This revision keeps the existing 16x16x16 Gate/Up/exact-SiLU/SwiGLU production math and moves resource ownership from per-FFN-call construction to a route-owned persistent executor.

The revision also repairs the FFN weight-generation binding used for texture-content eligibility. A layer ordinal is not a weight generation.

---

## 1. Primary objective

Parent execution rebuilt the following resources for each FFN invocation:

```text
Gate texture
Up texture
Gate texture view
Up texture view
population uniform buffer
fused uniform buffer
population/fused bind-group layouts
population/fused pipeline layouts
population/fused shader modules
population/fused compute pipelines
population/fused bind groups
```

R1 changes the lifetime model to:

```text
route lifetime
    -> persistent pipeline slab
    -> persistent one-pair RGBA4 texture slot
    -> persistent static texture bind groups
    -> persistent uniform buffers

invocation lifetime
    -> Gate/Up source bind group
    -> input/tape output bind group
```

The optimized object lifetime must not become a second model-state authority.

---

## 2. Weight-generation SSOT repair

The parent fused callsites used:

```text
u64::from(layer)
```

as the value passed into the `weight_generation` parameter.

That value is a layer ordinal, not a weight-generation authority.

R1 removes that binding from the FFN production path.

Canonical runtime generation source for wave-resident BaseTrain execution:

```text
ResidentWeightPack::generation()
```

If no resident pack is present but the VRAM hot-weight cache exists:

```text
GpuWeightPageCache::active_generation()
```

The resulting value is passed into:

```text
prepare_atlas_wave_00_runtime_transaction(..., source_weight_generation)
    -> BaseTrainAtlasWaveGenerationFence.source_weight_generation
    -> FFN production callsite
    -> persistent texture content key
```

Standalone preflight/diagnostic route construction may explicitly pass generation `0`. Such a route does not claim post-optimizer generation identity.

---

## 3. Legacy receipt preservation

`AtlasRuntimeForwardLayerReceipt.weight_generation` is an older field whose current runtime semantics are tied to layer progression.

R1 does not silently reinterpret it.

A new field is published:

```text
ffn_source_weight_generation
```

Canonical distinction:

```text
weight_generation
    legacy compatibility field

ffn_source_weight_generation
    FFN texture-content generation authority
```

---

## 4. Route-owned executor

New backend owner:

```rust
BaseTrainFfnTensorCubePersistentExecutor
```

The route context owns:

```rust
Arc<BaseTrainFfnTensorCubePersistentExecutor>
```

through:

```text
AtlasRuntimeRouteAdmissionContext.ffn_tensorcube_executor
```

The executor is constructed once when the route-admission context is prepared.

Forbidden:

```text
process-global OnceLock executor
cross-run texture cache
cross-device resource cache
cross-route implicit reuse
```

Route destruction retires the executor and its GPU resources.

---

## 5. Device and queue seal

Executor construction binds exact runtime handles:

```text
Arc<BackendDevice>
Arc<BackendQueue>
```

Every production invocation checks:

```text
Arc::ptr_eq(executor.device, invocation.device)
Arc::ptr_eq(executor.queue, invocation.queue)
```

A mismatch fails closed.

No adapter/device/queue recreation is admitted.

---

## 6. Persistent physical texture slot

Canonical slot count:

```text
1
```

The slot owns:

```text
Gate Rgba32Float D2Array texture
Up Rgba32Float D2Array texture
Gate D2Array view
Up D2Array view
```

Current model geometry:

```text
d_model = 2048
d_ff    = 5632
texture width  = 1408
texture height = 2048
```

Current pair size:

```text
Gate = 44 MiB
Up   = 44 MiB
Pair = 88 MiB
```

R1 does not allocate one pair per transformer layer.

---

## 7. Allocation identity versus content identity

The physical texture object and the weight content stored inside it are separate state domains.

```text
texture allocation generation
!=
weight content generation
```

Changing layer, source weight generation, tensor set or source-buffer identity does not automatically recreate the physical textures.

Instead:

```text
same physical texture pair
    -> content becomes ineligible
    -> GPU repopulation
    -> new content key sealed
```

---

## 8. Texture content key

Canonical content key binds:

```text
model source digest
model spec ID
tensor set digest
layer index
source weight generation
Gate source identity digest
Up source identity digest
packing revision
```

Packing revision remains:

```text
FFN_OUTPUT_LANE_RGBA4_R1
```

Gate/Up source identity digests bind at least:

```text
primitive ID
stream ID
buffer offset
buffer binding size
payload length
shape
bytes per element
```

Debug labels alone are never source authority.

---

## 9. Exact cache-hit rule

Population may be skipped only when:

```text
existing sealed content key
==
requested content key
```

Equality covers the entire key, not only `source_weight_generation`.

Therefore these are cache misses:

```text
same generation + different layer
same generation + different tensor set
same generation + different Gate primitive
same generation + different Up primitive
same generation + different source range
same generation + different packing revision
```

No metadata relabeling is permitted.

---

## 10. Content-hit behavior

On exact content hit:

```text
texture population dispatch = 0
population dynamic bind group creation = 0
physical texture allocation = 0
texture view creation = 0
pipeline creation = 0
static bind-group creation = 0
```

The fused production dispatch still executes against the persistent texture pair.

---

## 11. Content-miss behavior

On content miss:

```text
physical Gate/Up texture objects remain allocated
Gate/Up source dynamic bind group is created
GPU population pass rewrites the existing pair
new content key becomes current
fused production dispatch executes
```

Initial population and repopulation are distinguished in the resource receipt.

```text
texture_content_initial_population_count
texture_content_repopulation_count
```

---

## 12. Persistent pipeline slab

Executor construction creates and retains:

```text
population static BGL
population dynamic BGL
fused static BGL
fused dynamic BGL

population pipeline layout
fused pipeline layout

population shader module / pipeline
fused shader module / pipeline
```

Pipeline compilation is outside the production `execute()` hot path.

---

## 13. Persistent uniform slab

Persistent buffers:

```text
PopulationParams uniform
FusedParams uniform
```

`PopulationParams` contains geometry that is fixed for the executor:

```text
hidden
intermediate
```

`FusedParams.token_count` changes per invocation and is updated through a small:

```text
queue.write_buffer
```

This control write is not classified as tensor payload movement.

---

## 14. Static and dynamic bind-group split

### Population pass

Persistent group 0:

```text
PopulationParams
Gate storage texture
Up storage texture
```

Invocation group 1:

```text
Gate source weight buffer
Up source weight buffer
```

### Fused pass

Persistent group 0:

```text
FusedParams
Gate sampled texture
Up sampled texture
```

Invocation group 1:

```text
normalized FFN input
gate_pre output
silu_gate output
up_linear output
ffn_product output
```

---

## 15. Why dynamic bind groups are not cached

R1 intentionally does not retain dynamic source/output bind groups.

A cached population-source bind group could keep streamed Gate/Up weight buffers alive beyond their residency authority.

A cached fused-I/O bind group could keep old input and training-tape buffers alive beyond their invocation lifetime.

Forbidden:

```text
persistent old Gate/Up source binding
persistent old FFN input binding
persistent gate_pre/silu_gate/up_linear/product binding
```

The optimization must not create VRAM zombie ownership.

---

## 16. Shader split

New persistent population shader:

```text
crates/burn_webgpu_backend/src/shaders/
base_train_ffn_tensorcube_persistent_population_output_lane_rgba4.wgsl
```

New persistent fused shader:

```text
crates/burn_webgpu_backend/src/shaders/
base_train_ffn_tensorcube_persistent_gate_up_swiglu_fused_production.wgsl
```

The mathematical implementation remains the parent 16x16x16 kernel.

---

## 17. Parent fused math preservation

Required unchanged properties:

```text
@workgroup_size(64, 1, 1)
M = 16
N = 16
K = 16

row_in_tile = lid / 4
col_vec4_in_tile = lid % 4

integer textureLoad
Gate and Up same K traversal
exact SiLU using exp
SwiGLU multiply in the fused shader
explicit token-tail guard
no workgroupBarrier
no workgroup storage
```

No SiLU LUT is introduced.

---

## 18. Four-tape preservation

The fused production shader continues to write:

```text
gate_pre
silu_gate
up_linear
ffn_product
```

The existing Down projection and analytic backward remain unchanged.

Resource-lifetime optimization does not authorize training-tape compression or recomputation.

---

## 19. Serialization boundary

The single physical texture slot and shared fused-parameter buffer are protected by executor-owned state serialization.

Canonical implementation:

```text
Mutex<PersistentState>
```

The guarded region covers:

```text
content-key check
optional population bind-group construction
FusedParams write
command encoding
queue submission
content-state publication
```

This prevents a second CPU invocation from repopulating the slot while another invocation is preparing to consume it.

---

## 20. Queue ordering and blocking-poll retirement

Pipeline/resource capability validation is performed once during executor construction under a WebGPU validation error scope.

The production `execute()` path contains no:

```text
device.push_error_scope
device.poll(PollType::Wait)
```

The same queue lineage is used for population and fused consumption, preserving submission order without a per-FFN blocking device poll.

Canonical steady-state counter:

```text
hot_path_blocking_poll_count = 0
```

---

## 21. Production callsite closure

BaseTrain forward has two production callsites and real-loss backward recomputation has two callsites.

All four continue to use:

```text
continue_from_external_preoproj_context_prepared_set_tensorcube_fused_production
```

The model method now receives:

```text
persistent executor
tensor set digest
layer index
source weight generation
```

and delegates physical execution to:

```text
BaseTrainFfnTensorCubePersistentExecutor::execute
```

No shadow route is introduced.

---

## 22. Wave-resident generation derivation

`execute_r6a_r1_wave_resident_accumulation_step` derives the source generation before route creation.

Canonical precedence:

```text
ResidentWeightPack present
    -> resident.generation()

else VRAM hot cache present
    -> cache.active_generation()

else
    -> 0 baseline
```

The resulting value is sealed into the runtime transaction generation fence and reused consistently by forward and backward within the step.

---

## 23. Resource receipt

New receipt:

```text
BaseTrainFfnTensorCubePersistentResourceReceipt
```

It records at least:

```text
executor generation
source weight generation
layer index
pipeline slab build/reuse counts
texture allocation/view creation counts
texture slot count and bytes
content hit/miss counts
content population count
initial population count
repopulation count
population skip count
static bind-group creation/reuse counts
dynamic population/fused bind-group creation counts
uniform-buffer creation count
uniform parameter write count
hot-path error-scope count
hot-path blocking-poll count
stale-texture reuse count
source-weight bind-group cache count
training-tape bind-group cache count
host weight repack count
weight D2H bytes
content-key digest
receipt digest
```

---

## 24. Forward layer receipt integration

`AtlasRuntimeForwardLayerReceipt` adds:

```text
ffn_source_weight_generation
ffn_persistent_resource_receipt_digest
ffn_texture_population_skipped
ffn_static_bind_group_reused
```

Existing:

```text
ffn_texture_production_bound
ffn_texture_receipt_digest
ffn_texture_pair_bytes
```

remain present.

---

## 25. First-use expected resource state

First executor use:

```text
pipeline slab build receipt = 1
texture allocation creation = 2
texture view creation = 2
static bind-group creation = 2
uniform-buffer creation = 2
content miss = 1
initial population = 1
population dispatch = 1
fused dispatch = 1
```

The physical resources were created at route-executor construction; the first invocation reports that cold initialization once.

---

## 26. Warm same-content expected state

Exact same content key:

```text
pipeline creation = 0
texture creation = 0
view creation = 0
static BG creation = 0
content hit = 1
population skip = 1
population dispatch = 0
fused dispatch = 1
```

---

## 27. Different-layer expected state

With the canonical one-slot policy:

```text
layer N
-> layer N+1
```

is a content miss because layer identity and source primitive identity change.

Expected:

```text
texture allocation = reused
static BG = reused
pipeline slab = reused
content repopulation = 1
stale reuse = 0
```

R1 therefore primarily removes resource-construction churn across normal layer traversal. It does not claim every layer is a texture-content hit.

---

## 28. Generation transition expected state

Same layer, new source generation:

```text
G -> G+1
```

must produce:

```text
content hit = 0
same physical texture allocation retained
repopulation = 1
old-generation consumption = 0
```

No texture object recreation is required solely because content generation changed.

---

## 29. No host movement

PASS requires:

```text
host_weight_repack_count = 0
weight_payload_d2h_bytes = 0
input_payload_d2h_bytes = 0
output_payload_d2h_bytes = 0
```

Gate/Up texture population remains same-device GPU work.

---

## 30. No legacy fallback

Persistent executor failure does not authorize:

```text
legacy Burn Gate projection
legacy Burn Up projection
old Pass160 projection route
CPU FFN projection
host-packed texture upload
```

The production call fails closed.

---

## 31. Static validator

New validator:

```text
tools/validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py
```

Current baked result:

```text
66 / 66 PASS
```

It verifies, among other things:

```text
route-owned executor
no global singleton
actual generation parameterization
resident-pack generation derivation
VRAM cache generation derivation
content-key identity fields
one texture slot
persistent textures/views/pipelines/uniforms
static/dynamic BG split
exact content-hit equality
population skip on hit
same allocation reuse on miss
pipeline/texture creation outside execute()
no hot-path error scope
no hot-path blocking poll
same-device/queue seal
mutex slot serialization
exact SiLU and four-tape preservation
four BaseTrain production/recompute callsites
no dynamic source/tape BG cache
no payload D2H
no host repack
no legacy fallback
```

---

## 32. Parent regression gates

Current baked static results:

```text
ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1
66 / 66 PASS

ASH-BASETRAIN-FFN-TENSORCUBE-16X16X16-GATE-UP-SWIGLU-FUSED-PRODUCTION-R1
45 / 45 PASS

ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-X-PAD17-WORKGROUP-BANK-CONFLICT-REDUCTION-R1
52 / 52 PASS
```

The historical Pass160 FFN texture-bridge validator remains superseded at its two old production-callsite assertions and is not promoted back to authority.

---

## 33. Compile and physical authority

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU device execution
```

Therefore:

```text
Rust compile PASS = not established
physical GPU PASS = not established
performance improvement = not established
```

No fabricated compile or speedup claim is made.

---

## 34. Local validation order

```powershell
cd D:\1111113232\DUST\1\ash_pass3

cargo fmt --all -- --check
cargo check -p burn_webgpu_backend --release
cargo check -p model_core --release
cargo check -p base_train --release

python tools\validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_16x16x16_gate_up_swiglu_fused_production_r1_static.py
python tools\validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

N8 is not required as the first promotion gate for this resource-lifetime patch.

---

## 35. First physical evidence required

The first physical run should establish:

```text
route executor initializes successfully
first FFN use reports cold resource creation once
later layers report pipeline/texture/static-BG reuse
layer transitions repopulate the existing texture pair
same-content repeated invocation skips population
source-generation change cannot hit stale content
hot-path blocking poll remains zero
forward fused output remains finite
real-loss backward consumes the unchanged four tapes
no payload D2H occurs
no legacy fallback occurs
```

---

## 36. Non-goals

R1 does not implement:

```text
all-layer texture cache
multi-slot LRU
bindless resource arrays
persistent source-weight bind groups
persistent training-tape bind groups
Down projection fusion
SiLU LUT
FP16 texture conversion
new optimizer math
new backward math
```

---

## 37. Packaging closure

The baked code ZIP excludes:

```text
Markdown specifications
*.sha256
manifest JSON
artifact JSON
report JSON
```

Build-required source and Cargo TOML files remain included.

Overlay scope is limited to the files changed or added by this revision.

---

## 38. Next natural stage

Recommended next stage:

```text
ASH-BASETRAIN-FFN-TENSORCUBE-GPU-TIMESTAMP-AND-RESOURCE-CHURN-PERF-GUARD-R1
```

The persistent slab should be physically measured before fusing Down or introducing approximate activation paths.

Target measurements:

```text
cold route initialization cost
warm same-content FFN cost
different-layer repopulation cost
pipelines avoided
textures avoided
views avoided
static bind groups avoided
blocking polls avoided
population dispatches avoided
```

Host wall time and GPU timestamp must remain separately labeled.

---

## Final seal

```text
The parent revision fused the FFN arithmetic.

This revision fuses its lifetime discipline.

Pipelines belong to the route executor.
Texture allocation belongs to the one physical FFN slot.
Texture content belongs to an exact model/tensor/layer/source-generation/source-buffer key.
Input and training tape belong only to the current invocation.

A layer number is no longer allowed to masquerade as weight generation.
The wave-resident path derives generation from the actual resident weight pack, or from the active VRAM weight cache when that is the live source authority.

Changing weight content does not destroy the 88-MiB texture window.
It invalidates the content key and repopulates that same window.

Static texture bind groups live with the window.
Dynamic weight and tape bind groups die with the invocation.

The hot path no longer recompiles pipelines, reallocates textures or views, rebuilds static texture bind groups, or blocks on a device poll for each FFN call.

Resource reuse is allowed.
Stale weight reuse is not.
```
