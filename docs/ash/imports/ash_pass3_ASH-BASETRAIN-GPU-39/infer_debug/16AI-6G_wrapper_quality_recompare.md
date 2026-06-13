# 16AI-6G Wrapper Quality Recompare with Assembled IDs

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_policy_gate | 16AI-6H PASS_POLICY_COMPARE_ONLY |
| source_commit_gate | 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY |

## 2. Scope

| field | value |
|---|---|
| generation | true |
| checkpoint_required | true |
| assembly_commit_mode | compare-only |
| default_commit | false |
| token_ids_mutated | false |
| committed_prompt_ids | branch-local compare only |

## 3. Summary

| field | value |
|---|---:|
| total_pairs | 21 |
| baseline_runs | 21 |
| assembled_runs | 21 |
| assembled_improved_count | 2 |
| assembled_unchanged_count | 19 |
| assembled_worsened_count | 0 |
| avg_quality_delta | 0.476 |
| acceptance_status | PASS_QUALITY_RECOMPARE |

## 4. Case Pair Table

| case | wrapper | baseline_text | assembled_text | baseline_score | assembled_score | delta | winner |
|---|---|---|---|---:|---:|---:|---|
| ko_beetle_question | dialogue-ko | `▁중요한` | `▁건강상에` | 75.0 | 75.0 | 0.0 | Tie |
| ko_beetle_question | instruction-ko | `▁생각해` | `▁건강상에` | 75.0 | 75.0 | 0.0 | Tie |
| ko_beetle_question | plain | `▁모양으로` | `▁건강상에` | 75.0 | 75.0 | 0.0 | Tie |
| ko_compound_noun | dialogue-ko | `▁중요한` | `▁살인` | 75.0 | 75.0 | 0.0 | Tie |
| ko_compound_noun | instruction-ko | `▁이런` | `▁살인` | 75.0 | 75.0 | 0.0 | Tie |
| ko_compound_noun | plain | `▁살인` | `▁살인` | 75.0 | 75.0 | 0.0 | Tie |
| ko_descriptive_sentence | dialogue-ko | `<0x63>` | `▁계실까` | 70.0 | 75.0 | 5.0 | Assembled |
| ko_descriptive_sentence | instruction-ko | `▁양념치킨` | `▁계실까` | 75.0 | 75.0 | 0.0 | Tie |
| ko_descriptive_sentence | plain | `▁김치` | `▁계실까` | 75.0 | 75.0 | 0.0 | Tie |
| ko_ending_question | dialogue-ko | `▁중요한` | `▁성취감이` | 75.0 | 75.0 | 0.0 | Tie |
| ko_ending_question | instruction-ko | `▁이런` | `▁성취감이` | 75.0 | 75.0 | 0.0 | Tie |
| ko_ending_question | plain | `▁잘하면` | `▁성취감이` | 75.0 | 75.0 | 0.0 | Tie |
| ko_particle_short | dialogue-ko | `<0x63>` | `▁석회` | 70.0 | 75.0 | 5.0 | Assembled |
| ko_particle_short | instruction-ko | `▁그때까지만` | `▁석회` | 75.0 | 75.0 | 0.0 | Tie |
| ko_particle_short | plain | `▁무용` | `▁석회` | 75.0 | 75.0 | 0.0 | Tie |
| wrapper_assistant_label | dialogue-ko | `라도` | `라도` | 100.0 | 100.0 | 0.0 | Tie |
| wrapper_assistant_label | instruction-ko | `라도` | `라도` | 100.0 | 100.0 | 0.0 | Tie |
| wrapper_assistant_label | plain | `▁효과적으로` | `▁효과적으로` | 75.0 | 75.0 | 0.0 | Tie |
| wrapper_user_label | dialogue-ko | `<0x63>` | `<0x63>` | 70.0 | 70.0 | 0.0 | Tie |
| wrapper_user_label | instruction-ko | `<0x63>` | `<0x63>` | 70.0 | 70.0 | 0.0 | Tie |
| wrapper_user_label | plain | `<0x63>` | `<0x63>` | 70.0 | 70.0 | 0.0 | Tie |

## 5. 확정

- baseline/assembled branch-local generation comparison was executed.
- default commit remains false.
- assembled ids were not globally committed.

## 6. 판단불가

- default commit safety.
- long-form generation stability.
- production default wrapper policy.
