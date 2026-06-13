# SFT-RUN-01 — Explicit Training Execution Runner Handoff / No Artifact Capture

## Status
PASS_EXPLICIT_TRAINING_EXECUTION_RUNNER_HANDOFF_NO_ARTIFACT_CAPTURE

## Scope
- Reads SFT-SLOT-04 run preflight report.
- Requires execution gate candidate.
- Verifies preflight passed.
- Verifies explicit training is required.
- Verifies command has not started.
- Verifies output adapter path is `.safetensors`.
- Verifies runner identity and runner command fingerprint.
- Creates explicit training execution request envelope for an external runner.
- Creates deterministic handoff record.
- Does not execute SFT training in core.
- Does not execute native dump in core.
- Does not write gradients in core.
- Does not run optimizer step in core.
- Does not write training telemetry.
- Does not capture trained artifact.
- Does not write LoRA artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate registry.

## Files
- crates/ash_core/src/sft_run_execution_handoff.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_run_01_execution_runner_handoff.rs

## Seal Flags
- runner_handoff_created = true
- external_runner_execution_request_created = true
- preflight_passed_verified = true
- explicit_training_verified = true
- command_not_started_verified = true
- output_safetensors_path_verified = true
- sft_training_execution_performed_in_core = false
- native_dump_execution_performed_in_core = false
- gradient_write_performed_in_core = false
- optimizer_step_performed_in_core = false
- training_telemetry_write_allowed = false
- trained_artifact_capture_allowed = false
- lora_artifact_write_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false
- registry_mutation_allowed = false

## Reproducibility
- execution_request_envelope_id is deterministically derived from:
  - handoff request id
  - execution gate candidate id
  - run preflight record id
  - slot id
  - lease id
  - command plan id
  - runner id
  - runner kind
  - runner command fingerprint
  - adapter id
  - backend kind
  - source training manifest id
  - source dataset artifact id
  - train jsonl path
  - dataset manifest path
  - output adapter path
  - output manifest path
  - target modules fingerprint
  - rank
  - alpha
  - epochs
  - batch size

- handoff_record_id is deterministically derived from:
  - handoff request id
  - execution gate candidate id
  - run preflight record id
  - slot id
  - lease id
  - command plan id
  - runner id
  - runner kind
  - runner command fingerprint
  - decision
  - execution request envelope id
  - requested timestamp

## Result
SFT-RUN-01 creates explicit training execution runner handoff evidence only. Core training execution, native dump, gradient write, optimizer step, telemetry write, trained artifact capture, LoRA artifact write, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
