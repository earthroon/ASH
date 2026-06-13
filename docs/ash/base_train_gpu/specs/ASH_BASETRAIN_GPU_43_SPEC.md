# ASH-BASETRAIN-GPU-43 Spec

## Patch ID

`ASH-BASETRAIN-GPU-43`

## Patch Title

Approved Projection Candidate Handoff / Next Stage Forward Boundary Candidate Seal / No Logits Materialization No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-43` uses the `ASH-BASETRAIN-GPU-42` PASS approved projection candidate receipt as the primary gate, validates the approved candidate digest, shape, source-map preservation, and operator approval validity, then creates a metadata-only handoff boundary envelope and a next-stage boundary candidate without authorizing execution.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`
- `artifacts/ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json`
- `artifacts/ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_43_APPROVED_PROJECTION_HANDOFF_BOUNDARY.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_43_approved_projection_handoff_boundary.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_43_approved_projection_handoff_boundary.rs`

## Required 42 Gate

- `patch_id == ASH-BASETRAIN-GPU-42`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_42`
- `artifact_write.runtime_receipt_written == true`
- `approved_projection_candidate.approved_projection_candidate_created == true`
- `approved_projection_candidate.approved_projection_candidate_kind == operator_approved_projection_stitch_candidate`
- `approved_projection_candidate.approved_projection_candidate_digest_hex != ""`
- `approved_projection_candidate.approved_projection_candidate_shape == [512]`
- `approved_projection_candidate.source_map_preserved == true`
- `approved_projection_candidate.source_projection_receipt_patch_id == ASH-BASETRAIN-GPU-41`
- `approved_projection_candidate.projection_candidate_adopted_as_model_output == false`
- `approved_projection_candidate.logits_materialized == false`
- `operator_approval.operator_approval_required == true`
- `operator_approval.operator_approval_present == true`
- `operator_approval.approval_token_valid == true OR operator_approval.approval_receipt_valid == true`
- `review_gate.review_gate_approved == true`
- `review_gate.approved_candidate_ready_for_next_stage == true`
- `review_gate.logits_allowed_next == false`
- `review_gate.optimizer_allowed_next == false`

## Handoff Boundary Envelope Contract

- `handoff_envelope_created == true`
- `handoff_envelope_kind == approved_projection_candidate_handoff`
- `handoff_mode == metadata_only`
- `next_boundary_kind == projection_to_forward_input`
- `source_patch_id == ASH-BASETRAIN-GPU-42`
- `source_projection_digest_hex == 42.approved_projection_candidate_digest_hex`
- `source_projection_shape == [512]`
- `source_map_preserved == true`
- `upstream_chain_preserved == true`
- `handoff_envelope_digest_hex != ""`
- `handoff_execution_allowed_now == false`

## Next Stage Boundary Candidate Contract

- `next_stage_boundary_candidate_created == true`
- `next_stage_boundary_candidate_kind == projection_output_to_forward_boundary_input`
- `next_stage_boundary_candidate_shape == [512]`
- `next_stage_boundary_candidate_digest_hex == approved_projection_validation.approved_projection_candidate_digest_hex`
- `next_stage_boundary_candidate_ready_for_review == true`
- `next_stage_boundary_execution_authorized == false`
- `requires_next_stage_execution_gate == true`

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
cargo run -p base_train --bin ash_basetrain_gpu_43_approved_projection_handoff_boundary -- `
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

`ASH-BASETRAIN-GPU-44` — Forward Boundary Execution Preflight / Approved Projection Candidate To Next Kernel Input Contract Seal / No Logits No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-43 is accepted only if a real ASH-BASETRAIN-GPU-42 PASS approved projection candidate receipt opens a handoff boundary envelope, the approved candidate digest, shape, source map, and operator approval validity are preserved, a next-stage boundary candidate is created without authorizing execution, a runtime receipt is written, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
