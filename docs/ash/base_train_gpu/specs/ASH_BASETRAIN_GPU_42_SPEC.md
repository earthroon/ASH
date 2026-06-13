# ASH-BASETRAIN-GPU-42 Spec

## Patch ID

`ASH-BASETRAIN-GPU-42`

## Patch Title

Projection Candidate Review Approval Gate / Operator Approved Stitch Candidate Promotion Seal / No Logits No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-42` uses the `ASH-BASETRAIN-GPU-41` PASS projection stitch review gate receipt as the primary gate, requires explicit operator approval by token or approval receipt, validates that the projection candidate digest and source map are preserved, and seals an approved projection candidate without treating it as logits, model output, or training commit.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`
- `artifacts/ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json`
- `artifacts/ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Approval Input

Initial token:

`APPROVE_ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE`

Silent approval is forbidden. The approval must come from CLI or an approval receipt.

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_42_projection_candidate_review_approval_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_42_projection_candidate_review_approval_gate.rs`

## Required 41 Gate

- `patch_id == ASH-BASETRAIN-GPU-41`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_41`
- `artifact_write.runtime_receipt_written == true`
- `projection_stitch_candidate.stitch_candidate_created == true`
- `projection_stitch_candidate.stitching_executed == true`
- `projection_stitch_candidate.projection_output_count == 512`
- `projection_stitch_candidate.projection_candidate_shape == [512]`
- `projection_stitch_candidate.projection_candidate_digest_hex != ""`
- `projection_stitch_candidate.shape_coercion_used == false`
- `projection_stitch_candidate.missing_segment_filled == false`
- `projection_stitch_candidate.logits_materialized == false`
- `projection_stitch_candidate.forward_output_adopted == false`
- `review_gate.review_gate_created == true`
- `review_gate.review_gate_mode == evidence_only`
- `review_gate.projection_candidate_ready_for_review == true`
- `review_gate.operator_approval_required_next == true`
- `review_gate.projection_candidate_adopted_now == false`
- `review_gate.logits_allowed_next == false`
- `review_gate.optimizer_allowed_next == false`

## Operator Approval Contract

Without approval:

- `operator_approval_present == false`
- `approved_projection_candidate_created == false`
- blocked with `BLOCKED_OPERATOR_APPROVAL_MISSING`

Token approval:

- `operator_approval_present == true`
- `approval_mode == token`
- `approval_token_supplied == true`
- `approval_token_valid == true`
- `approval_token_expected == APPROVE_ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE`

Receipt approval must include:

```json
{
  "approval_patch_target": "ASH-BASETRAIN-GPU-42",
  "approval_scope": "projection_candidate_review_gate",
  "operator_approval": true,
  "operator_id": "operator",
  "approval_note": "approve projection stitch candidate for next gated stage",
  "approved_projection_candidate_digest_hex": "<41 projection_candidate_digest_hex>"
}
```

## Approved Projection Candidate Contract

- `approved_projection_candidate_created == true`
- `approved_projection_candidate_kind == operator_approved_projection_stitch_candidate`
- `approved_projection_candidate_digest_hex == 41.projection_candidate_digest_hex`
- `approved_projection_candidate_shape == [512]`
- `approved_projection_candidate_source_receipt_patch_id == ASH-BASETRAIN-GPU-41`
- `approved_projection_candidate_source_map_preserved == true`
- `projection_candidate_adopted_as_model_output == false`
- `logits_materialized == false`

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

## Blocked Codes

- `BLOCKED_41_RECEIPT_NOT_FOUND`
- `BLOCKED_41_RECEIPT_READ_FAILED`
- `BLOCKED_41_RECEIPT_PARSE_FAILED`
- `BLOCKED_41_RECEIPT_NOT_PASS`
- `BLOCKED_41_PROJECTION_CANDIDATE_INVALID`
- `BLOCKED_41_REVIEW_GATE_INVALID`
- `BLOCKED_41_SOURCE_MAP_INVALID`
- `BLOCKED_41_CANDIDATE_DIGEST_MISSING`
- `BLOCKED_40_RECEIPT_NOT_FOUND`
- `BLOCKED_40_RECEIPT_NOT_PASS`
- `BLOCKED_39_RECEIPT_NOT_FOUND`
- `BLOCKED_39_RECEIPT_NOT_PASS`
- `BLOCKED_38_RECEIPT_NOT_FOUND`
- `BLOCKED_38_RECEIPT_NOT_PASS`
- `BLOCKED_37R_R2_RECEIPT_NOT_FOUND`
- `BLOCKED_37R_R2_RECEIPT_NOT_PASS`
- `BLOCKED_37Q_R1_RECEIPT_NOT_FOUND`
- `BLOCKED_37Q_R1_RECEIPT_NOT_PASS`
- `BLOCKED_37P_R1_RECEIPT_NOT_FOUND`
- `BLOCKED_37P_R1_RECEIPT_NOT_PASS`
- `BLOCKED_37F_RECEIPT_NOT_FOUND`
- `BLOCKED_37F_RECEIPT_NOT_PASS`
- `BLOCKED_OPERATOR_APPROVAL_MISSING`
- `BLOCKED_OPERATOR_APPROVAL_TOKEN_INVALID`
- `BLOCKED_OPERATOR_APPROVAL_RECEIPT_NOT_FOUND`
- `BLOCKED_OPERATOR_APPROVAL_RECEIPT_INVALID`
- `BLOCKED_OPERATOR_APPROVAL_DIGEST_MISMATCH`
- `BLOCKED_APPROVED_PROJECTION_CANDIDATE_DIGEST_FAILED`
- `BLOCKED_APPROVED_PROJECTION_CANDIDATE_SHAPE_MISMATCH`
- `BLOCKED_APPROVED_PROJECTION_CANDIDATE_SOURCE_MAP_LOST`
- `BLOCKED_APPROVED_PROJECTION_CANDIDATE_ADOPTION_LEAK`
- `BLOCKED_LOGITS_GUARD_FAILED`
- `BLOCKED_OPTIMIZER_GUARD_FAILED`
- `BLOCKED_WEIGHT_MUTATION_GUARD_FAILED`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_42_projection_candidate_review_approval_gate -- `
  --projection-stitch-review-receipt .\artifacts\ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json `
  --segmented-dispatch-matrix-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --slot-ring-receipt .\artifacts\ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json `
  --forward-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json `
  --reduction-parity-receipt .\artifacts\ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json `
  --multi-workgroup-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json `
  --operator-approval-token APPROVE_ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE
```

## Next Patch

`ASH-BASETRAIN-GPU-43` — Approved Projection Candidate Handoff / Next Stage Forward Boundary Candidate Seal / No Logits Materialization No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-42 is accepted only if a real ASH-BASETRAIN-GPU-41 PASS projection stitch review gate receipt opens an explicit operator approval gate, the approval token or approval receipt is valid, the projection candidate digest and source map are preserved, an approved projection candidate receipt is written without treating it as logits or model output, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
