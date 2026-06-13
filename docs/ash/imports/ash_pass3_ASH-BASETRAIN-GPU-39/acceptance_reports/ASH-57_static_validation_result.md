# ASH-57 Static Validation Result

- lib_brace_balance: PASS
- lib_bracket_balance: PASS
- lib_paren_balance: PASS
- lib_pub_mod: PASS
- lib_pub_use: PASS
- module_exists: PASS
- report_exists: PASS
- source_brace_balance: PASS
- source_bracket_balance: PASS
- source_paren_balance: PASS
- src_contains_ASH_57_PASS_THROUGH_STATUS: PASS
- src_contains_ASH_57_QUARANTINE_CANDIDATE_STATUS: PASS
- src_contains_ASH_57_QUARANTINE_GUARD_STATUS: PASS
- src_contains_ASH_57_QUARANTINE_REJECTED_STATUS: PASS
- src_contains_allow_artifact_delete_false: PASS
- src_contains_allow_artifact_rewrite_false: PASS
- src_contains_allow_current_pointer_change_false: PASS
- src_contains_allow_explicit_apply_commit_false: PASS
- src_contains_allow_quarantine_persistent_write_false: PASS
- src_contains_allow_quarantine_release_false: PASS
- src_contains_allow_registry_mutation_false: PASS
- src_contains_allow_runtime_attach_false: PASS
- test_brace_balance: PASS
- test_bracket_balance: PASS
- test_contains_ash_57_dry_run_rejected_record_quarantines_candidate: PASS
- test_contains_ash_57_failed_provided_smoke_evidence_quarantines_candidate: PASS
- test_contains_ash_57_low_delta_confidence_requires_manual_review_without_quarantine_by_default: PASS
- test_contains_ash_57_passes_through_when_risk_and_smoke_are_clean_without_enabling_apply: PASS
- test_contains_ash_57_quarantine_record_id_is_deterministic: PASS
- test_contains_ash_57_quarantines_when_hard_negative_risk_exceeds_threshold: PASS
- test_contains_ash_57_rejects_config_that_allows_quarantine_release: PASS
- test_contains_ash_57_rejects_prior_seal_violation_from_smoke_report: PASS
- test_contains_ash_57_smoke_plan_only_requires_manual_review_not_immediate_quarantine: PASS
- test_exists: PASS
- test_paren_balance: PASS

## Note
This environment does not provide cargo/rustc, so this is a static validation only. Run `cargo test -p ash_core ash_57 -- --nocapture` locally for Rust compilation and runtime test validation.
