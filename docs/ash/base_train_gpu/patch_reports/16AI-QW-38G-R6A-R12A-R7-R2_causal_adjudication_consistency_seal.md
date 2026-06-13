# 16AI-QW-38G-R6A-R12A-R7-R2 — Causal Adjudication Consistency Seal

## Status
STATIC_PASS_CAUSAL_ADJUDICATION_CONSISTENCY_SEAL_BAKED

## Purpose
R7-R2 does not rerun R7 interventions and does not alter R7 results. It reads R7/R6 artifacts and separates the decision axes:

- intervention axis: which intervention produced the largest margin drop
- source axis: which source-position candidate is better for R8 mask design
- value-direction axis: whether the value-direction hypothesis reached causal support

## Expected Source Alignment
- R7 source status: PASS_HEAD2_VALUE_VECTOR_CAUSAL_PROBE
- R7 source adjudication: POSITION55_VALUE_SOURCE_CAUSAL_CANDIDATE_SUPPORTED
- intervention-axis top: HEAD2_TARGET_DIRECTION_PROJECTION_REMOVAL
- source-axis target: POSITION55_RELATIVE_TO_POSITION20_SUPPORTED
- value-direction axis: OBSERVED_BUT_NOT_CAUSALLY_STRONG_ENOUGH

## R8 Decision
R8 target remains position55 source-token causal mask design because R8 is a source-position design patch, not a global projection-removal patch.

## Guard
- mutation_performed: false
- checkpoint_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false
