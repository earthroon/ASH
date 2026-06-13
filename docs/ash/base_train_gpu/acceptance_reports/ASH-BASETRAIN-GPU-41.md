# ASH-BASETRAIN-GPU-41 Acceptance Report

## Acceptance Target

41 passes only if a real 40 PASS segmented dispatch matrix receipt opens a projection stitch candidate, all segment outputs are validated as finite/parity-passed/released, the projection candidate is assembled with an explicit source map and digest, and the candidate is placed behind an evidence-only review gate without adoption.

## Expected Runtime Receipt

`artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json`

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

## Current Container Verification

- Static checks: PASS
- Cargo build: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- Runtime GPU: NOT_RUN_LOCAL_GPU_REQUIRED
- rustfmt: NOT_RUN_RUSTFMT_UNAVAILABLE_IN_CONTAINER
