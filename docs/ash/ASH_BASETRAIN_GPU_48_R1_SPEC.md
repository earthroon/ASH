# ASH-BASETRAIN-GPU-48-R1 Spec

## Patch ID

`ASH-BASETRAIN-GPU-48-R1`

## Title

Selected Group Payload Materialization Bridge / GPU40 Segment Dispatch Matrix To Explicit 2048 Byte Upload Payload Artifact Seal / No Full Tensor Load No Bind Group No Dispatch No Loss No Backward No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-48-R1` consumes GPU-40 segment execution evidence, GPU-41 stitch source map, GPU-42/GPU-44 approval and forward-boundary contract receipts, and GPU-45/GPU-47 buffer/upload descriptor receipts. It attempts to materialize `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` as exactly `512 x f32 = 2048 bytes` for GPU-48 actual queue-write execution. It does not use GPU upload, bind groups, shader modules, compute pipelines, dispatch, readback, loss, backward, optimizer, or weight mutation.

## State Ownership

| Layer | Ownership |
|---|---|
| `crates/base_train/src/ash_basetrain_gpu_48_r1_selected_group_payload_materialization_bridge.rs` | CPU replay/materialization logic and receipt generation |
| `crates/base_train/src/bin/ash_basetrain_gpu_48_r1_selected_group_payload_materialization_bridge.rs` | CLI entrypoint |
| `crates/base_train/src/lib.rs` | module export |
| `crates/base_train/Cargo.toml` | explicit binary registration |
| `artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin` | output payload artifact, only on PASS |
| `artifacts/ASH_BASETRAIN_GPU_48_R1_SELECTED_GROUP_PAYLOAD_MATERIALIZATION_BRIDGE.json` | runtime receipt, PASS or BLOCKED |

## Required Upstream Receipts

- `ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`
- `ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`
- `ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json`
- `ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json`
- `ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json`
- `ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json`

## Contract Checks

GPU-48-R1 must verify:

- GPU-40 total output count is `512`.
- GPU-41 stitch output count is `512`.
- GPU-44 next kernel input is `2048` bytes, `512` f32.
- GPU-45 buffer descriptor is `2048` bytes, `512` f32, `storage_readonly`.
- GPU-47 upload descriptor is `2048` bytes, alignment `4`, `storage_readonly`.
- GPU-41/GPU-42/GPU-44/GPU-45/GPU-47 approved projection digest chain is identical.
- GPU-40 segment output digests match GPU-41 segment source map digests.

## Materialization Mode

The materialization mode is:

```text
gpu40_segment_matrix_cpu_replay_to_explicit_payload_bin
```

GPU-48-R1 reads only the exact segment byte ranges recorded by GPU-40 and replays the deterministic CPU reference MatVec used by GPU-40:

```text
input_vector[i] = ((i % 17) - 8) / 17
row_output = sum(weight[row, k] * input_vector[k])
```

The resulting segment bytes are accepted only if they match both:

1. GPU-40 CPU reference digest for that segment.
2. GPU-40 exact GPU output digest for that segment.

If CPU replay matches GPU-40 CPU reference but does not reproduce the exact GPU output digest, GPU-48-R1 must fail closed with:

```text
GPU40_EXACT_OUTPUT_BYTES_NOT_REPRODUCED
```

This prevents CPU reference bytes from being falsely promoted as the approved GPU projection payload.

## Output Files

On PASS:

```text
artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin
artifacts/ASH_BASETRAIN_GPU_48_R1_SELECTED_GROUP_PAYLOAD_MATERIALIZATION_BRIDGE.json
```

On BLOCKED:

```text
artifacts/ASH_BASETRAIN_GPU_48_R1_SELECTED_GROUP_PAYLOAD_MATERIALIZATION_BRIDGE.json
```

No payload `.bin` is written on BLOCKED.

## Forbidden Paths

GPU-48-R1 must not call or perform:

- WGPU buffer creation.
- Queue write/upload.
- Bind group creation.
- Shader module creation.
- Compute pipeline creation.
- Compute dispatch.
- GPU readback.
- Loss.
- Backward.
- Optimizer.
- Delta apply.
- Weight mutation.
- Full tensor load.
- Random/dummy/zero-vector payload fallback.
- Digest-only payload reconstruction.

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_48_r1_selected_group_payload_materialization_bridge -- `
  --gpu40-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --gpu41-receipt .\artifacts\ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json `
  --gpu42-receipt .\artifacts\ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json `
  --gpu44-receipt .\artifacts\ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json `
  --gpu45-receipt .\artifacts\ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --selected-group-id selected-atlas-group-unknown `
  --out-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --out-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R1_SELECTED_GROUP_PAYLOAD_MATERIALIZATION_BRIDGE.json `
  --strict-selected-group true `
  --max-payload-bytes 2048
```

## PASS Meaning

GPU-48-R1 PASS means only this:

> A verified `512 x f32 = 2048 bytes` payload artifact was materialized from GPU-40 segment evidence and matched the approved projection digest chain.

GPU-48-R1 PASS does not mean GPU upload succeeded.
GPU-48-R1 PASS does not mean forward succeeded.
GPU-48-R1 PASS does not mean training succeeded.

## Next Stage

After GPU-48-R1 PASS, rerun GPU-48:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_48_forward_boundary_gpu_buffer_upload_execution -- `
  --upload-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --selected-group-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --selected-group-id selected-atlas-group-unknown `
  --max-upload-bytes 2048 `
  --out .\artifacts\ASH_BASETRAIN_GPU_48_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_EXECUTION.json
```
