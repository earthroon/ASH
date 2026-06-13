# 16AI-6W-7 Shadow Policy Expansion Probe

## Status

PASS_SHADOW_POLICY_EXPANSION_PROBE

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| policy_count | 2 |
| shadow_policy_hit_count | 2 |
| expansion_candidate_count | 2 |
| low_risk_expansion_count | 1 |
| medium_risk_expansion_count | 1 |
| high_risk_count | 0 |
| rejected_count | 0 |
| risk_tracking_required_count | 1 |
| horizon_8_required_count | 2 |
| horizon_16_required_count | 2 |
| default_runtime_enabled_count | 0 |
| default_sampler_mutated_count | 0 |
| output_mutated_count | 0 |
| runtime_default_committed_count | 0 |

## Expansion Table

| case | raw | candidate | risk | tracking | eligible | route |
|---|---|---|---|---:|---:|---|
| ko_descriptive_sentence | <0x63> | ▁양념치킨 | Medium | true | true | medium_risk_shadow_expansion_with_tracking |
| ko_particle_short | <0x63> | 라도 | Low | false | true | low_risk_shadow_expansion |

## Contract

- expansion_mode=shadow-expansion-only
- default_runtime_enabled=false
- default_sampler_mutated=false
- runtime_default_committed=false
