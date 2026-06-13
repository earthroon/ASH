# 16AI-6I Dialogue-KO Gated Assembled Commit Probe

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_policy_gate | 16AI-6H-R2 PASS_POLICY_QUALITY_INTEGRATED |
| source_quality_gate | 16AI-6G PASS_QUALITY_RECOMPARE |
| source_commit_gate | 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY |

## 2. Scope

| field | value |
|---|---|
| generation | true |
| checkpoint_required | true |
| global_default_commit | false |
| branch_local_commit | true |
| commit_scope | dialogue-ko-policy-approved |
| token_ids_mutated | false |
| vocab_augmented | false |
| new_token_ids_created | false |

## 3. Summary

| field | value |
|---|---:|
| total_cases | 21 |
| eligible_commit_cases | 2 |
| branch_commit_applied_count | 2 |
| baseline_fallback_count | 19 |
| global_commit_applied_count | 0 |
| quality_worsened_count | 0 |
| dpo_provisional_count | 2 |
| coverage_score | 91.000 |
| status | PASS_GATED_COMMIT_PROBE |

## 4. Branch Commit Cases

| case | wrapper | quality_delta | committed_source | new_text | quality_score |
|---|---|---:|---|---|---:|
| ko_descriptive_sentence | dialogue-ko | 5.000 | assembled | `▁계실까` | 75.000 |
| ko_particle_short | dialogue-ko | 5.000 | assembled | `▁석회` | 75.000 |

## 5. Baseline Fallback Cases

| case | wrapper | fallback_reason | quality_delta |
|---|---|---|---:|
| ko_beetle_question | dialogue-ko | PolicyNotAssembledShadow | 0.000 |
| ko_beetle_question | instruction-ko | WrapperNotDialogueKo | 0.000 |
| ko_beetle_question | plain | WrapperNotDialogueKo | 0.000 |
| ko_compound_noun | dialogue-ko | PolicyNotAssembledShadow | 0.000 |
| ko_compound_noun | instruction-ko | WrapperNotDialogueKo | 0.000 |
| ko_compound_noun | plain | WrapperNotDialogueKo | 0.000 |
| ko_descriptive_sentence | instruction-ko | WrapperNotDialogueKo | 0.000 |
| ko_descriptive_sentence | plain | WrapperNotDialogueKo | 0.000 |
| ko_ending_question | dialogue-ko | PolicyNotAssembledShadow | 0.000 |
| ko_ending_question | instruction-ko | WrapperNotDialogueKo | 0.000 |
| ko_ending_question | plain | WrapperNotDialogueKo | 0.000 |
| ko_particle_short | instruction-ko | WrapperNotDialogueKo | 0.000 |
| ko_particle_short | plain | WrapperNotDialogueKo | 0.000 |
| wrapper_assistant_label | dialogue-ko | PolicyNotAssembledShadow | 0.000 |
| wrapper_assistant_label | instruction-ko | WrapperNotDialogueKo | 0.000 |
| wrapper_assistant_label | plain | WrapperNotDialogueKo | 0.000 |
| wrapper_user_label | dialogue-ko | PolicyNotAssembledShadow | 0.000 |
| wrapper_user_label | instruction-ko | WrapperNotDialogueKo | 0.000 |
| wrapper_user_label | plain | WrapperNotDialogueKo | 0.000 |

## 6. 확정

- Branch-local assembled commit probe was executed.
- Global default commit remains false.
- Non-eligible cases fallback to baseline with explicit reasons.

## 7. 판단불가

- Default commit safety.
- Long-form generation quality.
- DPO training effect.
