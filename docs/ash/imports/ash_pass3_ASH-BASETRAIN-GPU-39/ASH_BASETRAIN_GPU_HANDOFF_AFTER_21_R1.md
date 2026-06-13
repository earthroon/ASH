# ASH BaseTrain GPU Handoff After 21-R1

## Current SSOT

ASH-BASETRAIN-GPU-21-R1 route rebind source is baked.

## Original 21 State

ASH-BASETRAIN-GPU-21 remains a valid failure:

- pass = false
- verdict = FAIL_ASH_BASETRAIN_GPU_21_COMPOSITE_BLOCKER_MASK_52
- raw logits payload missing
- local logits unavailable
- loss scalar not created

## 21-R1 State

ASH-BASETRAIN-GPU-21-R1 only corrects the failure route:

- mask 52 active bits = [2, 4, 5]
- primary blocker bit = 2
- corrected route = ASH-BASETRAIN-GPU-21-0_RAW_LOGITS_PAYLOAD_EXPORT
- no loss
- no raw payload export
- no backward
- no optimizer

## Next Patch

ASH-BASETRAIN-GPU-21-0
Raw Logits Payload Export /
Window 2048 Readback Bytes Materialization For Local Loss Smoke No Loss No Backward No Optimizer Seal
