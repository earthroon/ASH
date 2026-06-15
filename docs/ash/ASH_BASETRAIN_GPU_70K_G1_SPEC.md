# ASH-BASETRAIN-GPU-70K-G1

## Planned 1.1B Weight Atlas Registry Synthesis / Model Spec To Atlas Group Tensor Registry Seal

Seal: No Tensor Payload Materialization / No Safetensors Payload Read / No GPU Upload / No Forward / No Backward / No Optimizer / No Training / No Checkpoint Write.

## SSOT

`70K-G1` is the genesis route for incomplete or dummy safetensors. It does not search an existing checkpoint manifest for Q/K/V keys. It reads an explicit 1.1B model architecture spec and synthesizes a planned weight atlas registry.

Primary input:

```text
artifacts/model/ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json
```

Output:

```text
artifacts/ASH_BASETRAIN_GPU_70K_G1_PLANNED_WEIGHT_ATLAS_REGISTRY.json
```

## Required Model Spec Fields

```text
model_id
source_mode = planned_weight_registry
architecture_family
layer_count
hidden_size
attention_head_count
attention_head_dim
ffn_intermediate_size
vocab_size
max_sequence_length
dtype
embedding.tied_lm_head
atlas_policy.grouping_mode
atlas_policy.parallel_streaming_required
atlas_policy.full_tensor_load_allowed = false
```

Known carried requirements from prior receipts may be used as evidence only, not as invented defaults:

```text
hidden_size = 2048
attention_head_count = 16
attention_head_dim = 128
max_sequence_length = 52
```

## Planned Registry

The generated registry contains planned logical keys, not existing checkpoint keys.

Families:

```text
embedding
attention_qkv
attention_output
ffn_gate
ffn_up
ffn_down
norm
lm_head
```

Per-layer planned attention keys:

```text
layers.{i}.attention.q_proj.weight
layers.{i}.attention.k_proj.weight
layers.{i}.attention.v_proj.weight
layers.{i}.attention.o_proj.weight
```

Per-layer planned FFN keys:

```text
layers.{i}.ffn.gate_proj.weight
layers.{i}.ffn.up_proj.weight
layers.{i}.ffn.down_proj.weight
```

All planned tensor entries must carry:

```text
source_key_kind = planned_logical_key_not_existing_checkpoint_key
payload_materialized = false
gpu_uploaded = false
optimizer_state_allocated = false
checkpoint_written = false
```

## PASS

PASS requires a complete model spec, attention head product match, atlas full tensor load disabled, planned tensors generated, atlas groups generated, parameter count audit generated, and all forbidden execution flags false.

## BLOCKED

Blocked codes include:

```text
ERR_70K_G1_MODEL_ARCHITECTURE_SPEC_MISSING
ERR_70K_G1_SOURCE_MODE_NOT_PLANNED_WEIGHT_REGISTRY
ERR_70K_G1_MISSING_LAYER_COUNT
ERR_70K_G1_MISSING_HIDDEN_SIZE
ERR_70K_G1_MISSING_ATTENTION_HEAD_COUNT
ERR_70K_G1_MISSING_ATTENTION_HEAD_DIM
ERR_70K_G1_ATTENTION_HEAD_PRODUCT_MISMATCH
ERR_70K_G1_MISSING_FFN_INTERMEDIATE_SIZE
ERR_70K_G1_MISSING_VOCAB_SIZE
ERR_70K_G1_MISSING_DTYPE
ERR_70K_G1_MISSING_ATLAS_POLICY
ERR_70K_G1_FULL_TENSOR_LOAD_NOT_FORBIDDEN
ERR_70K_G1_MODEL_SPEC_PARSE_FAILED
```

## CLI

```powershell
cargo run --manifest-path .\crates\base_train\Cargo.toml `
  --bin ash_basetrain_gpu_70k_g1_planned_weight_atlas_registry_synthesis -- `
  --model-architecture-spec .\artifacts\model\ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json `
  --source-70h-shape-audit .\artifacts\ASH_BASETRAIN_GPU_70H_QKV_REQUIREMENT_SHAPE_AUDIT.json `
  --source-70j-route-plan .\artifacts\ASH_BASETRAIN_GPU_70J_QKV_ATLAS_GROUP_ROUTE_PLAN.json `
  --registry-id ash-basetrain-gpu-70k-g1-planned-weight-atlas-registry-0000 `
  --out .\artifacts\ASH_BASETRAIN_GPU_70K_G1_PLANNED_WEIGHT_ATLAS_REGISTRY.json
```

## Next

```text
ASH-BASETRAIN-GPU-70L-G1
Planned QKV Role Binding Review / Registry-Owned QKV Role Binding Operator Gate Seal
No Tensor Payload Materialization No GPU Upload
```
