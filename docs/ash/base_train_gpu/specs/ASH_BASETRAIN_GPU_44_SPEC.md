# ASH-BASETRAIN-GPU-44 Spec

## Patch ID

`ASH-BASETRAIN-GPU-44`

## Patch Title

Forward Boundary Execution Preflight / Approved Projection Candidate To Next Kernel Input Contract Seal / No Logits No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-44` uses the `ASH-BASETRAIN-GPU-43` PASS handoff boundary receipt as the primary gate, validates the metadata-only handoff envelope and next-stage boundary candidate, then creates a next-kernel input contract and binding-layout preflight metadata without creating GPU buffers, bind groups, or dispatching kernels.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_43_APPROVED_PROJECTION_HANDOFF_BOUNDARY.json`

## Secondary Inputs

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

`artifacts/ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_44_forward_boundary_execution_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_44_forward_boundary_execution_preflight.rs`

## Required 43 Gate

- `patch_id == ASH-BASETRAIN-GPU-43`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_43`
- `artifact_write.runtime_receipt_written == true`
- `approved_projection_validation.approved_projection_candidate_created == true`
- `approved_projection_validation.approved_projection_candidate_digest_hex != ""`
- `approved_projection_validation.approved_projection_candidate_shape == [512]`
- `approved_projection_validation.source_map_preserved == true`
- `approved_projection_validation.operator_approval_valid == true`
- `approved_projection_validation.projection_candidate_adopted_as_model_output == false`
- `approved_projection_validation.logits_materialized == false`
- `handoff_boundary_envelope.handoff_envelope_created == true`
- `handoff_boundary_envelope.handoff_mode == metadata_only`
- `handoff_boundary_envelope.next_boundary_kind == projection_to_forward_input`
- `handoff_boundary_envelope.source_map_preserved == true`
- `handoff_boundary_envelope.upstream_chain_preserved == true`
- `handoff_boundary_envelope.handoff_execution_allowed_now == false`
- `next_stage_boundary_candidate.next_stage_boundary_candidate_created == true`
- `next_stage_boundary_candidate.next_stage_boundary_candidate_shape == [512]`
- `next_stage_boundary_candidate.next_stage_boundary_candidate_ready_for_review == true`
- `next_stage_boundary_candidate.next_stage_boundary_execution_authorized == false`
- `next_stage_boundary_candidate.requires_next_stage_execution_gate == true`

## Next Kernel Input Contract

- `next_kernel_input_contract_created == true`
- `input_contract_mode == metadata_only`
- `input_candidate_kind == approved_projection_as_forward_boundary_input`
- `input_source_patch_id == ASH-BASETRAIN-GPU-43`
- `input_shape == [512]`
- `input_element_count == 512`
- `input_dtype == f32`
- `input_byte_len == 2048`
- `input_alignment_bytes == 4`
- `binding_slot == 0`
- `binding_visibility == compute`
- `binding_layout_preflight_created == true`
- `binding_layout_kind == storage_readonly_input`
- `actual_gpu_buffer_created == false`
- `actual_gpu_bind_group_created == false`
- `actual_kernel_dispatch_executed == false`

## Guards

The following must remain false:

- `model_forward_executed`
- `forward_output_adopted`
- `logits_materialized`
- `logits_written`
- `loss_computed`
- `backward_executed`
- `optimizer_created`
- `optimizer_step_executed`
- `gradient_buffer_written`
- `delta_candidate_written`
- `weight_buffer_mutated`
- `checkpoint_written`
- `safetensors_written`
- `training_commit_executed`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_44_forward_boundary_execution_preflight -- `
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

`ASH-BASETRAIN-GPU-45` — Forward Boundary Buffer Materialization Candidate / Approved Projection Input To GPU Buffer Bind Preflight Seal / No Dispatch No Logits No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-44 is accepted only if a real ASH-BASETRAIN-GPU-43 PASS handoff boundary receipt opens a next-kernel input contract preflight, the approved projection digest, shape, source map, and upstream chain are preserved, binding layout metadata is sealed without creating GPU buffers or dispatching kernels, a runtime receipt is written, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
