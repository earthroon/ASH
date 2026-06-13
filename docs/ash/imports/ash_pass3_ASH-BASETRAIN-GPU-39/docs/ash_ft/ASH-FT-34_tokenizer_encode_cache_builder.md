# ASH-FT-34 Tokenizer Encode Cache Builder / Frozen Tokenizer Seal

## SSOT

ASH-FT-34 reads the ASH-FT-33 training corpus registry and encodes existing samples into deterministic JSONL token-id cache shards using the frozen tokenizer manifest. It must not mutate tokenizer vocab, tokenizer manifest, special token ids, corpus sources, model weights, optimizer state, shadow artifacts, runtime aliases, or promotion state.

## Boundary

Allowed:
- Read ASH-FT-33 receipt, corpus inventory, schema, split registry, corpus hash manifest.
- Read frozen tokenizer manifest and vocab.
- Encode existing samples only.
- Write encode cache shards, encode cache manifest, sample index, stats, and split encode registry.

Forbidden:
- Tokenizer mutation.
- Vocab expansion.
- Special token invention or remap.
- Model forward, backward, training, optimizer step, weight update.
- Shadow route, delta packet, runtime apply, alias rebind, promotion.

## Expected verdict

`PASS_ASH_FT34_TOKENIZER_ENCODE_CACHE_BUILDER_FROZEN_TOKENIZER`

## Blocked states

- `BLOCKED_ASH_FT34_MISSING_FT33_RECEIPT`
- `BLOCKED_ASH_FT34_FT33_NOT_PASS`
- `BLOCKED_ASH_FT34_CORPUS_INVENTORY_MISSING`
- `BLOCKED_ASH_FT34_CORPUS_SCHEMA_INVALID`
- `BLOCKED_ASH_FT34_EMPTY_SAMPLE_SET`
- `BLOCKED_ASH_FT34_TOKENIZER_MANIFEST_MISSING`
- `BLOCKED_ASH_FT34_TOKENIZER_VOCAB_MISSING`
- `BLOCKED_ASH_FT34_TOKENIZER_RUNTIME_UNAVAILABLE`
- `BLOCKED_ASH_FT34_TOKENIZER_HASH_MISMATCH`
- `BLOCKED_ASH_FT34_ALL_SAMPLES_ENCODE_FAILED`
- `BLOCKED_ASH_FT34_ENCODE_CACHE_WRITE_FAILED`
- `BLOCKED_ASH_FT34_SPLIT_REGISTRY_MISSING`

## Next

ASH-FT-35 — Training Sample Window / Sequence Pack Builder Seal.
