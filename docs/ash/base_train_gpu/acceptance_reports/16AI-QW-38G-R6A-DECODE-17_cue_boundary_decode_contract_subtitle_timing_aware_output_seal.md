# 16AI-QW-38G-R6A-DECODE-17
## Cue Boundary Decode Contract / Subtitle Timing-Aware Output Seal

status: PASS_STATIC_CUE_BOUNDARY_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07
  - 16AI-QW-38G-R6A-DECODE-08
  - 16AI-QW-38G-R6A-DECODE-09
  - 16AI-QW-38G-R6A-DECODE-10
  - 16AI-QW-38G-R6A-DECODE-11
  - 16AI-QW-38G-R6A-DECODE-12
  - 16AI-QW-38G-R6A-DECODE-13
  - 16AI-QW-38G-R6A-DECODE-14
  - 16AI-QW-38G-R6A-DECODE-15
  - 16AI-QW-38G-R6A-DECODE-16

cue_boundary_policy_created_count: 1
cue_boundary_receipt_created_count: 7
deterministic_key_created_count: 7

pass_cue_boundary_contract_count: 1
review_required_count: 3
compression_recommended_count: 2
retry_decode_recommended_count: 1
missing_cue_timing_skip_count: 1

cps_soft_overflow_detected_count: 1
line_count_overflow_detected_count: 1
total_char_budget_overflow_detected_count: 1
short_cue_overflow_detected_count: 1
underfilled_candidate_detected_count: 1

candidate_reject_executed_count: 0
compression_executed_count: 0
line_reflow_executed_count: 0
retry_decode_executed_count: 0
rollback_executed_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
subtitle_export_executed_count: 0

decode10_surface_rerank_receipt_required: true
decode14_source_adequacy_receipt_required: true
decode15_glossary_receipt_required: true
decode16_tm_context_receipt_required: true
decode04_quality_score_cue_boundary_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0
