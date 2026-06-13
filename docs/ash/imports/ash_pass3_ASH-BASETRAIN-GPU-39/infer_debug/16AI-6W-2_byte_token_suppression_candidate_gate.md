# 16AI-6W-2 Byte Token Suppression Candidate Gate

## Status

PASS_BYTE_TOKEN_SUPPRESSION_CANDIDATE_GATE

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| run_count | 4 |
| raw_byte_top1_count | 4 |
| candidate_available_count | 4 |
| korean_candidate_available_count | 4 |
| weak_margin_count | 0 |
| no_safe_candidate_count | 0 |
| model_common_byte_bias_count | 2 |
| prompt_path_influenced_count | 0 |
| output_mutated_count | 0 |
| sampler_mutated_count | 0 |

## Candidate Table

| case | mode | raw_piece | raw_id | candidate_piece | candidate_rank | margin | decision |
|---|---|---|---:|---|---:|---:|---|
| ko_descriptive_sentence | v5-baseline | `<0x63>` | 171 | `▁양념치킨` | 2 | 1.2655911445617676 | "KoreanCandidateAvailable" |
| ko_descriptive_sentence | v6-branch-local | `<0x63>` | 171 | `▁양념치킨` | 2 | 1.2655911445617676 | "KoreanCandidateAvailable" |
| ko_particle_short | v5-baseline | `<0x63>` | 171 | `라도` | 2 | 0.8470816612243652 | "KoreanCandidateAvailable" |
| ko_particle_short | v6-branch-local | `<0x63>` | 171 | `라도` | 2 | 0.8470816612243652 | "KoreanCandidateAvailable" |

## 확정

- raw byte token is preserved.
- output_mutated=false.
- sampler_mutated=false.
- candidate availability is recorded for later dry-run/retry policy.

## 판단불가

- Whether candidate replacement improves output quality.
- Whether suppression causes another abnormal token to surface.
