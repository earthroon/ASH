# 16AI-6V-5-R2 Acceptance

## Status

PENDING_RUNTIME

## Required Runtime Seal

PASS_BRANCH_LOCAL_REPLAY_WRITER_FIX

## Criteria

- V5 runtime output JSON is written after replay execution.
- run.kind is tokenizer_v6_branch_local_replay.
- run.acceptance_status matches the console seal.
- summary.acceptance_status matches the console seal.
- leak_count is preserved.
- PENDING_RUNTIME is absent from runtime output after execution.
- bake manifest kind is absent from runtime output after execution.

## Non-Mutation Contract

- generation=true remains unchanged.
- gpu_execution=false remains unchanged.
- global_default_commit=false remains unchanged.
- gpu_default=false remains unchanged.
- token_ids_mutated=false remains unchanged.
- vocab_augmented=false remains unchanged.
- new_token_ids_created=false remains unchanged.
- embedding_resize_required=false remains unchanged.
