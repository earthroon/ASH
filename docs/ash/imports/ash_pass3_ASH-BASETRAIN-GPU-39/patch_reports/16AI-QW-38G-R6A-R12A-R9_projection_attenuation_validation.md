# 16AI-QW-38G-R6A-R12A-R9 — Projection Attenuation Validation

## Status
BAKED_STATIC

## Scope
- Validate the R8A safe candidate `HEAD2_TARGET_DIRECTION_ORTHOGONAL_ONLY`.
- Reuse the existing R8A diagnostic projection trace path for repeated baseline/candidate measurements.
- Keep the attenuation diagnostic-only and do not apply it to default runtime.

## Added
- `scripts/run_16AI_QW_38G_R6A_R12A_R9_projection_attenuation_validation.ps1`
- R9 env-gate markers in `crates/model_core/src/native_wgpu.rs`

## Output Artifacts
- `workspace/qw38g_r6a_r12a_r9_projection_attenuation_validation_trace.jsonl`
- `workspace/qw38g_r6a_r12a_r9_projection_attenuation_validation_summary.json`
- `workspace/qw38g_r6a_r12a_r9_projection_attenuation_validation_receipt.json`
- `workspace/qw38g_r6a_r12a_r9_repeat_validation_matrix.json`
- `workspace/qw38g_r6a_r12a_r9_prompt_variant_validation_matrix.json`
- `workspace/qw38g_r6a_r12a_r9_negative_control_matrix.json`
- `workspace/qw38g_r6a_r12a_r9_output_stability_validation.json`
- `workspace/qw38g_r6a_r12a_r9_margin_reduction_validation.json`
- `workspace/qw38g_r6a_r12a_r9_validation_decision.json`

## Guard
- checkpoint_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false
- runtime_default_apply: false
