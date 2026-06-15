# ASH-BASETRAIN-GPU-70K-G1-R1

## Planned 1.1B Weight Atlas Registry Synthesis From Operator-Approved Architecture Spec / Layer Family Tensor Registry Closure Seal

Seal: No Tensor Payload Materialization / No GPU Upload / No Training.

## SSOT

`70K-G1-R1` consumes `artifacts/model/ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json`, which must be produced by `ASH-BASETRAIN-GPU-70K-G0-R1` and must have `spec_status = operator_approved` and `source_mode = planned_weight_registry`.

This patch creates a planned tensor registry only. It does not read or trust safetensors payload bytes, does not materialize tensors, does not create GPU buffers, does not dispatch kernels, and does not train.

## Approved Architecture Required

```text
layer_count = 22
hidden_size = 2048
attention_head_count = 16
key_value_head_count = 2
attention_head_dim = 128
kv_projection_dim = 256
ffn_intermediate_size = 5632
vocab_size = 48259
dtype = F32
```

Validation:

```text
2048 == 16 * 128
256 == 2 * 128
```

## Planned Registry Contract

Global tensors:

```text
model.embed_tokens.weight
model.norm.weight
lm_head.weight
```

Per layer `0..21`:

```text
model.layers.{i}.input_layernorm.weight
model.layers.{i}.self_attn.q_proj.weight
model.layers.{i}.self_attn.k_proj.weight
model.layers.{i}.self_attn.v_proj.weight
model.layers.{i}.self_attn.o_proj.weight
model.layers.{i}.post_attention_layernorm.weight
model.layers.{i}.mlp.gate_proj.weight
model.layers.{i}.mlp.up_proj.weight
model.layers.{i}.mlp.down_proj.weight
```

Planned tensor count:

```text
22 * 9 + 3 = 201
```

Planned parameter count from shape metadata only:

```text
1166645248
```

## Outputs

```text
artifacts/ASH_BASETRAIN_GPU_70K_G1_R1_PLANNED_WEIGHT_ATLAS_REGISTRY.json
artifacts/ASH_BASETRAIN_GPU_70K_G1_R1_LAYER_FAMILY_TENSOR_REGISTRY_CLOSURE.json
```

## PASS Meaning

PASS means the operator-approved architecture spec has been converted into a planned layer-family tensor registry. It does not mean any payload exists or any GPU/training operation has run.

## BLOCKED Codes

```text
ERR_70K_G1_R1_APPROVED_ARCHITECTURE_SPEC_MISSING
ERR_70K_G1_R1_APPROVED_ARCHITECTURE_SPEC_PARSE_FAILED
ERR_70K_G1_R1_SPEC_STATUS_NOT_OPERATOR_APPROVED
ERR_70K_G1_R1_SOURCE_MODE_INVALID
ERR_70K_G1_R1_REQUIRED_FIELD_MISSING
ERR_70K_G1_R1_OPERATOR_DECISION_REQUIRED_TOKEN_REMAINING
ERR_70K_G1_R1_HIDDEN_SIZE_PRODUCT_MISMATCH
ERR_70K_G1_R1_KV_PROJECTION_PRODUCT_MISMATCH
ERR_70K_G1_R1_PLANNED_TENSOR_COUNT_MISMATCH
ERR_70K_G1_R1_PLANNED_PARAMETER_COUNT_MISMATCH
ERR_70K_G1_R1_PAYLOAD_MATERIALIZATION_DETECTED
ERR_70K_G1_R1_PAYLOAD_TRUST_DETECTED
ERR_70K_G1_R1_GPU_UPLOAD_DETECTED
ERR_70K_G1_R1_TRAINING_EXECUTION_DETECTED
ERR_70K_G1_R1_PLANNED_REGISTRY_WRITE_FAILED
ERR_70K_G1_R1_REGISTRY_CLOSURE_WRITE_FAILED
```

## CLI

```powershell
cargo run --manifest-path .\crates\base_train\Cargo.toml `
  --bin ash_basetrain_gpu_70k_g1_r1_planned_weight_atlas_registry_synthesis -- `
  --approved-architecture-spec .\artifacts\model\ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json `
  --source-70k-g0-r1-decision-closure .\artifacts\ASH_BASETRAIN_GPU_70K_G0_R1_MODEL_ARCHITECTURE_SPEC_DECISION_CLOSURE.json `
  --source-70k-g0-r1-required-field-closure .\artifacts\ASH_BASETRAIN_GPU_70K_G0_R1_REQUIRED_FIELD_CLOSURE_REPORT.json `
  --source-70k-g0b-topology-evidence .\artifacts\ASH_BASETRAIN_GPU_70K_G0B_HEADER_TOPOLOGY_EVIDENCE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_70K_G1_R1_PLANNED_WEIGHT_ATLAS_REGISTRY.json `
  --registry-closure-out .\artifacts\ASH_BASETRAIN_GPU_70K_G1_R1_LAYER_FAMILY_TENSOR_REGISTRY_CLOSURE.json
```

## Next

```text
ASH-BASETRAIN-GPU-70K-G2
Planned Registry To Dummy Safetensors Scaffold Compatibility / Approved Tensor Registry To Header Assembly Layout Seal
No Payload Write No GPU Upload No Training
```
