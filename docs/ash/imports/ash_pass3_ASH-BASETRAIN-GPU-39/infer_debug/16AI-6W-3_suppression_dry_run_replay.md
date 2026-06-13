# 16AI-6W-3 Suppression Dry-Run Replay

## Status

PASS_SUPPRESSION_DRY_RUN_REPLAY

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| run_count | 4 |
| raw_byte_top1_count | 4 |
| candidate_available_count | 4 |
| candidate_clean_count | 4 |
| korean_candidate_count | 4 |
| strong_candidate_count | 2 |
| usable_candidate_count | 2 |
| weak_candidate_count | 0 |
| dry_run_pass_count | 4 |
| weak_quality_count | 0 |
| rejected_count | 0 |
| retry_or_abort_preferred_count | 0 |
| output_mutated_count | 0 |
| sampler_mutated_count | 0 |
| runtime_committed_count | 0 |

## Dry-Run Table

| case | mode | raw_piece | candidate_piece | margin | dry_run_text | quality | decision |
|---|---|---|---|---:|---|---:|---|
| ko_descriptive_sentence | v5-baseline | `<0x63>` | `▁양념치킨` | 1.2655911445617676 | `▁양념치킨` | 84.0 | SuppressionDryRunPass |
| ko_descriptive_sentence | v6-branch-local | `<0x63>` | `▁양념치킨` | 1.2655911445617676 | `▁양념치킨` | 84.0 | SuppressionDryRunPass |
| ko_particle_short | v5-baseline | `<0x63>` | `라도` | 0.8470816612243652 | `라도` | 88.0 | SuppressionDryRunPass |
| ko_particle_short | v6-branch-local | `<0x63>` | `라도` | 0.8470816612243652 | `라도` | 88.0 | SuppressionDryRunPass |

## 확정

- Raw byte token evidence is preserved.
- Candidate is previewed only in dry_run_text.
- output_mutated=false, sampler_mutated=false, runtime_committed=false.

## 판단불가

- Whether a real sampler suppression commit improves long-form quality.
- Whether the next-token distribution remains stable after candidate substitution.
