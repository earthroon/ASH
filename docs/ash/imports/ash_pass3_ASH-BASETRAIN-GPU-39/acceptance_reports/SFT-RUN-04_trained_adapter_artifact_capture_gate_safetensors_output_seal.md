# SFT-RUN-04 — Trained Adapter Artifact Capture Gate / Safetensors Output Seal

## Status
PASS_TRAINED_ADAPTER_ARTIFACT_CAPTURE_GATE_SAFETENSORS_OUTPUT_SEAL

## Scope
- Reads SFT-RUN-03 training telemetry receipt report.
- Requires complete successful telemetry receipt for normal artifact capture.
- Captures output adapter `.safetensors` digest evidence.
- Captures output adapter manifest `.json` digest evidence.
- Treats trained adapter `.safetensors` as artifact tensor SSOT.
- Treats output manifest as metadata only.
- Creates deterministic trained adapter artifact id.
- Creates `AshTrainedLoraAdapterArtifact` evidence using the existing ash_core artifact type.
- Creates deterministic artifact capture seal.
- Creates deterministic artifact capture record.
- Marks artifact as ready for outcome evaluation.
- Requires outcome evaluation.
- Requires promotion gate.
- Does not write artifact files.
- Does not persist artifact registry.
- Does not execute SFT training in core.
- Does not execute native dump in core.
- Does not write gradients in core.
- Does not run optimizer step in core.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not apply promotion.
- Does not update current pointer.
- Does not mutate registry.

## Files
- `crates/ash_core/src/sft_run_artifact_capture.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_run_04_trained_adapter_artifact_capture.rs`

## Seal Flags
- `trained_artifact_capture_performed = true`
- `output_adapter_digest_recorded = true`
- `output_manifest_digest_recorded = true`
- `trained_lora_artifact_created = true`
- `ready_for_outcome_evaluation = true`
- `requires_outcome_evaluation = true`
- `requires_promotion_gate = true`
- `lora_artifact_file_write_allowed = false`
- `artifact_persistent_write_allowed = false`
- `sft_training_execution_performed_in_core = false`
- `native_dump_execution_performed_in_core = false`
- `gradient_write_performed_in_core = false`
- `optimizer_step_performed_in_core = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`
- `registry_mutation_allowed = false`
- `promotion_apply_allowed = false`
- `current_pointer_update_allowed = false`

## Safetensors SSOT Contract
- Trained adapter tensor artifact must be `.safetensors`.
- `adapter_sha256` must be present.
- `adapter_size_bytes` must be greater than zero.
- `adapter_tensor_format` must equal `safetensors`.
- Output manifest must be `.json` and metadata only.
- Manifest digest is recorded, but manifest is not treated as tensor SSOT.

## Reproducibility
- `artifact_digest_evidence_id` is deterministically derived from:
  - adapter artifact path
  - adapter sha256
  - adapter size
  - adapter tensor format
  - adapter manifest path
  - manifest sha256
  - manifest size
  - manifest kind

- `trained_artifact_id` is deterministically derived from:
  - adapter id
  - source SFT plan id
  - source training manifest id
  - source dataset artifact id
  - source command plan id
  - adapter artifact path
  - adapter sha256
  - adapter manifest path
  - manifest sha256
  - sorted target modules
  - rank
  - alpha
  - training telemetry id

- `artifact_capture_seal_id` is deterministically derived from:
  - artifact capture request id
  - telemetry receipt seal id
  - telemetry receipt record id
  - execution receipt seal id
  - execution request envelope id
  - slot id
  - lease id
  - command plan id
  - adapter id
  - trained artifact id
  - adapter sha256
  - manifest sha256
  - artifact digest evidence id
  - reported timestamp

## Result
SFT-RUN-04 captures trained adapter artifact digest evidence only. Artifact file write, artifact persistence, slot readiness, ASH synapse binding, runtime attachment, promotion apply, current pointer update, and registry mutation remain sealed.
