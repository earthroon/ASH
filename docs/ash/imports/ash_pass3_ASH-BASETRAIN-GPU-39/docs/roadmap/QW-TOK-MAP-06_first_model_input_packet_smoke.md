# QW-TOK-MAP-06

Tokenizer V5 First Model Input Packet Smoke / No Transformer Forward Seal

## SSOT
- target_vocab_size: 48259
- valid_token_id_range: 0..48258
- reserved_range: 0..71
- byte_fallback_range: 72..327

## Scope
Build model input packet smoke fixtures from Tokenizer V5 48259 encoded ids. Validate `input_ids`, `attention_mask`, `position_ids`, batch shape, and id range.

## Explicit bans
Embedding lookup, transformer forward, lm_head logits, sampler execution, token generation, runtime persistent apply, checkpoint write, and tokenizer artifact mutation remain blocked.

## Next
QW-TOK-MAP-07: Embedding Row Gather Dry-run / No Transformer Forward Seal.
