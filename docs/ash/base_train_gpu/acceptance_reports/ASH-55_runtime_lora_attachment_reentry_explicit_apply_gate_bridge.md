# ASH-55 — Runtime LoRA Attachment Re-entry / Explicit Apply Gate Bridge

## Status
PASS_RUNTIME_LORA_ATTACHMENT_REENTRY_EXPLICIT_APPLY_GATE_BRIDGE

## Scope
- Reads ASH-54 registry mutation dry-run report.
- Collects accepted dry-run records.
- Validates single target adapter scope.
- Validates bound LoRA artifact lineage evidence.
- Builds runtime LoRA attachment re-entry candidate.
- Builds ASH-48-compatible explicit apply request bridge envelope.
- Does not call the ASH-48 explicit apply gate.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not create apply receipt.
- Does not change current pointer.
- Does not mutate registry.
- Does not create previous attachment snapshot.

## Files
- `crates/ash_core/src/runtime_lora_attachment_reentry_bridge.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_55_runtime_lora_attachment_reentry_bridge.rs`

## Seal Flags
- `reentry_candidate_created = true`
- `explicit_apply_request_envelope_created = true`
- `bridge_to_explicit_apply_gate_created = true`
- `runtime_attach_allowed = false`
- `explicit_apply_commit_allowed = false`
- `apply_receipt_allowed = false`
- `current_pointer_changed = false`
- `registry_mutation_allowed = false`
- `previous_attachment_snapshot_allowed = false`

## Runtime Boundary
ASH-55 creates an `AshRuntimeLoraExplicitApplyRequest` envelope only. It does not call `build_runtime_lora_explicit_apply_gate_report`, and it never opens `CommitExplicitApply`.

## Reproducibility
`reentry_candidate_id`, `explicit_apply_request_id`, and `envelope_id` are deterministically derived from:

- ASH-55 `reentry_request_id`
- ASH-54 `dry_run_plan_id`
- ASH-53 `ledger_id`
- target adapter id
- target artifact id
- accepted dry-run record ids
- LoRA lineage trace id
- manifest path
- weights path

## Result
ASH-55 creates runtime LoRA attachment re-entry bridge evidence only. Actual runtime attach, explicit apply commit, apply receipt creation, current pointer movement, registry mutation, and previous attachment snapshot creation remain sealed.
