# DECODE OVERRIDE CANDIDATE POOL PRIORITY5 PATCH

## Goal
Promote task-specific candidate diversity policy from an implicit convention into a runtime-level plan builder.

## What changed
- Added `StandardInferCandidatePlanProfile`
- Added `candidate_plan_profile_for_task(...)`
- Added `build_candidate_plan_for_profile(...)`
- Added `build_candidate_plan_for_task(...)`
- Changed `run_standard_infer_candidate_pool(...)` so that an empty plan now auto-expands into a task-specific candidate plan instead of falling back to a single candidate.

## Profiles
- `Analysis`: more candidates, higher `min_new_tokens`, wider temperature spread
- `SubtitlePolish`: tighter temperature spread, shorter generation budget
- `TranslationAssist`: moderate spread with restrained `top_p`
- `JsonPolish`: conservative decode settings
- `Default`: balanced profile

## Behavioral contract
- Route / lora / prompt remain frozen at the candidate-plan layer
- Diversity now comes from decode overrides only
- Empty candidate plans are no longer "single-candidate mode"; they are "auto-profile mode"

## Follow-up
Next priority is to let rerank trace surface the chosen diversity profile explicitly and tune per-profile weights.
