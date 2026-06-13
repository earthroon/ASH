# 16AI-QW-38G-R6A-WCTX-PROMO-00 Acceptance Report

## Acceptance Target

`Mock Runtime Boundary Baseline Freeze / No Mock Masquerade No Runtime Apply Seal`

## SSOT

- `domain_ssot = en_to_ko_translation_subtitle_machine`
- Upstream mock boundary: `WCTX-MOCK-16..20`
- Upstream runtime receipt chain: `WCTX-RT-00..10`
- Current authority: boundary freeze only.

## Acceptance Criteria Baked

- `total_cases >= 23`
- `accepted_cases >= 4`
- `blocked_cases >= 19`
- `expectation_mismatched_cases == 0`
- MOCK-16..20 chain presence is required.
- RT-00..10 chain presence is required.
- MOCK-20 receipt shape draft key cannot be reused as RT-00 forward dry probe receipt key.
- Mock or fixture provenance cannot be relabelled as real runtime.
- Receipt-only evidence cannot be promoted to runtime evidence.
- Runtime adapter evidence cannot be attached in PROMO-00.
- Runtime receipt cannot be created without runtime adapter evidence.
- Tokenizer encode, forward, decode, generation, sampling, token selection, preview queue insert, production review insert, approval, commit, runtime apply, training, backward, weight commit, and delta stack append are blocked.

## Local Commands

```bash
cargo check -p ash_core --bin ash_word_context_promo_00_mock_runtime_boundary_baseline
cargo run -p ash_core --bin ash_word_context_promo_00_mock_runtime_boundary_baseline
```

## Expected Outputs

```text
workspace/word_context_probe/wctx_promo_00_mock_runtime_boundary_baseline_cases.json
workspace/word_context_probe/wctx_promo_00_mock_runtime_boundary_baseline_receipts.json
workspace/word_context_probe/wctx_promo_00_mock_runtime_boundary_baseline_matrix.json
workspace/word_context_probe/wctx_promo_00_mock_runtime_boundary_baseline_summary.json
workspace/word_context_probe/wctx_promo_00_mock_runtime_boundary_baseline_sample_receipt.json
```

## Container Status

`cargo` and `rustc` were not available in this container, so this bake is sealed as `BAKED_STATIC_NO_CARGO`.
