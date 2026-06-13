# 16AI-QW-38G-R6A-WCTX-MOCK-16 Bake Report

## Patch

- `patch_id`: `16AI-QW-38G-R6A-WCTX-MOCK-16`
- `title`: `Runtime Candidate Envelope Mock / Real Decode Output Shape Contract Seal`
- `domain_ssot`: `en_to_ko_translation_subtitle_machine`
- `status`: `BAKED_STATIC_NO_CARGO`

## Intent

This patch fills the WCTX MOCK-16 layer with a deterministic runtime-candidate-envelope mock.
It defines the output shape that a future real runtime decode result must satisfy before it can enter WCTX review flow.
The patch is explicitly shape-only and does not create a real runtime candidate.

## Files Added

- `crates/ash_core/src/word_context_mock_runtime_candidate_envelope.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_runtime_candidate_envelope.rs`

## Files Updated

- `crates/ash_core/src/lib.rs`

## Runtime Boundary

MOCK-16 forbids:

- runtime decode
- generation
- model forward
- sampling
- full logits attachment
- real runtime receipt attachment
- review queue insertion
- auto accept
- target mutation
- runtime apply
- checkpoint apply
- weight commit
- promotion

## Implemented Shape Fixtures

Positive shape cases:

1. `mock16:greedy_shape_single_candidate`
2. `mock16:lookahead_shape_ranked_candidate`
3. `mock16:safety_blocked_shape_candidate`

Negative leak/block cases:

1. `mock16:missing_source_receipt_key`
2. `mock16:missing_token_spans`
3. `mock16:token_count_mismatch`
4. `mock16:runtime_decode_executed_leak`
5. `mock16:full_logits_attached_leak`
6. `mock16:runtime_provenance_leak`

## CLI

```bash
cargo run -p ash_core --bin ash_word_context_mock_runtime_candidate_envelope
```

Expected output files:

- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelope_cases.json`
- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelopes.json`
- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelope_receipts.json`
- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelope_matrix.json`
- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelope_summary.json`
- `workspace/word_context_probe/wctx_mock_16_runtime_candidate_envelope_sample_receipt.json`

## Static Validation

The container does not provide `cargo` or `rustc`, so compile/run validation was not executed here.
Static checks were performed for:

- module file existence
- CLI bin file existence
- `lib.rs` module export
- brace balance
- patch constants
- shape fixture case ids
- negative leak case ids
- acceptance summary fields

See `WCTX_MOCK_16_STATIC_CHECKS.txt` and `WCTX_MOCK_16_BAKE_MANIFEST.json`.
