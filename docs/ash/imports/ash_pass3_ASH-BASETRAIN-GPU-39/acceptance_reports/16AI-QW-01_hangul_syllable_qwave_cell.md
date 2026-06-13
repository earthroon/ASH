# 16AI-QW-01 — Hangul Syllable QWave Cell SSOT / Choseong-Jungseong-Jongseong Pulse Seed Seal

## Scope

This seal consumes the QW-00 Text-QWave boundary receipt and existing `HangulFeatureRow` values to create deterministic `QWaveSyllableCell` records for precomposed Hangul syllables. It preserves choseong, jungseong, jongseong, Cheon/Ji/In feature fields, syllable mass, curvature bias, coda weight, and creates a `QWavePulseSeed` without implementing full Pulse Vector, syllable transitions, eojeol chains, sentence graphs, token id mutation, vocab augmentation, embedding resize, or backend QWave switching.

## Implemented Files

- `crates/tokenizer_core/src/hangul_qwave_cell.rs`
- `crates/tokenizer_core/tests/hangul_qwave_cell.rs`
- `crates/tokenizer_core/src/lib.rs`

## Required Evidence

- QW-00 boundary receipt id/fingerprint
- QW-00 guard-passed flag
- source text fingerprint
- HangulFeatureRow list
- Hangul decomposition values
- Cheon/Ji/In feature values
- syllable mass / curvature / coda values
- pulse seed policy

## Guards

- QW-00 boundary receipt required
- HangulFeatureRow required
- decomposition preserved
- Cheon/Ji/In features preserved
- pulse seed created
- full Pulse Vector forbidden
- syllable transition creation forbidden
- eojeol chain creation forbidden
- sentence graph creation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds QWave cells from HangulFeatureRow
- preserves choseong/jungseong/jongseong indices
- preserves Cheonjiin feature fields
- creates pulse seed but not full pulse vector
- skips non-Hangul without mutation
- missing QW-00 boundary receipt rejected
- missing HangulFeatureRow rejected
- unexpected transition creation rejected
- token/vocab/backend mutation rejected
- deterministic cell receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW02 until `QWavePulseVector` derives from `QWavePulseSeed`.
