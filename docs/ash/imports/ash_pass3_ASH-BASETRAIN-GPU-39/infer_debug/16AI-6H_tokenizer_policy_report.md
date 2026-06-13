# 16AI-6H Tokenizer Enhancement Policy Report

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_delta_gate | 16AI-6E-R4 PASS_DELTA_REPORT |
| source_coverage_gate | 16AI-6E-R5 PASS_COVERAGE_REPORT |
| source_commit_gate | 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY |
| source_quality_gate | pending |

## 2. Scope

| field | value |
|---|---|
| policy_mode | compare-only |
| generation | false |
| token_ids_mutated | false |
| committed_prompt_ids | baseline |
| vocab_augmented | false |
| new_token_ids_created | false |

## 3. Policy Thresholds

| threshold | value |
|---|---:|
| min_fragmentation_delta | 1.000 |
| min_path_score | 70.000 |
| min_coverage_score | 90.000 |
| min_quality_delta | 1.000 |
| allow_variant_covered | true |
| allow_fallback_encoded | false |
| allow_unknown | false |
| allow_lookup_miss | false |

## 4. Summary

| field | value |
|---|---:|
| total | 21 |
| use_baseline_count | 13 |
| assembled_candidate_count | 8 |
| assembled_gated_count | 0 |
| baseline_fallback_count | 13 |
| generation_not_validated_count | 21 |
| variant_warning_count | 21 |
| exact_zero_warning_count | 21 |
| commit_applied_count | 0 |
| acceptance_status | PASS_POLICY_COMPARE_ONLY |

## 5. Case Policy Decisions

| case | wrapper | decision | selected_mode | delta | path | coverage | quality_delta | fallback_reason | warnings |
|---|---|---|---|---:|---:|---:|---:|---|---|
| ko_beetle_question | plain | UseBaseline | BaselineFallback | 80.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_beetle_question | dialogue-ko | UseBaseline | BaselineFallback | 80.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_beetle_question | instruction-ko | UseBaseline | BaselineFallback | 80.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_particle_short | plain | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_particle_short | dialogue-ko | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_particle_short | instruction-ko | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_ending_question | plain | UseBaseline | BaselineFallback | 0.000 | 100.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_ending_question | dialogue-ko | AllowAssembledCompareOnly | AssembledCandidate | 30.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_ending_question | instruction-ko | AllowAssembledCompareOnly | AssembledCandidate | 30.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_compound_noun | plain | UseBaseline | BaselineFallback | 55.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_compound_noun | dialogue-ko | UseBaseline | BaselineFallback | 80.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_compound_noun | instruction-ko | UseBaseline | BaselineFallback | 80.000 | 100.000 | 91.000 | NA | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| ko_descriptive_sentence | plain | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_descriptive_sentence | dialogue-ko | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| ko_descriptive_sentence | instruction-ko | AllowAssembledCompareOnly | AssembledCandidate | 80.000 | 100.000 | 91.000 | NA | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted |
| wrapper_user_label | plain | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| wrapper_user_label | dialogue-ko | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| wrapper_user_label | instruction-ko | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| wrapper_assistant_label | plain | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| wrapper_assistant_label | dialogue-ko | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |
| wrapper_assistant_label | instruction-ko | UseBaseline | BaselineFallback | 0.000 | 0.000 | 91.000 | NA | NoFragmentationGain | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CompareOnlyMode,CheckpointCompatibleButQualityPending |

## 6. 확정

- policy decision layer 생성.
- baseline fallback reason 기록.
- assembled candidate reason 기록.
- compare-only에서는 commit_applied=0 유지.

## 7. 추정

- 어느 케이스가 assembled 후보인지.
- 어느 케이스가 baseline fallback 대상인지.
- generation compare 이후 gated 후보가 될 가능성.

## 8. 판단불가

- generation 품질 개선 여부.
- assembled ids 기본 commit 안전성.
- 최종 best_wrapper.
