# 16AI-6V-5-R2 Branch-Local Replay Runtime Output Writer Fix

## Purpose

Fix the 16AI-6V-5 runtime output writer so that the console seal and source-gate JSON/MD/acceptance files remain synchronized after execution.

## Contract

- generation remains true.
- gpu_execution remains false.
- global_default_commit remains false.
- gpu_default remains false.
- token_ids_mutated remains false.
- vocab_augmented remains false.
- new_token_ids_created remains false.
- embedding_resize_required remains false.
- leak_count is preserved and never hidden.

## Writer Fix

After V5 replay execution, the writer must record the runtime status in:

- infer_debug/16AI-6V-5_tokenizer_v6_branch_local_replay.json
- infer_debug/16AI-6V-5_tokenizer_v6_branch_local_replay.md
- acceptance_reports/16AI-6V-5_acceptance_PENDING_OR_PASS_BRANCH_LOCAL_REPLAY.md

The runtime output must not remain as a bake manifest with PENDING_RUNTIME.

## Expected Runtime JSON

- run.kind = tokenizer_v6_branch_local_replay
- run.writer_fix = 16AI-6V-5-R2
- run.acceptance_status = console seal status
- summary.acceptance_status = console seal status
- summary.leak_count is preserved
- runtime_output_writer.console_file_seal_sync = true
- runtime_output_writer.pending_runtime_forbidden_after_execution = true

## Non-goals

- No change to branch-local replay decision logic.
- No change to generation logic.
- No change to leak detection.
- No byte-like output sanitization.
- No GPU execution.
- No token/vocab/checkpoint mutation.
