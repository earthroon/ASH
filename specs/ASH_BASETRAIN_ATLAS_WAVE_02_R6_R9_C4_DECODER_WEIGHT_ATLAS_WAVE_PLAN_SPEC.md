# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4

## Decoder Weight Atlas Wave Plan / Canonical Nine Weight Role Registry / Checkpoint Tensor Span Binding / Byte-Budget Wave Packing / Parallel Decode Lane Plan / Sequential Canonical Commit Order / Per-Wave Fence Boundary / No Mega Atlas / No Cross-Wave Payload Overlap / No Runtime Weight Authority Duplication Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C3` physical PASS  
> Parent wave domains: `ArtifactReceiptWave=ADMITTED`, `EmbeddingRowMicroAtlasWave=ADMITTED_BY_PARENT_LINEAGE`, `DecoderWeightAtlasWave=RESERVED_BLOCKED`  
> Active decoder-weight transport: `checkpoint-resolved-full-layer-loader`  
> C4 scope: deterministic planner only  
> Runtime decoder math: unchanged  
> Canonical runtime weight owner: `BaseTrainLayerWeightResidencySlot`  
> Transport execution: `NOT_EXECUTED`  
> Proof ledger: `HOLD` until physical C4 planner PASS

## 1. C4 promotion boundary

C4 promotes only the decoder-weight wave planning authority:

```text
DecoderWeightAtlasWave
  RESERVED_NOT_IMPLEMENTED / BLOCKED
    ->
DecoderWeightAtlasWavePlan
  IMPLEMENTED_CANDIDATE_PLAN_ONLY
  NOT_EXECUTED
  PLANNER_ONLY
```

C4 must not read decoder-weight payload bytes, spawn physical decode workers, upload GPU buffers, create decoder modules, create a staging slot, mutate the resident weight slot, mutate hidden state, or rebind the canonical loader.

## 2. Current loader truth

The active path remains:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
  -> load_base_train_atlas_wave_02_r6_r6_decoder_block
```

The current loader resolves the nine layer tensors, reads each whole tensor, decodes to `Vec<f32>`, and may retain all nine decoded vectors before constructing the decoder block. C4 plans a later bounded wave transport but does not replace this loader.

## 3. State ownership

```text
checkpoint tensor metadata
  = BaseTrainAtlasWave02R5CheckpointTensorSetAuthority

decoder weight role registry
  = DecoderWeightRole

decoder weight wave planning
  = DecoderWeightAtlasWavePlan

resident runtime decoder block
  = BaseTrainLayerWeightResidencySlot

hidden runtime state
  = LayerHiddenAuthoritySlot

incomplete block construction authority
  = NONE IN C4

artifact serialization
  = ArtifactReceiptParallelStreamingWaveMap
