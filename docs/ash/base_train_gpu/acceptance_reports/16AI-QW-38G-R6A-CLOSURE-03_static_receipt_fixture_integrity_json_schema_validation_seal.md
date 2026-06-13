# 16AI-QW-38G-R6A-CLOSURE-03
## Static Receipt Fixture Integrity / JSON Schema Validation Seal

status: PASS_OBSERVED_STATIC_RECEIPT_FIXTURE_INTEGRITY_FAILURE_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine

depends_on:
  - 16AI-QW-38G-R6A-CLOSURE-00
  - 16AI-QW-38G-R6A-CLOSURE-01
  - 16AI-QW-38G-R6A-CLOSURE-02

static_receipt_fixture_integrity_policy_created_count: 1
static_fixture_inventory_created_count: 1
json_parse_validation_index_created_count: 1
required_field_validation_index_created_count: 1
receipt_key_validation_index_created_count: 1
acceptance_count_consistency_index_created_count: 1
schema_drift_index_created_count: 1
static_receipt_fixture_integrity_receipt_created_count: 1
deterministic_key_created_count: 1

total_fixture_count: 1857
json_checked_count: 654
json_parse_failed_count: 2

receipt_checked_count: 151
missing_required_field_count: 0

receipt_key_missing_count: 0
duplicate_receipt_key_count: 4

acceptance_count_mismatch_count: 0
domain_ssot_mismatch_count: 0

blocking_drift_count: 2
non_blocking_drift_count: 4

static_fixture_integrity_passed: false
ready_for_run_decode: false
ready_for_export_sub: false

source_file_mutation_executed_count: 0
json_autofix_executed_count: 0
acceptance_report_autofix_executed_count: 0

cargo_check_executed_count: 0
runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
subtitle_export_executed_count: 0

external_queue_mutation_executed_count: 0
external_reviewer_assignment_executed_count: 0
production_profile_mutation_executed_count: 0

next_recommended_patch:
  16AI-QW-38G-R6A-FIX-FIXTURE-00
  Static Fixture Integrity Repair / Minimal JSON Receipt Patch Seal

duplicate_receipt_key_count_observed: 4
canonical_receipt_key: q4sha256:d21eabc9cd2e7589b6e118f72382ade0799ea27775a584b9c3053a3ce6ffdded

## Observed parse failures
- workspace/qw38g_r6a_r12i_r2_r1_static_validation_result.json line=20 column=28 error_hash=sha256:8c87fb3cba09cf0f0acb87275d9ec1e11d89757b620dc21c7561650f8f52fd0c
- workspace/qw38g_r6a_r12i_r2_static_validation_result.json line=22 column=28 error_hash=sha256:039fe540adf1169d53296a8705d055c32a5b9cad6dd56e37b378f09883ba19b7

## Mutation boundary

source_file_mutation_executed: false
json_autofix_executed: false
acceptance_report_autofix_executed: false
runtime_decode_executed: false
model_forward_executed: false
sampling_executed: false
subtitle_export_executed: false
