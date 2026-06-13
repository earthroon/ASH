# ASH BaseTrain GPU Handoff After 17

## Current patch

ASH-BASETRAIN-GPU-17 — Chunk-Window Logits Expansion Output Audit / Window 2048 Dispatch State To Readback Boundary Verification No Backward No Optimizer Seal

## Source SSOT

ASH-BASETRAIN-GPU-16-R2, with aligned 2048 dispatch verdict:

PASS_ASH_BASETRAIN_GPU_16_CHUNK_WINDOW_LOGITS_EXPANSION_DISPATCH_SMOKE_WINDOW_2048_CANDIDATE_TO_DISPATCH_STATE_NO_BACKWARD_NO_OPTIMIZER

## 17 target

- Replays the 2048 dispatch path.
- Creates 8192-byte staging buffer.
- Copies logits output into staging.
- Executes map_async readback.
- Verifies readback byte length and element count.
- Performs finite scan and sample capture.
- Creates sha256 raw byte digest.

## Still closed

No full logits, generation, decode, loss, backward, optimizer, weight commit, safetensors mutation, or checkpoint finalization.

## Next if PASS

ASH-BASETRAIN-GPU-18 — Window 2048 Logits Readback Determinism Audit / Repeated Dispatch Readback Raw Digest Stability No Backward No Optimizer Seal
