# ASH-BASETRAIN-GPU-53 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-53`

## Title

Forward Boundary Output Readback Parity / GPU Output Buffer To Host Digest Verification Seal

## Seal

No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-53` consumes the successful `ASH-BASETRAIN-GPU-52` controlled output dispatch receipt and performs the first controlled output readback parity check.

GPU-53 reproduces the GPU-52 identity-copy dispatch, copies the GPU output buffer to a readback buffer, maps the readback buffer on the host, verifies the readback digest, and records a receipt without adopting logits or entering any training path.

GPU-53 may read back output bytes for digest/parity verification only. GPU-53 must not adopt the output as logits, compute loss, run backward, create or apply optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-48-R2-R1` | explicit 2048-byte selected payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual GPU buffer upload execution receipt |
| `ASH-BASETRAIN-GPU-49` | input bind group / shader / pipeline materialization |
| `ASH-BASETRAIN-GPU-50` | controlled input-only dispatch probe |
| `ASH-BASETRAIN-GPU-51` | input/output bind group layout and output buffer contract |
| `ASH-BASETRAIN-GPU-52` | controlled identity output-writing dispatch |
| `ASH-BASETRAIN-GPU-53` | output readback and digest parity verification |
| `ASH-BASETRAIN-GPU-54` | non-adopted forward output candidate review gate, not part of GPU-53 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json
```

Required GPU-52 facts:

```text
patch_id == ASH-BASETRAIN-GPU-52
pass == true
output_mode == identity_copy
input_binding_slot == 0
output_binding_slot == 1
input_bound_buffer_bytes == 2048
output_bound_buffer_bytes == 2048
dispatch_used == true
dispatch_workgroup_count == 8
dispatch_x == 8
dispatch_y == 1
dispatch_z == 1
queue_submit_count == 1
output_written == true
readback_used == false
output_artifact_written == false
loss/backward/optimizer/weight_mutation == false
```

Expected GPU-53 readback digest:

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
| `--gpu52-receipt` | `artifacts/ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json` |
| `--gpu51-receipt` | `artifacts/ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json` |
| `--gpu50-receipt` | `artifacts/ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json` |
| `--gpu49-receipt` | `artifacts/ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json` |
| `--gpu48-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json` |
| `--gpu47-receipt` | `artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json` |
| `--r2-r1-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json` |
| `--selected-group-payload` | `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--backend` | `auto` |
| `--strict-selected-group` | `true` |
| `--max-upload-bytes` | `2048` |
| `--output-byte-len` | `2048` |
| `--output-f32-count` | `512` |
| `--allow-local-reupload-for-readback-parity` | `true` |
| `--shader-entrypoint` | `main` |
| `--input-binding-slot` | `0` |
| `--output-binding-slot` | `1` |
| `--dispatch-x` | `8` |
| `--dispatch-y` | `1` |
| `--dispatch-z` | `1` |
| `--output-mode` | `identity_copy` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--write-readback-artifact` | `false` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json` |

---

## 4. Allowed Operations

GPU-53 may perform:

```text
Read GPU-52/GPU-51/GPU-50/GPU-49/GPU-48/GPU-47/R2-R1 receipts
Read selected 2048-byte payload file
Validate payload byte_len == 2048
Validate payload sha256 == expected_output_sha256
Acquire WGPU adapter/device/queue
Create process-local input storage buffer
queue.write_buffer payload into process-local input buffer
Create process-local output storage buffer
Create readback buffer
Create input/output bind group layout
Create bind group with input and output buffers
Create identity-copy shader module
Create pipeline layout
Create compute pipeline
Create command encoder
Begin compute pass
Set compute pipeline
Set bind group
Dispatch workgroups once
Copy output buffer to readback buffer
Submit command buffer
Map readback buffer
Read output bytes on host
Compute readback sha256
Check readback byte_len/f32_count
Check finite/nonfinite counts
Write runtime receipt
```

---

## 5. Forbidden Operations

GPU-53 must not perform:

```text
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
CPU reference substitution as replacement for GPU readback
random payload generation
zero payload fallback
placeholder payload generation
silent correction
runtime default apply
```

GPU-53 must not write raw output `.bin` artifacts by default.

---

## 6. Readback Contract

Input buffer:

```text
binding: 0
usage: STORAGE | COPY_DST
byte_len: 2048
f32_count: 512
```

Output buffer:

```text
binding: 1
usage: STORAGE | COPY_SRC
byte_len: 2048
f32_count: 512
```

Readback buffer:

```text
usage: COPY_DST | MAP_READ
byte_len: 2048
f32_count: 512
```

GPU-53 must reproduce:

```text
dispatch_workgroups(8, 1, 1)
copy_buffer_to_buffer(output_buffer, 0, readback_buffer, 0, 2048)
map_async(MapMode::Read)
```

`map_async` is allowed in GPU-53 only for the readback parity seal.

---

## 7. WGSL

```wgsl
struct InputPayload {
    values: array<f32>,
};

struct OutputPayload {
    values: array<f32>,
};

@group(0) @binding(0)
var<storage, read> input_payload: InputPayload;

@group(0) @binding(1)
var<storage, read_write> output_payload: OutputPayload;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let index: u32 = gid.x;

    if (index < 512u) {
        output_payload.values[index] = input_payload.values[index];
    }
}
```

---

## 8. PASS Conditions

GPU-53 PASS requires:

```text
GPU-52 PASS receipt validated
GPU-51 PASS receipt validated
selected payload exists
payload byte_len == 2048
payload sha256 == expected_output_sha256
identity-copy output dispatch reproduced
copy_buffer_to_buffer_used == true
map_async_used == true
readback_used == true
readback_byte_len == 2048
readback_f32_count == 512
readback_sha256 == expected_output_sha256
readback_matches_expected_digest == true
finite_count == 512
nonfinite_count == 0
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
```

---

## 9. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_53_forward_boundary_output_readback_parity -- `
  --gpu52-receipt .\artifacts\ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json `
  --gpu51-receipt .\artifacts\ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json `
  --gpu50-receipt .\artifacts\ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json `
  --gpu49-receipt .\artifacts\ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json `
  --gpu48-receipt .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --r2-r1-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --output-byte-len 2048 `
  --output-mode identity_copy `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --dispatch-x 8 `
  --dispatch-y 1 `
  --dispatch-z 1 `
  --out .\artifacts\ASH_BASETRAIN_GPU_53_FORWARD_BOUNDARY_OUTPUT_READBACK_PARITY.json
```

---

## 10. Next Stage

After GPU-53 PASS:

```text
ASH-BASETRAIN-GPU-54
Forward Output Candidate Review Gate /
Readback Output To Non-Adopted Forward Candidate Seal
No Logits Adoption No Loss No Backward No Optimizer
```

GPU-54 may wrap the verified readback output as a non-adopted forward candidate. GPU-54 must not adopt logits, compute loss, run backward, create optimizer state, or mutate weights.

---

## 11. PASS Meaning

GPU-53 PASS means only that the GPU-52 identity-copy output dispatch was reproduced, the GPU output buffer was copied to a readback buffer, the host readback digest matched the expected selected payload digest, and no logits adoption, loss, backward, optimizer, or weight mutation occurred.
