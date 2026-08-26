# ASH-BASETRAIN-N8-CROSS-RELEASE-PHYSICAL-PARENT-COMPATIBILITY-AUTHORITY-R1-R5

## Status

Semantic authority correction for R1 model identity after physical sealing exposed stale dataset lineage metadata.

## Observed conflict

The current guarded Phase-A dataset manifest is byte-exactly bound by the physical N2 cursor, but its lineage still records:

```text
model_tinyllama_1p1b_v4
```

The current model specification is:

```text
model_tinyllama_1p1b_v5_48259
```

These are not interchangeable model specifications. The v4 and v5 vocabularies differ, so R1 must not silently rewrite the dataset manifest or pretend the lineage strings are equal.

## Authority correction

The dataset manifest owns dataset provenance. Its `lineage.model_spec_id` is observed historical dataset metadata, not the physical packed N2 model-state SSOT.

R1-R5 therefore records the lineage comparison but removes it as a hard model-compatibility gate:

```text
datasetLineageModelSpecId = observed dataset value
datasetLineageModelSpecIdExact = observed equality result
datasetLineageModelSpecIdAuthoritativeForParentState = false
```

For the currently observed manifest, `datasetLineageModelSpecIdExact` is expected to be false.

## Physical model-state authority

The immutable physical N2 packed parameter registry is the model-state authority for cross-release consumption.

The current `ModelSpec` is admitted only if the existing production atlas planner can resolve the physical packed parent exactly:

```text
modelPlan.modelSpecId == current ModelSpec.modelSpecId
resolvedTensorCount = 201
missingTensorCount = 0
```

The physical parameter names, shapes, byte offsets, packed spans, embedding rows, and LM-head rows must therefore be consumable without conversion by the current model planner.

A stale dataset lineage cannot hide a vocabulary-shape mismatch because embedding and LM-head topology are validated from the actual immutable packed state.

## Evidence boundary

R1-R5 does not claim historical raw model TOML equality:

```text
producerModelRawFileDigestClaimed = false
```

`modelIdentityExact` in the retained R1 receipt schema means exact state-consumption model identity established by physical packed topology. It does not mean dataset-lineage-string equality, source-tree equality, or historical raw model file parity.

## No repair

```text
No dataset manifest mutation /
No lineage rewrite /
No physical parent rewrite /
No optimizer state migration /
No N2 replay /
No source-tree equality fiction /
No kernel-math parity claim /
```

## Fail-closed rules

The correction does not weaken physical compatibility. R1 still fails if the current production model planner cannot resolve all 201 physical tensors exactly, if any packed shape/offset/length is incompatible, or if any physical payload digest drifts.

Representative model failures become:

```text
ASH_N8_CROSS_RELEASE_MODEL_STATE_TOPOLOGY_MISMATCH
ASH_N8_CROSS_RELEASE_MODEL_PLAN_SPEC_ID_MISMATCH
ASH_N8_CROSS_RELEASE_MODEL_TOPOLOGY_MISMATCH
ASH_N8_CROSS_RELEASE_DATASET_MODEL_LINEAGE_AUTHORITY_FICTION
```

`ASH_N8_CROSS_RELEASE_MODEL_SPEC_LINEAGE_MISMATCH` is retired as an admission failure because that field is not the physical-parent model authority.

## Receipt truth

A valid authority may therefore contain:

```text
datasetLineageModelSpecId = model_tinyllama_1p1b_v4
datasetLineageModelSpecIdExact = false
datasetLineageModelSpecIdAuthoritativeForParentState = false
modelStateTopologyExact = true
modelIdentityExact = true
producerModelRawFileDigestClaimed = false
```

This is not a compatibility repair. It is an explicit separation between dataset provenance metadata and physical model-state ownership.