```

## 4. Canonical nine roles

Exactly nine roles are admitted:

```text
0 InputLayerNorm
1 SelfAttnQProj
2 SelfAttnKProj
3 SelfAttnVProj
4 SelfAttnOProj
5 PostAttentionLayerNorm
6 MlpGateProj
7 MlpUpProj
8 MlpDownProj
```

Tensor keys for target layer `L`:

```text
model.layers.{L}.input_layernorm.weight
model.layers.{L}.self_attn.q_proj.weight
model.layers.{L}.self_attn.k_proj.weight
model.layers.{L}.self_attn.v_proj.weight
model.layers.{L}.self_attn.o_proj.weight
model.layers.{L}.post_attention_layernorm.weight
model.layers.{L}.mlp.gate_proj.weight
model.layers.{L}.mlp.up_proj.weight
model.layers.{L}.mlp.down_proj.weight
```

Canonical roles remain:

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

## 5. Shape contract

Let:

```text
H   = hidden_size
I   = intermediate_size
QD  = num_attention_heads * head_dim
KVD = num_key_value_heads * head_dim
```

Expected shapes:

```text
InputLayerNorm          [H]
SelfAttnQProj           [QD, H]
SelfAttnKProj           [KVD, H]
SelfAttnVProj           [KVD, H]
SelfAttnOProj           [H, QD]
PostAttentionLayerNorm  [H]
MlpGateProj             [I, H]
MlpUpProj               [I, H]
MlpDownProj             [H, I]
```

Dimension and element products are checked. C4 does not replace `QD` with an unverified hardcoded `H` assumption.

## 6. Checkpoint span binding

Each role binds one existing `BaseTrainAtlasWave02R5R6TensorAuthority` and reuses its authority fields:

```text
tensor_key
canonical_role
layer_index
shard_id
shard_relative_path
shard_sha256
header_sha256
dtype
shape
element_count
payload_bytes
relative_data_start
relative_data_end
absolute_file_start
absolute_file_end
tensor_identity_digest
```

No second safetensors inventory parser is allowed.

Required span invariants:

```text
absolute_file_end - absolute_file_start == payload_bytes
relative_data_end - relative_data_start == payload_bytes
layer_index == target_layer
canonical_role == expected role
shape == expected shape
element_count == checked shape product
```

Admitted source dtypes:

```text
F16
BF16
F32
```

Payload width is checked against dtype and element count.

## 7. Planning byte accounting

For each role:

```text
source_payload_bytes = checkpoint authority payload_bytes
decoded_f32_bytes = element_count * 4
transient_host_bytes = source_payload_bytes + decoded_f32_bytes
```

All arithmetic is checked.

This is a conservative planning bound, not an observed physical peak-memory claim.

## 8. Explicit policy

C4 requires explicit CLI policy:

```text
--r6-r9-c4-decoder-weight-plan-target-layer 2
--decoder-weight-wave-max-host-transient-bytes 268435456
--decoder-weight-wave-parallel-decode-workers 4
--decoder-weight-wave-max-lanes-per-wave 4
--decoder-weight-wave-require-sequential-commit true
--decoder-weight-wave-require-fence-between-waves true
--decoder-weight-wave-allow-mega-atlas false
--decoder-weight-wave-allow-cross-wave-payload-overlap false
--decoder-weight-wave-allow-runtime-authority false
--require-r6-r9-c4-decoder-weight-wave-plan true
--allow-r6-r9-c4-active-decoder-weight-wave-transport false
```

The 256 MiB budget and worker/lane cardinality are current canary fixture policy, not hidden engine defaults.

## 9. Ordered-greedy byte-budget packing

Packing algorithm identity:

```text
ordered-greedy-contiguous-v1
```

Input order is registry ordinal `0..8`.

For each role, append to the current wave only when both remain true:

```text
current transient bytes + role transient bytes <= max_host_transient_bytes
next lane count <= min(max_lanes_per_wave, parallel_decode_worker_count)
```

Otherwise seal the current wave and open the next.

Semantic hardcoding such as `QKV always together`, `Gate/Up always together`, or `Norms always together` is forbidden.

If one role exceeds the byte budget by itself, fail closed with no silent budget increase, tensor split, dtype switch, disk spill, skipped role, or mega-atlas fallback.

## 10. Lane plan

Each role produces one `DecoderWeightWaveLanePlan` containing:

```text
wave ordinal
lane ordinal
role
registry ordinal
commit ordinal
checkpoint span
plannedParallelDecode
plannedPayloadReadCount = 1
plannedDecodeCount = 1
lanePlanDigest
```

`planned*` counters are plan declarations, not runtime observations.

Lane identity is deterministic and independent from worker scheduling.

## 11. Canonical commit ordinals

Registry discovery order and future module construction order are separate SSOTs.

Canonical commit ordinal mapping:

```text
0 InputLayerNorm
1 PostAttentionLayerNorm
2 SelfAttnQProj
3 SelfAttnKProj
4 SelfAttnVProj
5 SelfAttnOProj
6 MlpGateProj
7 MlpUpProj
8 MlpDownProj
```

C4 records these ordinals only. It performs no module commit.

Future C5 staging must preserve this distinction when material intake and final block construction are implemented.

## 12. Per-wave fence contract

Each `DecoderWeightAtlasWavePlanEntry` records:

```text
wave 0:
  requiresPreviousWaveFence = false

wave N > 0:
  requiresPreviousWaveFence = true

all waves:
  producesCompletionFence = true
  nextWaveDecodeBlockedUntilFence = true
