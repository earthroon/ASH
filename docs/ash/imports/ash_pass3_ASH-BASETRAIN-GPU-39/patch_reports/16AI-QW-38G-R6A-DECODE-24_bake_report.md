# 16AI-QW-38G-R6A-DECODE-24 Bake Report

## Review Queue Assignment Candidate / No-Reviewer-Mutation Seal

status: PASS_STATIC_REVIEW_QUEUE_ASSIGNMENT_CANDIDATE_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine

Added Rust modules:
- crates/ash_core/src/review_queue_assignment_policy.rs
- crates/ash_core/src/reviewer_capability.rs
- crates/ash_core/src/review_queue_assignment_candidate.rs
- crates/ash_core/src/no_reviewer_mutation_gate.rs
- crates/ash_core/src/review_queue_assignment_receipt.rs
- crates/ash_core/src/review_queue_assignment_stub.rs

Updated Rust modules:
- crates/ash_core/src/lib.rs
- crates/ash_core/src/enko_decode_quality_receipt.rs

Execution boundary:
- assignment_candidate_created is allowed for 5 fixtures.
- reviewer_assignment_executed remains false for every fixture.
- external reviewer lookup, availability check, ticket creation, notification, candidate mutation, and subtitle export remain false.

Receipt count: 8
Deterministic keys: 8
Duplicate keys: 0
