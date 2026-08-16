# ASH-BASETRAIN-FFN-TENSORCUBE-MULTI-SLOT-LAYER-LOCAL-TEXTURE-RESIDENCY-R1

## Status

- Patch ID: `ASH-BASETRAIN-FFN-TENSORCUBE-MULTI-SLOT-LAYER-LOCAL-TEXTURE-RESIDENCY-R1`
- Build revision: `basetrain-ffn-tensorcube-multi-slot-layer-local-texture-residency-r1`
- Parent: `ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1`
- Perf evidence parent: `ASH-BASETRAIN-FFN-TENSORCUBE-PHYSICAL-PERF-HARNESS-AND-BASELINE-CAPTURE-R1`
- Authority: route-local `BaseTrainFfnTensorCubePersistentExecutor`
- Shader math: unchanged
- Optimizer/checkpoint/backward formulas: unchanged

## SSOT

FFN Gate/Up textures are derived GPU residency for exact trainable weight content. The route-local executor may retain multiple layer-local texture pairs only inside an explicit byte budget. Exact model/tensor-set/layer/generation/Gate-source/Up-source/packing identity is required for a hit. Allocation identity and content identity remain separate. No texture becomes trainable-weight, checkpoint, optimizer, or generation authority.

## Motivation

The physical baseline established that the existing persistent slab already removes repeated pipeline, texture-view, static-bind-group, and allocation churn on warm hits, while layer/generation content transitions still require Gate/Up population. Therefore this patch targets content-residency churn rather than recreating resource infrastructure.

The patch does not claim a production percentage speedup from deterministic fixture weights. Physical fixture evidence is sufficient to justify a bounded residency candidate and to verify population avoidance, but not to auto-promote a production optimization policy.

## Required topology

```text
AtlasRuntimeRouteAdmissionContext
    -> Arc<BaseTrainFfnTensorCubePersistentExecutor>
        -> common population/fused pipelines
        -> common layouts and uniform buffers
        -> one timestamp slab
        -> Mutex<PersistentState>
            -> Vec<FfnTextureResidencySlot>
```

No process-global cache, `OnceLock`, hidden thread-local cache, second model-owned pool, forward-only pool, or backward-only pool is permitted.

## Constructors and control authority

`BaseTrainFfnTensorCubePersistentExecutor::new(...)` remains a one-slot compatibility/control constructor. This preserves the parent physical baseline as a single-slot comparison surface.

Production route admission uses:

```rust
BaseTrainFfnTensorCubePersistentExecutor::new_with_residency_budget_bytes(...)
```

The default production byte budget is:

```text
384 MiB
```

and may be explicitly overridden with:

```text
ASH_BASETRAIN_FFN_TEXTURE_RESIDENCY_BUDGET_BYTES
```

The byte budget is authoritative. Slot count is derived from geometry and admitted bytes, not a fixed production constant.

## Texture pair byte authority

The canonical pair byte calculation is:

```text
(intermediate / 4) * hidden * 16 bytes * 2 textures
```

implemented by:

```rust
ffn_tensorcube_texture_pair_bytes(hidden, intermediate)
```

For the current 2048 x 5632 FFN geometry this is approximately 88 MiB per Gate/Up pair. The default 384 MiB budget therefore admits four full pairs while remaining geometry-derived rather than slot-count-derived.

## Slot state machine

Each physical slot owns one Gate texture, one Up texture, their views, and persistent slot-specific static bind groups. Pipelines and layouts remain common executor resources.

Required logical states:

```text
Vacant -> Populating -> Resident -> Retiring
                       ^          |
                       |----------|
```

An exact resident hit remains `Resident -> Resident`.

A retiring slot may be repopulated in-place. The texture allocation does not need to be destroyed merely because the content identity changes.

## Content key

The exact residency key contains:

- model source digest
- model spec ID
- tensor-set digest
- layer index
- source weight generation
- Gate raw source identity digest
- Up raw source identity digest
- RGBA4 packing revision

