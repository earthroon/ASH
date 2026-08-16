# `ASH-BASETRAIN-VRAM-HOT-WEIGHT-PAGE-RESIDENCY-R1`

## Atlas-Aware Generation-Bound VRAM Weight Residency

```text
ASH-BASETRAIN-VRAM-HOT-WEIGHT-PAGE-RESIDENCY-R1

Atlas-Aware VRAM Hot Page Cache /
Generation-Bound GPU Page Identity /
Forward-to-Backward Weight Reuse /

RAM Resident Pack as Miss Source /
No HDD Weight Read on GPU Miss /

Bounded VRAM Budget /
No Full VRAM Weight Residency Requirement /
No Activation-Starvation Fallback /

16MiB Page Geometry Preservation /
Atlas Reuse-Distance Eviction /

GPU Hit /
RAM Hit /
HDD Bootstrap Only /

Generation Promotion Invalidation /
No Stale Weight Reuse /

VRAM Cache Telemetry /
Hit Rate Inputs /
Miss Rate Inputs /
H2D Bytes Avoided /
Eviction Count /
Peak VRAM Residency
```

Receipt schema:

```text
ash.basetrain.vram_hot_weight_page_residency.v1
```

## 1. Parent authority

Required parent line:

```text
ASH-BASETRAIN-RAM-WEIGHT-PACK-PERSISTENT-RESIDENCY-AND-ATLAS-READAHEAD-R1
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1
R6A-R1 Packed Runtime Native Bootstrap / Accumulation Wave Residency
R6A-R2 Device-Limit-Aware Micro-Atlas / Vocab Row Paging
R6A-R2-R2 Subgroup32 Tiled Segment Gradient AdamW
CF1 Release Profile Authority
```

The runtime hierarchy becomes:

```text
Tier 0: VRAM hot decoder-weight residency
Tier 1: RAM ResidentWeightPack for the current generation
Tier 2: HDD durable packed state for bootstrap/resume/commit
```

HDD remains durable authority. RAM remains current-generation runtime weight-delivery authority. VRAM is a compute projection cache only.

## 2. Physical cache granularity

The current production compute route materializes a decoder layer as a Burn GPU tensor bundle, not as independently bindable 16 MiB raw page buffers.

R1 therefore uses the physical cache granularity:

```text
DECODER_BLOCK_GPU_BUNDLE_PAGE_ACCOUNTED
```

Meaning:

```text
physical residency object
= the exact GPU decoder bundle already created by the existing compute path

budget accounting unit
= canonical decoder source payload rounded upward to 16 MiB pages
```

This is intentional. R1 does not create a second raw-page VRAM cache that would leave the actual compute path re-uploading separate Burn tensors.

A later raw-page bind-path rewrite may change physical cache granularity, but R1 does not claim that rewrite.

## 3. 16 MiB page authority

The existing micro-Atlas page constant remains authoritative:

```text
16 MiB = 16,777,216 bytes
```

For each decoder layer:

```text
sourcePayloadBytes
= sum of the exact canonical safetensors byte ranges for the 9 decoder weight roles

pageCount
= ceil(sourcePayloadBytes / 16MiB)

pageAccountedBytes
= pageCount * 16MiB
```

No approximate layer-size table is introduced.

## 4. Explicit VRAM budget

New CLI:

```text
--admit-vram-hot-weight-page-residency
--vram-hot-weight-cache-budget-bytes <exact bytes>
```

R1 has no implicit default cache size.

Admission requires:

```text
budget >= 16 MiB
budget % 16 MiB = 0
budget < current ResidentWeightPack byte size
```

The final condition prevents silent whole-model VRAM promotion.

R1 does not claim a portable live-free-VRAM query from WGPU. Therefore activation non-starvation is not inferred from an invented free-VRAM value. The cache is bounded by the explicit physical harness budget, never auto-grows, and any unexpected device allocation failure remains fail-closed rather than silently shrinking or disabling the cache.

## 5. Cache identity

Conceptual page identity:

```text
generation
+ layer / parameter-group identity
+ page ordinal
```

Current physical cache entries are one decoder GPU bundle covering one or more page-accounted units.

A cache entry from generation N can never hit a generation N+1 request.

## 6. Lookup path

For decoder weight requests under R1:

```text
GPU cache lookup
  -> hit: reuse existing GPU decoder bundle, no second H2D
  -> miss: load exact current-generation bytes through RAM ResidentWeightPack,
           materialize the existing GPU decoder bundle once,
           admit it into the bounded cache
```

A GPU miss does not open the HDD source.

The Pass154 resident range session remains the miss source authority and continues to require:

```text
physical_source_open_count = 0
physical_source_read_bytes = 0
physical_source_seek_count = 0
```

after initial RAM residency.

