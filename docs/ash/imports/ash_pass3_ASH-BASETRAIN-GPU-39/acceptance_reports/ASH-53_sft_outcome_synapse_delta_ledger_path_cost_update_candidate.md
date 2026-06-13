# ASH-53 — SFT Outcome Synapse Delta Ledger / Path Cost Update Candidate

## Status
PASS_SFT_OUTCOME_SYNAPSE_DELTA_LEDGER_PATH_COST_UPDATE_CANDIDATE

## Scope
- Creates deterministic SFT outcome synapse delta ledger evidence.
- Creates edge weight update candidates when `affected_edge_id` exists.
- Creates path action cost update candidates when `affected_path_id` exists.
- Creates hard-negative demotion candidates when regression risk exceeds the configured threshold.
- Does not mutate synapse registry.
- Does not mutate edge weight.
- Does not mutate path cost.
- Does not attach runtime LoRA.
- Does not change current pointer.
- Does not write persistent ledger files.

## Files
- `crates/ash_core/src/sft_outcome_synapse_delta_ledger.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_53_sft_outcome_synapse_delta_ledger.rs`

## Seal Flags
- `delta_ledger_created = true`
- `path_cost_update_candidate_created = true`
- `edge_weight_update_candidate_created = true`
- `synapse_registry_mutation_allowed = false`
- `edge_weight_mutation_allowed = false`
- `path_cost_mutation_allowed = false`
- `runtime_attach_allowed = false`
- `current_pointer_changed = false`
- `persistent_ledger_write_allowed = false`

## Reproducibility
`ledger_id` is deterministically derived from:

- `ledger_request_id`
- ASH-51 `candidate_id`
- ASH-52 `schedule_id`
- `sft_run_id`
- `affected_path_id`
- `affected_edge_id`

`entry_id` is deterministically derived from:

- `ledger_id`
- `delta_kind`
- `affected_path_id`
- `affected_edge_id`
- `target_adapter_id`
- proposed edge weight delta
- proposed action cost delta

## Result
ASH-53 creates ledger evidence only. Actual registry mutation, edge weight update, path cost update, runtime attach, current pointer movement, and persistent ledger write remain sealed.
