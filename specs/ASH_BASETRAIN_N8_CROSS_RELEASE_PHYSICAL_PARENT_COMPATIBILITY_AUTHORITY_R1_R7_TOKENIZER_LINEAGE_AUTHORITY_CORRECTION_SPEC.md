# ASH-BASETRAIN-N8-CROSS-RELEASE-PHYSICAL-PARENT-COMPATIBILITY-AUTHORITY-R1-R7

## Purpose

Separate physical tokenizer lineage authority from stale dataset tokenizer-spec provenance.

## Observed failure

Physical sealing reached:

```text
ASH_N8_CROSS_RELEASE_TOKENIZER_SPEC_LINEAGE_MISMATCH
```

This occurs only after the stronger parent-cursor tokenizer lineage check has passed:

```text
active.datasetCursor.tokenizerLineageId
== current TokenizerManifest.manifestId
```

Therefore `dataset.lineage.tokenizerSpecId` must not silently override the physical cursor's tokenizer lineage ownership.

## Authority correction

R1-R7 records dataset tokenizer-spec lineage as an immutable observation:

```text
datasetLineageTokenizerSpecId
datasetLineageTokenizerSpecIdExact
datasetLineageTokenizerSpecIdAuthoritativeForParentState = false
```

The physical tokenizer lineage remains fail-closed on the cursor manifest binding. The current tokenizer manifest must also pass its canonical self-hash validation. Dataset bytes and dataset-builder identity remain exact.

## Runtime revalidation

Runtime revalidates that the dataset tokenizer-spec observation has not drifted and that the sealed equality result is still truthful:

```text
ASH_N8_CROSS_RELEASE_RUNTIME_DATASET_TOKENIZER_LINEAGE_DRIFT
ASH_N8_CROSS_RELEASE_RUNTIME_DATASET_TOKENIZER_LINEAGE_OBSERVATION_DRIFT
ASH_N8_CROSS_RELEASE_DATASET_TOKENIZER_LINEAGE_AUTHORITY_FICTION
```

The retired hard gates are:

```text
ASH_N8_CROSS_RELEASE_TOKENIZER_SPEC_LINEAGE_MISMATCH
ASH_N8_CROSS_RELEASE_RUNTIME_TOKENIZER_SPEC_LINEAGE_MISMATCH
```

## Evidence boundary

R1-R7 still does not claim historical raw tokenizer JSON byte equality:

```text
tokenizerHistoricalContentDigestClaimed = false
```

No dataset rewrite. No tokenizer rewrite. No physical parent mutation. No N2 replay. No compatibility repair.
