# ASH-BASETRAIN-GPU-46 Spec

## Patch ID

`ASH-BASETRAIN-GPU-46`

## Patch Title

Forward Boundary GPU Buffer Creation Dryrun / Approved Projection Input Buffer Allocation Seal / No Upload No Dispatch No Logits No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-46` uses the `ASH-BASETRAIN-GPU-45` PASS buffer materialization candidate receipt as the primary gate, validates descriptor-only buffer and bind candidates, performs GPU device and buffer-limit preflight, and attempts a transient dryrun-owned storage buffer allocation without upload, bind-group creation, pipeline creation, dispatch, runtime adoption, or model-state export.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json`
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

`artifacts/ASH_BASETRAIN_GPU_46_FORWARD_BOUNDARY_GPU_BUFFER_CREATION_DRYRUN.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_46_forward_boundary_gpu_buffer_creation_dryrun.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_46_forward_boundary_gpu_buffer_creation_dryrun.rs`

## Required 45 Gate

- `patch_id == ASH-BASETRAIN-GPU-45`
- `pass == true`
- `verdict == PASS`
- `artifact_write.runtime_receipt_written == true`
- `buffer_materialization_candidate.buffer_materialization_candidate_created == true`
- `buffer_materialization_candidate.materialization_mode == descriptor_only`
- `buffer_materialization_candidate.buffer_shape == [512]`
- `buffer_materialization_candidate.buffer_element_count == 512`
- `buffer_materialization_candidate.buffer_dtype == f32`
- `buffer_materialization_candidate.buffer_byte_len == 2048`
- `buffer_materialization_candidate.buffer_alignment_bytes == 4`
- `buffer_materialization_candidate.buffer_usage == storage_readonly`
- `buffer_materialization_candidate.actual_gpu_buffer_created == false`
- `buffer_materialization_candidate.actual_gpu_buffer_uploaded == false`
- `bind_group_candidate.bind_group_candidate_created == true`
- `bind_group_candidate.binding_slot == 0`
- `bind_group_candidate.binding_visibility == compute`
- `bind_group_candidate.actual_bind_group_created == false`
- `bind_group_candidate.actual_dispatch_executed == false`
- `execution_control.dispatch_allowed_now == false`
- `execution_control.model_forward_allowed_now == false`
- `execution_control.logits_allowed_now == false`
- `execution_control.optimizer_allowed_now == false`

## GPU Buffer Allocation Dryrun Contract

- `gpu_device_preflight_created == true`
- `gpu_device_available == true`
- `max_storage_buffer_binding_size_checked == true`
- `required_buffer_byte_len == 2048`
- `required_buffer_byte_len_within_limit == true`
- `required_alignment_bytes == 4`
- `required_alignment_satisfied == true`
- `buffer_allocation_dryrun_created == true`
- `dryrun_allocation_mode == transient_resource`
- `buffer_allocation_candidate_kind == approved_projection_input_storage_buffer`
- `buffer_shape == [512]`
- `buffer_element_count == 512`
- `buffer_dtype == f32`
- `buffer_byte_len == 2048`
- `buffer_usage == storage_readonly`
- `actual_gpu_buffer_created_for_dryrun == true`
- `actual_gpu_buffer_upload_performed == false`
- `actual_gpu_buffer_map_write_performed == false`
- `actual_gpu_buffer_bound_to_pipeline == false`
- `dryrun_resource_adopted_by_runtime == false`
- `dryrun_resource_exported_as_model_state == false`
- `dryrun_resource_used_for_dispatch == false`
- `dryrun_resource_released_or_dropped_before_exit == true`

## Guard Contract

The following must remain false:

- `actual_bind_group_created`
- `actual_pipeline_layout_created`
- `actual_compute_pipeline_created`
- `actual_kernel_dispatch_executed`
- `model_forward_executed`
- `forward_output_adopted`
- `logits_materialized`
- `logits_written`
- `loss_computed`
- `backward_executed`
- `optimizer_created`
- `optimizer_step_executed`
- `weight_buffer_mutated`
- `checkpoint_written`
- `safetensors_written`
- `training_commit_executed`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_46_forward_boundary_gpu_buffer_creation_dryrun -- `
  --buffer-materialization-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json `
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

`ASH-BASETRAIN-GPU-47` — Forward Boundary GPU Buffer Upload Candidate / Approved Projection Input Host To Device Upload Seal / No Bind Group No Dispatch No Logits No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-46 is accepted only if a real ASH-BASETRAIN-GPU-45 PASS buffer materialization candidate receipt opens a GPU buffer allocation dryrun, device limits and alignment are checked, a transient dryrun-owned GPU buffer allocation receipt is sealed without upload, bind group creation, pipeline creation, dispatch, runtime adoption, or model state export, a runtime receipt is written, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
