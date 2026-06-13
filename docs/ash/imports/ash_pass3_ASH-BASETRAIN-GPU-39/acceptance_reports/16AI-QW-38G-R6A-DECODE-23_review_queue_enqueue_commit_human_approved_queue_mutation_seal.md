# 16AI-QW-38G-R6A-DECODE-23
## Review Queue Enqueue Commit / Human-Approved Queue Mutation Seal

status: PASS_STATIC_REVIEW_QUEUE_ENQUEUE_COMMIT_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-18
  - 16AI-QW-38G-R6A-DECODE-19
  - 16AI-QW-38G-R6A-DECODE-20
  - 16AI-QW-38G-R6A-DECODE-21
  - 16AI-QW-38G-R6A-DECODE-22

review_queue_enqueue_policy_created_count: 1
review_queue_enqueue_commit_receipt_created_count: 8
deterministic_key_created_count: 8

enqueue_committed_to_internal_ledger_count: 1
enqueue_skipped_duplicate_queue_entry_count: 1
enqueue_blocked_approval_denied_count: 1
enqueue_blocked_approval_pending_count: 1
enqueue_blocked_repair_required_count: 1
enqueue_blocked_calibration_insufficient_count: 1
enqueue_not_required_auto_accept_count: 1
missing_approval_dry_run_receipt_skip_count: 1

queue_entry_created_count: 1
queue_enqueue_executed_count: 1
internal_ledger_mutation_executed_count: 1
external_queue_sink_executed_count: 0

duplicate_queue_entry_detected_count: 1

reviewer_assignment_executed_count: 0
external_ticket_creation_executed_count: 0
notification_executed_count: 0

candidate_commit_executed_count: 0
candidate_reject_executed_count: 0
rewrite_executed_count: 0
compression_executed_count: 0
retry_decode_executed_count: 0
subtitle_export_executed_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0

decode22_human_review_approval_dry_run_receipt_required: true
decode21_human_review_queue_candidate_receipt_required: true
decode20_score_threshold_calibration_receipt_required: true
decode19_final_quality_score_receipt_required: true
decode18_final_commit_receipt_required: true
decode04_quality_score_review_queue_enqueue_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0
