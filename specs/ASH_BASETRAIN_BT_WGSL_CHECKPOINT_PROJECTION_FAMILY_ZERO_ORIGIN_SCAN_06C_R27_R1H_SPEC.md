# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-PROJECTION-FAMILY-ZERO-ORIGIN-SCAN-06C-R27-R1H

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-PROJECTION-FAMILY-ZERO-ORIGIN-SCAN-06C-R27-R1H`
- Build revision: `bt-wgsl-checkpoint-projection-family-zero-origin-scan-06c-r27-r1h`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-LAYER21-CHECKPOINT-PROJECTION-PAYLOAD-ZERO-SOURCE-FRONTIER-06C-R27-R1G`
- Checkpoint source authority: canonical decoder-weight checkpoint tensor-set authority
- Decoder layer count: runtime-derived, current physical parent `22`
- Projection roles per layer: `7`
- RMS control roles per layer: `2`
- Current projection scan cardinality: `22 * 7 = 154`
- Current RMS scan cardinality: `22 * 2 = 44`
- GPU execution authority: `NONE`
- Checkpoint mutation authority: `NONE`
- Proof ledger: `HOLD`

## Parent SSOT

R27-R1G physically established that Layer21 Q/K/V/O/Gate/Up/Down are numeric zero in the actual checkpoint source bytes, with exact canonical/direct range digest parity and raw-scanner parity. It also established the current anchor counts:

```text
checkpoint_layer_count=22
layer0_projection_nonzero_role_count=7
layer20_projection_nonzero_role_count=1
layer21_projection_nonzero_role_count=0
layer0_rms_nonzero_role_count=2
layer20_rms_nonzero_role_count=2
layer21_rms_nonzero_role_count=2
checkpoint_source_frontier_root_cause=LAYER21_CHECKPOINT_SOURCE_BYTES_NUMERIC_ZERO_CONFIRMED
```

R1H does not reopen the Layer21 source-byte verdict, checkpoint key/range transport, projection executor, R26 optimizer, R26 commit, R27 state carry or R27 override copy.

## Primary question

For each canonical decoder projection role Q/K/V/O/Gate/Up/Down, determine the first decoder layer whose physical checkpoint payload is numeric zero. Scan every layer because zero states are not assumed monotonic and a role may later revive.

Required per-role outputs:

```text
layer_state_vector
first_zero_layer
first_revival_layer
zero_layer_count
nonzero_layer_count
zero_suffix_contiguous
zero_transition_count
revival_transition_count
first_zero_source_shard
first_zero_payload_offset
first_zero_payload_span
role_zero_origin_class
```

## Scope

Canonical projection roles:

```text
self_attn_q_proj
self_attn_k_proj
self_attn_v_proj
self_attn_o_proj
mlp_gate_proj
mlp_up_proj
mlp_down_proj
```

Controls:

```text
input_layernorm
post_attention_layernorm
```

The canonical `DECODER_WEIGHT_REGISTRY_ORDER` and `DecoderWeightRole::tensor_key(layer)` remain the single role/key authority. No second guessed key registry is allowed.

## Runtime-derived matrix

For each layer ordinal `0..checkpoint_layer_count-1`, resolve all nine base roles through the canonical checkpoint tensor authority.

Current physical parent requires:

```text
projection_scan_expected_count=154
rms_scan_expected_count=44
```

PASS requires complete physical classification of all expected projection and RMS records. No binary search and no Layer0/20/21-only inference is allowed.

## Source descriptor preflight

Every tensor record is bound to:

```text
layer ordinal
semantic role
tensor key
source file identity
source shard identity
source shard relative path
dtype
shape
element count
payload offset
payload span
```

Missing keys, zero-length ranges, out-of-bounds ranges and unsupported dtypes fail closed. Missing tensors may not become zero tensors, empty tensors or nearest-layer fallbacks.

## Range alias authority

Within each layer, the seven projection ranges must not unexpectedly alias. Across layers, exact projection range reuse is also rejected unless future checkpoint metadata explicitly establishes parameter sharing.

Required current result:

```text
unexpected_projection_range_alias_count=0
unexpected_cross_layer_projection_range_alias_count=0
```

## Physical scanner SSOT

R1H reuses the R1G independent physical range scanner rather than creating a third scanner authority. The R1G scanner is exposed internally as a crate-visible diagnostic primitive while its existing R1G behavior remains unchanged.

The scanner:

```text
opens the authoritative local checkpoint source read-only
reads only the exact tensor payload range
uses bounded 4 MiB chunks
classifies F16/BF16/F32 zero directly from scalar bits
counts numeric zero/nonzero scalars
counts zero/nonzero bytes
computes exact payload SHA256
checks source file size/mtime before and after
performs zero GPU work
```

