# QW-TOK-00 — Tokenizer V5 Runtime Binding Probe / Vocab Cap Parity Seal

## Purpose
Probe the external local Tokenizer V5 artifacts and bind their metadata to a runtime vocab-cap parity receipt without packaging tokenizer files and without auto repair.

## Local artifact SSOT candidate

```txt
D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts
```

Expected files:

```txt
tokenizer_v5.model
tokenizer_v5.vocab
```

## Hard bans

- No tokenizer file embedding in this bake packet.
- No vocab padding.
- No vocab truncation.
- No token id remap.
- No lm_head resize.
- No model weight mutation.
- No runtime decode binding.
- No sampler/QW selector/MCTS mutation.

## Status rule

- PASS only when tokenizer line count, sentencepiece piece size, runtime vocab cap, lm_head output dim, and native projection cap are all known and equal.
- PENDING when runtime dimensions are not yet known.
- FAILED when any known parity comparison mismatches.
