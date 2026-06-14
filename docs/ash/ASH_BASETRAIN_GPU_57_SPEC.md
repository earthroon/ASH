# ASH-BASETRAIN-GPU-57 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-57`

## Title

Forward Candidate Logits Surface Preflight / Raw Payload To Non-Adopted Logits Shape Candidate Seal

## Seal

No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-57` consumes the successful `ASH-BASETRAIN-GPU-56` raw payload artifact integrity audit and creates a non-adopted logits surface preflight descriptor.

GPU-57 only describes the audited raw payload as a finite `f32[512]` surface candidate. It must not claim the surface is final logits, must not verify vocab compatibility, must not embed raw values into the descriptor, and must not adopt the payload into runtime inference.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-55` | raw candidate payload artifact materialization SSOT |
| `ASH-BASETRAIN-GPU-56` | raw payload artifact integrity audit SSOT |
| `ASH-BASETRAIN-GPU-57` | non-adopted logits surface preflight descriptor SSOT |
| `ASH-BASETRAIN-GPU-58` | surface compatibility review gate, not part of GPU-57 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin
```

Required GPU-56 facts:

```text
patch_id == ASH-BASETRAIN-GPU-56
pass == true
raw_payload_exists == true
raw_payload_byte_len == 2048
raw_payload_f32_count == 512
raw_payload_sha256 == expected_output_sha256
raw_payload_matches_expected_digest == true
finite_count == 512
nonfinite_count == 0
candidate_state == review_required
adopted == false
runtime_default_apply == false
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
```

---

## 3. Inputs

| Argument | Default |
|---|---|
| `--gpu56-receipt` | `artifacts/ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json` |
| `--gpu55-receipt` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json` |
| `--raw-payload-manifest` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json` |
| `--raw-payload` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin` |
| `--candidate-envelope` | `artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--candidate-id` | `ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000` |
| `--surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--surface-kind` | `non_adopted_logits_surface_shape_candidate` |
| `--surface-state` | `review_required` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--expected-byte-len` | `2048` |
| `--expected-f32-count` | `512` |
| `--expected-rank` | `1` |
| `--expected-surface-len` | `512` |
| `--out-surface` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json` |

---

## 4. Outputs

GPU-57 writes two JSON artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json
```

GPU-57 must not write raw payload bytes, runtime logits buffers, adopted logits artifacts, loss, gradient, optimizer, delta packets, checkpoints, or runtime default apply markers.

---

## 5. Allowed Operations

GPU-57 may read receipts and raw payload bytes, recompute digest, parse little-endian `f32`, count finite/nonfinite values, derive metadata-only surface shape descriptor, and write descriptor/receipt JSON.

---

## 6. Forbidden Operations

GPU-57 must not perform GPU dispatch, GPU device acquisition, GPU readback, `map_async`, `copy_buffer_to_buffer`, raw payload rewrite/regeneration, digest-only reconstruction, logits adoption, runtime logits registration, model forward adoption, loss, backward, optimizer, weight mutation, full tensor load, unselected group load, silent correction, or runtime default apply.

GPU-57 must not claim final logits or vocab compatibility.

---

## 7. PASS Conditions

GPU-57 PASS requires:

```text
gpu56_pass == true
gpu55_pass == true
candidate_id matches expected candidate id
candidate_state == review_required
raw_payload_exists == true
raw_payload_byte_len == 2048
raw_payload_f32_count == 512
raw_payload_sha256 == expected_output_sha256
finite_count == 512
nonfinite_count == 0
surface_descriptor_written == true
surface_state == review_required
surface_shape == [512]
surface_element_count == 512
surface_values_embedded == false
logits_adopted == false
runtime_default_apply == false
runtime_adoption_allowed == false
loss/backward/optimizer/weight_mutation == false
```

---

## 8. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_57_forward_candidate_logits_surface_preflight -- `
  --gpu56-receipt .\artifacts\ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json `
  --gpu55-receipt .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json `
  --raw-payload-manifest .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json `
  --raw-payload .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin `
  --candidate-envelope .\artifacts\ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json `
  --selected-group-id selected-atlas-group-unknown `
  --candidate-id ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000 `
  --surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --expected-byte-len 2048 `
  --expected-f32-count 512 `
  --expected-rank 1 `
  --expected-surface-len 512 `
  --out-surface .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json
```

---

## 9. Next Stage

After GPU-57 PASS:

```text
ASH-BASETRAIN-GPU-58
Forward Candidate Logits Surface Compatibility Gate /
Non-Adopted Surface To Shape Policy Review Seal
No Logits Adoption No Loss No Backward No Optimizer
```
