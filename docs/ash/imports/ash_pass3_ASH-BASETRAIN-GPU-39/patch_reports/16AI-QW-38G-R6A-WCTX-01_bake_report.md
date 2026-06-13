# 16AI-QW-38G-R6A-WCTX-01 Bake Report

## Correction

User SSOT correction received: **Ash is an EN-to-KO translation subtitle-machine domain system.**

The earlier broad subtitle-domain corpus was replaced with an EN→KO translation-subtitle corpus.

## Changed Files

- `crates/ash_core/src/word_context_smoke.rs`
- `crates/ash_core/src/word_context.rs`
- `workspace/word_context_probe/wctx_01_korean_smoke_cases.json`
- `workspace/word_context_probe/wctx_01_smoke_matrix.json`
- `workspace/word_context_probe/wctx_01_smoke_summary.json`
- `workspace/word_context_probe/wctx_01_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-01_korean_word_context_smoke_corpus_probe_regression_matrix_seal.md`

## Summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-01",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 36,
  "pass_cases": 36,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "required_surface_failures": 0,
  "expected_role_failures": 0,
  "span_slice_failures": 0,
  "risk_failures": 0,
  "token_id_mutation_count": 0,
  "generation_mutation_count": 0,
  "roundtrip_failure_count": 0
}
```

## Toolchain

Rust toolchain is unavailable in this container, so the report is static and file-generated rather than cargo-executed.
