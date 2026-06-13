# SFT-GPU-OBS-02 Acceptance Report

## Status

- status: `PASS_LONG_HORIZON_GPU_ADAPTER_HEALTH_LEDGER_SEAL`
- audit: `PASS_RUNTIME_DRIFT_LEDGER_APPEND_ONLY_NO_MUTATION_SEAL`
- cargo/rustc availability in this bake container: unavailable
- compile execution: not performed in this container

## Source

- source_telemetry_dashboard_seal_id: required
- source_telemetry_matrix_digest: required
- source_dashboard_projection_digest: required
- source_operator_action_apply_seal_id: required
- source_fault_recovery_seal_id: required
- source_partial_artifact_quarantine_seal_id: required
- previous_health_ledger_digest: required

## Adapter

- current_gpu_trained_adapter_id: required
- adapter_slot_id: required
- train_run_id: required

## Trend

- health_score_start_milli: computed from first ordered observation
- health_score_end_milli: computed from last ordered observation
- health_score_delta_milli: computed without auto-sorting observations
- smoke_failure_count: computed
- smoke_failure_rate_milli: computed
- fallback_readiness_flip_count: computed
- rollback_availability_flip_count: computed
- adapter_digest_drift_detected: computed, never corrected
- runtime_backend_drift_detected: computed, never corrected
- texture_load_guard_drift_detected: computed, never converted to textureSample fallback success
- fault_recovery_count_total: computed
- partial_artifact_quarantine_count_total: computed

## Ledger

- health_ledger_event_digest: deterministic digest
- health_trend_digest: deterministic digest
- runtime_drift_digest: deterministic digest
- long_horizon_gpu_adapter_health_ledger_seal_id: deterministic seal id
- append_only_confirmed: true on accepted reports

## Closed Mutation Confirmed

- current_pointer_update_performed: false
- rollback_execution_performed: false
- demotion_apply_performed: false
- quarantine_apply_performed: false
- registry_mutation_performed: false
- lifecycle_mutation_performed: false
- runtime_sft_training_performed: false
- runtime_gradient_write_performed: false
- runtime_optimizer_step_performed: false

## Verification Commands For Local Rust Environment

```bash
cargo test -p ash_core sft_gpu_obs_02 -- --nocapture
cargo test -p lora_train gpu_adapter_health_ledger -- --nocapture
cargo test -p burn_webgpu_backend gpu_runtime_drift_ledger -- --nocapture
cargo test -p ash_core sft_gpu_obs_01 -- --nocapture
cargo test -p ash_core sft_gpu_safety_02 -- --nocapture
cargo test -p ash_core sft_gpu_safety_01 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```

## Bake Notes

OBS-02 is an observation/ledger patch only. It appends long-horizon health and runtime drift evidence but does not apply recommendations, mutate registry state, write current pointers, execute rollback, apply demotion/quarantine, run SFT, write gradients, or step optimizers.
