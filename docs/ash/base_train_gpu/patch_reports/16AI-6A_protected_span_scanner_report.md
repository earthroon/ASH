# 16AI-6A Protected Span Scanner Bake Report

## 1. 확정

This bake adds a standalone protected span scanner probe:

- `crates/model_core/src/bin/af16ai6a_protected_span_probe.rs`
- `scripts/run_16AI_6A_protected_span_probe.sh`
- `scripts/run_16AI_6A_protected_span_probe.ps1`

The probe keeps these gate values fixed:

- `generation=false`
- `checkpoint_required=false`
- `assembly_mode=off`
- `cheonjiin_dp=false`
- `chatml_lite_excluded=true`
- default wrappers: `plain,dialogue-ko,instruction-ko`
- default mode: `diagnostic`

## 2. 구현 내용

- Added `SpanKind` with `ProtectedSpecial`, `ProtectedWrapper`, `Newline`, `Whitespace`, `Korean`, `Latin`, `Number`, `Punctuation`, `Mixed`, and `Unknown`.
- Added longest-match scanning priority: special tokens, wrapper labels, newline, whitespace, Korean run, Latin run, number run, punctuation, unknown.
- Added per-span diagnostics including `vocab_exact_hit`, `fallback_required`, `wrapper_label_fragmented`, and baseline decode preservation checks.
- Added `protected_span_risk_score` alongside existing fragmentation diagnostics.
- Added JSON/Markdown/acceptance output paths.

## 3. 추정

16AI-6A should reveal whether role labels are being protected before general Korean analysis, without yet claiming generation quality improvement.

## 4. 판단불가

Compile/runtime status is pending because the bake environment has no `cargo` executable.

## 5. Next Gate

16AI-6B Cheonjiin Structural Analyzer.
