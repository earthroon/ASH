# ASH-BP-DELTA-K-CANONICAL-GRADIENT-SEGMENTED-DIRECT-OBSERVATION-LOCAL-GENERATION-BATCH-BRIDGE-GENERATION-BATCH-PARAMETER-WAIT-RETIREMENT-R2

## 0. Revision

```text
Short name:
DK-PERF-R1A1-R2

Static source state:
SEGMENTED DIRECT SOURCE CUTOVER = MATERIALIZED
GENERATION BATCH / O(1) SYNC    = HOLD
PHYSICAL PERFORMANCE PASS       = HOLD
```

Static token:

```text
PASS_ASH_BP_DELTA_K_CANONICAL_GRADIENT_SEGMENTED_DIRECT_OBSERVATION_LOCAL_BRIDGE_GENERATION_BATCH_PARAMETER_WAIT_RETIREMENT_R2_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_CANONICAL_GRADIENT_SEGMENTED_DIRECT_OBSERVATION_LOCAL_BRIDGE_GENERATION_BATCH_PARAMETER_WAIT_RETIREMENT_R2_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_CANONICAL_GRADIENT_SEGMENTED_DIRECT_OBSERVATION_LOCAL_BRIDGE_GENERATION_BATCH_PARAMETER_WAIT_RETIREMENT_R2
```

## 1. Direct parent

```text
ASH_PASS3_DK_PERF_R1A1_GENERATION_PACKED_GRADIENT_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 d16747b8d47ecb9e29ee02359f1ef93df4e892afd52bbeca5697b9f88513712b
```

R1A1 already established generation lease/coordinator authority without increasing packed-gradient VRAM peak. R2 narrows the role of that interim packed-gradient authority: Local and Bridge observation now consume canonical R6 finalized gradient segments directly; packed-gradient remains a Muon representation.

## 2. Mathematical non-goal

R2 does not change Delta-K = I * M^2, Local information/material definitions, exact flattened 256D Bridge cosine, bridge temporal Delta-K, fusion/fission thresholds, confirmation/cooldown, greedy pair ordering, Muon rectangular geometry, Newton-Schulz, counterfactual mathematics or objective-probe mathematics.

## 3. Canonical R6 segmented source

R2 reuses `R6FinalizedGradient` / `TensorCubeLocalMuonGradientSegment` as the canonical device-resident gradient source. No Delta-K-specific full gradient buffer, host materialization, H2D upload or D2D full-gradient duplicate is introduced.

New backend authority:

```text
crates/burn_webgpu_backend/src/bp_delta_k_segmented_gradient_source_r2.rs
```

`BpDeltaKCanonicalGradientSegmentSetR2::from_muon_segments` requires monotonically contiguous F32 segments, exact full logical coverage, tile-aligned matrix geometry, and at most three physical segment slots for the current canonical model ABI.

## 4. Three-slot direct ABI

Current canonical largest Muon matrix is 5632x2048 (or transpose), 11,534,336 f32 elements. With the existing R6 16 MiB page bound this needs at most three finalized gradient segments. R2 therefore freezes the current model ABI at three read-only gradient segment bindings.

Unused slots bind a persistent 4-byte null storage buffer and carry zero segment count. Inactive slots are never read.

## 5. Segment boundary exactness

The shader resolves every logical matrix element by row-major logical index and selects the segment whose `[logical_start, logical_start + count)` contains the index. R2 does not assume page boundaries align to rows or 16x16 tiles.

The mandatory physical parity campaign must cover the current 5632-column boundary cases where an R6 page boundary cuts through a 16-row tile band.

## 6. Local direct shader

Added:

```text
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_local_observe_segmented_16x16_r2.wgsl
```

The shader reads canonical segmented gradient values directly and preserves the existing 16-row sketch, gradient RMS, parameter RMS, information, material, raw Delta-K and smoothed Delta-K equations.

