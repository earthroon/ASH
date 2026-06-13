# ASH-BASETRAIN-GPU-52 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-52`

## Title

**Forward Boundary Controlled Output Dispatch / Input Output Bind Group To GPU Output Buffer Seal**

## Seal

**No Readback / No Loss / No Backward / No Optimizer**

---

## 1. Purpose

`ASH-BASETRAIN-GPU-52` consumes the successful `ASH-BASETRAIN-GPU-51` output buffer bind contract receipt and executes the first controlled output-writing dispatch.

GPU-52 proves that the GPU-51 input/output bind group can be recreated, a compute pipeline can be created, a command encoder and compute pass can be opened, the pipeline and bind group can be set, `dispatch_workgroups` can be issued, and the shader can write the process-local output storage buffer.

GPU-52 must not read back output, persist output bytes, materialize logits, compute loss, run backward, create optimizer state, apply optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-48-R2-R1` | explicit 2048-byte payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual GPU buffer upload execution receipt |
| `ASH-BASETRAIN-GPU-49` | input bind group / shader / pipeline materialization |
| `ASH-BASETRAIN-GPU-50` | controlled input-only dispatch probe |
| `ASH-BASETRAIN-GPU-51` | input/output bind group layout and output buffer contract |
| `ASH-BASETRAIN-GPU-52` | controlled output-writing dispatch |
| `ASH-BASETRAIN-GPU-53` | output readback/parity, not part of GPU-52 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json
```

Required GPU-51 facts:

```text
patch_id == ASH-BASETRAIN-GPU-51
pass == true
input_binding_slot == 0
output_binding_slot == 1
input_bound_buffer_bytes == 2048
output_bound_buffer_bytes == 2048
input_buffer_type == storage_readonly
output_buffer_type == storage_read_write
output_buffer_bound == true
output_buffer_created == true
dispatch_used == false
readback_used == false
output_written == false
loss/backward/optimizer/weight_mutation == false
```

Payload hash SSOT:

```text
GPU40 matrix_digest_hex
= GPU48 payload_hash
= GPU49 payload_sha256
= GPU50 payload_sha256
= GPU51 payload_sha256
= 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

Projection lineage digest remains lineage evidence only:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

---

## 3. Inputs

| Argument | Default |
|---|---|
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
| `--allow-local-reupload-for-output-dispatch` | `true` |
| `--shader-entrypoint` | `main` |
| `--input-binding-slot` | `0` |
| `--output-binding-slot` | `1` |
| `--dispatch-x` | `8` |
| `--dispatch-y` | `1` |
| `--dispatch-z` | `1` |
| `--output-mode` | `identity_copy` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json` |

---

## 4. Allowed Operations

GPU-52 may perform:

```text
Read GPU-51/GPU-50/GPU-49/GPU-48/GPU-47/R2-R1 receipts
Read selected 2048-byte payload file
Validate payload byte_len == 2048
Validate payload sha256 against GPU51/GPU50/GPU49/GPU48/R2-R1
Acquire WGPU adapter/device/queue
Create process-local input storage buffer
queue.write_buffer payload into process-local input buffer
Create process-local output storage buffer
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
Submit command buffer
Write runtime receipt
```

---

## 5. Forbidden Operations

GPU-52 must not perform:

```text
copy output to readback
map_async readback
copy_buffer_to_buffer for host readback
output buffer host readback
output artifact write
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
CPU reference substitution
random payload generation
zero payload fallback
placeholder payload generation
silent correction
```

---

## 6. Output Mode

Initial GPU-52 mode is:

```text
output_mode == identity_copy
```

Rationale:

```text
GPU-52 is an output write path probe, not a forward math validation patch.
identity_copy gives GPU-53 a clean parity target.
expected output digest after readback should equal input payload digest.
```

Expected future GPU-53 readback digest:

```text
2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

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

Recommended dispatch:

```text
dispatch_workgroups(8, 1, 1)
```

---

## 8. PASS Conditions

GPU-52 PASS requires:

```text
GPU-51 PASS receipt validated
GPU-50 PASS receipt validated
selected payload exists
payload byte_len == 2048
payload sha256 matches GPU51/GPU50/GPU49/GPU48/R2-R1
input buffer created
output buffer created
input/output bind group created
identity-copy compute pipeline created
compute pass created
pipeline set
bind group set
dispatch_workgroups executed
queue submitted
output_written == true
readback_used == false
output_artifact_written == false
loss/backward/optimizer/weight_mutation == false
```

---

## 9. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_52_forward_boundary_controlled_output_dispatch -- `
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
  --dispatch-x 8 `
  --dispatch-y 1 `
  --dispatch-z 1 `
  --out .\artifacts\ASH_BASETRAIN_GPU_52_FORWARD_BOUNDARY_CONTROLLED_OUTPUT_DISPATCH.json
```

---

## 10. Next Stage

After GPU-52 PASS:

```text
ASH-BASETRAIN-GPU-53
Forward Boundary Output Readback Parity /
GPU Output Buffer To Host Digest Verification Seal
No Logits Adoption No Loss No Backward No Optimizer
```

GPU-53 may read back output and verify digest/parity. GPU-53 must not adopt logits, compute loss, run backward, create optimizer state, or mutate weights.
