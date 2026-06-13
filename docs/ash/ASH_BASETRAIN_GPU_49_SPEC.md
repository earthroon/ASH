# ASH-BASETRAIN-GPU-49 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-49`

## Title

**Forward Boundary Bind Group And Pipeline Materialization / Uploaded Buffer To Bind Group Contract No Dispatch Seal**

## Seal

**No Loss / No Backward / No Optimizer**

---

## 1. Purpose

`ASH-BASETRAIN-GPU-49` consumes the successful `ASH-BASETRAIN-GPU-48` upload execution receipt and materializes the next forward-boundary GPU resource contract.

GPU-48 proved:

```text
selected payload exists
payload byte_len == 2048
queue.write_buffer executed once
actual_uploaded_bytes == 2048
gpu_buffer_count == 1
dispatch == false
```

GPU-49 binds this verified uploaded payload into a process-local bind group and materializes the shader/pipeline contract required for the next controlled dispatch stage.

GPU-49 must not execute dispatch. GPU-49 must not compute logits. GPU-49 must not compute loss, backward, optimizer, or mutate weights.

---

## 2. SSOT

### 2.1 State Ownership

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-44` | next kernel input contract / storage readonly binding contract |
| `ASH-BASETRAIN-GPU-45` | buffer materialization descriptor |
| `ASH-BASETRAIN-GPU-47` | upload descriptor candidate |
| `ASH-BASETRAIN-GPU-48-R2-R1` | explicit 2048-byte payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual GPU buffer upload execution receipt |
| `ASH-BASETRAIN-GPU-49` | bind group, bind group layout, shader module, pipeline materialization contract |
| `ASH-BASETRAIN-GPU-50` | controlled dispatch candidate, not part of GPU-49 |

### 2.2 SSOT Presence

SSOT exists.

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json
```

Required GPU-48 facts:

```text
patch_id == ASH-BASETRAIN-GPU-48
pass == true
actual_uploaded_bytes == 2048
declared_upload_bytes == 2048
queue_write_count == 1
gpu_buffer_count == 1
payload_hash == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
bind_group_created == false
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
= 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

Projection lineage digest:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

The projection lineage digest must be preserved as lineage evidence, not treated as the payload file hash.

### 2.3 Reproducibility

GPU-49 is reproducible if:

```text
GPU-48 PASS receipt exists
GPU-48 uploaded payload hash matches GPU40 matrix digest
GPU-47 upload descriptor is accepted
GPU-44/45/47 binding contract agrees on binding slot, usage, dtype, byte length
WGPU adapter/device can be acquired
bind group layout and pipeline can be materialized without dispatch
```

---

## 3. Inputs

| Argument | Default |
|---|---|
| `--gpu48-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json` |
| `--gpu47-receipt` | `artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json` |
| `--gpu45-receipt` | `artifacts/ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json` |
| `--gpu44-receipt` | `artifacts/ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json` |
| `--r2-r1-receipt` | `artifacts/ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json` |
| `--selected-group-payload` | `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` |
| `--selected-group-id` | `selected-atlas-group-unknown` |
| `--backend` | `auto` |
| `--strict-selected-group` | `true` |
| `--max-upload-bytes` | `2048` |
| `--allow-local-reupload-for-materialization` | `true` |
| `--shader-entrypoint` | `main` |
| `--binding-slot` | `0` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json` |

GPU-49 may re-upload the verified selected payload into a new local WGPU buffer for materialization proof, because GPU-48's runtime buffer handle is not persistable across process boundaries. This re-upload must be recorded as GPU-49 local materialization upload, not as a new payload source.

---

## 4. Allowed Operations

GPU-49 may perform:

```text
Read GPU-48 PASS receipt
Read GPU-47 upload candidate receipt
Read GPU-45 buffer descriptor receipt
Read GPU-44 forward-boundary input contract receipt
Read R2-R1 payload digest rebind receipt
Read selected 2048-byte payload file
Validate payload byte_len == 2048
Validate payload sha256 == GPU48 payload_hash
Validate payload sha256 == GPU40 matrix digest from R2-R1
Acquire WGPU adapter/device/queue
Create process-local uploaded storage buffer
queue.write_buffer payload into the process-local buffer
Create bind group layout
Create bind group
Create shader module
Create pipeline layout
Create compute pipeline
Write runtime receipt
```

---

## 5. Forbidden Operations

GPU-49 must not perform:

```text
dispatch_workgroups
dispatch_workgroups_indirect
copy output to readback
map_async readback
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

## 6. Bind Group Contract

Required binding:

```text
binding: 0
visibility: COMPUTE
buffer_type: storage read-only
has_dynamic_offset: false
min_binding_size: 2048 bytes or compatible nonzero bound
```

Expected semantic contract:

```text
binding_slot == 0
target_buffer_usage == storage_readonly
payload_byte_len == 2048
payload_f32_count == 512
alignment_bytes == 4
```

---

## 7. Shader / Pipeline Contract

GPU-49 may create a minimal non-dispatch compute shader module to prove binding compatibility.

```wgsl
struct InputPayload {
    values: array<f32>,
};

@group(0) @binding(0)
var<storage, read> input_payload: InputPayload;

@compute @workgroup_size(1)
fn main() {
    // Materialization-only shader.
    // No dispatch in GPU-49.
}
```

---

## 8. PASS Conditions

GPU-49 PASS requires:

```text
GPU-48 PASS receipt validated
payload byte_len == 2048
payload sha256 == GPU48 payload_hash
payload sha256 == R2-R1 payload sha256
adapter/device acquired
process-local storage buffer created
process-local materialization queue write executed
bind group layout created
bind group created
shader module created
pipeline layout created
compute pipeline created
dispatch_used == false
readback_used == false
loss/backward/optimizer/weight_mutation == false
```

---

## 9. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_49_forward_boundary_bind_group_pipeline_materialization -- `
  --gpu48-receipt .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --gpu45-receipt .\artifacts\ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json `
  --gpu44-receipt .\artifacts\ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json `
  --r2-r1-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --out .\artifacts\ASH_BASETRAIN_GPU_49_FORWARD_BOUNDARY_BIND_GROUP_PIPELINE_MATERIALIZATION.json
```

---

## 10. Next Stage

After GPU-49 PASS:

```text
ASH-BASETRAIN-GPU-50
Forward Boundary Controlled Dispatch Candidate /
Bind Group Pipeline To No-Readback Dispatch Probe Seal
No Loss No Backward No Optimizer
```

GPU-50 may perform dispatch, but must still avoid loss/backward/optimizer unless explicitly promoted later.

---

## 11. PASS Meaning

GPU-49 PASS means only that the GPU-48 uploaded payload contract was consumed, a process-local uploaded buffer was created from the verified payload, the bind group layout, bind group, shader module, pipeline layout, and compute pipeline were materialized, and no dispatch/readback/training path was executed.

GPU-49 PASS does not mean dispatch succeeded. GPU-49 PASS does not mean logits were produced. GPU-49 PASS does not mean training occurred.
