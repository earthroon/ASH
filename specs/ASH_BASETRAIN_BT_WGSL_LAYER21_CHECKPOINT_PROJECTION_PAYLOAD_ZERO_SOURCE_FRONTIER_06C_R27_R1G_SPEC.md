# ASH-BASETRAIN-BT-WGSL-LAYER21-CHECKPOINT-PROJECTION-PAYLOAD-ZERO-SOURCE-FRONTIER-06C-R27-R1G

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-LAYER21-CHECKPOINT-PROJECTION-PAYLOAD-ZERO-SOURCE-FRONTIER-06C-R27-R1G`
- Build revision: `bt-wgsl-layer21-checkpoint-projection-payload-zero-source-frontier-06c-r27-r1g`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-PARAMETER-WEIGHT-ZERO-PROVENANCE-06C-R27-R1F`
- Checkpoint source authority: canonical decoder-weight Atlas-wave checkpoint tensor set authority
- Selected final decoder layer: runtime-derived `checkpoint_layer_count - 1`, current fixture `21 / 22`
- Proof ledger: `HOLD`

## Parent SSOT

R27-R1F physically established:

```text
projection_zero_count=7
rms_control_zero_count=0
base_weight_zero_pattern=PROJECTION_ONLY_ZERO
shared_projection_first_zero_stage=P0_CHECKPOINT_RAW
shared_projection_first_zero_count=7
weight_zero_provenance_root_cause=CHECKPOINT_PARAMETER_PAYLOAD_ZERO
checkpoint_source_repair_required=true
```

All later R26/R27 weight-state boundaries preserve exact zero parity. R1G therefore does not reopen projection execution, backward execution, Adam, candidate construction, R26 root promotion, R27 state carry or R27 override copy.

## Primary question

R1G determines whether R1F's `P0_CHECKPOINT_RAW = ZERO` corresponds to the correct physical checkpoint tensor range, or whether the source resolver selected the wrong tensor key, layer, shard/file, byte range, placeholder, read result or raw-scan interpretation.

R1G must not silently conclude that the checkpoint artifact is corrupt merely because P0 is zero.

## Canonical role and source authority

R1G reuses the existing `DECODER_WEIGHT_REGISTRY_ORDER` and `DecoderWeightRole::tensor_key(layer)` authority. It does not maintain a second guessed LLaMA key registry.

Nine base roles are inspected per control layer:

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

Seven projection roles remain the repair candidates. The two RMSNorm roles remain controls.

## Cross-layer comparison

R1G inspects exactly:

```text
Layer 0
Layer 20
Layer 21
```

for all nine base roles. Layer0 is an early control, Layer20 is the immediate predecessor control and Layer21 is the selected target.

No control layer is assumed healthy. Nonzero/zero state is observed from its physical checkpoint range.

## Source descriptor binding

Every resolved role is bound through the existing checkpoint tensor authority:

```text
semantic role
-> expected tensor key
-> resolved tensor key
-> canonical role
-> layer ordinal
-> shard ID / relative path / shard SHA256
-> dtype
-> shape
-> element count
-> absolute file start
-> payload byte span
```

For exact fixed-width payloads:

```text
payload_bytes == element_count * dtype_width
absolute_file_end == absolute_file_start + payload_bytes
```

Zero-length and out-of-bounds ranges fail closed.

## Independent physical range verifier

R1G independently opens the already-authoritative local checkpoint source artifact read-only and scans the exact physical tensor range. This diagnostic read does not create a second model/checkpoint runtime authority.

The scanner is bounded:

```text
DIRECT_SCAN_CHUNK_BYTES = 4 MiB
full model reload = 0
full tensor diagnostic materialization = 0
```

For F16/BF16/F32, numeric zero classification is performed directly from scalar bit representations. Positive zero and negative zero are both zero. Unsupported dtypes fail closed rather than being reinterpreted as F32.

