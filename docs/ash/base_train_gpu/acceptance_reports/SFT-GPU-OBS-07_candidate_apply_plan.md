# SFT-GPU-OBS-07 Acceptance Report

## Source
- source_action_candidate_apply_gate_preflight_seal_id: required
- source_candidate_preflight_digest: required
- source_preflight_ledger_event_digest: required
- source_action_candidate_digest: required
- source_handoff_packet_digest: required
- previous_apply_plan_ledger_digest: required

## Candidate / Preflight
- candidate_kind: deterministic mapping source
- preflight_status: validated
- apply_gate_intake_allowed: validated as submit-only, not execution
- target_adapter_id: validated through candidate snapshot
- target_slot_id: validated through candidate snapshot
- train_run_id: validated through candidate snapshot

## Dry-run Plan
- plan_kind: deterministic candidate-kind mapping
- plan_created: true on accepted dry-run plan
- dry_run_only: true
- dry_run_transaction_plan_digest: generated deterministically
- apply_plan_ledger_event_digest: generated deterministically

## Planned Operation Summary
- would_update_current_pointer: recorded only as would_*
- would_activate_fallback: recorded only as would_*
- would_execute_rollback: recorded only as would_*
- would_apply_demotion: recorded only as would_*
- would_apply_quarantine: recorded only as would_*
- would_mutate_registry: recorded only as would_*
- would_mutate_lifecycle: recorded only as would_*

## No-Apply Confirmed
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
- textureSample / sampler / normalized UV weight fetch: closed

## Static Verification
- New Rust file delimiter balance: PASS
- ash_core export wiring: PASS
- lora_train export wiring: PASS
- burn_webgpu_backend export wiring: PASS
- ZIP required file inclusion: PASS after archive creation

## Verification Commands for Local Rust Toolchain
The execution container used for this bake does not provide cargo/rustc/rustfmt, so compile-time verification remains local-pending.

```bash
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
cargo test -p lora_train gpu_candidate_apply_plan -- --nocapture
cargo test -p burn_webgpu_backend gpu_candidate_apply_plan_signals -- --nocapture
cargo test -p ash_core sft_gpu_obs_06 -- --nocapture
cargo test -p ash_core sft_gpu_obs_05 -- --nocapture
cargo test -p ash_core sft_gpu_obs_04 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```
