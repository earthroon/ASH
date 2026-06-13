# 16AI-QW-38G-R6A-R12A-R12D — Static Validation Result

PASS_STATIC_VALIDATION

- runner_exists: true
- source_short_prefix_supported: true
- source_long_prefix_alias_supported: true
- policy_load_audit_written: true
- execution_loop_apply_audit_written: true
- negative_control_execution_block_audit_written: true
- prompt_variant_execution_apply_audit_written: true
- mutation_safety_audit_written: true
- negative_control_actual_apply_blocked_literal: true
- execution_loop_adjudication_literal: true
- pv001_block_expectation: true
- pv002_allow_expectation: true
- pv003_allow_expectation: true
- runtime_default_apply_false: true
- production_safe_confirmed_false: true
- root_cause_confirmed_false: true
- model_artifact_mutation_flags_false: true
- r13_auto_entry_absent_from_r12d_runner: true
- r12c_recommended_next_patch_corrected_to_r12d: true

- runtime_default_apply: false
- production_safe_confirmed: false
- root_cause_confirmed: false
- checkpoint_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false
