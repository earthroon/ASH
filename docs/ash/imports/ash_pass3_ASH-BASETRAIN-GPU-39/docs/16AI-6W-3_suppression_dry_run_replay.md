# 16AI-6W-3 Suppression Dry-Run Replay

Dry-run probe for byte token suppression candidates.

## Contract

- Preserve `raw_selected_token_id` and `raw_selected_piece`.
- Record candidate preview in `dry_run_text` only.
- Keep `output_mutated=false`, `sampler_mutated=false`, and `runtime_committed=false`.
- Do not change vocab, token IDs, embeddings, checkpoint, sampler, or runtime defaults.

## Expected source gates

- 16AI-6W-2: `PASS_BYTE_TOKEN_SUPPRESSION_CANDIDATE_GATE`
- 16AI-6W-1: `PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION`
- 16AI-6V-5-R3: `PASS_DECODER_OUTPUT_SANITY_GATE`
