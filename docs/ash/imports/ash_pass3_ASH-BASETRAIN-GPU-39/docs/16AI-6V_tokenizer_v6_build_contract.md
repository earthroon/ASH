# 16AI-6V Tokenizer V6 Build Contract

## Contract Summary

Tokenizer V6 Compat is a checkpoint-compatible runtime tokenizer profile for Ash 1.1B. It preserves tokenizer v5 vocabulary and token IDs while packaging the 16AI-6 assembly, policy, branch-local commit, and GPU shadow verification line into a single versioned runtime identity.

## Must Preserve

- `base_tokenizer_version = v5`
- `vocab_size = 48259`
- `token_id_table_mutated = false`
- `new_token_ids_created = false`
- `vocab_augmented = false`
- `embedding_resize_required = false`
- `checkpoint_rewrite_required = false`
- `fallback_to_v5 = true`
- `default_mode = v5-baseline`
- `global_default_commit = false`
- `gpu_default = false`
- `cpu_fallback = true`

## May Add

- v6 compat manifest
- v6 audit probe
- v6 encoder facade
- protected span scanner binding
- Cheonjiin structural analyzer binding
- existing vocab lookup lattice binding
- DP best token path assembler binding
- quality policy gate binding
- branch-local commit selector binding
- GPU shadow backend metadata

## Must Not Add In V0

- new tokenizer vocab
- new token IDs
- embedding resize
- checkpoint rewrite
- generation execution
- GPU execution
- DPO training
- default tokenizer switch

## Gate Chain To Preserve

1. 16AI-6E-R4 PASS_DELTA_REPORT
2. 16AI-6E-R5 PASS_COVERAGE_REPORT
3. 16AI-6F PASS_COMMIT_GATE_COMPARE_ONLY
4. 16AI-6G PASS_QUALITY_RECOMPARE
5. 16AI-6H-R2 PASS_POLICY_QUALITY_INTEGRATED
6. 16AI-6I PASS_GATED_COMMIT_PROBE
7. 16AI-6J PASS_GPU_SHADOW_PARITY
8. 16AI-6J-R2 PASS_GPU_SHADOW_REPLAY8
