# SFT-GPU-8J quality eval / promotion gate

## Status
PASS_STATIC / PENDING_RUNTIME_QUALITY_EVAL

## Sealed
- quality eval prompt set
- base vs LoRA comparison proxy
- runtime delta guard
- loss trace guard
- generation sanity guard
- promotion status
- promoted adapter copy

## Guards
- no pass on zero delta
- no pass on NaN logits
- no pass on empty generation
- no pass on excessive unk/repetition
- no silent promotion
- manual review fallback on uncertain quality

## Next
SFT-GPU-8K runtime integration hardening
