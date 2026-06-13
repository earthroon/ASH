# 16AI-6F Checkpoint-Compatible Assembly Commit Gate Report

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_delta_gate | 16AI-6E-R4 PASS_DELTA_REPORT |
| source_coverage_gate | 16AI-6E-R5 PASS_COVERAGE_REPORT |

## 2. Scope

| field | value |
|---|---|
| assembly_commit_mode | compare-only |
| generation | false |
| token_ids_mutated | false |
| committed_prompt_ids | baseline |
| vocab_augmented | false |
| new_token_ids_created | false |

## 3. Gate Thresholds

| threshold | value |
|---|---:|
| min_fragmentation_delta | 1.000 |
| min_path_score | 70.000 |
| min_coverage_score | 90.000 |
| allow_variant_covered | true |
| allow_fallback_encoded | false |
| allow_unknown | false |
| allow_lookup_miss | false |

## 4. Summary

| field | value |
|---|---:|
| total | 21 |
| commit_allowed_count | 8 |
| commit_blocked_count | 13 |
| commit_applied_count | 0 |
| baseline_committed_count | 21 |
| variant_warning_count | 21 |
| exact_zero_warning_count | 21 |
| acceptance_status | PASS_COMMIT_GATE_COMPARE_ONLY |

## 5. Case Decisions

| case | wrapper | delta | path_score | coverage_score | allowed | applied | block_reason | warnings |
|---|---|---:|---:|---:|---:|---:|---|---|
| ko_beetle_question | plain | 80.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_beetle_question | dialogue-ko | 80.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_beetle_question | instruction-ko | 80.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_particle_short | plain | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_particle_short | dialogue-ko | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_particle_short | instruction-ko | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_ending_question | plain | 0.000 | 100.000 | 91.000 | false | false | FragmentationDeltaTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_ending_question | dialogue-ko | 30.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_ending_question | instruction-ko | 30.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_compound_noun | plain | 55.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_compound_noun | dialogue-ko | 80.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_compound_noun | instruction-ko | 80.000 | 100.000 | 91.000 | false | false | FallbackEncodedDetected | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_descriptive_sentence | plain | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_descriptive_sentence | dialogue-ko | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| ko_descriptive_sentence | instruction-ko | 80.000 | 100.000 | 91.000 | true | false | none | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_user_label | plain | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_user_label | dialogue-ko | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_user_label | instruction-ko | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_assistant_label | plain | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_assistant_label | dialogue-ko | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |
| wrapper_assistant_label | instruction-ko | 0.000 | 0.000 | 91.000 | false | false | FragmentationDeltaTooLow,PathScoreTooLow | VariantCoverageDominant,ExactCoverageZero,GenerationNotValidated,CommitShadowOnly,CheckpointCompatibleButNotQualityValidated |

## 6. 확정

- commit gate가 생성됨.
- assembled ids는 기본 compare-only mode에서 commit되지 않음.
- commit_allowed와 commit_applied는 분리됨.
- R4/R5 PASS 상태를 읽음.

## 7. 추정

- commit_allowed=true인 케이스는 다음 generation recompare 후보임.
- variant coverage 중심이므로 VariantCoverageDominant warning은 유지해야 함.

## 8. 판단불가

- generation 품질 개선 여부.
- assembled commit 기본 활성화 안전성.
- 최종 best_wrapper.
