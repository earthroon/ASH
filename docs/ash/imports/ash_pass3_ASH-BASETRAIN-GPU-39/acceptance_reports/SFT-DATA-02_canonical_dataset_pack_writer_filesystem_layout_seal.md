# SFT-DATA-02 — Canonical Dataset Pack Writer / Filesystem Layout Seal

## Status
PASS_CANONICAL_DATASET_PACK_WRITER_FILESYSTEM_LAYOUT_SEAL

## Scope
- Reads SFT-DATA-01 canonical dataset pack evidence.
- Creates deterministic dataset pack filesystem layout.
- Creates deterministic dataset pack writer plan.
- Optionally binds an Atlas checkpoint `.safetensors` reference.
- Treats `.safetensors` as the Atlas checkpoint SSOT.
- Treats Atlas checkpoint manifest as metadata only.
- Creates Atlas checkpoint lock evidence when a safetensors reference is present.
- Does not write dataset files.
- Does not write safetensors checkpoints.
- Does not execute native dump.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- crates/ash_core/src/sft_dataset_pack_writer.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_data_02_dataset_pack_writer.rs

## Seal Flags
- dataset_pack_write_plan_created = true
- filesystem_layout_sealed = true
- atlas_checkpoint_safetensors_ssot_bound = true or false depending on input
- atlas_checkpoint_manifest_metadata_only = true when checkpoint ref is present
- dataset_pack_filesystem_write_allowed = false
- atlas_checkpoint_safetensors_write_allowed = false
- atlas_checkpoint_manifest_as_ssot_allowed = false
- sft_training_execution_allowed = false
- native_dump_execution_allowed = false
- gradient_write_allowed = false
- optimizer_step_allowed = false
- lora_artifact_write_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false

## Safetensors SSOT Contract
- Atlas checkpoint SSOT must be `.safetensors`.
- `safetensors_sha256` must be present.
- `safetensors_size_bytes` must be greater than zero.
- `tensor_format` must equal `safetensors`.
- `is_atlas_checkpoint_ssot` must be true.
- `manifest_is_metadata_only` must be true.
- Atlas checkpoint manifest must never be treated as checkpoint SSOT.

## Reproducibility
- `write_plan_id` is deterministically derived from:
  - writer request id
  - dataset id
  - dataset fingerprint
  - dataset lock hash
  - dataset root
  - optional atlas checkpoint id
  - optional atlas safetensors sha256

- `checkpoint_fingerprint` is deterministically derived from:
  - safetensors sha256
  - safetensors size
  - tensor format
  - tensor index hash
  - checkpoint kind

- `checkpoint_lock_hash` is deterministically derived from:
  - checkpoint id
  - checkpoint fingerprint
  - safetensors path
  - safetensors sha256
  - safetensors size
  - source dataset lock hash
  - created timestamp

## Result
SFT-DATA-02 creates canonical dataset pack writer and atlas safetensors checkpoint SSOT evidence only. Dataset file write, safetensors write, native dump execution, SFT training, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
