# 16AI-QW-38G-R6A-WCTX-RT-04 Bake Report

## Patch

- **ID:** 16AI-QW-38G-R6A-WCTX-RT-04
- **Title:** One-Step Decoded Surface Receipt Bind / No Candidate Envelope No Review Insert Seal
- **Domain SSOT:** en_to_ko_translation_subtitle_machine
- **Status:** BAKED_STATIC_NO_CARGO

## Implemented Files

- `crates/ash_core/src/word_context_rt_one_step_decoded_surface_bind.rs`
- `crates/ash_core/src/bin/ash_word_context_rt_one_step_decoded_surface_bind.rs`
- `crates/ash_core/src/lib.rs` export surface update
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-RT-04.md`
- `WCTX_RT_04_STATIC_CHECKS.txt`
- `WCTX_RT_04_BAKE_MANIFEST.json`

## Scope

RT-04 binds the RT-03 one-step decoded token surface as surface evidence only.
It verifies upstream receipt keys, tokenizer identity, token surface digest, UTF-8 validity, and special-token classification while preserving the no-candidate/no-review/no-commit boundary.

## Positive Cases

- `rt04:normal_token_surface_receipt_bind`
- `rt04:eos_token_surface_receipt_bind_no_candidate`
- `rt04:whitespace_token_surface_receipt_bind`
- `rt04:hangul_token_surface_receipt_bind`

## Negative Matrix

32 negative cases were added for missing upstream receipt keys, tokenizer/surface mismatches, unsafe special token, new decode/selection leaks, sequence/multi-token decode leaks, decoded/candidate text leaks, candidate envelope finalization, review queue insertion, auto-accept/commit, target mutation, runtime apply, training, backward, and weight commit.

## Static Checks

- module exists: `True`
- bin exists: `True`
- lib export present: `True`
- module brace balance: `0`
- bin brace balance: `0`
- total case count: `36`

## Cargo

`cargo` / `rustc` were not available in this container, so compile and runtime execution were not run here. Local verification command:

```bash
cargo check -p ash_core --bin ash_word_context_rt_one_step_decoded_surface_bind
cargo run -p ash_core --bin ash_word_context_rt_one_step_decoded_surface_bind
```
