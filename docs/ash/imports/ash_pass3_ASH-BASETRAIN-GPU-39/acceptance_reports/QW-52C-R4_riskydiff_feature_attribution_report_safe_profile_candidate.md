# QW-52C-R4 — RiskyDiff Feature Attribution Report / Safe Profile Candidate Seal

## Status
PASS_STATIC_RISKYDIFF_FEATURE_ATTRIBUTION_REPORT

## Base
QW-52C-R3

## Purpose
RiskyDiff causes from the QW-52C shadow rerank chain were summarized into a feature attribution report, and safe profile candidates were sealed as review-only artifacts.

## Generated
- RiskyDiffFeatureAttributionReport
- SafeProfileCandidates
- SafeProfileCandidateManifest

## Confirmed
- RiskyDiff attribution is recorded.
- Dominant suspected cause is recorded.
- Safe profile candidates are ranked.
- Best candidate profile is recorded.
- Safe profile candidates are not applied.
- No weight profile is committed.
- No policy promotion is allowed.
- Human review is required.
- Runtime sample expansion is required.

## Decision
- best_candidate_profile_id = reduced_dream_weight_v1
- safe_profile_apply_allowed = false
- weight_commit_allowed = false
- policy_promotion_allowed = false
- runtime_apply_allowed = false
- recommended_next_patch = QW-52C-R5

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- hard_ban = false
- blacklist_mutation = false
- rerank_execution = false
- retry_execution = false
- policy_promotion = false
- threshold_autotune = false
- weight_commit = false
- safe_profile_apply = false
- memory_mutation = false
- training_mutation = false
- lora_mutation = false

## Language Policy
- crate_js_ts_allowed = false
- report_language = Rust
- validator_language = Rust

## Next
QW-52C-R5 — Safe Profile Review Gate / Operator Approval Queue Seal
