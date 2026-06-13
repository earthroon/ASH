# 16AI-6E-R4 Assembly Delta Report

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| input_json | `infer_debug/16AI-6E_dp_token_path_probe.json` |
| source_gate | 16AI-6E-R3 PASS_RUNTIME_PROBE |

## 2. Scope

| field | value |
|---|---|
| delta_mode | report_only |
| generation | false |
| token_ids_mutated | false |
| committed_prompt_ids | baseline |
| assembled_ids_not_committed | true |

## 3. Field Status

| field | value |
|---|---|
| acceptance_status | PASS_DELTA_REPORT |
| required_delta_fields_complete | true |
| delta_fields_present | true |
| complete_results | 21 |
| partial_results | 0 |
| missing_required_fields | `` |
| missing_recommended_fields | `` |
| missing_fields | `` |
| delta_status | PASS_DELTA_FIELDS |

## 4. Summary

| field | value |
|---|---:|
| total | 21 |
| completed | 21 |
| failed | 0 |
| improved_count | 14 |
| unchanged_count | 7 |
| worsened_count | 0 |
| avg_baseline_fragmentation_score | 55.95238095238095 |
| avg_assembled_fragmentation_score | 8.571428571428571 |
| avg_fragmentation_delta | 47.38095238095238 |
| avg_token_len_delta | -8.047619047619047 |
| avg_path_score | 71.42857142857143 |
| field_complete_count | 21 |
| field_partial_count | 0 |
| missing_required_field_count | 0 |
| missing_recommended_field_count | 0 |

## 5. Wrapper Delta Table

| wrapper | cases | improved | unchanged | worsened | avg_delta | avg_path_score |
|---|---:|---:|---:|---:|---:|---:|
| dialogue-ko | 7 | 5 | 2 | 0 | 50.000 | 71.429 |
| instruction-ko | 7 | 5 | 2 | 0 | 50.000 | 71.429 |
| plain | 7 | 4 | 3 | 0 | 42.143 | 71.429 |

## 6. Case Delta Table

| case | wrapper | baseline_frag | assembled_frag | delta | token_len_delta | path_score | protected_only | class |
|---|---|---:|---:|---:|---:|---:|---:|---|
| ko_beetle_question | plain | 80.000 | 0.000 | 80.000 | -8 | 100.000 | false | improved |
| ko_beetle_question | dialogue-ko | 80.000 | 0.000 | 80.000 | -20 | 100.000 | false | improved |
| ko_beetle_question | instruction-ko | 80.000 | 0.000 | 80.000 | -16 | 100.000 | false | improved |
| ko_particle_short | plain | 80.000 | 0.000 | 80.000 | -3 | 100.000 | false | improved |
| ko_particle_short | dialogue-ko | 80.000 | 0.000 | 80.000 | -15 | 100.000 | false | improved |
| ko_particle_short | instruction-ko | 80.000 | 0.000 | 80.000 | -11 | 100.000 | false | improved |
| ko_ending_question | plain | 0.000 | 0.000 | 0.000 | -1 | 100.000 | false | unchanged |
| ko_ending_question | dialogue-ko | 30.000 | 0.000 | 30.000 | -13 | 100.000 | false | improved |
| ko_ending_question | instruction-ko | 30.000 | 0.000 | 30.000 | -9 | 100.000 | false | improved |
| ko_compound_noun | plain | 55.000 | 0.000 | 55.000 | -5 | 100.000 | false | improved |
| ko_compound_noun | dialogue-ko | 80.000 | 0.000 | 80.000 | -17 | 100.000 | false | improved |
| ko_compound_noun | instruction-ko | 80.000 | 0.000 | 80.000 | -13 | 100.000 | false | improved |
| ko_descriptive_sentence | plain | 80.000 | 0.000 | 80.000 | -6 | 100.000 | false | improved |
| ko_descriptive_sentence | dialogue-ko | 80.000 | 0.000 | 80.000 | -18 | 100.000 | false | improved |
| ko_descriptive_sentence | instruction-ko | 80.000 | 0.000 | 80.000 | -14 | 100.000 | false | improved |
| wrapper_user_label | plain | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |
| wrapper_user_label | dialogue-ko | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |
| wrapper_user_label | instruction-ko | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |
| wrapper_assistant_label | plain | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |
| wrapper_assistant_label | dialogue-ko | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |
| wrapper_assistant_label | instruction-ko | 30.000 | 30.000 | 0.000 | 0 | 0.000 | true | unchanged |

## 7. Confirmed

- R3 runtime pass is checked through the source acceptance and 6E JSON gate.
- generation=false, token_ids_mutated=false, committed_prompt_ids=baseline are preserved.
- Required delta fields are evaluated separately from recommended fields.
- Protected-only cases are allowed to have path_score=0 and delta=0 without forcing PARTIAL.

## 8. Inference

- A high avg_fragmentation_delta wrapper is only an assembly-delta candidate, not a generation best_wrapper.

## 9. Unknown

- generation quality improvement
- actual commit safety
- CPU/native parity effect
- final best_wrapper
