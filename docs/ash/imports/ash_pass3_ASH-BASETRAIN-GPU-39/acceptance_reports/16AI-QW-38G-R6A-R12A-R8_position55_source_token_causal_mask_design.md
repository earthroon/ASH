# Acceptance — 16AI-QW-38G-R6A-R12A-R8

- R8 env gate exists.
- R7-R2 receipt is required before execution.
- Target source position is fixed to 55 unless overridden by SSOT.
- Mask profiles include baseline, full scale 0, scale sweep, target-direction removal, and norm clip.
- Runner writes receipt, summary, report, scoreboard, safe candidate, and output stability matrix.
- No checkpoint/tokenizer/lm_head/final_norm/ban_mask mutation is performed.
