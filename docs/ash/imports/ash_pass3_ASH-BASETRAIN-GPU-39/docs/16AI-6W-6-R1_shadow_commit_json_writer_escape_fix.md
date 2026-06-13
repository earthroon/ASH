# 16AI-6W-6-R1 Shadow Commit JSON Writer Escape Fix

## Purpose

Fixes the 16AI-6W-6 JSON writer so Korean candidate pieces such as `▁양념치킨` and `라도` are emitted as ASCII-safe JSON unicode escapes.

## Scope

- Fixes only `write_json` in `af16ai6w6_suppression_policy_shadow_commit.rs`.
- Keeps W6 policy logic unchanged.
- Keeps shadow-only/default runtime disabled contracts unchanged.
- Prevents PowerShell `ConvertFrom-Json` failures caused by non-UTF8/default encoding reads.

## Contract

- `shadow_policy_commit=true`
- `activation_mode=shadow-only`
- `default_runtime_enabled=false`
- `default_sampler_mutated=false`
- `output_mutated=false`
- `runtime_default_committed=false`
- `token_ids_mutated=false`
- `vocab_augmented=false`
- `new_token_ids_created=false`
- `embedding_resize_required=false`
