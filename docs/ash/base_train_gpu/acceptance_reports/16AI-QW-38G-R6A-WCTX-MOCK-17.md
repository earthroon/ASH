# 16AI-QW-38G-R6A-WCTX-MOCK-17 Acceptance

## Acceptance Contract

The MOCK-17 provenance split passes only if:

- `total_cases >= 14`
- `accepted_cases >= 4`
- `blocked_cases >= 10`
- `expectation_mismatched_cases == 0`
- `mock_shape_promotion_blocked_count >= 1`
- `mock_runtime_masquerade_blocked_count >= 1`
- `runtime_candidate_without_receipt_blocked_count >= 1`
- `human_edited_without_approval_blocked_count >= 1`
- `review_approved_without_approval_blocked_count >= 1`
- `commit_candidate_without_approval_blocked_count >= 1`
- `committed_target_forbidden_blocked_count >= 1`
- `archived_target_forbidden_blocked_count >= 1`
- `production_safe_leak_blocked_count >= 1`
- `no_real_runtime_candidate_created == true`
- `no_committed_target_created == true`
- `no_archived_target_created == true`
- `no_target_mutation == true`
- `no_runtime_apply == true`
- `acceptance_pass == true`

## Local Verification

```bash
cargo check -p ash_core --bin ash_word_context_mock_candidate_provenance_split
cargo run -p ash_core --bin ash_word_context_mock_candidate_provenance_split
cat workspace/word_context_probe/wctx_mock_17_candidate_provenance_summary.json
```

## Container Verification Status

- Static bake: PASS
- Cargo compile: NOT RUN, container has no `cargo` / `rustc`
- Runtime CLI output: NOT RUN, requires local Rust environment
