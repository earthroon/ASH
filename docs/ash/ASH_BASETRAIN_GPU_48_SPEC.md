# ASH-BASETRAIN-GPU-48 Spec

## Patch ID

`ASH-BASETRAIN-GPU-48`

## Patch Title

Forward Boundary GPU Buffer Upload Execution / Descriptor Candidate To Actual Queue Write Seal / No Full Tensor Load No Bind Group No Dispatch No Loss No Backward No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-48` consumes the `ASH-BASETRAIN-GPU-47` upload candidate descriptor and an explicit selected-group payload file, creates a real WGPU buffer, and executes exactly one host-to-device `queue.write_buffer` path. It does not create a bind group, create a shader module, create a compute pipeline, dispatch compute, read back GPU bytes, compute loss, run backward, run an optimizer, or mutate weights.

## State Ownership

| Layer | Ownership |
|---|---|
| `crates/base_train/src/ash_basetrain_gpu_48_forward_boundary_gpu_buffer_upload_execution.rs` | Runtime logic and receipt generation |
| `crates/base_train/src/bin/ash_basetrain_gpu_48_forward_boundary_gpu_buffer_upload_execution.rs` | CLI entrypoint |
| `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json` | Runtime receipt path when executed locally |
| `docs/ash/ASH_BASETRAIN_GPU_48_SPEC.md` | GitHub spec SSOT |
| `docs/ash/artifacts/ASH_BASETRAIN_GPU_48_STATIC_CHECKS.json` | Static guard artifact SSOT |
| `docs/ash/artifacts/ASH_BASETRAIN_GPU_48_BAKE_MANIFEST.json` | Bake manifest artifact SSOT |

## Primary Inputs

- `--upload-candidate-receipt`
  - Default: `artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json`
- `--selected-group-payload`
  - Required for actual upload execution.
- `--out`
  - Default: `artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json`

## Optional Inputs

- `--selected-group-id`
- `--device-label`
- `--max-upload-bytes`
- `--strict-selected-group`

## Required GPU-47 Gate

The input receipt must satisfy:

- `patch_id == ASH-BASETRAIN-GPU-47`
- `pass == true` or `verdict == PASS`
- `gpu_buffer_upload_candidate.gpu_buffer_upload_candidate_created == true`
- `gpu_buffer_upload_candidate.upload_candidate_ready_for_probe_next == true`
- `gpu_buffer_upload_candidate.actual_gpu_buffer_upload_performed == false`
- `bind_and_dispatch_boundary.actual_bind_group_created == false`
- `bind_and_dispatch_boundary.actual_kernel_dispatch_executed == false`

## Descriptor Fields Consumed

- `gpu_buffer_upload_candidate.upload_descriptor_digest_hex`
- `gpu_buffer_upload_candidate.source_projection_digest_hex`
- `gpu_buffer_upload_candidate.target_byte_len`
- `gpu_buffer_upload_candidate.target_alignment_bytes`
- `gpu_buffer_upload_candidate.target_buffer_usage`
- `gpu_buffer_upload_candidate.target_binding_slot`
- `payload_source_validation.payload_digest_hex` when present

GPU-48 does not repair or synthesize the GPU-47 descriptor. If required descriptor fields are missing, the patch fails closed.

## Allowed Runtime Work

- Read GPU-47 upload candidate receipt.
- Read one explicit selected-group payload file.
- Verify payload byte count against descriptor byte count.
- Verify payload alignment.
- Verify payload hash if GPU-47 provided an expected hash.
- Create WGPU instance, adapter, device, and queue.
- Create one GPU buffer with `COPY_DST | STORAGE` usage.
- Execute `queue.write_buffer(&buffer, 0, &payload_bytes)`.
- Emit GPU-48 runtime receipt.

## Forbidden Runtime Work

- Full tensor load.
- Selected group auto-reconstruction from digest-only metadata.
- Zero-vector or placeholder fallback payload.
- Bind group creation.
- Shader module creation.
- Compute pipeline creation.
- Compute dispatch.
- GPU readback.
- Logits materialization.
- Loss computation.
- Backward pass.
- Optimizer step.
- Delta packet creation.
- Weight mutation.
- Checkpoint or safetensors mutation.
- Silent descriptor correction.

## Fail-Closed Codes

| Code | Meaning |
|---|---|
| `MISSING_GPU47_UPLOAD_CANDIDATE_RECEIPT` | GPU-47 receipt path does not exist |
| `GPU47_UPLOAD_CANDIDATE_RECEIPT_READ_FAILED` | GPU-47 receipt could not be read |
| `GPU47_UPLOAD_CANDIDATE_RECEIPT_PARSE_FAILED` | GPU-47 receipt JSON parse failed |
| `INVALID_GPU47_PATCH_ID` | Input receipt is not GPU-47 |
| `UPLOAD_CANDIDATE_NOT_APPROVED` | GPU-47 receipt is not PASS |
| `UPLOAD_CANDIDATE_CONTRACT_INVALID` | GPU-47 descriptor boundary is not ready or already opened |
| `SELECTED_GROUP_PAYLOAD_NOT_FOUND` | Explicit payload path is missing |
| `SELECTED_GROUP_PAYLOAD_READ_FAILED` | Explicit payload file could not be read |
| `SELECTED_GROUP_PAYLOAD_EMPTY` | Explicit payload file is empty |
| `UPLOAD_BYTE_COUNT_MISMATCH` | Payload byte count does not match descriptor |
| `UPLOAD_BYTE_LIMIT_EXCEEDED` | Payload exceeds operator-provided cap |
| `UPLOAD_ALIGNMENT_MISMATCH` | Payload byte count violates descriptor alignment |
| `PAYLOAD_HASH_MISMATCH` | Payload hash does not match GPU-47 expected hash |
| `SELECTED_GROUP_MISMATCH` | Strict selected group check failed |
| `FULL_TENSOR_LOAD_DETECTED` | Full tensor path was detected |
| `GPU_DEVICE_UNAVAILABLE` | WGPU adapter/device creation failed |
| `GPU_UPLOAD_LIMIT_UNSATISFIED` | Payload exceeds GPU storage buffer limit |
| `QUEUE_WRITE_FAILED` | Queue write boundary failed |
| `RECEIPT_WRITE_FAILED` | Receipt write failed |

## Output Receipt

Default runtime output path:

```text
artifacts/ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json
```

The receipt records:

- GPU-47 source receipt path and digest.
- Descriptor candidate hash.
- Payload hash and byte count.
- Actual uploaded bytes.
- GPU adapter/backend metadata.
- GPU buffer label and queue write range.
- Forbidden path flags, all false.

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_48_forward_boundary_gpu_buffer_upload_execution -- `
  --upload-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --out .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json
```

## Acceptance Criteria

GPU-48 PASS means only this:

> A GPU-47 descriptor candidate reached actual GPU buffer upload execution via one explicit `queue.write_buffer`, with no full tensor load, no bind group, no dispatch, no loss, no backward, no optimizer, and no weight mutation.

GPU-48 PASS does not mean forward succeeded.
GPU-48 PASS does not mean logits were created.
GPU-48 PASS does not mean training succeeded.

## Next Patch

`ASH-BASETRAIN-GPU-49` — Forward Boundary Bind Group And Pipeline Materialization / Uploaded Buffer To Bind Group Contract No Dispatch Seal.
