# SFT-GPU-8I-B all-step GPU redispatch loop

## Status
PASS_STATIC / PASS_ALL_STEP_GPU_REDISPATCH_LOOP

## Sealed
- per-step buffer clear
- all-group pass1 redispatch count gate
- per-step global CE reduce gate
- all-group pass2 redispatch count gate
- per-step AdamW update gate
- checkpoint / resume reports
- buffer hygiene trace

## Guards
- no stale partial CE
- no stale loss
- no stale grad
- no SGD fallback when optimizer=adamw
- no full logits
- no full lm_head.weight

## Next
SFT-GPU-8J quality eval / promotion gate
