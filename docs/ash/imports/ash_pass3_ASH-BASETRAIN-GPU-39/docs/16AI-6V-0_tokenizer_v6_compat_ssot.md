# 16AI-6V-0 Tokenizer V6 Compat SSOT Seal

## 1. Identity

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| base_tokenizer_version | v5 |
| target_tokenizer_version | v6-compat |
| v6_type | checkpoint-compatible runtime tokenizer |
| vocab_size | 48259 |
| checkpoint_compatible | true |

## 2. Non-Mutation Contract

| field | value |
|---|---|
| token_id_table_mutated | false |
| new_token_ids_created | false |
| vocab_augmented | false |
| embedding_resize_required | false |
| checkpoint_rewrite_required | false |

## 3. Default Runtime Contract

| field | value |
|---|---|
| default_mode | v5-baseline |
| fallback_to_v5 | true |
| global_default_commit | false |
| branch_local_commit_supported | true |
| policy_gated_commit_supported | true |

## 4. Runtime Layers

- protected_span_scanner
- cheonjiin_structural_analyzer
- existing_vocab_lookup_lattice
- dp_best_token_path_assembler
- quality_policy_gate
- branch_local_commit_selector
- gpu_shadow_backend_gate

## 5. Verified Gates

| gate | status |
|---|---|
| 16AI-6E-R4 | PASS_DELTA_REPORT |
| 16AI-6E-R5 | PASS_COVERAGE_REPORT |
| 16AI-6F | PASS_COMMIT_GATE_COMPARE_ONLY |
| 16AI-6G | PASS_QUALITY_RECOMPARE |
| 16AI-6H-R2 | PASS_POLICY_QUALITY_INTEGRATED |
| 16AI-6I | PASS_GATED_COMMIT_PROBE |
| 16AI-6J | PASS_GPU_SHADOW_PARITY |
| 16AI-6J-R2 | PASS_GPU_SHADOW_REPLAY8 |

## 6. GPU Contract

| field | value |
|---|---|
| gpu_shadow_supported | true |
| gpu_shadow_parity_1_verified | true |
| gpu_shadow_replay8_verified | true |
| gpu_default | false |
| cpu_fallback | true |
| max_verified_new_tokens | 8 |

## 7. Runtime PASS vs Bake PENDING Contract

Tokenizer V6 Compat must never treat a bake placeholder or PENDING manifest as a runtime PASS. Runtime gates must be read from verified runtime output or from explicit invariant checks. PENDING_RUNTIME is not equivalent to PASS_GPU_SHADOW_PARITY or PASS_GPU_SHADOW_REPLAY8.

## 8. 확정

- v6는 vocab 확장 버전이 아니다.
- v6는 기존 v5 vocab/checkpoint 위에 얹는 runtime profile이다.
- 기본값은 v5-baseline이다.
- v6는 명시 옵션 또는 branch-local/policy-gated mode에서만 작동한다.
- GPU는 shadow/replay8까지 검증됐지만 default는 아니다.

## 9. 추정

- v6 manifest / audit / facade / runtime integration으로 이어질 수 있다.
- dialogue-ko policy-approved branch-local path가 v6의 1차 검증 대상이다.
- DPO 후보 export는 v6 후반 단계에서 가능하다.

## 10. 판단불가

- v6 default tokenizer 안전성
- gpu_default 안전성
- 16토큰 이상 장문 안정성
- 전체 matrix 안정성
- DPO 학습 효과
