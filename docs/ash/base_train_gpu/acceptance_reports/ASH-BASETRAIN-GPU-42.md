# ASH-BASETRAIN-GPU-42 Acceptance Report

## Acceptance Target

42 passes only if a real 41 PASS projection stitch review gate receipt opens an explicit operator approval gate, the approval token or approval receipt is valid, the projection candidate digest and source map are preserved, and an approved projection candidate receipt is written without treating it as logits or model output.

## Expected Runtime Receipt

`artifacts/ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json`

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

## Missing Approval Negative Test

Run without `--operator-approval-token` or `--operator-approval-receipt`; expected blocker:

`BLOCKED_OPERATOR_APPROVAL_MISSING`

## Current Container Verification

- Static checks: PASS
- Cargo build: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- Runtime GPU: NOT_RUN_LOCAL_GPU_REQUIRED
- rustfmt: NOT_RUN_RUSTFMT_UNAVAILABLE_IN_CONTAINER
