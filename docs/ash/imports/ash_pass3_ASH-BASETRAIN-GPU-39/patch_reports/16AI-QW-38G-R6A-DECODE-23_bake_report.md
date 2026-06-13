# 16AI-QW-38G-R6A-DECODE-23 Bake Report

status: PASS_STATIC_REVIEW_QUEUE_ENQUEUE_COMMIT_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
base: ash_pass3_16AI-QW-38G-R6A-DECODE-22_human_review_approval_receipt_queue_enqueue_dry_run_seal_baked.zip

## Added modules
- crates/ash_core/src/review_queue_enqueue_policy.rs
- crates/ash_core/src/review_queue_entry.rs
- crates/ash_core/src/review_queue_mutation.rs
- crates/ash_core/src/review_queue_enqueue_receipt.rs
- crates/ash_core/src/review_queue_enqueue_stub.rs

## Mutated modules
- crates/ash_core/src/enko_decode_quality_receipt.rs
- crates/ash_core/src/lib.rs

## Boundary
Internal review queue ledger enqueue is allowed only for the approval-granted dry-run-passed fixture. External queue sink, reviewer assignment, ticket creation, notification, candidate commit/reject, rewrite/compression/retry, subtitle export, runtime decode, model forward, and sampling remain false.

## Canonical receipt keys
- approval_granted_enqueue: q4sha256:b2184adb6b74c61931efe9b6e5fcbe0eb5307676953fbaa9da8c80d07cc069fd
- approval_denied_block: q4sha256:8968704792cd508e44c49b1cceef5a07678078baebbe273c5a8e5ec4bb1e72fd
- approval_pending_block: q4sha256:a9d5a99ec5a9a426c68aa54a8ef3205c86347e2c2de3fdb25aa139f130ee9617
- missing_approval_dry_run_receipt: q4sha256:164610f6a28ea0d3db3acb94ecf27b54e316f630bac745e48c8fa80d0388bd23
- repair_required_block: q4sha256:fee2ca3290d57b43ac459577149f598cc15ec521fee4d1fccb3a1a88e50c5e82
- calibration_insufficient_block: q4sha256:8a7742fb03bcc9f50fd350887b6c10272fa5f4e6d7e91c2dafa54be9f6fc4727
- duplicate_queue_entry_idempotent: q4sha256:3dff4575cf7f43b80ffe7fece2119e504e3f1fe2e4fb0182894af2ee80f3da1b
- auto_accept_no_queue: q4sha256:6c8ecb371e163a15c0d8e073fccc7c1f937d7c7acb091b34d4cf8a283ff046de
