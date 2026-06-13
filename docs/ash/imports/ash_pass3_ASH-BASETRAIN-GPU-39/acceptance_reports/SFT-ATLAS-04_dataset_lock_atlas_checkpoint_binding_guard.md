# SFT-ATLAS-04 - Dataset Lock <-> Atlas Checkpoint Binding Guard

## Status
PASS_DATASET_LOCK_ATLAS_CHECKPOINT_BINDING_GUARD

## Scope
- Reads SFT-DATA-03 dataset atomic write receipt.
- Reads SFT-ATLAS-01 checkpoint receipt.
- Reads SFT-ATLAS-02 safetensors header audit seal.
- Verifies dataset_id match.
- Verifies dataset_lock_hash match.
- Verifies checkpoint source_write_receipt_id points to the dataset write receipt.
- Verifies checkpoint receipt and header audit seal refer to the same safetensors checkpoint.
- Verifies tensor index cross-verification passed.
- Treats `.safetensors` as Atlas checkpoint SSOT.
- Treats manifest as metadata only.
- Creates deterministic dataset-checkpoint binding evidence.
- Does not write or mutate safetensors.
- Does not execute native dump.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- crates/ash_core/src/sft_atlas_dataset_checkpoint_binding_guard.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_atlas_04_dataset_checkpoint_binding_guard.rs

## Seal Flags
- dataset_checkpoint_bound = true
- dataset_lock_checkpoint_cross_verified = true
- ssot_file_is_safetensors = true
- manifest_is_metadata_only = true
- safetensors_write_allowed = false
- safetensors_mutation_allowed = false
- native_dump_execution_allowed = false
- sft_training_execution_allowed = false
- gradient_write_allowed = false
- optimizer_step_allowed = false
- lora_artifact_write_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false

## Reproducibility
- binding_evidence_id is deterministically derived from:
  - binding guard request id
  - SFT-DATA-03 write receipt id
  - SFT-ATLAS-01 checkpoint receipt id
  - SFT-ATLAS-02 header audit seal id
  - dataset id
  - dataset lock hash
  - checkpoint id
  - checkpoint lock hash
  - tensor index id
  - safetensors sha256
  - decision
  - issue ids
  - created timestamp

## Result
SFT-ATLAS-04 binds dataset lock evidence to atlas safetensors checkpoint evidence. Safetensors write/mutation, native dump execution, SFT training, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
