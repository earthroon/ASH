# ASH-BASETRAIN-GPU-21 Acceptance Report

## Status

Baked as a guarded local-window loss smoke implementation.

## SSOT

- Source SSOT: ASH-BASETRAIN-GPU-20 fixed target loss candidate gate PASS result.
- State owner: ASH-BASETRAIN-GPU-21 local window loss smoke receipt.
- Reproducibility: conditional; requires explicit raw logits payload file.

## Boundary

- Opens CPU local-window logsumexp and NLL scalar only when `ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH` points to an 8192-byte f32-le payload matching the ASH-BASETRAIN-GPU-18 digest.
- Does not open new WGPU device, dispatch, queue submit, readback, full-vocab loss, backward, optimizer, mutation, or checkpoint finalization.

## Expected PASS Verdict

`PASS_ASH_BASETRAIN_GPU_21_LOCAL_WINDOW_LOSS_SMOKE_FIXED_TARGET_1_OVER_WINDOW_2048_LOGITS_CANDIDATE_NO_BACKWARD_NO_OPTIMIZER`

## Blocker Behavior

If raw payload is absent, the bundle must not fabricate loss. It emits a nonzero violation mask and routes to `ASH-BASETRAIN-GPU-21-0_RAW_LOGITS_PAYLOAD_EXPORT` or `ASH-BASETRAIN-GPU-21A` triage.
