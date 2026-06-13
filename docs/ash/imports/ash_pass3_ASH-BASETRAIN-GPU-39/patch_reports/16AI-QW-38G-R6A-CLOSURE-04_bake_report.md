# 16AI-QW-38G-R6A-CLOSURE-04 bake report

- Patch: 16AI-QW-38G-R6A-CLOSURE-04
- Name: Fixture JSON Integrity Repair / Static Receipt Parse Closure Seal
- Domain SSOT: en_to_ko_translation_subtitle_machine
- Static integrity status: PASS
- JSON parse failures: 4 -> 0
- Duplicate receipt keys: 4 -> 0
- Runtime decode executed: false
- Model forward executed: false
- Sampling executed: false
- Subtitle export executed: false
- Next: 16AI-QW-38G-R6A-BUILD-00

## Files changed by repair
- `meta.json` (replace_empty_json_with_explicit_unavailable_metadata)
- `infer_debug/probe_17A_native_base_ascii_A.json` (remove_utf8_bom_and_rewrite_canonical_json)
- `workspace/qw38g_r6a_r12i_r2_r1_static_validation_result.json` (escape_windows_powershell_path_backslashes)
- `workspace/qw38g_r6a_r12i_r2_static_validation_result.json` (escape_windows_powershell_path_backslashes)
- `workspace/qw38g_r6a_decode06_transition_guard_receipt.json` (replace_duplicate_receipt_aggregate_with_canonical_reference_index)
