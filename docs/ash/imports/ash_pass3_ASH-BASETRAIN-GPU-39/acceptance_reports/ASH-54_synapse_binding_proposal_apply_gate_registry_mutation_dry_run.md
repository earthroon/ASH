# ASH-54 — Synapse Binding Proposal Apply Gate / Registry Mutation Dry-run

## Status
PASS_SYNAPSE_BINDING_PROPOSAL_APPLY_GATE_REGISTRY_MUTATION_DRY_RUN

## Scope
- Reads ASH-53 SFT outcome synapse delta ledger.
- Reads `AshAdapterSynapseRegistry` as a read-only snapshot.
- Builds deterministic proposal apply dry-run records.
- Verifies edge/path target viability without mutation.
- Records accepted/rejected/skipped dry-run decisions.
- Does not apply to clone.
- Does not mutate synapse registry.
- Does not mutate edge weight.
- Does not mutate path cost.
- Does not attach runtime LoRA.
- Does not change current pointer.
- Does not write persistent registry files.

## Files
- `crates/ash_core/src/synapse_binding_proposal_apply_gate.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_54_synapse_binding_proposal_apply_gate.rs`

## Seal Flags
- proposal_apply_dry_run_created = true
- registry_mutation_dry_run_created = true
- apply_to_clone_allowed = false
- synapse_registry_mutation_allowed = false
- edge_weight_mutation_allowed = false
- path_cost_mutation_allowed = false
- runtime_attach_allowed = false
- current_pointer_changed = false
- persistent_registry_write_allowed = false
- original_registry_unchanged = true

## Reproducibility
`dry_run_plan_id` is deterministically derived from:
- `dry_run_request_id`
- ASH-53 `ledger_id`
- `registry.version`
- ledger entry ids

`record_id` is deterministically derived from:
- `dry_run_plan_id`
- ledger `entry_id`
- proposal kind
- affected path/edge ids
- target adapter id
- proposed edge/action-cost deltas

## Result
ASH-54 performs registry mutation dry-run only. Actual registry mutation, edge weight update, path cost update, runtime attach, current pointer movement, apply-to-clone, and persistent registry write remain sealed.