The source identity seals primitive ID, stream ID, buffer offset, buffer size, payload length, shape, and element width.

No partial-key hit is allowed.

## Generation authority

`PersistentState` tracks an active source-weight generation.

Rules:

1. First observed generation establishes the active generation.
2. A larger generation advances the active generation.
3. A request with a generation lower than the active generation fails closed with `FFNResidencyGenerationRegression`.
4. Old-generation physical slots may remain allocated until reused or retired, but they cannot satisfy a request for the new active generation.
5. Layer-local rebind prefers overwriting the old content for the same logical layer rather than accumulating parallel versions of the same layer.

This prevents silent resurrection of a stale generation after a generation transition.

## Source-identity drift

For the same logical model/tensor-set/layer/packing identity, a Gate or Up source-identity change is a miss and repopulation event.

The existing layer-local slot is reused for the changed source rather than creating duplicate authoritative variants for the same logical layer. This keeps one active layer-local content binding per layer/generation path.

## Admission before allocation

Before a new physical pair is allocated:

```text
resident_bytes_before + texture_pair_bytes <= active_budget_bytes
```

must be true.

If the growth admission fails, no new texture is created first and evicted later. The executor records a budget-growth rejection and chooses an existing eligible victim deterministically.

No allocate-then-evict VRAM overshoot is permitted.

## Victim selection

When no vacant slot exists and budget does not allow growth:

1. only `Resident` slots are candidates;
2. stale-generation content is preferred for retirement;
3. otherwise the smallest `last_use_serial` wins;
4. `slot_id` is the deterministic tie-breaker.

The physical slot is repopulated in place. No hot-path GPU resource destruction is performed.

## Slot identity

Slot IDs are monotonically allocated with `next_slot_id` and are never derived from the current vector length. This prevents slot-ID reuse/collision after pressure contraction removes physical slots.

## Forward to backward reuse

Forward and `BackwardRecompute` share the same executor and residency pool.

Each slot tracks:

- last use serial
- last forward use serial
- last backward use serial

On an exact backward hit where the same content was previously used by forward, the receipt records:

```text
forward_backward_reuse_hit = true
reuse_distance = current_use_serial - last_forward_use_serial
population_avoided_count = 1
```

This is the primary physical reuse target of R1.

## Pressure-driven contraction

Growth is hot-path nonblocking. Physical contraction is intentionally separated from the hot execute path.

The explicit safe-point API is:

```rust
resize_residency_budget_blocking(new_budget_bytes)
```

Rules:

1. the target budget must still admit at least one full pair;
2. the method performs an explicit device-idle wait outside `execute`;
3. oldest eligible resident slots are retired until allocated bytes fit the target;
4. `pressure_retirement_count` records the retirement count;
5. the active hot `execute` path contains no `PollType::Wait` and no `map_async`.

Thus durability/safety of in-flight GPU work is not traded for immediate memory pressure response.

## Resource boundaries

Common persistent resources:

- population pipeline
- fused Gate+Up+SiLU+SwiGLU pipeline
- pipeline layouts
- bind-group layouts
- population uniform buffer
- fused parameter buffer
- timestamp query/resolve/readback slab

Per-slot persistent resources:

- Gate texture
- Up texture
- Gate view
- Up view
- population static bind group
- fused static bind group

Per-invocation dynamic resources remain:

- population source bind group on miss
- fused input/tape bind group

Dynamic bind-group reuse is explicitly out of scope for R1.

## Math preservation

The existing WGSL stays unchanged:

- `Rgba32Float` Gate/Up textures
- RGBA4 output-lane packing
- 64-thread workgroup
- 16 x 16 x 16 logical macro geometry
- `textureLoad` only
- no sampler
- exact SiLU `x / (1 + exp(-x))`
- SwiGLU multiplication in the fused kernel
- four training tape outputs
- no workgroup barrier
- no workgroup storage introduction

Down projection remains separate and unchanged.

