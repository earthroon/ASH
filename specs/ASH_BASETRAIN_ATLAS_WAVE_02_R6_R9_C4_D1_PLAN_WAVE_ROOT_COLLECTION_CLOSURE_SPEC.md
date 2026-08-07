# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4-D1

## Decoder Weight Plan Wave Root Collection Closure / Artifact Receipt Global Root-Key Uniqueness Preservation / Nested Plan-Wave Collection Binding / Duplicate-Key Fail-Closed Preservation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4`  
> Observed physical failure: `R6R9C1ArtifactAtlasRootKeyCollision` while serializing the C4 plan receipt  
> Failure class: artifact receipt construction / root-key ownership collision  
> Decoder weight planner math: unchanged  
> Decoder weight transport: `NOT_EXECUTED`  
> Active transport: `checkpoint-resolved-full-layer-loader`  
> Proof ledger: `HOLD` until C4-D1 physical PASS

## 1. Observed failure

C4 successfully reached the physically admitted C3 parent and entered the C4 planner receipt path, then failed with:

```text
R6R9C1ArtifactAtlasRootKeyCollision:
r6_r9.c4.decoder_weight_atlas_wave.plan_receipt:
decoder-weight-plan-wave-0001:
decoder-weight-plan-wave-0001:
decoderWeightPlanWave
```

The `ArtifactReceiptParallelStreamingWaveMap` intentionally owns one globally unique flat root-key namespace across all artifact receipt waves. C4 emitted one artifact receipt wave per decoder payload-plan wave while inserting the same root key `decoderWeightPlanWave` for every plan wave. Wave 0 inserted the key successfully. Wave 1 attempted to insert the same root key and was correctly rejected by the global duplicate-key fail-closed guard.

This is not a decoder weight packing failure and not a checkpoint span failure. It is an artifact serialization ownership mismatch.

## 2. Forbidden workaround

C4-D1 must not weaken duplicate-key fail-closed, global root-key uniqueness, wave ordinal validation, lane ordinal validation, lane-name validation, or streaming deterministic merge.

Forbidden workarounds include duplicate root overwrite, last-writer-wins, deleting earlier plan waves, randomized root-key suffixes, process-address/timestamp-derived keys, hash-prefix-generated schema keys, recursion-limit increases, or monolithic `json!` fallback.

## 3. Correct ownership model

Decoder weight plan waves are payload-plan descriptors. They are a collection owned by one plan receipt field, not independent artifact-root authorities.

C4-D1 therefore introduces one domain-explicit nested collection:

```text
decoderWeightPlanWaves: [
  planWave0,
  planWave1,
  ...
]
```

The artifact receipt map inserts this collection exactly once.

Required root fields:

```text
decoderWeightPlanWaveCollectionSchema
decoderWeightPlanWaveCollectionDigest
decoderWeightPlanWaveCount
decoderWeightPlanWaves
```

Required schema:

```text
ash.basetrain.decoder_weight_atlas_wave.plan_wave_collection.v1
```

## 4. Domain separation

After D1:

```text
DecoderWeightAtlasWavePlan.wave_count
  = decoder payload-plan wave cardinality

ArtifactReceiptParallelStreamingWaveMap.wave_count
  = metadata serialization wave cardinality
```

They are deliberately not required to be equal.

The plan-wave collection is serialized in one artifact receipt wave named `decoder-weight-plan-wave-collection`.

Artifact receipt layout becomes:

```text
artifact wave 0  identity-and-policy
artifact wave 1  registry-and-span-binding
artifact wave 2  memory-and-plan-summary
artifact wave 3  decoder-weight-plan-wave-collection
artifact wave 4  planner-closure
```

This does not collapse or alter the decoder payload-plan waves inside the nested collection.

## 5. Collection digest binding

Canonical collection digest:

```text
SHA256(canonical serde serialization of plan.waves)
```

The digest is emitted as `decoderWeightPlanWaveCollectionDigest` and rebound into the C4-D1 final receipt, local manifest, and terminal physical receipt line.

The planner's existing `planDigest` remains independent. `planDigest`, `planReceiptDigest`, `decoderWeightPlanWaveCollectionDigest`, and `artifactReceiptWaveMapDigest` are distinct authorities and may not be aliased.

