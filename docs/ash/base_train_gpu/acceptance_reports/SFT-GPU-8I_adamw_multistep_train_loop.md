# SFT-GPU-8I AdamW / multi-step train loop

## Status
PASS_STATIC / PASS_ADAMW_MULTISTEP_TRAIN_LOOP

## Sealed
- AdamW optimizer config/state snapshot
- multi-step train loop report
- checkpoint / resume contract
- loss trace
- runtime delta eval interval reference
- final adapter paths preserved from 8H-G export

## Guards
- optimizer must be `adamw`
- loss finite
- update delta positive inherited from 8H-G seal
- checkpoint target_key consistency
- no logits readback
- no full lm_head.weight buffer

## Note
8I seals the multi-step control/checkpoint SSOT from the 8H-G train-step output. Full repeated GPU redispatch can be promoted in 8I-B after this loop contract compiles.

## Next
SFT-GPU-8J quality eval / promotion gate