## 7. Forward-to-backward reuse

Within one optimizer generation, decoder traversal is deterministic:

```text
forward:  layer 0 -> ... -> layer N-1
backward: layer N-1 -> ... -> layer 0
```

A decoder bundle first loaded during forward remains eligible for backward reuse if the bounded VRAM budget retains it.

On a backward hit:

```text
second RAM decode/upload = retired
second H2D weight upload = retired
```

The cache never changes forward or backward computation order.

## 8. Atlas reuse-distance eviction

R1 does not use wall-clock LRU as authority.

For a layer loaded during forward, the next deterministic use is its reverse-order backward visit.

Eviction priority is:

```text
1. no future use / already consumed
2. furthest deterministic next-use ordinal
3. deterministic layer-index tie break
```

Thus, under pressure, lower forward layers whose backward use is furthest away are evicted before near-future upper layers.

Same generation + same Atlas schedule + same cache budget must yield the same eviction decisions.

## 9. Pinned resource protection

A cache entry whose GPU bundle still has an external execution handle cannot be selected for eviction.

R1 uses the owned Arc handle count as the host-side lease boundary for cache-owned bundles.

If no eligible entry exists while a new bundle is required, the cache fails closed rather than evicting an in-use bundle.

## 10. Generation promotion invalidation

Optimizer commit changes weight generation.

Required order:

```text
candidate generation N+1 built
-> durable commit succeeds
-> RAM ResidentWeightPack N+1 is promoted
-> VRAM cache promote_generation(N+1)
-> all generation N cache entries logically invalidated and physically released
-> generation N+1 lookups may begin
```

VRAM cache invalidation never precedes durable/RAM promotion.

At promotion, any externally held old-generation bundle is a hard failure rather than stale reuse.

R1 does not implement cross-generation GPU successor continuity.

## 11. No stale reuse

Hard invariant:

```text
requested generation == cache active generation
```

Generation mismatch is:

```text
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_STALE_REUSE
```

No logical page equality may override generation identity.

## 12. RAM and HDD miss semantics

R1 requires Pass154 RAM residency.

```text
VRAM miss -> RAM resident source
RAM resident source unavailable -> FAIL
HDD fallback on GPU miss -> FORBIDDEN
```

Terminal receipt requires:

```text
ramMissCount = 0
hddWeightReadOnGpuMissBytes = 0
staleWeightReuseCount = 0
```

## 13. Cache budget state

Canonical cache state includes:

```text
activeGeneration
cacheBudgetBytes
residentPageCount
residentBytes
peakResidentPageCount
peakResidentBytes
entries
seenLayers
telemetry
```

`residentBytes` is page-accounted and must never exceed `cacheBudgetBytes`.

The cache has no runtime auto-growth path.

## 14. Existing transport preservation

R1 does not create a second upload ring, second WGPU device, or second queue authority.

A cache miss uses the existing decoder materialization/upload path. Existing R6A-R2 micro-Atlas and 3-slot transport authorities remain unchanged for the routes that already use them.

R1 does not falsely claim that the decoder GPU bundle is physically carried by a newly created 16 MiB raw-page ring.

## 15. No full-model GPU promotion

Forbidden:

```text
create one GPU buffer sized to the full ResidentWeightPack
preload every decoder layer regardless of demand
silent whole-model promotion because VRAM appears available
```

The cache is demand-filled and bounded.

## 16. Cache telemetry

New receipt:

```text
basetrain_vram_hot_weight_page_residency_receipt.json
```

Core fields:

```text
cacheEntryGranularity
cacheBudgetBytes
cachePageBytes
cachePageCapacity
lookupCount
gpuHitCount
gpuMissCount
staleLookupCount
h2dUploadCount
h2dUploadBytes
h2dBytesAvoided
evictionCount
evictedPageCount
reuseDistanceEvictionCount
generationInvalidationCount
generationPromotionCount
peakResidentPageCount
peakResidentBytes
forwardToBackwardHitCount
forwardToBackwardBytesAvoided
duplicateUploadSuppressedCount
sameGenerationPageReloadCount
ramMissCount
hddWeightReadOnGpuMissBytes
staleWeightReuseCount
cacheBudgetExceededCount
fullGpuWeightResidency
cacheAutoGrowthCount
activationStarvationFallbackCount
trainingMathChangeCount
optimizerMathChangeCount
```

Hit rate and H2D avoidance ratio are derived evidence, not correctness gates.

## 17. Physical success criteria

For an eight-step N8 physical run:

```text
generationPromotionCount = 8
ramMissCount = 0
hddWeightReadOnGpuMissBytes = 0
staleWeightReuseCount = 0
cacheBudgetExceededCount = 0
fullGpuWeightResidency = false
cacheAutoGrowthCount = 0
activationStarvationFallbackCount = 0
trainingMathChangeCount = 0
optimizerMathChangeCount = 0
```

