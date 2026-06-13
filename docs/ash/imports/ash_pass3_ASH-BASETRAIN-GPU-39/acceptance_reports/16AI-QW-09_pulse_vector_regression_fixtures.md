# 16AI-QW-09 — Pulse Vector Regression Fixtures / Korean Minimal Pair Seal

## Scope

This seal consumes QW-08 tokenizer shadow no-regression evidence and Korean minimal pair fixtures to verify that QWave pulse, transition, eojeol, morph, and sentence graph metrics reproduce expected contrasts for coda, particle, ending, and addressivity cases. It rejects missing fixtures, failed assertions, byte fallback regressions, unknown token regressions, protected wrapper leaks, surface reconstruction mismatches, fixture autofill, expected assertion mutation, token id mutation, vocab augmentation, embedding resize, new token creation, or backend QWave switching.

## Required Evidence

- QW-08 shadow run receipt id/fingerprint
- QWave shadow diff id/fingerprint
- Korean minimal pair fixture corpus
- fixture snapshots
- assertion list
- regression policy id/fingerprint

## Implemented Files

- `crates/tokenizer_core/src/hangul_qwave_regression_fixtures.rs`
- `crates/tokenizer_core/tests/hangul_qwave_regression_fixtures.rs`
- `crates/tokenizer_core/src/lib.rs`

## Guards

- QW-08 shadow receipt required
- coda fixture required
- particle fixture required
- ending fixture required
- addressivity fixture required
- all snapshots finite
- coda contrast must pass
- particle contrast must pass
- ending contrast must pass
- addressivity contrast must pass
- byte fallback must not increase
- unknown token must not increase
- protected wrapper leak forbidden
- surface reconstruction must match
- fixture autofill forbidden
- expected assertion mutation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- new token creation forbidden
- backend QWave switch forbidden

## Acceptance Tests

- builds Korean minimal pair regression report
- coda contrast increases coda drag
- particle contrast changes topic flow
- ending contrast changes closure curve
- honorific contrast increases addressivity
- missing QW-08 receipt rejected
- incomplete fixture corpus rejected
- failed assertion rejected
- byte fallback regression rejected
- deterministic regression receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW10 until QWave graph serialization and diagnostics export the regression traces.
