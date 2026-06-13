# ASH-61 — Explicit Apply Gate Preflight / Runtime Orchestrator Handoff

## Status
PASS_EXPLICIT_APPLY_GATE_PREFLIGHT_RUNTIME_ORCHESTRATOR_HANDOFF

## Scope
- Reads ASH-60 runtime LoRA hot reload explicit apply candidate report.
- Validates ASH-48-compatible explicit apply candidate envelope.
- Validates source id and target artifact path consistency.
- Creates deterministic explicit apply gate preflight checklist.
- Creates deterministic runtime orchestrator handoff bundle.
- Does not call ASH-48 explicit apply gate.
- Does not execute runtime orchestrator.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not change current pointer.
- Does not create apply receipt.
- Does not mutate registry.
- Does not write LoRA artifact.
- Does not create rollback snapshot.

## Files
- `crates/ash_core/src/explicit_apply_gate_preflight_orchestrator_handoff.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_61_explicit_apply_gate_preflight_orchestrator_handoff.rs`

## Seal Flags
- `explicit_apply_gate_preflight_created = true`
- `runtime_orchestrator_handoff_candidate_created = true`
- `ash48_gate_call_allowed = false`
- `runtime_orchestrator_execution_allowed = false`
- `runtime_attach_allowed = false`
- `explicit_apply_commit_allowed = false`
- `current_pointer_changed = false`
- `apply_receipt_allowed = false`
- `registry_mutation_allowed = false`
- `lora_artifact_write_allowed = false`
- `rollback_snapshot_create_allowed = false`

## Reproducibility
- `checklist_id` is deterministically derived from:
  - handoff request id
  - ASH-60 hot reload candidate id
  - explicit apply request id
  - target adapter id
  - target artifact id
  - manifest path
  - weights path

- `handoff_bundle_id` is deterministically derived from:
  - handoff request id
  - ASH-60 candidate/envelope ids
  - ASH-59 promotion candidate id
  - ASH-58 health snapshot id
  - ASH-56 smoke plan id
  - ASH-53 ledger id
  - target artifact identity
  - creation timestamp

- `explicit_apply_request_fingerprint` and `orchestrator_payload_fingerprint` are deterministic and do not include random material.

## Result
ASH-61 creates explicit apply gate preflight and runtime orchestrator handoff evidence only. ASH-48 gate call, runtime orchestrator execution, runtime attachment, explicit apply commit, current pointer movement, apply receipt creation, registry mutation, LoRA artifact write, and rollback snapshot creation remain sealed.
