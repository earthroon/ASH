# ASH-FT-35 Training Sample Window / Sequence Pack Builder Seal

## SSOT

ASH-FT-35 consumes the ASH-FT-34 frozen-tokenizer encode cache and builds deterministic training sequence windows while preserving train/valid split and sample provenance.

## Scope

Allowed:
- Read ASH-FT-34 receipt, encode cache manifest, sample index, split encode registry, and tokenizer binding receipt.
- Read encode cache shards.
- Build deterministic fixed-length sequence windows.
- Write sequence pack shards, sequence pack manifest, sequence sample index, stats, field boundary map, and split sequence registry.
- Create label shift candidates and attention mask candidates.

Forbidden:
- Loss objective finalization.
- ignore_index finalization.
- target-only loss finalization.
- tokenizer mutation.
- corpus mutation.
- encode cache source mutation.
- model forward, backward, training, optimizer step, weight update.
- shadow route, delta packet, runtime apply, alias rebind, promotion.

## Expected verdict

`PASS_ASH_FT35_TRAINING_SAMPLE_WINDOW_SEQUENCE_PACK_BUILDER`

## Blocked states

- `BLOCKED_ASH_FT35_MISSING_FT34_RECEIPT`
- `BLOCKED_ASH_FT35_FT34_NOT_PASS`
- `BLOCKED_ASH_FT35_ENCODE_CACHE_MANIFEST_MISSING`
- `BLOCKED_ASH_FT35_ENCODE_CACHE_SHARD_MISSING`
- `BLOCKED_ASH_FT35_ENCODE_SAMPLE_INDEX_MISSING`
- `BLOCKED_ASH_FT35_SPLIT_ENCODE_REGISTRY_MISSING`
- `BLOCKED_ASH_FT35_EMPTY_ENCODED_SAMPLE_SET`
- `BLOCKED_ASH_FT35_INVALID_WINDOW_POLICY`
- `BLOCKED_ASH_FT35_INVALID_SEQUENCE_LENGTH`
- `BLOCKED_ASH_FT35_INVALID_STRIDE`
- `BLOCKED_ASH_FT35_ALL_SAMPLES_TOO_SHORT`
- `BLOCKED_ASH_FT35_SEQUENCE_PACK_WRITE_FAILED`
- `BLOCKED_ASH_FT35_SPLIT_PRESERVATION_FAILED`

## Next

ASH-FT-36 — Loss Objective Contract / Subtitle Causal LM Target Seal.
