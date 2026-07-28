# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R6

## TensorCube Stage 1 Feature Activation / HeadwiseActive Parent Binding / Single-Feature Mask Transition / Same-Device Execution / Output·KV Numerical Parity / Exact Headwise Fallback / Generation 24→25→26 Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R5
PARENT_VERDICT=PASS
PARENT_ATTENTION_ROUTE_STATE=HeadwiseActive
PARENT_TENSORCUBE_STAGE_STATE=Stage0ConsumerReady
PARENT_TENSORCUBE_FEATURE_MASK=none
PARENT_TERMINAL_GENERATION=24
RUN_SCOPE=headwise-active-tensorcube-stage1-single-feature-activation-v1
DEFAULT_VERDICT=HOLD
ATTENTION_ROUTE_ID=gqa4-cluster-production-canary-v1
ATTENTION_ROUTE_STATE=HeadwiseActive
TENSORCUBE_PARENT_STAGE_ID=tensorcube-stage-0-consumer-ready-v1
TENSORCUBE_STAGE_ID=tensorcube-stage-1-physical8x8-vec4-output-v1
TENSORCUBE_STAGE1_FEATURE_ID=tensorcube-physical-8x8-vec4-microtile-output-v1
TENSORCUBE_PARENT_FEATURE_MASK=0x0000000000000000
TENSORCUBE_STAGE1_FEATURE_BIT=0
TENSORCUBE_STAGE1_FEATURE_MASK=0x0000000000000001
TENSORCUBE_KERNEL_KIND=Vec4Atlas
TENSORCUBE_PHYSICAL_TILE=8x8
TENSORCUBE_SCALAR_KIND=f32
TENSORCUBE_PACKING_KIND=vec4-f32
TENSORCUBE_SCALARS_PER_TILE=64
TENSORCUBE_VEC4_PER_TILE=16
TENSORCUBE_BYTES_PER_TILE=256
TENSORCUBE_SHADER_PATH=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_vec4.wgsl
TENSORCUBE_SHADER_ENTRYPOINT=main
FEATURE_TRANSITION_POLICY=exactly-one-disabled-to-enabled-bit-v1
STAGE_ACTIVATION_POLICY=stage1-supported-scope-explicit-commit-v1
SAME_DEVICE_POLICY=producer-consumer-buffer-queue-single-device-v1
OUTPUT_PARITY_POLICY=f32-abs-rel-1e-4-zero-nonfinite-v1
KV_PARITY_POLICY=no-stage1-kv-write-bit-exact-unchanged-v1
FALLBACK_POLICY=stage1-to-headwise-active-exact-before-publication-v1
GENERATION_POLICY=parent24-stage-open25-stage-commit26-v1
PAYLOAD_POLICY=zero-host-materialization-zero-host-upload-zero-payload-readback-bounded-compact-decision-v1
OWNERSHIP_POLICY=headwise-owned-read-borrow-provisional-output-lease-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
RUNTIME_ROOT_POLICY=typed-streaming-deterministic-root-v1
```

R2-R6 enables the first actual TensorCube computational feature beneath the already active headwise route. The feature is the existing physical 8×8 Vec4 microtile output dispatch. It reads the HeadwiseActive handoff buffers on the same device, produces a provisional output tile, compares that output against the HeadwiseActive result, and commits Stage 1 only after numerical parity and unchanged KV state are proven.

R2-R6 does not enable workgroup-memory microtiles, subgroup paths, logical 16×16 composition, K-panel streaming, TensorCube KV writes, or any second feature bit.

---

## 1. Purpose

R2-R6 must prove all of the following:

```text
1. The R2-R5 HeadwiseActive route and Stage 0 handoff remain exact and immutable.
2. TensorCube feature mask transitions from none to exactly one feature bit.
3. The enabled feature is the physical 8x8 Vec4 microtile output path only.
4. The TensorCube dispatch executes on the same physical device and queue lineage as HeadwiseActive.
5. Q/K/V, KV-cache, provisional output, and committed output remain generation-bound.
6. Stage 1 reads Headwise-owned inputs without transferring ownership to CPU or another device.
7. Stage 1 receives an output write lease but receives no KV write lease.
8. TensorCube Stage 1 produces numerically equivalent output to HeadwiseActive.
9. TensorCube Stage 1 leaves the KV post-state bit-exact and unchanged.
10. Unsupported scope falls back exactly to HeadwiseActive before output publication.
11. Stage 1 failure does not fall directly to the legacy reference route while HeadwiseActive remains healthy.
12. Host materialization, host upload, tensor payload readback, payload-buffer mapping, and cross-device copy remain zero; one bounded compact decision-token readback is permitted for parity verdict publication.
13. Stage 1 commit advances generation 24 -> 25 -> 26 exactly.
14. Parent scientific PASS or HOLD remains visible and unchanged.
15. No second TensorCube feature is activated, prepared, or silently dispatched.
```

---

## 2. Stage 1 feature choice

The first feature is deliberately the smallest existing computational TensorCube unit:

```text
feature_id=tensorcube-physical-8x8-vec4-microtile-output-v1
kernel_kind=Vec4Atlas
physical_tile=8x8
packing=vec4-f32
input_tiles=two physical 8x8 f32 tiles
output_tile=one physical 8x8 f32 tile
input_scalar_count_per_tile=64
input_vec4_count_per_tile=16
output_scalar_count=64
output_vec4_count=16
bytes_per_tile=256
uses_workgroup_memory=false
uses_subgroup=false
creates_contiguous_16x16_tile=false
writes_kv_cache=false
writes_attention_output=true, provisional until commit
```

The bound shader is:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_vec4.wgsl
entrypoint=main
```

