# QW-TOK-MAP-04 — Tokenizer V5 Runtime Bind Dry-run / No Inference Seal

## SSOT
- target vocab size: 48259
- valid token id range: 0..48258
- reserved ids: 0..71
- byte fallback ids: 72..327 (`<0xXX>`)

## Scope
Creates runtime model spec candidate, vocab cap dry-run, native projection cap dry-run, tokenizer artifact load dry-run, reserved-token encode/decode dry-run, and hotcache regeneration candidate.

## No-Apply Contract
Runtime spec write, runtime vocab cap apply, runtime tokenizer bind, model inference, embedding lookup, transformer forward, lm_head logits, token generation, sampler execution, hotcache write, checkpoint write, and tokenizer artifact mutation are blocked.

## Next
QW-TOK-MAP-05 — Tokenizer V5 First Runtime Encode Decode Smoke / No Model Forward Seal