## 6. Planner identity preservation

The planner remains the C4 planner:

```text
plannerPatchId = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4
plannerBuildRevision = r6-r9-c4-decoder-weight-atlas-wave-plan-v1
```

The closure receipt identity is promoted to:

```text
patchId = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4-D1
buildRevision = r6-r9-c4-d1-plan-wave-root-collection-closure-v1
```

This preserves the distinction between the unchanged C4 planner algorithm and the D1 artifact-serialization closure.

## 7. Runtime semantics unchanged

C4-D1 does not change the canonical nine weight roles, checkpoint tensor span binding, dtype/shape/element validation, `ordered-greedy-contiguous-v1` packing, byte budget, parallel decode lane plan, canonical commit ordinals, per-wave fence plan, planned peak byte accounting, mega-atlas planning count, cross-wave payload overlap planning count, or runtime weight authority planning count.

Runtime state remains:

```text
planner payload reads = 0
planner GPU module creates = 0
planner weight-slot mutations = 0
planner hidden-slot mutations = 0
transport execution = NOT_EXECUTED
active transport = checkpoint-resolved-full-layer-loader
```

## 8. State ownership

No ownership moves in D1.

```text
checkpoint tensor metadata
  = checkpoint authority

planner
  = DecoderWeightAtlasWavePlan

plan-wave collection
  = artifact serialization projection of plan.waves

resident runtime weights
  = BaseTrainLayerWeightResidencySlot

hidden state
  = LayerHiddenAuthoritySlot
```

The nested collection is not a second planner authority and not a runtime payload owner.

## 9. Changed source

Semantic changes:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
```

The base-train C4 planner module itself is unchanged. No WGSL semantic changes are introduced.

## 10. Static closure checks

```text
legacy root key `decoderWeightPlanWave` insertion count = 0
root key `decoderWeightPlanWaves` insertion count = 1
plan-wave collection schema = present
plan-wave collection digest = present
plan-wave collection count = plan.wave_count
plan-wave collection payload = plan.waves
artifact plan receipt literal root-key duplicates = 0
ArtifactReceipt duplicate-key fail-closed implementation = unchanged
artifact receipt plan-wave descriptor wave count = 1 collection wave
artifact receipt closure ordinal = 4
C4 planner algorithm source changed = false
R6-R7 active loader semantic change = 0
WGSL semantic changed file count = 0
```

## 11. Physical PASS requirements

A C4-D1 PASS requires the existing C3 parent to remain PASS and the C4 planner to complete without root-key collision.

Expected terminal fields:

```text
target_layer=2
roles=9
waves=<checkpoint-derived plan wave count>
lanes=9
budget=268435456
workers=4
max_lanes=4
peak_wave_transient=<derived>
mega_atlas=0
cross_wave_overlap=0
runtime_weight_authority=0
planned_transport=decoder-weight-atlas-wave
active_transport=checkpoint-resolved-full-layer-loader
transport_executed=0
plan_digest=<digest>
plan_wave_collection_digest=<digest>
artifact_root_key_collision=0
proof_ledger=HOLD
```

PASS proves only planner plus artifact-serialization closure. Actual decoder-weight wave payload execution remains blocked.

## 12. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## 13. Admission after PASS

```text
R6-R9-C3 wave-domain split                  = ADMITTED
R6-R9-C4 decoder-weight wave planner        = ADMITTED_PLANNER_ONLY
R6-R9-C4-D1 artifact collection closure     = ADMITTED on physical PASS
DecoderWeightAtlasWave transport            = BLOCKED_NOT_EXECUTED
LayerWeightBuildStagingSlot                 = BLOCKED / C5
wave-built Layer-2 rebind                   = BLOCKED / C6
wave-loader execution parity                = BLOCKED / C7
canonical wave-loader adoption              = BLOCKED / C8
```

## Seal

> C4-D1 does not make duplicate keys legal. It corrects the ownership model: many decoder payload-plan waves are members of one nested `decoderWeightPlanWaves` collection, while the artifact receipt root remains globally unique and fail-closed.
