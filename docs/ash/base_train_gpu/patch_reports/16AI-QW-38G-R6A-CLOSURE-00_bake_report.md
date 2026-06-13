# 16AI-QW-38G-R6A-CLOSURE-00 Bake Report

## Decode Chain Freeze / Receipt Manifest Seal

status: PASS_STATIC_DECODE_CHAIN_FREEZE_MANIFEST_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
base: ash_pass3_16AI-QW-38G-R6A-DECODE-26_reviewer_assignment_commit_approved_internal_assignment_ledger_seal_baked.zip

## Added modules

- crates/ash_core/src/decode_chain_freeze_policy.rs
- crates/ash_core/src/decode_patch_manifest.rs
- crates/ash_core/src/decode_receipt_chain_index.rs
- crates/ash_core/src/decode_fixture_index.rs
- crates/ash_core/src/decode_module_index.rs
- crates/ash_core/src/decode_acceptance_report_index.rs
- crates/ash_core/src/decode_chain_freeze_receipt.rs
- crates/ash_core/src/decode_chain_freeze_stub.rs

## Added workspace artifacts

- workspace/qw38g_r6a_closure00_decode_chain_freeze_policy.json
- workspace/qw38g_r6a_closure00_decode_patch_manifest.json
- workspace/qw38g_r6a_closure00_decode_receipt_chain_index.json
- workspace/qw38g_r6a_closure00_decode_fixture_index.json
- workspace/qw38g_r6a_closure00_decode_module_index.json
- workspace/qw38g_r6a_closure00_decode_acceptance_report_index.json
- workspace/qw38g_r6a_closure00_known_unverified_status.json
- workspace/qw38g_r6a_closure00_decode_chain_freeze_manifest_receipt.json
- workspace/qw38g_r6a_closure00_decode_chain_freeze_key_material.json
- workspace/qw38g_r6a_closure00_decode_chain_freeze_report.json

## Seal

- first_decode_patch_id: 16AI-QW-38G-R6A-DECODE-04
- last_decode_patch_id: 16AI-QW-38G-R6A-DECODE-26
- decode_patch_count: 23
- decode_line_frozen: true
- allow_new_decode_patch_after_freeze: false
- deterministic_receipt_key: q4sha256:b4611f3cee926214762e2b3546778b5011b3f609788595c50a57e7b5afaf2a7a

## Known boundary

cargo/rustc compile verification was not executed in this patch. Runtime decode, model forward, sampling, subtitle export, external queue mutation, external reviewer assignment, and production profile mutation remain false.
