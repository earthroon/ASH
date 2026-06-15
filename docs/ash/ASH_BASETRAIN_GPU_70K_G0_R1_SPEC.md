# ASH-BASETRAIN-GPU-70K-G0-R1

## Model Architecture Spec Decision Closure / Header Topology Evidence To Operator-Approved Architecture Spec Seal

Seal: No Planned Registry / No GPU Upload / No Training.

## SSOT

`70K-G0-R1` consumes the `70K-G0B` header topology evidence and an explicit operator decision JSON. It may create `artifacts/model/ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json` only when the operator decision is `approve`, the adoption scope is `model_architecture_spec_only_no_planned_registry`, all required fields are complete, and the approved fields match the evidence.

This patch must not synthesize planned tensors, create a planned weight atlas registry, trust the safetensors payload, upload to GPU, or train.

## Required Inputs

```text
--source-70k-g0b-topology-evidence artifacts/ASH_BASETRAIN_GPU_70K_G0B_HEADER_TOPOLOGY_EVIDENCE.json
--source-70k-g0b-architecture-evidence artifacts/ASH_BASETRAIN_GPU_70K_G0B_ARCHITECTURE_DRAFT_EVIDENCE.json
--operator-decision artifacts/model/ASH_1_1B_MODEL_ARCHITECTURE_OPERATOR_DECISION.json
```

## Outputs

```text
artifacts/ASH_BASETRAIN_GPU_70K_G0_R1_MODEL_ARCHITECTURE_SPEC_DECISION_CLOSURE.json
artifacts/ASH_BASETRAIN_GPU_70K_G0_R1_REQUIRED_FIELD_CLOSURE_REPORT.json
```

Approved only:

```text
artifacts/model/ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json
```

## Evidence Validation

Expected evidence from `70K-G0B`:

```text
layer_count_candidate = 22
ffn_intermediate_size_candidate = 5632
vocab_size_candidate = 48259
estimated_parameter_count_from_header_shapes = 1166645248
```

GQA decomposition validation:

```text
hidden_size == attention_head_count * attention_head_dim
kv_projection_dim == key_value_head_count * attention_head_dim
```

Expected candidate values:

```text
2048 == 16 * 128
256 == 2 * 128
```

## Operator Decision Requirements

Required fields include:

```text
model_id
source_mode
architecture_family
layer_count
hidden_size
attention_head_count
key_value_head_count
attention_head_dim
kv_projection_dim
ffn_intermediate_size
vocab_size
max_sequence_length
batch_size_reference
dtype
embedding.tied_lm_head
position_encoding.kind
normalization.kind
normalization.epsilon
initializer.policy
initializer.seed
atlas_policy.grouping_mode
atlas_policy.parallel_streaming_required
atlas_policy.full_tensor_load_allowed
atlas_policy.max_live_group_count
parameter_count_target.label
parameter_count_target.strict_exact_match_required
parameter_count_target.tolerance_ratio
explicit_no_payload_trust
explicit_no_runtime_checkpoint_adoption
explicit_no_planned_registry_creation
```

`operator_decision_required` tokens must not remain.

## PASS Meaning

PASS means the model architecture spec was explicitly operator-approved and written as an SSOT input for `70K-G1`.

PASS does not mean a planned registry was created. PASS does not mean payload bytes are trusted.

## BLOCKED Codes

```text
ERR_70K_G0_R1_SOURCE_70K_G0B_TOPOLOGY_EVIDENCE_MISSING
ERR_70K_G0_R1_SOURCE_70K_G0B_ARCHITECTURE_EVIDENCE_MISSING
ERR_70K_G0_R1_SOURCE_70K_G0B_NOT_PASS
ERR_70K_G0_R1_OPERATOR_DECISION_MISSING
ERR_70K_G0_R1_OPERATOR_DECISION_NOT_APPROVE
ERR_70K_G0_R1_ADOPTION_SCOPE_INVALID
ERR_70K_G0_R1_APPROVED_LAYER_COUNT_MISMATCH
ERR_70K_G0_R1_APPROVED_FFN_INTERMEDIATE_SIZE_MISMATCH
ERR_70K_G0_R1_APPROVED_VOCAB_SIZE_MISMATCH
ERR_70K_G0_R1_HIDDEN_SIZE_PRODUCT_MISMATCH
ERR_70K_G0_R1_KV_PROJECTION_PRODUCT_MISMATCH
ERR_70K_G0_R1_REQUIRED_FIELD_MISSING
ERR_70K_G0_R1_OPERATOR_DECISION_REQUIRED_TOKEN_REMAINING
ERR_70K_G0_R1_PAYLOAD_TRUST_DETECTED
ERR_70K_G0_R1_RUNTIME_CHECKPOINT_ADOPTION_DETECTED
ERR_70K_G0_R1_PLANNED_REGISTRY_CREATION_DETECTED
ERR_70K_G0_R1_GPU_UPLOAD_DETECTED
ERR_70K_G0_R1_TRAINING_EXECUTION_DETECTED
ERR_70K_G0_R1_MODEL_ARCHITECTURE_SPEC_WRITE_FAILED
```

## CLI

```powershell
cargo run --manifest-path .\crates\base_train\Cargo.toml `
  --bin ash_basetrain_gpu_70k_g0_r1_model_architecture_spec_decision_closure -- `
  --source-70k-g0b-topology-evidence .\artifacts\ASH_BASETRAIN_GPU_70K_G0B_HEADER_TOPOLOGY_EVIDENCE.json `
  --source-70k-g0b-architecture-evidence .\artifacts\ASH_BASETRAIN_GPU_70K_G0B_ARCHITECTURE_DRAFT_EVIDENCE.json `
  --operator-decision .\artifacts\model\ASH_1_1B_MODEL_ARCHITECTURE_OPERATOR_DECISION.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_70K_G0_R1_MODEL_ARCHITECTURE_SPEC_DECISION_CLOSURE.json `
  --required-field-closure-out .\artifacts\ASH_BASETRAIN_GPU_70K_G0_R1_REQUIRED_FIELD_CLOSURE_REPORT.json `
  --approved-spec-out .\artifacts\model\ASH_1_1B_MODEL_ARCHITECTURE_SPEC.json
```

## Next

```text
ASH-BASETRAIN-GPU-70K-G1-R1
Planned 1.1B Weight Atlas Registry Synthesis From Operator-Approved Architecture Spec
No Tensor Payload Materialization No GPU Upload No Training
```
