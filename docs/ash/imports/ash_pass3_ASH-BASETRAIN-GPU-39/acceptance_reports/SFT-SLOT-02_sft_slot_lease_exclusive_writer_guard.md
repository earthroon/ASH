# SFT-SLOT-02 — SFT Slot Lease / Exclusive Writer Guard

## Status
PASS_SFT_SLOT_LEASE_EXCLUSIVE_WRITER_GUARD

## Scope
- Reads SFT-SLOT-01 slot registry report.
- Requires deterministic slot id contract.
- Requires dataset-checkpoint bound slot.
- Requires ready_for_training_plan slot state.
- Creates exclusive writer lease evidence.
- Creates lease ledger snapshot evidence.
- Rejects active conflicting lease.
- Treats expired lease as non-conflicting.
- Does not persist lease ledger.
- Does not execute SFT training.
- Does not execute native dump.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.
- Does not mutate registry.

## Files
- crates/ash_core/src/sft_slot_lease_guard.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/sft_slot_02_lease_exclusive_writer_guard.rs

## Seal Flags
- lease_grant_created = true
- exclusive_writer_guard_created = true
- lease_conflict_detected = false
- lease_persistent_write_allowed = false
- sft_training_execution_allowed = false
- native_dump_execution_allowed = false
- gradient_write_allowed = false
- optimizer_step_allowed = false
- lora_artifact_write_allowed = false
- sft_slot_ready_allowed = false
- synapse_binding_allowed = false
- runtime_attach_allowed = false
- registry_mutation_allowed = false

## Reproducibility
- lease_id is deterministically derived from:
  - lease request id
  - slot id
  - source slot registry snapshot id
  - lease owner id
  - lease owner kind
  - lease granted timestamp
  - lease expiry timestamp
  - slot dataset lock hash
  - slot checkpoint lock hash
  - slot tensor index hash
  - slot binding evidence id

## Result
SFT-SLOT-02 creates exclusive writer lease evidence only. Lease persistence, SFT execution, native dump, gradient write, optimizer step, LoRA artifact write, slot readiness, ASH synapse binding, runtime attachment, and registry mutation remain sealed.
