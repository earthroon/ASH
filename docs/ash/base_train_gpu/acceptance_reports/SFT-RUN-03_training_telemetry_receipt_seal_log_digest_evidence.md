# SFT-RUN-03 — Training Telemetry Receipt Seal / Log Digest Evidence

## Status
PASS_TRAINING_TELEMETRY_RECEIPT_SEAL_LOG_DIGEST_EVIDENCE

## Scope
- Reads SFT-RUN-02 execution receipt intake report.
- Reads existing `AshSftTrainingRunTelemetry` evidence.
- Verifies source execution receipt seal, record, envelope, slot, lease, command, and runner execution id.
- Verifies telemetry command plan id matches execution receipt command plan id.
- Verifies telemetry start/end/duration evidence against execution receipt.
- Verifies backend exit code against execution receipt.
- Verifies log path and log digest evidence.
- Verifies metrics digest evidence for successful runs.
- Accepts partial telemetry for failed runner execution without marking slot ready.
- Creates deterministic training telemetry receipt seal.
- Creates deterministic training telemetry receipt record.
- Does not persist telemetry.
- Does not capture trained artifact.
- Does not record output adapter digest.
- Does not record output manifest digest.
- Does not record trained artifact id.
- Does not write LoRA artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate registry.

## Files
- `crates/ash_core/src/sft_run_telemetry_receipt.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_run_03_training_telemetry_receipt.rs`

## Seal Flags
- `telemetry_receipt_intake_created = true`
- `telemetry_complete = input-dependent`
- `telemetry_partial = input-dependent`
- `execution_receipt_matched = true`
- `telemetry_command_matched = true`
- `telemetry_time_matched = true`
- `telemetry_exit_code_matched = true`
- `log_digest_matched = true`
- `artifact_capture_performed = false`
- `output_adapter_digest_recorded = false`
- `output_manifest_digest_recorded = false`
- `trained_artifact_id_recorded = false`
- `training_telemetry_persistent_write_allowed = false`
- `sft_training_execution_performed_in_core = false`
- `native_dump_execution_performed_in_core = false`
- `gradient_write_performed_in_core = false`
- `optimizer_step_performed_in_core = false`
- `trained_artifact_capture_allowed = false`
- `lora_artifact_write_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`
- `registry_mutation_allowed = false`

## Reproducibility
`telemetry_receipt_seal_id` is deterministically derived from:
- telemetry receipt request id
- execution receipt seal id
- execution receipt record id
- execution request envelope id
- slot id
- lease id
- command plan id
- runner execution id
- telemetry id
- start/end/duration timestamps
- train and holdout record counts
- final loss
- best eval loss
- step count
- backend exit code
- log digest
- optional metrics/event/step/loss curve digests

## Result
SFT-RUN-03 creates training telemetry receipt and log digest evidence only. Telemetry persistence, trained artifact capture, output adapter digest recording, output manifest digest recording, LoRA artifact write, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
