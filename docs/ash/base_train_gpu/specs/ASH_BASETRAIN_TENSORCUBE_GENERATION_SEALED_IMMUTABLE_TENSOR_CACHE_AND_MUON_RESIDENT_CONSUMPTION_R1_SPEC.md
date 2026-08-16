# ASH-BASETRAIN-TENSORCUBE-GENERATION-SEALED-IMMUTABLE-TENSOR-CACHE-AND-MUON-RESIDENT-CONSUMPTION-R1

## Patch

```text
ASH-BASETRAIN-TENSORCUBE-GENERATION-SEALED-IMMUTABLE-TENSOR-CACHE-AND-MUON-RESIDENT-CONSUMPTION-R1

Canonical Trainable Tensor Authority /
Physical Multi-Slot Residency Parent Adoption /
Structural Immutable Tensor Cache /
Generation-Sealed Immutable Tensor Cache /
Mutable Muon State Separation /
TensorCube-Native Resident Operand /
Muon Direct Resident Consumption /
No Cache-Eligible Raw Bypass /
No Cross-Generation Content Hit /
No Muon Math Mutation /
No Automatic Production Promotion
```

## Purpose

This patch makes TensorCube own reusable Muon operand residency instead of recreating the same structural GPU descriptors and generation-local weight buffers for every eligible Muon execution.

The patch changes operand preparation and residency only. Canonical trainable tensor content, optimizer commit authority, generation authority, checkpoint authority, Muon formula, PAD17 geometry, Newton-Schulz coefficients/iteration count, gradient semantics, and optimizer update semantics remain unchanged.

## Parent SSOT

Physical parent:

```text
ASH-BASETRAIN-FFN-TENSORCUBE-MULTI-SLOT-LAYER-LOCAL-TEXTURE-RESIDENCY-R1
```

Parent physical evidence already closed:

```text
two_layer_ping_pong_pass=true
four_layer_forward_backward_pass=true
capacity_plus_one_pass=true
pressure_contraction_pass=true
generation_transition_pass=true
source_identity_drift_pass=true
generation_regression_rejected=true
canonical_nonfinite_count=0
```

This R1 adopts the same policy direction for Muon resident buffers: byte-bounded residency, exact generation/source identity, deterministic retirement, safe-point contraction, and no active/in-flight reuse.

## Authority

```text
Canonical Trainable Tensor
= content authority
= generation authority
= optimizer commit authority
= checkpoint authority

TensorCube Immutable Cache
= derived physical GPU representation only
```

A cache slot never becomes canonical weight or checkpoint authority.

## Cache layers

### L0 Structural Immutable Cache

Generation-independent GPU descriptor buffers are reused when the exact structural key matches.

Structural identity binds:

```text
tensor identity
Muon tile descriptors
batch tile base
batch tile count
PAD17/kernel layout revision
```

The structural cache may survive weight generation changes when the structural contract remains exact.

### L1 Generation-Sealed Tensor Cache

Generation-local packed Muon weight buffers are keyed by:

```text
tensor identity
Muon eligible tensor-set digest
source generation
canonical source weight digest
logical shape
packed element count
F32 dtype
PACKED_LOCAL_16X16_ROW_MAJOR layout
PAD17 revision
TensorCube tile revision
Muon projection revision
physical batch index/range
```

`source_generation` and the canonical per-parameter weight digest are passed from the production BaseTrain scheduler. Pointer identity is not accepted as content identity.

## State ownership

```text
TensorCubeLocalMuonBatchExecutor
  -> Mutex<TensorCubeMuonImmutableCache>
       -> structural GPU descriptor entries
       -> generation-sealed resident weight slots
       -> byte budget / serial / telemetry

ProductionMuonRuntime
  -> Muon mutable momentum authority
```

Muon is a cache consumer, not the cache owner.

## Mutable state exclusion

The immutable cache does not own:

```text
gradient
momentum
candidate momentum
Newton-Schulz mutable working state
optimizer accumulator
step statistics
candidate weights
```

These remain mutable execution/optimizer state.

## Production binding

The production scheduler passes:

```text
source.generation
src.candidate_weight_digest
```

to `ProductionMuonRuntime::execute_muon_parameter(...)`.

The production runtime creates `TensorCubeMuonResidentTensorIdentity` and calls:

```text
TensorCubeLocalMuonBatchExecutor::execute_resident(...)
```

The Muon bind group consumes the resident weight `wgpu::Buffer` directly.

The existing raw `execute(...)` API remains for baseline/parity harnesses and compatibility surfaces. Production Muon uses the resident path.

## Generation semantics

```text
Generation N resident weight
  -> exact-generation HIT allowed
  -> optimizer commit
Generation N+1
  -> old content becomes STALE
  -> structural descriptor cache may remain HIT
  -> weight content must rebuild/rebind
```

A request for a generation lower than the active generation fails closed.

## Source identity drift

Within the same generation, a changed canonical source digest invalidates matching tensor resident slots. No silent reuse is allowed.

## Residency budget

Default Muon immutable residency budget:

```text
128 MiB
```

Runtime override:

```text
ASH_BASETRAIN_TENSORCUBE_MUON_IMMUTABLE_CACHE_BUDGET_BYTES
```

