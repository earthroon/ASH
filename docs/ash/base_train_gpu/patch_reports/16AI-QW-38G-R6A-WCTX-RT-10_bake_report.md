# 16AI-QW-38G-R6A-WCTX-RT-10 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-RT-10`
- `Preview Queue Receipt Bind / No Approval No Commit Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Base

- Base bake: `ash_pass3_WCTX-RT-09_review_queue_candidate_preview_baked.zip`

## Implemented

- Added `crates/ash_core/src/word_context_rt_preview_queue_receipt_bind.rs`
- Added `crates/ash_core/src/bin/ash_word_context_rt_preview_queue_receipt_bind.rs`
- Updated `crates/ash_core/src/lib.rs`
- Added static checks, bake manifest, patch report, and acceptance report.

## Contract

RT-10 consumes RT-09 review queue candidate preview evidence and binds a preview queue receipt only.
It explicitly blocks approval receipt creation, commit receipt creation, production review queue receipt creation, production review queue insertion, auto-accept, auto-commit, candidate envelope finalization, candidate id issuance, commit candidate creation, committed target creation, target mutation, runtime apply, production subtitle mutation, training, backward, and weight commit.

## Case Matrix

- Positive cases: 4
- Negative cases: 54
- Total cases: 58

## Runtime Status

- `status`: `BAKED_STATIC_NO_CARGO`
- `cargo_status`: `NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`

This bake is a static code/materialization bake. Local Rust validation should run:

```bash
cargo check -p ash_core --bin ash_word_context_rt_preview_queue_receipt_bind
cargo run -p ash_core --bin ash_word_context_rt_preview_queue_receipt_bind
```
