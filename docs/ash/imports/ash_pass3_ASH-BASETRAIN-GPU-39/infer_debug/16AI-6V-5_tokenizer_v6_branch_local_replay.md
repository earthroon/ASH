# 16AI-6V-5 V6 Branch-Local Replay

## Status

PARTIAL_TOKENIZER_V6_BRANCH_LOCAL_REPLAY

## Scope

| field | value |
|---|---|
| generation | true |
| checkpoint_required | true |
| gpu_execution | false |
| runtime_mode | v6-branch-local |
| global_default_commit | false |
| gpu_default | false |
| branch_local_commit | true |

## Summary

| field | value |
|---|---:|
| approved_case_count | 2 |
| replay_case_count | 2 |
| branch_local_commit_applied_count | 2 |
| baseline_fallback_count | 0 |
| global_commit_applied_count | 0 |
| generation_success_count | 2 |
| generation_fail_count | 0 |
| quality_worsened_count | 0 |
| leak_count | 2 |
| vocab_violation_count | 0 |

## Leak Summary

| field | value |
|---|---:|
| leak_count | 2 |
| byte_like_output_preserved | true |

## Runtime Output Writer

| field | value |
|---|---|
| writer_fix | 16AI-6V-5-R2 |
| console_file_seal_sync | true |
| pending_runtime_forbidden_after_execution | true |

## Replay Table

| case | wrapper | committed_source | baseline_len | assembled_len | committed_len | new_text | quality |
|---|---|---|---:|---:|---:|---|---:|
| ko_descriptive_sentence | dialogue-ko | V6AssembledBranchLocal | 24 | 24 | 24 | `<0x63>` | 70.000 |
| ko_particle_short | dialogue-ko | V6AssembledBranchLocal | 18 | 18 | 18 | `<0x63>` | 70.000 |

## 확정

- v6 policy registry was read.
- Approved branch-local cases were replayed only through v6-branch-local mode.
- Generation was performed on CPU reference; GPU execution remains disabled.
- Global default commit and GPU default remain disabled.
- Token/vocab/checkpoint mutation remains disabled.

## 판단불가

- v6 default tokenizer safety.
- broader dialogue-ko matrix stability.
- DPO export quality.
