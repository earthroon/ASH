# 16AI-QW-38G-R6A-WCTX-PROMO-00 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-PROMO-00`
- `Mock Runtime Boundary Baseline Freeze / No Mock Masquerade No Runtime Apply Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Base

- Base bake: `ash_pass3_WCTX-RT-10_preview_queue_receipt_bind_baked.zip`

## Implemented

- Added `crates/ash_core/src/word_context_promo_00_mock_runtime_boundary_baseline.rs`
- Added `crates/ash_core/src/bin/ash_word_context_promo_00_mock_runtime_boundary_baseline.rs`
- Updated `crates/ash_core/src/lib.rs`
- Added static checks, bake manifest, patch report, and acceptance report.

## Contract

PROMO-00 freezes the boundary between WCTX-MOCK-16..20 and WCTX-RT-00..10.
It explicitly blocks mock receipt key reuse as RT-00 evidence, mock provenance relabelling as real runtime, receipt-only evidence promotion, runtime adapter evidence attachment, runtime receipt creation without adapter evidence, tokenizer encode, model forward, decode, generation, sampling, token selection, preview queue insertion, production review insertion, operator approval, candidate commit, runtime apply, training, backward, weight commit, and delta stack append.

## Case Matrix

- Positive cases: 4
- Negative cases: 19
- Total cases: 23

## Runtime Status

- `status`: `BAKED_STATIC_NO_CARGO`
- `cargo_status`: `NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`

This bake is a static code/materialization bake. Local Rust validation should run:

```bash
cargo check -p ash_core --bin ash_word_context_promo_00_mock_runtime_boundary_baseline
cargo run -p ash_core --bin ash_word_context_promo_00_mock_runtime_boundary_baseline
```
