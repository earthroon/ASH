# ASH-BASETRAIN-GPU-70M

## QKV Manifest Source Selection / Operator Reviewed QKV Candidate Key Binding To Metadata Scanner Plan Seal

Seal: No Tensor Payload Read / No Full Tensor Load / No GPU Upload / No Projection Dispatch / No Attention Score / No Softmax / No Logits / No Decode / No Loss / No Backward / No Optimizer

## SSOT

Input SSOT:

- `artifacts/ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW.json`
- `artifacts/ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW_RECEIPT.json`
- `artifacts/model/safetensors_manifest.json`

Output SSOT:

- `artifacts/ASH_BASETRAIN_GPU_70M_QKV_MANIFEST_SOURCE_SELECTION.json`

## State Ownership

70M owns only the Q/K/V source key selection and metadata scanner plan for the next partial-window read stage.

70M does not own tensor payload reading, full tensor loading, GPU buffer creation, queue writes, projection dispatch, attention score, softmax, logits, token selection, decode, generation, loss, backward, optimizer, weight mutation, runtime attach, or default route adoption.

## Required Upstream State

70M requires 70L to have operator-approved resolved manifest keys:

```text
operator_approval_status=approved_resolved_manifest_keys
q_weight_key_binding_approved=true
k_weight_key_binding_approved=true
v_weight_key_binding_approved=true
q_weight_candidate_key_bound=true
k_weight_candidate_key_bound=true
v_weight_candidate_key_bound=true
```

If the 70L review remains `blocked_manifest_required`, `not_approved`, or manifest absent, 70M must emit `BLOCKED` and must not invent Q/K/V keys.

## Runtime Surface

```text
crates/base_train/src/ash_basetrain_gpu_70m_qkv_manifest_source_selection.rs
crates/base_train/src/bin/ash_basetrain_gpu_70m_qkv_manifest_source_selection.rs
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
```

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70m_qkv_manifest_source_selection -- `
  --qkv-review .\artifacts\ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW.json `
  --qkv-review-receipt .\artifacts\ASH_BASETRAIN_GPU_70L_QKV_CANDIDATE_KEY_BINDING_REVIEW_RECEIPT.json `
  --safetensors-manifest .\artifacts\model\safetensors_manifest.json `
  --selected-layer 0 `
  --selected-group-id group.layer.0.attention `
  --metadata-scanner-plan-id ash-basetrain-gpu-70m-qkv-metadata-scanner-plan-0000 `
  --out .\artifacts\ASH_BASETRAIN_GPU_70M_QKV_MANIFEST_SOURCE_SELECTION.json
```

## PASS

PASS requires:

- 70L review JSON exists.
- 70L receipt exists and `pass=true`.
- `operator_approval_status=approved_resolved_manifest_keys`.
- Q/K/V candidate keys are present, reviewed, approved, and manifest-backed.
- Q/K/V shape and dtype metadata are compatible.
- metadata scanner plan is created for 70N.
- all forbidden execution flags remain false.

## BLOCKED

Known blocked codes:

```text
ERR_70M_MISSING_70L_REVIEW_RECEIPT
ERR_70M_MISSING_70L_REVIEW_STATUS_RECEIPT
ERR_70M_SAFETENSORS_MANIFEST_MISSING
ERR_70M_70L_REVIEW_RECEIPT_NOT_PASS
ERR_70M_OPERATOR_REVIEW_NOT_APPROVED
ERR_70M_Q_KEY_CANDIDATE_EMPTY
ERR_70M_K_KEY_CANDIDATE_EMPTY
ERR_70M_V_KEY_CANDIDATE_EMPTY
ERR_70M_Q_KEY_NOT_APPROVED_OR_NOT_IN_MANIFEST
ERR_70M_K_KEY_NOT_APPROVED_OR_NOT_IN_MANIFEST
ERR_70M_V_KEY_NOT_APPROVED_OR_NOT_IN_MANIFEST
ERR_70M_QKV_SHAPE_OR_DTYPE_MISMATCH
ERR_70M_UPSTREAM_UPLOAD_ALLOWED
ERR_70M_UPSTREAM_DISPATCH_ALLOWED
```

## Next Stage

`ASH-BASETRAIN-GPU-70N` — Selected Group QKV Tensor Window Read / No Full Tensor Load No GPU Upload No Projection Dispatch Seal.
