# 16AI-6V-0 Acceptance — Tokenizer V6 Compat SSOT Seal

## Status

`PASS_TOKENIZER_V6_COMPAT_SSOT`

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

## Required Contract

| field | value |
|---|---|
| v6_type | checkpoint-compatible runtime tokenizer |
| base_tokenizer_version | v5 |
| target_tokenizer_version | v6-compat |
| vocab_size | 48259 |
| fallback_to_v5 | true |
| default_mode | v5-baseline |
| global_default_commit | false |
| gpu_default | false |
| cpu_fallback | true |

## Verified Gates Recorded

- 16AI-6E-R4 PASS_DELTA_REPORT
- 16AI-6E-R5 PASS_COVERAGE_REPORT
- 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY
- 16AI-6G PASS_QUALITY_RECOMPARE
- 16AI-6H-R2 PASS_POLICY_QUALITY_INTEGRATED
- 16AI-6I PASS_GATED_COMMIT_PROBE
- 16AI-6J PASS_GPU_SHADOW_PARITY
- 16AI-6J-R2 PASS_GPU_SHADOW_REPLAY8

## Guardrails

- V6 is not a vocab expansion.
- V6 does not create new token IDs.
- V6 does not require embedding resize.
- V6 does not rewrite the checkpoint.
- V6 does not make GPU default.
- V6 does not treat PENDING_RUNTIME as PASS.
