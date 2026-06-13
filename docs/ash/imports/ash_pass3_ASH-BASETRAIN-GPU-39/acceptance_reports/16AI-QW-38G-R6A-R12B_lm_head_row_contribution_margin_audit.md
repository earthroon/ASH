# 16AI-QW-38G-R6A-R12B — LM Head Row Contribution Margin Audit / Target Row vs Neighbor Rows Seal

## Status
PENDING_RUNTIME / PASS_LM_HEAD_ROW_CONTRIBUTION_AUDIT / PARTIAL_LM_HEAD_ROW_CONTRIBUTION_AUDIT_SOURCE_LIMITED

## SSOT
- previous patch: `16AI-QW-38G-R6A-R12`
- previous status required: `PASS_ROOT_CAUSE_SPLIT_PLAN`
- target row: `token_id=13 / <glossary:on>`
- masked replacement row: `token_id=373 / 이`
- root cause confirmed: `false`
- mutation performed: `false`

## Purpose
Audit whether `lm_head[13]` is itself an anomalous row, or whether the final hidden vector is merely aligned into that row at the projection boundary.

## Required Comparisons
- target row vs masked top1 row
- target row vs neighbor rows `12`, `14`
- target row vs normal Korean sample rows
- row norm anomaly vs contribution anomaly split

## Output Artifacts
- `workspace/qw38g_r6a_r12b_lm_head_row_contribution_trace.jsonl`
- `workspace/qw38g_r6a_r12b_lm_head_row_contribution_summary.json`
- `workspace/qw38g_r6a_r12b_lm_head_row_contribution_receipt.json`
- `workspace/qw38g_r6a_r12b_lm_head_row_contribution_report.md`
- `workspace/infer_qw38g_r6a_r12b_lm_head_row_contribution_live.log`

## Acceptance
- `compile_pass = true`
- `r12b_env_gate_exists = true`
- `r12b_default_off = true`
- `r12_source_loaded = true`
- `r10_r2_source_loaded = true`
- `lm_head_row_audit_loaded = true`
- `target_row_loaded = true`
- `masked_top1_row_loaded = true`
- `neighbor_rows_loaded = true`
- `target_vs_masked_margin_written = true`
- `target_vs_neighbor_margin_written = true`
- `target_vs_normal_korean_margin_written = true`
- `row_norm_anomaly_result_written = true`
- `row_contribution_anomaly_result_written = true`
- `root_cause_confirmed = false`
- `lm_head_row_axis_confidence_updated = true`
- `trace_jsonl_written = true`
- `summary_json_written = true`
- `receipt_json_written = true`
- `report_md_written = true`
- `mutation_performed = false`
- `safetensors_modified = false`
- `tokenizer_modified = false`

## Decision Branches
- `LM_HEAD_ROW_ALIGNMENT_OR_HIDDEN_DIRECTION_INTERACTION`
- `LM_HEAD_ROW_ANOMALY_CANDIDATE`
- `HIDDEN_DIRECTION_PRIMARY_CANDIDATE`
- `INSUFFICIENT_ROW_COMPARISON_EVIDENCE`
