# 16AI-6V-1 Acceptance

## Status

PASS_TOKENIZER_V6_COMPAT_MANIFEST

## Required Contract

| field | expected |
|---|---|
| tokenizer_version | v6-compat |
| base_tokenizer_version | v5 |
| base_manifest | artifacts/tokenizer_manifest_v5_final.json |
| vocab_size | 48259 |
| checkpoint_compatible | true |
| token_id_table_mutated | false |
| new_token_ids_created | false |
| vocab_augmented | false |
| embedding_resize_required | false |
| checkpoint_rewrite_required | false |
| default_mode | v5-baseline |
| fallback_to_v5 | true |
| global_default_commit | false |
| gpu_default | false |
| cpu_fallback | true |
| pending_manifest_is_not_runtime_pass | true |

## Non-Goals

- no generation
- no checkpoint load
- no GPU execution
- no vocab mutation
- no token id creation
- no embedding resize
- no runtime default change

## Seal

V6 compat manifest is a runtime profile declaration, not a new vocabulary or checkpoint rewrite.
