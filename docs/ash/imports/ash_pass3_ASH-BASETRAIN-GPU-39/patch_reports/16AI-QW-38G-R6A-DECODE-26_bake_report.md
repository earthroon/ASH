# 16AI-QW-38G-R6A-DECODE-26 Bake Report

## Reviewer Assignment Commit / Approved Internal Assignment Ledger Seal

- base: ash_pass3_16AI-QW-38G-R6A-DECODE-25_reviewer_assignment_approval_receipt_assignment_dry_run_seal_baked.zip
- output: ash_pass3_16AI-QW-38G-R6A-DECODE-26_reviewer_assignment_commit_approved_internal_assignment_ledger_seal_baked.zip
- status: PASS_STATIC_REVIEWER_ASSIGNMENT_COMMIT_CONTRACT
- domain_ssot: en_to_ko_translation_subtitle_machine

## Scope

Added internal reviewer assignment ledger commit policy, mutation request snapshots, assignment entries, ledger snapshots, idempotent duplicate handling, and ReviewerAssignmentCommitReceipt fixtures.

## Mutation Boundary

- reviewer_assignment_executed may be true only for the approved internal ledger fixture.
- internal_assignment_ledger_mutation_executed may be true only for the approved internal ledger fixture.
- external reviewer assignment, reviewer lookup, availability check, ticket creation, notification, candidate commit, subtitle export, model forward, and sampling remain false.

## Counts

```json
{
  "assignment_blocked_approval_denied_count": 1,
  "assignment_blocked_approval_pending_count": 1,
  "assignment_blocked_capability_unavailable_count": 1,
  "assignment_committed_to_internal_ledger_count": 1,
  "assignment_not_required_auto_accept_count": 1,
  "assignment_skipped_duplicate_entry_count": 1,
  "availability_check_executed_count": 0,
  "candidate_commit_executed_count": 0,
  "candidate_reject_executed_count": 0,
  "compression_executed_count": 0,
  "deterministic_key_created_count": 8,
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "domain_ssot_mismatch_count": 0,
  "duplicate_assignment_entry_detected_count": 1,
  "duplicate_receipt_key_count": 0,
  "external_reviewer_assignment_executed_count": 0,
  "external_reviewer_lookup_executed_count": 0,
  "external_ticket_creation_executed_count": 0,
  "internal_assignment_ledger_mutation_executed_count": 1,
  "missing_assignment_candidate_receipt_skip_count": 1,
  "missing_assignment_dry_run_receipt_skip_count": 1,
  "model_forward_executed_count": 0,
  "notification_executed_count": 0,
  "retry_decode_executed_count": 0,
  "reviewer_assignment_commit_policy_created_count": 1,
  "reviewer_assignment_commit_receipt_created_count": 8,
  "reviewer_assignment_entry_created_count": 1,
  "reviewer_assignment_executed_count": 1,
  "rewrite_executed_count": 0,
  "runtime_decode_executed_count": 0,
  "sampling_executed_count": 0,
  "status": "PASS_STATIC_REVIEWER_ASSIGNMENT_COMMIT_CONTRACT",
  "subtitle_export_executed_count": 0
}
```
