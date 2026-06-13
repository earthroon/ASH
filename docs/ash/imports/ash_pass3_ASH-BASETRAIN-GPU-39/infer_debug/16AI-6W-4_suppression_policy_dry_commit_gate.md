# 16AI-6W-4 Suppression Policy Dry Commit Gate

## Status

PASS_SUPPRESSION_POLICY_DRY_COMMIT_GATE

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| run_count | 4 |
| eligible_count | 4 |
| ineligible_count | 0 |
| low_risk_count | 2 |
| medium_risk_count | 2 |
| high_risk_count | 0 |
| rejected_count | 0 |
| both_eligible_pair_count | 2 |
| same_candidate_pair_count | 2 |
| output_mutated_count | 0 |
| sampler_mutated_count | 0 |
| runtime_committed_count | 0 |

## Gate Table

| case | mode | candidate | quality | margin | eligible | risk |
|---|---|---|---:|---:|---:|---|
| ko_descriptive_sentence | v5-baseline | `▁양념치킨` | 84.0 | 1.2655911445617676 | true | Medium |
| ko_descriptive_sentence | v6-branch-local | `▁양념치킨` | 84.0 | 1.2655911445617676 | true | Medium |
| ko_particle_short | v5-baseline | `라도` | 88.0 | 0.8470816612243652 | true | Low |
| ko_particle_short | v6-branch-local | `라도` | 88.0 | 0.8470816612243652 | true | Low |

## 확정

- Dry-run candidates were evaluated for dry commit eligibility.
- output_mutated=false, sampler_mutated=false, runtime_committed=false.
- This report does not apply suppression to runtime generation.

## 판단불가

- Whether controlled suppression replay remains stable for 2/8/16 token continuations.
- Whether the candidate improves real output quality after sampler integration.
