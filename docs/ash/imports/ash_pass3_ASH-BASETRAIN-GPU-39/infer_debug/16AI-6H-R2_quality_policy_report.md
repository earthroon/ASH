# 16AI-6H-R2 Quality Policy Integration Report

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_policy_gate | 16AI-6H-R1 PASS_POLICY_COMPARE_ONLY |
| source_quality_gate | 16AI-6G PASS_QUALITY_RECOMPARE |
| source_commit_gate | 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY |

## 2. Scope

| field | value |
|---|---|
| policy_mode | quality-integrated |
| generation | false |
| quality_generation_source | 16AI-6G |
| default_commit | false |
| allow_gated_commit | false |
| token_ids_mutated | false |
| committed_prompt_ids | baseline |

## 3. Quality Summary

| field | value |
|---|---:|
| total | 21 |
| quality_improved_count | 2 |
| quality_unchanged_count | 19 |
| quality_worsened_count | 0 |
| avg_quality_delta | 0.476 |

## 4. Policy Summary

| field | value |
|---|---:|
| assembled_shadow_count | 2 |
| assembled_gated_count | 0 |
| baseline_fallback_count | 0 |
| dpo_candidate_count | 2 |
| dpo_provisional_count | 2 |
| commit_applied_count | 0 |
| acceptance_status | PASS_POLICY_QUALITY_INTEGRATED |

## 5. Shadow / DPO Candidates

| case | wrapper | baseline_score | assembled_score | delta | policy | dpo_status |
|---|---|---:|---:|---:|---|---|
| ko_descriptive_sentence | dialogue-ko | 70.0 | 75.0 | 5.0 | AssembledShadow | Provisional |
| ko_particle_short | dialogue-ko | 70.0 | 75.0 | 5.0 | AssembledShadow | Provisional |

## 6. Case Policy Decisions

| case | wrapper | quality | updated_mode | dpo | warnings |
|---|---|---:|---|---|---|
| ko_beetle_question | dialogue-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_beetle_question | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_beetle_question | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_compound_noun | dialogue-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_compound_noun | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_compound_noun | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_descriptive_sentence | dialogue-ko | 5.0 | AssembledShadow | Provisional | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated,DpoCandidateProvisional,ShadowModeOnly |
| ko_descriptive_sentence | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| ko_descriptive_sentence | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| ko_ending_question | dialogue-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| ko_ending_question | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| ko_ending_question | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| ko_particle_short | dialogue-ko | 5.0 | AssembledShadow | Provisional | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated,DpoCandidateProvisional,ShadowModeOnly |
| ko_particle_short | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| ko_particle_short | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,AssembledCandidateNotCommitted,ShortGenerationOnly,LongFormQualityNotValidated |
| wrapper_assistant_label | dialogue-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| wrapper_assistant_label | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| wrapper_assistant_label | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| wrapper_user_label | dialogue-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| wrapper_user_label | instruction-ko | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |
| wrapper_user_label | plain | 0.0 | AssembledCandidate | ExcludedTie | VariantCoverageDominant,ExactCoverageZero,CompareOnlyMode,CheckpointCompatibleButQualityPending,ShortGenerationOnly,LongFormQualityNotValidated,AssembledCandidateNotCommitted |

## 7. 확정

- 6G quality 결과가 6H policy에 통합됨.
- quality improved 케이스는 AssembledShadow 후보로 승격됨.
- default commit은 false 유지.
- DPO candidate는 provisional로만 기록됨.

## 8. 추정

- dialogue-ko wrapper가 assembled tokenizer와 궁합이 좋을 가능성.
- shadow 후보는 장문 재검증 후 DPO 후보로 발전 가능.

## 9. 판단불가

- assembled default commit 안전성.
- 장문 generation 품질.
- DPO 학습 효과.
- 최종 wrapper 정책.
