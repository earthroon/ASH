# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-LAYER-RANGE-PROJECTION-POPULATION-FRONTIER-06C-R27-R1I

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-LAYER-RANGE-PROJECTION-POPULATION-FRONTIER-06C-R27-R1I`
- Build revision: `bt-wgsl-checkpoint-export-layer-range-projection-population-frontier-06c-r27-r1i`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-PROJECTION-FAMILY-ZERO-ORIGIN-SCAN-06C-R27-R1H`
- Primary target layers: `19, 20, 21`
- Projection roles: `Q/K/V/O/Gate/Up/Down`
- RMS controls: `input_layernorm`, `post_attention_layernorm`
- Checkpoint repair authority: `NONE`
- GPU / backward / optimizer authority: `OUT_OF_SCOPE`
- Proof ledger: `HOLD`

## Parent SSOT

R27-R1H physically established the complete checkpoint projection-family zero topology:

```text
checkpoint_layer_count=22
projection_scan_complete_count=154
rms_scan_complete_count=44

Layers 0..19: Q/K/V/O/Gate/Up/Down = NONZERO
Layer20: Q/K/V/O/Gate/Up = ZERO, Down = NONZERO
Layer21: Q/K/V/O/Gate/Up/Down = ZERO

Q/K/V/O/Gate/Up first_zero_layer=20
Down first_zero_layer=21
projection_role_revival_count=0
shared_projection_first_zero_layer=20
shared_projection_first_zero_count=6
projection_zero_origin_distinct_layer_count=2
checkpoint_projection_zero_origin_pattern=MONOTONIC_PROJECTION_FAMILY_COLLAPSE
projection_rms_correlation=PROJECTION_ZERO_RMS_HEALTHY
```

R1I does not reopen checkpoint read transport, source range resolution, raw scanning, GPU projection execution, backward math, optimizer state carry, R26 commit or R27 override copy.

## Primary question

R1I determines the earliest physically supported boundary at which the Layer19 -> Layer20 -> Layer21 projection topology became zero:

```text
E0 SOURCE_PARAMETER
E1 WRITER_SOURCE_BINDING
E2 PRE_SERIALIZE
E3 DESTINATION_RANGE / NO_WRITE
E4 WRITE_EXECUTION / PARTIAL_WRITE
E5 POST_WRITE_RANGE
E6 FINAL_CHECKPOINT_RANGE
```

The finished checkpoint being zero is not itself evidence that the exporter caused the zero.

## Export provenance admission

R1I first establishes whether authoritative generation/export provenance exists.

Possible states:

```text
EXPORT_PROVENANCE_AVAILABLE
EXPORT_PROVENANCE_PARTIAL
EXPORT_PROVENANCE_UNAVAILABLE
```

A canonical exact provenance sidecar may be admitted only as:

```text
ASH_CHECKPOINT_EXPORT_PROVENANCE_V1.json
schema_id=ash.checkpoint.export.provenance.v1
schema_version=1
```

The sidecar must bind exactly to the current checkpoint identity and checkpoint-set digest. It must contain explicit source parameter evidence and real writer iteration evidence for all 27 Layer19/20/21 base-role targets.

Existing ASH G146/G147/G148 receipts may be probed as historical evidence, but they do not become current checkpoint writer authority merely because their filenames exist. Unless they bind the exact current checkpoint identity/digest and contain the required per-tensor export evidence, they remain partial evidence only.

If no authoritative provenance is physically available:

```text
checkpoint_export_frontier_root_cause=CHECKPOINT_EXPORT_PROVENANCE_UNAVAILABLE
checkpoint_export_repair_authorized=false
recommended_next_frontier=CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_FRONTIER
```

This is a valid fail-closed diagnostic result. R1I must not fabricate past telemetry.

## Canonical target registry

R1I reuses the existing `DECODER_WEIGHT_REGISTRY_ORDER` and `DecoderWeightRole::tensor_key(layer)` authority.

Target matrix:

```text
3 layers x 7 projections = 21 projection records
3 layers x 2 RMS controls = 6 control records
Total = 27
```

The exact final checkpoint payload digests and nonzero counts for these 27 records are retained from R1H and bound into R1I. No second final-checkpoint inference authority is created.

## Source parameter evidence

When export provenance is available, every target record must contain:

```text
source_parameter_present
source_semantic_role_match
source_layer_ordinal_match
source_identity
source_version
source_dtype
source_shape
source_element_count
source_zero_count
source_nonzero_count
source_nonfinite_count
source_payload_digest
```

The authoritative source must be independent of the finished checkpoint bytes being diagnosed.

