# 16AI-QW-38G-R6A-R10-R2 — Multi-Seed Evidence Field Extraction Repair / Trace-backed Aggregation Seal

## Status
PENDING_RUNTIME / PASS_TRACE_BACKED_MULTI_SEED_AGGREGATION / PARTIAL_TRACE_BACKED_AGGREGATION_FIELD_LOSS / FAIL_TRACE_BACKED_AGGREGATION

## SSOT
- Source line: R10-R1 aggregation field loss
- Repair mode: `trace_backed_aggregation`
- Primary evidence: seed별 `qw38g_r6a_r11_seed_*_projection_margin_trace.jsonl`
- Secondary evidence: seed별 R11 summary/receipt
- No new inference: true
- Full vector readback: forbidden

## Required Evidence Fields
A seed is `VALID` only if these fields are present:

- `target_token_id`
- `target_piece`
- `raw_top1_token_id`
- `raw_top1_logit`
- `masked_top1_token_id`
- `masked_top1_logit`
- `target_minus_masked_top1_margin`
- `target_is_raw_top1`
- `ban_mask_displaced_target`
- `scalar_only`
- `full_vector_readback_used`
- `normal_path_guard_passed`
- `rollback_receipt_written`

## Seed Evidence
| seed | status | raw_top1 | masked_top1 | margin | displaced | missing_fields |
|---:|---|---:|---:|---:|---:|---|
| 42 | PENDING | | | | | |
| 43 | PENDING | | | | | |
| 44 | PENDING | | | | | |

## Aggregation
- valid_seed_count:
- partial_seed_count:
- invalid_seed_count:
- raw_top1_target_rate:
- ban_mask_displacement_rate:
- min_margin_vs_masked_top1:
- confidence_after_repair:
- repro_confidence_lifted:

## Field Integrity
- field_extraction_complete:
- field_loss_seed_count:
- warning_codes:

## Acceptance Criteria
- `repair_env_gate_exists = true`
- `r11_trace_is_primary_source = true`
- `partial_field_loss_classification_exists = true`
- `valid_seed_count_counts_only_complete_evidence = true`
- `confidence_lift_blocked_on_field_loss = true`
- `trace_jsonl_written = true`
- `summary_json_written = true`
- `receipt_json_written = true`
