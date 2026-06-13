# ASH-51 — Atlas-Parallel SFT Outcome → Path-Integral LoRA Synapse Binding Candidate

## Status
PASS_ATLAS_PARALLEL_SFT_OUTCOME_PATH_INTEGRAL_SYNAPSE_BINDING_CANDIDATE

## Scope
- Creates a deterministic SFT outcome → path-integral LoRA synapse binding candidate.
- Does not mutate the synapse registry.
- Does not attach runtime LoRA.
- Does not change current pointers.
- Does not apply edge weight or action cost deltas.

## Files
- `crates/ash_core/src/atlas_sft_synapse_binding_candidate.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_51_atlas_sft_synapse_binding_candidate.rs`
- `acceptance_reports/ASH-51_atlas_parallel_sft_outcome_path_integral_synapse_binding_candidate.md`

## Seal Flags
- `binding_candidate_created = true`
- `synapse_registry_mutation_allowed = false`
- `runtime_attach_allowed = false`
- `current_pointer_changed = false`
- `artifact_lineage_required = true`
- `sft_outcome_required = true`
- `path_integral_route_required = true`

## SSOT Inputs
- ASH-17 `AshPathIntegralSynapseRoutePlan`
- ASH-39 `AshSftOutcomeEvaluationReport`
- ASH-45D `AshLoraArtifactLineageTrace`

## Reproducibility
`candidate_id` is deterministic from:

- `sft_run_id`
- `trained_lora_artifact_id`
- `artifact_lineage_id`
- `selected_path_id`
- `affected_edge_id`
- `source_adapter_id`
- `target_adapter_id`
- `affected_adapter_ids`

## Guard Tests
- candidate creation preserves no-mutation seal
- deterministic candidate id
- missing selected path rejection
- SFT outcome failure rejection
- lineage auto-adjustment rejection
- config-opened mutation/runtime/current-pointer rejection

## Result
ASH-51 creates candidate evidence only. Registry mutation, runtime attachment, current pointer movement, and production apply remain sealed.