Performance evidence should report:

```text
gpuHitCount
gpuMissCount
forwardToBackwardHitCount
h2dUploadBytes
h2dBytesAvoided
evictionCount
sameGenerationPageReloadCount
peakResidentBytes
```

No minimum hit-rate percentage is a correctness gate in R1.

## 18. Expected physical behavior

With a useful bounded cache:

```text
forward warmup
-> initial misses and H2D
-> cache fills

upper backward layers
-> forward-to-backward GPU hits
-> H2D avoided

lower layers beyond cache capacity
-> deterministic miss/reload from RAM resident source
```

The exact hit count depends on model layer geometry and the explicit cache budget.

## 19. Failure semantics

Representative failures:

```text
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_CACHE_BUDGET_EXCEEDED
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_STALE_REUSE
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_PAGE_EVICTED_WHILE_IN_FLIGHT
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_RAM_SOURCE_MISS
FAIL_ASH_BASETRAIN_VRAM_WEIGHT_HDD_FALLBACK_FORBIDDEN
VRAM_HOT_WEIGHT_FULL_MODEL_RESIDENCY_FORBIDDEN
VRAM_HOT_WEIGHT_CACHE_BUDGET_BELOW_ONE_PAGE
VRAM_HOT_WEIGHT_CACHE_BUDGET_NOT_16MIB_ALIGNED
```

No failure may trigger silent HDD fallback, cache disablement, budget auto-growth, Adam eviction, quantization, batch shrink, or training semantic change.

## 20. PASS tokens

```text
PASS_ASH_BASETRAIN_VRAM_HOT_WEIGHT_PAGE_RESIDENCY_R1_STATIC
PASS_ASH_BASETRAIN_VRAM_HOT_WEIGHT_PAGE_RESIDENCY_R1
PASS_ASH_BASETRAIN_ATLAS_AWARE_VRAM_WEIGHT_CACHE_R1
PASS_ASH_BASETRAIN_VRAM_WEIGHT_GENERATION_INVALIDATION_R1
PASS_ASH_BASETRAIN_VRAM_HOT_WEIGHT_PAGE_RESIDENCY_AND_FORWARD_BACKWARD_REUSE_R1
```

## 21. Static validation

New validator:

```text
tools/validate_vram_hot_weight_page_residency_r1_static.py
```

It is appended to the CF1 static validator chain and verifies:

```text
CLI/config/literal closure
explicit 16MiB-aligned budget
RAM residency dependency
bounded cache authority
full-model residency rejection
exact canonical decoder source-byte accounting
Atlas deterministic reuse-distance eviction
pinned-entry eviction rejection
forward/backward cache acquisition
RAM resident miss source
no HDD fallback semantics
durable-then-RAM-then-VRAM generation promotion order
receipt and telemetry closure
no auto growth
no silent activation-starvation fallback
no CUDA core dependency
no training math change
no optimizer math change
```

The prior R6A-R1 validator is updated only to recognize either direct decoder-block loading or cache-mediated decoder-block acquisition outside the lane loop. Its original wave-first/lane-fanout semantic requirement is unchanged.

## 22. Non-goals

R1 does not implement:

```text
cross-generation GPU successor continuity
full-model VRAM residency
raw 16MiB per-page shader bind rewrite
new GPU device or queue
new upload ring
CUDA runtime
VRAM auto-sizing from guessed free memory
cache auto-growth
Adam eviction
Adam quantization
training math change
optimizer math change
gradient math change
checkpoint semantic rewrite
dataset streaming rewrite
```

## 23. Final SSOT

```text
DURABLE AUTHORITY
= HDD packed state

CURRENT HOST WEIGHT DELIVERY
= RAM ResidentWeightPack

HOT COMPUTE PROJECTION
= bounded generation-bound GPU decoder bundle cache

CACHE BUDGET UNIT
= 16 MiB page-accounted exact canonical source bytes

PHYSICAL CACHE ENTRY
= existing GPU decoder bundle

GPU HIT
= existing bundle reused, second H2D retired

GPU MISS
= current-generation RAM resident source only

GPU MISS -> HDD
= forbidden

EVICTION
= deterministic Atlas future reuse distance

WALL-CLOCK LRU
= not authority

FORWARD -> BACKWARD REUSE
= allowed inside same generation

GENERATION PROMOTION
= durable commit
-> RAM resident promotion
-> VRAM generation invalidation

CROSS-GENERATION HIT
= forbidden

FULL GPU MODEL RESIDENCY
= forbidden as silent promotion

CACHE AUTO GROWTH
= 0

TRAINING MATH CHANGE
= 0

OPTIMIZER MATH CHANGE
= 0
```
