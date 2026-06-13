# 16AI-6V-5-R1 Branch-Local Byte Leak Triage

## Status

PASS_BRANCH_LOCAL_LEAK_TRIAGE

## Scope

| field | value |
|---|---|
| generation | true |
| checkpoint_required | true |
| gpu_execution | false |
| compare_modes | v5-baseline,v6-branch-local |
| max_new_tokens | 1 |
| global_default_commit | false |
| gpu_default | false |

## Summary

| field | value |
|---|---:|
| triage_case_count | 2 |
| baseline_leak_count | 2 |
| v6_leak_count | 2 |
| shared_leak_count | 2 |
| v6_only_leak_count | 0 |
| branch_local_not_causal_count | 2 |
| v6_leak_regression_count | 0 |
| leak_resolved_count | 0 |
| vocab_violation_count | 0 |

## Triage Table

| case | baseline_text | v6_text | baseline_leak | v6_leak | quality_delta | decision |
|---|---|---|---:|---:|---:|---|
| ko_descriptive_sentence | `<0x63>` | `<0x63>` | true | true | 0.000 | BranchLocalNotCausal |
| ko_particle_short | `<0x63>` | `<0x63>` | true | true | 0.000 | BranchLocalNotCausal |

## 확정

- baseline and v6 branch-local leak states were compared without hiding byte-like output.
- Leak causality decision was produced per case.
- Global default commit and GPU default remain disabled.
- Token/vocab/checkpoint mutation remains disabled.

## 판단불가

- max_new_tokens=8 leak behavior.
- GPU shadow path leak behavior.
- broader dialogue-ko stability.
