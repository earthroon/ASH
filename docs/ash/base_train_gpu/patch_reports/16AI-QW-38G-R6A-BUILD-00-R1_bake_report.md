# 16AI-QW-38G-R6A-BUILD-00-R1 Bake Report

## Title
Cargo Environment Re-run / Missing Path Dependency Classification Seal

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Status
`BLOCKED_ENVIRONMENT`

## Execution Summary

| Field | Value |
|---|---:|
| cargo_available | `False` |
| rustc_available | `False` |
| cargo_metadata_executed | `False` |
| cargo_check_workspace_all_targets_executed | `False` |
| tokenizer_core_guard_tests_executed | `False` |
| decode_run_00_guard_chain_executed | `False` |
| false_cargo_check_claim | `False` |
| false_rust_test_claim | `False` |
| python_guard_substitution | `False` |

## Notes

- This patch performs Cargo environment re-run and missing path dependency classification.
- It does not modify decode, runtime, sampler, model, export, or rerank logic.
- If Cargo is unavailable, all Cargo/Rust execution claims remain false.
