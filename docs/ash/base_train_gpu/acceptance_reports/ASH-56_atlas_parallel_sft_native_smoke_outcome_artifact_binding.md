# ASH-56 — Atlas-Parallel SFT Native Smoke / Outcome Artifact Binding

## Status
PASS_ATLAS_PARALLEL_SFT_NATIVE_SMOKE_OUTCOME_ARTIFACT_BINDING

## Scope
- Reads ASH-55 runtime LoRA re-entry bridge report.
- Validates explicit apply bridge envelope.
- Validates LoRA artifact lineage consistency.
- Builds deterministic native smoke command plan.
- Builds SFT outcome artifact binding evidence.
- Optionally binds externally provided native smoke evidence.
- Does not spawn native process.
- Does not execute smoke command.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not create apply receipt.
- Does not change current pointer.
- Does not mutate registry.
- Does not write LoRA artifact.

## Files
- crates/ash_core/src/atlas_sft_native_smoke_artifact_binding.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/ash_56_atlas_sft_native_smoke_artifact_binding.rs

## Seal Flags
- native_smoke_plan_created = true
- outcome_artifact_binding_created = true
- native_process_spawn_allowed = false
- smoke_command_execution_allowed = false
- runtime_attach_allowed = false
- explicit_apply_commit_allowed = false
- current_pointer_changed = false
- registry_mutation_allowed = false
- lora_artifact_write_allowed = false
- apply_receipt_allowed = false

## Reproducibility
- smoke_plan_id is deterministically derived from:
  - smoke_binding_request_id
  - ASH-55 reentry_candidate_id
  - explicit_apply_request_id
  - target_adapter_id
  - target_artifact_id
  - target_manifest_path
  - target_weights_path
  - source_sft_run_id
- binding_evidence_id is deterministically derived from:
  - smoke_binding_request_id
  - ASH-55 reentry_candidate_id
  - explicit_apply_request_id
  - source_sft_run_id
  - LoRA lineage trace id
  - smoke_plan_id

## Result
ASH-56 creates native smoke planning and outcome artifact binding evidence only. Native process execution, smoke command execution, runtime attach, explicit apply commit, apply receipt creation, current pointer movement, registry mutation, and LoRA artifact write remain sealed.