Actual scans are physically sorted by shard/file and payload offset. Logical receipt ordering remains deterministic by layer ordinal and canonical role ordinal.

## Tensor state authority

Every completed physical tensor receives exactly one primary state:

```text
NUMERIC_NONZERO
NUMERIC_ZERO
```

Read failure, unsupported dtype, invalid descriptor or missing key is a hard diagnostic failure and cannot be counted as numeric zero.

## R1G anchor parity

The full scan must reproduce the physical R1G anchors at Layers 0, 20 and 21.

Required current anchor parity:

```text
L0 projection nonzero = 7
L20 projection nonzero = 1
L21 projection nonzero = 0
L0 RMS nonzero = 2
L20 RMS nonzero = 2
L21 RMS nonzero = 2
r1g_anchor_parity=1
```

R1H does not preassign which Layer20 projection survives. Its semantic role is obtained from the runtime scan.

## Layer21 R1G digest parity

R1G retains the nine Layer21 independent physical source digests as a handoff surface. R1H re-scans the same immutable checkpoint ranges and requires exact digest parity:

```text
layer21_r1g_digest_parity_count=9
layer21_r1g_digest_mismatch_count=0
```

This confirms that R1H and R1G inspect the same physical source bytes.

## First-zero and revival semantics

For each projection role:

```text
first_zero_layer = minimum layer ordinal with NUMERIC_ZERO
```

After that layer, the first later `NUMERIC_NONZERO` layer is `first_revival_layer`.

`zero_suffix_contiguous=true` only if every layer from first zero through the final decoder layer remains zero.

Patterns such as `NONZERO -> ZERO -> NONZERO` must be preserved as discontinuous evidence rather than flattened into a suffix-zero assumption.

## Per-layer health vector

Every decoder layer emits:

```text
[Q,K,V,O,Gate,Up,Down]
[input_rms,post_rms]
projection_nonzero_role_count
projection_zero_role_count
rms_nonzero_role_count
rms_zero_role_count
```

For fully observed layers:

```text
projection_nonzero + projection_zero = 7
rms_nonzero + rms_zero = 2
```

## Projection origin classification

R1H supports:

```text
SINGLE_LAYER_PROJECTION_FAMILY_ZERO_ORIGIN
STAGGERED_PROJECTION_ZERO_ORIGIN
MONOTONIC_PROJECTION_FAMILY_COLLAPSE
DISCONTINUOUS_PROJECTION_ZERO_PATTERN
LEADING_PROJECTION_FAMILY_ZERO_PATTERN
MIXED_PROJECTION_ZERO_ORIGIN
CHECKPOINT_PROJECTION_ZERO_ORIGIN_EVIDENCE_INSUFFICIENT
```

Diagnostic tags may additionally record:

```text
ABRUPT_FULL_PROJECTION_FAMILY_ZERO_TRANSITION
STAGGERED_PROJECTION_ZERO_ORIGIN
MONOTONIC_PROJECTION_FAMILY_COLLAPSE
PROJECTION_ROLE_REVIVAL_PRESENT
```

The primary class remains single and evidence-bound.

## Shared origin

R1H derives the most populated first-zero layer group and emits:

```text
shared_projection_first_zero_layer
shared_projection_first_zero_count
projection_zero_origin_distinct_layer_count
projection_zero_origin_order
```

Ties preserve canonical role ordinal ordering.

## RMS correlation

Projection origins are compared with the full 22-layer RMS control timelines.

Possible correlations:

```text
PROJECTION_ZERO_RMS_HEALTHY
PROJECTION_ZERO_RMS_ZERO_SAME_LAYER
MIXED_RMS_CORRELATION
```

If RMS remains nonzero while projection families collapse, the next frontier remains projection-family/export specific rather than whole-base-block serialization.

## Shard and range correlation

For every first-zero role, retain its shard ID, payload offset and span. If the first-zero transition also changes source shard relative to the previous layer, record the correlation:

```text
projection_zero_origin_shard_boundary_match
projection_zero_origin_shard_boundary_match_count
```

This is correlation evidence only and never by itself proves a shard writer defect.

## Source-byte accounting

R1H reports actual successfully scanned bytes:

```text
projection_source_bytes_scanned
rms_source_bytes_scanned
total_source_bytes_scanned
```

No estimated byte counts are used.

## Scan digest

A deterministic `projection_family_scan_digest` seals:

