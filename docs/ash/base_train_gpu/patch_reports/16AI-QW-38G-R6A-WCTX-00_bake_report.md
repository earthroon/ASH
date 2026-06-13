# 16AI-QW-38G-R6A-WCTX-00 Bake Report

## Result

Baked as a static Rust-native probe-only patch.

## Main Change

Added `ash_core::word_context` as the Word Context SSOT layer for deterministic
current-turn span receipts.

## Guardrail

The patch intentionally does not wire the probe into inference, sampler, decoder,
QWave apply, or LexGraph persistence. It is safe to inspect and call manually,
but it does not alter Ash output quality by itself.

## Verification

Static verification only. Rust toolchain unavailable in bake container.

See:

- `acceptance_reports/16AI-QW-38G-R6A-WCTX-00_word_context_ssot_probe_schema_seal.md`
- `workspace/word_context_probe/ash_wctx_00_static_validation.json`
