# 16AI-6W-2 Byte Token Suppression Candidate Gate

## Purpose

Record suppression candidates for byte-like top-1 output without mutating the raw output, sampler, tokenizer, vocab, or checkpoint.

## Contract

- raw selected token is preserved.
- output_mutated=false.
- sampler_mutated=false.
- global_default_commit=false.
- gpu_default=false.
- new_token_ids_created=false.
- embedding_resize_required=false.

## Source Gates

- 16AI-6W-1 PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION
- 16AI-6V-5-R3 PASS_DECODER_OUTPUT_SANITY_GATE
- ModelCommonByteBias evidence present

## Output

- infer_debug/16AI-6W-2_byte_token_suppression_candidate_gate.json
- infer_debug/16AI-6W-2_byte_token_suppression_candidate_gate.md
- acceptance_reports/16AI-6W-2_acceptance_PENDING_OR_PASS_SUPPRESSION_CANDIDATE.md