## Receipt additions

`BaseTrainFfnTensorCubePersistentResourceReceipt` additionally exposes:

- residency budget bytes
- resident bytes before/after
- resident slot count before/after
- selected slot ID
- slot allocation created/reused
- eviction executed
- evicted content-key digest
- forward/backward reuse hit
- reuse distance
- population avoided count
- resident high-water bytes
- budget-growth reject count
- pressure-retirement count
- active-slot eviction count
- in-flight resource-destroy count

The last two must remain zero for the R1 production path.

## Physical harness

Binary:

```text
ash_basetrain_ffn_tensorcube_multi_slot_residency_harness_r1
```

Required scenarios:

### TwoLayerPingPong

```text
L0 -> L1 -> L0 -> L1
```

With a two-pair budget, the final two executions must be exact hits with no population.

### FourLayerForwardBackward

```text
Forward:  L0 L1 L2 L3
Backward: L3 L2 L1 L0
```

With a four-pair budget, all four backward executions must hit the forward-created residency, avoid population, and emit reuse distance.

### CapacityPlusOne

With a two-pair budget:

```text
L0 -> L1 -> L2
```

The third layer must trigger deterministic in-place eviction without exceeding the byte budget.

### PressureContraction

Populate four layers under a four-pair budget, explicitly contract to two pairs at the blocking safe point, then verify two physical slots remain inside the new budget and hot execution still reports zero blocking polls.

### GenerationTransition

Same layer/source:

```text
generation 1 -> generation 2
```

must miss and repopulate the layer-local slot. A later attempt to regress to generation 1 must fail closed.

### SourceIdentityDrift

Same layer and generation with changed Gate/Up source identity must miss and repopulate the existing layer-local slot rather than create a duplicate layer authority.

### Canonical finite check

A diagnostic GPU scan checks Gate-pre, SiLU-Gate, Up-linear, and FFN-product outputs using the f32 exponent mask. The canonical nonfinite count must be zero.

## Promotion criteria

Static promotion requires:

- exact content-key authority preserved
- production route uses byte-budgeted constructor
- parent single-slot constructor retained
- admission-before-allocation present
- deterministic victim selection present
- monotonic slot IDs present
- generation regression fails closed
- source drift repopulates instead of duplicate layer authority
- forward/backward pool shared
- reuse-distance telemetry present
- pressure contraction only blocks outside execute
- no hot-path blocking poll/error scope
- parent fused shader math unchanged

Physical promotion requires:

- TwoLayerPingPong PASS
- FourLayerForwardBackward PASS
- CapacityPlusOne PASS
- PressureContraction PASS
- GenerationTransition PASS
- SourceIdentityDrift PASS
- generation regression rejected
- canonical nonfinite count = 0
- resident bytes never exceed the active budget
- active-slot eviction count = 0
- in-flight resource-destroy count = 0

## Non-goals

R1 does not implement:

- all-layer prepopulation
- unbounded VRAM residency
- predictive/ML cache policy
- dynamic bind-group caching
- fused-kernel tile rewrite
- input staging rewrite
- Down projection fusion
- optimizer changes
- checkpoint changes
- host weight repack
- payload D2H
- benchmark-only FFN kernel
- automatic production promotion from deterministic fixture results

## Final seal

```text
Bounded Multi-Slot FFN Texture Residency /
Layer-Local Gate-Up Texture Pair Residency /
Exact Content-Key Slot Authority /
Forward-to-Backward Recompute Reuse /
Admission Before Allocation /
Deterministic Oldest-Eligible Retirement /
Generation Regression Fail-Closed /
Source-Identity Rebind Closure /
Pressure Contraction At Explicit Safe Point /
No Hot-Path Blocking Poll /
No Texture Weight Authority /
No Shader Math Mutation /
No Optimizer Or Checkpoint Mutation /
MULTI-SLOT LAYER-LOCAL TEXTURE RESIDENCY SSOT CLOSURE
```
