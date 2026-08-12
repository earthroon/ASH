# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-PRODUCTION-ATLAS-PLAN-MATERIALIZATION-06C-R27-R1J-R2A

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-PRODUCTION-ATLAS-PLAN-MATERIALIZATION-06C-R27-R1J-R2A`
- Build revision: `bt-wgsl-checkpoint-export-provenance-capture-production-atlas-plan-materialization-06c-r27-r1j-r2a`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-ATLAS-RUNTIME-ROUTE-ADMISSION-06C-R27-R1J-R2`
- Source authority: physical safetensors checkpoint
- Output authority: production AW01 runtime-plan trio
- Weight repair authority: none
- Checkpoint mutation authority: none
- Forward/training/export authority: closed
- Proof ledger: `HOLD`

## Objective

R1J-R2 installs the explicit Atlas runtime route-admission bridge while retaining the AW00 fail-closed boundary. Physical AW01 admission remains blocked until a production-compatible runtime-plan trio exists.

R2A materializes exactly these three documents from the current physical checkpoint and the existing BaseTrain runtime authorities:

```text
tensor_group_manifest.json
atlas_group_plan.json
sequential_load_plan.json
```

R2A is not a weight-repair stage and must not infer or rewrite missing model values.

## Source SSOT

The current checkpoint is the only parameter-payload authority:

```text
D:\1111113232\DUST\1\ash_pass3\models\quarantine\ash_v5_native_genesis_full.decode04_r3_tail_norm_repaired.safetensors
```

Established checkpoint identity:

```text
ash-tinyllama-v5-48259-ad1edb55abef1466
```

Current model authority:

```text
model_spec_id = model_tinyllama_1p1b_v5_48259
decoder_layer_count = 22
```

The safetensors header owns tensor key, dtype, shape and physical byte ranges. The model spec validates architecture geometry but does not fabricate physical ranges.

## No repair or reconstruction

R2A prohibits:

- zero-tensor repair;
- missing-tensor synthesis;
- random initialization;
- neighbor-layer cloning;
- Layer19 to Layer20 or Layer20 to Layer21 copying;
- RMS-derived projection reconstruction;
- checkpoint rewrite or repack;
- silent dtype conversion;
- fixture-plan promotion;
- symbolic `ASH_TOK_TENSOR_03_*` plan promotion.

A numerically zero tensor is not a missing tensor. Membership is determined by physical key, dtype, shape and range.

## Existing runtime registry and schema reuse

R2A must reuse the existing BaseTrain role registry, including `DECODER_WEIGHT_REGISTRY_ORDER`, instead of introducing a second decoder-role authority.

The exact existing AW01 runtime plan structs are promoted to serializable public schema owners and are used for both generation and re-open validation.

### Tensor group manifest

```text
groups[]
  group_id
  group_order
  tensor_keys[]
```

### Atlas group plan

```text
max_slot_bytes

groups[]
  group_id
  slices[]
    tensor_key
    logical_element_start
    logical_element_count
    slot_segment_index
    slot_byte_offset
    padded_byte_len
```

### Sequential load plan

```text
waves[]
  wave_order
  group_id
```

No private generator-only runtime schema is allowed.

## Current AW01 slice constraint

The current AW01 join contract requires one Atlas slice entry per tensor key. R2A therefore does not silently expand runtime semantics to allow repeated tensor keys across multiple slices.

For this revision:

```text
one physical tensor = one Atlas slice
```

A later slicing revision must explicitly change the AW01 parser contract before tensors may be split across repeated tensor-key slices.

## Deterministic production grouping

Grouping follows canonical runtime semantic order rather than hash-map completion order or largest-first packing.

The current R2A materializer uses:

```text
aw02.layer0.prefill_bundle
  embeddings
  layer0 input RMS
  layer0 Q/K/V

aw02.layer0.decoder_tail_bundle
  layer0 O
  layer0 post-attention RMS
  layer0 Gate/Up/Down

aw02.layer{N}.decoder_block_bundle
  all nine DECODER_WEIGHT_REGISTRY_ORDER roles for N=1..21

aw02.output.final_bundle
  final model RMS
  untied LM head when model authority requires it
```

Group IDs are deterministic and layer order is canonical.

## Slot geometry

R2A does not use an arbitrary slot-size fallback.

Each group footprint is calculated from its actual production tensors with the established storage-buffer alignment policy. `max_slot_bytes` is the maximum aligned physical footprint among materialized production groups.

Current physical production admission requires F32 tensor payloads because the existing AW01 resident tensor view owns F32 residency semantics. An unsupported physical dtype fails closed rather than being converted silently.

All slot offsets and padded lengths must satisfy alignment, non-overlap and capacity constraints.

## Physical checkpoint validation

Each required runtime tensor must bind to a physical safetensors entry with:

```text
tensor_key
dtype
shape
element_count
payload_offset
payload_span
physical_range_valid
```

R2A validates required model geometry against the model spec and rejects missing tensors, shape mismatches, unsupported dtypes, invalid ranges and unexpected aliases.

The checkpoint is opened read-only. Full checkpoint host materialization and full checkpoint GPU upload are forbidden.

The checkpoint digest is computed before materialization and revalidated after output publication preparation. A changed source digest fails closed.

## Current V5 source-integrity canary

For the exact current model authority `model_tinyllama_1p1b_v5_48259` with 22 decoder layers, R2A preserves the already established source topology as an integrity canary only:

