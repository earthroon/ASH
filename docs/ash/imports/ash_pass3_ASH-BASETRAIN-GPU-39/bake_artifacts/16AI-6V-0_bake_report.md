# 16AI-6V-0 Tokenizer V6 Compat SSOT Seal Bake Report

## 확정

16AI-6V-0 기준 봉인 산출물을 생성했다.

- `docs/16AI-6V-0_tokenizer_v6_compat_ssot.md`
- `docs/16AI-6V_tokenizer_v6_build_contract.md`
- `infer_debug/16AI-6V-0_tokenizer_v6_compat_ssot.json`
- `acceptance_reports/16AI-6V-0_acceptance_PENDING_OR_PASS_SSOT.md`

## Scope

| field | value |
|---|---|
| generation | false |
| checkpoint_required | false |
| manifest_created | false |
| runtime_changed | false |
| token_ids_mutated | false |
| vocab_augmented | false |
| new_token_ids_created | false |
| embedding_resize_required | false |

## V6 Identity

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| base_tokenizer_version | v5 |
| target_tokenizer_version | v6-compat |
| v6_type | checkpoint-compatible runtime tokenizer |
| vocab_size | 48259 |
| default_mode | v5-baseline |
| fallback_to_v5 | true |

## GPU Contract

| field | value |
|---|---|
| gpu_shadow_supported | true |
| gpu_shadow_parity_1_verified | true |
| gpu_shadow_replay8_verified | true |
| gpu_default | false |
| cpu_fallback | true |
| max_verified_new_tokens | 8 |

## 판단불가

- v6 default tokenizer 안전성
- gpu_default 안전성
- 16토큰 이상 장문 안정성
- 전체 matrix 안정성
- DPO 학습 효과
