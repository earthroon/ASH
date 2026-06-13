# 16AI-QW-38G-R6A-WCTX-01 Acceptance Report

## Status

PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE

## Corrected Domain SSOT

Ash is an **EN-to-KO translation subtitle-machine** domain system.

The previous broad `subtitle_machine` interpretation was invalidated by the user correction. This bake re-anchors WCTX-01 around English source cue preservation, Korean target subtitle wording, timing/cue invariants, compression, line breaks, speaker/register continuity, terminology consistency, and no-hallucinated translation.

## Matrix Summary

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

## Non-mutation Contract

- token id mutation: 0
- generation mutation: 0
- QWave default apply: none
- LexGraph long-term write: none
- runtime default apply: none

## Judgment

This patch validates WCTX-00 probe stability for EN-to-KO translation subtitle smoke cases only. It does not claim generation-quality improvement.
