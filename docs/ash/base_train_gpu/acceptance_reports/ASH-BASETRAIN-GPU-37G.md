# ASH-BASETRAIN-GPU-37G Acceptance Report

## Status

Static baked artifact status:

```txt
BLOCKED_37F_RECEIPT_NOT_FOUND
```

This blocked static receipt is expected inside the baked archive because the local 37F PASS receipt is intentionally not bundled. The operator must provide:

```powershell
--gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## PASS target

```txt
PASS_ASH_BASETRAIN_GPU_37G_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PROMOTION_GATE_VERIFIED_READBACK_BUFFER_TO_DISPATCH_CANDIDATE_NO_FORWARD_NO_BACKWARD
```

## SSOT

- Input SSOT: `ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`
- State owner: `crates/base_train`
- Stage: receipt-only dispatch promotion gate

## Reproducibility

Same 37F receipt and same `--candidate-workgroup-size-x` must produce the same dispatch candidate contract digests.

## Closed boundaries

- No source shard open
- No row-block re-read
- No F32 decode
- No GPU device request
- No GPU buffer creation
- No queue upload
- No readback
- No shader module
- No compute pipeline
- No bind group
- No dispatch
- No forward/backward/optimizer/mutation
