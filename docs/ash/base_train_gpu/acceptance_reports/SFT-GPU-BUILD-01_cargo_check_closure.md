# SFT-GPU-BUILD-01 Acceptance Report

## Scope
- sherpa_rs_sys_excluded_from_main_gpu_sft_check: true
- check_command: cargo check -p ash_core -p lora_train -p burn_webgpu_backend
- full_workspace_check_claimed: false
- native_gpu_runtime_claimed: false

## HardNegative Replay SSOT
- canonical_buffer_type: crate::hard_negative_replay::AshHardNegativeReplayBuffer
- replay_buffer_ambiguity_removed: true
- files_disambiguated:
  - crates/ash_core/src/phase_hint_registry.rs
  - crates/ash_core/src/synapse_suppression.rs
  - crates/ash_core/src/hard_negative_replay_eval.rs
  - crates/ash_core/src/public_api.rs

## Import Closure
- ASH_30_AUDIT_STATUS imported: true
- assert_metric_resolution_order_invariant_for_report imported: true

## Config Field Drift
- require_runtime_model_fingerprint restored_or_mapped: restored on AshSftGpuRuntimeAttachDryRunConfig
- require_current_pointer_before restored_or_mapped: restored on AshSftGpuPromotionApplyCandidateConfig and AshSftGpuCurrentPointerSwitchConfig
- require_planned_current_pointer_after restored_or_mapped: restored on AshSftGpuPromotionApplyCandidateConfig and AshSftGpuCurrentPointerSwitchConfig
- require_current_pointer_after_match restored_or_mapped: restored on AshSftGpuCurrentPointerSwitchConfig
- guard_deletion_used_for_compile_closure: false

## Rust Closure
- borrow_contains_fixed: true
- candidate_version_shadowing_fixed: true
- collect_type_annotation_fixed: true
- confidence_multiplier_type_fixed: true
- decide_signature_drift_fixed: true
- timing_probe_device_fingerprint_field_drift_fixed: true
- moved_value_errors_fixed: true

## Verification
- cargo_available_in_bake_container: false
- rustc_available_in_bake_container: false
- rustfmt_available_in_bake_container: false
- static_delimiter_balance_checked: true
- stale_error_pattern_scan_performed: true

## Result
- check_passed: not_run_in_bake_container
- remaining_errors: unknown_until_local_cargo_check
- remaining_warnings: unknown_until_local_cargo_check
