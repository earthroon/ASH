# 16AI-6W-5 Controlled Suppression Replay

## Status

PASS_CONTROLLED_SUPPRESSION_REPLAY

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| run_count | 8 |
| horizon_2_count | 4 |
| horizon_8_count | 4 |
| controlled_replay_pass_count | 4 |
| pass_with_risk_tracking_count | 4 |
| weak_quality_count | 0 |
| rejected_count | 0 |
| byte_leak_count | 0 |
| special_marker_leak_count | 0 |
| wrapper_echo_count | 0 |
| output_mutated_count | 0 |
| sampler_mutated_count | 0 |
| runtime_default_committed_count | 0 |

## Controlled Replay Table

| case | mode | horizon | candidate | text | byte_leak | quality | decision |
|---|---|---:|---|---|---:|---:|---|
| ko_descriptive_sentence | v5-baseline | 2 | ▁양념치킨 | 양념치킨 | false | 83 | ControlledReplayPassWithRiskTracking |
| ko_descriptive_sentence | v5-baseline | 8 | ▁양념치킨 | 양념치킨 ... | false | 82 | ControlledReplayPassWithRiskTracking |
| ko_descriptive_sentence | v6-branch-local | 2 | ▁양념치킨 | 양념치킨 | false | 83 | ControlledReplayPassWithRiskTracking |
| ko_descriptive_sentence | v6-branch-local | 8 | ▁양념치킨 | 양념치킨 ... | false | 82 | ControlledReplayPassWithRiskTracking |
| ko_particle_short | v5-baseline | 2 | 라도 | 라도 | false | 88 | ControlledReplayPass |
| ko_particle_short | v5-baseline | 8 | 라도 | 라도 ... | false | 87 | ControlledReplayPass |
| ko_particle_short | v6-branch-local | 2 | 라도 | 라도 | false | 88 | ControlledReplayPass |
| ko_particle_short | v6-branch-local | 8 | 라도 | 라도 ... | false | 87 | ControlledReplayPass |

## Contract

- controlled_replay_only=true
- default_sampler_mutated=false
- output_mutated=false
- runtime_default_committed=false
