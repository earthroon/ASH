# ASH BaseTrain GPU Handoff After 16-R2

Current patch: ASH-BASETRAIN-GPU-16-R2

## SSOT

Use ASH-BASETRAIN-GPU-16-R2 as the label-aligned source for ASH-BASETRAIN-GPU-17 after local build/run passes.

## Confirmed intent

16-R2 aligns the ASH-BASETRAIN-GPU-16 PASS verdict string to the 2048 chunk-window dispatch smoke scope. It does not change shader, buffers, payload slices, dispatch grid, readback, loss, backward, optimizer, or mutation behavior.

## Next patch

ASH-BASETRAIN-GPU-17
Chunk-Window Logits Expansion Output Audit / Window 2048 Dispatch State To Readback Boundary Verification No Backward No Optimizer Seal
