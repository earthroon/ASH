# ASH-52 — SFT Atlas Batch Schedule / Adapter-Scoped Hidden Token Grouping

## Status
PASS_SFT_ATLAS_BATCH_SCHEDULE_ADAPTER_SCOPED_HIDDEN_TOKEN_GROUPING

## Scope
- Creates adapter-scoped hidden token groups for SFT atlas batching.
- Creates a deterministic metadata-only atlas batch schedule from an ASH-51 binding candidate.
- Does not execute training.
- Does not write gradients.
- Does not run optimizer steps.
- Does not write LoRA artifacts.
- Does not mutate the synapse registry.
- Does not attach runtime LoRA.
- Does not change current pointers.

## Files
- `crates/ash_core/src/sft_atlas_batch_schedule.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_52_sft_atlas_batch_schedule.rs`
- `acceptance_reports/ASH-52_sft_atlas_batch_schedule_adapter_scoped_hidden_token_grouping.md`
- `acceptance_reports/ASH-52_static_validation_result.md`

## Seal Flags
- `hidden_token_grouping_created = true`
- `adapter_scoped_grouping = true`
- `training_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `synapse_registry_mutation_allowed = false` through ASH-51 candidate validation
- `runtime_attach_allowed = false` through ASH-51 candidate validation
- `current_pointer_changed = false` through ASH-51 candidate validation

## Contract
ASH-52 consumes `AshAtlasSftSynapseBindingCandidate` and `AshSftAtlasHiddenTokenSample` metadata. It validates that every hidden token sample stays inside the ASH-51 candidate's affected adapters, then groups samples by deterministic ordering:

1. `adapter_id ASC`
2. `hidden_width ASC`
3. `source_sequence_id ASC`
4. `token_start ASC`
5. `sample_id ASC`

Groups are split by:

- adapter boundary
- hidden width boundary
- `max_tokens_per_group`
- `max_sequences_per_group`

## Reproducibility
`schedule_id` is deterministically derived from:

- ASH-51 `candidate_id`
- `sft_run_id`
- `target_adapter_id`
- `affected_path_id`
- `affected_edge_id`
- generated `group_id` list

`group_id` is deterministically derived from:

- ASH-51 `candidate_id`
- `adapter_id`
- `hidden_width`
- adapter-local group index
- grouped sample ids

## Tests Added
- creates adapter-scoped hidden token schedule without training execution
- rejects sample outside candidate affected adapters
- splits groups by hidden width
- splits groups by token capacity
- rejects training/gradient/optimizer/artifact write flags
- schedule and group ids are deterministic

## Result
ASH-52 creates scheduling evidence only. Atlas SFT execution, gradient write, optimizer step, LoRA artifact write, registry mutation, runtime attach, and current pointer movement remain sealed.
