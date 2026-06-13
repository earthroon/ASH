# 16AI-6V-2 Acceptance

## Status

PASS_TOKENIZER_V6_COMPAT_AUDIT

## Summary

| field | value |
|---|---:|
| total_checks | 61 |
| pass_count | 61 |
| warn_count | 0 |
| fail_count | 0 |
| blocking_fail_count | 0 |

## Required Contract

- v5 manifest exists
- v6 manifest exists
- tokenizer_version=v6-compat
- base_tokenizer_version=v5
- vocab_size=48259
- checkpoint_compatible=true
- new_token_ids_created=false
- vocab_augmented=false
- embedding_resize_required=false
- default_mode=v5-baseline
- fallback_to_v5=true
- gpu_default=false
- cpu_fallback=true
- pending_manifest_is_not_runtime_pass=true

## Scope

- generation=false
- checkpoint_required=false
- gpu_execution=false
- runtime_changed=false
