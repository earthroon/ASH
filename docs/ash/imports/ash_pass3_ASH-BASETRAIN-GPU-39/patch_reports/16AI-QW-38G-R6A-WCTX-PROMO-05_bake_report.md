# WCTX-PROMO-05 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-PROMO-05`

`Real Runtime TopK Trace Capture / No Full Logits No Token Selection Seal`

## Files added

- `crates/ash_core/src/word_context_promo_05_real_runtime_topk_trace_capture.rs`
- `crates/ash_core/src/bin/ash_word_context_promo_05_real_runtime_topk_trace_capture.rs`

## Files updated

- `crates/ash_core/src/lib.rs`

## Reports added

- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-05.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-PROMO-05_bake_report.md`
- `WCTX_PROMO_05_STATIC_CHECKS.txt`
- `WCTX_PROMO_05_BAKE_MANIFEST.json`

## Boundary

PROMO-05 is a top-k trace capture patch. It does not create a selected token, does not decode token surfaces, does not create candidate text, does not persist full logits, and does not rebind RT-00.

## Local verification

```bash
cargo check -p ash_core --bin ash_word_context_promo_05_real_runtime_topk_trace_capture
cargo run -p ash_core --bin ash_word_context_promo_05_real_runtime_topk_trace_capture
```

## Static result

`BAKED_STATIC_NO_CARGO`
