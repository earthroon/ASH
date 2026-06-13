# 16AI-QW-38G-R6A-CLOSURE-04
## Fixture JSON Integrity Repair / Static Receipt Parse Closure Seal

status: PASS_STATIC_RECEIPT_FIXTURE_PARSE_CLOSURE
domain_ssot: en_to_ko_translation_subtitle_machine

depends_on:
  - 16AI-QW-38G-R6A-CLOSURE-03

json_checked_count: 1068
json_parse_failure_before: 4
closure03_reported_json_parse_failure_before: 2
extra_json_parse_failure_found_by_full_zip_scan: 2
json_parse_failure_after: 0

receipt_scan_scope: workspace *_receipt.json files only; historical reports/key_material/validation indices are evidence copies, not canonical active receipt registry
receipt_key_checked_count: 187
duplicate_receipt_key_before: 4
duplicate_receipt_key_after: 0
receipt_registry_unique: true

static_integrity_status: PASS
ready_for_run_decode: false
ready_for_export_sub: false

cargo_check_executed_count: 0
cargo_test_executed_count: 0
runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
subtitle_export_executed_count: 0

## Repaired files
- meta.json -> replace_empty_json_with_explicit_unavailable_metadata
- infer_debug/probe_17A_native_base_ascii_A.json -> remove_utf8_bom_and_rewrite_canonical_json
- workspace/qw38g_r6a_r12i_r2_r1_static_validation_result.json -> escape_windows_powershell_path_backslashes
- workspace/qw38g_r6a_r12i_r2_static_validation_result.json -> escape_windows_powershell_path_backslashes
- workspace/qw38g_r6a_decode06_transition_guard_receipt.json -> replace_duplicate_receipt_aggregate_with_canonical_reference_index

## Duplicate key resolution
- `workspace/qw38g_r6a_decode06_transition_guard_receipt.json` is no longer an embedded duplicate receipt list.
- Standalone DECODE-06 receipt files remain canonical.
- The aggregate path now stores canonical receipt references and a unique aggregate index receipt key.

## Backup handling
- Original repaired files are preserved under `workspace/closure_04_repair_backup/` with `.json.bak` suffix where needed, so full `*.json` scans remain parse-clean.

## Validation artifacts
- `workspace/closure_04_fixture_integrity_report.json`
- `workspace/closure_04_receipt_key_resolution_map.json`
- `workspace/closure_04_repair_log.json`
- `workspace/closure_04_static_validation_receipt.json`
- `workspace/closure_04_ad_hoc_static_validation.json`

## Mutation boundary

source_file_mutation_executed: false
json_autofix_executed: false
manual_static_repair_executed: true
runtime_decode_executed: false
model_forward_executed: false
sampling_executed: false
subtitle_export_executed: false

next_recommended_patch: 16AI-QW-38G-R6A-BUILD-00

canonical_receipt_key: q4sha256:8c313ecfc78798bb9e027b5123ea9c9c1ff130f965c0c35a616fe83bbdc3b23b
