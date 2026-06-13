# ASH-BASETRAIN-GPU-47 Spec

## Patch ID

`ASH-BASETRAIN-GPU-47`

## Patch Title

Forward Boundary GPU Buffer Upload Candidate / Approved Projection Input Host To Device Upload Seal / No Bind Group No Dispatch No Logits No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-47` uses the `ASH-BASETRAIN-GPU-46` PASS GPU buffer creation dryrun receipt as the primary gate, validates the transient buffer allocation and source digest chain, then creates a candidate-only host-to-device upload descriptor. It does not upload bytes, create a bind group, create a pipeline, dispatch a kernel, materialize logits, or run an optimizer.

47 is not an actual upload execution patch. It is the upload candidate seal.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_46_FORWARD_BOUNDARY_GPU_BUFFER_CREATION_DRYRUN.json`

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_47_forward_boundary_gpu_buffer_upload_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_47_forward_boundary_gpu_buffer_upload_candidate.rs`

## Required Gates

- `46.pass == true`
- `46.buffer_allocation_dryrun.buffer_allocation_dryrun_created == true`
- `46.buffer_allocation_dryrun.actual_gpu_buffer_upload_performed == false`
- `46.buffer_allocation_dryrun.actual_gpu_buffer_map_write_performed == false`
- `46.buffer_allocation_dryrun.actual_gpu_buffer_bound_to_pipeline == false`
- `46.dryrun_resource_lifetime.dryrun_resource_released_or_dropped_before_exit == true`
- `46.bind_and_dispatch_boundary.actual_bind_group_created == false`
- `46.bind_and_dispatch_boundary.actual_kernel_dispatch_executed == false`
- `45.pass == true`
- `45.buffer_materialization_candidate.buffer_source_digest_hex == 46.buffer_allocation_dryrun.buffer_source_digest_hex`

## Upload Candidate Contract

Default mode is `candidate_only`.

- `gpu_buffer_upload_candidate_created == true`
- `upload_mode == candidate_only`
- `upload_candidate_kind == approved_projection_host_to_device_storage_upload`
- `source_projection_digest_hex == 46.buffer_allocation_dryrun.buffer_source_digest_hex`
- `target_buffer_usage == storage_readonly`
- `target_binding_slot == 0`
- `target_binding_visibility == compute`
- `target_byte_len == 2048`
- `target_alignment_bytes == 4`
- `upload_candidate_ready_for_probe_next == true`
- `actual_gpu_buffer_created_for_upload_probe == false`
- `actual_gpu_buffer_upload_performed == false`
- `actual_gpu_buffer_map_write_performed == false`

## Payload Source Handling

- Explicit payload may be provided with `--approved-projection-payload-path`.
- If no payload is provided, 47 still passes as candidate-only and records `payload_source_kind = deferred_to_upload_probe`.
- 47 must not claim payload reconstruction from digest-only metadata.
- 47 must not use zero-vector fallback or placeholder payload.

## Forbidden in 47

- actual upload
- bind group creation
- pipeline layout creation
- compute pipeline creation
- kernel dispatch
- model forward
- logits materialization
- loss/backward
- optimizer step
- weight mutation
- checkpoint write
- safetensors write

## Next Patch

`ASH-BASETRAIN-GPU-48` — Forward Boundary GPU Upload Probe / Approved Projection Host Payload To Transient Device Buffer Write Seal / No Bind Group No Dispatch No Logits No Optimizer
