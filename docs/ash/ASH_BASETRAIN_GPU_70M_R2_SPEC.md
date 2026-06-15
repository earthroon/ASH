# ASH-BASETRAIN-GPU-70M-R2

## QKV Atlas Grouping Cluster LUT Rebind / Match-Based Role Binding And Backend-Independent Cluster Map Seal

Seal: No Tensor Payload Read / No Selected Tensor Window Read / No Full Tensor Load / No GPU Upload / No Projection Dispatch / No Attention Score / No Softmax / No Logits / No Decode / No Loss / No Backward / No Optimizer / No Runtime Default Adoption.

## SSOT

70M-R2 rebinds the 70M-R1 QKV source selection into an atlas grouping cluster map.

Input SSOT:

- `artifacts/ASH_BASETRAIN_GPU_70M_QKV_MANIFEST_SOURCE_SELECTION.json`
- `artifacts/model/safetensors_manifest.json`
- optional compatibility inputs:
  - `artifacts/ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW.json`
  - `artifacts/ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW_RECEIPT.json`

Output SSOT:

- `artifacts/ASH_BASETRAIN_GPU_70M_R2_QKV_ATLAS_GROUPING_CLUSTER_LUT_REBIND.json`

## State Ownership

70M-R2 owns only:

- QKV role classification policy: `QKV_ROLE_PATTERNS_V1`
- cluster kind policy: `CLASSIFY_CLUSTER_KIND_STRICT_V1`
- streaming policy source: `STREAMING_POLICY_FOR_CLUSTER_KIND_V1`
- backend-independent `atlas_grouping_cluster`
- legacy selected key fields marked compatibility-only

70M-R2 does not own tensor payload reads, GPU upload, backend policy creation, WebGPU execution, WGPU upload, projection dispatch, attention execution, logits, decode, generation, training, optimizer, or runtime default adoption.

## Core Change

Before R2, downstream patches could consume top-level selected key fields:

```text
selected_q_key
selected_k_key
selected_v_key
```

After R2, downstream patches should consume the cluster-owned role binding map:

```text
atlas_grouping_cluster.role_bindings.query.manifest_key
atlas_grouping_cluster.role_bindings.key.manifest_key
atlas_grouping_cluster.role_bindings.value.manifest_key
```

The legacy selected key fields remain only for compatibility and are marked:

```json
{ "legacy_compatibility_only": true }
```

## Match + LUT Contract

Q/K/V role classification must be resolved by registered suffix patterns only.

Allowed registered role patterns:

```text
Query: .q_proj.weight, .wq.weight, .self_attn.query.weight, .attention.query.weight
Key:   .k_proj.weight, .wk.weight, .self_attn.key.weight, .attention.key.weight
Value: .v_proj.weight, .wv.weight, .self_attn.value.weight, .attention.value.weight
```

Loose string inference is forbidden.

Forbidden examples:

```text
key contains q
key contains k
key contains v
key contains query
similar name fallback
silent alias correction
```

## Cluster Kind

70M-R2 can PASS only this cluster kind:

```text
attention_qkv_separated
```

Fused QKV is only detected and blocked/deferred:

```text
ERR_70M_R2_FUSED_QKV_DETECTED_REQUIRES_SPLIT_PLAN
```

## Backend Boundary

70M-R2 is backend-independent. Browser WebGPU and Native WGPU are declared only as allowed future backend targets.

```json
{
  "backend_independent": true,
  "backend_policy_created": false,
  "backend_policy_stage": "70O_or_later",
  "allowed_backend_targets": ["native_wgpu", "browser_webgpu", "cpu_reference", "receipt_only"]
}
```

Actual backend upload/layout/shader/dispatch branching belongs to 70O or later, not 70M-R2.

## Runtime Surface

```text
crates/base_train/src/ash_basetrain_gpu_70m_qkv_manifest_source_selection.rs
crates/base_train/src/bin/ash_basetrain_gpu_70m_qkv_manifest_source_selection.rs
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
```

## CLI

```powershell
cargo run --manifest-path .\crates\base_train\Cargo.toml `
  --bin ash_basetrain_gpu_70m_qkv_manifest_source_selection -- `
  --source-70m-r1 .\artifacts\ASH_BASETRAIN_GPU_70M_QKV_MANIFEST_SOURCE_SELECTION.json `
  --qkv-review .\artifacts\ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW.json `
  --qkv-review-receipt .\artifacts\ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW_RECEIPT.json `
  --safetensors-manifest .\artifacts\model\safetensors_manifest.json `
  --selected-layer 0 `
  --selected-group-id group.layer.0.attention `
  --metadata-scanner-plan-id ash-basetrain-gpu-70m-r2-qkv-atlas-grouping-cluster-map-0000 `
  --out .\artifacts\ASH_BASETRAIN_GPU_70M_R2_QKV_ATLAS_GROUPING_CLUSTER_LUT_REBIND.json
```

## PASS

PASS requires:

- 70M-R1 source selection receipt exists.
- safetensors manifest exists.
- Q/K/V keys each match exactly one registered LUT suffix.
- Q/K/V role bindings are manifest-backed, reviewed/approved, shape-complete, dtype-complete, and alias-correction-free.
- role binding set resolves to `attention_qkv_separated`.
- streaming policy is produced from LUT.
- backend policy is not created in R2.
- all forbidden execution flags remain false.

## BLOCKED

Known blocked codes:

```text
ERR_70M_R2_MISSING_70M_R1_RECEIPT
ERR_70M_R2_SAFETENSORS_MANIFEST_MISSING
ERR_70M_R2_OPERATOR_REVIEW_NOT_APPROVED
ERR_70M_R2_Q_ROLE_NO_MATCH
ERR_70M_R2_K_ROLE_NO_MATCH
ERR_70M_R2_V_ROLE_NO_MATCH
ERR_70M_R2_Q_ROLE_AMBIGUOUS
ERR_70M_R2_K_ROLE_AMBIGUOUS
ERR_70M_R2_V_ROLE_AMBIGUOUS
ERR_70M_R2_FUSED_QKV_DETECTED_REQUIRES_SPLIT_PLAN
ERR_70M_R2_MIXED_SEPARATED_AND_FUSED_QKV
ERR_70M_R2_INCOMPLETE_QKV_CLUSTER
ERR_70M_R2_QKV_SHAPE_OR_DTYPE_MISMATCH
ERR_70M_R2_STREAMING_POLICY_MISSING
ERR_70M_R2_GPU_UPLOAD_DETECTED
ERR_70M_R2_UPSTREAM_DISPATCH_ALLOWED
```

## Next Stage

Recommended next patch:

```text
ASH-BASETRAIN-GPU-70N
Atlas Grouping Cluster Window Read / Cluster Role Binding To Partial Tensor Window Seal
No Full Tensor Load No GPU Upload No Projection Dispatch
```
