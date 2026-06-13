# ASH-BASETRAIN-GPU-45 Spec

## Patch ID

`ASH-BASETRAIN-GPU-45`

## Patch Title

Forward Boundary Buffer Materialization Candidate / Approved Projection Input To GPU Buffer Bind Preflight Seal / No Dispatch No Logits No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-45` uses the `ASH-BASETRAIN-GPU-44` PASS forward boundary preflight receipt as the primary gate, validates the next-kernel input contract, and creates descriptor-only buffer materialization and bind-group candidates without creating GPU buffers, uploading buffers, creating bind groups, creating pipelines, or dispatching kernels.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_43_APPROVED_PROJECTION_HANDOFF_BOUNDARY.json`
- `artifacts/ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`
- `artifacts/ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json`
- `artifacts/ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_45_forward_boundary_buffer_materialization_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_45_forward_boundary_buffer_materialization_candidate.rs`

## Required 44 Gate

- `patch_id == ASH-BASETRAIN-GPU-44`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_44`
- `artifact_write.runtime_receipt_written == true`
- `next_kernel_input_contract.next_kernel_input_contract_created == true`
- `next_kernel_input_contract.input_contract_mode == metadata_only`
- `next_kernel_input_contract.input_candidate_kind == approved_projection_as_forward_boundary_input`
- `next_kernel_input_contract.input_source_patch_id == ASH-BASETRAIN-GPU-43`
- `next_kernel_input_contract.input_source_digest_hex != ""`
- `next_kernel_input_contract.input_shape == [512]`
- `next_kernel_input_contract.input_element_count == 512`
- `next_kernel_input_contract.input_dtype == f32`
- `next_kernel_input_contract.input_byte_len == 2048`
- `next_kernel_input_contract.input_alignment_bytes == 4`
- `next_kernel_input_contract.binding_slot == 0`
- `next_kernel_input_contract.binding_visibility == compute`
- `next_kernel_input_contract.binding_layout_preflight_created == true`
- `next_kernel_input_contract.binding_layout_kind == storage_readonly_input`
- `next_kernel_input_contract.binding_layout_digest_hex != ""`
- `next_kernel_input_contract.actual_gpu_buffer_created == false`
- `next_kernel_input_contract.actual_gpu_bind_group_created == false`
- `next_kernel_input_contract.actual_kernel_dispatch_executed == false`
- `execution_preflight.next_kernel_dispatch_allowed_now == false`
- `execution_preflight.model_forward_allowed_now == false`
- `execution_preflight.logits_allowed_now == false`
- `execution_preflight.optimizer_allowed_now == false`

## Buffer Materialization Candidate Contract

- `buffer_materialization_candidate_created == true`
- `materialization_mode == descriptor_only`
- `buffer_candidate_kind == approved_projection_forward_boundary_storage_input`
- `buffer_source_patch_id == ASH-BASETRAIN-GPU-44`
- `buffer_shape == [512]`
- `buffer_element_count == 512`
- `buffer_dtype == f32`
- `buffer_byte_len == 2048`
- `buffer_alignment_bytes == 4`
- `buffer_usage == storage_readonly`
- `buffer_descriptor_digest_hex != ""`
- `actual_gpu_buffer_created == false`
- `actual_gpu_buffer_uploaded == false`
- `actual_gpu_buffer_mapped == false`
- `actual_gpu_buffer_unmapped == false`

## Bind Group Candidate Contract

- `bind_group_candidate_created == true`
- `bind_group_candidate_kind == readonly_storage_input_bind_candidate`
- `binding_slot == 0`
- `binding_visibility == compute`
- `bind_group_descriptor_digest_hex != ""`
- `bind_group_ready_for_materialization_next == true`
- `actual_bind_group_created == false`
- `actual_pipeline_layout_created == false`
- `actual_compute_pipeline_created == false`
- `actual_dispatch_executed == false`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_45_forward_boundary_buffer_materialization_candidate -- `
  --forward-boundary-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json `
  --handoff-boundary-receipt .\artifacts\ASH_BASETRAIN_GPU_43_APPROVED_PROJECTION_HANDOFF_BOUNDARY.json `
  --approved-projection-receipt .\artifacts\ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json `
  --projection-stitch-review-receipt .\artifacts\ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json `
  --segmented-dispatch-matrix-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --slot-ring-receipt .\artifacts\ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json `
  --forward-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json `
  --reduction-parity-receipt .\artifacts\ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json `
  --multi-workgroup-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## Next Patch

`ASH-BASETRAIN-GPU-46` — Forward Boundary GPU Buffer Creation Dryrun / Approved Projection Input Buffer Allocation Seal / No Dispatch No Logits No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-45 is accepted only if a real ASH-BASETRAIN-GPU-44 PASS forward boundary preflight receipt opens a buffer materialization candidate and bind-group candidate, the approved projection input shape, dtype, byte length, alignment, digest, and binding layout are preserved, no actual GPU buffer, bind group, pipeline, or dispatch is created, a runtime receipt is written, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
