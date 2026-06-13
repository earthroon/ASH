# 16AI-6V-3 V6 Runtime Encoder Facade

## Identity

16AI-6V-3 adds a checkpoint-compatible tokenizer facade for AshTokenizerV6Compat.

The facade preserves tokenizer v5 baseline IDs while exposing v6 assembled candidate IDs and mode-based committed IDs.

## Runtime Modes

- `v5-baseline`: commit baseline ids.
- `v6-shadow`: generate assembled ids, commit baseline ids.
- `v6-branch-local`: commit assembled ids only for policy-approved dialogue-ko cases.
- `v6-policy-gated`: policy-gated branch-local mode, still default-off.
- `v6-gpu-shadow`: encode metadata for GPU shadow path, no GPU execution in V3.

## Non-Mutation Contract

- token_ids_mutated=false
- new_token_ids_created=false
- vocab_augmented=false
- embedding_resize_required=false
- global_default_commit=false

## Non-Goals

- No generation.
- No checkpoint loading.
- No GPU execution.
- No v5 manifest mutation.
- No vocab/token-id mutation.