```text
Layer20 projection zero roles     = 6
Layer20 projection nonzero roles  = 1
Layer20 RMS nonzero roles         = 2

Layer21 projection zero roles     = 7
Layer21 projection nonzero roles  = 0
Layer21 RMS nonzero roles         = 2
```

Layer20 `mlp_down_proj` is the surviving projection control. R2A does not interpret this topology causally and does not repair it.

## Transactional materialization

Materialization is an explicit mode:

```text
--materialize-production-atlas-plan
--atlas-plan-output-dir <PATH>
```

It is mutually separate from runtime admission, R1J capture and full-snapshot admission.

The requested plan output directory must not already exist. R2A writes to a sibling staging generation, serializes all three runtime plans, reopens them through the existing AW01 parser and `join_atlas_wave_01_plans()`, validates them, builds the receipt, then atomically promotes the completed generation.

Partial 1/3 or 2/3 plan publication is forbidden.

The canonical output contains:

```text
tensor_group_manifest.json
atlas_group_plan.json
sequential_load_plan.json
production_atlas_plan_materialization_receipt.json
```

plus R2A receipt wave/chunk evidence.

## Reproducibility

The plan set is independently built twice in memory from the same source authority. The serialized bytes of all three plans must match exactly before publication.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

Wall-clock timestamps do not participate in semantic plan identity.

## Atlas receipt architecture

R2A follows the Pass88 receipt rule and does not reintroduce a giant `json!({...})` terminal object or a recursion-limit workaround.

Receipt flow:

```text
17 semantic waves
  -> <=8 fields per chunk
  -> parallel chunk construction
  -> sequential wave write
  -> deterministic stream-ordinal merge
  -> duplicate-key fail closed
  -> final materialization receipt
```

Required:

```text
receipt_atlas_waves=17
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
duplicate_key_fail_closed=1
monolithic_final_json=0
recursion_limit_workaround=0
```

## Semantic receipt waves

```text
00 R1J-R2 parent
01 checkpoint identity
02 physical safetensors directory
03 runtime role registry
04 decoder layer-role binding
05 non-decoder runtime registry binding
06 physical range validation
07 group materialization
08 slot capacity authority
09 slice packing
10 sequential wave schedule
11 runtime parser roundtrip
12 AW01 plan join
13 source zero-pattern parity
14 reproducibility
15 publication transaction
16 R2 physical handoff
```

## Runtime authority ceiling

The materialization invocation is plan-only:

```text
forward=0
loss=0
backward=0
optimizer=0
weight_value_mutation=0
checkpoint_write=0
checkpoint_rewrite=0
checkpoint_export=0
```

`--materialize-production-atlas-plan` and `--admit-atlas-runtime-route` are not combined in one invocation. The intended operational flow is:

```text
Run A: R2A production plan materialization
Run B: R2 physical AW01 admission using those exact generated plans
```

## Structural gate contract

Exactly 48 R2A contract gates are integrated into the R27 structural gate:

```text
--require-bt-wgsl-r27r1j-r2a-contract-001
...
--require-bt-wgsl-r27r1j-r2a-contract-048
```

Required:

```text
required_gate_count=48
gate_cardinality_exact=1
gate_gap_count=0
gate_duplicate_count=0
```

The structural gate validates the R2A contract and must explicitly report that physical materialization did not happen inside gate context.

## Negative canaries

At least 38 canaries cover missing/wrong checkpoint authority, malformed headers, missing/duplicate roles, shape and dtype mismatch, invalid or aliased ranges, zero-tensor misclassification, the Layer20 Down control, fixture/symbolic-plan import, random generation, checkpoint mutation, full-model materialization, slot fallback, packing gaps/overlaps, slot overflow, group/wave gaps and duplicates, parser/join failure, partial publication, silent overwrite, nondeterministic ordering, second role registry, giant terminal JSON macro, recursion-limit workaround, duplicate receipt keys and double-build mismatch.

## PASS semantics

`PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_PRODUCTION_ATLAS_PLAN_MATERIALIZATION_06C_R27_R1J_R2A` means the current V5 safetensors checkpoint has been treated as immutable physical source authority and projected deterministically into the exact existing AW01 production runtime schemas, the complete plan trio has been serialized and reopened through the existing runtime parser and join authority, source integrity and reproducibility checks have passed, and no model/training/checkpoint mutation authority has been exercised.

It does not mean AW01 GPU residency, forward, loss, backward, optimizer, checkpoint export, R1J live provenance capture or Layer20/21 repair occurred.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_PRODUCTION_ATLAS_PLAN_MATERIALIZATION_06C_R27_R1J_R2A
```

## Successful materialization HOLD

```text
HOLD_ASH_BASETRAIN_R1J_R2A_PRODUCTION_ATLAS_PLAN_READY_AW01_RUNTIME_NOT_YET_EXECUTED
```

## Next physical handoff

After R2A PASS, the exact generated trio becomes the input authority for R2 physical runtime admission:

```text
base checkpoint
+ generated tensor_group_manifest.json
+ generated atlas_group_plan.json
+ generated sequential_load_plan.json
+ --admit-atlas-runtime-route
-> AW00 Prepared
-> exact production-plan admission
-> AW01 same-device residency
-> ResidencyHandoffReady
```

A later R1J-R3 frontier may connect validated Atlas runtime/training state to the existing checkpoint writer and R1J provenance capture. R2A itself never performs that export.