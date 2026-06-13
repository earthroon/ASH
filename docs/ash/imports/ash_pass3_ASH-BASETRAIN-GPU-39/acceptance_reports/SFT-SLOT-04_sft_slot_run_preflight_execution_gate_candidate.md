# SFT-SLOT-04 — SFT Slot Run Preflight / Execution Gate Candidate

## Status
PASS_SFT_SLOT_RUN_PREFLIGHT_EXECUTION_GATE_CANDIDATE

## Scope
- Reads SFT-SLOT-03 lease-bound training command intake report.
- Verifies accepted lease-bound command envelope.
- Verifies command remains not started.
- Verifies explicit training is required.
- Verifies dataset, output, and log paths are safe.
- Requires output adapter path to be `.safetensors`.
- Verifies execution gate config is preflight-only and does not execute training.
- Creates deterministic SFT slot execution gate candidate.
- Creates deterministic run preflight record.
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
- crates/ash_core/src/sft_slot_run_preflight.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_slot_04_run_preflight_execution_gate_candidate.rs

## Seal Flags
- preflight_passed = true
- execution_gate_candidate_created = true
- active_lease_verified = true
- exclusive_writer_verified = true
- safe_paths_verified = true
- output_safetensors_path_verified = true
- gate_config_preflight_mode_verified = true
- sft_training_execution_allowed = false
- native_dump_execution_allowed = false
- gradient_write_allowed = false
- optimizer_step_allowed = false
- lora_artifact_write_allowed = false
- training_telemetry_write_allowed = false
- trained_artifact_capture_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false
- registry_mutation_allowed = false

## Reproducibility
- execution_gate_candidate_id is deterministically derived from run preflight request id, intake record id, envelope id, slot id, lease id, command plan id, adapter id, backend kind, source training manifest id, source dataset artifact id, train JSONL path, dataset manifest path, output adapter path, output manifest path, target modules fingerprint, rank, alpha, epochs, batch size, and gate config mode.

## Result
SFT-SLOT-04 creates SFT slot execution gate candidate evidence only. SFT execution, native dump, gradient write, optimizer step, LoRA artifact write, telemetry write, trained artifact capture, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
