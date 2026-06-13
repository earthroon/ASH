# ASH-27 Hard Negative Replay Evaluation Loop

## Status
PASS_HARD_NEGATIVE_REPLAY_EVALUATION_LOOP

## Sealed
- AshReplayEvaluationMode
- AshReplayEvaluationCaseKind
- AshReplayEvaluationDecision
- AshReplaySeverityAction
- AshReplayEvaluationCandidateTarget
- AshHardNegativeReplayEvaluationCase
- AshHardNegativeReplayEvaluationSuite
- AshHardNegativeReplayEvaluationResult
- AshHardNegativeReplayEvaluationReport
- AshReplayPromotionGateEvidence
- contract-level replay evaluation
- runtime replay request planning
- runtime result merge
- adapter overlap scoring
- promotion gate evidence generation

## Policy
- Hard negative replay is evaluation evidence.
- ASH-27 does not mutate registry.
- ASH-27 does not change current pointer.
- ASH-27 does not train or bake LoRA.
- Raw prompt is not fabricated.
- Contract-only replay works without raw prompt.
- Critical overlap can block promotion.
- Missing weight telemetry can fail evaluation.
- Runtime replay is planned, not executed by ash_core.
- No Python validator.

## Boundary
ash_core computes replay evaluation.
runtime may execute replay requests later.
orchestrator_local reports audit evidence.
artifact_store preserves evaluation snapshots.
