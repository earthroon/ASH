# 16AI-6J-R2 GPU Shadow Replay8 / max_new_tokens=8

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_gated_commit | 16AI-6I PASS_GATED_COMMIT_PROBE |
| source_policy_gate | 16AI-6H-R2 PASS_POLICY_QUALITY_INTEGRATED |

## 2. Scope

| field | value |
|---|---|
| gpu_execution_mode | gpu-shadow |
| cpu_reference | true |
| gpu_native | true |
| cpu_fallback | true |
| gpu_default | false |
| global_default_commit | false |
| branch_local_commit | true |
| max_new_tokens | 8 |

## 3. Summary

| field | value |
|---|---:|
| eligible_cases | 2 |
| cpu_success_count | 2 |
| gpu_success_count | 2 |
| exact_8_parity_count | 2 |
| quality_equivalent_count | 0 |
| gpu_error_count | 0 |
| leak_count | 0 |
| status | "PASS_GPU_SHADOW_REPLAY8" |

## 4. 확정

- CPU/GPU shadow parity gate was executed.
- CPU fallback remains true.
- GPU default remains false.
- Global default commit remains false.

## 5. 판단불가

- GPU default safety.
- Long-form GPU stability.
- Full matrix GPU stability.