R2-R6 may wrap this shader with a stage-scoped adapter, but the adapter may not change the shader arithmetic, physical tile layout, packing order, binding order, or output interpretation without a new feature identity.

---

## 3. Explicit exclusions

The following remain disabled in R2-R6:

```text
WorkgroupTile kernel kind
workgroup-memory microtile path
subgroup fast path
logical 16x16 bridge
contiguous 16x16 allocation
software 16x16 softgroup
K-panel streaming
macro-tile scheduling
multi-tile accumulation
TensorCube KV-cache mutation
TensorCube in-place output overwrite before parity
TensorCube decode-route global replacement
TensorCube production performance claim
second or later feature bit
automatic feature expansion
CPU fallback disguised as TensorCube success
```

Any non-zero dispatch count for an excluded path is terminal HOLD.

---

## 4. Frozen parent authority

Required R2-R5 parent facts:

```text
parent pass=true
parent terminal generation=24
parent scientific terminal preserved=true
parent attention route=HeadwiseActive
active route ID=gqa4-cluster-production-canary-v1
active route pointer writes=1/1
headwise dispatches=128/128
headwise output parity=true
headwise KV parity=true
reference rollback output parity=true
reference rollback KV parity=true
TensorCube stage=Stage0ConsumerReady
TensorCube feature mask=none
TensorCube features enabled=0
TensorCube compute dispatches=0
TensorCube KV writes=0
TensorCube output writes=0
same device=true
KV ownership valid=true
host materializations=0
host uploads=0
payload readbacks=0
buffer maps=0
cross-device copies=0
generations=20/21/22/23/24
atlas groups=18/18
negative controls=440/440
```

R2-R6 must bind by digest:

```text
R2-R5 runtime artifact
R2-R5 local manifest
R2-R5 parent binding
R2-R5 parent terminal binding
R2-R5 evidence preservation receipt
R2-R5 headwise route identity
R2-R5 headwise adoption receipt
R2-R5 headwise parity receipt
R2-R5 Stage 0 registry
R2-R5 TensorCube consumer identity
R2-R5 Stage 0 handoff descriptor
R2-R5 same-device receipt
R2-R5 KV ownership receipt
R2-R5 zero-copy receipt
R2-R5 fallback-chain manifest
R2-R5 generation receipt
R2-R5 route pointer receipt
R2-R5 atlas digest
```

Every parent file must remain byte-identical before and after R2-R6.

---

## 5. State ownership and SSOT

### 5.1 AttentionRouteState

```text
owner=R2-R5 attention route manifest
value=HeadwiseActive
mutable_by_R2_R6=false
```

R2-R6 does not replace the top-level attention route. TensorCube Stage 1 is a child stage selected inside HeadwiseActive.

### 5.2 TensorCubeStageState

```text
owner=R2-R6 stage manifest
initial=Stage0ConsumerReady
open=Stage1Prepared
terminal=Stage1Active|Stage1Fallback|Quarantined
```

### 5.3 TensorCubeFeatureMaskState

```text
owner=R2-R6 feature-mask transition receipt
initial=0x0000000000000000
allowed_delta=0x0000000000000001
terminal_active=0x0000000000000001
```

### 5.4 KVOwnershipState

```text
owner=runtime device registry plus R2-R6 ownership receipt
parent_owner=HeadwiseOwned
stage1_input_state=TensorCubeReadBorrowed
stage1_output_state=TensorCubeWriteLeased
stage1_kv_write_state=forbidden
terminal_owner=HeadwiseOwned
```

### 5.5 StagePointerState

