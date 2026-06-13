# 16AI-6V-5-R3 Acceptance

## Status

PASS_DECODER_OUTPUT_SANITY_GATE

## Meaning

PASS_DECODER_OUTPUT_SANITY_GATE means byte-like output was detected, raw output was preserved, and unsafe display was blocked. It does not mean the output is clean.

## Summary

- case_count: 2
- byte_leak_detected_count: 2
- blocked_output_count: 2
- branch_local_not_causal_count: 2
- v6_leak_regression_count: 0
- raw_output_preserved_count: 2
- output_mutated_count: 0

## Contract

- generation=false
- gpu_execution=false
- global_default_commit=false
- gpu_default=false
- raw_output_preserved=true
- output_mutated=false
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false
- embedding_resize_required=false
