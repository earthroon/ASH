# SFT-SLOT-03 — SFT Slot Training Command / Lease-Bound Run Intake

## Status
PASS_SFT_SLOT_TRAINING_COMMAND_LEASE_BOUND_RUN_INTAKE

## Scope
- Reads SFT-SLOT-01 slot registry report.
- Reads SFT-SLOT-02 lease guard report.
- Reads existing `AshSftTrainingCommandPlan`.
- Verifies active exclusive writer lease.
- Verifies command adapter id matches slot adapter id.
- Verifies command training manifest id matches slot training manifest id.
- Verifies command target modules match slot target modules fingerprint.
- Requires explicit training flag on command.
- Rejects already-started command.
- Creates lease-bound training command intake record.
- Creates lease-bound command envelope.
- Does not execute SFT training.
- Does not execute native dump.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not write training telemetry.
- Does not capture trained artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate registry.

## Files
- `crates/ash_core/src/sft_slot_training_command_intake.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_slot_03_training_command_lease_bound_intake.rs`

## Seal Flags
- `command_intake_accepted = true`
- `lease_bound_command_envelope_created = true`
- `active_lease_verified = true`
- `exclusive_writer_verified = true`
- `adapter_id_matched = true`
- `training_manifest_id_matched = true`
- `target_modules_matched = true`
- `sft_training_execution_allowed = false`
- `native_dump_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `training_telemetry_write_allowed = false`
- `trained_artifact_capture_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`
- `registry_mutation_allowed = false`

## Reproducibility
- `envelope_id` is deterministically derived from:
  - intake request id
  - slot id
  - lease id
  - command plan id
  - adapter id
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

- `intake_record_id` is deterministically derived from:
  - intake request id
  - slot id
  - lease id
  - command plan id
  - decision
  - optional envelope id
  - requested timestamp

## Result
SFT-SLOT-03 creates lease-bound SFT training command intake evidence only. SFT execution, native dump, gradient write, optimizer step, LoRA artifact write, telemetry write, trained artifact capture, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
