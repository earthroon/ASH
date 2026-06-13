# 16AI-QW-38G-R6A-WCTX-MOCK-17 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-MOCK-17`
- Runtime Candidate Provenance Split / Mock Candidate Cannot Masquerade As Runtime Seal
- SSOT: `en_to_ko_translation_subtitle_machine`

## Implemented

This bake adds the executable mock provenance layer rather than a placeholder scaffold.

Added:

- `crates/ash_core/src/word_context_mock_candidate_provenance_split.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_candidate_provenance_split.rs`

Modified:

- `crates/ash_core/src/lib.rs`

The module defines:

- candidate provenance kinds
- transition rules
- candidate identity contract
- provenance status and block reasons
- deterministic receipts
- positive and negative fixture cases
- matrix summary and acceptance gate

## Fixture Coverage

Positive accepted cases:

1. `mock17:mock_fixture_candidate_source_bound`
2. `mock17:human_edited_candidate_with_approval`
3. `mock17:review_approved_candidate_with_approval`
4. `mock17:commit_candidate_with_commit_approval`

Negative blocked cases:

1. `mock17:missing_source_receipt_key`
2. `mock17:mock_shape_promoted_to_fixture`
3. `mock17:mock_fixture_masquerades_as_runtime`
4. `mock17:runtime_candidate_without_runtime_receipt`
5. `mock17:human_edited_without_approval`
6. `mock17:review_approved_without_approval`
7. `mock17:commit_candidate_without_commit_approval`
8. `mock17:committed_target_forbidden`
9. `mock17:archived_audit_target_forbidden`
10. `mock17:production_safe_true_leak`

## Non-scope Preserved

- No real runtime decode
- No generation
- No model forward
- No sampling
- No review queue insert
- No target mutation
- No runtime apply
- No checkpoint apply
- No weight commit
- No promotion

## CLI

```bash
cargo run -p ash_core --bin ash_word_context_mock_candidate_provenance_split
```

Expected outputs:

- `workspace/word_context_probe/wctx_mock_17_candidate_provenance_cases.json`
- `workspace/word_context_probe/wctx_mock_17_candidate_provenance_receipts.json`
- `workspace/word_context_probe/wctx_mock_17_candidate_provenance_matrix.json`
- `workspace/word_context_probe/wctx_mock_17_candidate_provenance_summary.json`
- `workspace/word_context_probe/wctx_mock_17_candidate_provenance_sample_receipt.json`

## Static Bake Status

`cargo` and `rustc` are unavailable in this container, so compile/run was not executed here.
The patch is sealed as `BAKED_STATIC_NO_CARGO`.

See:

- `WCTX_MOCK_17_STATIC_CHECKS.txt`
- `WCTX_MOCK_17_BAKE_MANIFEST.json`
