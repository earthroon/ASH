# 16AI-QW-38G-R6A-WCTX-MOCK-01 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-01` — EN-KO Subtitle Mock Decode Candidate Text Fixture / Review Path Unlock Seal

## Files Added

```text
crates/ash_core/src/word_context_mock_decode_fixture.rs
crates/ash_core/src/bin/ash_word_context_mock_decode_fixture.rs
workspace/word_context_probe/wctx_mock_01_enko_mock_decode_fixture_cases.json
workspace/word_context_probe/wctx_mock_01_enko_mock_decode_fixture_matrix.json
workspace/word_context_probe/wctx_mock_01_enko_mock_decode_fixture_summary.json
workspace/word_context_probe/wctx_mock_01_enko_mock_decode_fixture_sample_receipt.json
workspace/word_context_probe/wctx_mock_01_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-01_enko_subtitle_mock_decode_candidate_text_fixture_review_path_unlock_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-01_bake_report.md
```

## Files Modified

```text
crates/ash_core/src/lib.rs
```

## Core API

```rust
pub fn default_enko_mock_decode_candidate_fixture_cases() -> Vec<EnKoMockDecodeCandidateFixtureInputCase>

pub fn build_enko_mock_decode_candidate_fixture_receipt(
    staging_receipt: &EnKoDecodeStagingReceipt,
    mock_candidate_target_korean: &str,
    mock_reason: &str,
) -> EnKoMockDecodeCandidateFixtureReceipt

pub fn run_enko_mock_decode_candidate_fixture_matrix(
    cases: &[EnKoMockDecodeCandidateFixtureInputCase],
) -> EnKoMockDecodeCandidateFixtureMatrix
```

## Baked Default Cases

```text
WCTX03-C001 -> FixtureCreated
WCTX03-C003 -> FixtureCreated
WCTX03-C005 -> FixtureCreated
WCTX03-C007 -> FixtureCreated
WCTX03-C009 -> FixtureCreated
WCTX03-C011 -> FixtureCreated
WCTX03-C013 -> FixtureCreated
WCTX03-C015 -> FixtureCreated
WCTX03-C017 -> FixtureCreated
WCTX03-C019 -> FixtureCreated
WCTX03-C021 -> FixtureCreated
WCTX03-C023 -> FixtureCreated
```

## Safety Invariants

```text
mock_only=true
production_safe=false
runtime_decode_executed=false
generation_executed=false
model_forward_executed=false
sampling_executed=false
target_text_mutated=false
target_subtitle_committed=false
candidate_output_committed=false
runtime_default_apply=false
rerank_applied=false
mock_mislabeled_as_runtime=false
```

## Validation

Static validation passed with `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE` because the current environment does not provide a Rust toolchain.
