# QW-52C-R3 — Shadow Rerank Weight Sensitivity Sweep / No Apply Seal

## Status
PASS_STATIC_SHADOW_RERANK_WEIGHT_SENSITIVITY_SWEEP

## Base
QW-52C-R2

## Purpose
QW-52C shadow rerank weights were swept in shadow mode to analyze RiskyDiff causes without applying, committing, or promoting any profile.

## Generated
- ShadowRerankWeightSensitivityTrace
- WeightSweepMatrix JSONL
- WeightSensitivityReport
- WeightSensitivityManifest

## Summary
- profile_count = 7
- base_risky_diff_count = 1
- min_risky_diff_count = 0
- safe_profile_candidate_count = 3
- best_candidate_profile_id = reduced_dream_weight_v1

## Safe Profile Candidates
- reduced_dream_weight_v1
- reduced_cji_cairo_weight_v1
- balanced_risk_support_v1

## Confirmed
- RiskyDiff attribution is recorded.
- Reduced dream/cji profile candidates are recorded if they clear RiskyDiff.
- BeneficialDiff preservation is checked.
- StableBroken cases are checked.
- No weight profile is committed.
- No policy promotion is allowed.
- No threshold autotune is performed.
- No runtime behavior changes.

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
- memory_mutation = false
- training_mutation = false
- lora_mutation = false

## Language Policy
- crate_js_ts_allowed = false
- sweep_language = Rust
- validator_language = Rust

## Next
QW-52C-R4 — RiskyDiff Feature Attribution Report / Safe Profile Candidate Seal
