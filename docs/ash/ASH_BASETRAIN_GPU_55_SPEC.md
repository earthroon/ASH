# ASH-BASETRAIN-GPU-55 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-55`

## Title

Forward Candidate Raw Payload Materialization Gate / Non-Adopted Candidate To Explicit Artifact Seal

## Seal

No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-55` consumes the successful `ASH-BASETRAIN-GPU-54` forward output candidate review gate and explicitly materializes the first raw forward candidate payload artifact.

GPU-55 must validate the non-adopted GPU-54 candidate envelope, reproduce the GPU readback path from verified source receipts, write raw candidate payload bytes only from reproduced GPU readback, and keep the candidate non-adopted.

GPU-55 may write a raw candidate payload `.bin` artifact. GPU-55 must not adopt the raw payload as logits, compute loss, run backward, create or apply optimizer state, mutate weights, or silently reconstruct the payload from digest alone.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-53` | output readback digest/parity SSOT |
| `ASH-BASETRAIN-GPU-54` | non-adopted candidate review envelope SSOT |
| `ASH-BASETRAIN-GPU-55` | explicit raw candidate payload artifact materialization |
| `ASH-BASETRAIN-GPU-56` | raw payload artifact integrity audit, not part of GPU-55 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_GATE.json
artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json
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

## 3. Inputs

| Argument | Default |
|---|---|
| `--gpu54-receipt` | `artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_GATE.json` |
| `--candidate-envelope` | `artifacts/ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json` |
| `--gpu53-receipt` | `artifacts/ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json` |
| `--gpu52-receipt` | `artifacts/ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json` |
| `--gpu51-receipt` | `artifacts/ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json` |
| `--gpu50-receipt` | `artifacts/ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json` |
| `--gpu49-receipt` | `artifacts/ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json` |
| `--gpu48-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json` |
| `--r2-r1-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json` |
| `--selected-group-payload` | `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--candidate-id` | `ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000` |
| `--candidate-state` | `review_required` |
| `--adopt-candidate` | `false` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--expected-byte-len` | `2048` |
| `--expected-f32-count` | `512` |
| `--output-mode` | `identity_copy` |
| `--dispatch-x` | `8` |
| `--dispatch-y` | `1` |
| `--dispatch-z` | `1` |
| `--write-raw-output-artifact` | `true` |
| `--out-payload` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin` |
| `--out-payload-manifest` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json` |

---

## 4. Outputs

GPU-55 writes three artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json
artifacts/ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json
```

GPU-55 must not write logits, loss, gradient, optimizer, delta packet, checkpoint, or runtime default apply artifacts.

---

## 5. Allowed Operations

GPU-55 may read the GPU-54 candidate envelope, validate GPU-53/GPU-52 evidence, reproduce the identity-copy dispatch, map the readback buffer, validate digest/shape/finite evidence, and then write the raw payload artifact plus manifest.

---

## 6. Forbidden Operations

GPU-55 must not perform logits materialization, logits adoption, model forward adoption, loss computation, backward computation, gradient computation, optimizer creation, optimizer step, weight mutation, delta candidate creation, training commit, full tensor load, unselected group load, CPU reference substitution, digest-only payload reconstruction, selected-payload direct copy as output artifact, random payload generation, zero payload fallback, placeholder payload generation, silent correction, or runtime default apply.

Important:

```text
GPU-55 must not create the raw payload from digest alone.
GPU-55 must not copy the selected payload directly as a substitute for GPU readback.
GPU-55 must materialize bytes from verified GPU readback reproduction.
```

---

## 7. PASS Conditions

GPU-55 PASS requires:

```text
GPU-54 review gate validated
candidate envelope validated
GPU-53 readback parity validated
identity-copy GPU readback reproduced
raw payload artifact written
raw payload manifest written
raw payload sha256 == candidate digest
raw payload byte_len == 2048
raw payload f32_count == 512
finite_count == 512
nonfinite_count == 0
candidate remains review_required
adopted == false
runtime_default_apply == false
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
digest_only_reconstruction_used == false
selected_payload_direct_copy_used == false
```

---

## 8. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_55_forward_candidate_raw_payload_materialization_gate -- `
  --gpu54-receipt .\artifacts\ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_GATE.json `
  --candidate-envelope .\artifacts\ASH_BASETRAIN_GPU_54_FORWARD_OUTPUT_CANDIDATE_REVIEW_ENVELOPE.json `
  --gpu53-receipt .\artifacts\ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json `
  --gpu52-receipt .\artifacts\ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json `
  --gpu51-receipt .\artifacts\ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json `
  --gpu50-receipt .\artifacts\ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json `
  --gpu49-receipt .\artifacts\ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json `
  --gpu48-receipt .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json `
  --r2-r1-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --candidate-id ash-basetrain-gpu-54-forward-output-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --output-mode identity_copy `
  --dispatch-x 8 `
  --dispatch-y 1 `
  --dispatch-z 1 `
  --out-payload .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD.bin `
  --out-payload-manifest .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MANIFEST.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_55_FORWARD_CANDIDATE_RAW_PAYLOAD_MATERIALIZATION_GATE.json
```

---

## 9. Next Stage

After GPU-55 PASS:

```text
ASH-BASETRAIN-GPU-56
Forward Candidate Raw Payload Integrity Audit /
Explicit Artifact Digest Shape Finite Seal
No Logits Adoption No Loss No Backward No Optimizer
```
