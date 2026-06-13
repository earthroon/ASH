# 16AI-QW-38G-R6A-DECODE-25 Bake Report

## Reviewer Assignment Approval Receipt / Assignment Dry-run Seal

- base: ash_pass3_16AI-QW-38G-R6A-DECODE-24_review_queue_assignment_candidate_no_reviewer_mutation_seal_baked.zip
- output: ash_pass3_16AI-QW-38G-R6A-DECODE-25_reviewer_assignment_approval_receipt_assignment_dry_run_seal_baked.zip
- status: PASS_STATIC_REVIEWER_ASSIGNMENT_APPROVAL_DRY_RUN_CONTRACT
- domain_ssot: en_to_ko_translation_subtitle_machine

## Scope

Added reviewer assignment approval request/receipt structures, static reviewer slot fixtures, reviewer slot match snapshots, assignment dry-run packets, and ReviewerAssignmentApprovalDryRunReceipt fixtures.

## Mutation Boundary

- assignment dry-run may pass: true
- would_assign_if_real_run may be true: true
- real_assignment_executed: false
- reviewer_assignment_executed: false
- external reviewer lookup: false
- availability check: false
- ticket/notification/export/model execution: false

## Counts

```json
{
  "assignment_approval_denied_count": 1,
  "assignment_approval_granted_count": 3,
  "assignment_approval_not_required_count": 1,
  "assignment_approval_pending_count": 1,
  "assignment_dry_run_blocked_approval_denied_count": 1,
  "assignment_dry_run_blocked_approval_pending_count": 1,
  "assignment_dry_run_blocked_capability_unavailable_count": 1,
  "assignment_dry_run_blocked_duplicate_assignment_count": 1,
  "assignment_dry_run_blocked_missing_assignment_candidate_receipt_count": 1,
  "assignment_dry_run_not_required_auto_accept_count": 1,
  "assignment_dry_run_passed_count": 2,
  "availability_check_executed_count": 0,
  "candidate_commit_executed_count": 0,
  "candidate_reject_executed_count": 0,
  "capability_match_passed_count": 2,
  "capability_unavailable_count": 1,
  "compression_executed_count": 0,
  "deterministic_key_created_count": 8,
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "domain_ssot_mismatch_count": 0,
  "duplicate_assignment_candidate_block_count": 1,
  "duplicate_receipt_key_count": 0,
  "external_reviewer_lookup_executed_count": 0,
  "external_ticket_creation_executed_count": 0,
  "missing_assignment_candidate_receipt_count": 1,
  "model_forward_executed_count": 0,
  "notification_executed_count": 0,
  "real_assignment_allowed_count": 0,
  "real_assignment_executed_count": 0,
  "retry_decode_executed_count": 0,
  "reviewer_assignment_approval_dry_run_receipt_created_count": 8,
  "reviewer_assignment_approval_policy_created_count": 1,
  "reviewer_assignment_executed_count": 0,
  "rewrite_executed_count": 0,
  "runtime_decode_executed_count": 0,
  "sampling_executed_count": 0,
  "static_reviewer_slots_fixture_created_count": 1,
  "status": "PASS_STATIC_REVIEWER_ASSIGNMENT_APPROVAL_DRY_RUN_CONTRACT",
  "subtitle_export_executed_count": 0,
  "would_assign_if_real_run_count": 2
}
```
