# 16AI-QW-04 — Eojeol QWave Cell Chain / Whitespace-Bound Grouping Seal

## Scope

This seal consumes QW-03 `QWaveSyllableTransitionBatch` records, QW-02 `QWavePulseVectorBatch` records, and QW-01 `QWaveSyllableCellBatch` records to group Hangul QWave cells and transition edges into deterministic whitespace-bound `QWaveEojeolChain` records.

It computes pulse vector sum, pulse vector mean, circular phase mean, transition energy aggregate, flow continuity mean, binding energy, boundary open, and boundary close while forbidding sentence graphs, morph overlays, tokenizer DP cost mutation, token id mutation, vocab augmentation, embedding resize, or backend QWave switching.

## Implemented Files

- `crates/tokenizer_core/src/hangul_qwave_eojeol.rs`
- `crates/tokenizer_core/tests/hangul_qwave_eojeol.rs`
- `crates/tokenizer_core/src/lib.rs`

## Required Evidence

- QW-03 transition receipt id/fingerprint
- QWaveSyllableCellBatch id/fingerprint
- QWavePulseVectorBatch id/fingerprint
- QWaveSyllableTransitionBatch id/fingerprint
- source text fingerprint
- eojeol boundary policy id/fingerprint

## Guards

- QW-03 transition receipt required
- cell batch required
- pulse vector batch required
- transition batch required
- whitespace-bound grouping required
- punctuation boundary split required
- protected span boundary split required
- chain cell coverage required
- chain transition coverage required
- pulse vector sum required
- pulse vector mean required
- binding energy required
- boundary open/close required
- all chain values finite
- cross-whitespace chain forbidden
- cross-punctuation chain forbidden
- cross-protected-span chain forbidden
- sentence graph creation forbidden
- morph overlay creation forbidden
- tokenizer DP cost mutation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds eojeol chains from whitespace-bound text
- groups cells and transitions inside each eojeol
- computes pulse aggregate and binding energy
- computes boundary open and close
- blocks cross-whitespace chain
- missing QW-03 receipt rejected
- transition outside chain span rejected
- non-finite binding energy / invalid policy rejected
- unexpected sentence graph creation rejected
- deterministic eojeol chain receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW05 until Morph Role Pulse Overlay consumes `QWaveEojeolChain` records.
