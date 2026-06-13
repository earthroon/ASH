# QW-50-R0O — Action Handoff Snapshot / Runtime LoRA Native Stage Alignment

## Scope

- Target crates:
  - `ash_core`
  - `model_core`
- Target files:
  - `crates/ash_core/tests/sft_gpu_obs_06_action_candidate_preflight.rs`
  - `crates/model_core/src/runtime_lora.rs`

## Fix

- Replaced stale test import `AshGpuDecisionActionCandidateHandoffPacketSnapshot` with the current `AshGpuDecisionActionHandoffPacketSnapshot` SSOT type.
- Preserved the existing handoff packet snapshot literal and no-apply preflight semantics.
- Replaced `ModuleLocalNativeTrainStepOutput { native_step_started: true, ... }` test literals with `native_e2e_stage: Some("input_ready".to_string())`.
- Preserved `ModuleLocalNativeDedicatedNstepStepResult::native_step_started` fields; those are a different struct and remain valid.

## Guard

- No runtime apply execution.
- No adapter registry mutation.
- No production apply.
- No runtime LoRA execution semantics changed beyond test fixture field alignment.
- No compatibility alias type added.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
