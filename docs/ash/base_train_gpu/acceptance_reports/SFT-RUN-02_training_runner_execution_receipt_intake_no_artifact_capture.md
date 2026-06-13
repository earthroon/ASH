# SFT-RUN-02 — Training Runner Execution Receipt Intake / No Artifact Capture

## Status
PASS_TRAINING_RUNNER_EXECUTION_RECEIPT_INTAKE_NO_ARTIFACT_CAPTURE

## Scope
- Reads SFT-RUN-01 explicit training execution request envelope.
- Receives external runner execution receipt.
- Verifies source envelope, handoff record, slot id, lease id, and command plan id.
- Verifies runner id, runner kind, and runner command fingerprint.
- Verifies runner status, exit code policy, start/end timestamps, and log digest.
- Creates deterministic execution receipt seal.
- Creates deterministic execution receipt record.
- Accepts failed runner execution as failed receipt evidence without marking slot ready.
- Does not execute SFT training in core.
- Does not execute native dump in core.
- Does not write gradients in core.
- Does not run optimizer step in core.
- Does not write training telemetry.
- Does not capture trained artifact.
- Does not record output adapter digest.
- Does not record output manifest digest.
- Does not write LoRA artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate registry.

## Files
- crates/ash_core/src/sft_run_execution_receipt_intake.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_run_02_execution_receipt_intake.rs

## Seal Flags
- execution_receipt_intake_created = true
- execution_completed = true
- execution_succeeded = input-dependent
- execution_failed = input-dependent
- runner_identity_matched = true
- runner_command_fingerprint_matched = true
- log_path_matched = true
- artifact_capture_performed = false
- trained_artifact_capture_allowed = false
- output_adapter_digest_recorded = false
- output_manifest_digest_recorded = false
- sft_training_execution_performed_in_core = false
- native_dump_execution_performed_in_core = false
- gradient_write_performed_in_core = false
- optimizer_step_performed_in_core = false
- training_telemetry_write_allowed = false
- lora_artifact_write_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false
- registry_mutation_allowed = false

## Reproducibility
- execution_receipt_seal_id is deterministically derived from:
  - receipt request id
  - execution request envelope id
  - handoff record id
  - slot id
  - lease id
  - command plan id
  - runner id
  - runner kind
  - runner command fingerprint
  - runner execution id
  - runner status
  - process exit code
  - started timestamp
  - finished timestamp
  - duration
  - log path
  - log sha256
  - optional stdout/stderr digests

## Result
SFT-RUN-02 creates external runner execution receipt evidence only. Artifact capture, output adapter digest recording, output manifest digest recording, telemetry write, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