Admission occurs before new allocation. A single payload larger than the active budget is rejected.

Victim order under pressure:

```text
1. stale slot first
2. oldest last-use serial
3. lowest slot id tie-break
```

Slots with active leases are not eligible victims.

A stale slot whose allocated capacity is sufficient may be repopulated with `queue.write_buffer` instead of allocating a new GPU buffer.

## Safe-point contraction

`contract_immutable_cache_budget_at_safe_point(...)` performs deterministic retirement outside active/in-flight use. It does not add a blocking poll to the cache lookup hot path.

## Muon math preservation

The Muon shader files are unchanged from the parent baked SSOT:

```text
base_train_tensorcube_local_muon_16x16.wgsl
SHA256 3f08fa919cfde360722ab37706d0bbbb292d5e849afe6dd7c1b3014da36533d8

base_train_tensorcube_local_muon_gradient_pack.wgsl
SHA256 daaafe171081f60d4224c3540be884613c03439e2ab6b1db6a4863724a40619a
```

PAD17 remains:

```text
TENSORCUBE_LOCAL_MUON_KERNEL_LAYOUT_REVISION = X_PAD17_R1
```

No Muon formula or optimizer formula mutation is part of this patch.

## Telemetry

```text
structuralBuildCount
structuralHitCount
structuralMissCount

generationTensorBuildCount
generationTensorHitCount
generationTensorMissCount

generationStaleCount
sourceIdentityStaleCount

tensorRebuildCount
tensorRebuildAvoidedCount

residentMuonConsumeCount
rawMuonConsumeCount
cacheEligibleRawBypassCount

slotAllocationCount
slotAllocationReuseCount
evictionCount
staleRetirementCount

residentBytes
residentHighWaterBytes
residencyBudgetBytes
budgetAdmissionRejectCount

activeSlotEvictionCount
inFlightResourceRebindCount

weightUploadBytes
weightUploadAvoidedBytes
```

Production callsite counters project resident-consumption and upload-avoidance evidence into the existing Muon receipt surface.

## Fail-closed boundaries

The patch rejects or fails on:

```text
generation regression
single resident payload > active byte budget
no eligible victim under byte pressure
source identity drift exact-hit attempt
active lease underflow
cache-eligible raw bypass in production
resident-consume / physical-batch cardinality drift
nonfinite Muon output
```

No silent raw fallback is added.

## Physical harness

New binary:

```text
ash_basetrain_tensorcube_generation_sealed_immutable_tensor_cache_muon_resident_consumption_harness_r1
```

Harness coverage:

```text
raw baseline
first resident build
same-generation resident HIT
exact raw vs resident parity
exact first resident vs HIT parity
structural descriptor reuse
source identity drift rebuild
generation transition rebuild
generation regression rejection
capacity+1 deterministic eviction
safe-point pressure contraction
raw-bypass negative control
canonical nonfinite scan
```

Performance timing in this R1 harness is wall-time evidence only and does not automatically promote performance claims.

## Static validation

New validator:

```text
tools/validate_basetrain_tensorcube_generation_sealed_immutable_tensor_cache_muon_resident_consumption_r1_static.py
```

Current bake result:

```text
66/66 PASS
```

Parent regression validators remain PASS in the bake environment:

```text
Muon multi-tile batch dispatch        61/61
Muon production callsite              62/62
Muon PAD17                             52/52
FFN multi-slot residency               78/78
FFN persistent resource slab           66/66
FFN GPU timestamp/perf guard          101/101
FFN physical perf harness              72/72
FFN fused production                   45/45
G45 source restoration                 42/42
G27 source restoration                 35/35
GPU70K bin/library export              13/13
Atlas/HOTPATH compile repair           56/56
HOTPATH allocation audit               26/26
```

## Bake contents

Code overlay contains only:

```text
crates/burn_webgpu_backend/src/tensorcube_generation_sealed_muon_cache.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/bin/ash_basetrain_tensorcube_generation_sealed_immutable_tensor_cache_muon_resident_consumption_harness_r1.rs
tools/validate_basetrain_tensorcube_generation_sealed_immutable_tensor_cache_muon_resident_consumption_r1_static.py
```

The baked ZIP intentionally excludes markdown specs, `*.sha256`, manifests, artifact JSON, and report JSON.

## Current status

```text
BAKED_STATIC_READY
PHYSICAL_GPU_HARNESS_REQUIRED
NO_LOCAL_CARGO_COMPILE_CLAIM
NO_AUTOMATIC_PRODUCTION_PERFORMANCE_PROMOTION
```

The bake environment does not provide `cargo`, `rustc`, or `rustfmt`; therefore Rust compile PASS and physical GPU harness PASS are not claimed here. User-local Cargo/physical harness output is the final execution SSOT.

## Promotion target

```text
PASS_ASH_BASETRAIN_TENSORCUBE_GENERATION_SEALED_IMMUTABLE_TENSOR_CACHE_AND_MUON_RESIDENT_CONSUMPTION_R1
```

Promotion requires the physical harness to show exact resident parity, same-generation HIT, generation/source fencing, bounded residency, pressure contraction, zero cache-eligible raw bypass, zero active/in-flight reuse violations, and zero canonical nonfinite output.
