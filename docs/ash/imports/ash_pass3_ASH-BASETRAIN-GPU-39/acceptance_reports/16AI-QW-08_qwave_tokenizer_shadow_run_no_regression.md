# 16AI-QW-08 — QWave Tokenizer Shadow Run / V5-V6 No-Regression Seal

## Scope

This seal consumes the QW-07 QWave tokenizer DP cost bridge output and compares a baseline tokenizer run against a QWave-adjusted shadow tokenizer run. It records shadow token path differences while forbidding committed token id mutation, vocab augmentation, embedding resize, new token creation, runtime tokenizer policy mutation, SFT feature export, LoRA routing hint creation, and backend QWave switching.

## Required Evidence

- QW-07 DP bridge receipt id/fingerprint
- QW-07 DP bridge plan id/fingerprint
- baseline tokenizer run snapshot
- QWave shadow tokenizer run snapshot
- no-regression policy id/fingerprint
- source text fingerprint
- committed token ids before/after

## Guards

- QW-07 DP bridge receipt required
- baseline snapshot required
- shadow snapshot required
- shadow run executed
- shadow best path may be recorded
- shadow commit forbidden
- committed token ids unchanged
- byte fallback count must not increase
- unknown token count must not increase
- surface reconstruction must match
- special token boundaries must be preserved
- protected wrapper leak forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- new token creation forbidden
- runtime tokenizer policy mutation forbidden
- SFT feature export forbidden
- LoRA routing hint creation forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds shadow run without committing token ids
- allows shadow token ids to differ from baseline
- detects no byte fallback increase
- validates surface reconstruction match
- preserves special token boundaries
- missing QW-07 receipt rejected
- committed token id mutation rejected
- byte fallback increase rejected
- protected wrapper leak rejected
- deterministic shadow run receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW09 until shadow run diagnostics are serialized and compared across a Korean minimal-pair regression corpus.
