# 16AI-6W-6 Suppression Policy Shadow Commit

## Status

PASS_SUPPRESSION_POLICY_SHADOW_COMMIT

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| policy_count | 2 |
| shadow_registered_count | 2 |
| low_risk_count | 1 |
| medium_risk_count | 1 |
| high_risk_count | 0 |
| rejected_count | 0 |
| risk_tracking_required_count | 1 |
| default_runtime_enabled_count | 0 |
| default_sampler_mutated_count | 0 |
| output_mutated_count | 0 |
| runtime_default_committed_count | 0 |

## Policy Table

| case | raw | candidate | risk | tracking | activation | registered |
|---|---|---|---|---:|---|---:|
| ko_descriptive_sentence | <0x63> | ▁양념치킨 | Medium | true | shadow-only | true |
| ko_particle_short | <0x63> | 라도 | Low | false | shadow-only | true |

## Contract

- activation_mode=shadow-only
- default_runtime_enabled=false
- default_sampler_mutated=false
- runtime_default_committed=false
