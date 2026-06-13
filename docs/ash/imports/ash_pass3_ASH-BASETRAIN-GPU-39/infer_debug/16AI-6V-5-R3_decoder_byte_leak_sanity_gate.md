# 16AI-6V-5-R3 Decoder Byte Leak Handling / Output Sanity Gate

## Status

PASS_DECODER_OUTPUT_SANITY_GATE

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| byte_leak_detected_count | 2 |
| blocked_output_count | 2 |
| pass_clean_count | 0 |
| branch_local_not_causal_count | 2 |
| v6_leak_regression_count | 0 |
| raw_output_preserved_count | 2 |
| output_mutated_count | 0 |

## Case Table

| case | raw_new_text | byte_leak | sanity_status | action | causality |
|---|---|---:|---|---|---|
| ko_descriptive_sentence | `<0x63>` | true | BlockedByteLeak | block_output_and_retry_or_fallback | BranchLocalNotCausal |
| ko_particle_short | `<0x63>` | true | BlockedByteLeak | block_output_and_retry_or_fallback | BranchLocalNotCausal |

## 확정

- byte-like output leak is detected without mutating raw output.
- BranchLocalNotCausal is preserved as the source decision.
- Output action is block_output_and_retry_or_fallback for byte leaks.
- v6 branch-local policy is not demoted by this gate.

## 판단불가

- why the byte-like token is selected top-1.
- whether RoPE/reference fidelity contributes to the leak.
- whether max_new_tokens=8 has the same pattern.
