# `ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1`

## Production Hybrid Optimizer Callsite / Local Muon + AdamW Exact Route Partition

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1

Production Hybrid Optimizer Callsite Adoption /
First Candidate Eligibility Registry Authority /
Optimizer Routing Digest Authority /
No Runtime Shape Guess /

Full 16x16 Tile Local Muon /
Exact AdamW Residual Preservation /
No Dual Optimizer Authority /
No Writable Overlap /
No Candidate Hole /

Pass157 Multi-Tile Batch Executor Adoption /
GPU Segmented-Gradient Tile Packing /
No Muon Gradient D2H /
RAM Resident Weight Source /
No Muon HDD Weight Read /

F32 Local Muon Momentum Authority /
Explicit New-Lineage Zero Initialization Once /
No Zero-Momentum Resume Fallback /
No Momentum Reconstruction /

36GiB Process Budget Admission /
Exact Muon Momentum RAM Ownership /
Fail-Stop Run-Local In-Place Momentum Candidate /
Durable Momentum Sidecar Before Active Commit /

Whole-Step Hybrid Candidate Commit /
Pass154 RAM Residency Preservation /
Pass155 VRAM Hot Cache Preservation /
Pass156 Generation Ordering Preservation /
```

Receipt schema: `ash.basetrain.tensorcube_local_muon_production_callsite.v1`.

## Parent authority

This revision is parented by the Pass157 line through `ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-MULTI-TILE-BATCH-DISPATCH-R1`, Pass156 GPU successor continuity, Pass155 VRAM hot residency, Pass154 RAM weight residency, the Local Muon optimizer/first-candidate registry line, RAM36, and CF1 Release authority.

Pass157 established a physically batched Local Muon executor but intentionally left production training with `HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_MULTI_TILE_PRODUCTION_CALLSITE_NOT_PRESENT_R1`. Pass158 binds that executor to the production hybrid optimizer path.

## Optimizer semantic boundary

Pass158 intentionally changes optimizer routing for registry-admitted elements. It does not claim that all elements preserve AdamW optimizer math. The allowed change is exactly the registered Local Muon route; unregistered optimizer route changes and silent substitutions remain zero.

## Production routing SSOT

The single routing authority is the existing `FirstCandidateEligibilityRegistry` and its `modelSpecDigest`, `parameterInventoryDigest`, `optimizerRoutingDigest`, and `registryDigest`. Runtime code must not re-decide Local Muon eligibility by tensor-shape heuristics.

The existing candidate projection families are Q/K/V/O and Gate/Up/Down. Only complete 16x16 tiles are Local Muon routed. All non-candidate parameters and all candidate edge residuals remain AdamW routed.

For the complete trainable set `T`, `T = M union A` and `M intersect A = empty`, where `M` is the registry-admitted full-tile Local Muon set and `A` is the exact AdamW set.

Required terminal route invariants are: `unclassifiedElementCount = 0`, `overlapElementCount = 0`, `writableOverlapElementCount = 0`, `unwrittenCandidateElementCount = 0`, `runtimeShapeGuessCount = 0`, `silentMuonExpansionCount = 0`, and `silentAdamwFallbackCount = 0`.

## Production gradient authority

Production gradients already exist as bounded GPU segment leases. Pass158 introduces a WGPU gradient packer that maps those segment leases into the packed full-tile layout required by the Pass157 executor entirely on GPU. Local Muon routing does not read gradient payloads back to CPU.

The packer verifies WGSL u32 indexability, `max_buffer_size`, `max_storage_buffer_binding_size`, and each source gradient binding size before dispatch. Device-limit failures are fail-closed and never switch to CPU materialization.

Required counters: `muonGradientPayloadReadbackCount = 0` and `muonGradientPayloadReadbackBytes = 0`.

## Pass157 batch executor adoption

Every Local Muon production parameter uses `TensorCubeLocalMuonBatchExecutor`. The legacy one-tile/one-submit/one-wait execution topology is forbidden in the production route. One workgroup remains one 16x16 tile, and many workgroups are grouped into device-limit-bounded physical batches. `legacyPerTileMuonExecutorUsed = false` is mandatory.

## Current weight source

Current-generation Local Muon source weights come from the Pass154 `ResidentWeightPack`. No Local Muon source weight HDD read is permitted after residency. Required: `muonWeightDiskReadBytes = 0`.

## Hybrid candidate assembly

For a registry-admitted parameter, Pass158 gathers only full-tile Local Muon source weights, packs segmented gradients on GPU, executes the Pass157 batch executor, streams the full parameter from the current RAM resident source for candidate serialization, writes Local Muon candidate elements from the packed output, and executes existing AdamW candidate math only on exact residual spans. Parameters without a Local Muon grid remain on the existing AdamW path.

Running AdamW over a whole candidate parameter and then overwriting Local Muon tiles is forbidden because that would evolve Adam M/V inside Local Muon-owned ranges and create dual optimizer state.

## Optimizer-state authority split

For Local Muon-owned elements, the weight update authority is Local Muon and the optimizer state authority is distinct F32 Local Muon momentum. Adam M/V semantic reads and optimizer writes are forbidden for those ranges.

For AdamW-owned elements, the existing RAM-resident Adam M/V remain authoritative and Local Muon momentum reads/writes are forbidden.

Legacy Adam M/V backing bytes may physically remain for compatibility but are not semantic optimizer authority for Local Muon ranges.

## Local Muon momentum authority

Local Muon momentum is a distinct F32 authority. Its exact runtime size is `muonEligibleElementCount * sizeof(f32)`, with deterministic offsets derived from the compact registry. FP16/BF16 momentum authority and Adam-M/V-as-Muon-momentum substitution are forbidden.

## New optimizer lineage and resume

An AdamW-only source checkpoint has no Local Muon momentum state, so the first hybrid adoption requires explicit `--admit-tensorcube-local-muon-new-lineage`. Only that first transition may zero-initialize exact F32 Local Muon momentum.

After a hybrid checkpoint exists, resume requires both Local Muon momentum sidecars. Missing momentum never means zero. `zeroMomentumResumeFallbackCount = 0` and `momentumReconstructionCount = 0` remain hard invariants.

Candidate slots carry `tensorcube_local_muon_momentum.f32.bin` and `tensorcube_local_muon_momentum_manifest.json`. The manifest binds generation, optimizer step, registry/routing/profile identity, element count, byte length, SHA256, and F32 dtype. The payload digest is computed while writing; no post-write full-file digest reread is required.

## RAM36 ownership

`HostRamOwner::TensorCubeLocalMuonMomentum` and the matching exact-inventory category are introduced. Before allocation, the exact momentum byte requirement is reserved under the existing 38,654,705,664-byte process hard limit, followed by post-materialization verification. There is no precision downgrade, HDD paging fallback, automatic route shrink, or RAM cap relaxation.

## Fail-stop run-local in-place momentum candidate

Pass158 deliberately avoids a full current-plus-full-candidate momentum duplication because the 36GiB process budget can be tight. The in-memory Local Muon momentum backing is updated run-locally during optimizer execution, then the exact candidate momentum sidecar is durably written and bound into transaction validation before active-state promotion.

This is not rollback-capable in-process mutation. If a later part of the optimizer step fails after in-memory momentum mutation, the process is fail-stop and that mutated state must not be reused as a valid authority. The prior durable checkpoint remains the restart authority. The receipt exposes `failStopInPlaceRamCandidate = true`.

## Hybrid commit order

The production order is: seal current-generation gradients, bind registry route identity, execute all Local Muon batches, execute all AdamW residual spans, close the full hybrid weight candidate, persist Local Muon momentum sidecar and manifest, bind the momentum digest into transaction validated/ready metadata, commit active training state durably, then advance the hybrid step counter.

A failed Local Muon batch or AdamW residual path prevents active-state promotion. Partial Local Muon or partial AdamW commits are forbidden.

## Storage-root publication

The storage authority publishes the Local Muon momentum manifest and payload alongside packed checkpoint state when present and verifies the payload digest from the manifest. Pre-Muon checkpoints with neither sidecar remain valid. Exactly one sidecar without the other fails with `StorageMuonMomentumSidecarSplitAuthority`. This prevents a hybrid runtime checkpoint from losing its optimizer state during publication to the storage root.

## Pass154 / Pass155 / Pass156 preservation

Pass154 remains the current-generation RAM weight delivery authority. Pass155 remains the bounded generation-bound decoder VRAM projection cache. Pass156 ordering remains durable candidate commit, RAM ResidentWeightPack successor promotion, then GPU generation transaction and old-generation invalidation.

Local Muon tile candidate buffers are not falsely treated as ready decoder GPU bundles for Pass156 successor warm-start.

## CLI admission

Production admission uses:

```text
--admit-tensorcube-local-muon-production-callsite
--tensorcube-local-muon-first-candidate-registry <path>
--tensorcube-local-muon-profile <path>
```

First hybrid lineage additionally requires `--admit-tensorcube-local-muon-new-lineage`.

Production Local Muon requires the existing RAM weight residency, RAM-resident Adam M/V, exact inventory, and RAM36 authorities. Nested per-step configs disable the production Local Muon flags so the outer production loop remains the single authority.

## Runtime profile

Pass158 includes `specs/tensorcube_local_muon_production_profile_r1.json` with profile ID `pass158-production-local-muon-hybrid-r1`, F32 momentum authority, `ZERO_NEW_OPTIMIZER_LINEAGE`, F32 NS working dtype, and no full-matrix/cross-cube/global orthogonality claim. Its canonical digest is `b33e19937cf638eaccce6b21bab5e3f2b908b87f0d4e8ebae1295890710a17e0`.

## Production receipt

The production run writes `basetrain_tensorcube_local_muon_production_callsite_receipt.json`, binding generation, registry/profile identity, route counts, Local Muon batch/dispatch/workgroup counts, optimizer-state authority counters, gradient readback counters, HDD read counters, candidate ownership counters, momentum lineage/persistence counters, commit counters, and registered/unregistered optimizer route changes.

Physical production success ultimately requires a nonzero production Local Muon callsite/tile/dispatch count, no legacy per-tile executor, no route gaps/overlaps, no Local-Muon-range Adam M/V semantic access, no AdamW-range Muon momentum access, zero Muon gradient D2H, zero Muon weight HDD reads, no partial commits, no zero-momentum resume fallback/reconstruction, and zero unregistered route changes.

## Non-N8 codecheck target

Pass158 includes `ash_basetrain_tensorcube_local_muon_production_callsite_adoption_r1`, a dedicated non-training binary. It validates the ModelSpec, FirstCandidateEligibilityRegistry, production profile, exact route partition, exact Local Muon momentum byte requirement, and production admission contract. It does not run N8 or training and does not claim physical optimizer performance.

This non-N8 target is the primary code/contract check before a later physical production adoption run.

## PASS tokens

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PRODUCTION_CALLSITE_ADOPTION_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_ADAMW_HYBRID_ROUTING_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PRODUCTION_BATCH_EXECUTOR_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_HYBRID_ATOMIC_COMMIT_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_DURABLE_MOMENTUM_STATE_R1
```

