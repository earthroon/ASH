# ASH-BASETRAIN-GPU-56 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-56`

## Title

Forward Candidate Raw Payload Integrity Audit / Explicit Artifact Digest Shape Finite Seal

## Seal

No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-56` consumes the successful `ASH-BASETRAIN-GPU-55` raw forward candidate payload materialization gate and audits the explicit raw payload artifact as the file-level SSOT.

GPU-56 validates the GPU-55 receipt, the GPU-55 raw payload manifest, the GPU-54 candidate envelope, the GPU-54 review gate receipt, the GPU-53 readback parity receipt, and the raw candidate payload `.bin` artifact.

GPU-56 must prove that the raw payload exists, has the declared digest/shape/finite evidence, remains non-adopted, and has not been used as logits or training input.

GPU-56 must not run GPU dispatch, acquire a GPU device, map GPU buffers, rewrite the raw payload, regenerate the raw payload, adopt logits, compute loss, run backward, create or apply optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-55` | raw candidate payload artifact materialization SSOT |
| `ASH-BASETRAIN-GPU-56` | raw payload artifact integrity audit SSOT |
| `ASH-BASETRAIN-GPU-57` | logits surface preflight, not part of GPU-56 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin
```

Required GPU-55 receipt facts:

```text
patch_id == ASH-BASETRAIN-GPU-55
pass == true
raw_payload_written == true
raw_payload_manifest_written == true
source_materialization == reproduced_gpu_readback
digest_only_reconstruction_used == false
selected_payload_direct_copy_used == false
candidate_state == review_required
adopted == false
runtime_default_apply == false
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
```

Required raw payload facts:

```text
byte_len == 2048
f32_count == 512
sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
finite_count == 512
nonfinite_count == 0
```

Projection lineage digest remains lineage evidence only:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

---

## 3. Inputs

| Argument | Default |
|---|---|
| `--gpu55-receipt` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json` |
| `--raw-payload-manifest` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json` |
| `--raw-payload` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin` |
| `--candidate-envelope` | `artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json` |
| `--gpu54-receipt` | `artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_GATE.json` |
| `--gpu53-receipt` | `artifacts/ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--candidate-id` | `ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--expected-byte-len` | `2048` |
| `--expected-f32-count` | `512` |
| `--candidate-state` | `review_required` |
| `--adopt-candidate` | `false` |
| `--allow-gpu-dispatch` | `false` |
| `--allow-gpu-readback` | `false` |
| `--allow-logits-adoption` | `false` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json` |

---

## 4. Allowed Operations

GPU-56 may perform:

```text
Read GPU-55 materialization gate receipt
Read GPU-55 raw payload manifest
Read GPU-55 raw payload .bin
Read GPU-54 candidate envelope
Read GPU-54 review gate receipt
Read GPU-53 readback parity receipt
Validate candidate id/state
Validate raw payload byte length
Compute raw payload sha256
Parse raw payload as little-endian f32 values
Count finite/nonfinite values
Write integrity audit receipt JSON
```

---

## 5. Forbidden Operations

GPU-56 must not perform:

```text
GPU dispatch
GPU adapter/device acquisition
GPU queue submission
GPU readback
map_async
copy_buffer_to_buffer
raw payload rewrite
raw payload regeneration
selected payload direct copy
digest-only reconstruction
logits materialization
logits adoption
model forward adoption
loss computation
backward computation
gradient computation
optimizer creation
optimizer step
weight mutation
delta candidate creation
training commit
full tensor load
unselected group load
silent correction
runtime default apply
```

GPU-56 must fail closed on mismatch. It must not repair, rewrite, regenerate, or silently correct the raw payload artifact.

---

## 6. PASS Conditions

GPU-56 PASS requires:

```text
gpu55_pass == true
gpu54_pass == true
gpu53_pass == true
candidate_id matches expected candidate id
candidate_state == review_required
adopted == false
runtime_default_apply == false
raw_payload_exists == true
raw_payload_byte_len == 2048
raw_payload_f32_count == 512
raw_payload_sha256 == expected_output_sha256
raw_payload_sha256 == GPU55 manifest sha256
raw_payload_sha256 == GPU55 receipt sha256
finite_count == 512
nonfinite_count == 0
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
```

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_56_forward_candidate_raw_payload_integrity_audit -- `
  --gpu55-receipt .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json `
  --raw-payload-manifest .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json `
  --raw-payload .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin `
  --candidate-envelope .\artifacts\ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json `
  --gpu54-receipt .\artifacts\ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_GATE.json `
  --gpu53-receipt .\artifacts\ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json `
  --selected-group-id selected-atlas-group-unknown `
  --candidate-id ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --expected-byte-len 2048 `
  --expected-f32-count 512 `
  --out .\artifacts\ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json
```

---

## 8. Next Stage

After GPU-56 PASS:

```text
ASH-BASETRAIN-GPU-57
Forward Candidate Logits Surface Preflight /
Raw Payload To Non-Adopted Logits Shape Candidate Seal
No Logits Adoption No Loss No Backward No Optimizer
```

GPU-57 may inspect whether the raw payload can be described as a logits-surface candidate. GPU-57 must not adopt logits, compute loss, run backward, create optimizer state, or mutate weights.
