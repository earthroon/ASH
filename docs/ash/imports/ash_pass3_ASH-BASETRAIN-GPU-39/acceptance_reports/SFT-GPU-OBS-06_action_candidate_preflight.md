# SFT-GPU-OBS-06 Acceptance Report

## Scope
SFT-GPU-OBS-06 adds the Action Candidate Apply Gate Preflight / Reviewed Candidate Intake Seal on top of SFT-GPU-OBS-05.

The patch validates OBS-05 no-apply handoff candidates before any future apply gate can receive them. It does not apply candidate actions.

## Source
- source_operator_decision_action_candidate_handoff_seal_id: required
- source_action_candidate_digest: required
- source_handoff_packet_digest: required
- source_operator_review_receipt_intake_seal_id: required
- source_review_decision_digest: required
- source_review_item_digest: required
- previous_candidate_preflight_ledger_digest: required

## Candidate
- candidate_kind: validated against handoff packet snapshot
- target_adapter_id: validated against handoff packet snapshot
- target_slot_id: validated against handoff packet snapshot
- train_run_id: validated against handoff packet snapshot
- no_apply_confirmed: true required
- apply_performed: false required

## Preflight
- preflight_status: Passed | Held | Rejected | RequiresManualFollowup
- apply_gate_intake_allowed: computed; does not imply apply_performed
- requires_manual_followup: computed
- held: computed
- candidate_preflight_digest: generated deterministically
- preflight_ledger_event_digest: generated deterministically

## No-Apply Boundary
- no_apply_confirmed: true
- apply_performed: false
- current_pointer_update_performed: false
- fallback_activation_performed: false
- rollback_execution_performed: false
- demotion_apply_performed: false
- quarantine_apply_performed: false
- registry_mutation_performed: false
- lifecycle_mutation_performed: false

## Runtime Closed
- runtime_sft_training_performed: false
- runtime_gradient_write_performed: false
- runtime_optimizer_step_performed: false
- textureSample / sampler / normalized UV weight fetch remains closed

## Verification
Container-local Rust toolchain status:
- cargo: unavailable in this execution environment
- rustc: unavailable in this execution environment
- rustfmt: unavailable in this execution environment

Static checks performed:
- delimiter balance check for new Rust modules/tests
- lib.rs export wiring check for ash_core / lora_train / burn_webgpu_backend
- ZIP inclusion check for OBS-06 files

Local verification commands:
```bash
cargo test -p ash_core sft_gpu_obs_06 -- --nocapture
cargo test -p lora_train gpu_action_candidate_preflight -- --nocapture
cargo test -p burn_webgpu_backend gpu_action_candidate_preflight_signals -- --nocapture
cargo test -p ash_core sft_gpu_obs_05 -- --nocapture
cargo test -p ash_core sft_gpu_obs_04 -- --nocapture
cargo test -p ash_core sft_gpu_obs_03 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```
