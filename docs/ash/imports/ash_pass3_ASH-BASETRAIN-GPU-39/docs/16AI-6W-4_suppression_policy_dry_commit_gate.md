# 16AI-6W-4 Suppression Policy Dry Commit Gate

## Purpose

Qualify 16AI-6W-3 dry-run suppression candidates for a later controlled suppression replay without mutating the output, sampler, runtime commit state, tokenizer, vocabulary, or checkpoint.

## Source gates

- 16AI-6W-3: `PASS_SUPPRESSION_DRY_RUN_REPLAY`
- 16AI-6W-2: `PASS_BYTE_TOKEN_SUPPRESSION_CANDIDATE_GATE`
- 16AI-6W-1: `PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION`
- 16AI-6V-5-R3: `PASS_DECODER_OUTPUT_SANITY_GATE`

## Contract

- `generation=false`
- `checkpoint_required=false`
- `gpu_execution=false`
- `dry_commit_gate_only=true`
- `global_default_commit=false`
- `gpu_default=false`
- `output_mutated=false`
- `sampler_mutated=false`
- `runtime_committed=false`
- `new_token_ids_created=false`
- `vocab_augmented=false`
- `embedding_resize_required=false`

## Eligibility

A record is dry-commit eligible only when:

- raw selected token is byte-like and equals `<0x63>`
- candidate exists
- candidate is not byte-like, special marker, or wrapper echo
- dry-run decision is `SuppressionDryRunPass`
- candidate quality is at least `80.0`
- margin to raw token is at most `3.0`
- output, sampler, and runtime commit states remain unmodified

## Risk levels

- Low: quality >= 85.0 and margin <= 1.0
- Medium: quality >= 80.0 and margin <= 3.0
- High: candidate exists but is weak or suspicious
- Rejected: leak, marker echo, mutation, runtime commit, or failed dry-run

## Next step

If W4 passes, continue to `16AI-6W-5 Controlled Suppression Replay`.
