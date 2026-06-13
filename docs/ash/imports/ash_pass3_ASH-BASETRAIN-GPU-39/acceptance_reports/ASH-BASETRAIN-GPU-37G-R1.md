# ASH-BASETRAIN-GPU-37G-R1 Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37G-R1 — GPU Readback Receipt Binding Repair / 37F Verified Digest Rebind No Dispatch Seal

## Source SSOT

- Input SSOT: `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`
- State ownership: `crates/base_train`
- This patch does not open the source shard, GPU device, shader module, pipeline, bind group, dispatch, forward, backward, optimizer, or mutation route.

## Repair

37G previously expected the 37F readback smoke digest under `source_binding.*`.
The actual 37F receipt provides the required verified digest fields under:

- `gpu_upload_readback_smoke_summary.combined_row_block_gpu_upload_readback_smoke_digest_hex`
- `gpu_upload_readback_smoke_summary.gpu_upload_readback_execution_digest_hex`
- `gpu_upload_readback_smoke_summary.combined_gpu_readback_source_byte_digest_hex`
- `gpu_upload_readback_smoke_summary.cpu_source_payload_raw_sha256_hex`
- `gpu_upload_readback_smoke_summary.gpu_readback_byte_digest_hex`
- `gpu_readback_digest_receipt.cpu_source_payload_raw_sha256_hex`
- `gpu_readback_digest_receipt.gpu_readback_raw_sha256_hex`

37G-R1 rebinds the lookup path and cross-checks summary fields against `gpu_readback_digest_receipt`.

## Expected PASS

```txt
PASS_ASH_BASETRAIN_GPU_37G_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PROMOTION_GATE_VERIFIED_READBACK_BUFFER_TO_DISPATCH_CANDIDATE_NO_FORWARD_NO_BACKWARD
```

## Required local run

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37g_selected_group_row_block_gpu_upload_promotion_gate
cargo run -p base_train --bin ash_basetrain_gpu_37g_selected_group_row_block_gpu_upload_promotion_gate -- --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## Guard Contract

- `file_open_used = false`
- `row_block_read_executed = false`
- `f32_decode_executed = false`
- `actual_gpu_device_requested = false`
- `actual_gpu_buffer_created = false`
- `actual_queue_upload_executed = false`
- `actual_readback_executed = false`
- `actual_shader_module_created = false`
- `actual_compute_pipeline_created = false`
- `actual_bind_group_created = false`
- `actual_dispatch_executed = false`
- `forward/backward/optimizer/mutation = false`

## Next

If PASS, proceed to:

```txt
ASH-BASETRAIN-GPU-37H
Selected Group Row-Block Shader Module Compile Candidate /
Dispatch Candidate To WGSL Contract No Dispatch Seal
```
