# ASH-BASETRAIN-GPU-51 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-51`

## Title

Forward Boundary Output Buffer Bind Contract / Input Payload To Output Storage Buffer Layout Seal

## Seal

No Dispatch / No Readback / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-51` consumes the successful `ASH-BASETRAIN-GPU-50` controlled dispatch probe receipt and prepares the first output-capable forward-boundary GPU bind contract.

GPU-51 proves that the verified input payload can be rebound together with a process-local output storage buffer, using binding slot 0 for input and binding slot 1 for output.

GPU-51 must not execute dispatch. GPU-51 must not read back output. GPU-51 must not materialize logits, compute loss, run backward, create optimizer state, apply optimizer state, or mutate weights.

---

## 2. SSOT

State ownership:

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-48-R2-R1` | explicit 2048-byte payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual GPU buffer upload execution receipt |
| `ASH-BASETRAIN-GPU-49` | input bind group / shader / pipeline materialization |
| `ASH-BASETRAIN-GPU-50` | controlled input-only dispatch probe |
| `ASH-BASETRAIN-GPU-51` | input/output bind group layout and output buffer contract |
| `ASH-BASETRAIN-GPU-52` | controlled output-write dispatch, not part of GPU-51 |
| `ASH-BASETRAIN-GPU-53` | output readback/parity, not part of GPU-51 |

SSOT exists.

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json
```

Required GPU-50 facts:

```text
patch_id == ASH-BASETRAIN-GPU-50
pass == true
dispatch_used == true
dispatch_workgroup_count == 1
queue_submit_count == 1
readback_used == false
output_buffer_bound == false
output_written == false
loss/backward/optimizer/weight_mutation == false
```

Payload hash SSOT:

```text
GPU40 matrix_digest_hex
= GPU48 payload_hash
= GPU49 payload_sha256
= GPU50 payload_sha256
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
| `--allow-local-reupload-for-bind-contract` | `true` |
| `--shader-entrypoint` | `main` |
| `--input-binding-slot` | `0` |
| `--output-binding-slot` | `1` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json` |

---

## 4. Allowed Operations

GPU-51 may perform:

```text
Read GPU-50 PASS receipt
Read GPU-49 PASS receipt
Read GPU-48 PASS receipt
Read GPU-47 upload candidate receipt
Read R2-R1 payload digest rebind receipt
Read selected 2048-byte payload file
Validate payload byte_len == 2048
Validate payload sha256 == GPU50/GPU49/GPU48/R2-R1 payload hash
Acquire WGPU adapter/device/queue
Create process-local input storage buffer
queue.write_buffer payload into process-local input buffer
Create process-local output storage buffer
Create bind group layout with input binding 0 and output binding 1
Create bind group with input and output buffers
Create shader module declaring both bindings
Create pipeline layout
Create compute pipeline
Write runtime receipt
```

GPU-51 may create and bind an output storage buffer. GPU-51 may not dispatch, submit a compute command buffer, write output, read back output, or write an output artifact.

---

## 5. Forbidden Operations

GPU-51 must not perform:

```text
dispatch_workgroups
dispatch_workgroups_indirect
queue.submit for compute execution
copy output to readback
map_async readback
copy_buffer_to_buffer for readback
output buffer readback
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

## 6. Binding Contract

Binding 0:

```text
storage read-only input payload
byte_len == 2048
f32_count == 512
```

Binding 1:

```text
storage read-write output buffer
byte_len == 2048
f32_count == 512
```

The output buffer usage may include `COPY_SRC` for future GPU-53 readback preparation, but GPU-51 itself must not perform readback.

---

## 7. Recommended WGSL

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

@compute @workgroup_size(1)
fn main() {
    // Output buffer bind contract only.
    // No dispatch in GPU-51.
    // No output write in GPU-51.
    // No readback. No logits. No loss.
}
```

---

## 8. PASS Conditions

GPU-51 PASS requires:

```text
GPU-50 PASS receipt validated
GPU-49 PASS receipt validated
selected payload exists
payload byte_len == 2048
payload sha256 == GPU50/GPU49/GPU48/R2-R1 payload hash
adapter/device acquired
process-local input storage buffer created
process-local output storage buffer created
bind group layout created with binding 0 and binding 1
bind group created with both buffers
shader module created
pipeline layout created
compute pipeline created
dispatch_used == false
readback_used == false
output_written == false
loss/backward/optimizer/weight_mutation == false
```

---

## 9. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_51_forward_boundary_output_buffer_bind_contract -- `
  --gpu50-receipt .\artifacts\ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json `
  --gpu49-receipt .\artifacts\ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json `
  --gpu48-receipt .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --r2-r1-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --output-byte-len 2048 `
  --out .\artifacts\ASH_BASETRAIN_GPU_51_FORWARD_BOUNDARY_OUTPUT_BUFFER_BIND_CONTRACT.json
```

---

## 10. Next Stage

After GPU-51 PASS:

```text
ASH-BASETRAIN-GPU-52
Forward Boundary Controlled Output Dispatch /
Input Output Bind Group To GPU Output Buffer Seal
No Readback No Loss No Backward No Optimizer
```

GPU-52 may dispatch and write to the output buffer. GPU-52 must not read back. GPU-53 may read back and verify output digest/parity.

---

## 11. PASS Meaning

GPU-51 PASS means only that the GPU-50 dispatch-proven input pipeline was extended to an input/output storage bind contract, and a process-local output storage buffer was bound into a compute pipeline without dispatch, readback, output artifact creation, loss, backward, optimizer, or weight mutation.
