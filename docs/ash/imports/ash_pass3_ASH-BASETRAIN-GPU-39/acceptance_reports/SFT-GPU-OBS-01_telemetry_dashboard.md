# SFT-GPU-OBS-01 Acceptance Report

## Patch

SFT-GPU-OBS-01 — Strict GPU Train Telemetry Dashboard / Matrix Drift Console Seal

## Source Seals

- source_strict_gpu_train_seal_id: required
- source_artifact_intake_seal_id: required
- source_regression_matrix_seal_id: required
- source_operator_action_apply_seal_id: required
- source_post_switch_health_seal_id: required
- source_rollback_drill_seal_id: required
- source_slot_arbitration_seal_id: required
- source_lifecycle_merge_seal_id: required
- source_fault_recovery_seal_id: required
- source_partial_artifact_quarantine_seal_id: required

## Telemetry Matrix

- telemetry_matrix_digest: deterministic digest over source snapshots + policy version
- loss_direction_milli: required metric
- adapter_delta_norm_milli: required metric
- cpu_fallback_risk_milli: required metric
- current_adapter_health_score_milli: required metric
- post_switch_smoke_failure_rate_milli: required metric
- save_reload_parity_passed: required metric projection
- fallback_ready: required metric projection
- rollback_available: required metric projection
- texture_load_guard_passed: optional projection, kept textureLoad-only
- partial_artifact_quarantine_count: required metric
- highest_severity: Ok | Watch | Warning | Critical | Held

## Dashboard Projection

- dashboard_projection_digest: deterministic digest over telemetry matrix + projection version + warning/critical keys
- drift_console_digest: deterministic digest over backend drift / CPU fallback risk / quarantine count projection
- operator_attention_required: derived from severity >= Warning or silent correction flags
- recommendation_visibility_only: true
- action_controls_enabled: false

## Closed Mutation Confirmed

- current_pointer_update_performed: false
- rollback_execution_performed: false
- demotion_apply_performed: false
- quarantine_apply_performed: false
- runtime_sft_training_performed: false
- runtime_gradient_write_performed: false
- runtime_optimizer_step_performed: false
- textureSample / sampler / normalized UV weight fetch: not opened

## Files Added

- crates/ash_core/src/sft_gpu_telemetry_dashboard.rs
- crates/ash_core/tests/sft_gpu_obs_01_telemetry_dashboard.rs
- crates/lora_train/src/gpu_train_telemetry_matrix.rs
- crates/lora_train/tests/gpu_train_telemetry_matrix.rs
- crates/burn_webgpu_backend/src/gpu_backend_telemetry.rs
- crates/burn_webgpu_backend/tests/gpu_backend_telemetry.rs

## Verification Intended

```bash
cargo test -p ash_core sft_gpu_obs_01 -- --nocapture
cargo test -p lora_train gpu_train_telemetry_matrix -- --nocapture
cargo test -p burn_webgpu_backend gpu_backend_telemetry -- --nocapture
cargo test -p ash_core sft_gpu_safety_02 -- --nocapture
cargo test -p ash_core sft_gpu_safety_01 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```

## Local Container Limitation

The current bake container does not provide cargo, rustc, or rustfmt. Static verification was performed instead and recorded in `acceptance_reports/SFT-GPU-OBS-01_static_verification.log`.
