# ASH-BASETRAIN-N8-CROSS-RELEASE-PHYSICAL-PARENT-COMPATIBILITY-AUTHORITY-R1-R6

## Purpose

Close the remaining runtime contradiction after R1-R5 separated dataset provenance metadata from physical model-state authority.

## Defect

R1-R5 removed the sealing-time hard requirement that `dataset.lineage.modelSpecId == current ModelSpec.modelSpecId`, but runtime revalidation still contained the obsolete gate:

```text
ASH_N8_CROSS_RELEASE_RUNTIME_MODEL_LINEAGE_MISMATCH
```

That gate incorrectly reassigned physical-parent model authority back to dataset lineage metadata.

## R1-R6 authority rule

Runtime treats dataset model lineage as an immutable observation recorded in the sealed authority:

```text
dataset.lineage.modelSpecId
== authority.inputIdentity.datasetLineageModelSpecId

(dataset.lineage.modelSpecId == current ModelSpec.modelSpecId)
== authority.inputIdentity.datasetLineageModelSpecIdExact

authority.inputIdentity.datasetLineageModelSpecIdAuthoritativeForParentState
== false
```

Physical parent model compatibility remains owned by the packed parameter registry and current production model planner.

## Fail closed

Runtime rejects drift or authority fiction with:

```text
ASH_N8_CROSS_RELEASE_RUNTIME_DATASET_MODEL_LINEAGE_DRIFT
ASH_N8_CROSS_RELEASE_RUNTIME_DATASET_MODEL_LINEAGE_OBSERVATION_DRIFT
ASH_N8_CROSS_RELEASE_DATASET_MODEL_LINEAGE_AUTHORITY_FICTION
```

The retired failures are not valid R1-R6 execution results:

```text
ASH_N8_CROSS_RELEASE_MODEL_SPEC_LINEAGE_MISMATCH
ASH_N8_CROSS_RELEASE_RUNTIME_MODEL_LINEAGE_MISMATCH
```

## Non-goals

No dataset manifest rewrite. No model spec rewrite. No parent mutation. No compatibility repair. No N2 replay. No raw historical model-file parity claim. No kernel-math parity claim.