```text
owner=TensorCube stage registry
initial=tensorcube-stage-0-consumer-ready-v1
target=tensorcube-stage-1-physical8x8-vec4-output-v1
writes_allowed=exactly one successful compare-and-swap
```

### 5.6 ScientificEvidenceState

```text
owner=R1-R2 scientific artifact
value=PASS|HOLD as inherited through R2-R5
mutable_by_R2_R6=false
```

No state domain may substitute for another.

---

## 6. Single-feature mask transition

The only legal feature-mask transition is:

```text
0x0000000000000000
-> 0x0000000000000001
```

Required proof:

```text
parent mask exact
new feature bit index=0
new bit was Disabled in parent registry
new bit is Prepared before dispatch
new bit becomes Enabled only after commit
popcount(parent XOR child)=1
child mask=parent mask OR (1 << 0)
all other registered feature states remain Disabled
all unregistered bits remain zero
```

Forbidden:

```text
mask mutation before parent verification
multiple bit transition
bit replacement
bit clearing
unknown bit activation
feature alias mapping to two bits
second feature Prepared state
silent environment-driven feature enablement
```

---

## 7. Stage 1 input scope

Stage 1 supports only inputs satisfying the exact R2-R5 handoff contract plus the following microtile conditions:

```text
physical tile shape=8x8
scalar kind=f32
packing=vec4-f32
row-major logical interpretation
16 vec4 values per physical tile
256 bytes per physical tile
aligned offsets satisfy device storage-buffer alignment
A and B tile extents are complete
output extent is complete
batch and head mapping are explicit
no partial physical tile
no hidden padding value dependence
```

Minimum runtime matrix:

```text
KV lengths=128,384,512,768
32 deterministic decode steps per KV
supported Stage 1 attempts=128
expected Stage 1 committed dispatches=128
```

Each dispatch must retain:

```text
dispatch ID
KV length
decode step
physical device ID
queue lineage ID
producer generation
stage generation
Q buffer ID / offset / length
K buffer ID / offset / length
V buffer ID / offset / length
KV buffer ID / offset / length
provisional output buffer ID / offset / length
pipeline identity
shader identity
feature mask
fallback stage ID
output publication state
ownership token
```

---

## 8. Same-device and queue lineage

Stage 1 must use the already-bound R2-R5 runtime handles.

Forbidden:

```text
new wgpu Instance
new adapter request
new device request
new queue
second runtime registry
cross-device buffer migration
adapter name-only equivalence
separate smoke runner device
```

Required identities:

```text
Headwise producer physical_device_id
TensorCube physical_device_id
queue lineage ID
runtime registry generation
buffer allocation generation
```

All must match exactly.

---

## 9. KV ownership and mutation boundary

Stage 1 input transition:

```text
HeadwiseOwned
-> TensorCubeReadBorrowed
-> HeadwiseOwned
```

Stage 1 output transition:

```text
Unallocated or stage-local provisional buffer
-> TensorCubeWriteLeased
-> TensorCubeProvisionalOutput
-> HeadwiseCommittedOutput only after parity
```

Stage 1 KV write transition:

```text
forbidden
```

Required:

```text
KV write lease count=0
KV write count=0
KV bytes changed=0
KV page-table mutations=0
KV residency mutations=0
KV allocation generation unchanged
KV owner returns to HeadwiseOwned
```

---

## 10. Output provisional commit

TensorCube Stage 1 may write only to a stage-local provisional output buffer.

Before parity PASS and commit:

```text
active output pointer remains Headwise
consumer cannot see provisional TensorCube output
provisional buffer generation is Stage1Prepared
partial output is not published
stale provisional output is forbidden
```

At commit:

```text
output parity PASS
dispatch fences complete
device still healthy
stage generation exact
ownership token valid
feature mask still exact
stage pointer compare-and-swap precondition exact
```

After commit:

```text
Stage1Active visible
feature bit 0 Enabled
new stage generation=26
HReadwiseActive remains the top-level attention route
```

---

## 11. Output numerical parity

Authoritative reference:

```text
HeadwiseActive output for the same device, buffer slices, head, JV, decode step, and logical input
```

Required numeric policy:

```text
scalar kind=f32
abs_tolerance=1.0e-4
rel_tolerance=1.0e-4
nan_count=0
infinity_count=0
mismatch_count=0
```

A escalar comparison passes if:

```text
abs_error <= 1.0e-4
or
rel_error <= 1.0e-4
```

Relative error denominator:

```text
max(abs(reference), 1.0e-12)
```

Required comparisons:

```text
128 output tiles
64 scalars per tile
8192 total scalar comparisons
all fin