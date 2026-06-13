# ASH-BASETRAIN-GPU-41 Spec

## Patch ID

`ASH-BASETRAIN-GPU-41`

## Patch Title

Projection Segment Stitch Candidate / Multi Row-Block Output Assembly Review Gate / No Logits Adoption No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-41` uses the `ASH-BASETRAIN-GPU-40` PASS segmented dispatch matrix receipt as the primary gate, validates all finite/parity-passed/released segment outputs, assembles them into a projection stitch candidate with an explicit segment source map and digest, and places that candidate behind an evidence-only review gate. It does not materialize logits, adopt model output, run loss/backward/optimizer, mutate weights, or write checkpoints/safetensors.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json`
- `artifacts/ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_41_projection_segment_stitch_review_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_41_projection_segment_stitch_review_gate.rs`

## Required 40 Gate

- `patch_id == ASH-BASETRAIN-GPU-40`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_40`
- `artifact_write.runtime_receipt_written == true`
- `segment_plan.segment_count >= 2`
- `segment_plan.row_count_per_segment == 256`
- `segment_plan.input_vector_len == 256`
- `segment_plan.total_output_count == 512`
- `segment_plan.stitching_executed == false`
- `segment_plan.logits_materialized == false`
- `segment_plan.forward_output_adopted == false`
- `segmented_dispatch_matrix.matrix_created == true`
- `segmented_dispatch_matrix.completed_segment_count == segment_plan.segment_count`
- `segmented_dispatch_matrix.failed_segment_count == 0`
- `segmented_dispatch_matrix.all_segments_released == true`
- `segmented_dispatch_matrix.all_segments_finite == true`
- `segmented_dispatch_matrix.all_segments_parity_passed == true`
- `segmented_dispatch_matrix.matrix_digest_hex != ""`

## Segment Gate

For every segment:

- `final_state == Released`
- `release_executed == true`
- `actual_dispatch_executed == true`
- `actual_readback_executed == true`
- `output_count == 256`
- `finite_check_passed == true`
- `gpu_cpu_output_parity_passed == true`
- `mismatched_value_count == 0`
- `output_digest_hex != ""`

## Projection Stitch Candidate Contract

- `stitch_candidate_created == true`
- `stitching_executed == true`
- `stitch_order == ascending_segment_index`
- `segment_count == 2`
- `row_count_per_segment == 256`
- `projection_output_count == 512`
- `projection_candidate_shape == [512]`
- `projection_candidate_digest_hex != ""`
- `shape_coercion_used == false`
- `missing_segment_filled == false`
- `logits_materialized == false`
- `forward_output_adopted == false`

Initial source map:

- `projection[0..255] <- segment[0].output[0..255]`
- `projection[256..511] <- segment[1].output[0..255]`

## Review Gate Contract

- `review_gate_created == true`
- `review_gate_mode == evidence_only`
- `projection_candidate_ready_for_review == true`
- `operator_approval_required_next == true`
- `projection_candidate_adopted_now == false`
- `logits_allowed_next == false`
- `optimizer_allowed_next == false`

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

- `BLOCKED_40_RECEIPT_NOT_FOUND`
- `BLOCKED_40_RECEIPT_READ_FAILED`
- `BLOCKED_40_RECEIPT_PARSE_FAILED`
- `BLOCKED_40_RECEIPT_NOT_PASS`
- `BLOCKED_40_SEGMENT_MATRIX_INVALID`
- `BLOCKED_40_SEGMENT_OUTPUT_INVALID`
- `BLOCKED_40_SEGMENT_DIGEST_MISSING`
- `BLOCKED_40_SEGMENT_PARITY_NOT_PASS`
- `BLOCKED_40_SEGMENT_NOT_RELEASED`
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
- `BLOCKED_PROJECTION_STITCH_SEGMENT_COUNT_INVALID`
- `BLOCKED_PROJECTION_STITCH_SHAPE_MISMATCH`
- `BLOCKED_PROJECTION_STITCH_SOURCE_MAP_INVALID`
- `BLOCKED_PROJECTION_STITCH_DIGEST_FAILED`
- `BLOCKED_PROJECTION_STITCH_MISSING_SEGMENT`
- `BLOCKED_PROJECTION_STITCH_SHAPE_COERCION_DETECTED`
- `BLOCKED_PROJECTION_STITCH_ZERO_FILL_DETECTED`
- `BLOCKED_REVIEW_GATE_NOT_CREATED`
- `BLOCKED_REVIEW_GATE_ADOPTION_LEAK`
- `BLOCKED_LOGITS_ADOPTION_GUARD_FAILED`
- `BLOCKED_OPTIMIZER_GUARD_FAILED`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_41_projection_segment_stitch_review_gate -- `
  --segmented-dispatch-matrix-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --slot-ring-receipt .\artifacts\ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json `
  --forward-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json `
  --reduction-parity-receipt .\artifacts\ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json `
  --multi-workgroup-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## Next Patch

`ASH-BASETRAIN-GPU-42` — Projection Candidate Review Approval Gate / Operator Approved Stitch Candidate Promotion Seal / No Logits No Optimizer

## Final Acceptance Sentence

ASH-BASETRAIN-GPU-41 is accepted only if a real ASH-BASETRAIN-GPU-40 PASS segmented dispatch matrix receipt opens a projection stitch candidate, all segment outputs are validated as finite/parity-passed/released, the projection candidate is assembled with an explicit source map and digest, the candidate is placed behind a review gate without adoption, a runtime receipt is written, and model forward, logits materialization/adoption, loss, backward, optimizer, checkpoint, safetensors write, and weight mutation remain sealed.