Per range R1G records:

```text
actual bytes returned
zero/nonzero byte counts
numeric zero/nonzero scalar counts
independent source-range SHA256
file size before/after
file modified timestamp before/after
read completion
source payload origin = PHYSICAL_CHECKPOINT_BYTES
```

A file that changes during diagnosis invalidates the result.

## R1F P0 parity

For the selected Layer21 nine-role source, R1G compares the independent physical scan against R1F/C9 canonical P0 evidence:

```text
canonical raw payload digest
canonical raw nonzero scalar count
```

Required verdict surfaces:

```text
canonical_direct_digest_match
raw_scanner_parity
```

Strong distinctions:

```text
physical range nonzero + R1F raw zero
-> R1F_CHECKPOINT_RAW_SCANNER_FALSE_ZERO

same key/file/range but physical digest differs from canonical P0 digest
-> CHECKPOINT_CANONICAL_READ_TRANSPORT_MISMATCH

physical range zero + digest parity + scanner parity
-> physical source numeric zero confirmed
```

## Missing/fallback/alias policy

Forbidden:

```text
missing key -> zero tensor
missing key -> empty vector
missing layer21 key -> layer20 fallback
missing key -> default tensor
placeholder zero allocation -> P0 source authority
```

Required runtime fields remain zero:

```text
missing_tensor_key_fallback_count=0
zero_fill_fallback_count=0
nearest_layer_fallback_count=0
```

Unexpected exact range aliases across logically distinct Layer21 base roles are rejected unless the canonical schema explicitly provides distinct fused subranges.

## Cross-layer source patterns

After Layer21 physical zero confirmation, R1G classifies the sampled pattern:

```text
LAYER21_ONLY_PROJECTION_PAYLOAD_ZERO
LATE_LAYER_PROJECTION_ZERO_PATTERN
CROSS_LAYER_PROJECTION_FAMILY_ZERO_PATTERN
LAYER21_ZERO_MIXED_CONTROL_PATTERN
```

Examples:

```text
Layer0 projection 7/7 nonzero
Layer20 projection 7/7 nonzero
Layer21 projection 0/7 nonzero
-> LAYER21_ONLY_PROJECTION_PAYLOAD_ZERO

Layer0 7/7 nonzero
Layer20 0/7
Layer21 0/7
-> LATE_LAYER_PROJECTION_ZERO_PATTERN

Layer0 0/7
Layer20 0/7
Layer21 0/7
-> CROSS_LAYER_PROJECTION_FAMILY_ZERO_PATTERN
```

These sampled controls do not claim the unobserved state of every decoder layer.

## Aggregate source frontier

R1G may publish one evidence-bound root cause:

```text
CHECKPOINT_ARTIFACT_IDENTITY_MISMATCH
CHECKPOINT_TENSOR_KEY_BINDING_FAILURE
CHECKPOINT_LAYER_ORDINAL_BINDING_FAILURE
CHECKPOINT_MISSING_PROJECTION_KEY
CHECKPOINT_ZERO_FILL_FALLBACK
CHECKPOINT_SHARD_RESOLUTION_FAILURE
CHECKPOINT_BYTE_RANGE_RESOLUTION_FAILURE
CHECKPOINT_PROJECTION_RANGE_ALIAS
CHECKPOINT_PLACEHOLDER_ZERO_MISBOUND_AS_RAW_SOURCE
CHECKPOINT_CANONICAL_READ_TRANSPORT_MISMATCH
R1F_CHECKPOINT_RAW_SCANNER_FALSE_ZERO
LAYER21_CHECKPOINT_SOURCE_BYTES_NUMERIC_ZERO_CONFIRMED
LAYER21_ONLY_PROJECTION_PAYLOAD_ZERO
LATE_LAYER_PROJECTION_ZERO_PATTERN
CROSS_LAYER_PROJECTION_FAMILY_ZERO_PATTERN
CHECKPOINT_SOURCE_FRONTIER_EVIDENCE_INSUFFICIENT
```

