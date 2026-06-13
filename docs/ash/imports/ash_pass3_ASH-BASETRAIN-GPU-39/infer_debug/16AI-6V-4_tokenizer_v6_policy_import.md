# 16AI-6V-4 V6 Policy Import Report

## 1. Scope

| field | value |
|---|---|
| generation | false |
| checkpoint_required | false |
| gpu_execution | false |
| registry_created | true |
| global_default_commit | false |
| gpu_default | false |

## 2. Summary

| field | value |
|---|---:|
| approved_case_count | 2 |
| branch_local_allowed_count | 2 |
| gpu_shadow_allowed_count | 2 |
| dpo_candidate_count | 2 |
| global_commit_allowed_count | 0 |
| source_gate_fail_count | 0 |
| policy_conflict_count | 0 |

## 3. Approved Cases

| case | wrapper | quality_delta | branch_local | gpu_shadow | dpo |
|---|---|---:|---:|---:|---:|
| ko_descriptive_sentence | dialogue-ko | 5.0 | true | true | true |
| ko_particle_short | dialogue-ko | 5.0 | true | true | true |

## 4. Fallback Policy

| condition | action |
|---|---|
| tie_cases | v5-baseline |
| worsened_cases | v5-baseline |
| unknown_cases | v5-baseline |
| non_dialogue_ko_wrappers | v5-baseline |
| missing_policy | v5-baseline |

## 5. Acceptance

PASS_TOKENIZER_V6_POLICY_IMPORT
