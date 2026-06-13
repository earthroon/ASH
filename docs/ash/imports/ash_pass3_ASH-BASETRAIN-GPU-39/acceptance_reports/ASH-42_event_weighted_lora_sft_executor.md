# ASH-42 Event-Weighted LoRA SFT Executor / Training Run Gate

## Status
PASS_EVENT_WEIGHTED_LORA_SFT_EXECUTOR

## Sealed
- AshSftTrainingExecutorMode
- AshSftTrainingBackendKind
- AshSftTrainingRunDecision
- AshSftTrainingFailureKind
- AshSftTrainingRunGateConfig
- AshSftTrainingCommandPlan
- AshSftTrainingRunTelemetry
- AshTrainedLoraAdapterArtifact
- AshSftTrainingFailure
- AshSftTrainingRunGateReport
- AshSftTrainingResultReport
- explicit training gate
- command plan generation
- dataset artifact validation
- trained artifact capture
- training telemetry capture

## Policy
- ASH-42 may execute training only in explicit ExecuteTrainingRun mode.
- allow_execute_training must be true for execution.
- Dataset artifact must be ready_for_training.
- Training output requires checksum.
- Trained artifact requires ASH-39 outcome evaluation.
- Trained artifact requires ASH-40 promotion gate.
- ASH-42 does not mutate adapter registry.
- ASH-42 does not change current pointer.
- ASH-42 does not auto-apply runtime routing.
- No Python validator.

## Boundary
ash_core computes gate, command, and artifact contracts.
orchestrator_local may execute backend under explicit gate.
lora_train performs actual training later/behind the orchestrator gate.
ASH-39 evaluates outcome after training.