Root-cause precedence is source identity, key/layer identity, missing/fallback, shard/range, alias/placeholder, canonical read parity, scanner parity, physical numeric-zero confirmation, then sampled cross-layer pattern.

## Repair authority

R1G emits only diagnostic repair flags:

```text
checkpoint_identity_repair_required
checkpoint_tensor_key_repair_required
checkpoint_layer_binding_repair_required
checkpoint_missing_key_policy_repair_required
checkpoint_shard_resolver_repair_required
checkpoint_range_resolver_repair_required
checkpoint_read_transport_repair_required
checkpoint_placeholder_binding_repair_required
r1f_raw_scanner_repair_required
checkpoint_source_artifact_review_required
checkpoint_export_or_generation_frontier_required
```

The repair target count represents one systemic source repair domain when one is physically established.

R1G performs no checkpoint replacement or weight restoration.

Required zeros:

```text
checkpoint_write=0
checkpoint_repair_execution=0
automatic_checkpoint_replacement=0
automatic_checkpoint_download=0
automatic_weight_restore=0
weight_value_mutation=0
optimizer_state_mutation=0
gradient_value_mutation=0
projection_forward_math_change=0
projection_backward_math_change=0
```

## Semantic waves

R1G emits 12 sequential waves:

```text
00 R1F parent
01 layer/role registry
02 checkpoint artifact identity
03 tensor source descriptors
04 Layer0/Layer20 control sources
05 Layer21 source descriptors
06 Layer21 direct physical range scan
07 canonical P0 vs direct source parity
08 source failure frontier
09 cross-layer pattern
10 aggregate repair target
11 negative canaries / reproducibility / handoff
```

Receipt policy:

```text
receipt_atlas_waves=12
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI authority

Exactly 48 gates are required:

```text
--require-bt-wgsl-r27r1g-contract-001
...
--require-bt-wgsl-r27r1g-contract-048
```

The gates are present in the short args, full args, dedicated R1G contract args and resolved-args repair path.

Expected resolved-args output:

```text
r27r1g_required_gate_count=48
r27r1g_gate_cardinality_exact=1
```

## Negative canaries

At least 24 canaries cover wrong key, wrong layer, missing-key zero fill, role substitution, wrong file/shard, zero-length and short reads, out-of-bounds ranges, dtype/shape span mismatch, Q/K and Gate/Up aliases, RMS/projection alias, placeholder-zero misuse, pre-completion scan, canonical/direct digest mismatch, R1F false-zero scanner fixture, wrong dtype, layer20/layer21 swap, source mutation, unsupported encoding acceptance and attempted checkpoint/weight/GPU repair.

## Reproducibility

Two complete resolver/source snapshots are collected against unchanged source state.

Required:

```text
resolver_reproducibility_runs=2
resolver_reproducibility_match=1
source_range_reproducibility_runs=2
source_range_reproducibility_match=1
reproducibility_runs=2
reproducibility_match=1
```

## PASS semantics

R27-R1G PASS means R1F's Layer21 P0 zero was traced through the canonical role/key/tensor authority to the physical local checkpoint source range and independently verified with bounded read-only range scans and an independent scalar-zero classifier. Key, layer, source file/shard, dtype, shape, range, read completion, direct range digest and canonical P0 digest/scanner parity were separated. Layer0/Layer20 controls were physically sampled for the same roles. No checkpoint or model state was mutated, and the resulting source frontier was reproducible.

PASS does not mean the checkpoint artifact is corrupt, that another checkpoint should automatically replace it, that every decoder layer has the same projection pattern, that weights are repaired, or that BaseTrain gradient authority is open.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_LAYER21_CHECKPOINT_PROJECTION_PAYLOAD_ZERO_SOURCE_FRONTIER_06C_R27_R1G
```
