# WCTX-PROMO-06 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-PROMO-06`

`RT00 Real Forward Receipt Rebind / No Mock20 Receipt Substitution Seal`

## Files added

- `crates/ash_core/src/word_context_promo_06_rt00_real_forward_receipt_rebind.rs`
- `crates/ash_core/src/bin/ash_word_context_promo_06_rt00_real_forward_receipt_rebind.rs`

## Files updated

- `crates/ash_core/src/lib.rs`

## Reports added

- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-06.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-PROMO-06_bake_report.md`
- `WCTX_PROMO_06_STATIC_CHECKS.txt`
- `WCTX_PROMO_06_BAKE_MANIFEST.json`

## Boundary

PROMO-06 is an RT-00 rebind patch. It creates a real RT-00 forward receipt key from PROMO-04/PROMO-05 real evidence and explicitly blocks MOCK-20 receipt substitution, selected token creation, token selection, decode, candidate text, RT-01 receipt creation, queue insert, approval, commit, runtime apply, training, backward, optimizer step, and delta stack append.

## Local verification

```bash
cargo check -p ash_core --bin ash_word_context_promo_06_rt00_real_forward_receipt_rebind
cargo run -p ash_core --bin ash_word_context_promo_06_rt00_real_forward_receipt_rebind
```

## Static result

`BAKED_STATIC_NO_CARGO`