## Static validation

`tools/validate_tensorcube_local_muon_production_callsite_adoption_r1_static.py` is wired into CF1. It checks CLI/config closure, registry routing authority, production scheduler callsite, GPU gradient packing and live device-limit guards, Pass157 batch executor binding, exact hybrid residual semantics, F32 momentum sidecars, RAM36/inventory ownership, durable commit ordering, storage publication, receipt closure, and the non-N8 codecheck target.

## Non-goals

Pass158 does not implement subgroup32 Local Muon norm reduction, NS matmul vec4/transposed optimization, cross-parameter Muon batching, GPU decoder-bundle successor materialization from Muon tile candidates, full-model VRAM residency, Local Muon momentum quantization/paging, rollback-capable in-process momentum journaling, runtime route migration, or silent checkpoint optimizer migration.

## Final SSOT

```text
PRODUCTION OPTIMIZER = HYBRID LOCAL MUON + ADAMW
ROUTING AUTHORITY = FirstCandidateEligibilityRegistry
LOCAL MUON REGION = REGISTRY-ADMITTED COMPLETE 16x16 TILES ONLY
ADAMW REGION = EVERY OTHER TRAINABLE ELEMENT
RUNTIME SHAPE GUESS = FORBIDDEN
LOCAL MUON GRADIENT = GPU SEGMENT LEASES -> GPU PACKER -> PASS157 BATCH EXECUTOR
LOCAL MUON GRADIENT D2H = 0
LOCAL MUON WEIGHT SOURCE = CURRENT RAM ResidentWeightPack
LOCAL MUON HDD WEIGHT READ = 0
LOCAL MUON MOMENTUM = DISTINCT F32 AUTHORITY
FIRST HYBRID LINEAGE ZERO INIT = EXPLICIT ONCE
RESUME ZERO FALLBACK = FORBIDDEN
MUON RANGE ADAM M/V AUTHORITY = NONE
ADAMW RANGE MUON MOMENTUM AUTHORITY = NONE
CANDIDATE WRITER PER ELEMENT = EXACTLY ONE
WRITABLE OVERLAP = 0
CANDIDATE HOLE = 0
MUON MOMENTUM RAM CANDIDATE = RUN-LOCAL FAIL-STOP IN-PLACE
DURABLE MOMENTUM SIDECAR = REQUIRED BEFORE ACTIVE COMMIT
PARTIAL HYBRID COMMIT = FORBIDDEN
36GiB PROCESS CAP = PRESERVED / FAIL CLOSED
PASS154 RAM RESIDENCY = PRESERVED
PASS155 VRAM HOT CACHE = PRESERVED
PASS156 GENERATION ORDER = PRESERVED
UNREGISTERED OPTIMIZER ROUTE CHANGE = 0
```