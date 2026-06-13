# 16AI-6V-5 Acceptance

## Status

PARTIAL_TOKENIZER_V6_BRANCH_LOCAL_REPLAY

## Summary

- approved_case_count: 2
- replay_case_count: 2
- branch_local_commit_applied_count: 2
- baseline_fallback_count: 0
- global_commit_applied_count: 0
- generation_success_count: 2
- generation_fail_count: 0
- quality_worsened_count: 0
- leak_count: 2
- vocab_violation_count: 0

## Runtime Output Writer

- writer_fix: 16AI-6V-5-R2
- console_file_seal_sync: true
- pending_runtime_forbidden_after_execution: true
- leak_count_preserved: 2

## Partial Meaning

PARTIAL means branch-local replay structure passed, but leak_count > 0 blocked full PASS. The leak is preserved for V5-R1 triage and must not be hidden, deleted, or silently sanitized.

## Contract

- generation=true
- gpu_execution=false
- global_default_commit=false
- gpu_default=false
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false
- embedding_resize_required=false
