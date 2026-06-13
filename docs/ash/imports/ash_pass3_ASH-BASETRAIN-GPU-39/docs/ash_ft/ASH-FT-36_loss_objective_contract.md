# ASH-FT-36 Loss Objective Contract / Subtitle Causal LM Target Seal

## SSOT

ASH-FT-36 consumes the ASH-FT-35 sequence pack manifest and field boundary map as read-only inputs and creates the loss-objective SSOT for the training mainline.

## Scope

Allowed:
- Finalize objective kind as `subtitle_causal_lm`.
- Finalize label policy as `shifted_next_token`.
- Finalize `ignore_index`.
- Finalize raw-text, pair, and instruction loss mask policy.
- Declare source/target/response/padding/invalid token weights.
- Create domain and sample weight policies.
- Create loss contract manifest.

Forbidden:
- Model forward.
- Real loss computation.
- Backward.
- Training.
- Optimizer step.
- Weight update.
- Tokenizer, corpus, sequence pack mutation.
- Shadow route, delta packet, runtime apply, alias rebind, promotion.

## Default objective

`subtitle_causal_lm` with target-only pair loss:

- raw text: all non-padding tokens are trainable.
- translation/subtitle pair: source/context tokens are ignored, target tokens are trainable.
- instruction pair: instruction/input tokens are ignored, response tokens are trainable.

## Expected verdict

`PASS_ASH_FT36_LOSS_OBJECTIVE_CONTRACT_SUBTITLE_CAUSAL_LM_TARGET`

## Next

ASH-FT-37 — Atlas Group Train Run Plan / Schedule To Trainable Scope Seal.