The existing resident/packed weight authority remains unchanged. Local committed/pending EMA state remains shared with the legacy packed pipeline; R2 does not create a second Local temporal-state authority.

`TensorCubeBpDkLocalObserver` now owns both legacy packed and segmented-direct pipelines against the same `states` map.

## 7. Bridge direct shader

Added:

```text
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_bridge_pair_cosine_segmented_16x16_r2.wgsl
```

Bridge descriptors are interpreted as tile ordinals in the direct shader. Each of 256 lane elements derives its canonical row-major logical index and reads the same R6 segment set used by Local. Dot, lhs norm2, rhs norm2, zero-norm handling, nonfinite handling and cosine semantics are unchanged.

`TensorCubeBpDkBridgePairObserver` now owns legacy packed and segmented-direct pipelines.

## 8. Active callsite cutover

For typed Delta-K ObserveOnly and Active modes, `ProductionMuonRuntime::execute_muon_parameter` constructs one `BpDeltaKCanonicalGradientSegmentSetR2` directly from the already supplied `gradient_segments` and routes both Local and Bridge observation through `observe_segmented_r2`.

Legacy packed observation remains reachable only as a non-direct fallback path. The current Disabled outer bypass is not yet complete, so Disabled still reaches legacy observation in this source state and therefore remains a physical HOLD.

## 9. Generation gradient catalog

Added:

```text
crates/base_train/src/bp_delta_k_canonical_gradient_catalog_r2.rs
```

`ProductionBpDkRuntimeR8` owns one catalog per optimizer generation. ObserveOnly/Active record canonical parameter index, parameter ID, rows, cols, segment count and segment-plan digest. Duplicate parameter registration and generation regression fail closed.

This is generation identity/catalog authority, not a second gradient allocation owner.

## 10. Direct-source telemetry

Local and Bridge telemetry now distinguish:

```text
direct_segmented_gradient_source_count_r2
legacy_packed_gradient_source_count_r2
gradient_h2d_bytes_r2
gradient_duplicate_device_copy_bytes_r2
```

The segmented direct path reports zero Delta-K gradient H2D and zero duplicate-gradient device-copy bytes.

## 11. Physical receipt authority

Added:

```text
crates/base_train/src/bp_delta_k_perf_r1a1_r2_physical_receipt.rs
```

The receipt requires direct-source coverage, zero legacy fallback, zero Delta-K gradient packing/transport duplication, zero parameter-local waits, bounded generation waits/maps, zero hotpath full-payload SHA, zero steady-state pipeline rebuilding, semantic parity, topology parity and generation transaction continuity before physical PASS may be claimed.

`DK_PERF_R1A1_R2_PHYSICAL_QUALIFIED_AT_BAKE = false`.

## 12. What this static bake actually closes

```text
PASS / MATERIALIZED:
  canonical R6 segment-set authority
  fixed three-slot direct ABI
  Local segmented-direct shader/pipeline
  Bridge segmented-direct shader/pipeline
  Local ObserveOnly/Active direct callsite
  Bridge ObserveOnly/Active direct callsite
  shared Local temporal state between packed/direct routes
  generation gradient catalog
  direct-source physical receipt authority
  no new full-gradient copy/H2D/materialization
```

## 13. What remains HOLD

The backend direct methods still perform their current parameter-local submission/readback synchronization. Therefore the following are explicitly not claimed by this bake:

```text
Local generation batch
Bridge generation batch
Post generation batch
Local parameter wait retirement
Bridge parameter wait retirement
Post parameter exact-wait retirement
O(1) generation synchronization
aggregate generation mapped-readback closure
Disabled true zero-cost outer bypass
physical semantic/topology parity
physical performance PASS
```

The source still contains `wait_for_submission_exact` in Local/Bridge direct observers. This is intentional source truth, not a hidden PASS.

## 14. Why generation batching is not fabricated here

