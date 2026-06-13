# ASH-7 Eval Arbitration / Promotion Brain

## Status
PASS_STATIC / PASS_ASH_EVAL_ARBITRATION_PROMOTION_BRAIN

## Sealed
- RuntimeDeltaEvalSummary
- QualityEvalSummary
- LossTraceSummary
- GenerationHygieneSummary
- ReplayFailureSummary
- AdapterEvalPacket
- PromotionDecision
- EvalArbitrationPolicy
- AdapterSynapseStatusPatch

## Arbitration
- all pass -> Promote
- zero delta -> Reject
- missing required quality eval -> PendingManualReview
- unresolved silent fallback / P0 runtime failure -> RollbackRequired

## Guards
- no promotion on zero delta
- no promotion on NaN logits
- no promotion on loss explosion
- no promotion on empty generation
- unresolved P0 can force rollback
- Python validator forbidden

## Boundary
ash_core arbitrates eval summary DTOs only.
ash_core does not execute eval.
ash_core does not read report files.
ash_core does not copy adapter artifacts.
ash_core does not load safetensors.