If the source tensor is already numeric zero, the first zero stage is `E0` and checkpoint exporter repair is not authorized.

## Writer source binding

Per target:

```text
writer_iteration_ordinal
writer_source_identity
writer_source_version
writer_source_dtype
writer_source_shape
writer_source_element_count
```

Writer order is determined only from the real writer iteration ordinal. It must not be inferred from canonical role order, tensor-key lexical order or destination file offset.

A nonzero authoritative source bound to another/wrong source is classified as a writer source-binding frontier.

## Pre-serialize witness

Immediately before serialization:

```text
pre_serialize_zero_count
pre_serialize_nonzero_count
pre_serialize_nonfinite_count
pre_serialize_digest
```

Strong transition:

```text
SOURCE_NONZERO + PRE_SERIALIZE_ZERO
-> CHECKPOINT_EXPORT_PRE_SERIALIZE_POPULATION_ZERO
```

## Destination lifecycle

Per target:

```text
destination_file_identity
destination_shard_identity
destination_offset
destination_span
destination_range_allocated
destination_prewrite_zero_initialized
write_intent_created
write_started
bytes_written
write_complete
```

Allocation is not a write. Zero initialization is not serialization. A zero-initialized destination published without a complete write is a separate lifecycle failure.

Partial/short writes are never accepted as valid numeric-zero tensor serialization.

## Post-write witness

After write completion:

```text
post_write_numeric_zero_count
post_write_numeric_nonzero_count
post_write_digest
```

The post-write digest is compared with the exact final physical checkpoint digest retained by R1H.

Strong distinctions:

```text
source NONZERO -> pre-serialize ZERO
= source population / pre-serialize frontier

pre-serialize NONZERO -> no write
= required role skipped / traversal frontier

pre-serialize NONZERO -> partial write
= partial tensor write

pre-serialize NONZERO -> post-write ZERO
= serialization zero corruption

post-write NONZERO -> final checkpoint ZERO
= post-export range mutation

source ZERO
= source parameter zero pattern, not exporter repair
```

## Tensor transition classes

Every physically evidenced target may classify as:

```text
ZERO_ALREADY_IN_SOURCE
SOURCE_NONZERO_BINDING_ZERO
SOURCE_NONZERO_PRE_SERIALIZE_ZERO
PRE_SERIALIZE_NONZERO_NO_WRITE
PRE_SERIALIZE_NONZERO_PARTIAL_WRITE
PRE_SERIALIZE_NONZERO_POST_WRITE_ZERO
POST_WRITE_NONZERO_FINAL_ZERO
NONZERO_PRESERVED_END_TO_END
EVIDENCE_INSUFFICIENT
```

The earliest physically proven zero boundary wins.

## Layer20 Down survivor

R1H established:

```text
Layer20 Q/K/V/O/Gate/Up = ZERO
Layer20 Down = NONZERO
```

R1I therefore requires the actual Layer20 Down writer iteration ordinal whenever provenance is available, along with the six Layer20 failed projection writer ordinals.

Only real writer order may determine whether an exact traversal cutoff separates the survivor from the six zero roles:

```text
YES_EXACT_CUTOFF
NO_CUTOFF_PATTERN
EVIDENCE_INSUFFICIENT
```

The R1H topology alone may not be translated into a writer cutoff claim.

## Layer21 continuation

R1I determines whether Layer21's full seven-role zero state is:

```text
SAME_EXPORT_FAILURE_CHAIN
DISTINCT_LAYER21_FAILURE
ZERO_ALREADY_IN_SOURCE
EVIDENCE_INSUFFICIENT
```

Again, this classification requires source/export provenance and is not inferred from final checkpoint bytes alone.

## Aggregate root causes

Evidence-bound root classes include:

```text
CHECKPOINT_SOURCE_PARAMETER_ZERO_PATTERN
CHECKPOINT_EXPORT_SOURCE_PARAMETER_BINDING_FAILURE
CHECKPOINT_EXPORT_LAYER_BINDING_FAILURE
CHECKPOINT_EXPORT_PROJECTION_ROLE_FAMILY_POPULATION_FAILURE
CHECKPOINT_EXPORT_SOURCE_ITERATOR_EARLY_EXHAUSTION
CHECKPOINT_EXPORT_LAYER_RANGE_TRAVERSAL_CUTOFF
CHECKPOINT_EXPORT_REQUIRED_ROLE_SKIPPED
CHECKPOINT_EXPORT_PRE_SERIALIZE_POPULATION_ZERO
ZERO_INITIALIZED_DESTINATION_PUBLISHED_WITHOUT_COMPLETE_WRITE
CHECKPOINT_EXPORT_PARTIAL_TENSOR_WRITE
CHECKPOINT_EXPORT_SERIALIZATION_ZERO_CORRUPTION
CHECKPOINT_POST_EXPORT_RANGE_MUTATION
CHECKPOINT_EXPORT_ZERO_FALLBACK
CHECKPOINT_EXPORT_FALSE_SUCCESS
CHECKPOINT_EXPORT_ZERO_INTRODUCTION_CONFIRMED
CHECKPOINT_EXPORT_PROVENANCE_UNAVAILABLE
CHECKPOINT_EXPORT_FRONTIER_EVIDENCE_INSUFFICIENT
```