The production parameter loop still constructs and consumes planner results parameter-by-parameter. Moving Local/Bridge waits out of each parameter requires planner preparation to move above physical Muon parameter execution and requires generation-owned command/readback arenas. R2 does not create a second full-gradient store or fake an O(1) submit counter to claim this prematurely.

## 15. Next physical completion slice

The direct source now removes the main packed-gradient dependency. The next physical cut can safely operate on canonical segment views:

```text
DK-PERF-R1A1-R2A
Prepared Generation Observation Plan
+ Local Encode/Collect Batch
+ Bridge Encode/Collect Batch
+ Post Aggregate Collection
+ <=3 Generation Visibility Barriers
```

R2A should move planner preparation outside per-parameter Muon execution, use persistent generation evidence arenas, and retire Local/Bridge/Post parameter waits without retaining full packed gradients.

## 16. Physical parity campaign

Before R2 physical promotion compare legacy packed vs segmented direct on identical source state for:

```text
Local:
  gradient RMS
  parameter RMS
  sketch RMS
  sketch delta RMS
  information
  material
  raw/smoothed Delta-K
  Warming/Ready status

Bridge:
  dot
  lhs norm2
  rhs norm2
  cosine
  ZeroNorm/NonFinite/Ready status

Planner:
  candidate pairs
  ordering
  orientation
  fusion/fission decision
  confirmation streak
  cooldown
```

Topology parity is exact authority.

## 17. Canonical source admission

Physical PASS for the current model requires every admitted Muon parameter to use the segmented-direct path, with zero segment slot overflow and zero lookup/coverage failure. Any legacy packed fallback must be separately reported and prevents canonical direct-source PASS.

## 18. Transport law

For canonical direct observation:

```text
Delta-K full gradient H2D       = 0
Delta-K full gradient D2D copy  = 0
Delta-K full gradient D2H       = 0
Delta-K full weight H2D         = 0 on the existing resident-weight path
normal hotpath full SHA         = 0
```

Muon's own packed-gradient representation remains separately accounted and is not misclassified as Delta-K transport.

## 19. Static source delta

Relative to the direct R1A1 parent:

```text
ADD 5
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_canonical_gradient_catalog_r2.rs
crates/base_train/src/bp_delta_k_perf_r1a1_r2_physical_receipt.rs
crates/burn_webgpu_backend/src/bp_delta_k_segmented_gradient_source_r2.rs
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_local_observe_segmented_16x16_r2.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_bridge_pair_cosine_segmented_16x16_r2.wgsl
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
crates/burn_webgpu_backend/src/bp_delta_k_bridge_pair_observer.rs
```

## 20. Code artifacts

```text
ASH_PASS3_DK_PERF_R1A1_R2_SEGMENTED_DIRECT_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 cb4b6befcca47b97d1556d1e803b2db6c1efff6f9623e087adec7eeeececeba9
entries 8,433

ASH_PASS3_DK_PERF_R1A1_R2_SEGMENTED_DIRECT_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 eaecade221faa37d1e950684f332d29f34d5109ccfcfffe61698b4720241218f
entries 10
```

Parent + overlay reproduces the full tree byte-for-byte.

## 21. Compile truth

The bake environment has no Cargo/Rustc. Post-bake compile PASS is not claimed.

Immediate local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler results override every static source assumption.

## 22. Final law

> R6 finalized gradient segments are the canonical device-resident gradient authority.

> Local and Bridge Delta-K now have a direct segmented observation route that consumes that authority without a Delta-K packed-gradient copy.

> Local packed and segmented routes share one temporal-state authority.

> Bridge direct observation preserves the exact 256D cosine semantics.

> Segment boundaries may cut through rows and 16x16 tiles; logical-index lookup must remain exact across them.

> This static bake closes direct source adoption only. O(1) synchronization remains HOLD until Local, Bridge and Post stop owning parameter-local waits and planner preparation becomes generation-scoped.