```

C4 plans strict cross-wave non-overlap. It does not physically issue or await a GPU fence.

## 13. Plan root

`DecoderWeightAtlasWavePlan` carries at minimum:

```text
schema version
patch/build revision
target layer
checkpoint set digest
role registry digest
span binding digest
packing policy digest
canonical commit order digest
max host transient bytes
parallel decode workers
max lanes per wave
role count
wave count
lane count
wave entries
memory-accounting maxima and totals
planned mega-atlas count
planned cross-wave payload overlap count
planned runtime weight authority count
planner payload-read count
planner GPU-module-create count
planner weight-slot mutation count
planner hidden-slot mutation count
planned transport mode
active transport mode
transport execution state
implementation state
admission
plan digest
```

Required state:

```text
planned transport = decoder-weight-atlas-wave
active transport = checkpoint-resolved-full-layer-loader
transport execution = NOT_EXECUTED
implementation = IMPLEMENTED_CANDIDATE_PLAN_ONLY
admission = PLANNER_ONLY
planned mega atlas = 0
planned cross-wave overlap = 0
planned runtime weight authority = 0
planner payload read = 0
planner GPU module create = 0
planner weight mutation = 0
planner hidden mutation = 0
```

## 14. Coverage and collision gates

Required:

```text
role coverage = exact 9/9
registry ordinals = exact 0..8
commit ordinals = exact 0..8
lane count = 9
duplicate role assignment = 0
duplicate tensor identity assignment = 0
same-shard checkpoint span overlap = 0
```

Same-shard spans are sorted by absolute file start and verified as non-overlapping half-open ranges.

## 15. Runtime authority immutability proof

C4 is executed after the physically admitted C3 parent session.

Before planning, capture:

```text
weight pointer snapshot
hidden pointer snapshot
weight residency counts
hidden authority counts
```

After planning, capture them again and require exact equality.

For the Layer-2 canary parent state:

```text
resident weight layer = 2
hidden layer = 3
```

Planning must not evict/rebind weights simply to plan Layer 2.

## 16. Artifact receipt wave isolation

C4 continues to serialize receipts with `ArtifactReceiptParallelStreamingWaveMap`.

Artifact receipt waves serialize plan evidence only and must not be interpreted as decoder-weight payload waves.

Plan receipt layout:

```text
artifact wave 0 identity + policy
artifact wave 1 role registry + span binding
artifact wave 2 memory accounting + plan summary
artifact wave 3.. decoder-weight plan-wave descriptors
final artifact wave planner closure
```

Final receipt and local manifest are also assembled through deterministic artifact receipt waves.

No monolithic `json!` regression or recursion-limit workaround is admitted.

## 17. Implementation surface

New planner module:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r9_c4_decoder_weight_wave_plan.rs
```

Export surface:

```text
crates/base_train/src/lib.rs
```

Coordinator integration:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
```

Gate binding:

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
```

Policy:

