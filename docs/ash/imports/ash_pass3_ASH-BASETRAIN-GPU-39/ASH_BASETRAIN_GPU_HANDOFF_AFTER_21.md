# ASH BASETRAIN GPU HANDOFF AFTER 21

## Latest Patch

ASH-BASETRAIN-GPU-21

## Current SSOT

20 is the source SSOT. 21 introduces a guarded CPU local-window loss smoke that requires an explicit raw 2048-logits payload file.

## Important Boundary

Do not claim local-window loss PASS from digest/sample-only receipts. 21 must receive a full 8192-byte f32-le raw logits payload matching digest:

`856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052`

## Next Patch If 21 Passes

ASH-BASETRAIN-GPU-22 Loss Scalar Audit / Local Window Target 1 Loss Numeric Stability Receipt No Backward No Optimizer Seal

## Next Patch If Raw Payload Missing

ASH-BASETRAIN-GPU-21-0 Raw 2048 Logits Payload Export / Digest-Matched Source Materialization No Backward No Optimizer Seal
