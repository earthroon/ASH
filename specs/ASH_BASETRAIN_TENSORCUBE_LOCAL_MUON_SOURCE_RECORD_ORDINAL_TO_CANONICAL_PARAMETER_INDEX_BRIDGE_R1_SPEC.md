# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-SOURCE-RECORD-ORDINAL-TO-CANONICAL-PARAMETER-INDEX-BRIDGE-R1

## Status

Production correctness closure for TensorCube Local Muon parameter identity.

This patch separates two previously conflated index spaces:

- `source.records` physical packed traversal ordinal
- TensorCube Local Muon registry canonical parameter index

The patch does not reorder packed state and does not alter optimizer math.

## Trigger

A physical N8 production run reached TensorCube Local Muon and failed with:

`FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PRODUCTION_REGISTRY_DRIFT`

The production scheduler iterated:

`source.records.iter().enumerate()`

and passed that physical source-record ordinal directly into APIs whose contract is canonical parameter identity.

## SSOT

### Physical packed traversal authority

`SourceState.records`

Owns:

- source record ordinal
- physical parameter traversal order
- weight byte offset
- Adam-M byte offset
- Adam-V byte offset
- packed payload order

### Canonical optimizer identity authority

`FirstCandidateEligibilityRegistry.parameters`

Owns:

- parameter ID
- canonical parameter index
- Muon/AdamW optimizer route
- Muon grid geometry
- momentum base element offset

### Bridge authority

The bridge is constructed once before each physical optimizer parameter traversal from exact parameter IDs:

`Source Record Ordinal -> Source Parameter ID -> Registry Vector Index -> Registry Declared Canonical Index`

The resulting source-ordinal-to-canonical-index vector is immutable for the traversal.

## Required closure

```text
Source Record Count /
Registry Parameter Count /

Every Source Parameter ID Found Exactly Once /
No Duplicate Source Parameter ID /
No Duplicate Registry Parameter ID /
No Missing Registry Binding /
No Extra Source Binding /

Registry Vector Index /
Registry Declared Canonical Index /
Exact Equality /

Source Record Ordinal /
Source Parameter ID /
Canonical Parameter Index /

Mapping Cardinality Exact /

No Source Record Reorder /
No Packed Offset Rewrite /
No Registry Rewrite /
No Optimizer Routing Rewrite /
No Momentum Offset Rewrite /
```

## Registry preflight

For every registry route at vector index `i`:

- `route.canonical_index == i`
- parameter ID is unique
- canonical index is unique

Fail closed tokens:

- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_REGISTRY_CANONICAL_INDEX_DRIFT`
- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_REGISTRY_DUPLICATE_CANONICAL_INDEX`
- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_REGISTRY_DUPLICATE_PARAMETER_ID`

No registry rewrite is permitted.

## Source inventory preflight

Every `SourceState.records[*].parameter_id` must be unique.

Fail closed:

`FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_SOURCE_DUPLICATE_PARAMETER_ID`

The exact source/registry identity sets must match.

Fail closed:

- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_EXTRA_SOURCE_BINDING`
- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_MISSING_REGISTRY_BINDING`
- `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_SOURCE_REGISTRY_CARDINALITY_MISMATCH`

No ordinal fallback is permitted.

## Runtime binding

Rename the physical traversal index conceptually from `parameter_index` to `source_record_ordinal`.

The packed manifest `parameter_index` field continues to use the physical source record ordinal. This preserves packed source order and byte layout.

Before Muon routing, resolve:

`canonical_parameter_index = bridge[source_record_ordinal]`

The canonical parameter index is then the only index passed into:

- `muon_parameter_geometry`
- `packed_index_for_logical`
- `project_parameter_gradient_provenance`
- `execute_muon_parameter`
- `route_span`

The existing runtime guard remains intact:

`route.parameter_id == parameter_id`

The patch must not remove or relax `FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PRODUCTION_REGISTRY_DRIFT`.

## Receipt

Filename:

`tensorcube_local_muon_source_record_canonical_parameter_bridge_receipt.json`

Schema:

`ash.basetrain.tensorcube_local_muon.source_record_canonical_parameter_bridge.v1`

Required fields:

- `sourceGeneration`
- `sourceOptimizerStep`
- `targetGeneration`
- `targetOptimizerStep`
- `sourceRecordCount`
- `registryParameterCount`
- `mappingCardinality`
- `sourceParameterIdUnique`
- `registryParameterIdUnique`
- `registryCanonicalIndexUnique`
- `missingRegistryBindingCount`
- `extraSourceBindingCount`
- `registryVectorCanonicalIndexMismatchCount`
- `sourceRecordOrderMutationCount`
- `packedOffsetRewriteCount`
- `registryMutationCount`
- `optimizerRoutingRewriteCount`
- `momentumOffsetRewriteCount`
- `bindings[]`
- `passToken`

Each binding contains:

- `sourceRecordOrdinal`
- `sourceParameterId`
- `registryVectorIndex`
- `registryDeclaredCanonicalIndex`
- `canonicalParameterIndex`
- `exactParameterIdMatch`
- `vectorCanonicalIndexExact`

Pass token:

`PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_SOURCE_RECORD_CANONICAL_PARAMETER_BRIDGE_R1`

Runtime admission token:

`PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_SOURCE_RECORD_CANONICAL_PARAMETER_ADMISSION_R1`

## PASS conditions

All of the following must hold:

- source record count equals registry parameter count
- mapping cardinality equals source record count
- all source parameter IDs unique
- all registry parameter IDs unique
- all registry canonical indices unique
- every registry vector index equals its declared canonical index
- missing registry binding count is zero
- extra source binding count is zero
- source record order mutation count is zero
- packed offset rewrite count is zero
- registry mutation count is zero
- optimizer routing rewrite count is zero
- momentum offset rewrite count is zero

## Regression matrix

### Canonical physical order

Registry: `A B C D`

Source: `A B C D`

Expected mapping: `0->0, 1->1, 2->2, 3->3`.

### Reordered physical source

Registry: `A B C D`

Source: `A C B D`

Expected mapping:

- source ordinal 0 / A -> canonical 0
- source ordinal 1 / C -> canonical 2
- source ordinal 2 / B -> canonical 1
- source ordinal 3 / D -> canonical 3

Physical source order remains `A C B D`.

### Fail-closed fixtures

Reject:

- duplicate source parameter ID
- duplicate registry parameter ID
- duplicate canonical index
- registry vector/canonical index drift
- source parameter missing from registry
- registry parameter missing from source
- source/registry cardinality mismatch

## Performance contract

Bridge construction occurs outside the per-parameter Muon hot operation.

Hot traversal performs only direct vector lookup by source record ordinal.

Forbidden:

- registry scan per element
- string lookup per element
- string lookup per Muon tile
- source-record reorder to force ordinal equality

## Non-mutation contract

```text
No Source Record Reorder /
No Packed Offset Rewrite /
No Registry Rewrite /
No Optimizer Routing Rewrite /
No Momentum Offset Rewrite /

No Training Math Change /
No Gradient Math Change /
No Learning Rate Change /
No Weight Decay Change /
No Muon Kernel Change /
No AdamW Kernel Change /
No Scheduler Semantic Change /

No Registry Drift Guard Removal /
No Parameter-ID Fallback /
No Canonical-Index Arithmetic Inference /
```

## N8 continuation rule

The failing N8 Muon-new-lineage run terminated before a durable Muon momentum commit. Therefore the first retry after this patch still requires the one-shot new-lineage admission.

After the first successful durable Muon momentum commit, later resumes must not request new-lineage admission.
