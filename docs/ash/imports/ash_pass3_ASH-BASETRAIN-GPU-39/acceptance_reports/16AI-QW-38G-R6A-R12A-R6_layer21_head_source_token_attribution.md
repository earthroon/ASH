# Acceptance — 16AI-QW-38G-R6A-R12A-R6 Layer21 Head Source Token Attribution

## Required Acceptance Criteria
- compile_pass: local execution required
- r12a_r6_env_gate_exists: true
- r12a_r6_default_off: true
- r12a_r5_source_loaded: checked by runner
- r12a_r5_status_pass: checked by runner
- r12a_r5_single_head_candidate_confirmed: checked by runner
- target_layer_confirmed: runner target layer = 21
- target_head_confirmed: source head candidate or default = 2
- prompt_token_map_written: true after run
- source_token_piece_map_written: true after run
- position20_probe_written: true after run
- position55_probe_written: true after run
- position20_token_resolved: required for PASS
- position55_token_resolved: required for PASS
- attention_prob_vs_value_contribution_split_written: true after run
- source_origin_candidate_written: true after run
- post_oproj_retention_written: true as projected-head contribution note
- root_cause_confirmed: false
- mutation_performed: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false

## Expected PASS Status
`PASS_LAYER21_HEAD_SOURCE_TOKEN_ATTRIBUTION`

## Failure Gates
- `FAIL_R5_RECEIPT_MISSING`
- `FAIL_R5_STATUS_NOT_PASS`
- `FAIL_R5_NOT_SINGLE_HEAD`
- `FAIL_R6_BUILD`
- `FAIL_R6_INFER_BINARY_NOT_FOUND`
- `FAIL_R6_INFER_RUN_FAILED`
- `FAIL_R6_HEAD_SOURCE_TRACE_MISSING`
- `FAIL_R6_NO_TARGET_HEAD_EVENT`
- `FAIL_SOURCE_TOKEN_MAP_INCOMPLETE`
- `FAIL_POSITION20_PROBE_MISSING`
- `FAIL_POSITION55_PROBE_MISSING`
