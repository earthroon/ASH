# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-AND-WRITER-LINEAGE-06C-R27-R1J

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-AND-WRITER-LINEAGE-06C-R27-R1J`
- Build revision: `bt-wgsl-checkpoint-export-provenance-capture-and-writer-lineage-06c-r27-r1j`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-LAYER-RANGE-PROJECTION-POPULATION-FRONTIER-06C-R27-R1I`
- Capture schema: `ash.checkpoint.export.provenance.capture.r1j.v1`
- Canonical R1I sidecar schema: `ash.checkpoint.export.provenance.v1`
- Canonical sidecar: `ASH_CHECKPOINT_EXPORT_PROVENANCE_V1.json`
- Proof ledger: `HOLD`

## Parent SSOT

R27-R1I physically established that the current checkpoint has a known Layer19/20/21 zero topology but no source/writer provenance:

```text
export_provenance_status=EXPORT_PROVENANCE_UNAVAILABLE
source_parameter_evidence_count=0
writer_iteration_evidence_count=0
target_write_expected_count=27
target_write_unobservable_count=27
checkpoint_export_repair_authorized=false
```

R1J therefore captures a future live export. It does not reconstruct historical writer events from the already-written checkpoint.

## Live capture boundary

R1J observes the final full checkpoint export only. Existing intermediate `full_step_*` checkpoint writes remain on the unmodified checkpoint writer path.

Capture is opt-in through:

```text
ASH_R1J_CAPTURE_CHECKPOINT_EXPORT=1
```

When capture is disabled, `write_full_checkpoint_safetensors_with_r1j_capture()` delegates directly to the existing `write_full_checkpoint_safetensors()` path.

The implementation does not replace or ship a guessed `checkpoint.rs`. The retained public checkpoint writer remains the checkpoint-byte owner. R1J wraps the final call and records source/pre-serialize evidence before the writer, then verifies the resulting physical safetensors ranges after writer completion.

## Forensic target set

The layer window is runtime-derived:

```text
L = checkpoint_layer_count
forensic_layers = [L-3, L-2, L-1]
```

Current expected model:

```text
L=22
forensic_layers=19,20,21
```

The existing `DECODER_WEIGHT_REGISTRY_ORDER` is the single role authority. Per layer R1J captures:

```text
input_layernorm
self_attn_q_proj
self_attn_k_proj
self_attn_v_proj
self_attn_o_proj
post_attention_layernorm
mlp_gate_proj
mlp_up_proj
mlp_down_proj
```

Current target cardinality:

```text
3 layers * 9 roles = 27
21 projection records
6 RMS control records
```

No second handwritten role registry is authoritative.

## Captured stages

For each target R1J records evidence corresponding to:

```text
E0 source parameter
E1 writer source binding / serializer input ordinal
E2 exact F32 pre-serialize stream
E3 destination safetensors range
E4 writer completion evidence
E5 independently scanned physical output range
```

The final checkpoint identity used by R1I remains the canonical checkpoint authority and is not rederived by the capture wrapper.

## Source and pre-serialize evidence

Before the retained checkpoint writer is invoked, the final checkpoint snapshots are inspected in place. For every forensic target R1J records:

```text
source tensor identity and generation
canonical layer and semantic role
F32 shape and element count
numeric zero/nonzero/nonfinite counts
SHA256 of the exact F32 byte stream
```

The source payload is also the pre-serialize payload for the current identity-F32 writer contract. No duplicate full tensor payload buffer is created for provenance.

The source parameter authority and source model identity are deterministically sealed from the live final snapshots and configured run/model/spec generation identity.

## Writer ordering evidence

The capture wrapper assigns a serializer-input ordinal before invoking the retained checkpoint writer. The current writer revision is sealed as:

```text
base_train.checkpoint.write_full_checkpoint_safetensors.btreemap_serialize_to_file.v1
```

After serialization, R1J parses only the safetensors header and requires physical `data_offsets` order to exactly match the pre-writer serializer-input order. A mismatch fails closed.

The 27 canonical target records themselves are stored in semantic order:

```text
layer ordinal ascending
then DECODER_WEIGHT_REGISTRY_ORDER ordinal ascending
```

A separate writer-traversal digest is built by sorting records by the live serializer-input ordinal.

## Destination and post-write evidence

After the retained checkpoint writer successfully returns, R1J opens the newly written checkpoint read-only and scans only the 27 exact target payload ranges in bounded 4 MiB chunks.

Per target it records:

```text
destination relative offset and span
physical bytes observed
numeric zero/nonzero counts
physical post-write digest
```

Required current identity-F32 parity:

```text
source/pre-serialize digest == physical post-write digest
source zero/nonzero counts == physical post-write zero/nonzero counts
```

The wrapper does not perform an extra full-checkpoint SHA pass. Full-file digest authority remains explicitly unavailable at this wrapper layer. Later R1J finalization binds the live journal to the already-canonical checkpoint identity and checkpoint-set digest.

