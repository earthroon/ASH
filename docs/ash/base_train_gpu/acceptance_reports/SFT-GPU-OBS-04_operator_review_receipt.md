# SFT-GPU-OBS-04 Acceptance Report

## Source
- source_operator_health_review_queue_seal_id: required
- source_review_queue_digest: required
- source_console_projection_digest: required
- source_review_item_id: required
- source_review_item_digest: required
- previous_review_decision_ledger_digest: required

## Operator Receipt
- operator_review_receipt_id: required
- operator_review_receipt_digest: required
- operator_id_digest: required
- decision_kind: required
- decision_reason_digest: required

## Decision
- review_decision_digest: deterministic from queue item + operator receipt + decision kind
- decision_ledger_event_digest: deterministic from previous decision ledger digest + review decision digest
- decision_matches_review_item: true for accepted intake
- decision_requires_followup: true for recheck/rollback/fallback/demotion/quarantine/escalation/hold
- decision_escalates_priority: true only for explicit EscalateToBlocker on lower-priority items
- decision_downgrades_priority: false for accepted intake
- silent_priority_downgrade_detected: false for accepted intake

## Closed Mutation Confirmed
- action_apply_performed: false
- current_pointer_update_performed: false
- rollback_execution_performed: false
- demotion_apply_performed: false
- quarantine_apply_performed: false
- registry_mutation_performed: false
- lifecycle_mutation_performed: false
- runtime_sft_training_performed: false
- runtime_gradient_write_performed: false
- runtime_optimizer_step_performed: false

## Verification
- cargo test -p ash_core sft_gpu_obs_04 -- --nocapture
- cargo test -p lora_train gpu_health_review_receipt -- --nocapture
- cargo test -p burn_webgpu_backend gpu_health_review_decision_signals -- --nocapture

## Local container status
- cargo: not available in this execution container
- rustc: not available in this execution container
- rustfmt: not available in this execution container
- performed instead: delimiter balance check, export wiring check, required file inclusion check
