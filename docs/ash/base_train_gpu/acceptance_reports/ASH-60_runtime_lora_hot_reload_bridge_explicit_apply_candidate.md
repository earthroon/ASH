# ASH-60 — Runtime LoRA Hot Reload Bridge / Explicit Apply Candidate

## Status
PASS_RUNTIME_LORA_HOT_RELOAD_BRIDGE_EXPLICIT_APPLY_CANDIDATE

## Scope
- Reads ASH-59 operator-reviewed synapse promotion report.
- Reads ASH-55 runtime LoRA re-entry bridge report.
- Reads ASH-56 native smoke artifact binding report.
- Reads ASH-58 LoRA synapse health ledger report.
- Validates promotion readiness, smoke evidence, health score, drift score, and artifact path consistency.
- Creates runtime LoRA hot reload explicit apply candidate.
- Creates ASH-48-compatible explicit apply candidate envelope.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not change current pointer.
- Does not create apply receipt.
- Does not mutate registry.
- Does not write LoRA artifact.
- Does not create rollback snapshot.

## Files
- crates/ash_core/src/runtime_lora_hot_reload_explicit_apply_candidate.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/ash_60_runtime_lora_hot_reload_explicit_apply_candidate.rs

## Seal Flags
- explicit_apply_candidate_created = true
- bridge_to_ash48_explicit_apply_gate_created = true
- ready_for_runtime_apply_candidate_gate = true
- runtime_attach_allowed = false
- explicit_apply_commit_allowed = false
- current_pointer_changed = false
- apply_receipt_allowed = false
- registry_mutation_allowed = false
- lora_artifact_write_allowed = false
- rollback_snapshot_create_allowed = false

## Reproducibility
- hot_reload_candidate_id is deterministically derived from:
  - hot reload candidate request id
  - ASH-59 promotion candidate id
  - ASH-55 re-entry candidate id
  - explicit apply request id
  - ASH-58 health snapshot id
  - ASH-58 health entry id
  - ASH-56 smoke plan id
  - ASH-53 ledger id
  - binding candidate id
  - schedule id
  - SFT run id
  - target adapter id
  - target artifact id
  - manifest path
  - weights path
  - creation timestamp

## Result
ASH-60 creates runtime LoRA hot reload explicit apply candidate evidence only. Runtime attachment, explicit apply commit, current pointer movement, apply receipt creation, registry mutation, LoRA artifact write, and rollback snapshot creation remain sealed.
