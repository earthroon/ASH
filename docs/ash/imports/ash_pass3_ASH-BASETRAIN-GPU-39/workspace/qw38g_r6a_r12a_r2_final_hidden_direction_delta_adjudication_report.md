# 16AI-QW-38G-R6A-R12A-R2 — Final Hidden Direction Delta Adjudication / Captured Vector Comparison Seal

## Status
PASS_FINAL_HIDDEN_DIRECTION_DELTA_ADJUDICATION

## Source
- source_patch: 16AI-QW-38G-R6A-R12A-R1
- source_status: PASS_FINAL_HIDDEN_TRACE_CAPTURE_EXPANSION
- capture_complete: true

## Vector Continuity
- pre_to_post_cosine: 0.8799803853034973
- pre_to_post_l2_delta: 40.54243087768555
- pre_to_post_norm_ratio: 1.8101799488067627
- post_to_projection_cosine: 1.0
- post_to_projection_l2_delta: 0.0
- post_to_projection_norm_ratio: 1.0

## Alignment Delta
- pre_target_cosine: 0.18791888654232025
- post_target_cosine: 0.16750815510749817
- projection_target_cosine: 0.16750815510749817
- pre_masked_cosine: 0.1708703488111496
- post_masked_cosine: 0.15948519110679626
- projection_masked_cosine: 0.15948519110679626
- pre_target_minus_masked_cosine_delta: 0.017048537731170654
- post_target_minus_masked_cosine_delta: 0.008022964000701904
- projection_target_minus_masked_cosine_delta: 0.008022964000701904
- pre_target_minus_masked_dot_delta: 1.3768844604492188
- post_target_minus_masked_dot_delta: 1.823871612548828
- projection_target_minus_masked_dot_delta: 1.823871612548828

## Candidate Results
- pre_final_hidden_direction_result: SUPPORTED
- final_norm_direction_amplification_result: NOT_SUPPORTED
- final_norm_norm_amplification_result: SUPPORTED_AS_MAGNIFIER
- projection_boundary_result: WEAK_OR_NOT_PRIMARY

## Adjudication
- adjudication: PRE_FINAL_HIDDEN_DIRECTION_WITH_FINAL_NORM_NORM_MAGNIFICATION
- root_cause_confirmed: false
- recommended_next_patch: 16AI-QW-38G-R6A-R12A-R3_LAYERWISE_HIDDEN_DIRECTION_BACKTRACE

## Guard
- mutation_performed: false
- lm_head_modified: false
- final_norm_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- ban_mask_modified: false
