# 16AI-6A Static Scan

## 확정

Static markers were found for:

- `af16ai6a_protected_span_probe`
- `SpanKind::ProtectedWrapper`
- `SpanKind::ProtectedSpecial`
- `SpanKind::Newline`
- `should_bypass_korean_analyzer`
- `vocab_exact_hit`
- `fallback_required`
- `wrapper_label_fragmented`
- `protected_span_risk_score`
- `generation=false`
- `checkpoint_required=false`
- `chatml_lite_excluded=true`
- shell runner: `scripts/run_16AI_6A_protected_span_probe.sh`
- PowerShell runner: `scripts/run_16AI_6A_protected_span_probe.ps1`

## 추정

The scanner is wired as a standalone diagnostic probe and should not mutate token IDs in default `diagnostic` mode.

## 판단불가

No Rust compile/runtime proof is available in this container because `cargo` is not installed.
