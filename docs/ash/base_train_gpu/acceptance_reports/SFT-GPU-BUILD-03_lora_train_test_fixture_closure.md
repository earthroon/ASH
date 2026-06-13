# SFT-GPU-BUILD-03 Acceptance Report

## Scope
- check_layer_passed_before_build_03: true
- test_command_primary: cargo test -p lora_train lm_head_vocab_atlas -- --nocapture
- test_command_secondary: cargo test -p lora_train lm_head_runtime_delta_verify -- --nocapture
- sherpa_rs_sys_excluded_from_main_gpu_sft_check: true

## Dependency Closure
- tempfile_added_to_dev_dependencies: true
- runtime_dependency_pollution: false

## Test Helper Closure
- duplicate_make_target_runtime_summary_stub_fixed: true
- make_scorecard_stub_shared: default-based fixture closure applied via ModuleLoraScorecard::default()
- helper_duplication_avoided: true

## Pipeline Contract Imports
- RuntimeHealthCompact_imported: true
- BridgeExtractionRuntimeCompact_imported: true
- RunOutcomeSummary_imported: true
- SelectionGateDecision_imported: true
- TargetTrainingRuntimeSummary_imported: true
- orchestration_imports_restored: true
- hard_case_imports_restored: true

## Fixture Drift
- RuntimeHealthCompact_default_based: true
- StandardInferResult_default_based: true
- HardCaseSurfaceCompact_default_based: true
- ModuleLoraScorecard_default_based: true

## Manifest Schema Alignment
- target_outcome_records_path_used: compatibility alias retained for legacy test fixture intake; canonical latest path field remains present
- counterfactual_evaluations_path_used: compatibility alias retained for legacy test fixture intake; canonical latest path field remains present
- policy_adjustment_proposals_path_used: compatibility alias retained for legacy test fixture intake; canonical latest path field remains present
- canary_application_plans_path_used: compatibility alias retained for legacy test fixture intake; canonical latest path field remains present
- duplicate_governance_policy_version_removed: true
- duplicate_run_outcome_summary_path_removed: true

## Verification
- cargo test -p lora_train lm_head_vocab_atlas -- --nocapture: not executed in this container
- cargo test -p lora_train lm_head_runtime_delta_verify -- --nocapture: not executed in this container

## Result
- test_compile_passed: pending local cargo test
- tests_passed: pending local cargo test
- remaining_errors: unknown until local cargo test
- remaining_warnings: expected, warning cleanup out of scope
