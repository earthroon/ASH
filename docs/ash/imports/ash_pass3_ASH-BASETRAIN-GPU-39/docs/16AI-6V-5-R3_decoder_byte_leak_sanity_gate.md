# 16AI-6V-5-R3 Decoder Byte Leak Handling / Output Sanity Gate

## Intent

16AI-6V-5-R3 adds a non-mutating decoder output sanity gate for byte-like generation leaks such as `<0x63>`.

This commit does not delete, rewrite, or hide the raw generated text. It records the raw output, classifies unsafe output as `BlockedByteLeak`, and recommends `block_output_and_retry_or_fallback`.

## Source Contract

- 16AI-6V-5-R1 must provide `PASS_BRANCH_LOCAL_LEAK_TRIAGE`.
- The source decision must be `BranchLocalNotCausal`.
- `v6_leak_regression_count` must remain `0`.

## Non-Mutation Contract

- `global_default_commit=false`
- `gpu_default=false`
- `token_ids_mutated=false`
- `vocab_augmented=false`
- `new_token_ids_created=false`
- `embedding_resize_required=false`
- `raw_output_preserved=true`
- `output_mutated=false`

## Meaning of PASS

`PASS_DECODER_OUTPUT_SANITY_GATE` does not mean the output is clean. It means the gate detected unsafe byte-like output, preserved the raw output, and blocked unsafe display/action.
