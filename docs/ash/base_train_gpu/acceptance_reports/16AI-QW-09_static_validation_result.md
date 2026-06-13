# 16AI-QW-09 Static Validation Result

## Environment

- cargo: command not found
- rustc: command not found

## File Presence
- PASS: crates/tokenizer_core/src/hangul_qwave_regression_fixtures.rs
- PASS: crates/tokenizer_core/tests/hangul_qwave_regression_fixtures.rs
- PASS: acceptance_reports/16AI-QW-09_pulse_vector_regression_fixtures.md
- PASS: bake_artifacts/16AI-QW-09_BAKE_REPORT.md

## Export Checks
- PASS: module export present
- PASS: public builder export present
- PASS: receipt export present

## Guard Checks
- PASS: FixtureAutofillForbidden
- PASS: ExpectedAssertionMutationForbidden
- PASS: ByteFallbackRegressionDetected
- PASS: UnknownTokenRegressionDetected
- PASS: ProtectedWrapperLeakDetected
- PASS: SurfaceReconstructionMismatch
- PASS: TokenIdMutationForbidden
- PASS: VocabAugmentationForbidden
- PASS: EmbeddingResizeForbidden
- PASS: NewTokenCreationForbidden
- PASS: BackendQWaveSwitchForbidden

## Test Function Checks
- test functions: 10

## Bracket Balance
- PASS: crates/tokenizer_core/src/hangul_qwave_regression_fixtures.rs balanced
- PASS: crates/tokenizer_core/tests/hangul_qwave_regression_fixtures.rs balanced
