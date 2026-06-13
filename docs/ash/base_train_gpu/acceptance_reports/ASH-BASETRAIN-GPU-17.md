# ASH-BASETRAIN-GPU-17 Acceptance

## Patch

ASH-BASETRAIN-GPU-17 — Chunk-Window Logits Expansion Output Audit / Window 2048 Dispatch State To Readback Boundary Verification No Backward No Optimizer Seal

## Source SSOT

- Source patch: ASH-BASETRAIN-GPU-16-R2
- Source verdict: PASS_ASH_BASETRAIN_GPU_16_CHUNK_WINDOW_LOGITS_EXPANSION_DISPATCH_SMOKE_WINDOW_2048_CANDIDATE_TO_DISPATCH_STATE_NO_BACKWARD_NO_OPTIMIZER
- Source scope: fixed_token_embed_qproj_lmhead_window_2048_dispatch_smoke

## Acceptance target

- Runtime dispatch replay for readback: required
- Logits window size: 2048
- Logits output shape: [1, 1, 2048]
- Expected readback bytes: 8192
- Expected readback element count: 2048
- Staging buffer: MAP_READ | COPY_DST
- Raw byte digest: sha256 over raw_2048_logits_readback_bytes
- Repeated determinism: not claimed in 17

## Closed boundaries

- Full logits claim: false
- Generation/decode: false
- Loss/backward: false
- Optimizer/weight commit: false
- Safetensors mutation/checkpoint finalization: false

## Expected verdict

PASS_ASH_BASETRAIN_GPU_17_CHUNK_WINDOW_LOGITS_EXPANSION_OUTPUT_AUDIT_WINDOW_2048_DISPATCH_STATE_TO_READBACK_BOUNDARY_VERIFICATION_NO_BACKWARD_NO_OPTIMIZER
