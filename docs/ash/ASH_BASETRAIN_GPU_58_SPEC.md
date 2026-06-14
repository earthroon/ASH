# ASH-BASETRAIN-GPU-58 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-58`

## Title

Forward Candidate Logits Surface Compatibility Gate / Non-Adopted Surface To Shape Policy Review Seal

## Seal

No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-58` consumes the successful `ASH-BASETRAIN-GPU-57` logits surface preflight descriptor and validates that the non-adopted surface candidate is compatible with an explicit shape policy.

GPU-58 only proves shape-policy compatibility. It must not claim final logits, vocabulary compatibility, runtime adoption, loss readiness, backward readiness, optimizer readiness, or weight update readiness.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-57` | non-adopted logits surface preflight descriptor SSOT |
| `ASH-BASETRAIN-GPU-58` | surface compatibility policy review SSOT |
| `ASH-BASETRAIN-GPU-59` | operator approval gate, not part of GPU-58 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json
```

Required GPU-57 facts:

```text
patch_id == ASH-BASETRAIN-GPU-57
pass == true
surface_descriptor_written == true
surface_kind == non_adopted_logits_surface_shape_candidate
surface_state == review_required
scalar_type == f32
endianness == little
rank == 1
shape == [512]
element_count == 512
surface_values_embedded == false
vocab_compatibility == not_verified
final_logits_claimed == false
logits_adopted == false
runtime_default_apply == false
runtime_adoption_allowed == false
loss/backward/optimizer/weight_mutation == false
```

Candidate digest SSOT:

```text
2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

Projection lineage digest remains lineage evidence only:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

---

## 3. Shape Policy

Default policy:

```json
{
  "policy_id": "ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1",
  "policy_kind": "non_adopted_logits_surface_shape_policy",
  "allowed_surface_kind": "non_adopted_logits_surface_shape_candidate",
  "required_surface_state": "review_required",
  "required_scalar_type": "f32",
  "required_endianness": "little",
  "required_rank": 1,
  "required_shape": [512],
  "required_element_count": 512,
  "required_byte_len": 2048,
  "required_finite_count": 512,
  "required_nonfinite_count": 0,
  "allow_surface_values_embedded": false,
  "allow_final_logits_claim": false,
  "allow_vocab_compatibility_claim": false,
  "allow_logits_adoption": false,
  "allow_runtime_default_apply": false,
  "allow_loss": false,
  "allow_backward": false,
  "allow_optimizer": false,
  "allow_weight_mutation": false
}
```

This policy checks only shape and metadata compatibility.

---

## 4. Inputs

| Argument | Default |
|---|---|
| `--gpu57-receipt` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json` |
| `--surface-descriptor` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json` |
| `--gpu56-receipt` | `artifacts/ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json` |
| `--gpu55-receipt` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json` |
| `--policy-id` | `ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1` |
| `--policy-kind` | `non_adopted_logits_surface_shape_policy` |
| `--expected-surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--expected-surface-kind` | `non_adopted_logits_surface_shape_candidate` |
| `--expected-surface-state` | `review_required` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--expected-byte-len` | `2048` |
| `--expected-scalar-type` | `f32` |
| `--expected-endianness` | `little` |
| `--expected-rank` | `1` |
| `--expected-surface-len` | `512` |
| `--expected-element-count` | `512` |
| `--expected-finite-count` | `512` |
| `--expected-nonfinite-count` | `0` |
| `--allow-vocab-claim` | `false` |
| `--allow-final-logits-claim` | `false` |
| `--allow-logits-adoption` | `false` |
| `--allow-runtime-default-apply` | `false` |
| `--out-policy` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json` |

---

## 5. Outputs

GPU-58 writes two JSON artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json
```

GPU-58 must not write raw payload bytes, runtime logits buffers, adopted logits artifacts, loss receipts, gradients, optimizer receipts, delta packets, checkpoints, or runtime default apply markers.

---

## 6. Allowed Operations

GPU-58 may read GPU-57/GPU-56/GPU-55 receipts, read the GPU-57 surface descriptor, validate metadata against the explicit policy, write policy JSON, and write compatibility receipt JSON.

---

## 7. Forbidden Operations

GPU-58 must not perform GPU dispatch, GPU device acquisition, GPU readback, map_async, copy_buffer_to_buffer, raw payload rewrite, raw payload regeneration, surface value embedding, logits adoption, runtime logits registration, final logits claim, vocab compatibility verification claim, loss, backward, optimizer, weight mutation, full tensor load, unselected group load, silent correction, or runtime default apply.

---

## 8. PASS Conditions

GPU-58 PASS requires:

```text
gpu57_pass == true
gpu56_pass == true
surface_descriptor_exists == true
surface_id matches expected surface id
surface_kind == non_adopted_logits_surface_shape_candidate
surface_state == review_required
payload_sha256 == expected_output_sha256
byte_len == 2048
scalar_type == f32
endianness == little
rank == 1
shape == [512]
element_count == 512
finite_count == 512
nonfinite_count == 0
surface_values_embedded == false
final_logits_claimed == false
vocab_compatibility != verified
logits_adopted == false
runtime_default_apply == false
runtime_adoption_allowed == false
loss/backward/optimizer/weight_mutation == false
```

---

## 9. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_58_forward_candidate_logits_surface_compatibility_gate -- `
  --gpu57-receipt .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json `
  --surface-descriptor .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json `
  --gpu56-receipt .\artifacts\ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json `
  --gpu55-receipt .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json `
  --policy-id ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1 `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-surface-kind non_adopted_logits_surface_shape_candidate `
  --expected-surface-state review_required `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --expected-byte-len 2048 `
  --expected-scalar-type f32 `
  --expected-endianness little `
  --expected-rank 1 `
  --expected-surface-len 512 `
  --expected-element-count 512 `
  --expected-finite-count 512 `
  --expected-nonfinite-count 0 `
  --out-policy .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json
```

---

## 10. Next Stage

After GPU-58 PASS:

```text
ASH-BASETRAIN-GPU-59
Forward Candidate Operator Approval Gate /
Shape-Compatible Surface Review To Explicit Human Approval Seal
No Runtime Apply No Logits Adoption No Loss No Backward No Optimizer
```
