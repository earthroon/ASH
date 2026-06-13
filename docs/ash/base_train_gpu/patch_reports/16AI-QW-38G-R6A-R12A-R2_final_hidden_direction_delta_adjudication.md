# 16AI-QW-38G-R6A-R12A-R2 — Final Hidden Direction Delta Adjudication / Captured Vector Comparison Seal

## Patch Scope
R12A-R2 does not add new hidden capture hooks and does not mutate model state. It reads R12A-R1 pre/post/projection vector evidence and writes an adjudication scoreboard.

## Implemented
- Added `scripts/run_16AI_QW_38G_R6A_R12A_R2_final_hidden_direction_delta_adjudication.ps1`.
- Added R2 summary, receipt, trace, report, and candidate scoreboard artifacts.
- Preserved tokenizer/safetensors/lm_head/final_norm/ban-mask guard as mutation-free.

## Static Baked Adjudication
- pre_final_hidden_direction_result: SUPPORTED
- final_norm_direction_amplification_result: NOT_SUPPORTED
- final_norm_norm_amplification_result: SUPPORTED_AS_MAGNIFIER
- projection_boundary_result: WEAK_OR_NOT_PRIMARY
- adjudication: PRE_FINAL_HIDDEN_DIRECTION_WITH_FINAL_NORM_NORM_MAGNIFICATION
- recommended_next_patch: 16AI-QW-38G-R6A-R12A-R3_LAYERWISE_HIDDEN_DIRECTION_BACKTRACE
