# SFT-GPU-SAFETY-01 Acceptance Report

## Fault Source
- train_run_id: required
- adapter_slot_id: required
- adapter_candidate_id: required
- gpu_backend_fingerprint: required
- requested_backend: required
- actual_backend_at_fault: required

## Fault
- fault_kind: OutOfMemory | Timeout | DeviceLost | BackendLost | KernelDispatchFailed | TextureLoadGuardFailed | AdapterWriteFailed | UnknownGpuFault
- fault_stage: Preflight | DatasetLoad | ModelLoad | AdapterInit | ForwardPass | BackwardPass | OptimizerStep | AdapterSave | SaveReloadParity | RuntimeAttachDryRun | PostSwitchSmoke
- fault_message_digest: required

## CPU Fallback
- cpu_fallback_attempted: recorded as evidence only
- cpu_fallback_accepted: false

## Partial Artifact
- artifact_path: recorded
- artifact_digest: recorded
- zero_byte_detected: checked
- incomplete_manifest_detected: checked
- interrupted_optimizer_state_detected: checked
- failed_parity_detected: checked
- digest_mismatch_detected: checked
- incomplete_adapter_payload_detected: checked
- partial_artifact_quarantine_required: derived from scan

## Blocked Paths
- registry_intake_allowed: false
- promotion_allowed: false
- current_pointer_update_allowed: false

## Closed Runtime Mutation Confirmed
- runtime_sft_training_performed_after_fault: false
- runtime_gradient_write_performed_after_fault: false
- runtime_optimizer_step_performed_after_fault: false
- textureSample / sampler / normalized UV weight fetch: false

## Verification
- cargo test -p ash_core sft_gpu_safety_01 -- --nocapture
- cargo test -p lora_train gpu_train_failure_recovery -- --nocapture
- cargo test -p burn_webgpu_backend gpu_fault_recovery -- --nocapture

## Container Verification Note
`cargo` / `rustc` were not available in this execution container, so compilation tests were not executed here. Static file, export wiring, delimiter, and ZIP inclusion checks were performed instead.
