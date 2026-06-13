# 16AI-QW-02 — QWave Pulse Vector Derivation / Cell Direction-Amplitude-Phase Seal

## Scope

This seal consumes QW-01 QWaveSyllableCellBatch records and QWavePulseSeed values to derive deterministic QWavePulseVector records for Hangul syllable cells. It creates direction components, amplitude, phase, pressure, closure, resonance, onset push, vowel flow, coda drag, curvature, and mass values while forbidding syllable transitions, eojeol chains, sentence graphs, token id mutation, vocab augmentation, embedding resize, or backend QWave switching.

## Required Evidence

- QW-01 cell receipt id/fingerprint
- QWaveSyllableCellBatch id/fingerprint
- QWaveSyllableCell list
- QWavePulseSeed values
- pulse vector policy id/fingerprint
- source text fingerprint

## Implemented Files

- `crates/tokenizer_core/src/hangul_qwave_pulse.rs`
- `crates/tokenizer_core/tests/hangul_qwave_pulse.rs`
- `crates/tokenizer_core/src/lib.rs`

## Guards

- QW-01 cell receipt required
- cell batch required
- pulse seed required
- direction components required
- amplitude required
- phase required
- pressure required
- closure required
- resonance required
- all vector values finite
- syllable transition creation forbidden
- eojeol chain creation forbidden
- sentence graph creation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds pulse vectors from QWave cells
- derives direction components from Cheonjiin seeds
- derives amplitude and phase
- derives closure from coda
- creates full pulse vector but no transition
- missing QW-01 receipt rejected
- missing pulse seed rejected
- non-finite vector values rejected
- unexpected transition creation rejected
- deterministic pulse vector receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW03 until QWaveSyllableTransition derives from adjacent QWavePulseVector records.