```text
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

C4 does not semantically change R6-R7 active loader code or WGSL.

## 18. Rust-only core

The planner lives in the Rust `base_train` crate. JavaScript, TypeScript, browser workers, Node helpers, Python runtime dependencies, and new WGSL are forbidden in the canonical planner path.

## 19. Physical C4 PASS meaning

A C4 physical PASS proves, on the real checkpoint for target Layer 2:

```text
all nine decoder-weight roles resolved
real checkpoint spans/shapes/dtypes validated
byte-budget plan generated deterministically
all roles assigned exactly once
wave count >= 1
lane count = 9
peak planned transient bytes <= configured budget
all wave lane counts <= worker/lane cap
no mega atlas planned
no cross-wave payload overlap planned
no runtime weight authority created
runtime weight/hidden authority unchanged
active loader remains checkpoint-resolved-full-layer-loader
transport remains NOT_EXECUTED
```

It does not prove actual parallel reads, actual parallel decode, actual host peak memory, actual per-wave GPU construction, actual fence waits, wave-built Layer-2 parity, VRAM reduction, or performance improvement.

## 20. Terminal contract

Expected shape:

```text
[r6-r9-c4-decoder-weight-wave-plan]
target_layer=2
roles=9
waves=<derived>
lanes=9
budget=268435456
workers=4
max_lanes=4
peak_wave_transient=<derived>
mega_atlas=0
cross_wave_overlap=0
runtime_weight_authority=0
planned_transport=decoder-weight-atlas-wave
active_transport=checkpoint-resolved-full-layer-loader
transport_executed=0
plan_digest=<sha256>
proof_ledger=HOLD
```

PASS token:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C4_DECODER_WEIGHT_ATLAS_WAVE_PLAN_C3_PHYSICAL_PARENT_CANONICAL_NINE_WEIGHT_ROLE_REGISTRY_CHECKPOINT_TENSOR_SPAN_BINDING_DTYPE_SHAPE_ELEMENT_COUNT_BYTE_RANGE_IDENTITY_SEALED_ORDERED_GREEDY_BYTE_BUDGET_WAVE_PACKING_PARALLEL_DECODE_LANE_PLAN_SEQUENTIAL_CANONICAL_MODULE_COMMIT_ORDER_PER_WAVE_FENCE_BOUNDARY_NO_MEGA_ATLAS_NO_CROSS_WAVE_PAYLOAD_OVERLAP_NO_RUNTIME_WEIGHT_AUTHORITY_DUPLICATION_PLAN_ONLY_NOT_EXECUTED_ACTIVE_TRANSPORT_REMAINS_CHECKPOINT_RESOLVED_FULL_LAYER_LOADER_FULL_N_LAYER_FINAL_NORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

This token admits the planner only.

## 21. Static bake closure

```text
C4 patch/build revision = present
DecoderWeightRole = exactly 9 roles
registry/commit ordinal coverage = 0..8
checkpoint tensor key templates = exact
checkpoint authority reused = true
second safetensors inventory parser = 0
dtype/shape/element/span validation = present
source payload bytes = checkpoint authority
decoded bytes = checked element_count * 4
transient bytes = checked source + decoded
packing = ordered-greedy-contiguous-v1
hardcoded semantic packing groups = absent
single-role budget exceed = fail closed
intra-tensor chunking = absent
same-shard overlap validation = present
planner file I/O API = 0
planner WGPU/module construction API = 0
planned mega atlas = 0
planned cross-wave overlap = 0
planned runtime weight authority = 0
runtime weight pointer/count equality before/after = required
runtime hidden pointer/count equality before/after = required
active transport = checkpoint-resolved-full-layer-loader
planned transport = decoder-weight-atlas-wave
transport execution = NOT_EXECUTED
R6-R9 json! artifact macro regression = 0
recursion_limit workaround = 0
WGSL semantic changed files = 0
```

## 22. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## 23. Admission after PASS

```text
R6-R6 live body                         = ADMITTED
R6-R7 layer-weight residency            = ADMITTED
R6-R8 layer-1 forward                   = ADMITTED
R6-R9-C1 Layer-2 single-step            = ADMITTED
R6-R9-C2 coordinator evidence truth     = ADMITTED
R6-R9-C3 wave-domain split              = ADMITTED
R6-R9-C4 decoder-weight wave planner    = ADMITTED_PLANNER_ONLY

ArtifactReceiptWave                     = ADMITTED
EmbeddingRowMicroAtlasWave              = ADMITTED_BY_PARENT_LINEAGE
DecoderWeightAtlasWave                  = IMPLEMENTED_CANDIDATE_PLAN_ONLY
DecoderWeightAtlasWave transport        = BLOCKED_NOT_EXECUTED

LayerWeightBuildStagingSlot             = BLOCKED / C5
wave-built Layer-2 rebind               = BLOCKED / C6
wave-loader execution parity            = BLOCKED / C7
canonical wave-loader adoption          = BLOCKED / C8
progressive N-layer promotion           = BLOCKED / C9
full N-layer execution                  = BLOCKED
final norm / LM head                    = BLOCKED
forward loss / backward / optimizer     = BLOCKED
production inference                    = BLOCKED
proof ledger                            = HOLD
```

## 24. Next boundary

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C5

Layer Weight Build Staging Slot /
Private Incomplete-Block Authority /
Wave Decode Result Intake /
Sequential Module Material Commit /
Per-Role Source·Decoded Buffer Drop /
Complete Nine-Role Seal /
Atomic Decoder Block Construction /
Failure-to-RecoveryRequired Boundary /
No Partial Block Runtime Exposure /
No Second Runtime Weight Authority Seal
```

C5 is the first patch allowed to create transient incomplete-block construction authority. Canonical R6-R7 loader adoption remains deferred.

## Seal

> C4 turns the reserved decoder-weight wave name into a deterministic, checkpoint-bound, byte-budgeted nine-role plan only: real spans in, reproducible waves out, with zero payload execution, zero mega-atlas planning, zero cross-wave overlap, and zero runtime weight authority creation.
