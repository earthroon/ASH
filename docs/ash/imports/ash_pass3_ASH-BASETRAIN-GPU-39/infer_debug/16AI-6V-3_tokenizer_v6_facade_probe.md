# 16AI-6V-3 V6 Runtime Encoder Facade Probe

## 1. Scope

| field | value |
|---|---|
| generation | false |
| checkpoint_required | false |
| gpu_execution | false |
| global_default_commit | false |
| token_ids_mutated | false |
| vocab_augmented | false |

## 2. Summary

| field | value |
|---|---:|
| case_count | 2 |
| mode_count | 4 |
| encode_results | 8 |
| branch_local_commit_count | 4 |
| fallback_count | 4 |
| vocab_violation_count | 0 |
| acceptance_status | PASS_TOKENIZER_V6_FACADE |

## 3. Mode Table

| case | mode | committed_source | baseline_len | assembled_len | committed_len | fallback |
|---|---|---|---:|---:|---:|---|
| ko_descriptive_sentence | v5-baseline | V5Baseline | 24 | 24 | 24 | RuntimeModeBaseline |
| ko_descriptive_sentence | v6-shadow | V6AssembledShadowOnly | 24 | 24 | 24 | ShadowModeDoesNotCommit |
| ko_descriptive_sentence | v6-branch-local | V6AssembledBranchLocal | 24 | 24 | 24 | none |
| ko_descriptive_sentence | v6-gpu-shadow | V6AssembledBranchLocal | 24 | 24 | 24 | none |
| ko_particle_short | v5-baseline | V5Baseline | 18 | 18 | 18 | RuntimeModeBaseline |
| ko_particle_short | v6-shadow | V6AssembledShadowOnly | 18 | 18 | 18 | ShadowModeDoesNotCommit |
| ko_particle_short | v6-branch-local | V6AssembledBranchLocal | 18 | 18 | 18 | none |
| ko_particle_short | v6-gpu-shadow | V6AssembledBranchLocal | 18 | 18 | 18 | none |

## 5. 확정

- v6 facade probe output generated.
- generation/GPU execution/checkpoint loading are not performed in V3.
- no token/vocab/embedding mutation is allowed.

## 6. 판단불가

- generation quality.
- GPU runtime parity.
- v6 default tokenizer safety.
