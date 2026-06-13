# 16AI-QW-38G-R6A-DECODE-22 Bake Report

status: PASS_STATIC_HUMAN_REVIEW_APPROVAL_DRY_RUN_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
base: ash_pass3_16AI-QW-38G-R6A-DECODE-21_human_review_queue_candidate_no_enqueue_approval_gate_seal_baked.zip

## Added Rust modules
- crates/ash_core/src/human_review_approval_policy.rs
- crates/ash_core/src/human_review_approval_request.rs
- crates/ash_core/src/human_review_approval_receipt.rs
- crates/ash_core/src/queue_enqueue_dry_run.rs
- crates/ash_core/src/human_review_approval_dry_run_receipt.rs
- crates/ash_core/src/human_review_approval_dry_run_stub.rs

## Modified Rust modules
- crates/ash_core/src/enko_decode_quality_receipt.rs
- crates/ash_core/src/lib.rs

## Execution boundary
- real_enqueue_executed: false
- queue_enqueue_executed: false
- reviewer_assignment_executed: false
- external_ticket_creation_executed: false
- notification_executed: false
- candidate_commit_executed: false
- subtitle_export_executed: false
- model_forward_executed: false
- sampling_executed: false

## Receipt count
- human_review_approval_dry_run_receipt_created_count: 8
- deterministic_key_created_count: 8
