# 16AI-QW-01 Static Validation Result

## Result

PASS_STATIC_LIMITED

## Checks Performed

- `crates/tokenizer_core/src/hangul_qwave_cell.rs` exists.
- `crates/tokenizer_core/tests/hangul_qwave_cell.rs` exists.
- `crates/tokenizer_core/src/lib.rs` exports `hangul_qwave_cell` module and public QW-01 symbols.
- `QWaveSyllableCell`, `QWavePulseSeed`, `QWaveSyllableCellBatch`, and `QWaveSyllableCellReceipt` are defined.
- `build_qwave_syllable_cell_batch`, `build_qwave_syllable_cell_receipt`, and `build_qwave_syllable_cell_batch_and_receipt` are defined.
- 10 acceptance tests are present.
- Brace/parenthesis balance check passed for changed Rust files.

## Native Test Status

`cargo` is not installed in this container, so native Rust tests were not executed here.

```txt
cargo: command not found
```

## Guard Status

The implementation rejects or forbids:

- missing QW-00 receipt id/fingerprint
- failed QW-00 boundary flag when required
- missing HangulFeatureRow
- missing decomposition / invalid Hangul scalar
- missing or non-finite Cheon/Ji/In feature values
- full Pulse Vector implementation in QW-01
- syllable transition creation in QW-01
- eojeol chain creation in QW-01
- sentence graph creation in QW-01
- token id mutation
- vocab augmentation
- embedding resize
- backend QWave switch

## Pending Runtime Validation

Run on a Rust-enabled machine:

```bash
cargo test -p tokenizer_core --test hangul_qwave_cell -- --nocapture
```
