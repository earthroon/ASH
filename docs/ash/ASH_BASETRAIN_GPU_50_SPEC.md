# ASH-BASETRAIN-GPU-50 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-50`

## Title

Forward Boundary Controlled Dispatch Probe / Materialized Pipeline To Empty Compute Dispatch Seal

## Seal

No Readback / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-50` consumes the successful `ASH-BASETRAIN-GPU-49` bind group and pipeline materialization receipt and opens the first controlled dispatch boundary.

GPU-50 proves that a command encoder can be created, a compute pass can be opened, the materialized pipeline and bind group can be set, `dispatch_workgroups(1, 1, 1)` can be issued once, and the queue can submit the command buffer.

GPU-50 must not read back output, materialize logits, compute loss, run backward, create optimizer state, apply optimizer state, or mutate weights.

---

## 2. SSOT

State ownership:

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-48-R2-R1` | explicit 2048-byte payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual GPU buffer upload execution receipt |
| `ASH-BASETRAIN-GPU-49` | bind group, shader module, pipeline materialization contract |
| `ASH-BASETRAIN-GPU-50` | controlled dispatch probe, no readback |
| `ASH-BASETRAIN-GPU-51` | output buffer binding contract, not part of GPU-50 |
| `ASH-BASETRAIN-GPU-52` | output-producing dispatch, not part of GPU-50 |

SSOT exists.

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json
```

Required GPU-49 facts:

```text
patch_id == ASH-BASETRAIN-GPU-49
pass == true
bind_group_layout_created == true
bind_group_created == true
shader_module_created == true
pipeline_layout_created == true
compute_pipeline_created == true
dispatch_used == false
readback_used == false
loss_used == false
backward_used == false
optimizer_used == false
weight_mutation_used == false
```

Payload hash SSOT:

```text
GPU40 matrix_digest_hex
= GPU48 payload_hash
= GPU49 payload_sha256
= 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

Projection lineage digest:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

Projection lineage digest remains lineage evidence only and must not be treated as the payload file hash.

---

## 3. Inputs

| Argument | Default |
|---|---|
| `--gpu49-receipt` | `artifacts/ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json` |
| `--gpu48-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json` |
| `--gpu47-receipt` | `artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json` |
| `--r2-r1-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json` |
| `--selected-group-payload` | `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--backend` | `auto` |
| `--strict-selected-group` | `true` |
| `--max-upload-bytes` | `2048` |
| `--allow-local-reupload-for-dispatch-probe` | `true` |
| `--shader-entrypoint` | `main` |
| `--binding-slot` | `0` |
| `--dispatch-x` | `1` |
| `--dispatch-y` | `1` |
| `--dispatch-z` | `1` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json` |

---

## 4. Allowed Operations

GPU-50 may perform:

```text
Read GPU-49 PASS receipt
Read GPU-48 PASS receipt
Read GPU-47 upload candidate receipt
Read R2-R1 payload digest rebind receipt
Read selected 2048-byte payload file
Validate payload byte_len == 2048
Validate payload sha256 == GPU49 payload_sha256
Acquire WGPU adapter/device/queue
Create process-local uploaded storage buffer
queue.write_buffer payload into process-local buffer
Create bind group layout
Create bind group
Create shader module
Create pipeline layout
Create compute pipeline
Create command encoder
Begin compute pass
Set compute pipeline
Set bind group
Dispatch workgroups once
End compute pass
Submit command buffer
Write runtime receipt
```

GPU-50 may dispatch only the materialization-only shader path. GPU-50 may not bind an output buffer and may not read back any GPU output.

---

## 5. Forbidden Operations

GPU-50 must not perform:

```text
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

GPU-50 must also not write output payload artifacts, forward output candidate artifacts, loss artifacts, gradient artifacts, optimizer artifacts, delta packets, or checkpoint mutations.

---

## 6. Dispatch Contract

Recommended WGSL:

```wgsl
struct InputPayload {
    values: array<f32>,
};

@group(0) @binding(0)
var<storage, read> input_payload: InputPayload;

@compute @workgroup_size(1)
fn main() {
    // Dispatch probe only.
    // No output write.
    // No readback.
    // No logits.
    // No loss.
}
```

GPU-50 must issue exactly one controlled dispatch:

```text
dispatch_workgroups(1, 1, 1)
```

---

## 7. PASS Conditions

GPU-50 PASS requires:

```text
GPU-49 PASS receipt validated
GPU-48 PASS receipt validated
selected payload exists
payload byte_len == 2048
payload sha256 == GPU49 payload_sha256
adapter/device acquired
process-local storage buffer created
process-local queue write executed
bind group layout created
bind group created
shader module created
pipeline layout created
compute pipeline created
command encoder created
compute pass created
pipeline set
bind group set
dispatch_workgroups executed exactly once
queue submitted exactly once
readback_used == false
loss/backward/optimizer/weight_mutation == false
```

---

## 8. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_50_forward_boundary_controlled_dispatch_probe -- `
  --gpu49-receipt .\artifacts\ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json `
  --gpu48-receipt .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --r2-r1-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --out .\artifacts\ASH_BASETRAIN_GPU_50_FORWARD_BOUNDARY_CONTROLLED_DISPATCH_PROBE.json
```

---

## 9. Next Stage

After GPU-50 PASS:

```text
ASH-BASETRAIN-GPU-51
Forward Boundary Output Buffer Bind Contract /
Input Payload To Output Storage Buffer Layout Seal
No Dispatch No Readback No Loss No Backward No Optimizer
```

GPU-51 may bind an output storage buffer, but must not dispatch. GPU-52 may dispatch with output write, but must not read back. GPU-53 may read back and verify output digest/parity.

---

## 10. PASS Meaning

GPU-50 PASS means only that the GPU-49 materialized bind group and pipeline path survived an actual controlled dispatch and queue submission without readback, output adoption, loss, backward, optimizer, or weight mutation.

GPU-50 PASS does not mean output was produced. GPU-50 PASS does not mean logits were produced. GPU-50 PASS does not mean loss was computed. GPU-50 PASS does not mean training occurred.
