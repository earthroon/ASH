# ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1

## 1. Patch identity

```text
ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1

SourceState Generation Authority /
Disk·RAM·VRAM Route Invariance /
Residency Generation Parity Witness /
Zero Fallback Elimination /
Gradient Fence·Optimizer Bind Continuity Seal
```

Build revision:

```text
n8-source-weight-generation-ssot-r1
```

## 2. Parent failure

The parent N8 physical run reached native bootstrap, exact subgroup32 admission,
scheduler horizon extension, Atlas runtime route admission, and R14 owner-pin validation,
then failed at optimizer provenance binding:

```text
ASH_TRAINING_GENERATION_PROVENANCE_OPTIMIZER_BIND_FAILED
Caused by:
ASH_TRAINING_PROVENANCE_SOURCE_WEIGHT_GENERATION_MISMATCH
```

The resume source was generation 5, but the wave-resident execution path derived
`source_weight_generation` from optional residency objects. When both RAM resident
weight-pack and VRAM hot-weight cache were absent, that path synthesized generation 0.
The gradient-generation fence therefore carried 0 while the optimizer binding authority
still carried the real source generation 5.

This is a state-ownership defect. It is not an optimizer-math, gradient-math, scheduler,
subgroup, TensorCube, or Atlas computation defect.

## 3. Generation authority

The single semantic authority is:

```text
SourceState.generation
```

The current optimizer-step source generation is captured once at step entry:

```text
source_generation_snapshot = SourceState.generation
```

That snapshot is passed explicitly into wave execution and remains the source-generation
identity for the entire optimizer transaction.

The authority chain is:

```text
SourceState.generation
        -> source_generation_snapshot
        -> wave execution admission
        -> BaseTrainAtlasWaveGenerationFence.source_weight_generation
        -> finalized gradient provenance envelope
        -> optimizer generation binding
```

No storage or cache implementation may recreate or replace this value.

## 4. Disk·RAM·VRAM route invariance

Physical residency changes storage location only. It does not change semantic generation.
For a source generation `G`:

```text
Disk only:      effective generation = G
RAM resident:   effective generation = G
VRAM cache:     effective generation = G
RAM + VRAM:     effective generation = G
```

The runtime function receives `source_weight_generation: u64` explicitly from the
scheduler snapshot. It must not infer generation from whether a cache exists.

## 5. Residency generation parity witness

`ResidentWeightPack.generation()` and `GpuWeightPageCache.active_generation()` are
parity witnesses only.

When present they must equal the SourceState-owned generation:

```text
ResidentWeightPack.generation == source_weight_generation
GpuWeightPageCache.active_generation == source_weight_generation
```

Mismatch is hard failure:

```text
R6AR1ResidentWeightPackSourceGenerationDrift
R6AR1VramHotWeightSourceGenerationDrift
```

The runtime must not silently repair SourceState from cache metadata and must not rewrite
cache generation merely to satisfy the check.

Decoder-block acquisition in the VRAM path uses the authoritative
`source_weight_generation`; the resident/cache generations are checked before use rather
than used to create the authority.

## 6. Zero fallback elimination

The forbidden behavior is synthetic authority creation:

```text
None => 0
unwrap_or(0)
unwrap_or_default()
```

when those expressions are used to invent source generation after residency lookup fails.

R1 does **not** declare numeric generation zero intrinsically invalid. If
`SourceState.generation` itself is authoritatively zero, zero remains a valid propagated
value. The prohibited case is:

```text
missing residency metadata -> fabricated generation 0
```

Therefore:

```text
authoritative zero         = preserved
synthetic fallback zero    = forbidden
```

## 7. Immutable step snapshot

At the start of each production optimizer loop:

```text
source_generation_snapshot = source.generation
```

The target generation is derived from that snapshot.

The scheduler preserves an explicit drift guard:

```text
N8SourceWeightGenerationSnapshotDrift
```

After wave execution it also requires:

```text
wave_execution.generation_fence.source_weight_generation
    == source_generation_snapshot
```

Failure token:

```text
N8SourceWeightGenerationFenceDrift
```

This prevents a mid-step state-owner drift from being hidden by later provenance sealing.

## 8. Gradient fence and optimizer continuity

The finalized gradient envelope is sealed from the wave generation fence.
R1 requires:

```text
training_gradient_batch_envelope
    .training_generation
    .source_weight_generation
== source_generation_snapshot
```

Failure token:

```text
N8SourceWeightGenerationGradientFenceDrift
```

The optimizer binding receives the same snapshot as its
`source_training_generation` authority.

The existing hard guard remains unchanged:

```text
ASH_TRAINING_PROVENANCE_SOURCE_WEIGHT_GENERATION_MISMATCH
```

R1 fixes the producer-side ownership error and does not weaken, bypass, wildcard, or
remove that provenance guard.

## 9. Runtime diagnostic

For N8 long-horizon admission the wave runtime emits a structured diagnostic under:

```text
[ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1]
```

It records:

```text
authority=source_state
sourceGeneration=<G>
residentWeightPackPresent=<bool>
residentWeightPackGeneration=<G|null>
residentWeightPackGenerationMatch=<bool|null>
vramHotWeightCachePresent=<bool>
vramHotWeightGeneration=<G|null>
vramHotWeightGenerationMatch=<bool|null>
syntheticZeroFallbackUsed=0
```

This diagnostic is evidence only. It does not become a new generation authority.

## 10. Static validator

Canonical validator:

```text
tools/validate_ash_basetrain_n8_source_weight_generation_ssot_r1_static.py
```

It seals:

- patch identity and revision,
- explicit wave `source_weight_generation` argument,
- `SourceState.generation` step snapshot,
- target generation derived from that snapshot,
- scheduler-to-wave propagation,
- RAM and VRAM parity-witness semantics,
- absence of cache-derived source authority,
- absence of synthetic zero fallback,
- VRAM acquire calls using source authority,
- runtime source-state diagnostic,
- snapshot/fence/gradient drift guards,
- optimizer binding using the same snapshot,
- preservation of the existing optimizer provenance mismatch guard,
- step receipt generation continuity,
- CF1 registration,
- Disk/RAM/VRAM/RAM+VRAM invariance fixtures,
- resident and VRAM mismatch negative fixtures,
- authoritative zero preservation fixture.

Static promotion tokens:

```text
PASS_ASH_BASETRAIN_N8_SOURCE_WEIGHT_GENERATION_SSOT_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_SOURCE_WEIGHT_GENERATION_ROUTE_INVARIANCE_R1
PASS_ASH_BASETRAIN_N8_SOURCE_WEIGHT_GENERATION_GRADIENT_OPTIMIZER_CONTINUITY_R1
```

## 11. CF1 integration

The validator is included in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Because this patch modifies the `base_train` source authority, the Release CF1 receipt
must be regenerated after applying the overlay. A pre-patch CF1 receipt must not be used
with the rebuilt runtime binary.

The existing compile/runtime binary identity guard remains authoritative.

## 12. Existing validator contract repair

The prior persistent FFN resource validator expected generation to be derived from
resident/cache objects. That expectation is retired.

`validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py`
now requires:

```text
explicit source generation argument
resident generation parity witness
VRAM generation parity witness
no synthetic zero generation fallback
```

This is a validator-authority correction, not a resource-slab semantic change.

## 13. Baked implementation surface

R1 changes only these implementation/validator surfaces:

```text
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
tools/validate_ash_basetrain_n8_source_weight_generation_ssot_r1_static.py
tools/validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The baked overlay intentionally excludes artifacts, generated manifests, `.sha256`
sidecars, and Python cache output.

## 14. Static evidence at bake time

Observed in the bake worktree:

```text
N8 source-weight generation SSOT:                       28/28 PASS
FFN persistent resource slab/bindgroup validator:       68/68 PASS
Training generation provenance closure:                198/198 PASS
N8 long-horizon continuity:                             70/70 PASS
RAM weight-pack persistent residency/read-ahead:        67/67 PASS
VRAM hot-weight page residency:                         70/70 PASS
GPU successor weight commit continuity:                 52/52 PASS
```

The R6A-R1 full static validator and scheduler-profile validator could not be completed
inside the bake container because their required `specs/` fixtures are not present in the
lightweight worktree. This is an evidence limitation, not a PASS claim.

Cargo/Rust physical compilation is also not claimed from the bake container. Release CF1
on the authoritative ASH checkout remains required.

## 15. Non-goals / semantic no-change boundary

R1 does not change:

- training equations,
- gradient equations,
- AdamW or Muon equations,
- scheduler policy or learning-rate values,
- gradient accumulation count,
- checkpoint serialization format,
- parameter numerical values,
- subgroup32 execution semantics,
- TensorCube topology,
- Atlas wave ordering,
- R14 owner-pin semantics,
- Stage11 merge semantics,
- generation increment policy.

Only generation ownership, propagation, parity checking, and provenance continuity are
changed.

## 16. Physical acceptance

The physical N8 reproducer must begin from the promoted generation-5 source and prove:

```text
source generation snapshot                = 5
wave generation fence source generation   = 5
gradient envelope source generation       = 5
optimizer binding source generation       = 5
synthetic zero fallback                    = 0
```

The prior error must not recur:

```text
ASH_TRAINING_PROVENANCE_SOURCE_WEIGHT_GENERATION_MISMATCH
```

Physical promotion token:

```text
PASS_ASH_BASETRAIN_N8_SOURCE_WEIGHT_GENERATION_PHYSICAL_R1
```

Final promotion token:

```text
PROMOTE_ASH_BASETRAIN_N8_SOURCE_WEIGHT_GENERATION_SSOT_R1
```

These physical/final tokens are not considered satisfied by static bake evidence alone.

## 17. Final SSOT statement

```text
SourceState.generation owns training-generation truth.
Disk, RAM, and VRAM residency may witness that truth but may never create,
replace, infer, default, or silently repair it.
```