## Repair authorization

Exporter repair is authorized only when the authoritative source parameter is physically nonzero and a later E1-E6 stage introduces the zero.

```text
checkpoint_export_repair_authorized = source_nonzero && later_zero_proven
```

If source parameters already contain the zero topology:

```text
checkpoint_export_repair_authorized=false
source_parameter_population_frontier_required=true
```

## Mutation boundary

R1I is forensic only.

Required zeros:

```text
checkpoint_export_repair_execution=0
checkpoint_write=0
checkpoint_rewrite=0
source_parameter_mutation=0
weight_value_mutation=0
writer_retry_injection=0
writer_fallback_injection=0
automatic_checkpoint_replacement=0
gpu_dispatch_count=0
optimizer_dispatch=0
```

A diagnostic replay must never overwrite the canonical checkpoint and may not be treated as historical telemetry.

## Semantic waves

R1I emits 12 sequential semantic waves:

```text
00 R1H physical parent
01 export provenance / source-output identity
02 target role registry
03 source parameter evidence
04 writer source binding
05 writer traversal ledger
06 destination lifecycle
07 Layer19 healthy control
08 Layer20 six-zero + Down survivor frontier
09 Layer21 full-zero frontier
10 first export-zero / aggregate repair domain
11 reproducibility / negative canaries / handoff
```

Receipt contract:

```text
receipt_atlas_waves=12
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
duplicate_key_fail_closed=1
monolithic_final_json=0
```

## CLI authority

Exactly 48 R1I gates are required:

```text
--require-bt-wgsl-r27r1i-contract-001
...
--require-bt-wgsl-r27r1i-contract-048
```

They must exist exactly once in short args, full args, dedicated R1I contract args and regenerated resolved args.

Expected repair-script output:

```text
r27r1i_required_gate_count=48
r27r1i_gate_cardinality_exact=1
```

## Negative canaries

At least 26 canaries cover final-zero-to-writer blame, output-as-source substitution, Layer20/21 source rebinding, writer-order inference from offsets/role order, allocation-as-write, zero-init-as-serialization, no-write/partial-write acceptance, ignored source/pre/post transitions, missing-source zero fallback, source iterator exhaustion, writer skip, false success, error-to-zero substitution, Layer19 control omission, RMS omission, fabricated historical telemetry, non-equivalent replay, canonical checkpoint overwrite, checkpoint repair and source-parameter mutation.

## Reproducibility

R1I collects two complete provenance snapshots against the same immutable checkpoint identity.

Exact parity includes:

```text
provenance availability
canonical/legacy receipt evidence
target final checkpoint identities/digests
source identities
writer records when available
writer iteration ordinals
transition classes
root cause
repair flags
recommended next frontier
```

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

## BaseTrain authority

R1I remains diagnostic:

```text
full_model_gradient_authority=0
full_model_training_state_authority=0
basetrain_gradient_value_admission_ready=0
```

## PASS semantics

R27-R1I PASS means the Layer19/20/21 final checkpoint topology from R1H was handed to a source/export frontier without assuming exporter guilt. Exact export provenance was either bound through a current-checkpoint identity-sealed provenance sidecar or explicitly classified as partial/unavailable. When per-tensor provenance is available, each target is classified from source parameter through writer binding, pre-serialize state, destination lifecycle, write completion, post-write bytes and final checkpoint bytes using real writer iteration order. Export repair is authorized only when a nonzero source becomes zero after E0. When provenance is unavailable, R1I fails closed to `CHECKPOINT_EXPORT_PROVENANCE_UNAVAILABLE` rather than fabricating historical writer telemetry. No checkpoint or source parameter is mutated.

PASS does not mean the exporter is defective, that writer traversal stopped at Layer20, that buffer exhaustion or offset overflow occurred, or that the checkpoint should be regenerated automatically.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_LAYER_RANGE_PROJECTION_POPULATION_FRONTIER_06C_R27_R1I
```
