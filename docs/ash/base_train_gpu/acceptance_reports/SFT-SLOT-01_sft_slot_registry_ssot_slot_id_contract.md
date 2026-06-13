# SFT-SLOT-01 — SFT Slot Registry SSOT / SlotId Contract

## Status
PASS_SFT_SLOT_REGISTRY_SSOT_SLOT_ID_CONTRACT

## Scope
- Reads SFT-ATLAS-04 dataset-checkpoint binding guard report.
- Requires Bound dataset-checkpoint binding evidence.
- Creates deterministic SFT slot key.
- Creates deterministic SFT slot id.
- Creates SFT slot registry snapshot.
- Binds dataset lock hash, checkpoint lock hash, tensor index hash, adapter id, config fingerprint, target modules fingerprint, and training manifest id into one slot record.
- Detects slot id collision.
- Detects stale slot insertion.
- Preserves idempotent rebuild when the same slot id and same slot key already exist.
- Does not execute SFT training.
- Does not execute native dump.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not grant training lease.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate persistent registry.

## Files
- crates/ash_core/src/sft_slot_registry.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_slot_01_registry_ssot.rs

## Seal Flags
- slot_registry_created = true
- slot_id_contract_sealed = true
- deterministic_slot_id_created = true
- dataset_checkpoint_bound = true
- dataset_lock_checkpoint_cross_verified = true
- ready_for_training_plan = true
- training_lease_required = true
- ready_for_synapse_preflight = false
- sft_training_execution_allowed = false
- native_dump_execution_allowed = false
- gradient_write_allowed = false
- optimizer_step_allowed = false
- lora_artifact_write_allowed = false
- training_lease_grant_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false
- registry_mutation_allowed = false

## Reproducibility
- target_modules_fingerprint is deterministically derived from sorted target modules.
- slot_id is deterministically derived from:
  - adapter id
  - dataset id
  - dataset fingerprint
  - dataset lock hash
  - checkpoint id
  - checkpoint fingerprint
  - checkpoint lock hash
  - tensor index id
  - tensor index hash
  - binding evidence id
  - config fingerprint
  - target modules fingerprint
  - training manifest id

## Result
SFT-SLOT-01 creates SFT slot registry SSOT only. Training execution, native dump, gradient write, optimizer step, LoRA artifact write, training lease grant, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
