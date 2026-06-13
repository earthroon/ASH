# ASH-BASETRAIN-GPU-20 Handoff

## Current state

ASH-BASETRAIN-GPU-20 creates a fixed target local-window loss candidate gate from ASH-BASETRAIN-GPU-19 readback stability promotion.

- target_token_id: 1
- target_source: fixed_smoke_token_id
- loss_window: [0, 2048]
- loss_candidate_scope: fixed_target_window_2048_local_logits_candidate
- full_vocab_loss_claimed: false
- loss_computed: false
- backward_executed: false
- optimizer_step_executed: false

## Next patch

ASH-BASETRAIN-GPU-21 — Local Window Loss Smoke / Fixed Target 1 Over Window 2048 Logits Candidate No Backward No Optimizer Seal
