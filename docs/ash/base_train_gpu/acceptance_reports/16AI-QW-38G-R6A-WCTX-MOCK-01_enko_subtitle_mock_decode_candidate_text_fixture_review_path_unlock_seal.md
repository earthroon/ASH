# 16AI-QW-38G-R6A-WCTX-MOCK-01 Acceptance Report

## Patch

- Patch ID: `16AI-QW-38G-R6A-WCTX-MOCK-01`
- Name: `EN-KO Subtitle Mock Decode Candidate Text Fixture / Review Path Unlock Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Scope

MOCK-01 adds a test-only mock decode candidate fixture layer over WCTX-12 staged decode candidate receipts. It attaches explicit mock Korean candidate text, creates a WCTX-13 review-compatible mock staging receipt, and keeps the fixture clearly marked as non-production.

## Acceptance Criteria

- [PASS] EN-KO translation subtitle domain SSOT is preserved.
- [PASS] WCTX-12 decode staging receipt input is supported.
- [PASS] Only `Staged` receipts are used by the default fixture path.
- [PASS] Mock candidate target Korean text is created.
- [PASS] Mock candidate output is labeled as `MockCandidate`.
- [PASS] Mock fixture is marked `mock_only=true` and `production_safe=false`.
- [PASS] Mock fixture is not mislabeled as runtime output.
- [PASS] WCTX-13 review-compatible mock staging receipt is created.
- [PASS] Source WCTX-12 receipt is not mutated.
- [PASS] Target subtitle is not mutated.
- [PASS] Candidate output is not committed.
- [PASS] Runtime decode is not executed.
- [PASS] Generation/model-forward/sampling are not executed.
- [PASS] Runtime default apply remains false.
- [PASS] Rerank remains false.
- [PASS] Matrix JSON output is generated.
- [PASS] Summary JSON output is generated.
- [PASS] Sample receipt JSON output is generated.

## Static Matrix Summary

```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "fixture_created_count": 12,
  "mock_candidate_text_created_count": 12,
  "review_bridge_created_count": 12,
  "mock_review_staging_receipt_created_count": 12,
  "runtime_decode_executed_count": 0,
  "generation_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "runtime_default_apply_count": 0,
  "mock_mislabeled_as_runtime_count": 0
}
```

## Fixture Note

WCTX-12 default staging receipts did not carry `original_target_korean` through the staging input, so MOCK-01 uses an explicit stable EN-KO mock fixture corpus keyed by `center_cue_id`. This is not silent production correction: every bridged candidate is labeled `MockCandidate`, `mock_only=true`, and `production_safe=false`.

## Toolchain Note

Rust compilation was not executed in this environment because `cargo` / `rustc` are unavailable. The baked static validation status is `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