```text
checkpoint identity
runtime layer count
all ordered physical tensor records
```

Logical order is layer ascending, then canonical role ordinal ascending.

## Reproducibility

Two complete physical R1H scans run against the same immutable checkpoint source.

Required exact equality includes:

```text
all source descriptors
all physical payload digests
all scalar zero/nonzero counts
all layer vectors
all role timelines
all first-zero/revival values
all aggregate classifications
all repair handoff fields
```

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

## Next-frontier handoff

R1H performs no checkpoint repair. It only selects a later source/export investigation class.

Current possible handoff surfaces include:

```text
CHECKPOINT_EXPORT_LAYER_RANGE_FRONTIER
CHECKPOINT_EXPORT_ROLE_FAMILY_FRONTIER
CHECKPOINT_SOURCE_PARAMETER_POPULATION_FRONTIER
CHECKPOINT_ZERO_ORIGIN_MIXED_FRONTIER
```

Examples:

- one shared first-zero layer or monotonic collapse: prioritize layer-range/export traversal frontier
- discontinuous revival: prioritize source parameter population/binding frontier
- staggered role-specific origins: prioritize projection-role export/source population frontier

The checkpoint payload origin layer is not claimed to equal the writer operation that introduced the value.

## Mutation boundary

R1H is read-only forensic diagnosis.

Required zeros:

```text
checkpoint_write=0
weight_repair_execution=0
weight_value_mutation=0
gpu_dispatch_count=0
gpu_allocation_count=0
gpu_upload_bytes=0
gpu_readback_bytes=0
decoder_forward_recompute=0
loss_recompute=0
backward_recompute=0
optimizer_dispatch=0
optimizer_state_read=0
optimizer_state_write=0
automatic_checkpoint_replacement=0
automatic_checkpoint_rewrite=0
automatic_weight_reinitialization=0
```

## Semantic waves

R1H emits 10 sequential semantic waves:

```text
00 R1G parent and checkpoint identity
01 projection/RMS source registry
02 range/shard preflight
03 layers 00-07 scan evidence
04 layers 08-15 scan evidence
05 layers 16-21 scan evidence
06 projection role timelines
07 RMS control correlation
08 zero-origin classification
09 reproducibility/canaries/handoff
```

Physical reads remain source-offset ordered even when semantic receipts are grouped by layer ranges.

Receipt policy:

```text
receipt_atlas_waves=10
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI authority

Exactly 48 R1H contract gates are required:

```text
--require-bt-wgsl-r27r1h-contract-001
...
--require-bt-wgsl-r27r1h-contract-048
```

They must appear exactly once in short, full, dedicated R1H contract and regenerated resolved args.

Expected repair-script output:

```text
r27r1h_required_gate_count=48
r27r1h_gate_cardinality_exact=1
```

## Negative canaries

At least 24 canaries cover skipped/duplicated layers, Layer20/21 swap, Q/K and Gate/Up key swaps, wrong layer resolution, missing-key zero fill, invalid/short ranges, within/cross-layer range aliases, checkpoint identity changes, unsupported dtype reinterpretation, accepting 153/154 projection scans, ignored revival, Layer20/21-only first-zero inference, binary-search origin, skipped RMS controls, GPU allocation, checkpoint write, automatic weight restore and automatic checkpoint replacement.

## BaseTrain authority

R1H remains forensic only:

```text
full_model_gradient_authority=0
full_model_training_state_authority=0
basetrain_gradient_value_admission_ready=0
```

Any later checkpoint generation/export repair must rerun the physical projection-family scan and then revalidate R1G/R1F/R1E/R1C and the selected-layer gradient path.

## PASS semantics

R27-R1H PASS means every canonical Q/K/V/O/Gate/Up/Down checkpoint projection tensor and both RMS controls across every runtime-declared decoder layer were resolved through the existing canonical checkpoint authority and independently scanned from physical read-only source ranges; the full ordered layer/role zero topology, per-role first-zero and revival boundaries, zero suffix continuity, cross-layer family pattern, RMS correlation and shard/range provenance were measured; R1G Layer0/20/21 anchors and Layer21 physical source digests were reproduced; no intermediate layer was skipped or inferred; no GPU/model/optimizer/checkpoint mutation occurred; and the complete scan reproduced exactly twice.

PASS does not mean the checkpoint exporter is already proven defective, that a specific writer loop introduced the values, that the payload-origin layer equals the writer-failure operation, that the checkpoint should be rewritten automatically, or that BaseTrain gradients have recovered.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_PROJECTION_FAMILY_ZERO_ORIGIN_SCAN_06C_R27_R1H
```