## Live journal

A successful capture writes a non-authoritative live journal beside the new final checkpoint:

```text
<final-checkpoint>.ASH_CHECKPOINT_EXPORT_PROVENANCE_R1J_CAPTURE_V1.json
```

The journal is:

```text
captureSourceClass=LIVE_EXPORT_CAPTURE
captureStatus=CAPTURE_COMPLETE
realExportEventObserved=true
authoritative=false
```

It contains compact metadata, scalar counts, digests, destination ranges and lineage only. It contains no copied tensor payloads.

## R1J gate finalization

The BaseTrain R1J gate runs after R1I and binds the live journal to the current `BaseTrainAtlasWave02R5CheckpointTensorSetAuthority`.

If no journal exists, R1J returns:

```text
capture_status=CAPTURE_ARMED_EXPORT_REQUIRED
real_export_event_observed=0
target_write_unobservable_count=27
r1i_handoff_ready=0
physical_pass=false
```

and emits:

```text
HOLD_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_AND_WRITER_LINEAGE_06C_R27_R1J_EXPORT_EVENT_REQUIRED
```

No PASS is allowed merely because instrumentation exists.

When a live journal exists, R1J requires exact schema, layer/role/key geometry, source/writer identity, F32 transform, write completion and post-write parity for all 27 records. It reuses the R1G/R1H `direct_scan()` physical scanner against the current canonical checkpoint authority and requires exact journal-to-authority physical digest/count parity.

## Canonical sidecar promotion

Only a complete live capture bound to the current checkpoint authority may be promoted to:

```text
ASH_CHECKPOINT_EXPORT_PROVENANCE_V1.json
```

The canonical sidecar binds:

```text
checkpoint_identity
checkpoint_set_digest
source_model_identity
source_parameter_authority_identity
writer_revision
export_schema_revision
checkpoint_generation_invocation_identity
target records
capture / target / writer-traversal digests
```

It is directly parseable by existing R1I. An existing canonical sidecar may only be reused when its bytes are exactly identical. Identity drift or collision fails closed.

Current R1I compatibility additionally requires the current 22-layer, `[19,20,21]` target window because R1I's existing forensic target contract is fixed to that physical parent.

## Same-invocation ordering

The current gate sequence is:

```text
R1I
then R1J
```

Therefore the first gate run after a live captured export may allow R1J to publish the canonical provenance sidecar, while R1I in that same invocation has already executed. The gate must be run again so R1I can consume `ASH_CHECKPOINT_EXPORT_PROVENANCE_V1.json` and perform E0-to-E6 causal classification.

R1J does not itself assign exporter/source guilt.

## Mutation boundary

R1J necessarily observes a newly written final checkpoint, but the checkpoint payload remains owned by the existing exporter.

Required distinctions:

```text
diagnostic/new final export checkpoint write = allowed
existing investigated checkpoint mutation = 0
source parameter mutation = 0
weight repair = 0
optimizer mutation = 0
gradient mutation = 0
checkpoint repair execution = 0
automatic checkpoint replacement = 0
```

Capture instrumentation must not alter intermediate checkpoint writes or the checkpoint payload policy.

## Receipt and CLI authority

R1J emits 12 semantic waves with streaming chunk receipts and a small final envelope.

```text
receipt_atlas_waves=12
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

Exactly 48 gates are required:

```text
--require-bt-wgsl-r27r1j-contract-001
...
--require-bt-wgsl-r27r1j-contract-048
```

The resolved-args repair must report:

```text
r27r1j_required_gate_count=48
r27r1j_gate_cardinality_exact=1
```

At least 30 negative canaries cover historical reconstruction, output-as-source substitution, wrong role/layer bindings, inferred writer ordering, partial/no-write publication, stale capture adoption, sidecar identity mismatch, incomplete targets and forbidden mutation/repair.

## Reproducibility

R1J takes two independent snapshots of the live journal/current checkpoint binding and requires exact equality before sidecar promotion.

The capture journal itself is deterministic over semantic target records and a separate writer traversal view. Local absolute filesystem paths are not used as payload authority.

## PASS semantics

R27-R1J physical PASS means a real final checkpoint export produced a complete live provenance journal, all 27 forensic source/pre-serialize records were bound to exact physical post-write checkpoint ranges, the current checkpoint authority independently reproduced those physical ranges, and an authoritative R1I-compatible sidecar was published without mutating the source parameters or existing investigated checkpoint.

PASS does not mean the exporter caused the zero topology, the source parameters caused it, Layer20 is a writer cutoff, or training authority is reopened.

If no live export occurred, HOLD is the correct result.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_AND_WRITER_LINEAGE_06C_R27_R1J
```

## HOLD seal

```text
HOLD_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_AND_WRITER_LINEAGE_06C_R27_R1J_EXPORT_EVENT_REQUIRED
```
