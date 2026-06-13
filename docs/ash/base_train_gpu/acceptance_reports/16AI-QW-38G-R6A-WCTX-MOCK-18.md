# 16AI-QW-38G-R6A-WCTX-MOCK-18 Acceptance

## Expected acceptance after local cargo run

- total_cases >= 16
- accepted_cases >= 4
- blocked_cases >= 12
- expectation_mismatched_cases == 0
- rank_computed_cases >= 3
- flag_computed_cases >= 1
- top_candidate_present_cases >= 3
- all_positive_cases_accepted == true
- all_negative_cases_blocked == true
- no_real_runtime_candidate_created == true
- no_auto_accept_executed == true
- no_auto_commit_executed == true
- no_target_mutation == true
- no_runtime_apply == true
- no_production_queue_mutation == true
- acceptance_pass == true

## Local commands

```bash
cargo check -p ash_core --bin ash_word_context_mock_review_queue_multi_candidate
cargo run -p ash_core --bin ash_word_context_mock_review_queue_multi_candidate
cat workspace/word_context_probe/wctx_mock_18_review_queue_summary.json
```
