# ASH-39 SFT Outcome Evaluation / Replay Feedback Merge

## Status
PASS_SFT_OUTCOME_EVALUATION_REPLAY_FEEDBACK_MERGE

## Sealed
- AshSftOutcomeEvaluationMode
- AshSftOutcomeDecision
- AshSftOutcomeMetricKind
- AshPlasticityDeltaDirection
- AshSftOutcomeAdapterTarget
- AshSftOutcomeEvaluationPlan
- AshSftOutcomeMetricScore
- AshSftOutcomeAdapterResult
- AshSftOutcomeReplayMergeRecord
- AshSftOutcomeReplayMergeReport
- AshSftAdapterPlasticityDelta
- AshSftPlasticityDeltaReport
- AshPlasticityPromotionCandidateEvidence
- AshSftOutcomeEvaluationReport
- outcome evaluation plan
- observed result merge
- replay feedback merge
- plasticity delta report
- promotion candidate evidence

## Policy
- ASH-39 does not run SFT
- ASH-39 does not export JSONL
- ASH-39 does not mutate adapter registry
- ASH-39 does not change current pointer
- ASH-39 does not auto-apply runtime routing
- Holdout samples are evaluation-only
- Replay improvements produce resolved evidence, not deletion
- Replay regressions strengthen suppression evidence
- Promotion evidence still requires ASH-40 runtime re-entry gate
- No Python validator

## Boundary
ash_core computes SFT outcome evaluation.
orchestrator_local reports outcome evidence.
artifact_store preserves optional outcome snapshots.
ASH-40 performs promotion/runtime re-entry gating.
