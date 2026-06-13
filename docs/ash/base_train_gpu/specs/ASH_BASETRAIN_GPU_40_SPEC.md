# ASH-BASETRAIN-GPU-40 Spec

## Patch ID

`ASH-BASETRAIN-GPU-40`

## Patch Title

Multi Row-Block MatVec Candidate / Segmented Atlas Group Dispatch Matrix Seal / No Logits Adoption No Optimizer

## SSOT One-Liner

`ASH-BASETRAIN-GPU-40` uses the `ASH-BASETRAIN-GPU-39` Atlas Upload Ring Buffer / slot lease-release PASS receipt as the primary gate, then processes at least two row-block segments through explicit lease/fill/upload/dispatch/readback/release and seals the outputs as a segmented dispatch matrix. It does not materialize logits, adopt forward output, run loss/backward/optimizer, mutate weights, or write checkpoints/safetensors.

## Primary Input

`artifacts/ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json`

## Secondary Inputs

- `artifacts/ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Output Receipt

`artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json`

## Code SSOT

- `crates/base_train/src/ash_basetrain_gpu_40_multi_row_block_matvec_segmented_dispatch_matrix.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_40_multi_row_block_matvec_segmented_dispatch_matrix.rs`

## Default Segment Contract

- `segment_count = 2`
- `row_count_per_segment = 256`
- `input_vector_len = 256`
- `slot_count = 2`
- `slot_size_bytes >= 262144`
- `segment_matrix_shape = [2, 256]`
- `total_output_count = 512`

## Required 39 Gate

- `patch_id == ASH-BASETRAIN-GPU-39`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_39`
- `artifact_write.runtime_receipt_written == true`
- `atlas_upload_ring.ring_created == true`
- `atlas_upload_ring.slot_count >= 2`
- `atlas_upload_ring.slot_size_bytes >= 262144`
- `atlas_upload_ring.max_active_leases == 1`
- `atlas_upload_ring.reuse_policy == release_before_reuse`
- `slot_lifecycle.final_state == Released`
- `slot_lifecycle.release_executed == true`
- `slot_lifecycle.reuse_before_release_detected == false`
- `slot_lifecycle.overwrite_while_active_detected == false`
- `bounded_matvec_candidate.actual_dispatch_executed == true`
- `bounded_matvec_candidate.actual_readback_executed == true`
- `bounded_matvec_candidate.gpu_cpu_output_parity_passed == true`
- `bounded_matvec_candidate.mismatched_value_count == 0`

## Segment Lifecycle

Each segment must independently seal this lifecycle:

```txt
Empty
-> Leased
-> CpuPayloadFilled
-> GpuUploadSubmitted
-> GpuUploadVisible
-> DispatchUseActive
-> OutputReadbackVerified
-> Released
```

Sequential reuse is allowed only after the previous segment has reached `Released`.

## Runtime PASS Criteria

- `patch_id == ASH-BASETRAIN-GPU-40`
- `pass == true`
- `verdict == PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_40`
- `source_binding.slot_ring_receipt_patch_id == ASH-BASETRAIN-GPU-39`
- `source_binding.slot_ring_receipt_pass == true`
- `segment_plan.segment_count >= 2`
- `segmented_dispatch_matrix.matrix_created == true`
- `segmented_dispatch_matrix.completed_segment_count == segment_plan.segment_count`
- `segmented_dispatch_matrix.failed_segment_count == 0`
- `segmented_dispatch_matrix.all_segments_released == true`
- `segmented_dispatch_matrix.all_segments_finite == true`
- `segmented_dispatch_matrix.all_segments_parity_passed == true`
- Every segment has `final_state == Released`, `release_executed == true`, `actual_dispatch_executed == true`, `actual_readback_executed == true`, `finite_check_passed == true`, and `gpu_cpu_output_parity_passed == true`.
- `artifact_write.runtime_receipt_written == true`
- `next_patch_if_pass == ASH-BASETRAIN-GPU-41`

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

- `BLOCKED_39_RECEIPT_NOT_FOUND`
- `BLOCKED_39_RECEIPT_READ_FAILED`
- `BLOCKED_39_RECEIPT_PARSE_FAILED`
- `BLOCKED_39_RECEIPT_NOT_PASS`
- `BLOCKED_39_RING_CONTRACT_INVALID`
- `BLOCKED_39_SLOT_LIFECYCLE_INVALID`
- `BLOCKED_39_MATVEC_CANDIDATE_INVALID`
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
- `BLOCKED_SEGMENT_COUNT_INVALID`
- `BLOCKED_SEGMENT_ROW_COUNT_INVALID`
- `BLOCKED_SEGMENT_SOURCE_RANGE_UNAVAILABLE`
- `BLOCKED_SEGMENT_SOURCE_READ_FAILED`
- `BLOCKED_SEGMENT_PAYLOAD_EMPTY`
- `BLOCKED_SEGMENT_SLOT_REUSE_BEFORE_RELEASE`
- `BLOCKED_SEGMENT_READBACK_FAILED`
- `BLOCKED_SEGMENT_OUTPUT_NONFINITE`
- `BLOCKED_SEGMENT_OUTPUT_SHAPE_MISMATCH`
- `BLOCKED_SEGMENT_OUTPUT_PARITY_FAILED`
- `BLOCKED_SEGMENT_MATRIX_DIGEST_FAILED`

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_40_multi_row_block_matvec_segmented_dispatch_matrix -- `
  --slot-ring-receipt .\artifacts\ASH_BASETRAIN_GPU_39_ATLAS_UPLOAD_RING_BUFFER_SLOT_LEASE_RELEASE.json `
  --forward-candidate-receipt .\artifacts\ASH_BASETRAIN_GPU_38_SELECTED_GROUP_ROW_BLOCK_GPU_FORWARD_CANDIDATE.json `
  --reduction-parity-receipt .\artifacts\ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json `
  --multi-workgroup-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --parallel-reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37P_R1_SELECTED_GROUP_ROW_BLOCK_PARALLEL_REDUCTION_DIAGNOSTIC_KERNEL.json `
  --gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## Next Patch

`ASH-BASETRAIN-GPU-41` — Projection Segment Stitch Candidate / Multi Row-Block Output Assembly Review Gate / No Logits Adoption No Optimizer
