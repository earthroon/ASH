# ASH-54 Static Validation Result

Overall: PASS

- module_exists: PASS
- module_brace_balance: PASS
- module_paren_balance: PASS
- module_bracket_balance: PASS
- test_exists: PASS
- test_brace_balance: PASS
- test_paren_balance: PASS
- test_bracket_balance: PASS
- lib_exists: PASS
- lib_brace_balance: PASS
- lib_paren_balance: PASS
- lib_bracket_balance: PASS
- report_exists: PASS
- status_const_present: PASS
- rejected_const_present: PASS
- no_apply_to_clone_seal: PASS
- no_registry_mutation_seal: PASS
- no_edge_mutation_seal: PASS
- no_path_mutation_seal: PASS
- original_registry_unchanged: PASS
- deterministic_plan_id: PASS
- path_cost_skip_no_remap: PASS
- entry_delta_kind_clone: PASS
- lib_pub_mod: PASS
- lib_pub_use: PASS
- test_ash_54_creates_registry_mutation_dry_run_without_mutation: PASS
- test_ash_54_rejects_registry_version_mismatch: PASS
- test_ash_54_records_missing_edge_as_record_level_rejection: PASS
- test_ash_54_skips_path_cost_candidate_without_silent_edge_remap: PASS
- test_ash_54_accepts_hard_negative_demotion_candidate_without_weight_increase: PASS
- test_ash_54_rejects_apply_and_mutation_flags: PASS
- test_ash_54_dry_run_plan_and_record_ids_are_deterministic: PASS

## Compile
- cargo_available: FAIL
- rustc_available: FAIL
- note: Compile tests were not executed in this environment; static file/contract validation only.
